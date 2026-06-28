"""y-gsm demo"""
import sys; sys.path.insert(0,"y_gsm")
from case.schema import Complaint
from case.classifier import classify_complaint

def make_complaint(text):
    return Complaint(
        case_id="CMP-demo",
        customer_name="Guest",
        description=text,
        source="online",
        status="new"
    )

cases = [
    "隔壁房间太吵了，半夜还在喝酒",
    "前台态度冷淡，爱理不理的",
    "上菜等了40分钟，催了好几次",
    "房间地面不干净，床单有污渍",
    "空调不制冷，热得睡不着",
]
categories = {
    0: "环境/噪音", 1: "服务/态度", 2: "服务/效率",
    3: "环境/清洁", 4: "设施/空调",
}

print("=== y-gsm: Complaint Classification ===")
for i, text in enumerate(cases):
    complaint = make_complaint(text)
    result = classify_complaint(complaint)
    cat = categories.get(i, "?")
    print("  {} -> {} (cat={}, sub={}, conf={:.0f}%)".format(
        text[:20], cat, result.category, result.subcategory, result.confidence*100))
