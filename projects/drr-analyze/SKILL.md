# DRR Revenue Analysis v2

Analyzes Daily Revenue Report (DRR) Excel files from the incoming folder.
Extracts occupancy, ADR, RevPAR, F&B revenue by outlet, GOP, and compares against budget and last year.
**v2 update (2026-06-30)**: Added verified column/row mappings from Actual sheet (Hilton OnQ/LASATA format). Fixed Condo double-counting warning.

## File Location

DRR files arrive via Feishu → `C:\Users\Duke Wang\media\inbound\DRR_*.xlsx`
After processing, archive to `media/archived/`.

## Actual Sheet Structure (verified 2026-06-29)

This is the Hilton OnQ/LASATA-generated DRR. The **Actual** sheet is the primary data sheet.

### Column Map (Actual Sheet)

| Col | Content | Note |
|:---:|:--------|:-----|
| D(4) | Date | DAILY date |
| E(5) | **Daily Actual** | Key column - today's actual |
| F(6) | Daily Budget | Owner Budget |
| G(7) | Daily LY | Last Year same day |
| H(8) | **MTD Actual** | Month To Date cumulative |
| I(9) | MTD Budget | |
| J(10) | MTD LY | |
| K(11) | MTD vs Budget | Variance |
| L(12) | MTD vs LY | |
| M(13) | Whole Month Budget | |
| N(14) | Whole Month Forecast | |
| O(15) | **YTD Actual** | Year To Date cumulative |
| P(16) | YTD LY | |
| Q(17) | YTD Budget | |
| R(18) | YTD vs Budget | |

### Key Row Numbers (Actual Sheet)

**Room Metrics (rows 15-29):**
| Row | Label | Notes |
|:---:|:------|:------|
| 15 | ROOM SOLD | Rooms sold (excl. comp/house use) |
| 22 | % Occupancy | Decimal format, e.g. 0.6468 = 64.68% |
| 23 | REVPAR | Revenue Per Available Room |
| 24 | AVERAGE ROOM RATE | ADR |
| 29 | ROOM REVENUE | Total rooms revenue (incl. service charge) |

**Room Adjustments (rows 16-21):**
16=COMPLIMENTARY, 17=HOUSE USE, 18=OUT OF ORDER, 19=OUT OF SERVICE, 20=VACANT, 21=AVAILABLE

**F&B Revenue by Outlet (rows 58-68):**
| Row | Outlet | Category |
|:---:|:-------|:---------|
| 58 | BANQUET AND CONFERENCE | C&E |
| 59 | OPEN | Food |
| 60 | YUXI | Food |
| 61 | BACIO | Food |
| 62 | BEER SOCIETY | Food |
| 63 | YUAN | Food |
| 64 | FOOD STORE | Food |
| 65 | ROOM SERVICE | Food |
| 66 | MINI BAR | Food |
| 68 | TOTAL FOOD | Sum |

**Beverage by Outlet (rows 70-80):**
70-77 = each outlet beverage, 80 = TOTAL BEVERAGE

**Summary Rows:** 93=C&E, 94=F&B OUTLETS, 95=TOTAL F&B, 97=LAUNDRY, 98=HEALTH CLUB, 100=TELEPHONE

### ⚠️ Condo Warning
Condo rows 30-32 are **INCLUDED** in total rooms (row 15) and revenue (row 29). Never add condo separately.

## Python Parsing Pattern

```python
import openpyxl
wb = openpyxl.load_workbook(r'path\to\DRR.xlsx', data_only=True)
ws = wb['Actual']

def cell(r, c):
    v = ws.cell(r, c).value
    return float(v) if v else 0.0

report = {
    'daily': {'rooms_sold': cell(15,5), 'occ': cell(22,5), 'adr': cell(24,5), 'revpar': cell(23,5), 'room_revenue': cell(29,5), 'fb_total': cell(95,5)},
    'mtd': {'rooms_sold': cell(15,8), 'occ': cell(22,8), 'adr': cell(24,8), 'revpar': cell(23,8), 'room_revenue': cell(29,8), 'fb_total': cell(95,8)},
    'fb_outlets_mtd': {'banquet': cell(58,8), 'open': cell(59,8), 'yuxi': cell(60,8), 'bacio': cell(61,8), 'beer': cell(62,8), 'yuan': cell(63,8), 'food_store': cell(64,8), 'room_service': cell(65,8)},
    'month_target': {'room_budget': cell(29,13), 'room_forecast': cell(29,14)},
}
```

## Analysis Report Template

```
📊 **{date} 日报**
**🏨 客房**: {sold}间 / Occ {occ:.1%} / ADR ¥{adr:,.0f}
   RevPAR ¥{revpar:,.0f} | 客房收入 ¥{room_rev:,.0f}（预算¥{bud:,.0f}）
**🍽️ F&B**: ¥{fb_total:,.0f}（预算¥{fb_bud:,.0f}）

📈 **MTD ({mtd_days}天)**
   出租 {mtd_sold:,}间 / Occ {mtd_occ:.1%} / ADR ¥{mtd_adr:,.0f}
   客房收入 ¥{mtd_rev:,.0f}（预算¥{mtd_bud:,.0f}，差距¥{gap:,.0f})

⚠️ **关注点**: {observations}
```

## Observation Points

1. **Daily vs Budget vs LY** — Room Sold, Occ%, ADR, RevPAR
2. **MTD gap vs Budget** — How far behind/above monthly target
3. **Month Forecast** — Is forecast realistic vs MTD?
4. **YTD trend** — Cumulative gaps vs annual targets
5. **F&B outlier** — Any outlet significantly under/over budget
6. **Anomaly** — Health club >¥30k (annual fee entry), laundry spike, BEER=0
