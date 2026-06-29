---
name: "pest-report"
description: "Generate PCO pest control analysis from FSAA graph with trends/risk"
---

# PEST Report

Generates comprehensive pest control (PCO) analysis reports from the FSAA knowledge graph, covering trend analysis, finding distribution, risk assessment, and recommendations.

## Data Source

- FSAA graph: `knowledge_center/fsaa_graph.json`
- Entities of type `fsaa_pco_report` and `fsaa_pco_finding`
- Cross-references: GSM graph for pest-related complaints, RISK graph for pest risk items

## Report Sections

### 1. Timeline
List all PCO reports by date, with high/medium risk finding counts and completion status.

### 2. Finding Distribution by Area
- Which areas (kitchen, restaurant, storage, guest room, public area, etc.)
- Which specific locations are most affected

### 3. Finding Distribution by Pest Type
- Rodents (rat/mouse)
- Insects (roach, fly, ant, beetle)
- Birds
- Other

### 4. Risk Assessment
- High-risk findings requiring immediate action
- Patterns across reports
- Recurring issues

### 5. Cross-Reference with GSM Complaints
- Pest-related guest complaints
- Link between PCO findings and guest experience

### 6. Recommendations
- Priority actions
- Preventive measures
- Follow-up schedule

## Output Format

```
# 苏州希尔顿 · 虫控报告全维分析

## 一、报告时间线
| 日期 | 轮次 | 问题数 | 🔴高危 | 🟡中危 | ❌未完成 |
|:---:|:---:|:---:|:---:|:---:|:---:|

## 二、区域分布
{area}: {n}个问题点
...

## 三、虫害类型分布
{type}: {n}个
...

## 四、风险评级

## 五、与GSM关联的虫害投诉

## 六、建议措施
```

## Script Template

```python
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

fsaa = json.load(open('knowledge_center/fsaa_graph.json', encoding='utf-8'))
entities = fsaa.get('entities', [])

reports = [e for e in entities if e.get('type') == 'fsaa_pco_report']
findings = [e for e in entities if e.get('type') == 'fsaa_pco_finding']

# Sort reports by date
reports.sort(key=lambda x: str(x.get('properties', {}).get('date', '')))

# Generate report...
for r in reports:
    p = r.get('properties', {})
    # ...
```
