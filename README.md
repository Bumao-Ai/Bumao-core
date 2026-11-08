# Bumao Core

一句话：它不替你决定「该守什么规矩」，只保证你定下的规矩被不折不扣执行，且结论不能被偷偷放宽、跳过或伪造。

- **运行时依赖**：纯 Python 标准库，要求 **Python 3.12 或更高**，不需要 `pip install`。
- **它不是 Python 包**：没有 `__init__.py`、没有 `pyproject.toml`，只能把 `bumao_core/` 加入 `sys.path` 后 `import engine`。
- **它不带任何具体规则**：规则全部由使用它的发行版提供。

## 这个仓里有什么

```
bumao_core/
  engine.py            唯一运行时引擎：装载、注册闸门、跑 check、给唯一结论
  gate_registry.py     期望集与防缩水校验
  gate_count.py        三口径闸数统计（AST 注册数 / 声明数 / 运行时结论数）
  test_equivalence.py  新旧引擎等价性回归
  bumao_core_gates.py  13 个通用闸门模板（宿主注入函数契约）
  bumao_core_rules.py  三种规则格式的参考装载器
  test_check_rc.py     退出码回归测试
  HOST_CONTRACT.md     宿主必须实现的 12 个契约成员
assets/                官方 Logo
```

## 快速开始

```python
import sys
sys.path.insert(0, "path/to/bumao_core")
import engine as core

core.configure(rules_db_module=my_rules_db)   # 必须最先调用
core.register("B1", my_gate, "我的第一个闸门")
core.set_expected("MyEdition", frozenset(["B1"]))
raise SystemExit(core.main(["check", "--strict"]))   # 退出码即结论
```

命令行子命令：`whoami`、`check`（`--strict`）、`audit`、`bump`、`show <条款id>`、`selftest`、`refresh`。

接入前请先读 [`bumao_core/HOST_CONTRACT.md`](bumao_core/HOST_CONTRACT.md)，那里写着宿主必须实现的 12 个成员。

## 它不做什么

- 不是服务、不是 SDK、不是运行时：Web 应用不会「跑在它上面」，只会「调它做一次 check」。
- 不知道发行版身份，也不内置任何发行版的名字。
- 不判断规则内容本身好不好，只判断规则是否自洽、是否被完整执行。

## 配套仓库

- `bumao-xtgl-community`：带 56 条通用规则的完整发行版
- `bumao-xtgl-minimal`：不带规则的骨架发行版

两个发行版都需要把本仓的 `bumao_core/` 放到它们**上一级目录**的 `kernel/` 下，详见各自的 README。

## 许可

Copyright 2026 Bumao

Licensed under the Apache License, Version 2.0. 全文见 [`LICENSE`](LICENSE)。
商标与品牌使用边界见 [`TRADEMARK.md`](TRADEMARK.md)。
