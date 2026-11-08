# Bumao Core

![license](https://img.shields.io/badge/license-Apache--2.0-blue)
![python](https://img.shields.io/badge/python-3.12%2B-blue)
![gates](https://img.shields.io/badge/gate%20templates-13-brightgreen)
![runtime](https://img.shields.io/badge/runtime-stdlib%20only-informational)

Stdlib-only rule-execution kernel for AI agents: one written rule set in, one deterministic `ALL PASS` / `FAIL` verdict out — and the verdict cannot be silently loosened.

**What it is** — a kernel, not a framework. It ships no rules of its own.
**Who it's for** — developers building their own host who want the same verdict logic underneath.
**What it solves** — the same rule set being judged differently by different implementations.

![Kernel self-test](docs/screens/selftest.png)
*Real output: `test_check_rc.py` plus the shipped `bumao_core/` tree. Terminal capture, no mock UI.*

## Quick start (30 seconds)

```bash
git clone https://github.com/Bumao-Ai/Bumao-core.git
```

```python
import sys
sys.path.insert(0, "path/to/bumao_core")
import engine as core

core.configure(rules_db_module=my_rules_db)      # must be called first
core.register("B1", my_gate, "my first gate")
core.set_expected("MyEdition", frozenset(["B1"])) # anti-shrink baseline
raise SystemExit(core.main(["check", "--strict"]))# exit code is the verdict
```

Subcommands: `whoami`, `check` (`--strict`), `audit`, `bump`, `show <clause-id>`, `selftest`, `refresh`.

## Proof of work

| Item | Value | Source |
|---|---|---|
| Commits | 2 | `git rev-list --count HEAD` (before this facade commit) |
| Last commit | 2026-11-08 | `git log -1 --date=short` |
| Check items | 13 gate templates | `bumao_core/bumao_core_gates.py` (`make_*_gate`) |
| Reverse cases | 1 | `python test_check_rc.py` → `PASS` |
| Defect ledger | not kept in this repo | — |
| Releases | 2 tags, `v0.1` → `v0.11`, both 2026-11-08 | `git tag` |
| Changelog | [CHANGELOG.md](CHANGELOG.md) | — |

## 中文

- **是什么**：一个内核，不是框架；本身不含任何具体规则。
- **给谁用**：要自己搭宿主、但想复用同一套判定逻辑的开发者。
- **解决什么**：同一份规则在不同实现里被判出不同结论。

快速开始沿用上方代码块。宿主必须实现的 12 个成员见 [`bumao_core/HOST_CONTRACT.md`](bumao_core/HOST_CONTRACT.md)；配套发行版见 `bumao-xtgl-community`（59 rules / 44 checks）与 `bumao-xtgl-minimal`（0 rules / 28 checks）。

## Roadmap (0.2 — in progress)

Three pieces are under construction. None of them is shipped in this release.

1. **Pre-execution constraint** — declare intent before acting; the kernel judges the intent before the action runs.
2. **In-flight supervision** — check continuously while the action is in progress, not only at the end.
3. **Post-execution audit** — link action, basis, result and exception into one traceable chain.

Status: **in progress**. This section is a commitment, not a claim of completion.

## Architecture

```mermaid
flowchart LR
  H[Host application] --> W[Edition wrapper]
  W --> E[engine.py]
  E --> R[gate_registry.py]
  E --> G[bumao_core_gates.py<br/>13 templates]
  R --> D{expected set matches?}
  D -->|yes| P[ALL PASS]
  D -->|no| F[FAIL]
```

## What gets checked

| Area | Templates | Examples |
|---|---|---|
| Rule source structure | 6 | chapter count, unique IDs, contiguous blocks, missing keys, shell clauses, broken references |
| Rendered views | 2 | view drift, render idempotence |
| Repository layout | 2 | root files not flat, sub-directory naming |
| Hygiene | 3 | PII/path scan, stale lock, version syntax |

Total: 13 gate templates. A host supplies the rule set and the gate functions; the kernel supplies the contract, the registry and the verdict.

## Layout

```
bumao_core/
  engine.py            唯一运行时引擎
  gate_registry.py     expected-set registry and anti-shrink checks
  gate_count.py        three-caliber gate counting
  bumao_core_gates.py  13 reusable gate templates
  bumao_core_rules.py  reference loaders for three rule formats
  test_check_rc.py     exit-code regression
  test_equivalence.py  engine equivalence regression
  HOST_CONTRACT.md     the 12 members a host must implement
assets/                official logos
```

## Docs / License

- Host contract: [`bumao_core/HOST_CONTRACT.md`](bumao_core/HOST_CONTRACT.md)
- Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md) · DCO: [`DCO`](DCO)
- Security: [`SECURITY.md`](SECURITY.md)
- License: Apache-2.0, see [`LICENSE`](LICENSE)
- Trademark boundary: [`TRADEMARK.md`](TRADEMARK.md)

Copyright 2026 Bumao
