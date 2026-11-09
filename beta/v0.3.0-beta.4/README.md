# Bumao Core 0.3 · beta.4（只改文案，不动代码）

本目录是 `v0.3.0-beta.4` 的全部内容。

## 这一版改了什么

- 只改文案，不改代码：代码、配置与判据与 `v0.3.0-beta.2` 逐字节相同，本版不发任何代码变更。
- 随包收录规划原文 `0.3_guihua_261109.md`（7,479 字节，SHA256 `28ce30eb487fd312f81d530933cbb946b674beb841a9abd20eb0d2785a4863c6`），使计划书与差距分析里对它的引用在包内成立。
- 包内 `beta2/README.md`、`beta2/YANSHOU.md` 的标题与自述改为「随 beta.4 收录、代码与 beta.2 逐字节相同」，不再自称「本目录是 beta.2 的全部内容」。
- 对 beta.2 的中文只做**一处**修订：`beta2/YANSHOU.md` 第 5 项边界句由
  `无。第 5 项的边界：core 原生件覆盖…` 改为
  `无。第 5 项的边界如实标注：core 原生件覆盖…`
  （+4 个汉字 = 12 字节；`beta/v0.3.0-beta.2` 目录版 9,128 → 9,140 字节，与 beta.3 版一致）。除此一处，中文正文逐字节保留；本版另按上一条改了标题与首段，故 `beta2/YANSHOU.md` 在本包中为 9,455 字节。

## 包里有什么

```
v0.3.0-beta.4/
  README.md                     本文件
  0.3_guihua_261109.md          规划原文（逐字收录，7,479 字节）
  0.3_jihua_261109.md           0.3 长期任务计划书（中英对照）
  0.3_chaju_fenxi_261109.md     八项功能与 core 现状差距分析（中英对照）
  beta2/                        beta.2 的可运行骨架，原样收录（27 个文件）
```

共 31 个文件。

## 怎么跑

前置：Python 3.8+，无第三方依赖。

```
cd beta2
python run_beta2.py          # 末行 rc=0，21/21 项符合预期
python query_cli.py --status
python query_cli.py --op <op_id>
python query_cli.py --pending
```

`run_beta2.py` 每次运行会重建 `beta2/run/` 与 `beta2/workspace/`。入口脚本名与末行文字沿用 beta2，属原样保留，不代表本包是 beta.2。

## 元数据与账本标识（刻意不改）

`beta2/meta.json` 的 `version`（`0.3.0-beta2`）、`beta2/beta2_canshu.json` 的 `schema`／`chain_seed`／`core_chain_seed`、`beta2/rules/r01.json` 的章节名、`beta2/core_rules_jieru.json` 的 `rule_set`／`approved_by` 一律保留 beta.2 标识：改了会让已发 beta.2 的账本口径分叉，已发记录无法同口径比对。

## 各 beta 互不覆盖

- tag：`v0.3.0-beta.1`、`v0.3.0-beta.2`、`v0.3.0-beta.3`、`v0.3.0-beta.4` 各自独立，不改、不删、不移动。
- Release 与资产：beta.1／beta.2／beta.3 的 Release 与 zip／SHA256SUMS 原样保留；本版另发一个 Pre-release，不复用、不覆盖。

## 版本

本版为 Pre-release，不是正式版。beta.3 → beta.4 按同档 +0.01 晋升。

---

# English Version

# Bumao Core 0.3 · beta.4 (documentation only, no code changes)

This directory contains the entire contents of `v0.3.0-beta.4`.

## What changed in this version

- Documentation only, no code changes: the code, configuration and criteria are byte-identical to `v0.3.0-beta.2`; this version ships no code change.
- The planning source text `0.3_guihua_261109.md` is included in the package (7,479 bytes, SHA256 `28ce30eb487fd312f81d530933cbb946b674beb841a9abd20eb0d2785a4863c6`), so that the references to it in the plan and the gap analysis resolve inside the package.
- The title and self-description of `beta2/README.md` and `beta2/YANSHOU.md` inside the package now read "included with beta.4, code byte-identical to beta.2" instead of "this directory is the entire contents of beta.2".
- Exactly **one** Chinese revision is made to beta.2: in `beta2/YANSHOU.md`, the Item 5 boundary sentence changes from
  `无。第 5 项的边界：core 原生件覆盖…` to
  `无。第 5 项的边界如实标注：core 原生件覆盖…`
  (+4 Chinese characters = 12 bytes; the copy under `beta/v0.3.0-beta.2` goes from 9,128 to 9,140 bytes, matching the beta.3 copy). Apart from that single spot, the Chinese body is preserved byte for byte; this version also changes the title and opening paragraph per the bullet above, so `beta2/YANSHOU.md` is 9,455 bytes in this package.

## What is in the package

```
v0.3.0-beta.4/
  README.md                     this file
  0.3_guihua_261109.md          planning source text (included verbatim, 7,479 bytes)
  0.3_jihua_261109.md           0.3 long-term task plan (bilingual)
  0.3_chaju_fenxi_261109.md     gap analysis of the eight features vs core (bilingual)
  beta2/                        beta.2's runnable skeleton, included as-is (27 files)
```

31 files in total.

## How to run

Prerequisite: Python 3.8+, no third-party dependencies.

```
cd beta2
python run_beta2.py          # last line rc=0, 21/21 items met expectations
python query_cli.py --status
python query_cli.py --op <op_id>
python query_cli.py --pending
```

Each run of `run_beta2.py` rebuilds `beta2/run/` and `beta2/workspace/`. The entry-script name and the last-line wording keep the beta2 label as-is; this does not mean the package is beta.2.

## Metadata and ledger identifiers (deliberately unchanged)

The `version` in `beta2/meta.json` (`0.3.0-beta2`), the `schema` / `chain_seed` / `core_chain_seed` in `beta2/beta2_canshu.json`, the chapter title in `beta2/rules/r01.json`, and the `rule_set` / `approved_by` in `beta2/core_rules_jieru.json` all keep the beta.2 identifiers: changing them would fork the ledger convention of the already-published beta.2, making the published records no longer comparable on the same footing.

## Betas do not overwrite each other

- Tags: `v0.3.0-beta.1`, `v0.3.0-beta.2`, `v0.3.0-beta.3` and `v0.3.0-beta.4` are independent; none is changed, deleted or moved.
- Releases and assets: the Releases and zip / SHA256SUMS of beta.1, beta.2 and beta.3 are kept as-is; this version adds a separate Pre-release and reuses or overwrites nothing.

## Version

This version is a Pre-release, not an official release. beta.3 → beta.4 advances by +0.01 within the same tier.
