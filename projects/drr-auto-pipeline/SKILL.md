---
name: "drr-auto-pipeline"
description: "One-command: DRR arrives → parse → analyze → import FIN → report"
---

# DRR Auto Pipeline

The holy grail of DRR processing. When a DRR file arrives, run the full pipeline automatically.

## Workflow

### Step 1: Find DRR file
Scan `media/incoming/` for `Daily_Revenue_Report*.xlsx`. 
Already archived files in `media/archived/` can also be processed by filename.

### Step 2: Parse (via drr-analyze skills)
Load the Excel, extract:
- Daily room data from Data sheet (rows 5-16)
- Revenue data from Actual sheet (labels + values)
- F&B by outlet from F&B sheet

### Step 3: Generate analysis (via drr-analyze)
Create report at `knowledge_center/drr_analysis/{date}_analysis.md`.

### Step 4: Import to FIN graph (via kg-update)
Create `fin_graph.json` entities:
- For each day in the week: `{'id': 'DAILY_yyyy_mm_dd', 'name': '...', 'type': 'daily_report', 'properties': {'date': '...', 'sold': n, 'occ': x, 'adr': x, 'rooms_revenue': x, 'fb_revenue': x, 'total_revenue': x}}`
- Link to month entity
- Create week summary entity

### Step 5: Auto-backup
Before writing `fin_graph.json`:
- Create backup: `fin_graph.bak.yyyymmdd_hhmmss.json`
- Write updated JSON

### Step 6: Report to user
```
=== DRR全自动流水线 ===
📎 文件: Daily_Revenue_Report_2026.06.28.xlsx
📊 分析完成 ✅ → drr_analysis/drr_0628_analysis.md
🗄️ FIN入库完成 ✅ → 新增{n}实体, {k}关系
  - 备份: fin_graph.bak.yyyymmdd_hhmmss.json
📦 已归档

本次新增:
  - 6/22(一): ...
  - 6/28(日): ...
```

## Pipeline Flags

- `--all`: Process ALL unprocessed DRR files in incoming
- `--file <path>`: Process one specific file
- `--no-import`: Analyze only, skip FIN import
- `--dry-run`: Show what would be done without actually writing
