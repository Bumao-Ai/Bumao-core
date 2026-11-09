# -*- coding: utf-8 -*-
"""Agent 注册与身份管理 ＋ 能力登记。

一份 agents.json 同时承载身份与能力声明：能力是授权上限，不是建议。
"""
import io
import json
import os
import secrets
import time


def _load(path):
    if not os.path.isfile(path):
        return {"schema": "agents/1", "agents": {}}
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)


class AgentRegistry:
    def __init__(self, path):
        self.path = path

    def all(self):
        return _load(self.path).get("agents") or {}

    def get(self, agent_id):
        return self.all().get(str(agent_id or ""))

    def register(self, agent_id, display="", capabilities=None):
        """登记一个新 Agent；返回明文 secret（只在登记时给一次）。"""
        data = _load(self.path)
        agents = data.setdefault("agents", {})
        aid = str(agent_id or "").strip()
        if not aid:
            raise ValueError("agent_id 不能为空")
        if aid in agents:
            raise ValueError("agent_id 已存在：%s" % aid)
        secret = secrets.token_hex(32)
        agents[aid] = {
            "agent_id": aid,
            "display": display or aid,
            "secret": secret,
            "status": "active",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "revoked_at": "",
            "capabilities": list(capabilities or []),
        }
        _save(self.path, data)
        return agents[aid]

    def revoke(self, agent_id):
        data = _load(self.path)
        rec = (data.get("agents") or {}).get(str(agent_id or ""))
        if not rec:
            return False
        rec["status"] = "revoked"
        rec["revoked_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _save(self.path, data)
        return True

    @staticmethod
    def capability(agent, cap_id):
        for c in (agent or {}).get("capabilities") or []:
            if c.get("id") == cap_id:
                return c
        return None
