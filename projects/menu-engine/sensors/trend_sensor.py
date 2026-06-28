"""
sensors/trend_sensor.py — 消费趋势传感器
模拟追踪当前热门口味、菜系趋势。
"""
from collections import Counter
import random


# 模拟"当前热门"关键词
TREND_TAGS = [
    "spicy", "sour-spicy", "light", "seafood", "beef",
    "vegetarian", "salad", "sashimi", "bbq", "hotpot",
    "fusion", "comfort food", "healthy", "low-carb",
    "中西融合", "酸辣", "清淡", "海鲜", "烧烤",
    "轻食", "素食", "国潮", "传统", "创新",
]

# 口味权重（模拟搜索指数 / 社交媒体提及）
TREND_WEIGHTS = {
    "spicy": 85, "sour-spicy": 72, "light": 68, "seafood": 65,
    "beef": 55, "healthy": 52, "low-carb": 48, "fusion": 45,
    "vegetarian": 42, "salad": 40, "bbq": 38,
    "酸辣": 78, "清淡": 70, "海鲜": 62, "轻食": 55,
    "国潮": 50, "烧烤": 45,
}


class TrendSensor:
    """
    消费趋势传感器。

    用法：
        sensor = TrendSensor()
        trends = sensor.hot_right_now()
        print(trends)
        # [{"tag": "酸辣", "score": 78}, ...]

        trends = sensor.monthly_trend(month=6)
    """

    def hot_right_now(self, top_n: int = 10) -> list[dict]:
        """
        返回当前热门口味/关键词。
        score越高越热门。
        """
        items = list(TREND_WEIGHTS.items())
        # 模拟轻度随机抖动
        items = [(k, v + random.randint(-5, 5)) for k, v in items]
        items.sort(key=lambda x: -x[1])
        return [{"tag": k, "score": max(v, 0)} for k, v in items[:top_n]]

    def monthly_trend(self, month: int = None) -> list[dict]:
        """
        模拟月度趋势变化。
        返回本月 vs 上月 vs 去年同期对比。
        """
        if month is None:
            import datetime
            month = datetime.datetime.now().month

        this_month = self.hot_right_now(15)

        # 模拟上月数据（部分标签有变化）
        results = []
        for item in this_month:
            tag = item["tag"]
            this_score = item["score"]
            last_score = this_score + random.randint(-10, 10)
            yoy_score = last_score + random.randint(-5, 5)

            pct_mom = round((this_score - last_score) / last_score * 100, 1)
            pct_yoy = round((this_score - yoy_score) / yoy_score * 100, 1)

            results.append({
                "tag": tag,
                "score": this_score,
                "last_month": last_score,
                "year_ago": yoy_score,
                "mom_change_pct": pct_mom,
                "yoy_change_pct": pct_yoy,
            })

        results.sort(key=lambda x: -x["score"])
        return results
