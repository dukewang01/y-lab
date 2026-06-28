# y-forecast — 通用时间序列预测

不只是食材价格，房间量、客流量、入座率等任何时间序列都能预测。

## 预测能力

| 数据 | 方法 | 适用场景 |
|------|------|---------|
| 客房预订量 | 季节性ARIMA | 未来30天入住率 |
| 餐厅入座数 | Prophet / 移动平均 | 未来7天客流量 |
| 食材价格 | 加权移动平均+季节性 | 下月采购成本 |
| 能耗用量 | Holt-Winters | 月度水电费 |

## 用法

```python
from forecast import TimeSeriesPredictor

pred = TimeSeriesPredictor()
pred.learn("occupancy", {1: 85, 2: 82, 3: 78, 4: 80})
result = pred.predict("occupancy", steps=7)
```
