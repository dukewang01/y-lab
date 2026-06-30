#!/usr/bin/env python3
"""2026-06-11: Import 2026-06-10 DRR Excel into FIN graph.
   Source: Daily_Revenue_Report_2026.06.10---3f8a6402-062e-4834-a133-f93c98f2e59d.xlsx
"""
import json, openpyxl

FP = r'knowledge_center\fin_graph.json'
XLSX = r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.06.10---3f8a6402-062e-4834-a133-f93c98f2e59d.xlsx'

with open(FP, 'r', encoding='utf-8') as f:
    g = json.load(f)

entities = g['entities']

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws_a = wb['Actual']
ws_fb = wb['F&B']

def n(r, c):
    v = ws_a.cell(r, c).value
    if v is None or not isinstance(v, (int, float)):
        return None
    return round(float(v), 2)

def pct_col(r, c):
    v = ws_a.cell(r, c).value
    if v is None or not isinstance(v, (int, float)):
        return None
    return round(v * 100, 2)

# ===== Actual Sheet Data =====
# Row 15: ROOM SOLD
# Row 16: COMPLIMENTARY
# Row 17: HOUSE USE
# Row 18: OUT OF ORDER
# Row 19: OUT OF SERVICE
# Row 20: VACANT
# Row 21: AVAILABLE
# Row 22: % Occupancy
# Row 23: REVPAR
# Row 24: AVERAGE ROOM RATE
# Row 25: GUEST COUNT
# Row 26: TOTAL ROOMS REVENUE
# Row 27: OTHER INCOME
# Row 28: SERVICE CHARGE
# Row 29: ROOM REVENUE
# Row 30: INCLUDE CONDO ROOM SOLD
# Row 31: INCLUDE CONDO ROOM REVENUE
# Row 44: TOTAL FOOD COVERS
# Row 68: TOTAL FOOD REVENUE
# Row 80: TOTAL BEVERAGE REVENUE
# Row 92: TOTAL F&B SUNDRY REVENUE
# Row 95: TOTAL F&B REVENUE
# Row 106: TOTAL OOD/OTHER INCOME
# Row 107: TOTAL REVENUE

data = {}

# --- Daily ---
data['room_sold'] = n(15, 5)                   # Column E (5)
data['comp_rooms'] = n(16, 5)
data['house_use'] = n(17, 5)
data['ooo'] = n(18, 5)
data['oos'] = n(19, 5)
data['vacant'] = n(20, 5)
data['available'] = n(21, 5)
data['occ_pct'] = pct_col(22, 5)
data['revpar'] = n(23, 5)
data['adr'] = n(24, 5)
data['guest_count'] = n(25, 5)
data['total_rooms_revenue'] = n(26, 5)
data['other_income'] = n(27, 5)
data['service_charge'] = n(28, 5)
data['room_revenue'] = n(29, 5)
data['condo_sold'] = n(30, 5)
data['condo_revenue'] = n(31, 5)
data['food_covers_total'] = n(44, 5)
data['food_revenue'] = n(68, 5)
data['beverage_revenue'] = n(80, 5)
data['fb_sundry'] = n(92, 5)
data['fb_total'] = n(95, 5)
data['ood_total'] = n(106, 5)
data['total_revenue'] = n(107, 5)

# --- MTD (Month to Date) ---
data['room_sold_mtd'] = n(15, 8)
data['room_sold_mtd_budget'] = n(15, 9)
data['room_sold_mtd_ly'] = n(15, 10)
data['occ_pct_mtd'] = pct_col(22, 8)
data['occ_pct_mtd_budget'] = pct_col(22, 9)
data['occ_pct_mtd_ly'] = pct_col(22, 10)
data['revpar_mtd'] = n(23, 8)
data['revpar_mtd_budget'] = n(23, 9)
data['revpar_mtd_ly'] = n(23, 10)
data['adr_mtd'] = n(24, 8)
data['adr_mtd_budget'] = n(24, 9)
data['adr_mtd_ly'] = n(24, 10)
data['room_rev_mtd'] = n(26, 8)
data['room_rev_mtd_budget'] = n(26, 9)
data['room_rev_mtd_ly'] = n(26, 10)
data['fb_total_mtd'] = n(95, 8)
data['fb_total_mtd_ly'] = n(95, 10)
data['total_rev_mtd'] = n(107, 8)
data['total_rev_mtd_budget'] = n(107, 9)
data['total_rev_mtd_ly'] = n(107, 10)
data['food_rev_mtd'] = n(68, 8)
data['food_rev_mtd_ly'] = n(68, 10)
data['beverage_rev_mtd'] = n(80, 8)
data['beverage_rev_mtd_ly'] = n(80, 10)

# --- Daily variance vs budget ---
data['room_sold_vs_budget'] = n(15, 7) - n(15, 6) if n(15, 6) is not None else None  # Actual - Budget
data['occ_vs_budget'] = pct_col(22, 5) - pct_col(22, 6) if n(22,6) is not None else None
data['adr_vs_budget'] = n(24,5) - n(24,6) if n(24,6) else None

# ===== F&B Sheet - Outlet Detail =====
# F&B sheet structure (row 11-20):
# Col B = Today Revenue, Col F = MTD Covers, Col G = MTD Revenue, Col H = LY MTD, Col I = Forecast MTD, Col J = Budget MTD
outlets = {}
outlet_rows = {
    'Banquet_C&E': 11,
    'OPEN': 12,
    'YUXI': 13,
    'BACIO': 14,
    'BEER SOCIETY': 15,
    'YUAN': 16,
    'FOOD STORE': 17,
    'ROOM SERVICE': 18,
    'MINI BAR': 19,
    'TOTAL_FB': 20,
    'TOTAL_FB_EXCL_CE': 21,
}
for k, r in outlet_rows.items():
    rev_today = ws_fb.cell(r, 2).value
    covers_mtd = ws_fb.cell(r, 6).value
    rev_mtd = ws_fb.cell(r, 7).value
    rev_mtd_ly = ws_fb.cell(r, 8).value
    rev_mtd_forecast = ws_fb.cell(r, 9).value
    rev_mtd_budget = ws_fb.cell(r, 10).value
    outlets[k] = {
        'rev_today': round(float(rev_today), 2) if isinstance(rev_today, (int,float)) else (0 if rev_today in (0, '#REF!', None) else None),
        'covers_mtd': int(covers_mtd) if isinstance(covers_mtd, (int,float)) else (0 if covers_mtd in (0, None) else None),
        'rev_mtd': round(float(rev_mtd), 2) if isinstance(rev_mtd, (int,float)) else (0 if rev_mtd in (0, None) else None),
        'rev_mtd_ly': round(float(rev_mtd_ly), 2) if isinstance(rev_mtd_ly, (int,float)) else None,
        'rev_mtd_forecast': round(float(rev_mtd_forecast), 2) if isinstance(rev_mtd_forecast, (int,float)) else None,
        'rev_mtd_budget': round(float(rev_mtd_budget), 2) if isinstance(rev_mtd_budget, (int,float)) else None,
    }

# ===== Create/Update daily node =====
date_str = '2026-06-10'
day_id = f'day_{date_str}'

existing = [e for e in entities if e.get('id') == day_id]
if existing:
    node = existing[0]
    node.setdefault('properties', {})
    props = node['properties']
    print(f"Update: {day_id}")
else:
    node = {
        'id': day_id,
        'name': f'日报 {date_str}',
        'date': date_str,
        'dow': 'Wed',
        'type': 'daily_revenue',
        'properties': {}
    }
    entities.append(node)
    props = node['properties']
    print(f"Create: {day_id}")

# Core metrics
for k, v in data.items():
    if v is not None:
        props[k] = v

# Outlet data
for outlet_name, odata in outlets.items():
    for k, v in odata.items():
        if v is not None:
            props[f'fb_{outlet_name}_{k}'] = v

g['entities'] = entities

# ===== Update version =====
g['meta']['version'] = 'v9.1'
g['meta']['updated'] = '2026-06-11 09:30'
g['meta']['description'] = 'v9.0 + DRR 2026-06-10'

with open(FP, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

# ===== Summary =====
print(f"\n=== DRR 2026-06-10 (Wed) ===")
print(f"Rooms Sold: {data['room_sold']:.0f} (MTD: {data['room_sold_mtd']:.0f})")
print(f"Occ: {data['occ_pct']:.1f}% (MTD: {data['occ_pct_mtd']:.1f}%) vs Budget {data['occ_pct_mtd_budget']:.1f}% vs LY {data['occ_pct_mtd_ly']:.1f}%")
print(f"ADR: {data['adr']:.0f} (MTD: {data['adr_mtd']:.0f}) vs Budget {data['adr_mtd_budget']:.0f}")
print(f"RevPAR: {data['revpar']:.0f} (MTD: {data['revpar_mtd']:.0f})")
print(f"Room Rev: {data['total_rooms_revenue']:,.0f} (MTD: {data['room_rev_mtd']:,.0f}) vs Budget {data['room_rev_mtd_budget']:,.0f} vs LY {data['room_rev_mtd_ly']:,.0f}")
print(f"F&B Rev: {data['fb_total']:,.0f} (MTD: {data['fb_total_mtd']:,.0f})")
print(f"Total Rev: {data['total_revenue']:,.0f} (MTD: {data['total_rev_mtd']:,.0f})")

print(f"\n=== 6月MTD（至6/10）===")
print(f"已售房: {data['room_sold_mtd']:.0f} / 预算 {data['room_sold_mtd_budget']:.0f} / 去年 {data['room_sold_mtd_ly']:.0f}")
print(f"Rev MTD: {data['room_rev_mtd']:,.0f} / Bud {data['room_rev_mtd_budget']:,.0f} / LY {data['room_rev_mtd_ly']:,.0f}")
print(f"F&B MTD: {data['fb_total_mtd']:,.0f} / LY {data['fb_total_mtd_ly']:,.0f}")

print(f"\n=== F&B Outlet Detail (MTD) ===")
for k, odata in sorted(outlets.items()):
    if k.startswith('TOTAL'):
        continue
    r = odata.get('rev_mtd', 0)
    c = odata.get('covers_mtd', 0)
    if r and r > 0:
        print(f"  {k}: Rev {r:,.0f} ({c} covers)")

print(f"\nFIN站版本: v9.1")
print(f"当前FIN站: 实体{len(g['entities'])} / 关系{len(g.get('relations', []))}")
