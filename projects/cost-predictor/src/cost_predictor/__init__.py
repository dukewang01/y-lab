"""
cost_predictor — 食材成本预测

基于历史采购价格，预测下月食材价格区间。
方法：
  v0.1: 加权移动平均 + 季节性指数
  未来: ARIMA / LightGBM
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import math


@dataclass
class PriceRecord:
    name: str
    history: dict  # {"2026-01": 120, "2026-02": 128, ...}


# ── 行业季节性指数（月份0-11） ──
SEASONALITY = {
    "牛肉":       [1.00, 1.02, 1.00, 0.98, 1.00, 1.03, 1.05, 1.04, 1.02, 1.00, 0.98, 0.97],
    "猪肉":       [1.05, 1.03, 1.00, 0.97, 0.95, 0.93, 0.92, 0.94, 0.97, 1.00, 1.03, 1.05],
    "羊肉":       [1.08, 1.06, 1.03, 1.00, 0.97, 0.95, 0.94, 0.95, 0.97, 1.00, 1.03, 1.06],
    "鸡肉":       [1.00, 0.99, 0.99, 1.00, 1.01, 1.02, 1.02, 1.01, 1.00, 1.00, 0.99, 0.99],
    "基围虾":     [1.00, 1.00, 0.95, 0.88, 0.82, 0.85, 0.90, 1.00, 1.10, 1.15, 1.10, 1.05],
    "老虎斑":     [1.00, 1.00, 1.02, 1.05, 1.10, 1.15, 1.18, 1.15, 1.10, 1.05, 1.00, 0.98],
    "波士顿龙虾": [1.20, 1.18, 1.10, 1.00, 0.92, 0.88, 0.85, 0.88, 0.95, 1.02, 1.10, 1.18],
    "鸡蛋":       [0.98, 0.97, 0.96, 0.97, 1.00, 1.03, 1.05, 1.07, 1.05, 1.02, 1.00, 0.98],
}


class CostPredictor:
    """
    成本预测器

    用法：
        predictor = CostPredictor()

        # 添加历史数据
        predictor.learn("牛肉", {"2026-01": 85, "2026-02": 88, ...})

        # 预测
        result = predictor.predict("牛肉", months_ahead=1)
        print(result)
        # {"name": "牛肉", "current": 92, "predicted": 98, "range": [94, 102], "confidence": 0.81}
    """

    def __init__(self):
        self.records: dict[str, PriceRecord] = {}

    def learn(self, name: str, history: dict):
        """添加或更新一种食材的历史价格"""
        self.records[name] = PriceRecord(name=name, history=history)

    def learn_from_sensor(self, sensor_data: list[dict]):
        """从PriceSensor的数据学习（格式：{name, current, cost_history}）"""
        for item in sensor_data:
            if "cost_history" in item:
                self.learn(item["name"], item["cost_history"])

    def predict(self, name: str, months_ahead: int = 1) -> dict:
        """
        预测食材下月价格。

        Returns:
            {"name": str, "current": float,
             "predicted": float, "range": [low, high],
             "confidence": float, "trend": "up|down|stable"}
        """
        if name not in self.records:
            return {"name": name, "error": "no historical data"}

        record = self.records[name]
        prices = sorted(record.history.items())
        if len(prices) < 2:
            return {"name": name, "error": "need at least 2 data points"}

        # 当前价格（最新）
        current = float(prices[-1][1])

        # 1. 加权移动平均（最近3个月权重更高）
        recent = [float(p[1]) for p in prices[-min(len(prices), 6):]]
        weights = [0.5, 0.3, 0.2] if len(recent) >= 3 else [0.6, 0.4]
        if len(recent) > len(weights):
            recent = recent[-len(weights):]
        wma = sum(p * w for p, w in zip(recent, weights)) / sum(weights)

        # 2. 季节性调整
        now = datetime.now()
        target_month = (now.month - 1 + months_ahead) % 12
        season_factor = 1.0
        if name in SEASONALITY:
            current_season = SEASONALITY[name][(now.month - 1) % 12]
            target_season = SEASONALITY[name][target_month]
            season_factor = target_season / current_season if current_season > 0 else 1.0

        # 3. 预测值
        predicted = round(wma * season_factor, 1)

        # 4. 置信区间
        # 用历史波动幅度估算
        if len(prices) >= 3:
            diffs = [abs(float(prices[i][1]) - float(prices[i-1][1])) / float(prices[i-1][1])
                     for i in range(1, len(prices))]
            avg_volatility = sum(diffs) / len(diffs)
        else:
            avg_volatility = 0.05  # 默认5%

        margin = round(predicted * avg_volatility, 1) if avg_volatility > 0 else round(predicted * 0.05, 1)
        low = round(predicted - margin, 1)
        high = round(predicted + margin, 1)

        # 5. 置信度
        data_points = len(prices)
        max_confidence = min(0.95, 0.5 + data_points * 0.05)
        # 季节性越强，置信度略低
        if name in SEASONALITY:
            max_confidence -= 0.05
        confidence = round(max(max_confidence, 0.3), 2)

        # 6. 趋势
        change = (predicted - current) / current * 100
        if change > 3:
            trend = "up"
        elif change < -3:
            trend = "down"
        else:
            trend = "stable"

        return {
            "name": name,
            "current": current,
            "predicted": predicted,
            "range": [low, high],
            "confidence": confidence,
            "trend": trend,
            "change_pct": round(change, 1),
        }

    def predict_many(self, names: list[str], months_ahead: int = 1) -> list[dict]:
        """批量预测"""
        return [self.predict(n, months_ahead) for n in names]

    def all_predictions(self, months_ahead: int = 1) -> list[dict]:
        """预测所有已学习的食材"""
        results = []
        for name in self.records:
            r = self.predict(name, months_ahead)
            if "error" not in r:
                results.append(r)
        results.sort(key=lambda x: -abs(x.get("change_pct", 0)))
        return results


if __name__ == "__main__":
    # 简单测试
    p = CostPredictor()
    p.learn("牛肉", {"1月": 85, "2月": 88, "3月": 90, "4月": 92, "5月": 95, "6月": 100})
    p.learn("基围虾", {"1月": 55, "2月": 58, "3月": 56, "4月": 52, "5月": 49, "6月": 46})
    p.learn("老虎斑", {"1月": 120, "2月": 125, "3月": 128, "4月": 132, "5月": 138, "6月": 142})
    r = p.predict("牛肉")
    print(r)
