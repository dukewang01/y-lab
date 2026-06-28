"""
sensors/price_index.py — 食材批发市场价格传感器
模拟从全国农产品批发市场价格信息网拉数据。
"""
import json, random
from datetime import datetime, timedelta


# 常见食材的基础价格参考（元/公斤）
COMMODITY_BASE_PRICES = {
    "牛肉": 75, "羊肉": 68, "猪肉": 28, "鸡肉": 18,
    "基围虾": 60, "老虎斑": 128, "波士顿龙虾": 280, "珍宝蟹": 298,
    "鸡蛋": 10, "牛奶": 12, "大米": 5, "面粉": 4,
    "土豆": 3, "番茄": 6, "西兰花": 8, "生菜": 5,
    "苹果": 8, "橙子": 7, "草莓": 20,
}

# 季节性波动因子（月份索引0-11）
SEASONAL_FACTORS = {
    "基围虾": [1.0, 1.0, 0.9, 0.85, 0.8, 0.85, 0.9, 1.0, 1.1, 1.15, 1.1, 1.05],
    "老虎斑": [1.0, 1.0, 1.05, 1.1, 1.15, 1.2, 1.2, 1.15, 1.1, 1.05, 1.0, 0.95],
    "波士顿龙虾": [1.2, 1.2, 1.1, 1.0, 0.9, 0.85, 0.85, 0.9, 1.0, 1.05, 1.1, 1.15],
    "草莓": [0.8, 0.8, 0.8, 0.9, 1.0, 1.3, 1.5, 1.5, 1.3, 1.0, 0.9, 0.8],
}


class PriceSensor:
    """
    批发市场价格传感器。

    用法：
        sensor = PriceSensor()
        data = sensor.query(["牛肉", "基围虾"])
        print(data)
        # [{"name": "牛肉", "current": 78, "trend": "up", "change_pct": 4.0}, ...]
    """

    def __init__(self, base_prices: dict = None):
        self.base = base_prices or COMMODITY_BASE_PRICES.copy()
        self.seasonal = SEASONAL_FACTORS.copy()
        self._simulate_today = None  # 可覆盖日期

    def _today(self) -> datetime:
        return self._simulate_today or datetime.now()

    def _noise(self) -> float:
        """模拟市场随机波动 ±3%"""
        return 1 + (random.random() - 0.5) * 0.06

    def _seasonal_factor(self, name: str, month: int) -> float:
        if name in self.seasonal:
            return self.seasonal[name][month]
        return 1.0

    def query(self, ingredients: list[str] = None) -> list[dict]:
        """
        查询当前批发价格。

        Args:
            ingredients: 食材名称列表，None=全部基础食材

        Returns:
            [{"name": str, "current": float, "unit": "kg",
              "trend": "up|down|stable",
              "change_pct": float}, ...]
        """
        today = self._today()
        month = today.month - 1
        names = ingredients or list(self.base.keys())

        results = []
        for name in names:
            if name not in self.base:
                continue
            base = self.base[name]
            season = self._seasonal_factor(name, month)
            noise = self._noise()
            price = round(base * season * noise, 1)

            # 趋势判断
            yesterday = round(base * season * (1 + (random.random() - 0.5) * 0.04), 1)
            change = round((price - yesterday) / yesterday * 100, 1)

            if change > 2:
                trend = "up"
            elif change < -2:
                trend = "down"
            else:
                trend = "stable"

            results.append({
                "name": name,
                "current": price,
                "unit": "kg",
                "trend": trend,
                "change_pct": change,
            })

        return results

    def get_price_for(self, menu_item_name: str) -> dict | None:
        """
        根据菜品名猜测主要食材，返回价格。
        需要简单的菜品-食材映射，这里用关键词匹配。
        """
        for ingredient in self.base:
            if ingredient in menu_item_name:
                matches = self.query([ingredient])
                return matches[0] if matches else None
        return None
