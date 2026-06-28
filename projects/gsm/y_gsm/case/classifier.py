"""投诉分类引擎 — 基于关键词规则的自动分类"""

from dataclasses import dataclass, field
from typing import Optional
from .schema import Complaint


# ── 分类定义 ──────────────────────────────────────────────────────────

CATEGORY_RULES = {
    "NOISE": {
        "title": "噪音投诉",
        "keywords": [
            "噪音", "噪声", "吵", "钻孔", "施工", "装修",
            "机器", "设备声", "深夜", "凌晨", "喇叭",
            "安静", "无法休息", "睡不"
        ],
        "subcategories": {
            "施工现场噪音": ["施工", "装修", "钻孔", "打桩"],
            "设备运行噪音": ["机器", "设备声", "空调外机", "水泵"],
            "邻里噪音": ["邻里", "楼上", "隔壁", "脚步声"],
        }
    },
    "ATTITUDE": {
        "title": "态度投诉",
        "keywords": [
            "态度", "服务差", "不耐烦", "敷衍", "不尊重",
            "冷漠", "骂人", "态度恶劣", "态度不好",
            "爱理不理", "吊儿郎当", "不专业"
        ],
        "subcategories": {
            "服务态度差": ["态度差", "不耐烦", "冷漠", "敷衍"],
            "沟通不专业": ["不专业", "说不清", "回答错误", "误导"],
            "响应不及时": ["不回应", "迟迟", "没人管", "找不到人"],
        }
    },
    "EFFICIENCY": {
        "title": "效率投诉",
        "keywords": [
            "效率", "太久", "等了好久", "迟迟不", "进展慢",
            "速度", "拖延", "拖了", "催", "没人跟进",
            "反复", "多次", "还没解决", "周期"
        ],
        "subcategories": {
            "响应慢": ["迟迟不", "没回应", "催", "没人管"],
            "处理周期长": ["太久", "拖了", "反复", "多次"],
            "时效不达标": ["承诺", "超时", "逾期", "违约"],
        }
    },
    "CLEAN": {
        "title": "清洁投诉",
        "keywords": [
            "脏", "垃圾", "清洁", "卫生", "打扫",
            "蟑螂", "老鼠", "异味", "臭", "污水",
            "灰尘", "蛛网", "污渍", "不干净", "邋遢"
        ],
        "subcategories": {
            "公共区域脏乱": ["大厅", "楼道", "走廊", "电梯", "垃圾"],
            "设施清洁不到位": ["厕所", "洗手间", "浴室", "厨房"],
            "异味问题": ["臭味", "异味", "发霉", "臭"],
        }
    },
    "FACILITY": {
        "title": "设施投诉",
        "keywords": [
            "坏了", "故障", "损坏", "坏掉", "不工作",
            "老化", "破旧", "漏水", "断电", "停水",
            "电梯", "空调", "门锁", "马桶", "灯"
        ],
        "subcategories": {
            "设备损坏": ["坏了", "故障", "损坏", "不工作", "坏掉"],
            "设施老化": ["老化", "破旧", "生锈", "掉漆"],
            "功能缺失": ["没有", "缺少", "缺", "不够用"],
        }
    }
}

CATEGORY_LIST = list(CATEGORY_RULES.keys())


@dataclass
class ComplaintClassification:
    """分类结果"""
    category: str
    subcategory: str
    confidence: float
    matched_keywords: list = field(default_factory=list)


def classify_complaint(complaint: Complaint) -> ComplaintClassification:
    """对投诉进行自动分类，返回最佳匹配类别"""
    text = (complaint.description + complaint.customer_name).lower()
    matches = []

    for cat, rules in CATEGORY_RULES.items():
        matched_kws = [kw for kw in rules["keywords"] if kw in text]
        if not matched_kws:
            continue
        # 计算匹配度
        score = len(matched_kws) / len(rules["keywords"])
        # 子分类匹配
        best_sub = list(rules["subcategories"].keys())[0]
        best_sub_score = 0
        for sub_name, sub_kws in rules["subcategories"].items():
            sub_matched = sum(1 for kw in sub_kws if kw in text)
            if sub_matched > best_sub_score:
                best_sub_score = sub_matched
                best_sub = sub_name
        matches.append((cat, best_sub, score, matched_kws))

    if not matches:
        return ComplaintClassification(
            category="OTHER",
            subcategory="未分类投诉",
            confidence=0.0,
            matched_keywords=[]
        )

    # 取最高分
    matches.sort(key=lambda x: x[2], reverse=True)
    cat, sub, score, kws = matches[0]

    # confidence: 归一化到 0.3 ~ 0.99
    confidence = min(0.3 + score * 1.4, 0.99)

    return ComplaintClassification(
        category=cat,
        subcategory=sub,
        confidence=round(confidence, 2),
        matched_keywords=list(set(kws))
    )
