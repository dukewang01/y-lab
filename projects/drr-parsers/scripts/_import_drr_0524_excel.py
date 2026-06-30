#!/usr/bin/env python3
"""Import 2026-05-24 DRR Excel into FIN graph (replace PDF-derived data).
Actual sheet: C(4)=label, D(5)=Today, E(6)=Daily Budget, F(7)=LY Daily, 
G(8)=MTD, H(9)=MTD Budget, I(10)=MTD LY"""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0524_excel_import.json'
XLSX_PATH = r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.24---2a42d27f-afab-414f-b4a2-22ab7f5b111e.xlsx'

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

# R15: Rooms Sold
r_sold = n(15, 5)        # 300
r_sold_mtd = n(15, 8)    # 9005
r_sold_budget_mtd = n(15, 9)  # 11187
r_sold_ly_mtd = n(15, 10)     # 9379

# R22: Occ%
occ_today = pct_col(22, 5)   # 55.76%
occ_mtd = pct_col(22, 8)     # 69.74%
occ_budget_mtd = pct_col(22, 9)  # 86.64%
occ_ly_mtd = pct_col(22, 10)     # 72.64%

# R23: RevPAR
revpar_today = n(23, 5)      # 329.03
revpar_mtd = n(23, 8)        # 507.83
revpar_budget_mtd = n(23, 9)  # 569.37
revpar_ly_mtd = n(23, 10)     # 503.12

# R24: ADR
adr_today = n(24, 5)        # 590.06
adr_mtd = n(24, 8)          # 728.17
adr_budget_mtd = n(24, 9)   # 657.16
adr_ly_mtd = n(24, 10)      # 692.64

# R26: Room Revenue
room_rev_today = n(26, 5)     # 158491.08
room_rev_mtd = n(26, 8)       # 5895369.00
room_rev_budget_mtd = n(26, 9)  # 6683380.65
room_rev_ly_mtd = n(26, 10)     # 5859388.86

# R27: Other Income
other_inc_today = n(27, 5)   # 2434.98
other_inc_mtd = n(27, 8)     # 65671.86

# R28: Service Charge
sc_today = n(28, 5)          # 16092.63
sc_mtd = n(28, 8)            # 596113.81

# R29: Net Room Revenue
net_room_today = n(29, 5)    # 177018.69
net_room_mtd = n(29, 8)      # 6557154.67

# R16-21: Room stats
comp_rooms = n(16, 5)        # 6
comp_mtd = n(16, 8)          # 41
house_use = n(17, 5)         # 2
house_mtd = n(17, 8)         # 52
ooo = n(18, 5)               # 3
ooo_mtd = n(18, 8)           # 98
oos = n(19, 5)               # 47
oos_mtd = n(19, 8)           # 110
vacant = n(20, 5)            # 180
vacant_mtd = n(20, 8)        # 3606
available = n(21, 5)         # 538
guest_count = n(25, 5)

# F&B sheet
ws_fb = wb['F&B']
# Row 20: TOTAL F&B
fb_today = ws_fb.cell(20, 2).value
fb_mtd = ws_fb.cell(20, 7).value
fb_ly_mtd = ws_fb.cell(20, 8).value
fb_budget_mtd = ws_fb.cell(20, 10).value

# Outlet breakdown
outlets = {}
for fb_row in [11, 12, 13, 14, 15, 16, 17, 18]:
    name = str(ws_fb.cell(fb_row, 1).value or '').split()[0] if ws_fb.cell(fb_row, 1).value else ''
    if name:
        outlets[name] = {
            'today_rev': ws_fb.cell(fb_row, 2).value,
            'today_covers': ws_fb.cell(fb_row, 3).value,
            'today_avg': ws_fb.cell(fb_row, 4).value,
            'mtd_covers': ws_fb.cell(fb_row, 6).value,
            'mtd_rev': ws_fb.cell(fb_row, 7).value,
        }

print("=== Parsed 2026-05-24 (Excel) ===")
print(f"Rooms: Today={r_sold}, MTD={r_sold_mtd}, MTD Budget={r_sold_budget_mtd}, MTD LY={r_sold_ly_mtd}")
print(f"Occupancy: Today={occ_today}%, MTD={occ_mtd}%, MTD Budget={occ_budget_mtd}%, MTD LY={occ_ly_mtd}%")
print(f"ADR: Today={adr_today}, MTD={adr_mtd}, MTD Budget={adr_budget_mtd}, MTD LY={adr_ly_mtd}")
print(f"RevPAR: Today={revpar_today}, MTD={revpar_mtd}, MTD Budget={revpar_budget_mtd}, MTD LY={revpar_ly_mtd}")
print(f"Room Rev: Today={room_rev_today}, MTD={room_rev_mtd}, MTD Budget={room_rev_budget_mtd}, MTD LY={room_rev_ly_mtd}")
print(f"FB Rev: Today={fb_today}, MTD={fb_mtd}")
print(f"Net Room: Today={net_room_today}, MTD={net_room_mtd}")

date_str = '2026-05-24'
day_id = f'day_{date_str}'

data = {
    'room_sold': r_sold, 'room_sold_mtd': r_sold_mtd,
    'room_sold_mtd_budget': r_sold_budget_mtd, 'room_sold_mtd_ly': r_sold_ly_mtd,
    'occ_pct': occ_today, 'occ_pct_mtd': occ_mtd,
    'occ_pct_mtd_budget': occ_budget_mtd, 'occ_pct_mtd_ly': occ_ly_mtd,
    'arr': adr_today, 'arr_mtd': adr_mtd,
    'arr_mtd_budget': adr_budget_mtd, 'arr_mtd_ly': adr_ly_mtd,
    'revpar': revpar_today, 'revpar_mtd': revpar_mtd,
    'revpar_mtd_budget': revpar_budget_mtd, 'revpar_mtd_ly': revpar_ly_mtd,
    'room_revenue_total': room_rev_today, 'room_revenue_mtd': room_rev_mtd,
    'room_revenue_mtd_budget': room_rev_budget_mtd, 'room_revenue_mtd_ly': room_rev_ly_mtd,
    'other_income': other_inc_today, 'other_income_mtd': other_inc_mtd,
    'service_charge': sc_today, 'service_charge_mtd': sc_mtd,
    'net_room_revenue': net_room_today, 'net_room_revenue_mtd': net_room_mtd,
    'comp_rooms': comp_rooms, 'comp_rooms_mtd': comp_mtd,
    'house_use': house_use, 'house_use_mtd': house_mtd,
    'ooo_rooms': ooo, 'ooo_rooms_mtd': ooo_mtd,
    'oos_rooms': oos, 'oos_rooms_mtd': oos_mtd,
    'vacant_rooms': vacant, 'vacant_rooms_mtd': vacant_mtd,
    'available_rooms': available,
    'guest_count': guest_count,
    'fb_today': fb_today, 'fb_mtd': fb_mtd,
    'fb_mtd_budget': fb_budget_mtd, 'fb_mtd_ly': fb_ly_mtd,
}

# Also calculate derived totals
if fb_today and room_rev_today:
    data['hotel_rev_today'] = round(room_rev_today + other_inc_today + fb_today, 2)
if fb_mtd and room_rev_mtd:
    total = round(room_rev_mtd + (other_inc_mtd or 0) + fb_mtd, 2)
    data['hotel_rev_mtd'] = total

# Update graph
existing = [e for e in entities if e.get('id') == day_id]
if existing:
    node = existing[0]
    node.setdefault('properties', {})
    props = node['properties']
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

for k, v in data.items():
    if v is not None:
        props[k] = v

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nSaved: {len(entities)} entities")
print("Done!")
