#!/usr/bin/env python3
"""Update revenue_data.json and print comparison after 0523+0524 import."""
import json

with open(r'knowledge_center\fin_graph.json', 'r', encoding='utf-8') as f:
    g = json.load(f)

def get_props(eid):
    m = [e for e in g['entities'] if e.get('id') == eid]
    return m[0].get('properties', {}) if m else {}

p23 = get_props('day_2026-05-23')
p24 = get_props('day_2026-05-24')

def pct_of(a, b):
    if a and b and b != 0:
        return round(a / b * 100, 1)
    return None

rev_data = {
    'month': '2026-05',
    'last_updated': '2026-05-26 07:45',
    'last_data_date': '2026-05-24',
    'days_imported': ['2026-05-23', '2026-05-24'],
    'summary': {
        'rooms_sold_mtd': p23.get('room_sold_mtd'),
        'rooms_sold_budget_mtd': p23.get('room_sold_mtd_budget'),
        'rooms_sold_ly_mtd': p23.get('room_sold_mtd_ly'),
        'occ_mtd': p23.get('occ_pct_mtd'),
        'occ_budget_mtd': p23.get('occ_pct_mtd_budget'),
        'occ_ly_mtd': p23.get('occ_pct_mtd_ly'),
        'adr_mtd': p23.get('arr_mtd'),
        'adr_budget_mtd': p23.get('arr_mtd_budget'),
        'adr_ly_mtd': p23.get('arr_mtd_ly'),
        'revpar_mtd': p23.get('revpar_mtd'),
        'revpar_budget_mtd': p23.get('revpar_mtd_budget'),
        'revpar_ly_mtd': p23.get('revpar_mtd_ly'),
        'room_revenue_mtd': p23.get('room_revenue_mtd'),
        'room_revenue_budget_mtd': p23.get('room_revenue_mtd_budget'),
        'room_revenue_ly_mtd': p23.get('room_revenue_mtd_ly'),
        'fb_mtd': p23.get('fb_mtd'),
        'fb_budget_mtd': p23.get('fb_mtd_budget'),
        'fb_ly_mtd': p23.get('fb_mtd_ly'),
    },
    'today_0523': {},
    'today_0524': {},
}

for k in ['room_sold','occ_pct','arr','revpar','room_revenue_total','fb_today','other_income','service_charge']:
    if p23.get(k) is not None:
        rev_data['today_0523'][k] = p23[k]
    if p24.get(k) is not None:
        rev_data['today_0524'][k] = p24[k]

s = rev_data['summary']
s['rooms_budget_pct'] = pct_of(s['room_revenue_mtd'], s['room_revenue_budget_mtd'])
s['fb_budget_pct'] = pct_of(s['fb_mtd'], s['fb_budget_mtd'])
rv = s['room_revenue_mtd']
rl = s['room_revenue_ly_mtd']
s['rooms_yoy_pct'] = round((rv/rl-1)*100,1) if rv and rl else None
fv = s['fb_mtd']
fl = s['fb_ly_mtd']
s['fb_yoy_pct'] = round((fv/fl-1)*100,1) if fv and fl else None

# Save
with open(r'knowledge_center\revenue_data.json', 'w', encoding='utf-8') as f:
    json.dump(rev_data, f, ensure_ascii=False, indent=2)

# Print comparison
print('=' * 60)
print('  May 23 (Sat) vs May 24 (Sun) - Side by Side')
print('=' * 60)

items = [
    ('Room Sold', 'room_sold', '{:.0f}'),
    ('Occupancy', 'occ_pct', '{:.1f}%'),
    ('ADR', 'arr', '{:.0f}'),
    ('RevPAR', 'revpar', '{:.1f}'),
    ('Room Revenue', 'room_revenue_total', '{:,.0f}'),
    ('FB Revenue', 'fb_today', '{:,.0f}'),
    ('Other Income', 'other_income', '{:,.0f}'),
    ('Service Charge', 'service_charge', '{:,.0f}'),
]
print(f'  {"Metric":<16} {"May 23":>12} {"May 24":>12}')
print(f'  {"-" * 40}')
for name, key, fmt in items:
    v23 = p23.get(key)
    v24 = p24.get(key)
    s23 = fmt.format(v23) if v23 is not None else 'N/A'
    s24 = fmt.format(v24) if v24 is not None else 'N/A'
    print(f'  {name:<16} {s23:>12} {s24:>12}')

print()
print('MTD Summary (as of May 23):')
print(f'  Room Rev: {s["room_revenue_mtd"]:,.0f}  (budget: {s["rooms_budget_pct"]}%)')
print(f'  FB Rev:   {s["fb_mtd"]:,.0f}  (budget: {s["fb_budget_pct"]}%)')
rv = s['room_revenue_mtd']
rl = s['room_revenue_ly_mtd']
fy = s['fb_yoy_pct']
print(f'  Occ: {s["occ_mtd"]}%  ADR: {s["adr_mtd"]:,.0f}  RevPAR: {s["revpar_mtd"]:,.0f}')
print(f'  Room YoY: {s["rooms_yoy_pct"]}%  FB YoY: {fy or "N/A"}%')
print()
print('Saved: revenue_data.json')
