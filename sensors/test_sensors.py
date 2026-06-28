import sys
sys.path.insert(0, "sensors")

print("=== Price Sensor ===")
from price_index import PriceSensor
ps = PriceSensor()
prices = ps.query(["牛肉", "基围虾", "老虎斑", "波士顿龙虾"])
for p in prices:
    arrow = "+" if p["change_pct"] > 0 else ""
    print(f"  {p['name']}: {p['current']}元/kg ({p['trend']} {arrow}{p['change_pct']}%)")

print("\n=== Trend Sensor ===")
from trend_sensor import TrendSensor
ts = TrendSensor()
hot = ts.hot_right_now(6)
for h in hot:
    print(f"  {h['tag']}: {h['score']}")

print("\n=== Monthly Trend ===")
mt = ts.monthly_trend(6)
for m in mt[:5]:
    print(f"  {m['tag']}: now={m['score']} last={m['last_month']} ({m['mom_change_pct']:+.0f}%)")
