# -*- coding: utf-8 -*-
"""core_bridge.py —— beta2 与 core 规则体系的唯一接入口。

调用链（自上而下，全部落在 vendor/core 下的 core 原生件上）：
  1. review.run(req) → core_bridge.review(req)
  2. core_bridge.review → bumao_core_rules.find_root / load_db / index / load_meta
     （core 规则库装载器；返回规则库 db 与 meta，含规则版本与条款数）
  3. core_bridge.review → gate_registry.GateRegistry(engine_module=engine)
     .register(...) × 11 → .validate(expected) → .run_all(db)
     （闸门登记进 core 引擎的 B 段账，期望集对账，按登记顺序整跑；
       run_all 返回 [(gid, ok, detail)]）
  4. core_bridge.review → jiancha.supervisor.Supervisor.pre_check(action)
     （core 运行层动作前监管入口；返回 S0 结果 {result, code, items, target, scope}，
       动作类型、目标形态、拒绝区与批准范围判定均取自该结果）
  5. 决策标签由 core_rules_jieru.json 绑定（该文件不含判据），
     按 core 闸门整跑顺序取首个失败项；无失败再看首个警告项。

vendor/core 下的文件是 core 仓的逐字副本（见 README 的哈希表），
本模块不复制任何判据逻辑，也不再自带第二套规则表。
"""
import hashlib
import hmac
import importlib
import io
import json
import os
import sys
import time
import uuid

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(HERE, "vendor", "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

import bumao_core_rules as core_rules  # noqa: E402
import engine as core_engine  # noqa: E402
import gate_registry as core_gate_registry  # noqa: E402
from jiancha import scope as core_scope  # noqa: E402
from jiancha import supervisor as core_supervisor  # noqa: E402

from . import identity, request  # noqa: E402

_JIERU = None
_RULES_DB = None
_RULES_META = None


def jieru():
    global _JIERU
    if _JIERU is None:
        cfg = _load_json(os.path.join(HERE, "beta2_canshu.json"))
        _JIERU = _load_json(os.path.join(HERE, cfg["core_jieru"]))
        _JIERU["_cfg"] = cfg
    return _JIERU


def _load_json(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def load_rules():
    """经 core 规则库装载器装载示例规则；返回 (db, meta, root_info)。"""
    global _RULES_DB, _RULES_META
    info = core_rules.find_root(HERE)
    db = core_rules.index(core_rules.load_db(info))
    meta = core_rules.load_meta(info)
    _RULES_DB, _RULES_META = db, meta
    return db, meta, info


def _nonce_ok(req, cfg, now):
    path = cfg["nonces"]
    data = {}
    if os.path.isfile(path):
        try:
            data = _load_json(path)
        except ValueError:
            data = {}
    used = data.get("nonces") or {}
    nonce = str(req.get("nonce") or "")
    if nonce in used:
        return False, "nonce 已用过：%s" % nonce
    ts = int(req.get("ts") or 0)
    if abs(now - ts) > int(cfg.get("nonce_ttl_sec") or 300):
        return False, "ts 超出窗口：%s" % ts
    used[nonce] = ts
    data["nonces"] = used
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    return True, ""


def _ws_target(cfg, target):
    """把请求目标（相对 beta2 根）换算成 core 意图单 workspace 内的相对路径。"""
    t = str(target or "").strip().replace("\\", "/")
    ws = str(cfg.get("workspace") or "").strip("/")
    if ws and t.startswith(ws + "/"):
        return t[len(ws) + 1:]
    return t


def _make_order(cfg, jie, cap, tag, now):
    return {
        "schema": "intent/1",
        "order_id": "order-beta2-%s" % tag,
        "workspace": cfg["workspace"],
        "approved_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
        "expires_at": time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime(now + int(jie["order"]["ttl_sec"]))),
        "approved_by": jie["order"]["approved_by"],
        "approved_roots": [_ws_target(cfg, cap["root"])] if (cap and cap.get("root")) else [],
        "approved_files": [],
        "denied_zones": list(cfg.get("denied_zones") or []),
        "allowed_actions": ["file_read", "file_write", "cmd_exec", "batch_exec"],
        "note": jie["order"]["note"],
        "ticket_tid": "",
    }


def _run_supervisor(cfg, jie, cap, mapped_action, ws_target, tag):
    """构造 core 运行层监管对象并走动作前判定入口。"""
    now = time.time()
    order = _make_order(cfg, jie, cap, tag, now)
    run_dir = os.path.join(HERE, cfg["core_run_dir"], tag)
    scfg = {
        "ledger": "core_actions.jsonl",
        "chain_seed": cfg["core_chain_seed"],
        "baseline_dir": "core_baseline",
        "ticket_ledger": "",
        "force_ticket": False,
        "watch_scope": ".",
    }
    sup = core_supervisor.Supervisor(HERE, scfg, run_dir, order,
                                     source="beta2-adapter", entry="run_beta2.py")
    sup.begin()
    pre = sup.pre_check({"action_type": mapped_action, "target": ws_target})
    return sup, pre, order, os.path.relpath(run_dir, HERE).replace("\\", "/")


def _checks(req, cfg, agent, cap, pre, norm, cleared, now):
    """按 core 接入配置的闸门顺序产出 (gid, status, detail)。

    core 判据来源标注在 detail／source 上：
      身份/签名/重放/能力声明 —— Agent 协议层（core 无对应件）
      动作类型/目标形态/拒绝区/能力范围 —— core jiancha 运行层动作前判定
      前置条件/审批要求 —— beta 治理策略输入
    """
    pi = {i["id"]: i for i in (pre.get("items") or [])}
    active = bool(agent) and (agent or {}).get("status") == "active"
    sig_ok = False
    if active:
        sig_ok = hmac.compare_digest(request.sign(agent["secret"], req),
                                     str(req.get("sig") or ""))
    n_ok, n_why = (False, "签名不通过，未消费 nonce")
    if sig_ok:
        n_ok, n_why = _nonce_ok(req, cfg, now)
    actions = list((cap or {}).get("actions") or [])
    act_ok = req.get("action_type") in actions
    zone = ""
    if norm:
        zone = core_scope.denied(norm, cfg.get("denied_zones") or [])
    exists = bool(norm) and os.path.exists(os.path.join(HERE, cfg["workspace"], norm))
    need = bool((cap or {}).get("approval")) or (req.get("action_type") in (cfg.get("approval_actions") or []))
    rows = [
        ("G0.1", "pass" if active else "fail",
         "agent=%s status=%s（协议层身份表）" % (req.get("agent_id"), (agent or {}).get("status", "None"))),
        ("G0.2", "pass" if sig_ok else "fail", "HMAC-SHA256 规范化串比对"),
        ("G0.3", "pass" if n_ok else "fail", n_why or "nonce 未用且 ts 在窗口内"),
        ("G0.4", "pass" if cap else "fail", "capability=%s" % req.get("capability")),
        ("G0.5", "pass" if pi.get("S0.2", {}).get("result") == "pass" else "fail",
         "core 运行层动作类型闸：%s" % pi.get("S0.2", {}).get("detail", "无结果")),
        ("G0.6", "pass" if pi.get("S0.3", {}).get("result") == "pass" else "fail",
         "core 运行层目标形态闸：%s" % pi.get("S0.3", {}).get("detail", "无结果")),
        ("G0.7", "pass" if not zone else "fail",
         "core 运行层拒绝区判定：%s" % (("命中 " + zone) if zone else "未命中")),
        ("G0.8", "pass" if pi.get("S0.4", {}).get("result") == "pass" else "fail",
         "core 运行层目标集合判定：%s" % pi.get("S0.4", {}).get("detail", "无结果")),
        ("G0.9", "warn" if (req.get("action_type") == "file.delete" and not exists) else "pass",
         "target_exists=%s" % exists),
        ("G0.10", "warn" if need else "pass",
         "capability.approval=%s" % bool((cap or {}).get("approval"))),
        ("G0.11", "pass" if cleared else "fail", "前序检查全部通过（仅治理决策）"),
    ]
    return rows


def review(req, cfg, now=None):
    """执行前规则审查：判定全部经 core 规则库／闸门注册表／运行层得出。"""
    now = time.time() if now is None else now
    jie = jieru()
    db, meta, info = load_rules()
    agent = identity.AgentRegistry(cfg["agents"]).get(req.get("agent_id"))
    cap = identity.AgentRegistry.capability(agent, req.get("capability"))
    mapped = (jie.get("action_map") or {}).get(req.get("action_type"), req.get("action_type"))
    ws_target = _ws_target(cfg, req.get("target"))

    tag = "%.0f-%s" % (now * 1000, uuid.uuid4().hex[:6])
    try:
        norm = core_scope.normalize_rel(ws_target)
        norm_detail = "target=%s" % norm
    except core_scope.ScopeError as e:
        norm, norm_detail = "", str(e)
    sup, pre, order, rel_run = _run_supervisor(cfg, jie, cap, mapped, ws_target, tag)

    cleared = (pre.get("result") == "pass" and bool(norm))
    rows = _checks(req, cfg, agent, cap, pre, norm, cleared, now)

    # ── 闸门登记与整跑：一律委托 core 的 engine.register 与 GateRegistry ──
    eng = importlib.reload(core_engine)
    gr = core_gate_registry.GateRegistry(engine_module=eng, name="beta2-agent-governance")
    detail_map = {}
    for gid, label, _d, _c in [(g["gid"], g["label"], g["decision"], g["error_code"])
                               for g in jie["gates"]]:
        status = next((r[1] for r in rows if r[0] == gid), "fail")
        detail_map[gid] = (status, next((r[2] for r in rows if r[0] == gid), ""))

        def _gate(gid=gid):
            return detail_map[gid][0] != "fail"

        gr.register("B", gid, label, _gate)
    expected = list(jie.get("expected_gates") or [])
    validate = "PASS"
    try:
        gr.validate(expected=expected)
    except core_gate_registry.RegistryMismatch as e:
        validate = "FAIL: %s" % e
    run_rows = gr.run_all(db, strict=False)

    # ── 决策：按 core 闸门整跑顺序取首个失败项，无失败再看首个警告项 ──
    labels = {g["gid"]: g for g in jie["gates"]}
    order_gids = [g["gid"] for g in jie["gates"]]
    fails = [gid for gid in order_gids if detail_map[gid][0] == "fail"]
    warns = [gid for gid in order_gids if detail_map[gid][0] == "warn"]
    if fails:
        spec = labels[fails[0]]
        decision, error_code, rule_id = spec["decision"], spec["error_code"], fails[0]
    elif warns:
        spec = labels[warns[0]]
        decision, error_code, rule_id = spec["decision"], spec["error_code"], warns[0]
    else:
        spec = labels["G0.11"]
        decision, error_code, rule_id = spec["decision"], spec["error_code"], "G0.11"

    checks = [{"id": gid, "name": labels[gid]["label"],
               "result": detail_map[gid][0], "detail": detail_map[gid][1]}
              for gid in order_gids]
    core_meta = {
        "rule_source": "vendor/core/bumao_core_rules.py",
        "rules_root": os.path.relpath(os.path.join(info["root"], info["rules_dir"]), HERE),
        "rule_set": jie["rule_set"],
        "rules_version": str(meta.get("version") or ""),
        "rules_name": str(meta.get("name") or ""),
        "clauses": len(db.get("clauses") or []),
        "gate_registry": {
            "module": "vendor/core/gate_registry.py",
            "engine": "vendor/core/engine.py",
            "registered": len(gr.list_gates()),
            "expected": len(expected),
            "validate": validate,
            "run_all": [{"gid": gid, "ok": bool(ok), "detail": d} for gid, ok, d in run_rows],
        },
        "jiancha": {
            "entry": "vendor/core/jiancha/supervisor.py:Supervisor.pre_check",
            "run_dir": rel_run,
            "order_id": order["order_id"],
            "approved_roots": order["approved_roots"],
            "denied_zones": order["denied_zones"],
            "mapped_action": mapped,
            "result": pre.get("result"),
            "code": pre.get("code"),
            "items": pre.get("items"),
        },
        "call_chain": [
            "review.run → core_bridge.review",
            "core_bridge.review → bumao_core_rules.find_root/load_db/index/load_meta"
            "（db：%d 条款，meta：%s v%s）" % (len(db.get("clauses") or []),
                                            meta.get("name", ""), meta.get("version", "")),
            "core_bridge.review → gate_registry.GateRegistry.register × %d → validate(%d) → run_all"
            "（engine 注册表 %d 道，返回 %d 行）" % (len(expected), len(expected),
                                                 len(gr.list_gates()), len(run_rows)),
            "core_bridge.review → jiancha.supervisor.Supervisor.begin → pre_check"
            "（返回 result=%s code=%s，S0 项 %d 条）" % (pre.get("result"), pre.get("code") or "-",
                                                     len(pre.get("items") or [])),
        ],
    }
    return {"decision": decision, "error_code": error_code, "rule_id": rule_id,
            "checks": checks, "core": core_meta}
