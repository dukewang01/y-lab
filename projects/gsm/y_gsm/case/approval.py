"""审批阶梯引擎"""

from dataclasses import dataclass
from typing import Optional
from .schema import Complaint
from .classifier import ComplaintClassification


APPROVAL_TIERS = {
    "L1": {
        "name": "普通",
        "label": "🟢 L1-普通",
        "handler": "客服专员",
        "max_hours": 24,
        "min_risk": 0,
        "max_risk": 3,
    },
    "L2": {
        "name": "中等",
        "label": "🟡 L2-中等",
        "handler": "客服主管",
        "max_hours": 8,
        "min_risk": 3,
        "max_risk": 6,
    },
    "L3": {
        "name": "严重",
        "label": "🟠 L3-严重",
        "handler": "部门经理",
        "max_hours": 2,
        "min_risk": 6,
        "max_risk": 9,
    },
    "L4": {
        "name": "危机",
        "label": "🔴 L4-危机",
        "handler": "总经理/公关",
        "max_hours": 0,  # 即时处理
        "min_risk": 9,
        "max_risk": 10,
    },
}


# ── 提升条件 ──────────────────────────────────────────────────────────

ESCALATION_RULES = [
    # (条件描述, 检查函数返回额外分数)
    ("客户情绪激烈（情绪分≥7）", lambda c, cl: 2 if c.emotion_score >= 7 else 0),
    ("重复投诉（≥3次）", lambda c, cl: 2 if c.repeat_count >= 3 else 0),
    ("涉及安全/法律", lambda c, cl: 3 if any(kw in c.description.lower()
        for kw in ["安全", "受伤", "火灾", "漏电", "爆炸", "死亡", "事故", "法律", "起诉", "律师"]) else 0),
    ("关键词匹配力度强", lambda c, cl: 1 if cl.confidence > 0.85 else 0),
    ("涉及媒体/舆情风险", lambda c, cl: 3 if any(kw in c.description.lower()
        for kw in ["曝光", "媒体", "投诉平台", "微博", "抖音", "记者", "朋友圈", "发网上"]) else 0),
]


@dataclass
class ApprovalLevel:
    """审批等级"""
    level: str          # L1-L4
    label: str
    handler: str
    max_hours: int
    risk_score: float
    escalation_reasons: list


def determine_approval_level(
    classification: ComplaintClassification,
    complaint: Complaint
) -> ApprovalLevel:
    """确定投诉的审批阶梯等级"""

    # 基础风险分 = complaint.risk_score
    base_risk = complaint.risk_score

    # 累计额外风险
    extra_risk = 0
    reasons = []
    for desc, check_fn in ESCALATION_RULES:
        score = check_fn(complaint, classification)
        if score > 0:
            extra_risk += score
            reasons.append(desc)

    total_risk = min(base_risk + extra_risk, 10)

    # 匹配阶梯
    chosen_level = "L1"
    for code, tier in sorted(APPROVAL_TIERS.items()):
        if tier["min_risk"] <= total_risk <= tier["max_risk"]:
            chosen_level = code
            break
        elif total_risk > tier["max_risk"]:
            chosen_level = code  # 继续往上匹配

    info = APPROVAL_TIERS[chosen_level]
    return ApprovalLevel(
        level=chosen_level,
        label=info["label"],
        handler=info["handler"],
        max_hours=info["max_hours"],
        risk_score=round(total_risk, 1),
        escalation_reasons=reasons,
    )
