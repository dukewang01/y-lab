"""归因统计聚合"""

from dataclasses import dataclass, field
from collections import Counter, defaultdict
from typing import Optional
from y_gsm.case.schema import Complaint
from y_gsm.case.classifier import ComplaintClassification, classify_complaint
from y_gsm.analysis.attribution import attribute_case


@dataclass
class AttributionStats:
    """归因统计结果"""
    total_cases: int = 0
    category_distribution: dict = field(default_factory=dict)
    root_cause_rank: list = field(default_factory=list)
    top_categories: list = field(default_factory=list)
    suggested_focus: str = ""


def aggregate_stats(complaints: list[Complaint]) -> AttributionStats:
    """批量投诉的归因统计"""
    if not complaints:
        return AttributionStats()

    # 分类统计
    cat_counter = Counter()
    cause_counter = Counter()
    sub_cat_counter = Counter()

    for c in complaints:
        cl = classify_complaint(c)
        at = attribute_case(c, cl)
        cat_counter[cl.category] += 1
        sub_cat_counter[cl.subcategory] += 1
        cause_counter[at.root_cause] += 1

    # 排序
    cat_rank = [(name, count) for name, count in cat_counter.most_common()]
    cause_rank = [(cause, count) for cause, count in cause_counter.most_common(5)]
    top_cats = [name for name, _ in cat_counter.most_common(3)]

    # 建议关注点
    if cause_rank:
        focus = f"重点关注：{cause_rank[0][0]}（占比{cause_rank[0][1]/len(complaints)*100:.0f}%）"
    else:
        focus = "暂无足够数据"

    return AttributionStats(
        total_cases=len(complaints),
        category_distribution=dict(cat_counter),
        root_cause_rank=cause_rank,
        top_categories=top_cats,
        suggested_focus=focus,
    )
