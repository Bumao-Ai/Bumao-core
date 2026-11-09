# beta1 —— Bumao Core 0.3 最小可跑骨架

- 性质：沙盒实验件，不参与任何已发布产品
- 位置：`D:\XJQITA\GCML_lab\v0.3_20261109\beta1`
- 解释器实测：`D:\XJQITA\HSYX\Python\python.exe`（Python 3.12.4）
- 运行：`& "D:\XJQITA\HSYX\Python\python.exe" run_beta1.py`
- 退出码：0 = 五步链路 + 7 条反向用例全部符合预期且账本链无断点

## 目录结构

```
beta1/
├─ beta1_canshu.json          参数件（工作区、账本、种子、规则集）
├─ rules_beta1.json           规则包（R0.1–R0.11，含五值决策映射）
├─ run_beta1.py               五步链路实跑入口
├─ agentos/
│  ├─ identity.py             Agent 注册与身份管理 ＋ 能力登记
│  ├─ request.py              req/1 统一操作请求（结构校验＋HMAC 签名）
│  ├─ review.py               执行前规则审查（五值决策，rule_id 口径沿用 0.2）
│  ├─ evidence.py             act/1 证据记录（四外键＋审批占位）
│  └─ query.py                只读查询与链完整性状态
├─ vendor/
│  └─ ledger.py               0.2 jiancha/ledger.py 逐字副本（哈希链账本）
└─ workspace/                 示例目标（approved / review / _frozen）
```

## 复用（不重写）

- 哈希链账本：`vendor/ledger.py` 与 `D:\XJQITA\GCML_lab\v0.2_261108_jiancha\jiancha\ledger.py`
  **字节级一致**（SHA256 见本轮报告）。
- 四外键口径：`op_id`／`run_id`／`rule_id`／`error_code`，与 0.2 票链同名同义。
- `rule_id` 取值：最先失败项 id；无失败取最后通过项 id（沿用 0.2 `supervisor._rule_id` 规则）。

## beta1 做到了什么

1. 统一请求 `req/1`：9 个字段，缺项/类型错/schema 不符一律 `ERROR`；
2. 身份与能力：注册、能力声明、HMAC 验签、撤销位、nonce 防重放；
3. 规则审查：`ALLOW`／`DENY`／`REQUIRE_APPROVAL`／`WARNING`／`ERROR` 五值均实跑出现；
4. 证据记录：Agent 身份、请求摘要、时间、规则版本、命中规则、决策、审批占位、异常、四外键；
5. 回查：按 `op_id` 命中；`verify()` 链断点为空。

## beta1 没做到什么（明确边界）

- 只有 CLI 只读查询，没有 Web 控制台；
- 没有真实宿主接线（MCP／personal 适配器只是接口占位，未接生产）；
- 审批人身份未签名，审批结果仅占位字段；
- 没有并发与锁，单进程顺序跑；
- 没有把规则审查接到 core 的 `gate_registry` 实例上（复用其口径，未做注册期接线）；
- 十项验收条件原文未送达，beta1 只覆盖任务明示的五步链路。
