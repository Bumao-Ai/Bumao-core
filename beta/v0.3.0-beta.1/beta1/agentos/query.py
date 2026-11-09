# -*- coding: utf-8 -*-
"""治理状态与查询（beta1 只做 CLI 只读面）。"""


def by_op(led, op_id):
    for r in led.records():
        if str(r.get("op_id")) == str(op_id):
            return r
    return None


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


def status(led):
    recs = led.records()
    # 只追加账本：审批结果作为新记录回指原 op_id，原记录保持 pending 不改。
    answered = set(r.get("target") for r in recs if r.get("action_type") == "approval")
    pending = [r for r in recs
               if (r.get("approval") or {}).get("state") == "pending"
               and r.get("op_id") not in answered]
    return {
        "records": len(recs),
        "pending": len(pending),
        "chain": led.verify(),
    }
