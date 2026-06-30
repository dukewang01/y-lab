# GSM (客户投诉管理)

酒店客户投诉（Guest Service Manager）全流程管理。涵盖投诉分类、归因分析、SOP、审批流程、趋势预判。

## 源代码 (11个文件)

- y_gsm/case/classifier.py — 投诉分类器
- y_gsm/case/schema.py — 数据结构定义
- y_gsm/case/approval.py — 审批流程
- y_gsm/analysis/attribution.py — 归因分析
- y_gsm/analysis/stats.py — 统计报表
- y_gsm/sop/templates.py — SOP模板
- demo/run.py — 运行示例

## 三层能力

1. **治** — 即时处理（SOP指南）
2. **析** — 案例归因（分类树）
3. **预** — 趋势预判（风险预警）

## 投诉分类 (25+子类)

噪音19% / 态度16% / 效率13% / 设施9% / 清洁9% / 空调 / 水质 / 虫害 / 停车场 / 泳池...

## SOP专项

受伤/消防/虫害/漏水/电梯/行李/订房/赔偿决策 — 9个专项SOP

## 4D决策模型

收益层 → 理性层 → 情绪层 → 底线层

## 跨站联动

GSM?RISK / GSM?FSAA / GSM?MEP / GSM?QA
