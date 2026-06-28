"""
cost-predictor demo — 食材成本预测演示
"""
import sys
sys.path.insert(0, "src")

from cost_predictor import CostPredictor

# ── 模拟6个月历史数据 ──
sim_data = {
    "牛肉":       {"1月": 85, "2月": 88, "3月": 90, "4月": 92, "5月": 95, "6月": 100},
    "猪肉":       {"1月": 28, "2月": 29, "3月": 28, "4月": 27, "5月": 26, "6月": 25},
    "羊肉":       {"1月": 68, "2月": 70, "3月": 69, "4月": 68, "5月": 67, "6月": 66},
    "鸡肉":       {"1月": 18, "2月": 18, "3月": 18, "4月": 18, "5月": 19, "6月": 19},
    "基围虾":     {"1月": 55, "2月": 58, "3月": 56, "4月": 52, "5月": 49, "6月": 46},
    "老虎斑":     {"1月": 120, "2月": 125, "3月": 128, "4月": 132, "5月": 138, "6月": 142},
    "波士顿龙虾": {"1月": 280, "2月": 275, "3月": 268, "4月": 260, "5月": 255, "6月": 250},
    "鸡蛋":       {"1月": 10, "2月": 10, "3月": 9, "4月": 10, "5月": 11, "6月": 11},
}

predictor = CostPredictor()
for name, history in sim_data.items():
    predictor.learn(name, history)

print("=" * 55)
print("  cost-predictor — 食材成本预测演示")
print("=" * 55)
print()

# 1. 逐个预测
for name in ["牛肉", "基围虾", "老虎斑", "波士顿龙虾", "猪肉", "鸡蛋"]:
    r = predictor.predict(name)
    arrow = "+" if r["change_pct"] > 0 else ""
    trend_icon = "🔴" if r["trend"] == "up" else ("🟢" if r["trend"] == "down" else "🟡")
    print(f"  {trend_icon} {name:10s} ¥{r['current']:>5.0f} → ¥{r['predicted']:>5.0f}  "
          f"(±¥{r['range'][1]-r['predicted']:.0f})  "
          f"{arrow}{r['change_pct']:+.1f}%  "
          f"置信度{r['confidence']:.0%}")

print()

# 2. 涨价预警
print("  ⚠️ 涨价预警（>3%）：")
for r in predictor.all_predictions():
    if r.get("change_pct", 0) > 3:
        print(f"    {r['name']}: +{r['change_pct']:.1f}%  → 下月预计¥{r['predicted']}")

print()
print("  📌 季节性因素：")
print("    基围虾 6-10月丰产 → 价格持续低位")
print("    老虎斑 6-8月休渔 → 价格高位")
print("    波士顿龙虾 5-8月进口旺季 → 价格下降")
