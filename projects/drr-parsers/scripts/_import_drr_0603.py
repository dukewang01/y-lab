#!/usr/bin/env python3
"""Import 2026-06-03 DRR Excel into FIN graph."""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0603.json'
XLSX_PATH = r'knowledge_center\..\media\incoming\Daily_Revenue_Report_2026.06.03.xlsx'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
ws = wb['Actual']

def n(r, c):
    v = ws.cell(r, c).value
    if v is None or not isinstance(v, (int, float)):
        return None
    return float(v)

def pct_col(r, c):
    v = ws.cell(r, c).value
    if v is None or not isinstance(v, (int, float)):
        return None
    return round(v * 100, 2)

data = {}
data['room_sold'] = n(15, 5)
data['room_sold_mtd'] = n(15, 8)
data['room_sold_mtd_budget'] = n(15, 9)
data['room_sold_mtd_ly'] = n(15, 10)
data['occ_pct'] = pct_col(22, 5)
data['occ_pct_mtd'] = pct_col(22, 8)
data['occ_pct_mtd_budget'] = pct_col(22, 9)
data['occ_pct_mtd_ly'] = pct_col(22, 10)
data['arr'] = n(24, 5)
data['arr_mtd'] = n(24, 8)
data['arr_mtd_budget'] = n(24, 9)
data['arr_mtd_ly'] = n(24, 10)
data['revpar'] = n(23, 5)
data['revpar_mtd'] = n(23, 8)
data['revpar_mtd_budget'] = n(23, 9)
data['revpar_mtd_ly'] = n(23, 10)
data['room_revenue_total'] = n(26, 5)
data['room_revenue_mtd'] = n(26, 8)
data['room_revenue_mtd_budget'] = n(26, 9)
data['room_revenue_mtd_ly'] = n(26, 10)
data['other_income'] = n(27, 5)
data['other_income_mtd'] = n(27, 8)
data['service_charge'] = n(28, 5)
data['service_charge_mtd'] = n(28, 8)
data['net_room_revenue'] = n(29, 5)
data['net_room_revenue_mtd'] = n(29, 8)
data['comp_rooms'] = n(16, 5)
data['comp_rooms_mtd'] = n(16, 8)
data['house_use'] = n(17, 5)
data['house_use_mtd'] = n(17, 8)
data['ooo_rooms'] = n(18, 5)
data['ooo_rooms_mtd'] = n(18, 8)
data['oos_rooms'] = n(19, 5)
data['oos_rooms_mtd'] = n(19, 8)
data['vacant_rooms'] = n(20, 5)
data['vacant_rooms_mtd'] = n(20, 8)
data['available_rooms'] = n(21, 5)
data['guest_count'] = n(25, 5)

# F&B
ws_fb = wb['F&B']
data['fb_today'] = ws_fb.cell(20, 2).value
data['fb_mtd'] = ws_fb.cell(20, 7).value
data['fb_mtd_budget'] = ws_fb.cell(20, 10).value
data['fb_mtd_ly'] = ws_fb.cell(20, 8).value

date_str = '2026-06-03'
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
        'type': 'daily_revenue',
        'properties': {}
    }
    entities.append(node)
    props = node['properties']
    print(f"Create: {day_id}")

for k, v in data.items():
    if v is not None:
        props[k] = v

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nSaved: {len(entities)} entities")
print(f"\n=== 2026-06-03 (Wed) DRR ===")
print(f"Rooms Sold: {data['room_sold']:.0f} (MTD: {data['room_sold_mtd']:.0f})")
print(f"Occ: {data['occ_pct']:.1f}% (MTD: {data['occ_pct_mtd']:.1f}%) vs Budget {data['occ_pct_mtd_budget']:.1f}%")
print(f"ADR: {data['arr']:.0f} (MTD: {data['arr_mtd']:.0f})")
print(f"RevPAR: {data['revpar']:.0f} (MTD: {data['revpar_mtd']:.0f})")
print(f"Room Rev: {data['room_revenue_total']:,.0f} (MTD: {data['room_revenue_mtd']:,.0f})")
print(f"F&B Rev: {data['fb_today']:,.0f} (MTD: {data['fb_mtd']:,.0f})")
print(f"Comp={data['comp_rooms']:.0f}, HU={data['house_use']:.0f}, OOO={data['ooo_rooms']:.0f}")

# MTD Summary for June
print(f"\n=== 6月MTD（至6/3）===")
print(f"已售房累计: {data['room_sold_mtd']:.0f} / 预算 {data['room_sold_mtd_budget']:.0f}")
print(f"Rooms Rev MTD: {data['room_revenue_mtd']:,.0f} / Bud {data['room_revenue_mtd_budget']:,.0f}")
print(f"F&B MTD: {data['fb_mtd']:,.0f} / Bud {data['fb_mtd_budget']:,.0f}")

# Compare with LY
print(f"\n=== 同比 LY (2025-06-03 MTD) ===")
print(f"LY Occ: {data['occ_pct_mtd_ly']:.1f}% | 本年: {data['occ_pct_mtd']:.1f}% -> {'↑' if data['occ_pct_mtd'] and data['occ_pct_mtd_ly'] and data['occ_pct_mtd'] > data['occ_pct_mtd_ly'] else '↓'}{abs(data['occ_pct_mtd'] - data['occ_pct_mtd_ly']) if data['occ_pct_mtd'] and data['occ_pct_mtd_ly'] else '?'}")
print(f"LY ADR: {data['arr_mtd_ly']:.0f} | This Yr: {data['arr_mtd']:.0f}")
print(f"LY Rooms Rev: {data['room_revenue_mtd_ly']:,.0f} | This Yr: {data['room_revenue_mtd']:,.0f}")
