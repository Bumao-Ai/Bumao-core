# -*- coding: utf-8 -*-
"""最小第三方接入示例：不依赖三个产品仓，直接跑一次真实 check。

运行（在仓库根目录，无需 pip install）：

    python examples/minimal_host.py

它做四件事，也就是 HOST_CONTRACT.md §一 的接入四步：
  1. 取内核（import bumao_core.engine）；
  2. configure() 注入一个自备的 rules_db（本文件内实现，满足 12 成员契约的必需项）；
  3. register() 注册一个 B 段闸门，set_expected() 声明期望集；
  4. main(["check", "--strict"]) 跑检查，退出码即结论。

注意：本示例不附带审批册，所以 A10（版本变更授权闸）按设计判 DENY，
check 的退出码会是 1。这不是示例失败，而是内核「没有用户授权就不放行」的默认行为。
"""

import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from bumao_core import engine as core
except ImportError:  # 兼容历史的 sys.path.insert 扁平加载
    sys.path.insert(0, os.path.join(ROOT, "bumao_core"))
    import engine as core


class ExampleRulesDb(object):
    """一个最小但契约完整的 rules_db；真实宿主按同样签名换成自己的规则库。"""

    def __init__(self, rules_dir):
        self.ROOT = rules_dir
        self.HERE = rules_dir
        self.RULES_DIR = rules_dir
        self.ZH = ""

    def load(self):
        return {
            "meta": {"name": "example-host", "version": "1.0.0",
                     "effective": "示例", "zero_rules": False},
            "chapters": [{"ch": 0, "chapter_title": "0. 示例规则", "n": 2}],
            "clauses": [
                {"id": "0.1", "ch": 0, "title": "示例一", "body": ["示例正文"],
                 "broken_refs": []},
                {"id": "0.2", "ch": 0, "title": "示例二", "body": ["示例正文"],
                 "broken_refs": []},
            ],
        }

    def index(self, db):
        return db

    def load_meta(self):
        return self.load()["meta"]

    def dup_ids(self, db):
        ids = [c.get("id") for c in db["clauses"]]
        return sorted({i for i in ids if ids.count(i) > 1})

    def block_broken(self, clauses):
        return []

    def shell_clauses(self, db):
        return []


def main():
    tmp = tempfile.mkdtemp(prefix="bumao_example_")
    # A11 会扫规则目录下的 z*.json；给一个不含绝对路径的空结构即可。
    with open(os.path.join(tmp, "z00.json"), "w", encoding="utf-8") as f:
        f.write('{"ch": 0, "clauses": []}')

    core.configure(ExampleRulesDb(tmp))
    core.register("B1", lambda: (True, "示例闸通过"), "示例：宿主注入的 B 段闸")
    core.set_expected("ExampleHost", frozenset(["B1"]))

    print("=== whoami（宿主接入后的自述） ===")
    core.cmd_whoami()

    print("\n=== check --strict（真实判据） ===")
    rc = core.main(["check", "--strict"])
    print("\n[example] check 退出码 = %d" % rc)
    print("[example] A10 DENY 属预期：本示例不带审批册；"
          "真实宿主由使用者本人在审批册写当日授权条目。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
