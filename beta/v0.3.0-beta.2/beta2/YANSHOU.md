# beta2 十项验收逐条实测（2026-11-09）

实测环境：Windows，Python 3.12.4，`beta2/` 全新重建后执行 `python run_beta2.py`，
末行 `beta2 结果：21/21 项符合预期；rc=0`。以下「实测输出」为当次原始打印。

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
