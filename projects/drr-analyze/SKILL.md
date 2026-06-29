---
name: "drr-analyze"
description: "Analyze DRR Excel: daily revenue, Occ, ADR, GOP, budget comparisons"
---

# DRR Revenue Analysis

Analyzes Daily Revenue Report (DRR) Excel files from the incoming folder.
Extracts occupancy, ADR, RevPAR, F&B revenue by outlet, GOP, and compares against budget and last year.

## File Location

DRR files are at `media/incoming/` — named like `Daily_Revenue_Report_2026.06.15---*.xlsx`.

## Workflow

### 1. Find the DRR file
Scan `media/incoming/` for unprocessed `.xlsx` files matching `Daily_Revenue_Report` pattern.

### 2. Parse the Excel
Use openpyxl with `data_only=True`. The DRR has these sheet sections:

**Sheet "Data" — OCC section (rows 3-14):**
- Row 5: Rooms Sold (入住)
- Row 6: Comp/扣减
- Row 7: House Use
- Row 8: OOO
- Row 12: Occ%
- Row 13: RevPAR
- Row 14: ADR
- Column B onward = Day 1, 2, 3...

**Sheet "Data" — Revenue section (rows 16-32):**
- Column D: label
- Column E: Today (当日)
- Column F: Budget (预算)
- Column G: Last Year (上年)
- Column H: MTD
- Column I: MTD Budget (MTD预算)
- Column J: MTD Last Year (MTD上年)

**Labels to extract:**
- 客房部收入, 客房收入(前厅收入)
- 餐饮收入(不含宴会) / 餐饮收入合计
- 宴会及其他餐饮
- 其他营业部门小计
- 营业总收入
- GOP / GOP%

**Key formulas:**
- RevPAR = Rooms Revenue / Available Rooms
- ADR = Rooms Revenue / Rooms Sold
- Occ% = Rooms Sold / Available Rooms × 100%
- GOP% = GOP / Total Revenue × 100%

### 3. Generate analysis report

Output a structured report with:

```
=== DRR 分析报告: #{date} ===

📊 客房核心指标
  当日: 入住 X间 | Occ XX.X% | ADR ¥XXX | RevPAR ¥XXX
  MTD:  入住 X间 | Occ XX.X% | ADR ¥XXX | RevPAR ¥XXX
  YTD:  入住 X间 | Occ XX.X% | ADR ¥XXX | RevPAR ¥XXX

💰 营收总览
  当日: ¥XXX (预算 ¥XXX → ±X.X%)
  MTD:  ¥XXX (预算 ¥XXX → ±X.X%)
  YTD:  ¥XXX (预算 ¥XXX → ±X.X%)

🍽️ 餐饮各点位(当日)
  OPEN:    ¥XX,XXX | 人数XX | 人均¥XX
  YUXI:    ¥XX,XXX | 人数XX | 人均¥XX
  BACIO:   ¥XX,XXX | 人数XX | 人均¥XX
  YUAN:    ¥XX,XXX | 人数XX | 人均¥XX
  宴会:     ¥XX,XXX | 人数XX
  送餐:     ¥XX,XXX
  啤酒荟:   ¥XX,XXX
  美食屋:   ¥XX,XXX

🔑 关键洞察
  - 亮点/异常 (对比预算/上年/趋势)
  - 问题点位
  - 建议

📈 逐日趋势 (本月已过天数)
  日期 | 入住 | Occ% | ADR | RevPAR | 备注
```

### 4. Save output
Write the analysis to `knowledge_center/drr_analysis/{date}_analysis.md`.

## Script Template

```python
import openpyxl, json, os, sys
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

# === CONFIG ===
DRR_FILE = 'media/incoming/Daily_Revenue_Report_2026.06.15---*.xlsx'
OUTPUT_DIR = 'knowledge_center/drr_analysis/'
```

Replace DRR_FILE path with the actual file found.

## Integration with FIN station

After analysis, ask if it should be imported into `fin_graph.json` via the **kg-update** skill.
