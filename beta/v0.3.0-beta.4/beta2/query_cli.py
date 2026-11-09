# -*- coding: utf-8 -*-
"""治理记录命令行查询（beta2）。

用法：
  python query_cli.py --status
  python query_cli.py --op <op_id>          # 返回该 op_id 的全部关联记录
  python query_cli.py --agent agent-demo
  python query_cli.py --decision REQUIRE_APPROVAL
  python query_cli.py --pending
  python query_cli.py --json                 # 追加输出 JSON 明细
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from agentos import evidence, query  # noqa: E402


def load_cfg():
    with io.open(os.path.join(HERE, "beta2_canshu.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["base_dir"] = HERE
    return cfg


def main(argv):
    cfg = load_cfg()
    led = evidence.make_ledger(cfg)
    ap = argparse.ArgumentParser(prog="query_cli.py", description="beta2 治理记录查询")
    ap.add_argument("--op", default="")
    ap.add_argument("--agent", default="")
    ap.add_argument("--decision", default="")
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.status:
        st = query.status(led)
        print("记录 %d（治理请求 %d ／ 审批结论 %d）｜待批 %d｜链断点=%s" % (
            st["records"], st["requests"], st["approvals"], st["pending"],
            st["chain"]["break"] or "无"))
        print("决策分布：%s" % json.dumps(st["decisions"], ensure_ascii=False, sort_keys=True))
        return 0

    if a.op:
        rows = query.by_op(led, a.op)
        scope = "op_id=%s" % a.op
    elif a.pending:
        rows = query.pending(led)
        scope = "pending"
    elif a.agent or a.decision:
        rows = query.find(led, agent_id=a.agent or None, decision=a.decision or None, limit=999)
        scope = "agent=%s decision=%s" % (a.agent or "-", a.decision or "-")
    else:
        rows = led.records()
        scope = "all"

    print("查询 %s → %d 条" % (scope, len(rows)))
    for r in rows:
        b = query.brief(r)
        print("  seq=%-3s op_id=%s kind=%s agent=%s action=%s target=%s decision=%s "
              "error_code=%s rule_id=%s approval=%s approver=%s receipt=%s rule_set=%s rules_version=%s" % (
                  b["seq"], b["op_id"], b["kind"], b["agent"], b["action"], b["target"],
                  b["decision"], b["error_code"], b["rule_id"], b["approval"],
                  b["approver"], b["receipt"], b["rule_set"], b["rules_version"]))
    if a.json:
        print(json.dumps([query.brief(r) for r in rows], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
