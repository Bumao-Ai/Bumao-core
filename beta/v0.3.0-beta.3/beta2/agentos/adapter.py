# -*- coding: utf-8 -*-
"""标准 Agent Adapter（beta2）。

示例 Agent 只能经本 Adapter 提交：Adapter 负责
  请求转换（外部信封 → req/1 统一请求）
  响应转换（治理结论 → 统一响应体）
  身份映射（外部 agent_ref ↔ 内部 agent_id，落盘 run/identity_map.json）
  错误处理（任何异常都转成 ERROR 响应，不抛给 Agent 侧）
  接入状态检测（core 模块、规则库、闸门期望集、身份映射、账本可写）

Adapter 内部才调用 request.build；Agent 侧不直连。
"""
import io
import json
import os
import time

from . import request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIELDS = ("schema", "vendor", "agent_ref", "op", "target", "params", "capability", "reason")


class AdapterError(Exception):
    def __init__(self, code, detail=""):
        self.code = str(code or "ADAPTER_ERROR")
        self.detail = detail or self.code
        Exception.__init__(self, self.detail)


def _load(path):
    if not os.path.isfile(path):
        return {"schema": "identity_map/1", "mappings": {}}
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)


class StandardAdapter:
    def __init__(self, cfg, registry, pipeline):
        self.cfg = cfg
        self.reg = registry
        self.pipeline = pipeline
        self.map_path = os.path.join(HERE, cfg["identity_map"])
        with io.open(os.path.join(HERE, cfg["core_jieru"]), encoding="utf-8") as f:
            self.jieru = json.load(f)
        self.action_map = self.jieru.get("action_map") or {}

    # ---------------- 身份映射 ----------------
    def bind(self, external_ref, agent_id, display="", capabilities=None):
        """登记 Agent 并建立外部身份映射；返回登记记录（含一次性 secret）。"""
        rec = self.reg.register(agent_id, display, capabilities)
        data = _load(self.map_path)
        data.setdefault("mappings", {})[str(external_ref)] = {
            "agent_id": rec["agent_id"],
            "bound_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        _save(self.map_path, data)
        return rec

    def resolve(self, external_ref):
        return ((_load(self.map_path).get("mappings") or {}).get(str(external_ref)) or {}).get("agent_id")

    def unbind(self, external_ref):
        data = _load(self.map_path)
        gone = (data.get("mappings") or {}).pop(str(external_ref), None)
        _save(self.map_path, data)
        return gone

    def mappings(self):
        return _load(self.map_path).get("mappings") or {}

    # ---------------- 请求转换 ----------------
    def transform(self, envelope):
        if not isinstance(envelope, dict):
            raise AdapterError("ADAPTER_BAD_ENVELOPE", "外部请求不是对象")
        missing = [k for k in ("schema", "agent_ref", "op", "target") if k not in envelope]
        if missing:
            raise AdapterError("ADAPTER_BAD_ENVELOPE", "外部请求缺字段：%s" % ",".join(missing))
        if envelope.get("schema") != "agent_ext/1":
            raise AdapterError("ADAPTER_BAD_ENVELOPE",
                               "schema=%r 应为 'agent_ext/1'" % envelope.get("schema"))
        ext = str(envelope.get("agent_ref") or "")
        agent_id = self.resolve(ext)
        if not agent_id:
            raise AdapterError("ADAPTER_UNMAPPED_IDENTITY", "外部身份未映射：%s" % ext)
        agent = self.reg.get(agent_id)
        if not agent:
            raise AdapterError("ADAPTER_UNKNOWN_AGENT", "映射到的 Agent 不存在：%s" % agent_id)
        cap_id = str(envelope.get("capability") or "")
        if not cap_id:
            caps = agent.get("capabilities") or []
            cap_id = caps[0]["id"] if caps else ""
        params = dict(envelope.get("params") or {})
        if envelope.get("reason"):
            params["reason"] = str(envelope["reason"])
        req = request.build(agent_id, cap_id, str(envelope["op"]), str(envelope["target"]),
                            agent["secret"], params=params)
        return req, {"external_ref": ext, "vendor": str(envelope.get("vendor") or "")}

    # ---------------- 响应转换 ----------------
    def response(self, result, record, meta):
        return {
            "schema": "agent_resp/1",
            "decision": result.get("decision", "ERROR"),
            "allowed": result.get("decision") == "ALLOW",
            "error_code": result.get("error_code", ""),
            "rule_id": result.get("rule_id", ""),
            "op_id": record.get("op_id"),
            "identity": {"external_ref": meta.get("external_ref", ""),
                         "agent_id": record.get("agent_id", "")},
            "governance": {"rule_set": record.get("rule_set", ""),
                           "rules_version": record.get("rules_version", ""),
                           "core": result.get("core", {})},
            "receipt": record.get("receipt"),
            "receipt_note": record.get("receipt_note", ""),
        }

    def error_response(self, code, detail):
        return {"schema": "agent_resp/1", "decision": "ERROR", "allowed": False,
                "error_code": code, "rule_id": "ADAPTER", "op_id": None,
                "detail": detail, "receipt": None, "receipt_note": "请求未进入治理内核"}

    # ---------------- 提交入口（Agent 唯一可用入口） ----------------
    def submit(self, envelope, receipt=None):
        try:
            req, meta = self.transform(envelope)
            result, record = self.pipeline(req, receipt)
            return self.response(result, record, meta)
        except AdapterError as e:
            return self.error_response(e.code, e.detail)
        except Exception as e:
            return self.error_response("ADAPTER_ERROR", "%s: %s" % (type(e).__name__, e))

    # ---------------- 接入状态检测 ----------------
    def status(self):
        from . import core_bridge
        checks = []
        try:
            db, meta, _info = core_bridge.load_rules()
            checks.append({"id": "core_rules_db", "result": "pass",
                           "detail": "%s v%s，%d 条款" % (meta.get("name", ""), meta.get("version", ""),
                                                       len(db.get("clauses") or []))})
        except Exception as e:
            checks.append({"id": "core_rules_db", "result": "fail", "detail": "%r" % e})
        want = list(self.jieru.get("expected_gates") or [])
        try:
            import gate_registry as gr
            checks.append({"id": "gate_registry", "result": "pass",
                           "detail": "core 闸门注册表可导入；期望闸门 %d 道" % len(want)})
        except Exception as e:
            checks.append({"id": "gate_registry", "result": "fail", "detail": "%r" % e})
        mapped = self.mappings()
        checks.append({"id": "identity_map", "result": "pass" if mapped else "fail",
                       "detail": "%d 条外部身份映射" % len(mapped)})
        checks.append({"id": "request_schema", "result": "pass",
                       "detail": "req/1 字段 %d 个" % len(request.FIELDS)})
        ok = all(c["result"] == "pass" for c in checks)
        return {"schema": "adapter_status/1", "state": "ready" if ok else "degraded",
                "at": time.strftime("%Y-%m-%d %H:%M:%S"), "checks": checks}
