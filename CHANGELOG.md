# Changelog

## 0.2.6 — 2026-11-09

A13 基线按端分文件存放；首次纳入基线时如实标注「未授权基线建立」。判定口径不变。

- `engine.py`：`_round_auth_gate` 的基线文件由 `00_meta/a13_benlun_jizhun.json` 改为 `a13_benlun_jizhun.<端键>.json`；端键由入口位置推导（`<区根>/<产品>/10_rac/<入口>` → `<产品>`），内核不含任何端名。
- `engine.py`：`round_auth_verdict` 在「本轮无改动但有首次纳入」时不再只说「无改动」，改为明写「未授权基线建立，不以『无改动』冒充已授权」。
- `__init__.py`：`__version__` 0.2.5 → 0.2.6。
- 未变：12 个契约成员、7 个子命令、`CORE_VERSION`（0.10）；A10／B16 等闸门判据无改动。

**English**
- `engine.py`: the A13 round baseline moves from one shared `00_meta/a13_benlun_jizhun.json` to per-edition `a13_benlun_jizhun.<edition-key>.json`; the key is derived from the entry path (`<root>/<product>/10_rac/<entry>` → `<product>`), so the kernel still contains no edition names.
- `engine.py`: when a round adds files to the baseline for the first time, the verdict now says "unauthorised baseline creation" instead of reporting "no change".
- `__init__.py`: `__version__` 0.2.5 → 0.2.6.
- Unchanged: 12 contract members, 7 subcommands, `CORE_VERSION` (0.10); A10 / B16 verdicts untouched.

> 发版流程：每次发版，Release 正文必须中英双侧齐全（中文在前、英文在后，英文逐条对应，不得只给摘要）；只有一侧不算发完。核对项见 `CONTRIBUTING.md`「发版清单（维护者）」。

## 0.3.0-beta.4 — 2026-11-09

文案版：不改代码，只修对外文案、补一份文档。

**改了什么**
- 新增 `beta/v0.3.0-beta.4/README.md`：写明本版只改文案、代码与 `v0.3.0-beta.2` 逐字节相同、包内清单与跑法、各 beta 的 tag／Release／资产互不覆盖、元数据与账本标识为何刻意沿用 beta.2。
- 包内 `beta2/README.md`、`beta2/YANSHOU.md` 的标题与自述改为「随 beta.4 收录、代码与 beta.2 逐字节相同」，不再自称「本目录是 beta.2 的全部内容」。
- 随包收录规划原文 `0.3_guihua_261109.md`（7,479 字节，SHA256 `28ce30eb487fd312f81d530933cbb946b674beb841a9abd20eb0d2785a4863c6`），使计划书与差距分析里对它的引用在包内成立。
- 仓根 `README.md` 的发布事实更正为实际状态：最新正式发布 `v0.2.4`，0.3 的 beta 系列为 Pre-release，`v0.2.1` 已发布、未跳过；清掉英半区里重复的中文行；给 `v0.2.0-beta.3` 与「beta.3 的受控留证」加「0.2 的 beta.3」限定词。
- `beta/v0.3.0-beta.1/beta1/README.md` 去掉本机绝对路径、改为仓内相对路径；「十项原文未送达」改为指向 `beta/v0.3.0-beta.4/0.3_jihua_261109.md` §5／§6。
- 统一 `beta/v0.3.0-beta.2` 与 beta.3／beta.4 的 `beta2/YANSHOU.md` 第 5 项边界句（补「如实标注」4 个汉字，9,128 → 9,140 字节）。

**验了什么**
- 线上资产解包后 `python run_beta2.py` 末行 `21/21 项符合预期；rc=0`；`query_cli.py --status`／`--op`／`--pending` 均有输出。
- 代码未改：`beta2/vendor/core` 9 个文件的 SHA256 与 `v0.3.0-beta.2` 一致。

## 0.3.0-beta.3 — 2026-11-09

文档英文侧补齐：beta1 与 beta2 的 7 个说明文档改为中英对照，中文原文在前、完整英文在后；代码、配置与判据与 `v0.3.0-beta.2` 逐字节相同，本版不发代码变更。

**验了什么**
- 仓内 7 个文件均以 `---` 与 `# English Version` 分隔，线上抓回的仓内同名文件可见英文段。
- 已发 `v0.3.0-beta.1`、`v0.3.0-beta.2` 的 tag、Release 与资产未改动。

## 0.3.0-beta.2 — 2026-11-09

补齐 beta.1 十项验收里未满足的六项：审查改经 core 规则库、闸门登记与运行层 `pre_check`；新增 Adapter（请求／响应转换、身份映射、错误处理、接入状态）；注销后重提得 `DENY / AGENT_UNKNOWN`；批一条拒一条、审批人非占位；证据留 `params` 与 `receipt`（未提供时 `receipt: null`）；`by_op` 返回同 `op_id` 全部记录并配 CLI 查询。

**验了什么**
- `run_beta2.py` 末行 `21/21 项符合预期；rc=0`；账本 10 条记录（治理请求 8／审批结论 2），`pending=0`。

## 0.3.0-beta.1 — 2026-11-09

Bumao Core 0.3 的第一个 beta：外部 Agent 以受治理身份提交操作的最小骨架。含 `req/1`（9 字段＋HMAC-SHA256 签名＋nonce/ts）、身份与能力识别、执行前规则审查、四外键证据记录、按 `op_id` 回查；7 条反向用例各留一条证据。

**验了什么**
- `run_beta1.py` 末行 `13/13 项符合预期；rc=0`。

## 0.2.4 — 2026-11-09

A10 授权闸三态版：授权按「变更当日」判，跨版本轴的比对去掉。

**改了什么**
- A10 判据改为三态：契约 `core_version` 自上次授权后未变更（`updated_at` 早于最近授权条目日期）→ PASS；有变更（`updated_at` 不早于最近授权日）→ 变更当日有授权条目则 PASS、无则 DENY；判不了（契约缺字段、`updated_at` 非法、审批册不可读或无可解析授权条目）→ DENY。
- 旧实现把「没有审批册」直接当「未授权变更」，并拿契约版本号去比对审批册里另一条版本轴的版本号，导致合法包恒红；新判据只看变更日期有无授权，不再跨轴比版本。
- 契约 `meta.updated_at` 由 2026-11-07 改为 2026-11-09，同日审批册登记第 24 号授权条目。
- `test_a10_policy.py` 改为三态用例：未变更 PASS、有变更无授权 DENY、有变更有授权 PASS、判不了 DENY，另加真实文件路径两例。

**验了什么**
- `test_a10_policy.py` 10/10，rc=0。真实契约与审批册：`A10 判定=PASS ｜ 三态=changed ｜ 变更当日（2026-11-09）有授权条目`。
- `selftest --kernel` 6/6，rc=0；`contract_test.py` 12 项，0 FAIL，0 SKIP，3 N/A，rc=0。
- `test_build_parser.py`／`test_gate_registry.py`／`test_check_rc.py`／`test_jiancha_loader.py`／`test_jiancha_scope.py`／`test_jiancha_ledger.py`／`test_jiancha_recovery.py` 全部 rc=0。
- 全新解包 0.2.4 发布件复跑：`selftest --kernel` 6/6 rc=0、`contract_test.py` 12 项 0 FAIL rc=0。

## 0.2.3 — 2026-11-09

运行层与打包订正版：装上就完整、目标按真实位置判、账本可并发写。

**改了什么**
- 打包：`pyproject.toml` 改为自动发现 `bumao_core` 子包，显式声明包数据（`HOST_CONTRACT.md`、`jiancha/*.json`、`jiancha/schema/*.json`），并新增 `MANIFEST.in`。此前 wheel 只含顶层 `bumao_core`，`pip install` 后没有 `bumao_core/jiancha/`，也没有 `jiancha_canshu.json` 与 `schema/reason_codes.json`，导入运行层直接报错。现在 wheel 与 sdist 都含 `jiancha/` 全部源码与两个 JSON。
- 目标路径：`scope.target_abs()` 改为按真实路径（`realpath`）校验；目标不存在时按最近已存在父目录的真实路径判定。符号链接／目录联结指向 workspace 外一律拒绝，悬空链接或真实位置判不出时一律拒绝执行（fail-closed）。
- 拒绝区：`scope.denied()` 不再跳过无法规范化的拒绝区。`denied_zones` 不是列表、或其中任一项形态非法，装载期即判配置错误 `DENIED_ZONES_INVALID` 并拒绝执行；运行期同判一律按不放行处理。
- 账本：`ActionLedger` 增加跨进程写锁（Windows `msvcrt.locking`／POSIX `fcntl.lockf`），「读末端→写行→fsync→写锚」整段在锁内。每轮末端哈希另写独立锚点文件（fsync 后原子替换），`verify()` 在链校验后同时比对锚点行数与末行哈希。
- `schema/reason_codes.json` 新增 `DENIED_ZONES_INVALID`（stage=load）、`TARGET_UNRESOLVABLE`（stage=action）。
- 新增测试：`test_jiancha_scope.py`（链接逃逸／路径穿越／拒绝区非法配置／过期与非法授权单）、`test_jiancha_ledger.py`（多进程并发写／锚点篡改／进程强杀后恢复）、`test_jiancha_recovery.py`（意外退出后恢复／恢复失败／回滚失败）。

**验了什么**
- wheel：内容含 `bumao_core/jiancha/` 9 个 `.py` 与 `jiancha_canshu.json`、`schema/reason_codes.json`，无 `.bak`；干净 venv `pip install` 后导入成功（`__version__=0.2.3`，码表 34 个码），`selftest --kernel` 6/6 rc=0。
- `test_jiancha_scope.py` ALL PASS rc=0；`test_jiancha_ledger.py` ALL PASS rc=0（6 进程 × 12 条并发写，72 条无丢失，锚点一致）；`test_jiancha_recovery.py` ALL PASS rc=0。
- `selftest --kernel` 6/6 rc=0；`contract_test.py` 12 项 0 FAIL，0 SKIP，3 N/A，rc=0；四个内核单测与 `test_jiancha_loader.py` rc=0。
- 全新解包 0.2.3 发布件复跑：`selftest --kernel` 6/6 rc=0、`contract_test.py` 12 项 0 FAIL rc=0。

## 0.2.2 — 2026-11-09

0.2 的定型版：在 0.2.1 基础上补装载器、对齐文档与契约，并修掉 0.2.1 露出的装载缺口。

**改了什么**
- 新增 `bumao_core/jiancha/loader.py`：`mode()` 读取 `BUMO_JIANCHA_MODE`，只认 `off`／`shadow`／`enforce`；未设、空串、未知值一律归 `off`。`is_enabled()` 与 `load_if_enabled()` 据此返回；关闭时返回 `None`，开启时才延迟导入 `supervisor`。这是对 0.2.1「只有包、没有装载器」的补齐。
- 新增 `bumao_core/test_jiancha_loader.py`：覆盖未设／空串／未知值／`off`／`shadow`／`enforce` 六态，以及关闭/开启两种加载返回。
- 恢复失败的行为定为「停机等人」：基线副本缺失、或写回后哈希与基线不符，逐件记入 `failed`，整轮记 `recovery=fail`，抛 `RuntimeError`，不置 `recovered`；已恢复件保留，不提供 `partial` 状态。
- 文档与契约对齐：README 与 `HOST_CONTRACT.md §十一` 改为「默认关闭 + 装载器口径」，不再写「宿主自己 import 即可」；README 第 175 行 `the shipped ledger's single entry` 订正为 `entries`（随包审批册有两条历史条目）。

**验了什么**
- `test_jiancha_loader.py`：六态 + 两个加载用例全部 PASS，rc=0。
- `selftest --kernel` 6/6，rc=0；`contract_test.py` 12 项 0 FAIL，rc=0；四个内核单测 rc=0。
- 全新解包 0.2.2 发布件复跑：`selftest --kernel` 6/6 rc=0、`contract_test.py` 12/0 rc=0。

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

---

## English

> Release process: every release body must be complete in both Chinese and English (Chinese first, English after, item-by-item correspondence, not a summary); one side alone does not count as released. See "Release checklist (maintainers)" in `CONTRIBUTING.md`.

### 0.3.0-beta.4 — 2026-11-09

Documentation edition: no code change; only external-facing wording is fixed and one document is added.

**What changed**
- Added `beta/v0.3.0-beta.4/README.md`: states that this version changes documentation only, that the code is byte-identical to `v0.3.0-beta.2`, what the package contains and how to run it, that the betas' tags/Releases/assets never overwrite each other, and why the metadata and ledger identifiers are deliberately kept at beta.2.
- In the package, the title and self-description of `beta2/README.md` and `beta2/YANSHOU.md` now read "included with beta.4, code byte-identical to beta.2" instead of "this directory is the entire contents of beta.2".
- The planning source text `0.3_guihua_261109.md` is included in the package (7,479 bytes, SHA256 `28ce30eb487fd312f81d530933cbb946b674beb841a9abd20eb0d2785a4863c6`), so that the references to it in the plan and the gap analysis resolve inside the package.
- The release facts in the root `README.md` are corrected to the actual state: the latest non-prerelease Release is `v0.2.4`, the 0.3 beta line is Pre-release, and `v0.2.1` was published, not skipped; duplicate Chinese lines in the English half are removed; `v0.2.0-beta.3` and "controlled run in beta.3" are qualified as the 0.2 beta.3.
- In `beta/v0.3.0-beta.1/beta1/README.md`, local absolute paths are replaced with in-repo relative paths, and "the original text of the ten acceptance criteria was not delivered" now points to `beta/v0.3.0-beta.4/0.3_jihua_261109.md` §5/§6.
- The Item 5 boundary sentence in `beta2/YANSHOU.md` is unified across `beta/v0.3.0-beta.2` and beta.3/beta.4 (4 Chinese characters added, 9,128 → 9,140 bytes).

**What was verified**
- After unpacking the online asset, `python run_beta2.py` ends with `21/21 items met expectations; rc=0`; `query_cli.py --status` / `--op` / `--pending` all produce output.
- No code change: the SHA256 of the 9 files under `beta2/vendor/core` is identical to `v0.3.0-beta.2`.

### 0.3.0-beta.3 — 2026-11-09

English side of the documentation completed: the 7 explanatory documents of beta1 and beta2 become bilingual, with the Chinese original first and the full English after; code, configuration and criteria are byte-identical to `v0.3.0-beta.2`, and this version ships no code change.

**What was verified**
- All 7 in-repo files are separated by `---` and `# English Version`, and the same-named files fetched back from the online repo show the English section.
- The tags, Releases and assets of the published `v0.3.0-beta.1` and `v0.3.0-beta.2` are unchanged.

### 0.3.0-beta.2 — 2026-11-09

Filled the six unmet items of beta.1's ten-item acceptance: review now goes through the core rule library, gate registration and the runtime layer's `pre_check`; added the Adapter (request/response transformation, identity mapping, error handling, onboarding status); after revocation a resubmission yields `DENY / AGENT_UNKNOWN`; one approval and one rejection with non-placeholder approvers; evidence keeps `params` and `receipt` (`receipt: null` when not supplied); `by_op` returns every record under the same `op_id`, with CLI queries.

**What was verified**
- `run_beta2.py` ends with `21/21 items met expectations; rc=0`; the ledger holds 10 records (8 governance requests / 2 approval decisions), `pending=0`.

### 0.3.0-beta.1 — 2026-11-09

The first beta of Bumao Core 0.3: a minimal skeleton for an external Agent submitting operations under a governed identity. It covers `req/1` (9 fields + HMAC-SHA256 signature + nonce/ts), identity and capability resolution, pre-execution rule review, four-foreign-key evidence records, and lookup by `op_id`; each of the 7 reverse cases leaves one evidence record.

**What was verified**
- `run_beta1.py` ends with `13/13 items met expectations; rc=0`.

### 0.2.4 — 2026-11-09

A10 authorization gate, three-state edition: authorization is judged by the day of change, and the cross-version-axis comparison is removed.

**What changed**
- A10 criteria become three-state: the contract's `core_version` unchanged since the last authorization (`updated_at` earlier than the most recent authorization entry's date) → PASS; changed (`updated_at` not earlier than the latest authorization date) → PASS if there is an authorization entry on the day of change, DENY if not; undeterminable (contract missing a field, `updated_at` invalid, approval ledger unreadable or with no parseable authorization entry) → DENY.
- The old implementation treated "no approval ledger" directly as "unauthorized change", and compared the contract version number against the version number of another version axis in the approval ledger, so legitimate packages were permanently red; the new criteria look only at whether there is an authorization on the change date and no longer compare versions across axes.
- Contract `meta.updated_at` changed from 2026-11-07 to 2026-11-09, and authorization entry No. 24 is registered in the approval ledger the same day.
- `test_a10_policy.py` switches to three-state cases: unchanged PASS, changed without authorization DENY, changed with authorization PASS, undeterminable DENY, plus two cases using real file paths.

**What was verified**
- `test_a10_policy.py` 10/10, rc=0. Real contract and approval ledger: `A10 判定=PASS ｜ 三态=changed ｜ 变更当日（2026-11-09）有授权条目`.
- `selftest --kernel` 6/6, rc=0; `contract_test.py` 12 items, 0 FAIL, 0 SKIP, 3 N/A, rc=0.
- `test_build_parser.py` / `test_gate_registry.py` / `test_check_rc.py` / `test_jiancha_loader.py` / `test_jiancha_scope.py` / `test_jiancha_ledger.py` / `test_jiancha_recovery.py` all rc=0.
- Fresh unpack of the 0.2.4 release artifact, re-run: `selftest --kernel` 6/6 rc=0, `contract_test.py` 12 items, 0 FAIL, rc=0.

### 0.2.3 — 2026-11-09

Runtime-layer and packaging correction release: complete on install, targets judged by their real location, and the ledger can be written concurrently.

**What changed**
- Packaging: `pyproject.toml` now auto-discovers the `bumao_core` subpackages and explicitly declares package data (`HOST_CONTRACT.md`, `jiancha/*.json`, `jiancha/schema/*.json`), plus a new `MANIFEST.in`. Previously the wheel contained only top-level `bumao_core`; after `pip install` there was no `bumao_core/jiancha/`, and no `jiancha_canshu.json` or `schema/reason_codes.json`, so importing the runtime layer failed immediately. Both the wheel and the sdist now contain all `jiancha/` source and the two JSON files.
- Target paths: `scope.target_abs()` now validates against the real path (`realpath`); when the target does not exist, the decision uses the real path of the nearest existing parent directory. Symlinks / directory junctions pointing outside the workspace are always rejected; dangling links or a real location that cannot be determined always reject execution (fail-closed).
- Denied zones: `scope.denied()` no longer skips denied zones that cannot be normalized. If `denied_zones` is not a list, or any entry has an invalid shape, load time immediately reports the configuration error `DENIED_ZONES_INVALID` and rejects execution; at runtime the same finding is always treated as not allowed.
- Ledger: `ActionLedger` gains a cross-process write lock (Windows `msvcrt.locking` / POSIX `fcntl.lockf`), with the whole "read tail → write line → fsync → write anchor" sequence inside the lock. Each round's tail hash is also written to a separate anchor file (atomically replaced after fsync), and `verify()` compares anchor line count and tail hash after the chain check.
- `schema/reason_codes.json` adds `DENIED_ZONES_INVALID` (stage=load) and `TARGET_UNRESOLVABLE` (stage=action).
- New tests: `test_jiancha_scope.py` (link escape / path traversal / invalid denied-zone configuration / expired and invalid authorization tickets), `test_jiancha_ledger.py` (multi-process concurrent writes / anchor tampering / recovery after a process kill), `test_jiancha_recovery.py` (recovery after an unexpected exit / recovery failure / rollback failure).

**What was verified**
- wheel: contents include the 9 `.py` files under `bumao_core/jiancha/`, `jiancha_canshu.json` and `schema/reason_codes.json`, with no `.bak`; a clean venv `pip install` then imports successfully (`__version__=0.2.3`, 34 codes in the table), and `selftest --kernel` is 6/6 rc=0.
- `test_jiancha_scope.py` ALL PASS rc=0; `test_jiancha_ledger.py` ALL PASS rc=0 (6 processes × 12 concurrent writes, 72 lines with none lost, anchors consistent); `test_jiancha_recovery.py` ALL PASS rc=0.
- `selftest --kernel` 6/6 rc=0; `contract_test.py` 12 items, 0 FAIL, 0 SKIP, 3 N/A, rc=0; the four kernel unit tests and `test_jiancha_loader.py` rc=0.
- Fresh unpack of the 0.2.3 release artifact, re-run: `selftest --kernel` 6/6 rc=0, `contract_test.py` 12 items, 0 FAIL, rc=0.

### 0.2.2 — 2026-11-09

The finalized 0.2 release: on top of 0.2.1 it adds the loader, aligns docs and contract, and closes the loading gap exposed by 0.2.1.

**What changed**
- New `bumao_core/jiancha/loader.py`: `mode()` reads `BUMO_JIANCHA_MODE`, accepting only `off` / `shadow` / `enforce`; unset, empty string and unknown values all map to `off`. `is_enabled()` and `load_if_enabled()` return accordingly; when disabled they return `None`, and only when enabled is `supervisor` imported lazily. This closes 0.2.1's "package only, no loader" gap.
- New `bumao_core/test_jiancha_loader.py`: covers the six states unset / empty string / unknown value / `off` / `shadow` / `enforce`, plus both disabled and enabled load returns.
- Recovery-failure behaviour is defined as "halt and wait for a human": if a baseline copy is missing, or the hash after write-back does not match the baseline, each item is recorded in `failed`, the whole round is recorded as `recovery=fail`, a `RuntimeError` is raised, and `recovered` is not set; already-recovered items are kept and there is no `partial` state.
- Docs and contract aligned: README and `HOST_CONTRACT.md §十一` now state "disabled by default + loader semantics" instead of "the host just imports it itself"; README line 175 `the shipped ledger's single entry` is corrected to `entries` (the bundled approval ledger has two historical entries).

**What was verified**
- `test_jiancha_loader.py`: six states plus two load cases all PASS, rc=0.
- `selftest --kernel` 6/6, rc=0; `contract_test.py` 12 items, 0 FAIL, rc=0; the four kernel unit tests rc=0.
- Fresh unpack of the 0.2.2 release artifact, re-run: `selftest --kernel` 6/6 rc=0, `contract_test.py` 12/0 rc=0.

### 0.2.1 — 2026-11-09

**What changed**
- Runtime layer bundled: `bumao_core/jiancha/` adds `supervisor.py`, `ledger.py`, `scope.py`, `reasons.py`, `qingli.py`, `personal_adapter.py`, `gate_check.py`, `jiancha_canshu.json`, `schema/reason_codes.json` and `__init__.py`. All imports inside the package are relative and do not shadow host modules of the same name (the host's `10_rac/ledger.py` is a different ledger). `engine.py` does not import it, so kernel verdicts are unaffected.
- Fixed the `recover_restore` failure path: if a baseline copy is missing, or the hash after write-back does not match the baseline, each item is recorded in `failed`, the whole round is recorded as `recovery=fail`, a `RuntimeError` is raised, and `recovered` is not set. Previously such items were silently skipped and recorded as `result=ok`.
- `schema/reason_codes.json` adds `RESTORE_FAILED` (stage=action, ticket=true).
- Docs: README and `HOST_CONTRACT.md` add the "includes runtime layer" note and directory tree; the missing 0.2.0 entry is recorded.

**What was verified**
- `selftest --kernel` 6/6, rc=0; `contract_test.py` 12 items, 0 FAIL, rc=0; `bumao_core/jiancha` imports usable.
- Live-zone drill: recovery success path (2 items recovered, 1 quarantined, in_scope items kept, chain unbroken); missing baseline copy → `RESTORE_FAILED` + `recovery=fail` + raise + `RECOVERED=False`; `periodic_check` passes two cycles, the third cycle reports `EXTERNAL_DRIFT` and the guard refuses to halt; `qingli` 17→15 items, deletion list matches the plan item by item, evidence bundle keeps 10 copies.

**Still missing**
- The runtime layer has only a package and no loader: the host must `import bumao_core.jiancha` itself, there is no `BUMO_JIANCHA_MODE` switch, and `personal_adapter.py` / `gate_check.py` only fit the host layout.
- The semi-success recovery semantics option is not implemented: it is currently "halt and wait for a human" (any failure aborts the round, already-recovered items are kept); there is no "continue recovering the rest" and no `partial` state.
- community credential `check_last.json` lost: the deletable surface has been located, but that specific occurrence has not been identified.
- community `4/44` only pinned to trigger conditions: with the credential missing (baseline present) `3/44` is reproduced (A10+B19+B22); with the credential present but expired `4/44` is reproduced (A10+B16+B19+B22); the original occurrence has no per-item record, so it cannot be attributed.
- The three editions' kernels have not followed: community / minimal `engine.py` is still `7bd00e2cd72d` (this repo's is `c49b8e9ea198`) and still lacks `host_reference.py` / `test_a10_policy.py` / `test_gate_registry.py`; personal has no `kernel/bumao_core`.
- The community approval ledger has not been created; its A10 / A13 are still known standing gaps.

### 0.2.0 — 2026-11-09

Back-filled (this entry was previously missing).

- Fixed the A13 cross-drive `relpath`: relative paths are computed only on the same drive; on different drives the item is skipped as an "outside-area-root entry" with the item count stated in the verdict reason, and `ValueError: path is on mount ...` is no longer raised; same-drive verdicts are unchanged.
- The `--quick` FAIL conclusion line now states "quick covers only section A; B/Z were not run — this cannot replace check --strict".
- The `minimal_host.py` comment now reflects measurement (A10 + A13, `FAIL (2/13)`); the README wording now holds for both branches.
- Verified: `contract_test.py` 12 items, 0 FAIL; `selftest --kernel` 6/6; three-gate live-zone drill; `test_build_parser.py`.
- Asset `bumao-core-0.2.0.zip`: 923889 B, SHA-256 `071ca5277c16d93fd8871958bfb9a5c37784beed09224b3b8afb6b038b035f0a`.

### 0.2.0-beta.5 — 2026-11-09

The fifth beta of 0.2 — the last release of this phase; active iteration pauses for about a month. This release lands the fixes queued in the working tree and actually ships the three parameters that the previous release only promised in documentation.

- **Fix duplicate registration in `build_parser()`**: the old code called `sub.add_parser("check")` twice, so calling `build_parser()` raised `argparse.ArgumentError: conflicting subparser: check` (beta.3 / beta.4 both hit this). Now it registers once only, and `main()` reuses the same parser instead of building a second one. Regression test `bumao_core/test_build_parser.py` (4 items).
- **`--quick` actually works**: runs only the section A structural gates, skipping sections B/Z, the shrink-guard reconciliation and the check-credential write; the conclusion line explicitly says "cannot replace check --strict", instead of saying so only in the docs.
- **`--full` actually works**: `whoami --full` appends 4 lines — kernel path, Python version, rules directory, subcommand list; without `--full` the output is byte-for-byte identical to historical versions.
- **`selftest --kernel` actually works**: reads no host rule base and writes no host ledger; 6 items (engine importable / CLI 7 subcommands without duplicates / Out counts / shrink-guard round trip / gate_registry importable and A10 judgeable / guard not injected). Without `--kernel` it is the host integration self-check, which prints the reason and returns 2 when `rules_db` is not injected.
- **Two loading modes coexist**: adds `pyproject.toml` and `bumao_core/__init__.py`, so `from bumao_core import engine` works after `pip install -e .`; the historical `sys.path.insert` + `import engine` keeps working. Kernel-internal imports support both relative and flat imports (`_import_gate_registry()`). `pyproject.toml` declares packaging only, with no runtime dependency (still stdlib only).
- **New `examples/minimal_host.py`**: does not depend on the three product repos; copy it and it runs one real check. The example ships no approval ledger, so A10 verdicts DENY and `check` exits with 1 — this is the kernel refusing by default, not the example failing, and the script says so.
- **`bumao_core_rules.py` classified as a reference implementation**: zero references in the kernel and in all three editions, and it does not satisfy the host's 12-member contract, so it must not be passed directly to `configure()`; the docs now carry an explicit warning instead of only calling it "unwired dead code".
- **Measured**: `contract_test.py` `12 items, 0 FAIL, 0 SKIP, 3 N/A` (rc=0); `test_build_parser.py` 4/4; `test_a10_policy.py` 7/7; `test_gate_registry.py` 7/7; `selftest --kernel` 6/6.
- **Known reds (design behaviour, not relaxed)**: `check` in `python examples/minimal_host.py` is `FAIL (2/13 gates red)` — `A10` (zero entries in the bundled approval ledger → policy `deny` → DENY) and `A13` (a baseline already exists on this machine and there is no authorization entry for the day → changed without authorization). On a freshly unpacked artifact's first run, A13 is first taken into the baseline and then passes, leaving only A10. To turn A10 into `PASS`, only the user can write a same-day authorization entry into `30_taizhang/shenpi_jilu.txt`; the bundled artifact does not contain one.
- **Not done**: the three product editions' `kernel/bumao_core/` are out of this repo's scope; `gate_count.py` / `test_equivalence.py` still require the three editions checked out at the same level and exit with code 2 ("undeterminable") on a single-repo clone.

### 0.2.0-beta.4 — 2026-11-09

The fourth beta of 0.2; 0.2 itself is not finished.

- A10 / A13 evidence-lookup correction (verdicts unchanged, still DENY): on a single-repo clone the "area root" was taken as the parent outside the repo, so A10 could not read the bundled approval ledger structure and the reason became "no approval ledger". It now uses "when this repo root contains `30_taizhang`, this repo root is the area root". A10 now reads the `30_taizhang/shenpi_jilu.txt` template and prints `A10 判定=DENY ｜ 审批册里没有可解析的【第 N 号】条目`.
- `find_approval_ledger()` no longer scans sibling directories. Under the release repos' sibling layout the old implementation read another repo's approval ledger (this time it read `bumao-core`'s template), red for the right reason but wrong cause; the lookup scope is narrowed to the direct ancestors from this level to the root.
- Bundled artifacts unchanged: `facts.py` / `facts_check.py` / `portability_probe.py` are still judged N/A per `HOST_CONTRACT.md §十`, not via SKIP.
- Contract self-test `12 items, 0 FAIL, 0 SKIP, 3 N/A`; `test_a10_policy.py` 7/7; `test_gate_registry.py` 7/7.
- This repo's `check --strict`: `1/12` red (only A10, DENY by design).
- Not done: turning A10 into `PASS` needs a real same-day authorization entry; on a single-repo clone `gate_count.py` / `test_equivalence.py` exit with code 2 ("undeterminable") and judge neither PASS nor FAIL.

### 0.2.0-beta.3 — 2026-11-08

The third beta of 0.2; 0.2 itself is not finished.

- Contract self-test goes green: `contract_test.py` actually runs `12 items, 0 FAIL, 3 SKIP`, rc=0. `host_reference.py` / `test_gate_registry.py` ship (sanitized, no local absolute paths); `facts.py` / `facts_check.py` / `portability_probe.py` become explicit optional dependencies, and missing files print SKIP with the reason line by line and no longer count as FAIL. `gate_registry.py` gains the `GateRegistry` class (required by `test_gate_registry.py`).
- A10 becomes judgeable: no approval ledger / no entries / no authorization line for the day / version mismatch → `A10 判定=DENY`, with detail stating that policy `deny` does not allow it; same-day authorization with a matching version → `A10 判定=PASS`. Bundled `30_taizhang/shenpi_jilu.txt` is a structure template (zero entries; public repos always judge DENY). `test_a10_policy.py` actually runs 7 items, 7 PASS.
- Controlled verification of the intent ticket `enforce` (personal live tree, two independent runs): writes inside approved directories are allowed and land on disk; writes outside approved directories are rejected (`不在批准目录/文件集合内`) and the target file's SHA-256 is unchanged before and after; with no environment variable set, `BUMO_JIANCHA_MODE=off` and the adapter returns `None`. It can be enabled, it can block, and it is off by default.
- Known reds: this repo's `check --strict` is 1/12 red — A10 judging DENY is the designed result (zero-entry template); A13 passes after the first check detects and enrolls the baseline. `gate_count.py` / `test_equivalence.py` still require the three editions checked out at the same level.
- community `check --strict` once showed `4/44`, **never reproduced, cause unknown**; all 18 re-runs showed the `A10` / `A13` two lines.

### 0.2.0-beta.2 — 2026-11-08

The second beta of 0.2; 0.2 itself is not finished.

- Three-cell status: **pre-execution constraint = wired in, off by default**. personal's MCP write tools declare `intent` along with the action, and the `file_write` payload (`path` + `intent`) enters L3 review before dispatch; it is off by default because no launcher starts the MCP service, and nothing is blocked when it does not start. It is not on the kernel's own `check --strict` path. In-execution supervision is still a design and sandbox prototype; post-execution audit is still wired in for personal.
- Controlled verification (actually run, not "import and see green"): `test_capability.py` 10 items, 10 PASS / 0 FAIL; `test_pretool_guard.py` 10 items, 10 PASS / 0 FAIL, 5 dangerous calls denied (≥5), 0 false positives; `test_mcp.py` 27 items, 27 PASS / 0 FAIL. Controlled runs: 10/10 capability, 10/10 pre-tool guard (5 dangerous calls denied, 0 false positives), 27/27 MCP routing.
- The kernel runtime code is unchanged in this release (`bumao_core/` is the same as beta.1); this release is a phase-status and evidence update. Kernel runtime unchanged from `v0.2.0-beta.1`.
- Docs: README gains `Status: maintenance pause` / 「状态：维护暂停，稳定可用」 at the top; new `RETURN_HERE.md` (look at three things first on return, touch `CHANGELOG.md` first, which switches are off by default).
- Known issues unchanged: `contract_test.py` 12 items, 2 FAIL (5 modules not shipped); `A10` only hints when the approval ledger is missing and gives no credential; `op_id` closes only at the personal action level; 103 of the 683 rules are machine-judgeable (15.1%), and 89 are bound by the machine; `error_code` is recorded only at rc=3 per the convention.
- community `check --strict` once showed `4/44`, **never reproduced, cause unknown**; all 18 re-runs showed the `A10` / `A13` two lines.

### 0.2.0-beta.1 — 2026-11-08

The first beta of 0.2; 0.2 itself is not finished.

- Three-cell status: post-execution audit is wired in for personal (four action-row keys, `ledger.py shenji` can export the whole chain); pre-execution constraint and in-execution supervision are still a design and sandbox prototype, **not wired into live**.
- Docs: README gains the "two version spaces" note (kernel `0.10` and release tags are two independent numbering spaces); the Roadmap is explicitly marked as in progress.
- No new execution capability; `bumao_core/` runtime code is unchanged in this release.
- Known issues: `contract_test.py` 12 items, 2 FAIL (5 modules not shipped); `A10` only hints when the approval ledger is missing and gives no credential; `op_id` closes only at the personal action level; 103 of the 683 rules are machine-judgeable (15.1%), and 89 are bound by the machine; `error_code` is recorded only at rc=3 per the convention.
- community `check --strict` once showed `4/44`, **never reproduced, cause unknown**; all 18 re-runs showed the `A10` / `A13` two lines.

### 0.12 — 2026-11-08

This release aligns wording and structure and ships the kernel contract; it adds no execution capability.

- Before: gate `A10` threw `FileNotFoundError` on a fresh checkout, because `kernel_contract.json` was not in the repository. Now: `kernel_contract.json` and `contract_test.py` ship at the repository root — the exact path `engine.py` reads (one level above `bumao_core/`), so `A10` evaluates the contract and reports the missing approval ledger instead of crashing.
- Before: the README opened with gate IDs and internal paths. Now: the first screen answers what it is, who it is for and what it solves, English first, Chinese below (`README.md`).
- Before: no screenshots. Now: one real terminal capture under `docs/screens/` (`test_check_rc.py` output plus the shipped tree).
- No runtime change: `git diff v0.11..HEAD -- bumao_core/` is empty; `engine.py` bytes are unchanged.

Known issues in this batch (documented in `README.md`, not fixed here): `contract_test.py` reports `2 FAIL` because checks `[B]`/`[C]` expect five modules this repo does not ship; `gate_count.py` and `test_equivalence.py` fail on a single-repo clone because they assume sibling checkouts.

Not shipped yet (do not count as done): `runtime_preflight.py`, the second batch of fake-green patches, and the four foreign keys (`op_id` / `rule_id` / `run_id` / `error_code`).

### 0.1 — 2026-11-08

First public release.

- Unified kernel: `engine.py` as the only runtime engine.
- 13 generic gate templates and the host injection contract.
- Shrink guard: `set_expected()` declares the expected set, so failing to register a gate fails the run.
- Three-convention gate counting and the old-vs-new engine equivalence regression.
- Host contract document `bumao_core/HOST_CONTRACT.md`.
