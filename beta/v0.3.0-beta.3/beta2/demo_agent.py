# -*- coding: utf-8 -*-
"""示例 Agent（beta2）：只能经标准 Adapter 提交，不 import request、不直连 request.build。"""


class DemoAgent:
    def __init__(self, adapter, external_ref, vendor="demo-vendor"):
        self.adapter = adapter
        self.external_ref = external_ref
        self.vendor = vendor

    def envelope(self, op, target, capability="", reason="", params=None):
        return {"schema": "agent_ext/1", "vendor": self.vendor,
                "agent_ref": self.external_ref, "op": op, "target": target,
                "capability": capability, "params": params or {}, "reason": reason}

    def delete_file(self, target, capability="", reason="", params=None, receipt=None):
        return self.adapter.submit(
            self.envelope("file.delete", target, capability, reason, params), receipt=receipt)

    def read_file(self, target, capability="", reason="", params=None, receipt=None):
        return self.adapter.submit(
            self.envelope("file.read", target, capability, reason, params), receipt=receipt)
