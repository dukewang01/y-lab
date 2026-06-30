#!/usr/bin/env python3
"""Script: parse all 0522-0524 DRR Excel data and import into FIN graph."""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0522_0523_0524_batch.json'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

def parse_drr_xlsx(path, date_str):
    """Parse a standardized DRR Excel file and return data dict."""
    wb = openpyxl.load_workbook(path, data_only=True)
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
    
    data['_date'] = date_str
    
    return data

# Files
files = {
    '2026-05-22': r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.22---c1942bf4-38d2-416c-91e7-a6f74df61692.xlsx',
    '2026-05-23': r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.23---0ca44fc7-f465-4421-aff4-19d6f6aa52cd.xlsx',
    '2026-05-24': r'C:\Users\Duke Wang\.openclaw\media\inbound\Daily_Revenue_Report_2026.05.24---2a42d27f-afab-414f-b4a2-22ab7f5b111e.xlsx',
}

all_data = {}
for date_str, path in files.items():
    d = parse_drr_xlsx(path, date_str)
    all_data[date_str] = d
    print(f"Parsed {date_str}: rooms={d.get('room_sold')}, occ={d.get('occ_pct')}%, adr={d.get('arr')}, room_rev={d.get('room_revenue_total'):,.0f}, fb={d.get('fb_today'):,.0f}")

# Import to graph
for date_str, data in all_data.items():
    day_id = f'day_{date_str}'
    existing = [e for e in entities if e.get('id') == day_id]
    if existing:
        node = existing[0]
        node.setdefault('properties', {})
        props = node['properties']
        print(f"  Update: {day_id}")
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
        print(f"  Create: {day_id}")
    
    for k, v in data.items():
        if k.startswith('_'):
            continue
        if v is not None:
            props[k] = v

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nSaved: {len(entities)} entities")

# Print weekend summary
print("\n" + "=" * 60)
print("  2026年5月 周末复盘: 5.22(周五) - 5.24(周日)")
print("=" * 60)

headers = ['指标', 'Fri 5/22', 'Sat 5/23', 'Sun 5/24', '周末合计']
rows_data = [
    ('已售房',      'room_sold',              '{:.0f}'),
    ('出租率',      'occ_pct',                '{:.1f}%'),
    ('ADR',        'arr',                    '{:.0f}'),
    ('RevPAR',     'revpar',                 '{:.1f}'),
    ('客房收入',    'room_revenue_total',     '{:,.0f}'),
    ('餐饮收入',    'fb_today',               '{:,.0f}'),
    ('其他收入',    'other_income',           '{:,.0f}'),
    ('服务费',      'service_charge',         '{:,.0f}'),
]
print(f'  {"指标":<10} {"周五":>10} {"周六":>10} {"周日":>10} {"合计趋势":>10}')
print(f'  {"-"*50}')
summaries = {}
for name, key, fmt in rows_data:
    vals = [all_data[d].get(key) for d in ['2026-05-22','2026-05-23','2026-05-24']]
    strs = []
    for v in vals:
        strs.append(fmt.format(v) if v is not None else 'N/A')
    # Sum for revenue fields
    if 'revenue' in key or 'income' in key or 'charge' in key:
        total = sum(v for v in vals if v is not None)
        trend = '↑' if vals[0] and vals[2] and total > vals[0]*2 else ('↓' if vals[0] and vals[2] and total < vals[0]*1.5 else '→')
        strs.append(f'{total:,.0f} {trend}')
    elif 'sold' in key:
        total = sum(v for v in vals if v is not None)
        strs.append(f'{total:.0f}')
    else:
        strs.append('')
    print(f'  {name:<10} {strs[0]:>10} {strs[1]:>10} {strs[2]:>10} {strs[3] if len(strs)>3 else "":>10}')

print("\nMTD综合(至5月24日):")
d24 = all_data['2026-05-24']
print(f"  出租率: {d24.get('occ_pct_mtd')}%  (预算: {d24.get('occ_pct_mtd_budget')}%)")
print(f"  ADR: {d24.get('arr_mtd'):,.0f}  (预算: {d24.get('arr_mtd_budget'):,.0f})")
print(f"  RevPAR: {d24.get('revpar_mtd'):,.0f}  (预算: {d24.get('revpar_mtd_budget'):,.0f})")
print(f"  已售房累计: {d24.get('room_sold_mtd'):.0f}  (预算: {d24.get('room_sold_mtd_budget'):,.0f})")
print(f"  客房收入: {d24.get('room_revenue_mtd'):,.0f}  (预算: {d24.get('room_revenue_mtd_budget'):,.0f})")
print(f"  餐饮收入: {d24.get('fb_mtd'):,.0f}  (预算: {d24.get('fb_mtd_budget'):,.0f})")

# Budget pct
rr = d24.get('room_revenue_mtd')
rb = d24.get('room_revenue_mtd_budget')
fr = d24.get('fb_mtd')
fb = d24.get('fb_mtd_budget')
rrp = round(rr/rb*100,1) if rr and rb else 0
frp = round(fr/fb*100,1) if fr and fb else 0
print(f"  客房预算达成: {rrp}%")
print(f"  餐饮预算达成: {frp}%")
