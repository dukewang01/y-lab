# y-gsm — 投诉管理 · 案例分析 · 风险预判系统

**GSM = Complaint Management（投诉管理）+ Case Analysis（案例分析）+ Risk Prediction（风险预判）**

y-gsm 是 y-lab 体系下的核心业务模块，覆盖从**投诉即时处理 → 案例归因分析 → 趋势预判决策** 三层能力，帮助客服团队做到 **"一投诉即响应、一案例可归因、一趋势能预判"**。

---

## 定位

```
┌────────────────────────────────────────────┐
│          业务决策层 · 趋势预判               │
│  (aggregate → predict → alert)              │
├────────────────────────────────────────────┤
│          运营分析层 · 案例归因               │
│  (classify → root-cause → insight)          │
├────────────────────────────────────────────┤
│          一线执行层 · 投诉即时处理            │
│  (record → route → resolve)                 │
└────────────────────────────────────────────┘
```

| 层级 | 名称 | 核心能力 | 响应时效 |
|------|------|----------|----------|
| L1 | 投诉即时处理（Record & Route） | 录入、分类路由、标准回复模板 | 分钟级 |
| L2 | 案例归因分析（Case & Root-Cause） | 多维分类树、根因分析、归因统计 | 小时级 |
| L3 | 趋势预判决策（Trend & Forecast） | 时序聚合、异常检测、风险预警、报告生成 | 天级 |

---

## 架构

```
y-gsm/
├── case/              # 投诉录入与工单管理
│   ├── classifier.py  # 投诉分类引擎
│   ├── approval.py    # 审批阶梯引擎
│   └── schema.py      # 投诉数据模型
│
├── analysis/          # 归因分析
│   ├── attribution.py # 归因分析器（规则 + 统计）
│   └── stats.py       # 归因统计聚合
│
├── trend/             # 趋势洞察
│   ├── detector.py    # 异常检测器（统计阈值 + 规则）
│   └── reporter.py    # 趋势报告生成
│
├── sop/               # 标准流程库
│   └── templates.py   # 分类对应处理模板
│
└── demo/              # 演示模块
    └── run.py         # 命令行 Demo
```

---

## 投诉分类树

投诉依据 **类型 × 严重级别** 形成二维分类矩阵：

### 分类（一级）
| 编码 | 类型 | 描述 | 常见子类 |
|------|------|------|----------|
| NOISE | 噪音投诉 | 施工现场/设备运行/邻里 | 施工现场/设备运行/邻里噪音 |
| ATTITUDE | 态度投诉 | 服务人员态度/沟通方式 | 服务态度差/沟通不专业/响应不及时 |
| EFFICIENCY | 效率投诉 | 服务响应/处理时效 | 响应慢/处理周期长/时效不达标 |
| CLEAN | 清洁投诉 | 环境卫生/保洁 | 公共区域脏乱/设施清洁不到位 |
| FACILITY | 设施投诉 | 硬件设备/基础设施 | 设备损坏/设施老化/功能缺失 |

### 审批阶梯

| 级别 | 编码 | 特征 | 升级标准 | 处理时效 |
|------|------|------|----------|----------|
| 🟢 普通 | L1 | 常规诉求，单次发生 | 自动分配 | 24h |
| 🟡 中等 | L2 | 客户情绪激烈，或有重复投诉记录 | 重复≥2次或情绪分>7 | 8h |
| 🟠 严重 | L3 | 涉及人身安全/法律风险/媒体曝光 | 风险分>8 或 涉及L3条款 | 2h |
| 🔴 危机 | L4 | 已产生舆情/监管介入/法律诉讼 | 系统自动标记 | 即时 |

---

## 用法示例

```python
from y_gsm.case.schema import Complaint, CaseStatus
from y_gsm.case.classifier import classify_complaint
from y_gsm.case.approval import determine_approval_level
from y_gsm.analysis.attribution import attribute_case
from y_gsm.sop.templates import get_sop_template
from y_gsm.trend.detector import detect_anomaly
from y_gsm.trend.reporter import generate_report

# 1️⃣ 投诉录入
complaint = Complaint(
    case_id="CASE-202606-001",
    customer_name="张三",
    description="楼下施工队凌晨5点开始钻孔，噪音太大无法入睡",
    source="电话投诉"
)

# 2️⃣ 自动分类
classification = classify_complaint(complaint)
# → { category: "NOISE", subcategory: "施工现场噪音", confidence: 0.92 }

# 3️⃣ 确定审批阶梯
level = determine_approval_level(classification, complaint)
# → { level: "L2", handler: "客服主管", max_hours: 8 }

# 4️⃣ 获取标准处理模板
sop = get_sop_template(classification.category, classification.subcategory)

# 5️⃣ 根因归因
attribution = attribute_case(complaint, classification)
# → { root_cause: "施工时间管控缺失", related_cases: 3, patterns: [...] }

# 6️⃣ 趋势风险预判
anomaly = detect_anomaly("NOISE", time_window="24h")
# → { anomaly: True, severity: "warning", message: "噪音投诉24h内激增300%" }

# 7️⃣ 生成决策报告
report = generate_report(time_range="7d", categories=["NOISE", "ATTITUDE"])
```

---

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 Demo
python -m y_gsm.demo.run

# 测试
pytest tests/
```

---

## 路线图

- [x] 投诉分类引擎（基础规则版）
- [x] 审批阶梯模型
- [x] 标准流程模板库
- [x] 归因分析器（规则 + 统计）
- [ ] 基于 LLM 的智能分类（v2）
- [ ] 时序异常检测（统计阈值 → 机器学习）
- [ ] 自动预警推送（飞书/短信）
- [ ] 可视化 Dashboard
- [ ] 历史案例相似度匹配

---

y-lab © 2026 — 以系统化思维解决业务问题
