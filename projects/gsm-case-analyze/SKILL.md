---
name: "gsm-case-analyze"
description: "Deep complaint analysis: trends, root causes, financial impact, risk prediction"
---

# GSM Case Analysis

Deep analysis of GSM (Guest Service Management) complaints and cases. Generates trend reports, root cause analysis, and risk predictions.

## Data Source

- Graph: `knowledge_center/gsm_graph.json`
- Also references: `media/log_cases/` (raw Excel)
- Cross-station: references RISK, FSAA, MEP graphs

## Report Sections

### 1. Knowledge Space Overview
Count entities by namespace prefix (CASE_, CMP_, RCASE_, FAQ_, etc.)

### 2. Case Library
- Total cases by type
- Open vs closed cases
- Cases by severity

### 3. Complaint Categories Distribution
- 噪音投诉 (Noise)
- 服务态度 (Attitude)
- 效率问题 (Efficiency)
- 设施问题 (Facilities)
- 清洁卫生 (Cleanliness)
- 空调 (AC)
- 水质 (Water)
- 虫害 (Pest)
- 其他

### 4. Time Distribution
- Cases by month / quarter
- Peak complaint hours
- Seasonal patterns

### 5. Financial Impact
- Compensation amounts
- Average compensation by category
- Compensation trends

### 6. Root Cause Analysis
- By department responsibility
- Common patterns
- Repeat issues

### 7. Risk Prediction
- Emerging patterns
- Preventive recommendations
- Cross-station alerts (tie to RISK/FSAA/MEP)

### 8. Top SOP Suggestions
- Most-needed SOPs based on case frequency
- Improvement priority scoring

## Output Format

```
============================================================
  GSM投诉体系 · 深度全维分析
  {date}
============================================================

【1. 知识空间概览】
  CASE_: {n} | CMP_: {n} | RCASE_: {n} | FAQ_: {n} | ...

【2. 案例库 ({n}个案例)】
  活跃: {n} | 已结案: {n}
  本月新增: {n}

【3. 投诉分类】
  {category}: {n} ({pct}%)

【4. 财务影响】
  总赔偿: ¥{total} | 平均¥{avg}
  {category}赔偿最高: ¥{max}

【5. 趋势与建议】
  ...
```

## Cross-station Analysis

When the user asks, also check:
- **RISK**: `risk_graph.json` for related risk items
- **FSAA**: for food safety related complaints
- **MEP**: for facility/AC related complaints
