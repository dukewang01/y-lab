# DRR Auto Pipeline v2

The holy grail of DRR processing. When a DRR file arrives, run the full pipeline automatically.
**v2 update (2026-06-30)**: Added verified actual parsing code, JSON output schema, and Condo handling.

## Prerequisites

- `openpyxl` installed in Python
- DRR file from Feishu → lands at `C:\Users\Duke Wang\media\inbound\`

## Pipeline Steps

### Step 1: Find DRR File
```powershell
Get-ChildItem -Path "$env:USERPROFILE\media\inbound\" -Filter "*.xlsx" | Where-Object {$_.Name -match "DRR|Daily_Revenue"}
```

### Step 2: Parse Excel (Actual Sheet)
```python
import openpyxl, json, shutil
wb = openpyxl.load_workbook(filepath, data_only=True)
ws = wb['Actual']

def cell(r, c):
    v = ws.cell(r, c).value
    return float(v) if v else 0.0

drr = {
    'report_date': 'YYYY-MM-DD', 'mtd_days': 29,
    'daily': {'rooms_sold': cell(15,5), 'occ': cell(22,5), 'adr': cell(24,5), 'revpar': cell(23,5), 'room_revenue': cell(29,5), 'fb_total': cell(95,5)},
    'mtd': {'rooms_sold': cell(15,8), 'occ': cell(22,8), 'adr': cell(24,8), 'revpar': cell(23,8), 'room_revenue': cell(29,8), 'fb_total': cell(95,8)},
    'ytd': {'rooms_sold': cell(15,15), 'occ': cell(22,15), 'adr': cell(24,15), 'revpar': cell(23,15), 'room_revenue': cell(29,15), 'fb_total': cell(95,15)},
    'month_target': {'room_budget': cell(29,13), 'room_forecast': cell(29,14), 'fb_budget': cell(95,13), 'fb_forecast': cell(95,14)},
    'fb_outlets': {'banquet': cell(58,8), 'open': cell(59,8), 'yuxi': cell(60,8), 'bacio': cell(61,8), 'beer': cell(62,8), 'yuan': cell(63,8), 'food_store': cell(64,8), 'room_service': cell(65,8)},
    'daily_budget': {'rooms_sold': cell(15,6), 'adr': cell(24,6), 'room_revenue': cell(29,6), 'fb_total': cell(95,6)},
    'daily_ly': {'rooms_sold': cell(15,7), 'adr': cell(24,7), 'room_revenue': cell(29,7), 'fb_total': cell(95,7)},
    'other': {'laundry_daily': cell(97,5), 'health_club_daily': cell(98,5), 'laundry_mtd': cell(97,8), 'health_club_mtd': cell(98,8)},
    'condo': {'daily_sold': cell(30,5), 'daily_revenue': cell(31,5), 'mtd_sold': cell(30,8), 'mtd_revenue': cell(31,8)},
}
```

### Step 3: Save JSON
```python
kc_fin = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin'
os.makedirs(kc_fin, exist_ok=True)
with open(os.path.join(kc_fin, f'DRR_{YYYY_MM_DD}.json'), 'w', encoding='utf-8') as f:
    json.dump(drr, f, ensure_ascii=False, indent=2)
```

### Step 4: Archive Original
```powershell
Copy-Item $sourcePath -Destination "$archiveDir\DRR_{date}.xlsx" -Force
Remove-Item $sourcePath -Force
```

### Step 5: Generate Analysis (to Feishu)
```
📊 **{date} 日报**
🏨 {sold}间 / Occ {occ:.1%} / ADR ¥{adr:,.0f} / RevPAR ¥{revpar:,.0f}
   客房收入 ¥{rev:,.0f}（预算¥{bud:,.0f}）
🍽️ F&B: ¥{fb}（预算¥{fb_bud}）
📈 MTD: 客房¥{mtd_rev:,.0f}（差{mtd_gap:,.0f}）
⚠️ 全月预测: ¥{fcst:,.0f} / 预算¥{bud:,.0f}
```

### Step 6: (Optional) Update FIN Graph
Add daily entity to `fin_graph.json`:
```json
{"id":"DAILY_YYYY_MM_DD","type":"daily_report","properties":{"date":"2026-06-29","rooms_sold":348,"occ":0.6468,"adr":544.33,"room_revenue":189428.24}}
```

## Flags
- `--file <path>`: Process one file
- `--no-archive`: Keep in inbound
- `--dry-run`: Preview only
