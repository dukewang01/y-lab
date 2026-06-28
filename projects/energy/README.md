# y-energy — 能耗追踪系统

酒店水电燃气等能耗的日/周/月监控和异常检测。

## 解决的痛点

> 能耗账单来了才知道超了，没法及时发现异常。

## 架构

```
energy/
├── monitor/      — 实时能耗监控（水/电/气/蒸汽）
├── anomaly/      — 异常波动检测（环比/同比）
├── benchmark/    — 行业对标（同类酒店能耗对比）
└── report/       — 能耗报告
```

## 用法

```python
from energy import EnergyMonitor

mon = EnergyMonitor()
mon.record("electricity", date="2026-06-28", kwh=5200)
mon.record("water", date="2026-06-28", m3=120)
anomalies = mon.detect_anomalies()
```
