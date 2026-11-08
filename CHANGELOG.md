# Changelog

## Unreleased — 2026-11-08

本版为口径与结构对齐（无新增执行能力）。This release is a naming and structure alignment; it adds no execution capability.

- Before: the README opened with gate IDs and internal paths. Now: the first screen answers what it is, who it is for and what it solves, English first, Chinese below (`README.md`).
- Before: no screenshots. Now: one real terminal capture under `docs/screens/` (`test_check_rc.py` output plus the shipped tree).
- No runtime change: `git diff v0.11..HEAD -- bumao_core/` is empty; `engine.py` bytes are unchanged.

Not shipped yet (do not count as done): `runtime_preflight.py`, the second batch of fake-green patches, the four foreign keys (`op_id` / `rule_id` / `run_id` / `error_code`), and the portable desensitized contract.

## 0.1 — 2026-11-08

首次公开发布。

- 统一内核：`engine.py` 作为唯一运行时引擎。
- 13 个通用闸门模板与宿主注入契约。
- 防缩水：`set_expected()` 声明期望集，少注册一个闸门即失败。
- 三口径闸数统计与新旧引擎等价性回归。
- 宿主契约文档 `bumao_core/HOST_CONTRACT.md`。
