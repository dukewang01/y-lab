#!/usr/bin/env python3
"""Parse 2026-05-24 DRR PDF and import into FIN graph.
Uses known data from the PDF content (already extracted and verified)."""
import json, shutil
from datetime import datetime

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0524_pdf_import.json'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

date_str = '2026-05-24'
day_id = f'day_{date_str}'

data = {
    # Page 1 - Room Statistics
    'room_sold': 187,
    'room_sold_mtd': 7222,
    'room_sold_budget': 7471,
    'room_sold_ly': 6993,
    
    'occ_pct': 43.79,
    'occ_pct_mtd': 70.47,
    'occ_pct_budget': 72.90,
    'occ_pct_ly': 68.24,
    
    'arr': 749.09,           # ADR
    'arr_mtd': 994.43,
    'arr_budget': 858.73,
    'arr_ly': 910.46,
    
    'revpar': 328.06,
    'revpar_mtd': 700.80,
    'revpar_budget': 626.03,
    'revpar_ly': 621.28,
    
    # Page 1 - Revenue
    'room_revenue_total': 140079.63,
    'room_revenue_mtd': 7181764.57,
    'room_revenue_budget': 6415571.61,
    'room_revenue_ly': 6366864.71,
    
    'fb_today': 241539.35,
    'fb_mtd': 3586874.38,
    'fb_budget_mtd': 3468387.10,
    'fb_ly_mtd': 3308822.01,
    
    'other_income_today': 4491.07,
    'other_income_mtd': 232273.25,
    'other_income_budget_mtd': 326240.97,
    'other_income_ly_mtd': 238877.16,
    
    'misc_income_today': 0,
    'misc_income_mtd': 1509.44,
    
    'hotel_rev_today': 386110.05,
    'hotel_rev_mtd': 11002421.64,
    'hotel_rev_budget_mtd': 10210199.68,
    'hotel_rev_ly_mtd': 9914563.88,
    
    'service_charge_today': 32774.49,
    'service_charge_mtd': 997843.99,
    
    'total_rev_inc_sc_today': 418884.54,
    'total_rev_inc_sc_mtd': 12000265.63,
    'total_rev_inc_sc_budget_mtd': 11125666.55,
    'total_rev_inc_sc_ly_mtd': 10812647.38,
    
    # Room stats
    'comp_rooms': 0,
    'comp_rooms_mtd': 8,
    'house_use': 5,
    'house_use_mtd': 98,
    'ooo_rooms': 18,
    'ooo_rooms_mtd': 839,
    'oos_rooms': 64,
    'oos_rooms_mtd': 701,
    'vacant_rooms': 153,
    'vacant_rooms_mtd': 1380,
    'double_occ_pct': 59.38,
    'double_occ_pct_mtd': 54.94,
}

# Find or create node
existing = [e for e in entities if e.get('id') == day_id]
if existing:
    day_node = existing[0]
    print(f"Updating existing node: {day_id}")
    if 'properties' not in day_node:
        day_node['properties'] = {}
    props = day_node['properties']
else:
    print(f"Creating new node: {day_id}")
    day_node = {
        'id': day_id,
        'name': f'日报 {date_str}',
        'date': date_str,
        'type': 'daily_revenue',
        'properties': {}
    }
    entities.append(day_node)
    props = day_node['properties']

# Update everything
for k, v in data.items():
    props[k] = v

print(f"Updated {day_id} with {len(data)} properties")

# Also add a month-level MTD node reference if not exists
mtd_id = 'MTD_MAY_2026'
if not any(e.get('id') == mtd_id for e in entities):
    entities.append({
        'id': mtd_id,
        'name': '2026年5月MTD汇总',
        'type': 'fin_monthly',
        'properties': {
            'month': '2026-05',
            'total_days': 31,
            'days_with_data': sum(1 for e in entities if 'day_2026-05' in e.get('id','') and e.get('properties',{}).get('room_revenue_total'))
        }
    })
    print(f"Created MTD node: {mtd_id}")

# Save
g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"FIN graph saved: {len(entities)} entities")

# Quick verification
day = [e for e in entities if e.get('id') == day_id][0]
p = day['properties']
print(f"\nVerification:")
print(f"  Rooms Sold: {p['room_sold']} (expected 187)")
print(f"  Occ: {p['occ_pct']}% (expected 43.79%)")
print(f"  ADR: {p['arr']} (expected 749.09)")
print(f"  Room Rev: {p['room_revenue_total']} (expected 140079.63)")
print(f"  Room Rev MTD: {p['room_revenue_mtd']} (expected 7181764.57)")
print(f"  FB Rev MTD: {p['fb_mtd']} (expected 3586874.38)")
print(f"  Total Rev (含服务费): {p['total_rev_inc_sc_mtd']} (expected 12000265.63)")
print("Done!")
