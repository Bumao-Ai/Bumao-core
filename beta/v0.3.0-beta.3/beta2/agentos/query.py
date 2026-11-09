# -*- coding: utf-8 -*-
"""治理状态与查询（beta2）。

按 op_id 查询返回**该 op_id 的全部关联记录**（治理请求 + 审批结论），不是首条。
"""


def by_op(led, op_id):
    return [r for r in led.records() if str(r.get("op_id")) == str(op_id)]


def find(led, agent_id=None, decision=None, action_type=None, limit=50):
    out = []
    for r in led.records():
        if agent_id and r.get("agent_id") != agent_id:
            continue
        if decision and r.get("decision") != decision:
            continue
        if action_type and r.get("action_type") != action_type:
            continue
        out.append(r)
    return out[-int(limit or 50):]


def pending(led):
    recs = led.records()
    answered = set(r.get("op_id") for r in recs if r.get("kind") == "approval_decision")
    return [r for r in recs
            if r.get("kind") == "governance_request"
            and (r.get("approval") or {}).get("state") == "pending"
            and r.get("op_id") not in answered]


def status(led):
    recs = led.records()
    return {
        "records": len(recs),
        "requests": len([r for r in recs if r.get("kind") == "governance_request"]),
        "approvals": len([r for r in recs if r.get("kind") == "approval_decision"]),
        "pending": len(pending(led)),
        "decisions": {d: len([r for r in recs if r.get("decision") == d])
                      for d in ("ALLOW", "DENY", "REQUIRE_APPROVAL", "WARNING", "ERROR",
                                "approved", "rejected")},
        "chain": led.verify(),
    }


def brief(r):
    """一行摘要，供命令行查询使用。"""
    return {
        "op_id": r.get("op_id"),
        "kind": r.get("kind"),
        "seq": r.get("seq"),
        "agent": r.get("agent_id") or "-",
        "action": r.get("action_type"),
        "target": r.get("target"),
        "decision": r.get("decision"),
        "error_code": r.get("error_code") or "-",
        "rule_id": r.get("rule_id"),
        "approval": (r.get("approval") or {}).get("state"),
        "approver": (r.get("approval") or {}).get("by") or "-",
        "receipt": "null" if r.get("receipt") is None else "present",
        "rule_set": r.get("rule_set"),
        "rules_version": r.get("rules_version") or "-",
    }
