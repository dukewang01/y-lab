"""
menu-advisor demo
"""
import sys
sys.path.insert(0, "src")
from menu_advisor import MenuItem, MenuAdvisor

print("=" * 52)
print("  menu-advisor — 菜单调整建议引擎")
print("=" * 52)

# 模拟菜单
advisor = MenuAdvisor()
advisor.set_menu([
    MenuItem("香煎牛肋骨", "BACIO", 238, "main"),
    MenuItem("黑松露和牛", "BACIO", 388, "main"),
    MenuItem("帕尔马火腿", "BACIO", 168, "starter"),
    MenuItem("提拉米苏", "BACIO", 88, "dessert"),
    MenuItem("清蒸老虎斑", "YUXI", 498, "main"),
    MenuItem("东坡肉", "YUXI", 138, "main"),
    MenuItem("白灼基围虾", "YUXI", 168, "main"),
    MenuItem("蛋炒饭", "YUXI", 38, "staple"),
    MenuItem("酸辣汤", "YUXI", 58, "soup"),
    MenuItem("工作日自助", "OPEN", 198, "buffet"),
])

# 食材成本趋势
advisor.set_cost_trends([
    {"name": "牛肉", "current": 100, "predicted": 114, "change_pct": 14.0},
    {"name": "老虎斑", "current": 142, "predicted": 152, "change_pct": 7.0},
    {"name": "基围虾", "current": 46, "predicted": 40, "change_pct": -13.0},
    {"name": "意面原料", "current": 15, "predicted": 16, "change_pct": 6.7},
])

# 投诉数据
advisor.set_complaints([
    {"category": "菜品/quality"}, {"category": "菜品/quality"},
    {"category": "服务/efficiency"}, {"category": "环境/noise"},
])

# 偏好风向
advisor.set_preferences({"辣": 23, "酸辣": 18, "清淡": 15, "海鲜": 12, "轻食": 8})

# 菜单健康度
advisor.set_menu_health({
    "stars": ["黑松露和牛", "提拉米苏"],
    "dogs": ["蛋炒饭"],
})

print(advisor.format_report())

print()
print("  📌 单独为YUXI生成建议")
print("  " + "-" * 40)
print(advisor.format_report(outlet="YUXI"))
