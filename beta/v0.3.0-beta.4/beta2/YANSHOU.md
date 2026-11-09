# beta.4 包内 beta2 十项验收逐条实测（2026-11-09，代码与 beta.2 逐字节相同）

实测环境：Windows，Python 3.12.4，`beta2/` 全新重建后执行 `python run_beta2.py`，
末行 `beta2 结果：21/21 项符合预期；rc=0`（入口脚本名与末行文字沿用 beta2，属原样保留，不代表本包是 beta.2）。以下「实测输出」为当次原始打印。

| # | 验收项 | beta2 是否满足 | 证据路径 | 实测输出（原文节选） |
| --- | --- | --- | --- | --- |
| 1 | 注册和注销 Agent | 满足 | `agentos/identity.py:AgentRegistry.register/revoke`；`run_beta2.py`「第 1 项」段；`run/actions.jsonl` | `revoke() 返回：{"agent_id": "agent-revoke", "status_before": "active", "status_after": "revoked", "revoked_at": "2026-11-09 13:22:36"}`；注销后 `decision=DENY error_code=AGENT_UNKNOWN rule_id=G0.1` |
| 2 | 识别 Agent 身份 | 满足 | `agentos/identity.py:get`；`core_bridge.py:G0.1`；`run_beta2.py` STEP 2／REV-1 | `[STEP 2] identity=agent-demo status=active … sig=valid`；未注册身份 `decision=DENY error_code=AGENT_UNKNOWN` |
| 3 | 登记 Agent 声明的能力 | 满足 | `agentos/identity.py:register(capabilities=…)`；`core_bridge.py:G0.4` | `capability=cap-del-approved actions=file.delete root=workspace/approved approval_required=False` |
| 4 | 接收统一格式操作请求 | 满足 | `agentos/request.py`（req/1 九字段＋HMAC）；`agentos/adapter.py:transform` | Adapter 转换后请求：`"schema": "req/1"`，字段 `agent_id/capability/action_type/target/params/nonce/ts/sig` 齐备，`request_sha256=3bf315a…` |
| 5 | 调用现有规则治理体系审查 | 满足（范围判定与闸门整跑全在 core；身份/签名等协议层检查 core 无对应件，以 core 闸门形式登记，判据仍在 beta 协议层） | `agentos/core_bridge.py`；`core_rules_jieru.json`；`rules/r01.json`；`vendor/core/*` | 调用链 4 行：`bumao_core_rules.find_root/load_db/index/load_meta（db：11 条款，meta：v0.3.0-beta2）`；`GateRegistry.register × 11 → validate(11) → run_all（注册表 11 道，返回 11 行）`；`Supervisor.pre_check（result=pass，S0 项 7 条）`；`闸门注册表：登记 11／期望 11／对账 PASS` |
| 6 | 返回明确的治理决策 | 满足 | `agentos/core_bridge.py:review`；`core_rules_jieru.json:gates` | 五值全实测：`ALLOW`（STEP 3）、`DENY`（REVOKE-后／REV-2）、`REQUIRE_APPROVAL`（APPROVAL-待批 1/2）、`WARNING`（REV-6）、`ERROR`（REV-0 未映射／REV-5 缺字段） |
| 7 | 生成和处理人工审批请求 | 满足 | `agentos/evidence.py:approve`；`run_beta2.py`「第 7 项」段 | 批准：`by=张工（工号 A001，运维审批岗） decision=approved`；拒绝：`by=李工（工号 A002，安全审批岗） decision=rejected`；`pending=0 requests=8 approvals=2` |
| 8 | 记录完整的治理证据 | 满足 | `agentos/evidence.py:record`；`run/actions.jsonl` | `request.params={"reason": "清理临时文件"}`；`decision=ALLOW`；`receipt=null（接入方未提供执行回执；治理决策不等于实际执行结果）`；另一条 `receipt=present`；四外键 `op_id/run_id/rule_id/error_code` 齐备；`exception` 字段存在 |
| 9 | 标准 Adapter 接入示例 Agent | 满足 | `agentos/adapter.py`；`demo_agent.py`；`run_beta2.py` STEP 1 | 示例 Agent 入口 `DemoAgent.delete_file → adapter.submit`；`[ADAPTER] state=ready`，四项检查 `core_rules_db / gate_registry / identity_map / request_schema` 全 pass |
| 10 | 查询请求、决策与审批历史 | 满足 | `agentos/query.py:by_op`；`query_cli.py` | `[QUERY] by_op(op-…6261a1) → 2 条：governance_request + approval_decision`；CLI：`seq=7 … decision=REQUIRE_APPROVAL` / `seq=9 … decision=approved approver=张工…`；`--pending → 0 条`；`--status 记录 10（治理请求 8／审批结论 2）｜待批 0｜链断点=无` |

## 未满足项

无。第 5 项的边界如实标注：core 原生件覆盖规则库装载、闸门登记/对账/整跑、动作类型、目标形态、拒绝区与批准范围；
Agent 身份、签名、重放、能力声明四项 core 没有对应件，仍由 beta 协议层判定，但已作为闸门登记进 core 的
`GateRegistry` 并按登记顺序整跑。不把「core 无对应件」写成「已由 core 判定」。
---

# English Version

# beta2 item-by-item real-run verification of the ten acceptance items inside the beta.4 package (2026-11-09; code byte-identical to beta.2)

Real-run environment: Windows, Python 3.12.4, `beta2/` freshly rebuilt and then `python run_beta2.py` executed;
the last line reads `beta2 result: 21/21 items met expectations; rc=0` (the entry-script name and last-line wording keep the beta2 label as-is; this does not mean the package is beta.2). The "actual output" below is the original printout of that run.

| # | Acceptance item | Does beta2 satisfy it | Evidence path | Actual output (excerpt from the original) |
| --- | --- | --- | --- | --- |
| 1 | Register and revoke an Agent | Satisfied | `agentos/identity.py:AgentRegistry.register/revoke`; the "Item 1" section of `run_beta2.py`; `run/actions.jsonl` | `revoke() returns: {"agent_id": "agent-revoke", "status_before": "active", "status_after": "revoked", "revoked_at": "2026-11-09 13:22:36"}`; after revocation `decision=DENY error_code=AGENT_UNKNOWN rule_id=G0.1` |
| 2 | Identify the Agent's identity | Satisfied | `agentos/identity.py:get`; `core_bridge.py:G0.1`; `run_beta2.py` STEP 2 / REV-1 | `[STEP 2] identity=agent-demo status=active … sig=valid`; unregistered identity gives `decision=DENY error_code=AGENT_UNKNOWN` |
| 3 | Register the capabilities declared by the Agent | Satisfied | `agentos/identity.py:register(capabilities=…)`; `core_bridge.py:G0.4` | `capability=cap-del-approved actions=file.delete root=workspace/approved approval_required=False` |
| 4 | Receive operation requests in a unified format | Satisfied | `agentos/request.py` (req/1 nine fields + HMAC); `agentos/adapter.py:transform` | Request after Adapter conversion: `"schema": "req/1"`, fields `agent_id/capability/action_type/target/params/nonce/ts/sig` all present, `request_sha256=3bf315a…` |
| 5 | Invoke the existing rule governance system for review | Satisfied (scope determination and the full gate run are entirely in core; for protocol-layer checks such as identity and signature, core has no corresponding artifact, so they are registered in the form of core gates, while the criteria remain in the beta protocol layer) | `agentos/core_bridge.py`; `core_rules_jieru.json`; `rules/r01.json`; `vendor/core/*` | 4 lines of the call chain: `bumao_core_rules.find_root/load_db/index/load_meta (db: 11 clauses, meta: v0.3.0-beta2)`; `GateRegistry.register × 11 → validate(11) → run_all (11 gates in the registry, 11 lines returned)`; `Supervisor.pre_check (result=pass, 7 S0 items)`; `gate registry: registered 11 / expected 11 / reconciliation PASS` |
| 6 | Return an explicit governance decision | Satisfied | `agentos/core_bridge.py:review`; `core_rules_jieru.json:gates` | All five values actually measured: `ALLOW` (STEP 3), `DENY` (after REVOKE / REV-2), `REQUIRE_APPROVAL` (APPROVAL-awaiting 1/2), `WARNING` (REV-6), `ERROR` (REV-0 unmapped / REV-5 missing field) |
| 7 | Generate and handle human approval requests | Satisfied | `agentos/evidence.py:approve`; the "Item 7" section of `run_beta2.py` | Approved: `by=Engineer Zhang (employee ID A001, operations approval role) decision=approved`; rejected: `by=Engineer Li (employee ID A002, security approval role) decision=rejected`; `pending=0 requests=8 approvals=2` |
| 8 | Record complete governance evidence | Satisfied | `agentos/evidence.py:record`; `run/actions.jsonl` | `request.params={"reason": "clean up temporary files"}`; `decision=ALLOW`; `receipt=null (the integrating party did not provide an execution receipt; the governance decision is not equal to the actual execution result)`; another record `receipt=present`; the four foreign keys `op_id/run_id/rule_id/error_code` are all present; the `exception` field exists |
| 9 | Onboard a sample Agent through the standard Adapter | Satisfied | `agentos/adapter.py`; `demo_agent.py`; `run_beta2.py` STEP 1 | Sample Agent entry `DemoAgent.delete_file → adapter.submit`; `[ADAPTER] state=ready`, all four checks `core_rules_db / gate_registry / identity_map / request_schema` pass |
| 10 | Query request, decision and approval history | Satisfied | `agentos/query.py:by_op`; `query_cli.py` | `[QUERY] by_op(op-…6261a1) → 2 records: governance_request + approval_decision`; CLI: `seq=7 … decision=REQUIRE_APPROVAL` / `seq=9 … decision=approved approver=Engineer Zhang…`; `--pending → 0 records`; `--status records 10 (governance requests 8 / approval conclusions 2) | pending 0 | chain break = none` |

## Unmet items

None. The boundary of Item 5 is marked truthfully: the core native artifacts cover rule-base loading, gate registration/reconciliation/full run, action type, target shape, denial zone and approval scope;
the four items of Agent identity, signature, replay and capability declaration have no corresponding artifact in core, so they are still decided by the beta protocol layer, but they have been registered as gates into core's
`GateRegistry` and are run all together in registration order. "core has no corresponding artifact" is not written as "already decided by core".
