# beta1 —— Bumao Core 0.3 最小可跑骨架

- 性质：沙盒实验件，不参与任何已发布产品
- 位置：本仓 `beta/v0.3.0-beta.1/beta1/`（即已发 beta.1 包内的 `beta1/`）
- 解释器实测：Python 3.12.4
- 运行：`cd beta1; python run_beta1.py`
- 退出码：0 = 五步链路 + 7 条反向用例全部符合预期且账本链无断点

## 目录结构

```
beta1/
├─ beta1_canshu.json          参数件（工作区、账本、种子、规则集）
├─ rules_beta1.json           规则包（R0.1–R0.11，含五值决策映射）
├─ run_beta1.py               五步链路实跑入口
├─ agentos/
│  ├─ identity.py             Agent 注册与身份管理 ＋ 能力登记
│  ├─ request.py              req/1 统一操作请求（结构校验＋HMAC 签名）
│  ├─ review.py               执行前规则审查（五值决策，rule_id 口径沿用 0.2）
│  ├─ evidence.py             act/1 证据记录（四外键＋审批占位）
│  └─ query.py                只读查询与链完整性状态
├─ vendor/
│  └─ ledger.py               0.2 jiancha/ledger.py 逐字副本（哈希链账本）
└─ workspace/                 示例目标（approved / review / _frozen）
```

## 复用（不重写）

- 哈希链账本：`vendor/ledger.py` 与 0.2 早期（2026-11-08）的 `jiancha/ledger.py` 快照
  **字节级一致**（SHA256 `CFA2BD82DD1AED2BE07799E8CB2A20D371E02146B26A5E11538CABFD764519D8`）；当前 core 仓的 `bumao_core/jiancha/ledger.py` 已在 0.2.3 加固（并发写锁＋锚点），本包未升级到该版。
- 四外键口径：`op_id`／`run_id`／`rule_id`／`error_code`，与 0.2 票链同名同义。
- `rule_id` 取值：最先失败项 id；无失败取最后通过项 id（沿用 0.2 `supervisor._rule_id` 规则）。

## beta1 做到了什么

1. 统一请求 `req/1`：9 个字段，缺项/类型错/schema 不符一律 `ERROR`；
2. 身份与能力：注册、能力声明、HMAC 验签、撤销位、nonce 防重放；
3. 规则审查：`ALLOW`／`DENY`／`REQUIRE_APPROVAL`／`WARNING`／`ERROR` 五值均实跑出现；
4. 证据记录：Agent 身份、请求摘要、时间、规则版本、命中规则、决策、审批占位、异常、四外键；
5. 回查：按 `op_id` 命中；`verify()` 链断点为空。

## beta1 没做到什么（明确边界）

- 只有 CLI 只读查询，没有 Web 控制台；
- 没有真实宿主接线（MCP／personal 适配器只是接口占位，未接生产）；
- 审批人身份未签名，审批结果仅占位字段；
- 没有并发与锁，单进程顺序跑；
- 没有把规则审查接到 core 的 `gate_registry` 实例上（复用其口径，未做注册期接线）；
- beta1 编制时十项验收条件原文未送达；原文与逐项现状见 `beta/v0.3.0-beta.4/0.3_jihua_261109.md` §5／§6，beta1 只覆盖任务明示的五步链路。
---

# English Version

# beta1 — the Minimum Runnable Skeleton of Bumao Core 0.3

- Nature: sandbox experimental artifact; does not participate in any released product
- Location: `beta/v0.3.0-beta.1/beta1/` in this repo (that is, `beta1/` inside the published beta.1 package)
- Interpreter measured: Python 3.12.4
- Run: `cd beta1; python run_beta1.py`
- Exit code: 0 = the five-step chain + all 7 negative cases behave as expected and the ledger chain has no break point

## Directory structure

```
beta1/
├─ beta1_canshu.json          Parameter file (workspace, ledger, seed, rule set)
├─ rules_beta1.json           Rule package (R0.1–R0.11, including the five-value decision mapping)
├─ run_beta1.py               Entry point that actually runs the five-step chain
├─ agentos/
│  ├─ identity.py             Agent registration and identity management + capability registration
│  ├─ request.py              req/1 unified operation request (structural validation + HMAC signature)
│  ├─ review.py               Pre-execution rule review (five-value decision, rule_id definition inherited from 0.2)
│  ├─ evidence.py             act/1 evidence record (four foreign keys + approval placeholder)
│  └─ query.py                Read-only query and chain integrity status
├─ vendor/
│  └─ ledger.py               Verbatim copy of 0.2 jiancha/ledger.py (hash-chain ledger)
└─ workspace/                 Example targets (approved / review / _frozen)
```

## Reuse (no rewriting)

- Hash-chain ledger: `vendor/ledger.py` is **byte-for-byte identical** to the early 0.2 (2026-11-08) snapshot of `jiancha/ledger.py`
  (SHA256 `CFA2BD82DD1AED2BE07799E8CB2A20D371E02146B26A5E11538CABFD764519D8`); the current `bumao_core/jiancha/ledger.py` in the core repo was hardened in 0.2.3 (concurrent-write lock + anchor), and this package has not been upgraded to that version.
- Four foreign keys definition: `op_id` / `run_id` / `rule_id` / `error_code`, with the same names and the same meanings as in the 0.2 ticket chain.
- `rule_id` value: the id of the first failing item; if nothing fails, the id of the last passing item (following the 0.2 `supervisor._rule_id` rule).

## What beta1 achieved

1. Unified request `req/1`: 9 fields; a missing field, a wrong field type, or a schema mismatch always yields `ERROR`;
2. Identity and capability: registration, capability declaration, HMAC signature verification, revocation flag, nonce anti-replay;
3. Rule review: all five values `ALLOW` / `DENY` / `REQUIRE_APPROVAL` / `WARNING` / `ERROR` appeared in actual runs;
4. Evidence recording: Agent identity, request digest, time, rule version, hit rule, decision, approval placeholder, exception, four foreign keys;
5. Query back: hits by `op_id`; `verify()` reports no chain break point.

## What beta1 did not achieve (explicit boundaries)

- Only CLI read-only queries; no Web console;
- No real host wiring (the MCP / personal adapters are interface placeholders only, not connected to production);
- Approver identity is not signed; the approval result is only a placeholder field;
- No concurrency or locking; a single process runs sequentially;
- Rule review is not wired onto core's `gate_registry` instance (its definition is reused, but registration-time wiring is not done);
- The original text of the ten acceptance criteria was not delivered when beta1 was prepared; the original text and the item-by-item current state are in `beta/v0.3.0-beta.4/0.3_jihua_261109.md` §5/§6; beta1 covers only the five-step chain explicitly stated in the task.
