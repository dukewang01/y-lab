"""
menu_advisor — 菜单调整建议引擎

整合成本波动 + 客户偏好 + 投诉情绪 + 菜单健康，
自动生成下月菜单调整方案。
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MenuItem:
    name: str
    outlet: str
    selling_price: float
    category: str = ""
    cost_rate: Optional[float] = None  # 食材成本率
    appearances: int = 0               # 销量/出镜次数


@dataclass
class Suggestion:
    action: str          # "涨价" / "降价" / "改良" / "下架" / "新增" / "推广"
    target: str          # 目标菜品或方向
    priority: str        # "high" / "medium" / "low"
    reason: str          # 建议理由
    detail: str = ""     # 具体方案


# ── 建议规则（可配置） ──
RULES = {
    "cost_up_then_raise_price": {
        "condition": "食材成本上涨>5%且菜品售价>100",
        "action": "涨价",
        "priority": "high",
    },
    "cost_down_then_promote": {
        "condition": "食材成本下降>5%",
        "action": "推广",
        "priority": "medium",
    },
    "complaint_high_then_improve": {
        "condition": "投诉率高",
        "action": "改良",
        "priority": "high",
    },
    "preference_trend_new_items": {
        "condition": "口味趋势上升",
        "action": "新增",
        "priority": "medium",
    },
    "dog_on_menu_for_3_months": {
        "condition": "菜单健康度=Dog且连续3月",
        "action": "下架",
        "priority": "high",
    },
    "star_promote": {
        "condition": "菜单健康度=Star",
        "action": "推广",
        "priority": "low",
    },
}


class MenuAdvisor:
    """
    菜单顾问

    用法：
        advisor = MenuAdvisor()

        # 输入数据
        advisor.set_menu(items)
        advisor.set_cost_trends([{"name":"牛肉","change_pct":14}])
        advisor.set_complaints([{"category":"菜品/quality"}, ...])
        advisor.set_preferences({"辣": 23, "清淡": 15})
        advisor.set_menu_health({"stars": ["和牛"], "dogs": ["炸鸡"]})

        # 生成建议
        suggestions = advisor.advise(outlet="YUXI")
    """

    def __init__(self):
        self.menu: list[MenuItem] = []
        self.cost_trends: list[dict] = []
        self.complaints: list[dict] = []
        self.preferences: dict = {}
        self.menu_health: dict = {}

    def set_menu(self, items: list[MenuItem]):
        self.menu = items

    def set_cost_trends(self, trends: list[dict]):
        """趋势格式：[{"name": "牛肉", "current": 100, "predicted": 110, "change_pct": 10}]"""
        self.cost_trends = trends

    def set_complaints(self, complaints: list[dict]):
        self.complaints = complaints

    def set_preferences(self, prefs: dict):
        """偏好格式：{"辣": 23, "清淡": 15}"""
        self.preferences = prefs

    def set_menu_health(self, health: dict):
        """健康格式：{"stars": [...], "cash_cows": [...], "plow_horses": [...], "dogs": [...]}"""
        self.menu_health = health

    def advise(self, outlet: str = "") -> list[Suggestion]:
        """生成菜单调整建议"""
        suggestions = []

        # 1. 成本驱动建议
        for trend in self.cost_trends:
            name = trend.get("name", "")
            change = trend.get("change_pct", 0)
            if change > 5:
                # 查找菜单中用到此食材的菜品
                affected = [m for m in self.menu
                            if name in m.name and (not outlet or m.outlet == outlet)]
                for item in affected:
                    suggestions.append(Suggestion(
                        action="涨价",
                        target=item.name,
                        priority="high",
                        reason="{:+}%".format(change),
                        detail="食材{}上涨{:+}%，建议{}提价{:.0f}%".format(
                            name, change,
                            item.name[:12],
                            change * 0.3
                        ),
                    ))
            elif change < -5:
                affected = [m for m in self.menu
                            if name in m.name and (not outlet or m.outlet == outlet)]
                for item in affected:
                    suggestions.append(Suggestion(
                        action="推广",
                        target=item.name,
                        priority="medium",
                        reason="食材降价{:+}%".format(change),
                        detail="食材{}下降{:+}%，建议加大{}的推广力度".format(name, change, item.name[:12]),
                    ))

        # 2. 投诉驱动建议
        complaint_categories = {}
        for c in self.complaints:
            cat = c.get("category", "")
            complaint_categories[cat] = complaint_categories.get(cat, 0) + 1

        for cat, count in complaint_categories.items():
            if count >= 2:
                suggestions.append(Suggestion(
                    action="改良",
                    target=cat,
                    priority="high",
                    reason="投诉{}次".format(count),
                    detail="{}类投诉{}次，建议：{}".format(
                        cat, count,
                        "检查菜品品质" if "菜品" in cat else "加强员工培训" if "服务" in cat else "排查原因"
                    ),
                ))

        # 3. 偏好驱动建议
        if self.preferences:
            top_prefs = sorted(self.preferences.items(), key=lambda x: -x[1])[:3]
            for pref, count in top_prefs:
                suggestions.append(Suggestion(
                    action="新增",
                    target=pref,
                    priority="medium",
                    reason="偏好上升(+{})".format(count),
                    detail="顾客对「{}」偏好显著({}人)，建议新增1-2道{}风味菜品".format(pref, count, pref),
                ))

        # 4. 菜单健康驱动建议
        if self.menu_health:
            for dog in self.menu_health.get("dogs", []):
                suggestions.append(Suggestion(
                    action="下架",
                    target=dog,
                    priority="high",
                    reason="菜单健康度=Dog",
                    detail="「{}」长期表现不佳(Dog)，建议考虑下架或改良".format(dog),
                ))
            for star in self.menu_health.get("stars", []):
                suggestions.append(Suggestion(
                    action="推广",
                    target=star,
                    priority="low",
                    reason="菜单健康度=Star",
                    detail="「{}」是明星菜品，建议在菜单上给予更好位置".format(star),
                ))

        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        suggestions.sort(key=lambda s: priority_order.get(s.priority, 99))
        return suggestions

    def format_report(self, outlet: str = "") -> str:
        """生成可读报告"""
        suggestions = self.advise(outlet)
        if not suggestions:
            return "暂无调整建议，当前菜单状态良好。"

        lines = []
        if outlet:
            lines.append("=== {}菜单调整建议 ===".format(outlet))
        else:
            lines.append("=== 全餐厅菜单调整建议 ===")

        current_priority = ""
        for s in suggestions:
            if s.priority != current_priority:
                lines.append("")
                labels = {"high": "【高优先级】", "medium": "【中优先级】", "low": "【低优先级】"}
                lines.append(labels.get(s.priority, ""))
                current_priority = s.priority
            lines.append("  {} {} — {}".format(s.action, s.target[:15], s.reason))
            lines.append("    {}".format(s.detail))

        return "\n".join(lines)


if __name__ == "__main__":
    # 快速测试
    advisor = MenuAdvisor()
    advisor.set_menu([
        MenuItem("香煎牛肋骨", "BACIO", 238),
        MenuItem("清蒸老虎斑", "YUXI", 498),
        MenuItem("精酿啤酒", "BEER", 58),
    ])
    advisor.set_cost_trends([
        {"name": "牛肉", "change_pct": 14.0},
        {"name": "老虎斑", "change_pct": 8.0},
    ])
    advisor.set_complaints([
        {"category": "菜品/quality"},
        {"category": "菜品/quality"},
        {"category": "服务/efficiency"},
    ])
    advisor.set_preferences({"辣": 23, "清淡": 15, "海鲜": 18})
    advisor.set_menu_health({"stars": ["精酿啤酒"], "dogs": []})
    print(advisor.format_report())
