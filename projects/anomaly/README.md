# y-anomaly — 数据异常检测

营收/成本/能耗/客流等指标的自动异常标记。

## 检测维度

| 维度 | 方法 | 示例 |
|------|------|------|
| 点异常 | Z-score / IQR | 某天营收突然跌50% |
| 上下文异常 | 滑动窗口 | 周末客流突然不如工作日 |
| 集体异常 | 移动平均偏差 | 连续一周营收下降 |
| 季节性偏差 | 同比+环比 | 6月能耗比去年高30% |

## 用法

```python
from anomaly import AnomalyDetector

ad = AnomalyDetector()
ad.learn("daily_revenue", [80000, 82000, 79000, 40000, 81000])
flagged = ad.detect()
```
