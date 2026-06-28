import sys; sys.path.insert(0,"src")
from complaint_classifier import classify, batch, trend_summary

cases = [
    "菜太咸了，完全没法吃",
    "上菜太慢了，等了40分钟才来",
    "服务员态度很差，爱理不理",
    "空调不制冷，吃饭吃出一身汗",
    "汤里发现一根头发，太恶心了",
    "波士顿龙虾不新鲜有异味",
    "份量太少，198的套餐根本不够两个人",
    "地面脏，厕所也很臭",
    "电梯等了很久都不动",
    "结账的时候发现多收了服务费",
    "盘子有缺口，有安全隐患",
    "甜品太甜了，吃不下去",
    "预定的包厢到了说没有了",
    "噪音太大了，隔壁桌喝酒划拳",
    "牛排是凉的，要求重做",
]

results = batch(cases)
summary = trend_summary(results)

print("=== complaint-classifier Demo ===")
print()
for i, r in enumerate(results):
    print("  [{:5s}/{:15s}] {:3.0f}% {}".format(
        r["category"], r["sub_category"],
        r["confidence"]*100, cases[i][:30]))

print()
print("Summary:")
for cat, count in summary["categories"].items():
    print("  {}: {}".format(cat, count))
print("Avg confidence: {:.0f}%".format(summary["avg_confidence"]*100))
