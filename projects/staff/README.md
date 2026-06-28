# y-staff — 智能排班优化

基于客流量预测的酒店员工排班工具。

## 解决的痛点

> 忙的时候人不够，闲的时候人太多。排班靠经验，结果总是不准。

## 架构

```
staff/
├── demand/       — 客流量预测（过去数据→未来需求）
├── schedule/     — 自动排班（需求→排班方案）
├── cost/         — 人力成本分析
└── report/       — 排班报告+偏差分析
```

## 用法

```python
from staff import StaffOptimizer

opt = StaffOptimizer()
opt.set_demand(monday=120, tuesday=80, ...)
schedule = opt.optimize(max_staff=20, min_staff=5)
```
