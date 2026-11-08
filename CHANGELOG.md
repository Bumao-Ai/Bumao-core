# Changelog

## 0.2.0-beta.4 — 2026-11-09

0.2 的第四个 beta，仍不是已完成的 0.2。The fourth beta of 0.2; 0.2 itself is not finished.

- A10／A13 判据取件修正（判定结论不变，仍为 DENY）：单仓 clone 下「区根」被取成仓外上一级，A10 读不到随包审批册结构，理由变成「无审批册」。改为「本仓根带 `30_taizhang` 时以本仓根为区根」。现在 A10 读到 `30_taizhang/shenpi_jilu.txt` 模板，输出 `A10 判定=DENY ｜ 审批册里没有可解析的【第 N 号】条目`。
- `find_approval_ledger()` 不再扫描兄弟目录。旧实现在发布仓同级布局下会读到别仓审批册（本次即读到 `bumao-core` 的模板），红得对但理由错；取件范围收回到本层到根的直系祖先。
- 随包件不变：`facts.py`／`facts_check.py`／`portability_probe.py` 仍按 `HOST_CONTRACT.md §十` 判 N/A，不靠 SKIP。
- 契约自测 `12 项，0 FAIL，0 SKIP，3 N/A`；`test_a10_policy.py` 7/7；`test_gate_registry.py` 7/7。
- 本仓 `check --strict`：`1/12` red（仅 A10，判 DENY 为设计）。
- 未做：A10 转 `PASS` 需真实当日授权条目；`gate_count.py`／`test_equivalence.py` 在单仓 clone 下按退出码 2「不可判定」，不判 PASS/FAIL。

## 0.2.0-beta.3 — 2026-11-08

0.2 的第三个 beta，不是已完成的 0.2。The third beta of 0.2; 0.2 itself is not finished.

- 契约自测转绿：`contract_test.py` 实跑 `12 项，0 FAIL，3 SKIP`，rc=0。`host_reference.py`／`test_gate_registry.py` 随包（已脱敏，无本机绝对路径）；`facts.py`／`facts_check.py`／`portability_probe.py` 改为显式可选依赖，缺件逐条打印 SKIP 与原因，不再计 FAIL。`gate_registry.py` 补上 `GateRegistry` 类（`test_gate_registry.py` 所需）。
- A10 可判：无审批册／无条目／当日无授权行／版本不一致 → `A10 判定=DENY`，detail 写明按策略 `deny` 不放行；当日授权且版本一致 → `A10 判定=PASS`。随包 `30_taizhang/shenpi_jilu.txt` 结构模板（零条目，公开仓固定判 DENY）。`test_a10_policy.py` 实跑 7 项 7 PASS。
- 意图单 `enforce` 受控验证（personal live 树，两次独立 run 实跑）：批准目录内写入放行并落盘；批准目录外写入被拒（`不在批准目录/文件集合内`），目标文件 SHA-256 前后一致；不设环境变量时 `BUMO_JIANCHA_MODE=off`、适配器返回 `None`。能开、能拦、默认 off。
- 已知红项：本仓 `check --strict` 1/12 red —— A10 判 DENY 是设计结果（模板零条目）；A13 首次检出新纳入基线后 PASS。`gate_count.py`／`test_equivalence.py` 仍需三端同级检出。
- community `check --strict` 曾出现一次 `4/44`，**一次未复现，原因未知**；18 次复跑均为 `A10`／`A13` 两条。

## 0.2.0-beta.2 — 2026-11-08

0.2 的第二个 beta，不是已完成的 0.2。The second beta of 0.2; 0.2 itself is not finished.

- 三格状态：**执行前约束＝已接入、默认关闭**。personal 的 MCP 写出工具随动作声明 `intent`，`file_write` 的载荷（`path` + `intent`）在 dispatch 之前先进 L3 审查；默认关闭，因为没有任何启动器拉起 MCP 服务，不启动就什么都不拦。它不在内核自己的 `check --strict` 路径里。执行中监管仍为设计与沙盒原型；执行后审计仍为 personal 已接入。
- 受控验证（实跑，不是 import 看绿）：`test_capability.py` 10 项 10 PASS／0 FAIL；`test_pretool_guard.py` 10 项 10 PASS／0 FAIL，危险调用 DENY 计数 5（≥5），误拦 0；`test_mcp.py` 27 项 27 PASS／0 FAIL。Controlled runs: 10/10 capability, 10/10 pre-tool guard (5 dangerous calls denied, 0 false positives), 27/27 MCP routing.
- 内核运行时代码本版无改动（`bumao_core/` 与 beta.1 相同）；本版是阶段状态与证据更新。Kernel runtime unchanged from `v0.2.0-beta.1`.
- 文档：README 顶部加 `Status: maintenance pause`／「状态：维护暂停，稳定可用」；新增 `RETURN_HERE.md`（回来先看三样、先动 `CHANGELOG.md`、哪些开关默认关着）。
- 已知问题不变：`contract_test.py` 12 项 2 FAIL（缺 5 个未随附模块）；`A10` 缺审批册只给提示、不给凭据；`op_id` 仅 personal 动作级闭合；683 条规则中 103 条可机判（15.1%），机器已绑 89 条；`error_code` 按口径仅在 rc=3 时记。
- community `check --strict` 曾出现一次 `4/44`，**一次未复现，原因未知**；18 次复跑均为 `A10`／`A13` 两条。

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
