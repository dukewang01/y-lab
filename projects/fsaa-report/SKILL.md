---
name: "fsaa-report"
description: "Generate daily FSAA food safety audit reports from knowledge graph"
---

# FSAA Report

Generates daily food safety audit status reports from the FSAA knowledge graph (`fsaa_graph.json`).

## Data Source

- Graph: `knowledge_center/fsaa_graph.json`
- PCO reports: imported into FSAA graph as `fsaa_pco_finding` entities

## Report Sections

### 1. Scale Overview
- Total entities and relationships
- Recent additions (changes since yesterday)

### 2. Core Domain Breakdown
Counts by category:
- 检查项与标准 (check items & standards)
- NC不符合项 (non-conformances)
- HACCP/过敏原/温控
- 存储/保质期
- 设备/工具
- 化学品/虫害
- 厨房/区域
- 审计体系/评分
- FAQs
- 供应商
- 餐饮菜单

### 3. PCO Status (if applicable)
- Open pest control issues
- Recent findings
- Action items due

### 4. Recent Activity
- New NCs opened
- NCs closed/resolved
- New audit paths completed

### 5. Risk Alerts
- Critical items requiring immediate attention
- Expired/long-overdue items

## Output Format

```
============================================================
  FSAA 食品安全审计工作站 · 每日推送
  日期: {date}
============================================================

📊 当前规模: 实体 {n} | 关系 {n}
🏗️ NC不符合项: {n}项
🔴 未关闭: {n} | 🟢 已关闭: {n}
🕐 新增({period}): {n}条

📋 PCO发现项: {n}
  活跃: {n} | 已解决: {n}

⚠️ 高风险项目: {n}项

近期关注:
  ...
```

## Script Template

```python
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('knowledge_center/fsaa_graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

entities = data.get('entities', [])
rels = data.get('relationships', []) + data.get('relations', [])

# Categorize entities by type
cats = {}
for e in entities:
    t = e.get('type', e.get('category', 'unknown'))
    cats.setdefault(t, 0)
    cats[t] += 1

# Print report...
```
