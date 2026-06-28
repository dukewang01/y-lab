"""
complaint_classifier — 投诉自动分类器

把自然语言投诉自动归因到标准分类体系。
v0.1: 关键词规则引擎
v0.2+: TF-IDF / ML分类器
"""
import re
from collections import Counter


# ── 分类体系 ──
CATEGORIES = {
    "菜品": {
        "quality":   ["不新鲜", "变质", "异味", "酸了", "馊了", "发霉", "过期"],
        "taste":     ["太咸", "太甜", "太淡", "太辣", "太油", "没味", "不好吃", "难吃", "口感差"],
        "temperature": ["凉了", "冷了", "不够热", "温的", "冰的", "不烫"],
        "portion":   ["太少", "量少", "份量", "不够吃", "小份"],
        "foreign":   ["头发", "虫子", "异物", "钢丝", "塑料", "玻璃", "石头",  "苍蝇"],
    },
    "服务": {
        "efficiency": ["太慢", "上菜慢", "等太久", "等待", "迟迟", "半天", "催单"],
        "attitude":   ["态度差", "态度不好", "爱理不理", "冷漠", "不耐烦", "凶", "吼"],
        "mistake":    ["上错", "漏单", "点错", "弄错", "给错"],
        "communication": ["没说明", "没提醒", "没告知", "沟通"],
    },
    "设施": {
        "ac":        ["空调", "太热", "太冷", "不制冷"],
        "elevator":  ["电梯", "等了", "不动"],
        "water":     ["漏水", "水龙头", "马桶", "下水道", "排水"],
        "wifi":      ["网络", "WiFi", "wifi", "连不上"],
    },
    "环境": {
        "noise":     ["太吵", "噪音", "吵", "安静", "不安静", "隔音"],
        "cleanliness": ["不干净", "脏", "有味道", "有烟味", "地面", "厕所"],
        "ambient":   ["灯光", "音乐", "氛围", "布置", "装修"],
    },
    "其他": {
        "pricing":   ["太贵", "不值", "价格", "收费", "加收"],
        "booking":   ["预定", "预约", "订不到", "没位"],
        "policy":    ["政策", "规定", "不允许", "不让"],
    }
}

# 餐厅匹配
OUTLETS = {
    "bacio": "BACIO", "open": "OPEN", "yuxi": "YUXI", "yuan": "YUAN",
    "御玺": "YUXI", "意大利": "BACIO", "自助": "OPEN", "啤酒": "BEER",
}


def classify(text: str) -> dict:
    """
    分类一条投诉文本。

    输入：
        text: "菜太咸了，服务员态度也不好"
    输出：
        {"category": "菜品", "sub_category": "taste",
         "reason": "太咸",
         "confidence": 0.92,
         "outlet": "",           # 如果能提取到
         "matched_keywords": ["太咸", "态度"]}
    """
    text_lower = text.lower()
    results = []

    # 遍历分类体系
    for category, sub_cats in CATEGORIES.items():
        for sub_cat, keywords in sub_cats.items():
            matched = [kw for kw in keywords if kw in text_lower]
            if matched:
                # 置信度：匹配关键词越多越高
                base = 0.6
                bonus = min(len(matched) * 0.1, 0.35)
                # 如果匹配到了精确的关键词而不是泛匹配，额外加分
                exact_matches = sum(1 for kw in matched if len(kw) >= 3)
                bonus += exact_matches * 0.05
                results.append({
                    "category": category,
                    "sub_category": sub_cat,
                    "confidence": round(min(base + bonus, 0.98), 2),
                    "matched_keywords": matched,
                })

    # 提取餐厅
    outlet = ""
    for kw, name in OUTLETS.items():
        if kw in text_lower:
            outlet = name
            break

    # 取置信度最高的分类
    if not results:
        return {
            "category": "未分类",
            "sub_category": "unknown",
            "confidence": 0.0,
            "outlet": outlet,
            "reason": "没有匹配到已知分类关键词",
            "matched_keywords": [],
        }

    best = max(results, key=lambda r: r["confidence"])
    # 汇总所有匹配到的关键词
    all_keys = set()
    for r in results:
        all_keys.update(r["matched_keywords"])

    return {
        "category": best["category"],
        "sub_category": best["sub_category"],
        "confidence": best["confidence"],
        "outlet": outlet,
        "reason": "、".join(list(all_keys)[:3]),
        "matched_keywords": list(all_keys),
        "all_candidates": results[:3],  # 前三候选
    }


def batch(texts: list[str]) -> list[dict]:
    """批量分类"""
    return [classify(t) for t in texts]


def trend_summary(results: list[dict]) -> dict:
    """对批量分类结果做汇总统计"""
    cats = Counter()
    sub_cats = Counter()
    outlets = Counter()
    for r in results:
        cats[r["category"]] += 1
        sub_cats[r["category"] + "/" + r["sub_category"]] += 1
        if r.get("outlet"):
            outlets[r["outlet"]] += 1

    return {
        "total": len(results),
        "categories": dict(cats.most_common()),
        "top_sub_categories": dict(sub_cats.most_common(8)),
        "outlets": dict(outlets.most_common()),
        "avg_confidence": round(sum(r["confidence"] for r in results) / len(results), 2) if results else 0,
    }
