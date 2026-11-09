# -*- coding: utf-8 -*-
"""beta2 实跑：示例 Agent 经标准 Adapter 提交，判定全部落到 core 规则体系。

运行：python run_beta2.py
退出码：0 = 全部正反向用例符合预期且账本链无断点；1 = 有不符合项。
"""
import io
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from agentos import adapter, core_bridge, evidence, identity, query, request, review  # noqa: E402
from demo_agent import DemoAgent  # noqa: E402


def load_cfg():
    with io.open(os.path.join(HERE, "beta2_canshu.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["base_dir"] = HERE
    return cfg


def reset(cfg):
    for d in (cfg["run_dir"], cfg["workspace"]):
        p = os.path.join(HERE, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
    os.makedirs(os.path.join(HERE, cfg["workspace"], "approved"), exist_ok=True)
    os.makedirs(os.path.join(HERE, cfg["workspace"], "review"), exist_ok=True)
    os.makedirs(os.path.join(HERE, cfg["workspace"], "_frozen"), exist_ok=True)
    for rel, text in (("approved/tmp.txt", "TMP\n"),
                      ("approved/a.md", "A\n"),
                      ("review/b.md", "B\n"),
                      ("_frozen/keep.txt", "KEEP\n")):
        with io.open(os.path.join(HERE, cfg["workspace"], rel), "w",
                     encoding="utf-8", newline="\n") as f:
            f.write(text)


def p(tag, text=""):
    print("[%s] %s" % (tag, text))


def main():
    cfg = load_cfg()
    reset(cfg)
    led = evidence.make_ledger(cfg)
    reg = identity.AgentRegistry(os.path.join(HERE, cfg["agents"]))

    db, meta, info = core_bridge.load_rules()
    jie = core_bridge.jieru()

    results = []

    def pipeline(req, receipt=None):
        """治理闭环：结构校验 → 规则审查（core）→ 证据记录。"""
        try:
            req_v = request.validate(req)
        except request.RequestError as e:
            res = {"decision": "ERROR", "error_code": e.code, "rule_id": "G0.6",
                   "checks": [{"id": "G0.6", "name": "request_schema", "result": "fail",
                               "detail": str(e)}], "core": {}}
            ag = reg.get((req or {}).get("agent_id")) if isinstance(req, dict) else None
            opid = evidence.new_op_id()
            rec = evidence.record(cfg, led, req if isinstance(req, dict) else {}, ag, res,
                                  exception=str(e), op_id=opid, receipt=receipt, source="adapter")
            return res, rec
        ag = reg.get(req_v["agent_id"])
        res = review.run(req_v, cfg)
        opid = evidence.new_op_id()
        rec = evidence.record(cfg, led, req_v, ag, res, op_id=opid,
                              receipt=receipt, source="adapter")
        return res, rec

    ad = adapter.StandardAdapter(cfg, reg, pipeline)

    demo = ad.bind("vendor:demo-agent", "agent-demo", "示例 Agent（删文件）", [
        {"id": "cap-del-approved", "actions": ["file.delete"],
         "root": "workspace/approved", "approval": False},
    ])
    ad.bind("vendor:review-agent", "agent-review", "审批型 Agent", [
        {"id": "cap-del-review", "actions": ["file.delete"],
         "root": "workspace/review", "approval": True},
    ])
    ad.bind("vendor:approve-agent", "agent-approve", "审批通过示例 Agent", [
        {"id": "cap-del-approve", "actions": ["file.delete"],
         "root": "workspace/review", "approval": True},
    ])
    ad.bind("vendor:reject-agent", "agent-reject", "审批拒绝示例 Agent", [
        {"id": "cap-del-reject", "actions": ["file.delete"],
         "root": "workspace/review", "approval": True},
    ])

    print("=" * 72)
    print("beta2 实跑（沙盒：%s）" % HERE)
    print("core 规则库：%s v%s，%s/%s，%d 条款" % (
        meta.get("name"), meta.get("version"), info["root"], info["rules_dir"],
        len(db.get("clauses") or [])))
    print("接入配置：%s（只绑决策标签，不含判据）" % cfg["core_jieru"])
    print("=" * 72)

    def envelope(ext, op, target, cap=None, reason="", params=None, vendor="demo-vendor"):
        return {"schema": "agent_ext/1", "vendor": vendor, "agent_ref": ext,
                "op": op, "target": target, "capability": cap or "",
                "params": params or {}, "reason": reason}

    def expect(resp, want, label):
        ok = resp.get("decision") == want
        results.append(ok)
        p(label, "decision=%s error_code=%s rule_id=%s op_id=%s receipt=%s %s" % (
            resp.get("decision"), resp.get("error_code") or "-", resp.get("rule_id"),
            resp.get("op_id"), "null" if resp.get("receipt") is None else "present",
            "OK" if ok else "未达预期(%s)" % want))
        return resp

    # ── 第 1 步：示例 Agent 经 Adapter 提交一条统一操作请求 ──
    agent_demo = DemoAgent(ad, "vendor:demo-agent")
    env1 = agent_demo.envelope("file.delete", "workspace/approved/tmp.txt",
                               "cap-del-approved", "清理临时文件")
    p("STEP 1", "外部信封（Agent 侧唯一入口 DemoAgent.delete_file → adapter.submit）")
    print(json.dumps(env1, ensure_ascii=False, indent=2))
    resp1 = agent_demo.delete_file("workspace/approved/tmp.txt",
                                   "cap-del-approved", "清理临时文件")
    recs1 = query.by_op(led, resp1["op_id"])
    req1 = recs1[0]["request"] if recs1 else {}
    p("STEP 1", "Adapter 转换后的 req/1（由 evidence 留存）")
    print(json.dumps(req1, ensure_ascii=False, indent=2))
    results.append(req1.get("schema") == "req/1")

    # ── 第 2 步：识别身份与声明的能力 ──
    ag1 = reg.get(req1["agent_id"])
    cap1 = identity.AgentRegistry.capability(ag1, req1["capability"])
    sig_ok = request.sign(ag1["secret"], req1) == req1["sig"]
    p("STEP 2", "identity=%s status=%s capability=%s actions=%s root=%s approval_required=%s sig=%s" % (
        ag1["agent_id"], ag1["status"], cap1["id"], ",".join(cap1["actions"]),
        cap1["root"], bool(cap1.get("approval")), "valid" if sig_ok else "invalid"))
    results.append(bool(cap1) and sig_ok)

    # ── 第 3 步：core 规则审查 ──
    expect(resp1, "ALLOW", "STEP 3")
    core3 = resp1["governance"]["core"]
    p("STEP 3", "core 调用链")
    for line in core3.get("call_chain", []):
        print("    " + line)
    p("STEP 3", "闸门注册表：登记 %d／期望 %d／对账 %s；run_all 行数=%d" % (
        core3["gate_registry"]["registered"], core3["gate_registry"]["expected"],
        core3["gate_registry"]["validate"], len(core3["gate_registry"]["run_all"])))
    p("STEP 3", "jiancha 运行层：entry=%s result=%s code=%s S0项=%d" % (
        core3["jiancha"]["entry"], core3["jiancha"]["result"], core3["jiancha"]["code"] or "-",
        len(core3["jiancha"]["items"] or [])))

    # ── 第 4 步：证据记录 ──
    rec1 = recs1[0] if recs1 else {}
    p("STEP 4", "op_id=%s run_id=%s rule_set=%s rules_version=%s decision=%s approval=%s exception=%s" % (
        rec1.get("op_id"), rec1.get("run_id"), rec1.get("rule_set"),
        rec1.get("rules_version"), rec1.get("decision"),
        (rec1.get("approval") or {}).get("state"), rec1.get("exception") or "-"))
    p("STEP 4", "三者区分：治理请求 request.params=%s ｜ 治理决策 decision=%s ｜ 执行回执 receipt=%s（%s）" % (
        json.dumps(rec1.get("params"), ensure_ascii=False), rec1.get("decision"),
        "null" if rec1.get("receipt") is None else "present", rec1.get("receipt_note")))
    four = all(k in rec1 for k in ("op_id", "run_id", "rule_id", "error_code"))
    results.append(four and bool(rec1.get("params")) is not None)

    # ── 第 5 步：按 op_id 回查 ──
    back = query.by_op(led, rec1["op_id"])
    ch = led.verify()
    p("STEP 5", "按 op_id 回查：记录数=%d（kind=%s）；链断点=%s" % (
        len(back), ",".join(r.get("kind", "?") for r in back), ch["break"] or "无"))
    results.append(bool(back) and ch["break"] == "")

    print("-" * 72)
    print("第 1 项：注销实跑（注销后再提交必须 DENY/AGENT_UNKNOWN）")
    print("-" * 72)
    ad.bind("vendor:revoke-agent", "agent-revoke", "待注销 Agent", [
        {"id": "cap-del-revoke", "actions": ["file.delete"],
         "root": "workspace/approved", "approval": False},
    ])
    env_r = envelope("vendor:revoke-agent", "file.delete", "workspace/approved/a.md",
                     "cap-del-revoke", "注销前提交")
    before = expect(ad.submit(env_r), "ALLOW", "REVOKE-前")
    out = reg.revoke("agent-revoke")
    p("REVOKE", "revoke() 返回：%s" % json.dumps(out, ensure_ascii=False))
    after = expect(ad.submit(envelope("vendor:revoke-agent", "file.delete",
                                      "workspace/approved/a.md", "cap-del-revoke",
                                      "注销后提交")),
                   "DENY", "REVOKE-后")
    results.append(out is not None and out.get("status_after") == "revoked"
                   and after.get("error_code") == "AGENT_UNKNOWN")

    print("-" * 72)
    print("反向用例（必须被拒或报错）")
    print("-" * 72)
    expect(ad.submit(envelope("vendor:ghost", "file.delete", "workspace/approved/tmp.txt")),
           "ERROR", "REV-0 外部身份未映射")
    expect(ad.submit(envelope("vendor:demo-agent", "file.delete", "_frozen/keep.txt",
                              "cap-del-approved", "越界删除")),
           "DENY", "REV-2 拒绝区越界")

    ghost = request.build("agent-ghost", "cap-del-approved", "file.delete",
                          "workspace/approved/tmp.txt", "wrong-secret")
    r1 = review.run(ghost, cfg)
    p("REV-1", "未注册身份：decision=%s error_code=%s rule_id=%s" % (
        r1["decision"], r1["error_code"], r1["rule_id"]))
    results.append(r1["decision"] == "DENY" and r1["error_code"] == "AGENT_UNKNOWN")

    bad = request.build("agent-demo", "cap-del-approved", "file.delete",
                        "workspace/approved/a.md", demo["secret"])
    bad["sig"] = "0" * 64
    r3 = review.run(bad, cfg)
    p("REV-3", "签名篡改（直连协议层）：decision=%s error_code=%s rule_id=%s" % (
        r3["decision"], r3["error_code"], r3["rule_id"]))
    results.append(r3["decision"] == "DENY" and r3["error_code"] == "BAD_SIGNATURE")

    req_replay = request.build("agent-demo", "cap-del-approved", "file.delete",
                               "workspace/approved/a.md", demo["secret"])
    review.run(req_replay, cfg)
    rr = review.run(req_replay, cfg)
    p("REV-4", "同 nonce 二次提交：decision=%s error_code=%s rule_id=%s" % (
        rr["decision"], rr["error_code"], rr["rule_id"]))
    results.append(rr["decision"] == "DENY" and rr["error_code"] == "REPLAY")

    req_missing = request.build("agent-demo", "cap-del-approved", "file.delete",
                                "workspace/approved/a.md", demo["secret"])
    req_missing.pop("target")
    res5, rec5 = pipeline(req_missing)
    p("REV-5", "结构不合规（缺 target）：decision=%s error_code=%s rule_id=%s op_id=%s" % (
        res5["decision"], res5["error_code"], res5["rule_id"], rec5.get("op_id")))
    results.append(res5["decision"] == "ERROR" and rec5.get("exception"))

    expect(ad.submit(envelope("vendor:demo-agent", "file.delete",
                              "workspace/approved/ghost.txt", "cap-del-approved", "目标不存在"),
                     receipt={"executor": "demo-agent-local", "state": "dry_run",
                              "detail": "接入方声明本次未执行动作，仅演示回执字段",
                              "at": time.strftime("%Y-%m-%d %H:%M:%S")}),
           "WARNING", "REV-6 目标不存在 + 回执字段")

    print("-" * 72)
    print("第 7 项：人工审批 批准一条、拒绝一条（审批人实名，非占位）")
    print("-" * 72)
    ap1 = expect(ad.submit(envelope("vendor:approve-agent", "file.delete",
                                    "workspace/review/b.md", "cap-del-approve", "审批通过用例")),
                 "REQUIRE_APPROVAL", "APPROVAL-待批-1")
    ap2 = expect(ad.submit(envelope("vendor:reject-agent", "file.delete",
                                    "workspace/review/b.md", "cap-del-reject", "审批拒绝用例")),
                 "REQUIRE_APPROVAL", "APPROVAL-待批-2")
    evidence.approve(cfg, led, ap1["op_id"], "张工（工号 A001，运维审批岗）",
                     "approved", "同意删除 review/b.md")
    evidence.approve(cfg, led, ap2["op_id"], "李工（工号 A002，安全审批岗）",
                     "rejected", "拒绝：review 区目标未列入本次清理范围")
    for tag, resp in (("批准", ap1), ("拒绝", ap2)):
        rows = query.by_op(led, resp["op_id"])
        p("APPROVAL-%s" % tag, "op_id=%s 关联记录 %d 条" % (resp["op_id"], len(rows)))
        for r in rows:
            p("APPROVAL-%s" % tag, "  kind=%s decision=%s approval.state=%s by=%s at=%s note=%s" % (
                r.get("kind"), r.get("decision"),
                (r.get("approval") or {}).get("state"), (r.get("approval") or {}).get("by") or "-",
                (r.get("approval") or {}).get("at") or "-",
                (r.get("approval") or {}).get("note") or "-"))
        results.append(len(rows) == 2)
    st = query.status(led)
    p("APPROVAL", "pending=%d requests=%d approvals=%d 链断点=%s" % (
        st["pending"], st["requests"], st["approvals"], st["chain"]["break"] or "无"))
    results.append(st["pending"] == 0 and st["chain"]["break"] == "")

    print("-" * 72)
    print("第 10 项：查询能力（by_op 返回全部关联记录）")
    print("-" * 72)
    rows10 = query.by_op(led, ap1["op_id"])
    p("QUERY", "by_op(%s) → %d 条：%s" % (ap1["op_id"], len(rows10),
                                         " + ".join(r.get("kind", "?") for r in rows10)))
    results.append(len(rows10) >= 2)

    print("-" * 72)
    print("Adapter 接入状态检测")
    print("-" * 72)
    stt = ad.status()
    p("ADAPTER", "state=%s checks=%s" % (stt["state"], json.dumps(stt["checks"], ensure_ascii=False)))

    n_ok = sum(1 for r in results if r)
    rc = 0 if n_ok == len(results) else 1
    print("=" * 72)
    print("beta2 结果：%d/%d 项符合预期；账本=%s；记录数=%d；rc=%d" % (
        n_ok, len(results), os.path.join(cfg["ledger"]), st["records"], rc))
    print("=" * 72)
    return rc


if __name__ == "__main__":
    sys.exit(main())
