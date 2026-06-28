"""归因分析器 — 规则 + 统计 进行根因归因"""

from dataclasses import dataclass, field
from typing import Optional
from y_gsm.case.schema import Complaint
from y_gsm.case.classifier import ComplaintClassification


# ── 根因知识库 ────────────────────────────────────────────────────────

ROOT_CAUSE_DB = {
    "NOISE": {
        "施工现场噪音": [
            ("施工时间不合规", ["凌晨", "深夜", "夜间", "早上6点前", "23点后"]),
            ("隔音措施不足", ["隔音", "没隔音", "无隔音", "隔音差"]),
            ("施工报备缺失", ["没通知", "未告知", "不知道", "没收到通知"]),
        ],
        "设备运行噪音": [
            ("设备老化缺乏维护", ["老化", "旧设备", "嗡嗡", "异响"]),
            ("设备安装位置不当", ["靠近", "窗外", "卧室旁"]),
            ("运行时间管控缺失", ["一直开着", "没停过", "24小时"]),
        ],
        "邻里噪音": [
            ("邻里协调机制缺失", ["协调", "没人管", "物业不管"]),
            ("隔音建筑标准不足", ["隔音", "楼板薄", "听得清"]),
        ],
    },
    "ATTITUDE": {
        "服务态度差": [
            ("员工培训不到位", ["培训", "新人", "不懂"]),
            ("考核机制缺失", ["不在乎", "无所谓", "没人管"]),
            ("工作压力过大", ["太忙", "忙不过来", "累"]),
        ],
    },
    "EFFICIENCY": {
        "处理周期长": [
            ("流程繁琐", ["流程", "审批", "签字", "盖章"]),
            ("人手不足", ["没人", "缺人", "忙不过来"]),
            ("跨部门协调困难", ["部门", "踢皮球", "转来转去"]),
        ],
    },
    "CLEAN": {
        "公共区域脏乱": [
            ("清洁频率不足", ["很少打扫", "一天一次", "不勤"]),
            ("垃圾清运不及时", ["满了", "溢出来", "堆"]),
            ("监管不到位", ["没人检查", "没标准"]),
        ],
    },
    "FACILITY": {
        "设备损坏": [
            ("设备老化未更换", ["老化", "旧", "年头", "年限"]),
            ("巡检维护缺失", ["没人修", "报修", "报了很久"]),
            ("供应商响应慢", ["供应商", "厂家", "保修"]),
        ],
    },
}


@dataclass
class CaseAttribution:
    """案例归因结果"""
    root_cause: str
    root_cause_details: str
    related_patterns: list = field(default_factory=list)
    suggested_action: str = ""


def attribute_case(
    complaint: Complaint,
    classification: ComplaintClassification
) -> CaseAttribution:
    """对单个案例进行根因归因"""
    text = complaint.description.lower()

    # 查找匹配的根因
    cat_db = ROOT_CAUSE_DB.get(classification.category, {})
    sub_db = cat_db.get(classification.subcategory, [])

    best_cause = "综合因素"
    best_score = 0
    matched_patterns = []

    for cause_name, patterns in sub_db:
        score = 0
        for kw in patterns:
            if kw.lower() in text:
                score += 1
        if score > best_score:
            best_score = score
            best_cause = cause_name
            matched_patterns = [kw for kw in patterns if kw.lower() in text]

    if best_score == 0:
        # 没有明确模式，给通用根因
        best_cause = _default_root_cause(classification.category)
        matched_patterns = ["未匹配到具体关键词，基于分类推断"]

    action = _suggest_action(classification.category, best_cause)

    return CaseAttribution(
        root_cause=best_cause,
        root_cause_details=f"根据'{classification.subcategory}'下{len(matched_patterns)}个模式匹配",
        related_patterns=matched_patterns,
        suggested_action=action,
    )


def _default_root_cause(category: str) -> str:
    """分类默认根因"""
    defaults = {
        "NOISE": "噪音管控体系不完善",
        "ATTITUDE": "服务质量管理机制缺失",
        "EFFICIENCY": "流程效率优化空间大",
        "CLEAN": "环境维护标准执行不到位",
        "FACILITY": "设施维护管理体系薄弱",
    }
    return defaults.get(category, "综合管理原因")


def _suggest_action(category: str, root_cause: str) -> str:
    """根据根因生成建议行动"""
    suggestions = {
        "施工时间不合规": "加强施工时间管控，建立报备流程，违规扣分制度",
        "隔音措施不足": "评估并加强隔音设施，优先处理高投诉区域",
        "员工培训不到位": "启动服务态度专项培训，每月测评考核",
        "流程繁琐": "精简审批环节，建立标准化快速处理通道",
        "清洁频率不足": "增加清洁频次，建立清洁检查清单制度",
        "设备老化未更换": "制定设备替换计划，建立预防性维护台账",
        "噪音管控体系不完善": "建立分时段噪音管控标准，加强巡查",
        "服务质量管理机制缺失": "建立服务质量KPI考核，引入神秘访客制度",
        "流程效率优化空间大": "开展流程耗时分析，消除瓶颈环节",
        "环境维护标准执行不到位": "制定可视化清洁标准，建立每日巡检制度",
        "设施维护管理体系薄弱": "建立设备全生命周期管理体系，预防性维护计划",
    }
    return suggestions.get(root_cause, "深入调查后制定改进方案")
