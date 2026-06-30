#!/usr/bin/env python3
"""Query FIN graph for June+May daily data and analyze Occ patterns."""
import json
from datetime import datetime, date, timedelta

with open(r'C:\Users\Y\.openclaw\workspace\knowledge_center\fin_graph.json', 'r', encoding='utf-8') as f:
    g = json.load(f)

# Collect all daily revenue nodes
days = [e for e in g['entities'] if e.get('type') == 'daily_revenue' and e.get('date')]

# Sort by date
days.sort(key=lambda x: x.get('date',''))

# Get day of week
def dow(d):
    return datetime.strptime(d, '%Y-%m-%d').weekday()

DOW_NAMES = ['周一','周二','周三','周四','周五','周六','周日']

print("=" * 80)
print("  FIN图每日数�?�?周度Occ/ADR结构分析")
print("=" * 80)

# Group by week
weeks = {}
for d in days:
    dt = datetime.strptime(d['date'], '%Y-%m-%d')
    week_start = (dt - timedelta(days=dt.weekday())).strftime('%Y-%m-%d')
    weeks.setdefault(week_start, []).append(d)

# Show last 4 weeks
sorted_weeks = sorted(weeks.keys())
print(f"\n最�?周数�?({sorted_weeks[-4:]})")

for ws in sorted_weeks[-4:]:
    wd = weeks[ws]
    print(f"\n--- 周开�? {ws} ---")
    print(f"{'日期':<12} {'星期':>4} {'Sold':>6} {'Occ%':>7} {'ADR':>7} {'Rev':>10} {'vs同年':>7} {'vs前日':>7}")
    print("-" * 62)
    for d in wd:
        p = d.get('properties', {})
        s = p.get('room_sold', 0)
        o = p.get('occ_pct')
        a = p.get('arr')
        r = p.get('room_revenue_total')
        dow_name = DOW_NAMES[dow(d['date'])]
        print(f"{d['date']:<12} {dow_name:>4} {s:>6.0f} {o or 0:>6.1f}% {a or 0:>7.0f} {r or 0:>10,.0f}")

# Analyze: last 7 days pattern
print("\n")
print("=" * 80)
print("  最�?�?+ 季节性对�?)
print("=" * 80)

# Get last 7 days with data (2026)
recent = [d for d in days if d['date'] >= '2026-05-28']

# Try to get LY data
ly_days = [d for d in days if d['date'].startswith('2025-06')]
ly_june = {}
for d in ly_days:
    day_num = int(d['date'].split('-')[2])
    ly_june[day_num] = d

print(f"\n{'日期':<12} {'星期':>4} {'Sold':>6} {'Occ%':>7} {'ADR':>7} {'Rev':>10} {'LY Occ':>8} {'LY ADR':>8}")
print("-" * 70)
for d in recent[-7:]:
    p = d.get('properties', {})
    s = p.get('room_sold', 0)
    o = p.get('occ_pct')
    a = p.get('arr')
    r = p.get('room_revenue_total')
    dow_name = DOW_NAMES[dow(d['date'])]
    
    # Last year same weekday comparison (more meaningful)
    # Get LY day of same date
    ly_occ = 'N/A'
    ly_adr = 'N/A'
    for ld in ly_days:
        ld_dow = dow(ld['date'])
        if ld_dow == dow(d['date']) and ld['date'][:7] == '2025-06':
            lp = ld.get('properties', {})
            ly_occ = f"{lp.get('occ_pct', 0):.1f}%"
            ly_adr = f"{lp.get('arr', 0):.0f}"
            break
    
    print(f"{d['date']:<12} {dow_name:>4} {s:>6.0f} {o or 0:>6.1f}% {a or 0:>7.0f} {r or 0:>10,.0f} {ly_occ:>8} {ly_adr:>8}")

# Check: do we have 2025 LY data at all?
print(f"\n\nLY数据状�? 2025-06 �?{len(ly_days)} 条记�?)
for d in sorted(ly_days, key=lambda x: x['date'])[:5]:
    p = d.get('properties', {})
    print(f"  {d['date']}: Occ={p.get('occ_pct')}% ADR={p.get('arr')}")

# Check available dates span
dates = [d['date'] for d in days]
print(f"\n数据时间范围: {min(dates)} �?{max(dates)}")
print(f"总天�? {len(dates)}")

# Weekday breakdown for June (so far)
june_days_2026 = [d for d in days if d['date'].startswith('2026-06')]
print(f"\n6月每日明�?")
for d in sorted(june_days_2026, key=lambda x: x['date']):
    p = d.get('properties', {})
    dn = DOW_NAMES[dow(d['date'])]
    print(f"  {d['date']} {dn}: Sold={p.get('room_sold')}, Occ={p.get('occ_pct')}%, ADR={p.get('arr')}, Rev={p.get('room_revenue_total')}, Comp={p.get('comp_rooms')}, HU={p.get('house_use')}")
