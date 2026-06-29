---
name: "drr-analyze"
description: "Analyze DRR Excel: daily revenue, Occ, ADR, GOP, budget comparisons"
---

# DRR Revenue Analysis

Analyzes Daily Revenue Report (DRR) Excel files from the incoming folder.
Extracts occupancy, ADR, RevPAR, F&B revenue by outlet, GOP, and compares against budget and last year.

## File Location

DRR files are at `media/incoming/` — named like `Daily_Revenue_Report_2026.06.15---*.xlsx`.
After processing, archived to `media/archived/`.

## Workflow

### 1. Find and copy the DRR file
Scan `media/incoming/` for unprocessed `.xlsx` files matching `Daily_Revenue_Report` pattern.
Alternatively, the file may already be in `media/inbound/` (feishu upload) — copy to incoming then process.
Archived files in `media/archived/` can also be analyzed by path.

### 2. Parse the Excel
Use openpyxl with `data_only=True`. The DRR has these sheets:

**Sheet "Data" — OCC section:**
- Row 3: Day number index (1, 2, 3... 7)
- Row 5: Rooms Sold (入住)
- Row 6: Comp/扣减
- Row 7: House Use
- Row 8: OOO
- Row 10: Vacant (空房)
- Row 11: Available (可用房)
- Row 12: % Occupancy (Occ%)
- Row 13: RevPAR
- Row 14: Average Room Rate (ADR)
- Row 15: Occupied x Available (not used)
- Row 16: Rooms Revenue (客房收入)

**Column mapping:**
- Col B (index 2) = Day 1
- Col C (index 3) = Day 2
- ... Col H (index 8) = Day 7

**Day-to-date mapping (June 22-28 example):**
- Col 2 = 6/22(Mon) | Col 3 = 6/23(Tue) | Col 4 = 6/24(Wed) | Col 5 = 6/25(Thu)
- Col 6 = 6/26(Fri) | Col 7 = 6/27(Sat) | Col 8 = 6/28(Sun)
- Day 1 column always = Monday of the reporting week
- The report always covers the prior week (Mon-Sun)

**Sheet "F&B" — F&B by outlet:**
- Column A: outlet name
- Columns by day (same column mapping as Data sheet)
- Revenue and covers in adjacent columns per day
- Row 3 onward: individual outlets

**Sheet "Actual" — Revenue with budget/prior year comparison:**
- Column D: label names
- Column E: Today (当日)
- Column F: Budget (预算)
- Column G: Last Year (上年)
- Column H: MTD
- Column I: MTD Budget
- Column J: MTD Last Year
- Column K: YTD
- Column L: YTD Budget
- Column M: YTD Last Year

**Key labels to find in Actual sheet:**
- 客房部收入 / 客房收入(前厅收入)
- 餐饮收入合计 / 餐饮收入(不含宴会)
- 宴会及其他餐饮
- 其他营业部门小计
- 营业总收入
- GOP / GOP%

**Key formulas:**
- RevPAR = Rooms Revenue / Available Rooms
- ADR = Rooms Revenue / Rooms Sold
- Occ% = Rooms Sold / Available Rooms × 100%
- GOP% = GOP / Total Revenue × 100%

**⚠️ Gotchas:**
- Column D label matching: use `str(label).strip() in labels_to_find`
- Some rows have merged label names — try partial match as fallback
- F&B covers column may be 2 columns after revenue col (not 1)
- Day 1 (Monday) may have 0 data if the week starts Tuesday

### 3. Generate analysis report

Report format:

```
=== DRR 分析报告: {date} ===

【1】客房逐日
  {date:>10} | {sold:>4}间 | Occ {occ:>5.1f}% | ADR ¥{adr:>5.0f} | RevPAR ¥{rp:>5.0f} | 客房收入 ¥{rv:>7,.0f}
  ...

【2】{filename_date} 单日详解
  入住: {n}间 | 空房: {n}间
  Occ: {x}% | ADR: ¥{x} | RevPAR: ¥{x}
  客房收入: ¥{x}

【3】营收对比
  {label:>20}: ¥{today:>8,.0f} 预算¥{budget:>8,.0f} ({variance:+.1f}%) vs去年{variance:+.1f}%

【4】F&B各点位
  {outlet:>30}: ¥{rev:>8,.0f} | 人数{n} | 人均¥{x}

【5】关键洞察
  - 周均Occ {x}% — 旺季/淡季判断
  - 最佳/最弱日
  - 工作日 vs 周末对比
  - 问题/建议
```

### 4. Save output
Write the analysis to `knowledge_center/drr_analysis/{date}_analysis.md`.

### 5. Import to FIN station
If user confirms, add the data to `fin_graph.json` using **kg-update** skill.
Entities follow FIN format: `{'id': 'DAILY_yyyy_mm_dd', 'name': '...', 'type': 'daily_report', 'properties': {...}}`

## Script Template

```python
import openpyxl, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# === CONFIG ===
DRR_FILE = 'media/archived/Daily_Revenue_Report_2026.06.26---*.xlsx'
OUTPUT_DIR = 'knowledge_center/drr_analysis/'

def get_cell(ws, r, c):
    v = ws.cell(r, c).value
    if v is None: return 0
    if isinstance(v, (int, float)): return float(v)
    try: return float(v)
    except: return 0

# Day mapping
days = ['6/22(一)', '6/23(二)', '6/24(三)', '6/25(四)', '6/26(五)', '6/27(六)', '6/28(日)']

# Load workbook
wb = openpyxl.load_workbook(DRR_FILE, data_only=True)
ws = wb['Data']

# For each day column (col 2-8)
for i, d in enumerate(days):
    c = i + 2
    sold = int(get_cell(ws, 5, c))
    occ = get_cell(ws, 12, c) * 100
    adr = get_cell(ws, 14, c)
    rv = get_cell(ws, 16, c)
    # ... print result
```

## Integration with FIN station

After analysis, ask if it should be imported into `fin_graph.json` via **kg-update**.
