# -*- coding: utf-8 -*-
"""Agent 操作证据记录（beta1）。

账本与四外键直接复用 0.2：vendor/ledger.py 为 0.2 jiancha/ledger.py 的逐字副本
（sha256 CFA2BD82DD1AED2BE07799E8CB2A20D371E02146B26A5E11538CABFD764519D8）。
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(_HERE, "vendor") not in sys.path:
    sys.path.insert(0, os.path.join(_HERE, "vendor"))
import ledger as _ledger  # noqa: E402

from . import request  # noqa: E402


def make_ledger(cfg):
    return _ledger.ActionLedger(os.path.join(_HERE, cfg["ledger"]), cfg["chain_seed"])


def new_op_id():
    return "op-%s-%d-%s" % (time.strftime("%Y%m%dT%H%M%S"), os.getpid(),
                            __import__("uuid").uuid4().hex[:6])


def record(cfg, led, req, agent, result, exception="", source="demo",
           op_id=None, run_id=None):
    """追加一条证据记录；返回落盘后的记录。"""
    seq = led.next_seq()
    approval_state = "pending" if result.get("decision") == "REQUIRE_APPROVAL" else "n/a"
    rec = {
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ts": time.time(),
        "seq": seq,
        # —— 四外键（对齐 0.2 票链口径）——
        "op_id": op_id or _ledger.current_op_id(),
        "run_id": run_id or _ledger.current_run_id(),
        "rule_id": result.get("rule_id", ""),
        "error_code": result.get("error_code", ""),
        # —— Agent 身份与请求 ——
        "agent_id": str(req.get("agent_id") or ""),
        "agent_status": (agent or {}).get("status", "missing"),
        "capability": str(req.get("capability") or ""),
        "action_type": str(req.get("action_type") or ""),
        "target": str(req.get("target") or ""),
        "request_sha256": request.request_sha256(req) if isinstance(req, dict) else "",
        # —— 规则与决策 ——
        "rule_set": cfg.get("rule_set", ""),
        "decision": result.get("decision", "ERROR"),
        "approval": {"state": approval_state, "by": "", "at": ""},
        "exception": exception,
        "checks": result.get("checks", []),
        "source": source,
    }
    return led.append(rec)


def approve(cfg, led, op_id, by, decision="approved", note=""):
    """人工审批结果：另追加一条记录，原记录不回改。"""
    return led.append({
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ts": time.time(),
        "seq": led.next_seq(),
        "op_id": op_id,
        "run_id": _ledger.current_run_id(),
        "rule_id": "R0.10",
        "error_code": "" if decision == "approved" else "APPROVAL_REJECTED",
        "agent_id": "",
        "capability": "",
        "action_type": "approval",
        "target": op_id,
        "request_sha256": "",
        "rule_set": cfg.get("rule_set", ""),
        "decision": decision,
        "approval": {"state": decision, "by": by,
                     "at": time.strftime("%Y-%m-%d %H:%M:%S"), "note": note},
        "exception": "",
        "checks": [],
        "source": "approval",
    })
