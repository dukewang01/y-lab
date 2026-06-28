import sys; sys.path.insert(0,"src")
from risk import RiskManager

mgr = RiskManager()
mgr.register("电梯故障", "设施", 3, 4, "工程部")
mgr.register("食安投诉", "食安", 4, 4, "FSAA")
mgr.register("消防通道堵塞", "消防", 3, 3, "保安部")
mgr.register("空调老化停机", "设施", 2, 2, "工程部")
mgr.register("网络中断", "IT", 3, 2, "IT部")
mgr.register("停车场剐蹭", "安全", 4, 1, "保安部")
mgr.register("员工工伤", "人力", 2, 3, "HR")

r = mgr.assess()
print("=== y-risk: Risk Assessment ===")
print("Total risks: {}".format(r["total"]))
print("By level: {}".format(r["by_level"]))
print()
print("High risks:")
for risk in r["high_risks"]:
    print("  [{}] {} (L{},S{}) by: {}".format(
        risk.level, risk.name, risk.likelihood,
        risk.severity, risk.owner))
