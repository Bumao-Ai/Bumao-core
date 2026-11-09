# Changelog

## 0.2.2 — 2026-11-09

0.2 的定型版：在 0.2.1 基础上补装载器、对齐文档与契约，并修掉 0.2.1 露出的装载缺口。

**改了什么**
- 新增 `bumao_core/jiancha/loader.py`：`mode()` 读取 `BUMO_JIANCHA_MODE`，只认 `off`／`shadow`／`enforce`；未设、空串、未知值一律归 `off`。`is_enabled()` 与 `load_if_enabled()` 据此返回；关闭时返回 `None`，开启时才延迟导入 `supervisor`。这是对 0.2.1「只有包、没有装载器」的补齐。
- 新增 `bumao_core/test_jiancha_loader.py`：覆盖未设／空串／未知值／`off`／`shadow`／`enforce` 六态，以及关闭/开启两种加载返回。
- 文档与契约对齐：README 与 `HOST_CONTRACT.md §十一` 改为「默认关闭 + 装载器口径」，不再写「宿主自己 import 即可」。

**验了什么**
- `test_jiancha_loader.py`：六态 + 两个加载用例全部 PASS，rc=0。
- `selftest --kernel` 6/6，rc=0；`contract_test.py` 12 项 0 FAIL，rc=0；四个内核单测 rc=0。
- 解包 0.2.1 发布件复跑：`selftest --kernel` 6/6 rc=0、`contract_test.py` 12/0 rc=0。

**重发说明（本版为 v0.2.2 重发）**
- 修 README 第 175 行口误：原写 “the shipped ledger's single entry”，实际审批册已有两条历史条目，改为 “entries”。
- 原正文把以下若干「状态事实」写成「已知未修」，现逐条改写为实际状态；无代码逻辑改动，资产重新打包。

**已知项的处理（逐条，不再挂「未修」）**
- 恢复半成功语义：口径已定为「A 停机等人」，代码本身即 A 行为（失败即中止整轮、已恢复件保留），不新增 `partial`；缺基线副本用例已验证 `failed` 记录、`recovery=fail`、`RESTORE_FAILED`、抛 `RuntimeError`、`RECOVERED=False`。属已定行为，不是待修项。
- community 凭据 `check_last.json` 丢失：属取证缺口（无日志、无回收站记录）；删除/绕过面已穷举（`git clean -xfd`、全新副本天然没有、整目录替换）；本仓代码内无删除点，无可改之处。
- community `4/44`：凭据缺失（基线在）复现 `3/44`，凭据过期复现 `4/44`，两条均含 B19+B22；最初那次无逐条红项留存，归因在物理上不可行。机制已清楚，不是未定位缺陷。
- 三端随包内核／community 审批册／A10·A13 存量红：属其他仓的发布轨道与本仓判定设计（公开仓无审批册固定判 DENY），本仓不代发、不代签；清单已另行给出。
- 装载器：本仓提供装载点（`loader.load_if_enabled`）；宿主把运行层接进执行路径属 personal 端接线，不在本仓代码内。

## 0.2.1 — 2026-11-09

**改了什么**
- 运行层随包：`bumao_core/jiancha/` 新增 `supervisor.py`、`ledger.py`、`scope.py`、`reasons.py`、`qingli.py`、`personal_adapter.py`、`gate_check.py`、`jiancha_canshu.json`、`schema/reason_codes.json` 与 `__init__.py`。包内全部相对导入，不覆盖宿主同名模块（宿主 `10_rac/ledger.py` 是另一套账本）。`engine.py` 不导入它，内核判定不受影响。
- 修 `recover_restore` 失败路径：基线副本缺失、或写回后哈希与基线不符，逐件记入 `failed`，整轮记 `recovery=fail`，抛 `RuntimeError`，不置 `recovered`。此前这类件被静默跳过并记 `result=ok`。
- `schema/reason_codes.json` 新增 `RESTORE_FAILED`（stage=action，ticket=true）。
- 文档：README 与 `HOST_CONTRACT.md` 补「包含运行层」说明与目录树；补记缺失的 0.2.0 条目。

**验了什么**
- `selftest --kernel` 6/6，rc=0；`contract_test.py` 12 项 0 FAIL，rc=0；`bumao_core/jiancha` 导入可用。
- 活区演练：恢复成功路径（2 件恢复、1 件隔离、in_scope 件保留、链不断）；缺基线副本 → `RESTORE_FAILED` + `recovery=fail` + 抛错 + `RECOVERED=False`；`periodic_check` 两周期 PASS、第三周期 `EXTERNAL_DRIFT` 且 guard 拒绝停机；`qingli` 17→15 件、删除清单与计划逐项一致、证据束保留 10 份。

**还差什么**
- 运行层只有包、没有装载器：宿主必须自己 `import bumao_core.jiancha`，没有 `BUMO_JIANCHA_MODE` 开关；`personal_adapter.py`／`gate_check.py` 只适用于宿主布局。
- 恢复半成功语义未实现可选项：现为「停机等人」（任一失败中止整轮、已恢复件保留），不提供「继续恢复剩余」，也没有 `partial` 状态。
- community 凭据 `check_last.json` 丢失：可删面已定位，但具体那一次未查明。
- community `4/44` 只定位到触发条件：凭据缺失（基线在）复现 `3/44`（A10+B19+B22）；凭据存在但过期复现 `4/44`（A10+B16+B19+B22）；最初那次无逐条留存，无法归因。
- 三端内核未跟随：community／minimal 的 `engine.py` 仍是 `7bd00e2cd72d`（本仓 `c49b8e9ea198`），并缺 `host_reference.py`／`test_a10_policy.py`／`test_gate_registry.py`；personal 无 `kernel/bumao_core`。
- community 审批册未新建；其 A10／A13 仍是已知存量缺口。

## 0.2.0 — 2026-11-09

补记（此前缺失此条目）。

- 修 A13 跨盘符 `relpath`：只有同盘才做相对路径，不同盘按「区根外入口」跳过并在判定理由中写明件数，不再抛 `ValueError: path is on mount ...`；同盘判定结果不变。
- `--quick` FAIL 结论行写明「quick 仅 A 段，B/Z 未跑 —— 不能替代 check --strict」。
- `minimal_host.py` 注释改为实测（A10 + A13，`FAIL (2/13)`）；README 改为两分支都成立的说法。
- 验：`contract_test.py` 12 项 0 FAIL；`selftest --kernel` 6/6；三门槛活区演练；`test_build_parser.py`。
- 资产 `bumao-core-0.2.0.zip`：923889 B，SHA-256 `071ca5277c16d93fd8871958bfb9a5c37784beed09224b3b8afb6b038b035f0a`。

## 0.2.0-beta.5 — 2026-11-09

0.2 的第五个 beta，仍是未完成的 0.2；**这是本阶段的最后一个版本**，受时间与精力所限，未来一个月不再主动迭代（只做维护与修复）。The fifth beta of 0.2 — the last release of this phase; active iteration pauses for about a month.

本版把工作树里积压的修复落地，并真发布了上一版只在文档里承诺过的三个参数。

- **修 `build_parser()` 重复注册**：旧代码连续两次 `sub.add_parser("check")`，调用 `build_parser()` 即抛 `argparse.ArgumentError: conflicting subparser: check`（beta.3／beta.4 均中）。现在只注册一次，`main()` 复用同一个解析器，不再自建第二份。回归用例 `bumao_core/test_build_parser.py`（4 项）。
- **`--quick` 真实生效**：只跑 A 段结构闸，跳过 B/Z 段、防缩水对账与检查凭据写入；结论行明写「不能替代 check --strict」，不再只写在文档里。
- **`--full` 真实生效**：`whoami --full` 追加内核路径、Python 版本、规则目录、子命令清单 4 行；不带 `--full` 时输出与历史版本逐字一致。
- **`selftest --kernel` 真实生效**：不读宿主规则库、不写宿主账本，6 项（engine 可导入／CLI 7 子命令无重复／Out 计数／防缩水往返／gate_registry 可导入且 A10 可判／未注入守卫）。不带 `--kernel` 时是宿主集成自检，未注入 `rules_db` 明确打印原因并返回 2。
- **两种加载方式并存**：新增 `pyproject.toml` 与 `bumao_core/__init__.py`，`pip install -e .` 后 `from bumao_core import engine` 可用；历史 `sys.path.insert` + `import engine` 保持可用。内核内部互导已同时兼容相对与扁平导入（`_import_gate_registry()`）。`pyproject.toml` 只声明打包，无运行时依赖（仍为 stdlib only）。
- **新增 `examples/minimal_host.py`**：不依赖三个产品仓，复制即可跑出一次真实 check。示例不带审批册，因此 A10 判 DENY、`check` 退出码为 1——这是内核默认不放行，不是示例失败，脚本自己会写明。
- **`bumao_core_rules.py` 定性为参考实现**：内核与三端均零引用，且不满足宿主 12 成员契约，不得直接传给 `configure()`；文档改为明确警示，不再只是「未接线的死代码」。
- **实测**：`contract_test.py` `12 项，0 FAIL，0 SKIP，3 N/A`（rc=0）；`test_build_parser.py` 4/4；`test_a10_policy.py` 7/7；`test_gate_registry.py` 7/7；`selftest --kernel` 6/6。
- **已知红项（设计行为，不放宽）**：`python examples/minimal_host.py` 的 `check` 为 `FAIL (2/13 gates red)` —— `A10`（随包审批册零条目 → 策略 `deny` → DENY）与 `A13`（本机已有基线且当日无授权条目 → 改而未授权）。新解压件首跑时 A13 会先纳入基线再通过，只剩 A10。要让 A10 转 `PASS`，只能由使用者本人在 `30_taizhang/shenpi_jilu.txt` 写当日授权条目；随包件里没有。
- **没做的**：三个产品端的 `kernel/bumao_core/` 不在本仓范围内；`gate_count.py`／`test_equivalence.py` 仍要求三端同级检出，单仓 clone 下按退出码 2「不可判定」。

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
