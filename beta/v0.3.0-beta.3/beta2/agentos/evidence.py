# -*- coding: utf-8 -*-
"""Agent 操作证据记录（beta2）。

账本与四外键直接复用 0.2：vendor/ledger.py 为 0.2 jiancha/ledger.py 的逐字副本。

三个概念分开写，不合并：
  治理请求（request）：Agent 提交的完整请求，含全量 params 与请求哈希；
  治理决策（decision）：规则审查结论，只是「允许/拒绝/需审批」，不代表执行成功；
  实际执行结果（receipt）：接入方执行后回传的回执；未提供时明确写 null 并写原因。
"""
import os
import sys
import time
import uuid

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(_HERE, "vendor") not in sys.path:
    sys.path.insert(0, os.path.join(_HERE, "vendor"))
import ledger as _ledger  # noqa: E402

from . import request  # noqa: E402

RECEIPT_ABSENT = "接入方未提供执行回执；治理决策不等于实际执行结果"


def make_ledger(cfg):
    return _ledger.ActionLedger(os.path.join(_HERE, cfg["ledger"]), cfg["chain_seed"])


def new_op_id():
    return "op-%s-%d-%s" % (time.strftime("%Y%m%dT%H%M%S"), os.getpid(),
                            uuid.uuid4().hex[:6])


def record(cfg, led, req, agent, result, exception="", source="demo",
           op_id=None, run_id=None, receipt=None):
    """追加一条治理请求记录；返回落盘后的记录。"""
    seq = led.next_seq()
    approval_state = "pending" if result.get("decision") == "REQUIRE_APPROVAL" else "n/a"
    params = dict(req.get("params") or {}) if isinstance(req, dict) else {}
    req_obj = {
        "schema": str(req.get("schema") or ""),
        "agent_id": str(req.get("agent_id") or ""),
        "capability": str(req.get("capability") or ""),
        "action_type": str(req.get("action_type") or ""),
        "target": str(req.get("target") or ""),
        "params": params,
        "nonce": str(req.get("nonce") or ""),
        "ts": req.get("ts"),
        "sig": str(req.get("sig") or ""),
        "request_sha256": request.request_sha256(req) if isinstance(req, dict) else "",
    }
    core = result.get("core") or {}
    rec = {
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ts": time.time(),
        "seq": seq,
        "kind": "governance_request",
        # —— 四外键（对齐 0.2 票链口径）——
        "op_id": op_id or _ledger.current_op_id(),
        "run_id": run_id or _ledger.current_run_id(),
        "rule_id": result.get("rule_id", ""),
        "error_code": result.get("error_code", ""),
        # —— 治理请求 ——
        "agent_id": str(req.get("agent_id") or ""),
        "agent_status": (agent or {}).get("status", "missing"),
        "capability": str(req.get("capability") or ""),
        "action_type": str(req.get("action_type") or ""),
        "target": str(req.get("target") or ""),
        "params": params,
        "request": req_obj,
        "request_sha256": req_obj["request_sha256"],
        # —— 治理决策 ——
        "rule_set": cfg.get("rule_set", ""),
        "rules_version": str(core.get("rules_version") or ""),
        "decision": result.get("decision", "ERROR"),
        "approval": {"state": approval_state, "by": "", "at": "", "note": ""},
        # —— 实际执行结果（接入方回执）——
        "receipt": receipt,
        "receipt_note": ("接入方回执已接收" if receipt is not None else RECEIPT_ABSENT),
        "exception": exception,
        "checks": result.get("checks", []),
        "core": core,
        "source": source,
    }
    return led.append(rec)


def approve(cfg, led, op_id, approver, decision="approved", note=""):
    """人工审批结果：与治理请求同一 op_id 追加一条记录，原记录不回改。"""
    return led.append({
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ts": time.time(),
        "seq": led.next_seq(),
        "kind": "approval_decision",
        "op_id": op_id,
        "ref_op_id": op_id,
        "run_id": _ledger.current_run_id(),
        "rule_id": "G0.10",
        "error_code": "" if decision == "approved" else "APPROVAL_REJECTED",
        "agent_id": "",
        "capability": "",
        "action_type": "approval",
        "target": op_id,
        "params": {},
        "request_sha256": "",
        "rule_set": cfg.get("rule_set", ""),
        "decision": decision,
        "approval": {"state": decision, "by": approver,
                     "at": time.strftime("%Y-%m-%d %H:%M:%S"), "note": note},
        "receipt": None,
        "receipt_note": "审批记录不携带执行回执；审批结论只回答「是否放行」，不证明动作已执行",
        "exception": "",
        "checks": [],
        "source": "approval",
    })
