# -*- coding: utf-8 -*-
"""执行前规则审查（beta2）。

判据来源已并入 core 规则体系：本模块不再自带规则表，只把请求交给 core_bridge，
由 core 的规则库装载器、闸门注册表与 jiancha 运行层动作前判定入口给出结论。
五值决策：ALLOW / DENY / REQUIRE_APPROVAL / WARNING / ERROR。
"""
from . import core_bridge


def run(req, cfg, now=None):
    """返回 {decision, error_code, rule_id, checks, core}。异常一律 ERROR，绝不 ALLOW。"""
    try:
        return core_bridge.review(req, cfg, now)
    except Exception as e:
        return {"decision": "ERROR", "error_code": "INTERNAL_ERROR", "rule_id": "G0.99",
                "checks": [{"id": "G0.99", "name": "internal_error",
                            "result": "fail", "detail": "%s: %s" % (type(e).__name__, e)}],
                "core": {}}
