# -*- coding: utf-8 -*-
"""req/1 —— 统一操作请求接口（唯一入口）。

结构固定为 9 个字段，多一个少一个都不受理；签名覆盖规范化串。
"""
import hashlib
import hmac
import json
import time
import uuid

SCHEMA = "req/1"
FIELDS = ("schema", "agent_id", "capability", "action_type", "target",
          "params", "nonce", "ts", "sig")


class RequestError(ValueError):
    def __init__(self, code, detail=""):
        ValueError.__init__(self, detail or code)
        self.code = code
        self.detail = detail or code


def canonical(req):
    """规范化串：只取被签名的 8 个业务字段，sort_keys 保证可复算。"""
    body = {}
    for k in ("schema", "agent_id", "capability", "action_type",
              "target", "params", "nonce", "ts"):
        body[k] = req.get(k)
    return json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sign(secret, req):
    return hmac.new(str(secret).encode("utf-8"),
                    canonical(req).encode("utf-8"),
                    hashlib.sha256).hexdigest()


def request_sha256(req):
    return hashlib.sha256(canonical(req).encode("utf-8")).hexdigest()


def validate(req):
    """结构校验。任何不合规一律 ERROR，不猜、不兜底。"""
    if not isinstance(req, dict):
        raise RequestError("INVALID_SCHEMA", "请求不是 JSON 对象")
    missing = [k for k in FIELDS if k not in req]
    if missing:
        raise RequestError("INVALID_SCHEMA", "缺字段：%s" % ",".join(missing))
    if req.get("schema") != SCHEMA:
        raise RequestError("INVALID_SCHEMA", "schema=%r 应为 %r" % (req.get("schema"), SCHEMA))
    for k in ("agent_id", "capability", "action_type", "target", "nonce", "sig"):
        if not isinstance(req.get(k), str) or not req.get(k).strip():
            raise RequestError("INVALID_SCHEMA", "%s 必须是非空字符串" % k)
    if not isinstance(req.get("params"), dict):
        raise RequestError("INVALID_SCHEMA", "params 必须是对象")
    try:
        int(req.get("ts"))
    except (TypeError, ValueError):
        raise RequestError("INVALID_SCHEMA", "ts 必须是整数")
    return dict(req)


def build(agent_id, capability, action_type, target, secret,
          params=None, nonce=None, ts=None):
    """示例 Agent 侧：拼一条已签名请求（Agent 只能这样提交）。"""
    req = {
        "schema": SCHEMA,
        "agent_id": agent_id,
        "capability": capability,
        "action_type": action_type,
        "target": target,
        "params": params or {},
        "nonce": nonce or uuid.uuid4().hex,
        "ts": int(ts if ts is not None else time.time()),
        "sig": "",
    }
    req["sig"] = sign(secret, req)
    return req
