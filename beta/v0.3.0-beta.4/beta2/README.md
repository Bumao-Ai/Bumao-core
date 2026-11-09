# Bumao Core 0.3 · beta.4 收录的 beta2 可运行骨架（Agent 接入与执行前治理）

本目录随 `v0.3.0-beta.4` 收录；代码、配置与判据与 `v0.3.0-beta.2` 逐字节相同，本版未改任何代码。beta1、beta2、beta3 的 tag／Release／资产不在本包内，也不被本包覆盖。

## 这一版是什么

beta2 在 beta1 的五步链路上补了六处短板：

| 编号 | beta1 状态 | beta2 做法 |
| --- | --- | --- |
| 第 5 项 | 审查用自带 `rules_beta1.json`，与 core 规则体系无关 | 删掉自带规则表；`review` 只做转发，判定全部经 `vendor/core` 的 core 原生件（规则库装载器＋闸门注册表＋jiancha 运行层动作前判定入口） |
| 第 9 项 | 示例 Agent 直连 `request.build` | 新增 `agentos/adapter.py`；示例 Agent `DemoAgent` 只能调 `adapter.submit`，请求/响应转换、身份映射、错误处理、接入状态检测都在 Adapter 内 |
| 第 1 项 | 注销未实跑 | `revoke()` 返回注销前后状态；注销后再提交实测 `DENY/AGENT_UNKNOWN` |
| 第 7 项 | 只有占位审批人、无拒绝路径 | 批准一条、拒绝一条；审批人实名（张工/李工带工号），两条记录均可回查 |
| 第 8 项 | 只留请求哈希，无回执字段 | 证据整包留 `params`；新增 `receipt` 字段（接入方不提供时 `null` ＋原因）；请求／决策／执行结果三段分开 |
| 第 10 项 | `by_op` 只回首条；审批另起 op_id | `by_op` 返回同一 `op_id` 的全部记录；审批记录与治理请求同 `op_id`；附命令行查询 |

## 目录

```
beta2/
  run_beta2.py          实跑入口（21 项断言，rc=0/1）
  query_cli.py          治理记录命令行查询
  demo_agent.py         示例 Agent（只经 Adapter 提交）
  meta.json             core 规则库 meta（名称/版本/生效日）
  rules/r01.json        core 规则库条款（11 条，对应 11 道闸门）
  core_rules_jieru.json core 接入配置（只绑决策标签与动作映射，不含判据）
  beta2_canshu.json     运行参数件
  agentos/
    identity.py         Agent 注册/注销/能力登记
    request.py          req/1 统一请求（9 字段 + HMAC）
    review.py           审查转发（异常一律 ERROR）
    core_bridge.py      与 core 的唯一接入口
    adapter.py          标准 Adapter
    evidence.py         证据记录（含 params 与 receipt）
    query.py            查询（by_op 返回全部）
  vendor/
    ledger.py           0.2 jiancha/ledger.py 逐字副本
    core/               core 原生件逐字副本（见下表）
  workspace/            沙盒目标（运行时可重建）
  run/                  运行时产物（agents/identity_map/actions.jsonl/nonces/core）
```

## 怎么跑

前置：Python 3.8+，无第三方依赖。

```
cd beta2
python run_beta2.py          # 五步链路 + 注销 + 反向用例 + 双审批；末行打印 rc
python query_cli.py --status
python query_cli.py --op <op_id>      # 同一 op_id 的全部关联记录
python query_cli.py --pending
python query_cli.py --agent agent-demo --json
```

`run_beta2.py` 每次运行会重建 `run/` 与 `workspace/`，账本随之重建。

## core 接入调用链（第 5 项证据）

```
review.run(req)
  └─ core_bridge.review(req)
       ├─ bumao_core_rules.find_root / load_db / index / load_meta
       │    返回：规则库 db（11 条款）＋ meta（版本 0.3.0-beta2）
       ├─ gate_registry.GateRegistry(engine_module=engine)
       │    .register("B", G0.1 … G0.11, …)   × 11
       │    .validate(expected=11 道)          → PASS
       │    .run_all(db, strict=False)         → [(gid, ok, detail)] × 11
       └─ jiancha.supervisor.Supervisor.begin → pre_check(action)
             返回：{result, code, items}；S0 项 7 条
                  动作类型／目标形态／拒绝区／批准范围判定取自该结果
```

决策标签（ALLOW/DENY/REQUIRE_APPROVAL/WARNING/ERROR 与 error_code）由
`core_rules_jieru.json` 绑定；该文件不含判据，判据在 core 原生件里。
Agent 协议层（身份、签名、重放、能力声明）core 无对应件，仍由 `agentos` 判定，
但同样以 core 闸门形式登记进 `GateRegistry` 并按登记顺序整跑。

## 三个概念不合并

- **治理请求**：`record["request"]`，含 9 字段全量请求、`params` 与 `request_sha256`。
- **治理决策**：`record["decision"]`／`rule_id`／`error_code`／`checks`，只说明放行与否。
- **实际执行结果**：`record["receipt"]`。beta2 不执行任何动作，接入方不提供回执时写
  `receipt: null`，原因写 `receipt_note`。`ALLOW` 不等于动作已执行。

## vendor/core 逐字副本哈希（与 core 仓当前工作树一致）

| 文件 | SHA256 |
| --- | --- |
| `bumao_core_rules.py` | `A8692A78965CF05252E720A861DBBEE1A6B17F5ACD8A3EC7D264D928DA7877E7` |
| `engine.py` | `B5401F1F3C902867DB520ED5D449EC4342BF2955FF40BB94F900862A8FA1CD5E` |
| `gate_registry.py` | `5E682853E9A4DEFDD93711892DF98CB5BB9D7553CFC54D5DB96330ABC421A09A` |
| `jiancha/__init__.py` | `F1E1EC3B6E5BA9FB282CFE1AE03487580C0D653DE0F37BE9630210213B27D1E6` |
| `jiancha/scope.py` | `FAD56D0A7F0D2B32333099C9D7B8DC9AFDFCADF9CB28C45608FE4599606AEA1B` |
| `jiancha/reasons.py` | `3A5579CAC364E2D2150F6AF895AF511D15A985D930FA3A86E7202069FDB64EAE` |
| `jiancha/ledger.py` | `DBED288B0477B6501E586EB40F031D81A1DEB3E1651A64C5005B184CECAD15D4` |
| `jiancha/supervisor.py` | `6F932246C0F09100CB0747D91CFDBC99B04C3711F3830984A434CC243D0C9AAF` |
| `jiancha/schema/reason_codes.json` | `2DE3C2CCEED2284D6DA61DC0D48972D497C7C8E7D8A4C0AA1E403CAFBF26FDC9` |

副本只改路径不改内容：逐文件与 `bumao-core` 仓对应文件的 SHA256 一致。

## 边界

- 不执行任何真实操作；只给执行前治理决策。
- 不改 core 仓、不改 0.2.x、不改 beta1 的 tag/Release/资产。
- `rule_id` 口径沿用 0.2（首个失败项即命中规则）；本包不新增判据。
---

# English Version

# Bumao Core 0.3 · beta2 runnable skeleton included in beta.4 (Agent onboarding and pre-execution governance)

This directory is included with `v0.3.0-beta.4`; its code, configuration and criteria are byte-identical to `v0.3.0-beta.2`, and this version changes no code. beta1's, beta2's and beta3's tags/Releases/assets are not in this package and are not overwritten by it.

## What this version is

beta2 closes six weak points in beta1's five-step chain:

| # | beta1 state | beta2 approach |
| --- | --- | --- |
| Item 5 | Review used a built-in `rules_beta1.json`, unrelated to the core rule system | Deleted the built-in rule table; `review` only forwards, and all decisions go through core native artifacts in `vendor/core` (rule-base loader + gate registry + jiancha runtime pre-action decision entry point) |
| Item 9 | The sample Agent connected directly to `request.build` | Added `agentos/adapter.py`; the sample Agent `DemoAgent` can only call `adapter.submit`; request/response conversion, identity mapping, error handling, and integration status detection all live inside the Adapter |
| Item 1 | Revocation not actually run | `revoke()` returns the state before and after revocation; after revocation, a real submission gives `DENY/AGENT_UNKNOWN` |
| Item 7 | Only a placeholder approver, no rejection path | One approved, one rejected; approvers are real named persons (Engineer Zhang / Engineer Li with employee IDs), and both records can be looked up |
| Item 8 | Only the request hash was kept, no receipt field | Evidence keeps the whole `params`; added a `receipt` field (`null` plus reason when the integrating party does not provide one); request / decision / execution result are kept in three separate parts |
| Item 10 | `by_op` returned only the first record; approvals started a separate op_id | `by_op` returns all records under the same `op_id`; approval records share the same `op_id` as the governance request; command-line query provided |

## Directory

```
beta2/
  run_beta2.py          real-run entry (21 assertions, rc=0/1)
  query_cli.py          governance record command-line query
  demo_agent.py         sample Agent (submits only through the Adapter)
  meta.json             core rule-base meta (name/version/effective date)
  rules/r01.json        core rule-base clauses (11 clauses, corresponding to 11 gates)
  core_rules_jieru.json core integration config (binds only decision labels and action mappings, no criteria)
  beta2_canshu.json     runtime parameter file
  agentos/
    identity.py         Agent registration/revocation/capability registration
    request.py          req/1 unified request (9 fields + HMAC)
    review.py           review forwarding (anomalies are always ERROR)
    core_bridge.py      the only integration point with core
    adapter.py          standard Adapter
    evidence.py         evidence recording (including params and receipt)
    query.py            query (by_op returns all)
  vendor/
    ledger.py           verbatim copy of 0.2 jiancha/ledger.py
    core/               verbatim copies of core native artifacts (see table below)
  workspace/            sandbox targets (rebuildable at runtime)
  run/                  runtime artifacts (agents/identity_map/actions.jsonl/nonces/core)
```

## How to run

Prerequisite: Python 3.8+, no third-party dependencies.

```
cd beta2
python run_beta2.py          # five-step chain + revocation + negative cases + dual approvals; rc printed on the last line
python query_cli.py --status
python query_cli.py --op <op_id>      # all related records under the same op_id
python query_cli.py --pending
python query_cli.py --agent agent-demo --json
```

Each run of `run_beta2.py` rebuilds `run/` and `workspace/`, and the ledger is rebuilt accordingly.

## core integration call chain (evidence for Item 5)

```
review.run(req)
  └─ core_bridge.review(req)
       ├─ bumao_core_rules.find_root / load_db / index / load_meta
       │    returns: rule base db (11 clauses) + meta (version 0.3.0-beta2)
       ├─ gate_registry.GateRegistry(engine_module=engine)
       │    .register("B", G0.1 … G0.11, …)   × 11
       │    .validate(expected=11 gates)          → PASS
       │    .run_all(db, strict=False)         → [(gid, ok, detail)] × 11
       └─ jiancha.supervisor.Supervisor.begin → pre_check(action)
              returns: {result, code, items}; 7 S0 items
                  action type / target shape / denial zone / approval scope decisions come from this result
```

Decision labels (ALLOW/DENY/REQUIRE_APPROVAL/WARNING/ERROR and error_code) are bound by
`core_rules_jieru.json`; that file contains no criteria — the criteria live in the core native artifacts.
For the Agent protocol layer (identity, signature, replay, capability declaration) core has no corresponding
artifacts, so they are still decided by `agentos`, but they are likewise registered into `GateRegistry` in the
form of core gates and run all together in registration order.

## Three concepts are not merged

- **Governance request**: `record["request"]`, containing the full 9-field request, `params`, and `request_sha256`.
- **Governance decision**: `record["decision"]` / `rule_id` / `error_code` / `checks`, stating only whether it is allowed.
- **Actual execution result**: `record["receipt"]`. beta2 executes no action; when the integrating party does not
  provide a receipt, it writes `receipt: null` and puts the reason in `receipt_note`. `ALLOW` does not mean the action has been executed.

## vendor/core verbatim copy hashes (consistent with the current working tree of the core repo)

| File | SHA256 |
| --- | --- |
| `bumao_core_rules.py` | `A8692A78965CF05252E720A861DBBEE1A6B17F5ACD8A3EC7D264D928DA7877E7` |
| `engine.py` | `B5401F1F3C902867DB520ED5D449EC4342BF2955FF40BB94F900862A8FA1CD5E` |
| `gate_registry.py` | `5E682853E9A4DEFDD93711892DF98CB5BB9D7553CFC54D5DB96330ABC421A09A` |
| `jiancha/__init__.py` | `F1E1EC3B6E5BA9FB282CFE1AE03487580C0D653DE0F37BE9630210213B27D1E6` |
| `jiancha/scope.py` | `FAD56D0A7F0D2B32333099C9D7B8DC9AFDFCADF9CB28C45608FE4599606AEA1B` |
| `jiancha/reasons.py` | `3A5579CAC364E2D2150F6AF895AF511D15A985D930FA3A86E7202069FDB64EAE` |
| `jiancha/ledger.py` | `DBED288B0477B6501E586EB40F031D81A1DEB3E1651A64C5005B184CECAD15D4` |
| `jiancha/supervisor.py` | `6F932246C0F09100CB0747D91CFDBC99B04C3711F3830984A434CC243D0C9AAF` |
| `jiancha/schema/reason_codes.json` | `2DE3C2CCEED2284D6DA61DC0D48972D497C7C8E7D8A4C0AA1E403CAFBF26FDC9` |

The copies change only paths, not content: the SHA256 of each file matches the corresponding file in the `bumao-core` repo.

## Boundaries

- Executes no real operations; provides only pre-execution governance decisions.
- Does not modify the core repo, does not modify 0.2.x, does not modify beta1's tag/Release/assets.
- `rule_id` follows 0.2's convention (the first failing item is the matched rule); this package adds no criteria.
