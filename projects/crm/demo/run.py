#!/usr/bin/env python3
"""
y-crm Demo — 客户全生命周期管理系统

模拟 5 个酒店客户，演示：
  1. 客户档案聚合
  2. RFM 价值分段（高/中/低）
  3. 流失预警
  4. 偏好推荐

零外部依赖，仅使用 stdlib。
"""

from dataclasses import dataclass, field
from typing import List
import datetime
import random
import textwrap


# ─── 数据模型 ────────────────────────────────────────────────────────

@dataclass
class Transaction:
    date: str        # YYYY-MM-DD
    amount: float
    category: str    # e.g. "房费", "餐饮", "会议"


@dataclass
class Guest:
    uid: str
    name: str
    city: str
    tags: List[str]                     # 偏好标签
    transactions: List[Transaction] = field(default_factory=list)

    @property
    def total_spent(self) -> float:
        return round(sum(t.amount for t in self.transactions), 2)

    @property
    def total_visits(self) -> int:
        return len(self.transactions)

    @property
    def last_visit_days(self) -> int:
        """距离最近一次消费的天数（模拟日期 2026-06-28）"""
        if not self.transactions:
            return 999
        today = datetime.date(2026, 6, 28)
        dates = [datetime.date(*map(int, t.date.split("-"))) for t in self.transactions]
        return (today - max(dates)).days

    @property
    def avg_spend_per_visit(self) -> float:
        if self.total_visits == 0:
            return 0.0
        return round(self.total_spent / self.total_visits, 2)


# ─── 模拟数据 ──────────────────────────────────────────────────────

def _build_guests() -> List[Guest]:
    return [
        Guest(
            uid="uuid-001", name="张伟", city="上海",
            tags=["商务出行", "精品餐厅", "健身房", "行政酒廊"],
            transactions=[
                Transaction("2026-06-20", 1680.00, "房费"),
                Transaction("2026-06-20", 380.00, "餐饮"),
                Transaction("2026-06-21", 240.00, "洗衣"),
                Transaction("2026-06-15", 160.00, "餐饮"),
            ],
        ),
        Guest(
            uid="uuid-002", name="李娜", city="广州",
            tags=["亲子活动", "网红打卡", "自助餐"],
            transactions=[
                Transaction("2026-04-10", 380.00, "房费"),
                Transaction("2026-06-28", 0.00, ""),  # 今日刚下单，模拟未入住
            ],
        ),
        Guest(
            uid="uuid-003", name="王刚", city="北京",
            tags=["商务出差", "会议室", "机场接送", "行政酒廊"],
            transactions=[
                Transaction("2026-06-22", 950.00, "房费"),
                Transaction("2026-06-22", 320.00, "餐饮"),
                Transaction("2026-06-20", 800.00, "房费"),
                Transaction("2026-06-20", 150.00, "洗衣"),
                Transaction("2026-06-19", 2100.00, "房费"),
                Transaction("2026-06-19", 420.00, "餐饮"),
                Transaction("2026-06-18", 950.00, "房费"),
                Transaction("2026-06-18", 180.00, "餐饮"),
            ],
        ),
        Guest(
            uid="uuid-004", name="陈芳", city="深圳",
            tags=["情侣出行", "网红打卡", "Spa", "泳池"],
            transactions=[
                Transaction("2025-12-15", 620.00, "房费"),
                Transaction("2025-12-15", 280.00, "Spa"),
                Transaction("2025-12-14", 620.00, "房费"),
            ],
        ),
        Guest(
            uid="uuid-005", name="赵雷", city="成都",
            tags=["商务出行", "会议室", "健身房"],
            transactions=[
                Transaction("2026-06-25", 750.00, "房费"),
                Transaction("2026-06-25", 210.00, "餐饮"),
                Transaction("2026-06-23", 750.00, "房费"),
                Transaction("2026-06-23", 90.00, "餐饮"),
                Transaction("2026-06-22", 750.00, "房费"),
                Transaction("2026-06-22", 160.00, "餐饮"),
            ],
        ),
    ]


# ─── RFM 分段 ────────────────────────────────────────────────────────

# 简单三段：基于 Frequency 和 Monetary 分箱
# 高值 = 高频 + 高消费；低值 = 低频 + 低消费；其余中值

RfmSegment = str  # "高价值" | "中价值" | "低价值"


def calc_rfm_segment(g: Guest) -> RfmSegment:
    visits = g.total_visits
    avg_spend = g.avg_spend_per_visit
    last_days = g.last_visit_days

    # 打分规则
    r_score = 3 if last_days <= 7 else (2 if last_days <= 60 else 1)
    f_score = 3 if visits >= 5 else (2 if visits >= 3 else 1)
    m_score = 3 if avg_spend >= 600 else (2 if avg_spend >= 300 else 1)

    total = r_score + f_score + m_score  # 3-9

    if total >= 7:
        return "高价值"
    elif total >= 5:
        return "中价值"
    else:
        return "低价值"


# ─── 流失预警 ────────────────────────────────────────────────────────

ChurnLevel = str  # "高" | "中" | "低"


def calc_churn_risk(g: Guest) -> ChurnLevel:
    last_days = g.last_visit_days
    visits = g.total_visits

    if last_days > 90:
        return "高"
    if last_days > 60 and visits <= 2:
        return "高"
    if last_days > 30:
        return "中"
    return "低"


# ─── 偏好推荐 ───────────────────────────────────────────────────────

def calc_recommendation(g: Guest) -> str:
    if not g.tags:
        return "无可用偏好，建议收集"
    # 简单随机推荐一个标签
    random.seed(hash(g.uid))
    return random.choice(g.tags)


# ─── 输出格式化 ──────────────────────────────────────────────────────

def _summary_card(g: Guest, seg: RfmSegment, risk: ChurnLevel, rec: str) -> str:
    risk_icon = " !!" if risk == "\u9ad8" else ""
    lines = [
        f"# {g.name} ({g.uid}) - {g.city}",
        f"  本月消费: {g.total_visits} 次 / {g.total_spent:.2f} (均次 {g.avg_spend_per_visit:.0f})",
        f"  最近入住: {g.last_visit_days} 天前",
        f"  RFM 分段: {seg}",
        f"  流失风险: {risk}{risk_icon}",
        f"  推荐偏好: {rec}",
        "",
    ]
    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────

def main():
    print("=" * 52)
    print("  y-crm — 客户全生命周期管理系统 · Demo")
    print("=" * 52)
    print()

    guests = _build_guests()

    for g in guests:
        seg = calc_rfm_segment(g)
        risk = calc_churn_risk(g)
        rec = calc_recommendation(g)
        print(_summary_card(g, seg, risk, rec))
        print()

    # 汇总统计
    segments = [calc_rfm_segment(g) for g in guests]
    risks = [calc_churn_risk(g) for g in guests]

    print("-" * 40)
    print("  分段统计")
    for seg in ("高价值", "中价值", "低价值"):
        print(f"    . {seg}: {segments.count(seg)} 人")
    print()
    print("  流失预警")
    for risk in ("高", "中", "低"):
        cnt = risks.count(risk)
        icon = " !!" if risk == "高" else ""
        print(f"    . {risk}风险: {cnt} 人{icon}")
    print("=" * 40)


if __name__ == "__main__":
    main()
