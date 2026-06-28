# y-risk — 风险管理系统

酒店风险登记册+预案管理+专项跟踪。

## 解决的痛点

> 风险评估靠拍脑袋，整改追踪靠人盯，出了事才发现预案不存在。

## 架构

```
risk/
├── matrix/       — 风险登记册（可能性×严重性=风险等级）
├── plan/         — 应急预案库
├── track/        — 问题整改追踪
└── report/       — 风险报告
```

## 风险矩阵

```
严重性\可能性 | 极低 | 低 | 中 | 高 | 极高
    轻微     | 低   | 低 | 低 | 中 | 中
    一般     | 低   | 中 | 中 | 高 | 高
    严重     | 中   | 中 | 高 | 高 | 极高
    致命     | 中   | 高 | 高 | 极高 | 极高
```

## 用法

```python
from risk.risk_matrix import RiskMatrix
from risk import RiskManager

mgr = RiskManager()
mgr.register("电梯故障", likelihood=3, severity=4)
report = mgr.assess()
```
