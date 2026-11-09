# RETURN_HERE — resume here

Status: maintenance pause · 状态：维护暂停，稳定可用

Iteration is paused; the current prerelease is stable and usable as-is. When work resumes, start from this file.
迭代已暂停；当前预发行稳定可用。恢复迭代时，从这份文件开始。

## Look at these three first · 先看这三样

1. **Which version space you are in**
   `git tag --sort=-v:refname | head -4` (stable `v0.2.6`, prerelease `v0.3.0-beta.4`) and `kernel_contract.json` (`0.10`). These are independent numbers.
   先分清两个版本空间：稳定 tag `v0.2.6`、预发行 `v0.3.0-beta.4`、`kernel_contract.json` 的 `0.10`。

2. **The current verdict, twice**
   `python bumao_core/test_check_rc.py` (expect one PASS) and `python contract_test.py` (12 items, 0 FAIL, 3 N/A — the three are scripts outside the contract face). Two runs must agree before you trust them.
   先跑 `test_check_rc.py` 与 `contract_test.py`；后者 12 项 0 FAIL、3 N/A（3 项为契约范围外脚本），两次一致才算基线。

3. **What landed**
   Read the top entry of `CHANGELOG.md` and the `Roadmap (0.2 — live in the maintainer's edition)` section of `README.md`. The three pieces and the 2026-11-09 live replay are listed there.
   读 `CHANGELOG.md` 最上面一条与 README 的 Roadmap：三格状态写在那里。

## Default-off switches · 默认关闭的开关

- **MCP server** — no launcher starts it; pre-execution intent only applies when you start it yourself.
- **`intent`** — optional in the schema; every `file_write` still goes through the L3 review before dispatch.
- **In-flight supervision** — ships in-repo as `bumao_core/jiancha/`; `BUMO_JIANCHA_MODE` defaults to `off`; the maintainer's live edition replayed it on 2026-11-09.
- **`error_code`** — recorded only when `rc=3`, by the declared convention.

## Touch this file first · 先动这个文件

`CHANGELOG.md` — open the new version entry before editing any code, and say which of the three pieces actually moved.
先开 `CHANGELOG.md` 的新版本条目，并写明三格里哪一格真的动了；再改代码。

Then run the two checks twice and compare before committing.
然后连跑两次检查，两次一致再提交。
