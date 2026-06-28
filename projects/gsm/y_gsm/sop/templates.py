"""标准流程模板库 — 分类对应的流程与回复"""

SOP_TEMPLATES = {
    "NOISE": {
        "title": "噪音投诉处理流程",
        "response_template": """尊敬的{name}，关于您反馈的{complaint_desc}问题，我们深表歉意。我们将：
1️⃣ 立即联系现场负责人要求在合理时段施工
2️⃣ 安排专人于{time}内前往现场评估噪音情况
3️⃣ 在{hours}小时内给出整改方案并告知您
如有任何疑问，请拨打客服热线{hotline}。""",
        "steps": [
            "确认投诉时间及噪音来源",
            "联系现场/设备负责人核实",
            "若违规施工，立即要求停止",
            "安排隔音措施或调整作业时间",
            "24h内回访确认解决情况",
        ],
        "standard_hours": 24,
    },
    "ATTITUDE": {
        "title": "态度投诉处理流程",
        "response_template": """尊敬的{name}，非常抱歉给您带来了不好的服务体验。我们已经记录您反馈的{complaint_desc}问题，将：
1️⃣ 由客服主管在{time}内与您联系了解详情
2️⃣ 调取服务记录进行核查
3️⃣ 对相关人员进行服务规范培训
您的满意是我们最大的追求。""",
        "steps": [
            "安抚客户情绪，表明重视态度",
            "详细记录投诉对象、时间、具体言行",
            "调取服务录音/监控核实",
            "按制度进行服务规范教育和处理",
            "48h内回访确认客户满意度",
        ],
        "standard_hours": 8,
    },
    "EFFICIENCY": {
        "title": "效率投诉处理流程",
        "response_template": """尊敬的{name}，对于您反映的{complaint_desc}效率问题，我们非常重视。我们已经：
1️⃣ 标记您的工单为优先处理
2️⃣ 安排专人{time}内跟进进度
3️⃣ 查明延误原因并优化流程
请保持电话畅通，我们将尽快给您答复。""",
        "steps": [
            "确认投诉事项及现有处理进度",
            "查明延误环节及原因",
            "安排加急处理，设定明确解决时限",
            "优化相关流程避免重复问题",
            "处理完成后48h内回访",
        ],
        "standard_hours": 12,
    },
    "CLEAN": {
        "title": "清洁投诉处理流程",
        "response_template": """尊敬的{name}，关于{complaint_desc}的卫生问题，我们立即响应：
1️⃣ 安排保洁人员在{time}内前往清洁
2️⃣ 加强该区域的日常清洁频次
3️⃣ 建立定期检查机制防止反复
感谢您的反馈，帮助我们不断提升服务品质。""",
        "steps": [
            "确认投诉具体位置和脏乱类型",
            "立即安排清洁人员处理",
            "评估是否需要增加清洁频次",
            "建立区域清洁检查清单",
            "持续跟踪一周确保不反复",
        ],
        "standard_hours": 4,
    },
    "FACILITY": {
        "title": "设施投诉处理流程",
        "response_template": """尊敬的{name}，您反映的{complaint_desc}问题已收录。我们将：
1️⃣ 安排工程人员在{time}内到场检查
2️⃣ 可根据情况提供临时替代方案
3️⃣ 在{hours}小时内给出维修/更换时间表
给您带来的不便敬请谅解。""",
        "steps": [
            "确认设施类型、位置及故障表现",
            "安排工程人员现场检查判断",
            "确定维修方案或需供应商协助",
            "如无法立即修复，提供临时方案",
            "维修完成后72h内回访确认",
        ],
        "standard_hours": 8,
    },
    "OTHER": {
        "title": "通用投诉处理流程",
        "response_template": """尊敬的{name}，已收到您的反馈。我们将在{time}内安排专人与您联系处理{complaint_desc}问题，请您保持电话畅通。感谢您的理解与支持。""",
        "steps": [
            "记录投诉内容及客户联系方式",
            "指派对应部门处理",
            "48h内回访确认解决情况",
        ],
        "standard_hours": 24,
    },
}


def get_sop_template(category: str, subcategory: str = "") -> dict:
    """获取分类对应的标准处理模板"""
    cat = category if category in SOP_TEMPLATES else "OTHER"
    template = dict(SOP_TEMPLATES[cat])
    template["matched_category"] = cat
    template["matched_subcategory"] = subcategory
    return template


def list_all_templates() -> list[str]:
    """列出所有可用的流程模板"""
    return [f"{k}: {v['title']}" for k, v in SOP_TEMPLATES.items()]
