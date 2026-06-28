# y-revenue — 动态收益管理

多营收流的价格弹性分析和收益预测。

## 解决的痛点

> 房价、餐厅、宴会厅各自定价，没人知道一个调整对其他部门的影响。

## 能回答的问题

- "如果客房降价10%，总的RevPAR会怎么样？"
- "餐厅提价5%对入座率有多大影响？"
- "宴会厅和餐厅的客源重叠度？"

## 架构

```
revenue/
├── streams/      — 各营收流（客房/餐饮/宴会/其他）
├── elasticity/   — 价格弹性分析
├── forecast/     — 收益预测
└── optimizer/    — 定价优化建议
```

## 用法

```python
from revenue import RevenueManager

rm = RevenueManager()
rm.add_stream("rooms", rev=100000, volume=500, price=200)
rm.add_stream("fb", rev=80000, volume=4000, price_per_customer=200)
rm.optimize()
```
