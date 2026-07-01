# DRR Revenue Analysis v2

Analyzes Daily Revenue Report (DRR) Excel files from the incoming folder.
Extracts occupancy, ADR, RevPAR, F&B revenue by outlet, GOP, and compares against budget and last year.
**v2 update (2026-06-30)**: Added verified column/row mappings from Actual sheet (PMS/LASATA format). Fixed Condo double-counting warning.

## File Location

DRR files arrive via Feishu â†?`C:\Users\Y\media\inbound\DRR_*.xlsx`
After processing, archive to `media/archived/`.

## Actual Sheet Structure (verified 2026-06-29)

This is the PMS/LASATA-generated DRR. The **Actual** sheet is the primary data sheet.

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

### âš ï¸ Condo Warning
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
ðŸ“Š **{date} æ—¥æŠ¥**
**ðŸ¨ å®¢æˆ¿**: {sold}é—?/ Occ {occ:.1%} / ADR Â¥{adr:,.0f}
   RevPAR Â¥{revpar:,.0f} | å®¢æˆ¿æ”¶å…¥ Â¥{room_rev:,.0f}ï¼ˆé¢„ç®—Â¥{bud:,.0f}ï¼?**ðŸ½ï¸?F&B**: Â¥{fb_total:,.0f}ï¼ˆé¢„ç®—Â¥{fb_bud:,.0f}ï¼?
ðŸ“ˆ **MTD ({mtd_days}å¤?**
   å‡ºç§Ÿ {mtd_sold:,}é—?/ Occ {mtd_occ:.1%} / ADR Â¥{mtd_adr:,.0f}
   å®¢æˆ¿æ”¶å…¥ Â¥{mtd_rev:,.0f}ï¼ˆé¢„ç®—Â¥{mtd_bud:,.0f}ï¼Œå·®è·Â¥{gap:,.0f})

âš ï¸ **å…³æ³¨ç‚?*: {observations}
```

## Observation Points

1. **Daily vs Budget vs LY** â€?Room Sold, Occ%, ADR, RevPAR
2. **MTD gap vs Budget** â€?How far behind/above monthly target
3. **Month Forecast** â€?Is forecast realistic vs MTD?
4. **YTD trend** â€?Cumulative gaps vs annual targets
5. **F&B outlier** â€?Any outlet significantly under/over budget
6. **Anomaly** â€?Health club >Â¥30k (annual fee entry), laundry spike, BEER=0


---

## Variant: Meal-Period DRR (Monthly Horizontal Layout)

Some DRR files use a horizontal monthly layout instead of the vertical Actual sheet.
Each month is a separate sheet with daily columns across.

### Sheet Layout
- Each sheet = one month (named e.g. 202601, 202602, ...)
- Row 3: daily dates (col E onwards)
- After daily columns: Total | (blank) | Owner Budget | Budget Per Day | MTD Budget | VS Budget | Last Year | VS LY | ...

### Column Map (verified)
| Index | Content | Note |
|:-----:|:--------|:-----|
| 3 | Row Label | e.g. ROOM SOLD |
| 4 | Day 1 | First day of month |
| 4+N-1 | Day N | Last day |
| 4+N | Monthly Total | |
| 4+N+2 | Owner Budget | Monthly target |

N = days in month.

### Key Rows
Room: 5(SOLD), 25(OCC%), 26(REVPAR), 27(ARR), 56(ROOMS REV)
F&B: 92(COVERS), 124(AVG CHECK), 161(FOOD REV), 173(BEV REV), 180(FB REV), 192(TOTAL REV)

### Meal Period Revenue Rows
132 Breakfast(11101), 133 Lunch(11101), 134 Dinner(11101), 135 Brunch(11101)
137 Lunch(11102), 138 Dinner(11102), 139 Brunch(11102), 142 Dinner(11104)
127 Breakfast(11161), 129 Lunch(11161), 130 Dinner(11161), 128 Coffee Break
