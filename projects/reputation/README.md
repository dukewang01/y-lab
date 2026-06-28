# y-reputation — 舆情监控系统

OTA点评自动分析+情感评分+问题归因。

## 解决的痛点

> 300条OTA评论，没人有时间逐条看完、更没人会统计趋势。

## 架构

```
reputation/
├── fetch/        — 点评数据采集（携程/美团/Google）
├── sentiment/    — 情感分析（正面/中性/负面）
├── attribution/  — 问题归因（设施/服务/卫生/位置）
└── report/       — 舆情周报
```

## 用法

```python
from reputation import ReputationTracker

rt = ReputationTracker()
rt.ingest("房间很干净，但空调噪音太大", rating=4)
rt.ingest("早餐品种丰富，非常满意", rating=5)
report = rt.summary()
```
