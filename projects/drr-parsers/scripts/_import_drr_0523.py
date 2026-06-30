#!/usr/bin/env python3
"""Import 2026-05-23 DRR Excel into FIN graph.
Actual sheet layout: col C=label, D=today, E=budget, F=LY, G=MTD, H=MTD budget, I=MTD LY"""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0523_excel_import.json'
XLSX_PATH = r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.23---0ca44fc7-f465-4421-aff4-19d6f6aa52cd.xlsx'

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
    return float(v) if isinstance(v, int) else v

def pct_raw(r, c):
    v = ws.cell(r, c).value
    if v is None or not isinstance(v, (int, float)):
        return None
    return round(v * 100, 2)

# Actual sheet layout: C(4)=label, D(5)=Today, E(6)=Daily Budget, F(7)=LY Daily, G(8)=MTD, H(9)=MTD Budget, I(10)=MTD LY

# Row 15: Rooms Sold
r_sold = n(15, 5)
r_sold_daily_budget = n(15, 6)
r_sold_ly = n(15, 7)
r_sold_mtd = n(15, 8)
r_sold_mtd_budget = n(15, 9)
r_sold_mtd_ly = n(15, 10)

# Row 22: Occ%
occ_today = pct_raw(22, 5)
occ_daily_budget = pct_raw(22, 6)
occ_ly = pct_raw(22, 7)
occ_mtd = pct_raw(22, 8)
occ_mtd_budget = pct_raw(22, 9)
occ_mtd_ly = pct_raw(22, 10)

# Row 23: RevPAR
revpar_today = n(23, 5)
revpar_daily_budget = n(23, 6)
revpar_ly = n(23, 7)
revpar_mtd = n(23, 8)
revpar_mtd_budget = n(23, 9)
revpar_mtd_ly = n(23, 10)

# Row 24: ADR
adr_today = n(24, 5)
adr_daily_budget = n(24, 6)
adr_ly = n(24, 7)
adr_mtd = n(24, 8)
adr_mtd_budget = n(24, 9)
adr_mtd_ly = n(24, 10)

# Row 26: Room Revenue
room_rev_today = n(26, 5)
room_rev_daily_budget = n(26, 6)
room_rev_ly = n(26, 7)
room_rev_mtd = n(26, 8)
room_rev_mtd_budget = n(26, 9)
room_rev_mtd_ly = n(26, 10)

# Row 27: Other Income
other_inc_today = n(27, 5)
other_inc_mtd = n(27, 8)

# Row 28: Service Charge
sc_today = n(28, 5)
sc_mtd = n(28, 8)

# Row 29: Net Room Revenue
net_room_today = n(29, 5)
net_room_mtd = n(29, 8)

# Row 16-21: Room stats
comp_rooms = n(16, 5)
comp_mtd = n(16, 8)
house_use = n(17, 5)
house_mtd = n(17, 8)
ooo = n(18, 5)
ooo_mtd = n(18, 8)
oos = n(19, 5)
oos_mtd = n(19, 8)
vacant = n(20, 5)
vacant_mtd = n(20, 8)
available = n(21, 5)

# F&B sheet
ws_fb = wb['F&B']
# Row 11: Banquet, 12: OPEN, 13: YUXI, 14: BACIO, 15: BEER, 16: YUAN, 17: FOOD STORE, 18: ROOM SERVICE, 20: TOTAL
fb_today = ws_fb.cell(20, 2).value  # 141085.45
fb_mtd = ws_fb.cell(20, 7).value  # 2390000.59
fb_ly_mtd = ws_fb.cell(20, 8).value  # 2056925.33
fb_budget_mtd = ws_fb.cell(20, 10).value  # 2445691.41

print("=== Parsed 2026-05-23 ===")
print(f"Rooms: Today={r_sold}, MTD={r_sold_mtd}, MTD Budget={r_sold_mtd_budget}, MTD LY={r_sold_mtd_ly}")
print(f"Occupancy: Today={occ_today}%, MTD={occ_mtd}%, MTD Budget={occ_mtd_budget}%, MTD LY={occ_mtd_ly}%")
print(f"ADR: Today={adr_today}, MTD={adr_mtd}, MTD Budget={adr_mtd_budget}, MTD LY={adr_mtd_ly}")
print(f"RevPAR: Today={revpar_today}, MTD={revpar_mtd}, MTD Budget={revpar_mtd_budget}, MTD LY={revpar_mtd_ly}")
print(f"Room Rev: Today={room_rev_today}, MTD={room_rev_mtd}, MTD Budget={room_rev_mtd_budget}, MTD LY={room_rev_mtd_ly}")
print(f"FB Rev: Today={fb_today}, MTD={fb_mtd}")
print(f"Net Room: Today={net_room_today}, MTD={net_room_mtd}")

date_str = '2026-05-23'
day_id = f'day_{date_str}'

data = {
    'room_sold': r_sold, 'room_sold_mtd': r_sold_mtd,
    'room_sold_mtd_budget': r_sold_mtd_budget, 'room_sold_mtd_ly': r_sold_mtd_ly,
    'occ_pct': occ_today, 'occ_pct_mtd': occ_mtd,
    'occ_pct_mtd_budget': occ_mtd_budget, 'occ_pct_mtd_ly': occ_mtd_ly,
    'arr': adr_today, 'arr_mtd': adr_mtd,
    'arr_mtd_budget': adr_mtd_budget, 'arr_mtd_ly': adr_mtd_ly,
    'revpar': revpar_today, 'revpar_mtd': revpar_mtd,
    'revpar_mtd_budget': revpar_mtd_budget, 'revpar_mtd_ly': revpar_mtd_ly,
    'room_revenue_total': room_rev_today, 'room_revenue_mtd': room_rev_mtd,
    'room_revenue_mtd_budget': room_rev_mtd_budget, 'room_revenue_mtd_ly': room_rev_mtd_ly,
    'other_income': other_inc_today, 'other_income_mtd': other_inc_mtd,
    'service_charge': sc_today, 'service_charge_mtd': sc_mtd,
    'net_room_revenue': net_room_today, 'net_room_revenue_mtd': net_room_mtd,
    'comp_rooms': comp_rooms, 'comp_rooms_mtd': comp_mtd,
    'house_use': house_use, 'house_use_mtd': house_mtd,
    'ooo_rooms': ooo, 'ooo_rooms_mtd': ooo_mtd,
    'oos_rooms': oos, 'oos_rooms_mtd': oos_mtd,
    'vacant_rooms': vacant, 'vacant_rooms_mtd': vacant_mtd,
    'fb_today': fb_today, 'fb_mtd': fb_mtd,
    'fb_mtd_budget': fb_budget_mtd, 'fb_mtd_ly': fb_ly_mtd,
}

existing = [e for e in entities if e.get('id') == day_id]
if existing:
    node = existing[0]
    node.setdefault('properties', {})
    props = node['properties']
    print(f"\nUpdating: {day_id}")
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
    print(f"\nCreating: {day_id}")

for k, v in data.items():
    if v is not None:
        props[k] = v

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nSaved: {len(entities)} entities")
print("Done!")
