# -*- coding: utf-8 -*-
"""执行前规则审查（beta1）。

判定顺序与 rule_id 口径沿用 0.2：
  rule_id = 本记录的决定性检查项 id（最先失败的项；无失败取最后通过的项）。
五值决策：ALLOW / DENY / REQUIRE_APPROVAL / WARNING / ERROR。
"""
import io
import json
import os
import re
import time

from . import identity, request

_RULES = None


def load_rules(path):
    global _RULES
    with io.open(path, encoding="utf-8") as f:
        _RULES = json.load(f)
    return _RULES


def rules():
    return _RULES


class _Checks(object):
    def __init__(self):
        self.items = []

    def add(self, rid, name, result, detail=""):
        self.items.append({"id": rid, "name": name, "result": result, "detail": str(detail)})

    def rule_id(self):
        for it in self.items:
            if it["result"] == "fail":
                return it["id"]
        for it in self.items:
            if it["result"] == "warn":
                return it["id"]
        passed = [it["id"] for it in self.items if it["result"] == "pass"]
        return passed[-1] if passed else "RULESET"


def _norm_target(target):
    t = str(target or "").strip().replace("\\", "/")
    if not t:
        raise ValueError("target 为空")
    if re.match(r"^[A-Za-z]:", t) or t.startswith("//") or t.startswith("/"):
        raise ValueError("target 不得是绝对路径或 UNC：%s" % t)
    parts = [p for p in t.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise ValueError("target 不得含 ..：%s" % t)
    return "/".join(parts)


def _under(root, path):
    root = str(root or "").strip().replace("\\", "/").strip("/")
    if not root:
        return False
    return path == root or path.startswith(root + "/")


def _nonce_ok(req, cfg, now):
    path = cfg["nonces"]
    data = {}
    if os.path.isfile(path):
        try:
            with io.open(path, encoding="utf-8") as f:
                data = json.load(f)
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


def run(req, cfg, now=None):
    """返回 {decision, error_code, rule_id, checks}。异常一律 ERROR，绝不 ALLOW。"""
    now = time.time() if now is None else now
    c = _Checks()
    try:
        agent = identity.AgentRegistry(cfg["agents"]).get(req.get("agent_id"))
        active = bool(agent) and agent.get("status") == "active"
        c.add("R0.1", "identity_known", "pass" if active else "fail",
              "agent=%s status=%s" % (req.get("agent_id"), (agent or {}).get("status", "None")))
        if active:
            import hmac
            ok = hmac.compare_digest(request.sign(agent["secret"], req), str(req.get("sig") or ""))
        else:
            ok = False
        c.add("R0.2", "signature_valid", "pass" if ok else "fail", "HMAC-SHA256")
        if ok:
            n_ok, n_why = _nonce_ok(req, cfg, now)
        else:
            n_ok, n_why = False, "签名不通过，未消费 nonce"
        c.add("R0.3", "nonce_fresh", "pass" if n_ok else "fail", n_why or "nonce 未用且 ts 在窗口内")

        cap = identity.AgentRegistry.capability(agent, req.get("capability"))
        c.add("R0.4", "capability_declared", "pass" if cap else "fail",
              "capability=%s" % req.get("capability"))
        actions = list((cap or {}).get("actions") or [])
        act_ok = req.get("action_type") in actions
        c.add("R0.5", "action_allowed", "pass" if act_ok else "fail",
              "action=%s allowed=%s" % (req.get("action_type"), ",".join(actions)))

        norm = ""
        try:
            norm = _norm_target(req.get("target"))
            c.add("R0.6", "target_form", "pass", "target=%s" % norm)
        except ValueError as e:
            c.add("R0.6", "target_form", "fail", str(e))

        denied = set(cfg.get("denied_zones") or [])
        zone = norm.split("/")[0] if norm else ""
        c.add("R0.7", "denied_zone", "pass" if zone not in denied else "fail",
              "zone=%s denied=%s" % (zone, ",".join(sorted(denied))))

        in_scope = bool(norm) and _under((cap or {}).get("root"), norm)
        c.add("R0.8", "capability_scope", "pass" if in_scope else "fail",
              "root=%s target=%s" % ((cap or {}).get("root", ""), norm))

        exists = bool(norm) and os.path.exists(os.path.join(cfg.get("base_dir") or "", norm))
        warn = str(req.get("action_type")) == "file.delete" and not exists
        c.add("R0.9", "precondition", "warn" if warn else "pass",
              "target_exists=%s" % exists)

        need = bool((cap or {}).get("approval")) or req.get("action_type") in (cfg.get("approval_actions") or [])
        c.add("R0.10", "approval_required", "warn" if need else "pass",
              "capability.approval=%s" % bool((cap or {}).get("approval")))

        c.add("R0.11", "within_grant", "pass",
              "身份／能力／路径／范围全部通过")

        # 决策优先级：失败项按 R0.1→R0.10 顺序取第一个；无失败再看警告。
        fails = [it for it in c.items if it["result"] == "fail"]
        warns = [it for it in c.items if it["result"] == "warn"]
        rule_map = {r["rule_id"]: r for r in (rules() or {}).get("rules", [])}
        if fails:
            first = fails[0]
            spec = rule_map.get(first["id"], {})
            return {"decision": spec.get("decision", "DENY"),
                    "error_code": spec.get("error_code", "REVIEW_FAIL"),
                    "rule_id": first["id"], "checks": c.items}
        if warns:
            first = warns[0]
            spec = rule_map.get(first["id"], {})
            return {"decision": spec.get("decision", "WARNING"),
                    "error_code": spec.get("error_code", ""),
                    "rule_id": first["id"], "checks": c.items}
        return {"decision": "ALLOW", "error_code": "",
                "rule_id": c.rule_id(), "checks": c.items}
    except Exception as e:
        c.add("R0.99", "internal_error", "fail", "%s: %s" % (type(e).__name__, e))
        return {"decision": "ERROR", "error_code": "INTERNAL_ERROR",
                "rule_id": "R0.99", "checks": c.items}
