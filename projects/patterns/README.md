# y-patterns — 酒店运营分析模式库

常用数据分析模式的模板和源码。

## 模式列表

| 模式 | 适用场景 |
|------|---------|
| BCG矩阵分析 | 菜品/产品/渠道分类 |
| RFM分段 | 客户价值分层 |
| 帕累托分析 | 找到20%贡献80%的关键因素 |
| 同比/环比分析 | 业绩对标 |
| 趋势分解 | 季节性/趋势/残差 |
| 归因分析 | 投诉/好评的背后原因 |
| 关联规则 | 找出一起点的菜品/产品组合 |
| 预测区间 | 用历史数据估算未来波动范围 |

## 用法

```python
from patterns.bcg import bcg_matrix
from patterns.rfm import rfm_segment
from patterns.pareto import pareto_analysis
```
