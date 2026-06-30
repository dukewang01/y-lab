#!/usr/bin/env python3
"""Import 2026-05-25 DRR Excel into FIN graph, compare with HF forecast."""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0525_drr.json'
XLSX_PATH = r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.25---8c022a37-9e04-42dc-afdc-afa064a8de41.xlsx'

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

# Col mapping: D(5)=Today, E(6)=Daily Budget, F(7)=LY Daily, G(8)=MTD, H(9)=MTD Budget, I(10)=MTD LY
r_sold = n(15, 5)
r_sold_mtd = n(15, 8)
r_sold_budget_mtd = n(15, 9)
r_sold_ly_mtd = n(15, 10)

occ_today = pct_col(22, 5)
occ_mtd = pct_col(22, 8)
occ_budget_mtd = pct_col(22, 9)
occ_ly_mtd = pct_col(22, 10)

revpar_today = n(23, 5)
revpar_mtd = n(23, 8)
revpar_budget_mtd = n(23, 9)
revpar_ly_mtd = n(23, 10)

adr_today = n(24, 5)
adr_mtd = n(24, 8)
adr_budget_mtd = n(24, 9)
adr_ly_mtd = n(24, 10)

room_rev_today = n(26, 5)
room_rev_mtd = n(26, 8)
room_rev_budget_mtd = n(26, 9)
room_rev_ly_mtd = n(26, 10)

other_inc_today = n(27, 5)
other_inc_mtd = n(27, 8)
sc_today = n(28, 5)
sc_mtd = n(28, 8)
net_room_today = n(29, 5)
net_room_mtd = n(29, 8)

comp = n(16, 5); comp_mtd = n(16, 8)
hu = n(17, 5); hu_mtd = n(17, 8)
ooo = n(18, 5); ooo_mtd = n(18, 8)
oos = n(19, 5); oos_mtd = n(19, 8)
vacant = n(20, 5); vacant_mtd = n(20, 8)
avail = n(21, 5)

ws_fb = wb['F&B']
fb_today = ws_fb.cell(20, 2).value
fb_mtd = ws_fb.cell(20, 7).value
fb_budget_mtd = ws_fb.cell(20, 10).value
fb_ly_mtd = ws_fb.cell(20, 8).value

print("=== 2026-05-25 (Mon) DRR ===")
print(f"Rooms: Today={r_sold}, MTD={r_sold_mtd}")
print(f"Occ: {occ_today}% (MTD: {occ_mtd}%)")
print(f"ADR: {adr_today} (MTD: {adr_mtd})")
print(f"RevPAR: {revpar_today} (MTD: {revpar_mtd})")
print(f"Room Rev: {room_rev_today:,.0f} (MTD: {room_rev_mtd:,.0f})")
print(f"FB Rev: {fb_today:,.0f} (MTD: {fb_mtd:,.0f})")
print(f"Comp={comp}, HU={hu}, OOO={ooo}, OOS={oos}")

date_str = '2026-05-25'
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
    'comp_rooms': comp, 'comp_rooms_mtd': comp_mtd,
    'house_use': hu, 'house_use_mtd': hu_mtd,
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

# Compare DRR vs HF for 0525
n = [e for e in entities if e.get('id') == f'day_{date_str}']
if n:
    p = n[0].get('properties', {})
    print("\n=== HF Forecast vs DRR Actual (0525) ===")
    print(f'  {"Metric":<15} {"HF Forecast":>12} {"DRR Actual":>12} {"Diff":>10}')
    print(f'  {"-"*49}')
    fields = [('Room Sold', 'total_occ_hf', 'room_sold', '{:.0f}', '{:.0f}'),
              ('Occupancy', 'occ_pct_hf', 'occ_pct', '{:.1f}%', '{:.1f}%'),
              ('Avg Rate', 'avg_rate_hf', 'arr', '{:.0f}', '{:.0f}'),
              ('Room Rev', 'room_revenue_hf', 'room_revenue_total', '{:,.0f}', '{:,.0f}')]
    for name, hf_key, drr_key, hf_fmt, drr_fmt in fields:
        hf_v = p.get(hf_key)
        drr_v = p.get(drr_key)
        if hf_v is not None and drr_v is not None:
            diff = drr_v - hf_v
            print(f'  {name:<15} {hf_fmt.format(hf_v):>12} {drr_fmt.format(drr_v):>12} {diff:>+10.1f}')
        else:
            print(f'  {name:<15} {"N/A":>12} {"N/A":>12} {"":>10}')

# HF Total Occ vs DRR RoomSold
hf_total_occ = p.get('total_occ_hf')
drr_sold = p.get('room_sold')
if hf_total_occ and drr_sold:
    print(f'  {"Total Occ->Sold":<15} {hf_total_occ:>12.0f} {drr_sold:>12.0f} Diff(comp+hu): {hf_total_occ - drr_sold:+.0f}')
    print(f'  {"Comp (HF)":<15} {p.get("comp_rooms_hf","N/A"):>12} {comp:>12}')
    print(f'  {"House Use (HF)":<15} {p.get("house_use_hf","N/A"):>12} {hu:>12}')
