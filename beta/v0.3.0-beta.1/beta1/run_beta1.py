# -*- coding: utf-8 -*-
"""beta1 五步链路实跑：示例 Agent 提交一条「删除文件」操作。

运行：python run_beta1.py
退出码：0 = 五步链路 + 反向用例全部符合预期且账本链无断点；1 = 有不符合项。
"""
import io
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from agentos import evidence, identity, query, request, review  # noqa: E402


def load_cfg():
    with io.open(os.path.join(HERE, "beta1_canshu.json"), encoding="utf-8") as f:
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
        with io.open(os.path.join(HERE, cfg["workspace"], rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


def p(tag, text=""):
    print("[%s] %s" % (tag, text))


def main():
    cfg = load_cfg()
    reset(cfg)
    review.load_rules(os.path.join(HERE, cfg["rules"]))
    led = evidence.make_ledger(cfg)
    reg = identity.AgentRegistry(os.path.join(HERE, cfg["agents"]))

    agent = reg.register("agent-demo", "示例 Agent（删文件）", [
        {"id": "cap-del-approved", "actions": ["file.delete"],
         "root": "workspace/approved", "approval": False},
    ])
    reg.register("agent-review", "审批型 Agent", [
        {"id": "cap-del-review", "actions": ["file.delete"],
         "root": "workspace/review", "approval": True},
    ])

    results = []

    def submit(raw, expect, label):
        """统一入口：结构校验 → 身份/能力 → 规则审查 → 证据记录 → 回查。"""
        try:
            req = request.validate(raw)
            ag = reg.get(req["agent_id"])
            res = review.run(req, cfg)
            opid = evidence.new_op_id()
            rec = evidence.record(cfg, led, req, ag, res, op_id=opid)
        except request.RequestError as e:
            ag = reg.get((raw or {}).get("agent_id")) if isinstance(raw, dict) else None
            res = {"decision": "ERROR", "error_code": e.code, "rule_id": "R0.6",
                   "checks": [{"id": "R0.6", "name": "request_schema",
                               "result": "fail", "detail": str(e)}]}
            opid = evidence.new_op_id()
            rec = evidence.record(cfg, led, raw if isinstance(raw, dict) else {}, ag, res,
                                  exception=str(e), op_id=opid)
        ok = res["decision"] == expect
        results.append(ok)
        p(label, "decision=%s error_code=%s rule_id=%s op_id=%s %s" % (
            res["decision"], res["error_code"] or "-", res["rule_id"],
            rec.get("op_id"), "OK" if ok else "未达预期(%s)" % expect))
        return req if "req" in locals() else raw, res, rec

    print("=" * 68)
    print("beta1 五步链路实跑（沙盒：%s）" % HERE)
    print("=" * 68)

    # 第 1 步：示例 Agent 以统一请求结构提交一条操作
    req1 = request.build("agent-demo", "cap-del-approved", "file.delete",
                         "workspace/approved/tmp.txt", agent["secret"])
    p("STEP 1", "统一请求已生成 schema=%s" % req1["schema"])
    print(json.dumps(req1, ensure_ascii=False, indent=2))
    results.append(True)

    # 第 2 步：识别 Agent 身份与声明的能力
    ag1 = reg.get(req1["agent_id"])
    cap1 = identity.AgentRegistry.capability(ag1, req1["capability"])
    sig_ok = request.sign(ag1["secret"], req1) == req1["sig"]
    p("STEP 2", "identity=%s status=%s capability=%s actions=%s root=%s sig=%s" % (
        ag1["agent_id"], ag1["status"], cap1["id"], ",".join(cap1["actions"]),
        cap1["root"], "valid" if sig_ok else "invalid"))
    results.append(bool(cap1 and sig_ok))

    # 第 3 步：走规则审查，返回明确决策
    _, res1, rec1 = submit(req1, "ALLOW", "STEP 3")
    p("STEP 3", "rc=%d" % (0 if res1["decision"] == "ALLOW" else 1))

    # 第 4 步：生成一条证据记录
    p("STEP 4", "op_id=%s run_id=%s rule_set=%s decision=%s approval=%s exception=%s" % (
        rec1["op_id"], rec1["run_id"], rec1["rule_set"], rec1["decision"],
        rec1["approval"]["state"], rec1["exception"] or "-"))
    four = all(k in rec1 for k in ("op_id", "run_id", "rule_id", "error_code"))
    p("STEP 4", "四外键：op_id=%s run_id=%s rule_id=%s error_code(空=无错)=%r → %s；request_sha256=%s" % (
        bool(rec1.get("op_id")), bool(rec1.get("run_id")), bool(rec1.get("rule_id")),
        rec1.get("error_code"), "齐全" if four else "缺项", rec1["request_sha256"][:16]))
    results.append(four)

    # 第 5 步：从记录里查回来
    back = query.by_op(led, rec1["op_id"])
    ch = led.verify()
    p("STEP 5", "按 op_id 回查：%s；decision=%s；记录数=%d；链断点=%s" % (
        "命中" if back else "未命中", (back or {}).get("decision"),
        ch["records"], ch["break"] or "无"))
    results.append(bool(back) and ch["break"] == "")

    print("-" * 68)
    print("反向用例（必须被拒或报错）")
    print("-" * 68)

    # 反 1：未注册身份
    submit(request.build("agent-ghost", "cap-del-approved", "file.delete",
                         "workspace/approved/tmp.txt", "wrong-secret"),
           "DENY", "REV-1 未注册身份")
    # 反 2：能力越界（目标在 _frozen 拒绝区）
    submit(request.build("agent-demo", "cap-del-approved", "file.delete",
                         "_frozen/keep.txt", agent["secret"]),
           "DENY", "REV-2 拒绝区越界")
    # 反 3：签名被篡改
    bad = request.build("agent-demo", "cap-del-approved", "file.delete",
                        "workspace/approved/a.md", agent["secret"])
    bad["sig"] = "0" * 64
    submit(bad, "DENY", "REV-3 签名篡改")
    # 反 4：重放（同 nonce 再提交一次）
    submit(req1, "DENY", "REV-4 重放")
    # 反 5：结构不合规
    submit({"schema": "req/1", "agent_id": "agent-demo", "capability": "cap-del-approved",
            "action_type": "file.delete", "params": {}, "nonce": "nbad", "ts": int(time.time()),
            "sig": "x"}, "ERROR", "REV-5 缺 target")
    # 反 6：需人工审批
    _, res_appr, rec_appr = submit(
        request.build("agent-review", "cap-del-review", "file.delete",
                      "workspace/review/b.md", reg.get("agent-review")["secret"]),
        "REQUIRE_APPROVAL", "REV-6 需审批")
    # 警告：目标不存在
    submit(request.build("agent-demo", "cap-del-approved", "file.delete",
                         "workspace/approved/ghost.txt", agent["secret"]),
           "WARNING", "REV-7 目标不存在")

    # 审批闭环：追加批准记录（原记录不回改）
    evidence.approve(cfg, led, rec_appr["op_id"], "user", "approved", "beta1 演示")
    st = query.status(led)
    p("APPROVAL", "原记录 decision=%s approval=%s；追加后 pending=%d；记录数=%d；链断点=%s" % (
        rec_appr["decision"], rec_appr["approval"]["state"], st["pending"],
        st["records"], st["chain"]["break"] or "无"))
    results.append(st["pending"] == 0 and st["chain"]["break"] == "")

    n_ok = sum(1 for r in results if r)
    rc = 0 if n_ok == len(results) else 1
    print("=" * 68)
    print("beta1 结果：%d/%d 项符合预期；账本=%s；rc=%d" % (
        n_ok, len(results), os.path.join(cfg["ledger"]), rc))
    print("=" * 68)
    return rc


if __name__ == "__main__":
    sys.exit(main())
