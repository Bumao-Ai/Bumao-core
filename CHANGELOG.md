# Changelog

## 0.2.0-beta.1 — 2026-11-08

0.2 的第一个 beta，不是已完成的 0.2。The first beta of 0.2; 0.2 itself is not finished.

- 三格状态：执行后审计已接入 personal（动作行四键、`ledger.py shenji` 可导出全链路）；执行前约束、执行中监管仍为设计与沙盒原型，**未接入 live**。
- 文档：README 增加「两个版本空间」说明（内核 `0.10` 与发布 tag 是两个独立编号空间），Roadmap 明确标为进行中。
- 不新增执行能力；`bumao_core/` 运行时代码在本版无变更。
- 已知问题：`contract_test.py` 12 项 2 FAIL（缺 5 个未随附模块）；`A10` 缺审批册只给提示、不给凭据；`op_id` 仅 personal 动作级闭合；683 条规则中 103 条可机判（15.1%），机器已绑 89 条；`error_code` 按口径仅在 rc=3 时记。
- community `check --strict` 曾出现一次 `4/44`，**一次未复现，原因未知**；18 次复跑均为 `A10`／`A13` 两条。

## 0.12 — 2026-11-08

本版为口径与结构对齐，并补上内核契约（无新增执行能力）。This release aligns wording and structure and ships the kernel contract; it adds no execution capability.

- Before: gate `A10` threw `FileNotFoundError` on a fresh checkout, because `kernel_contract.json` was not in the repository. Now: `kernel_contract.json` and `contract_test.py` ship at the repository root — the exact path `engine.py` reads (one level above `bumao_core/`), so `A10` evaluates the contract and reports the missing approval ledger instead of crashing.
- Before: the README opened with gate IDs and internal paths. Now: the first screen answers what it is, who it is for and what it solves, English first, Chinese below (`README.md`).
- Before: no screenshots. Now: one real terminal capture under `docs/screens/` (`test_check_rc.py` output plus the shipped tree).
- No runtime change: `git diff v0.11..HEAD -- bumao_core/` is empty; `engine.py` bytes are unchanged.

Known issues in this batch (documented in `README.md`, not fixed here): `contract_test.py` reports `2 FAIL` because checks `[B]`/`[C]` expect five modules this repo does not ship; `gate_count.py` and `test_equivalence.py` fail on a single-repo clone because they assume sibling checkouts.

Not shipped yet (do not count as done): `runtime_preflight.py`, the second batch of fake-green patches, and the four foreign keys (`op_id` / `rule_id` / `run_id` / `error_code`).

## 0.1 — 2026-11-08

首次公开发布。

- 统一内核：`engine.py` 作为唯一运行时引擎。
- 13 个通用闸门模板与宿主注入契约。
- 防缩水：`set_expected()` 声明期望集，少注册一个闸门即失败。
- 三口径闸数统计与新旧引擎等价性回归。
- 宿主契约文档 `bumao_core/HOST_CONTRACT.md`。
