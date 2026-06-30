#!/usr/bin/env python3
"""Deep dive: Compare Suzhou market vs peers, and our HH Suzhou vs peer HH hotels."""
import json, openpyxl

path = r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\GCM_YTD.xlsx'
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb['Export']

# Collect market totals
markets = {}
hotels = {}
current_market = None
for r in range(2, ws.max_row + 1):
    c1 = ws.cell(r, 1).value; c2 = ws.cell(r, 2).value
    c3 = ws.cell(r, 3).value; c4 = ws.cell(r, 4).value
    c5 = ws.cell(r, 5).value; c6 = ws.cell(r, 6).value; c7 = ws.cell(r, 7).value
    if c1 is not None and c2 == 'Total' and c3 is not None:
        current_market = str(c1)
        markets[current_market] = {
            'adr': float(c3), 'rev': float(c4), 'revpar': float(c5),
            'rns': int(c6), 'occ': float(c7)*100
        }
        hotels[current_market] = []
    elif current_market and c2 is not None and c3 is not None:
        hotels.setdefault(current_market, []).append({
            'name': str(c2), 'adr': float(c3), 'rev': float(c4),
            'revpar': float(c5), 'rns': int(c6), 'occ': float(c7)*100
        })

# 1. Peer cities — similar scale to Suzhou
print("=" * 80)
print("  【苏州 vs 可比城市】")
print("=" * 80)
peers = ['Jiangsu/Suzhou', 'Jiangsu/Nanjing', 'Zhejiang/Hangzhou', 
         'Fujian/Xiamen', 'Sichuan/Chengdu', 'Chongqing', 'Tianjin',
         'Hubei/Wuhan', 'Shaanxi/Xi\'an', 'Hunan/Changsha']
print(f"{'城市':<22} {'ADR':>8} {'Rev(万)':>10} {'RevPAR':>8} {'RNs':>8} {'Occ':>7} {'ADR溢价':>8}")
print("-" * 72)
sz_adr = markets['Jiangsu/Suzhou']['adr']
for city in peers:
    if city in markets:
        m = markets[city]
        premium = (m['adr'] - sz_adr) / sz_adr * 100
        flag = " <<< 苏州" if 'Suzhou' in city else ""
        print(f"{city:<22} {m['adr']:>8.0f} {m['rev']/1e4:>10.1f} {m['revpar']:>8.0f} {m['rns']:>8d} {m['occ']:>6.1f}% {premium:>+7.1f}%{flag}")

# 2. Our hotel vs peer HH hotels in similar cities
print()
print("=" * 80)
print("  【苏州希尔顿 vs 全国可比HH酒店】")
print("=" * 80)
# Collect all HH hotels
hh_hotels = []
for mkt, hlist in hotels.items():
    for h in hlist:
        if h['name'].startswith('HH ') and not any(x in h['name'] for x in ['Garden', 'Yinshan', 'New District', 'Wuzhong']):
            hh_hotels.append({'market': mkt, **h})

hh_hotels.sort(key=lambda x: x['rev'], reverse=True)

# Find our hotel
our = None
for h in hh_hotels:
    if 'HH Suzhou' in h['name'] and 'New' not in h['name'] and 'Yinshan' not in h['name'] and 'Wuzhong' not in h['name']:
        our = h
        break

print(f"{'排名':>3} {'酒店':<40} {'所在市场':<18} {'ADR':>8} {'Rev(万)':>10} {'RevPAR':>8} {'RNs':>7} {'Occ':>7}")
print("-" * 100)
for i, h in enumerate(hh_hotels[:20], 1):
    flag = " <<<" if h == our else ""
    mkt_short = h['market'].split('/')[-1] if '/' in h['market'] else h['market']
    print(f"{i:>3} {h['name']:<40} {mkt_short:<18} {h['adr']:>8.0f} {h['rev']/1e4:>10.1f} {h['revpar']:>8.0f} {h['rns']:>7d} {h['occ']:>6.1f}%{flag}")

# Save to report
lines = []
lines.append("=" * 80)
lines.append("  【苏州 vs 可比城市】")
lines.append("=" * 80)
lines.append(f"{'城市':<22} {'ADR':>8} {'Rev(万)':>10} {'RevPAR':>8} {'RNs':>8} {'Occ':>7} {'ADR溢价':>8}")
lines.append("-" * 72)
for city in peers:
    if city in markets:
        m = markets[city]
        premium = (m['adr'] - sz_adr) / sz_adr * 100
        flag = " <<< 苏州" if 'Suzhou' in city else ""
        lines.append(f"{city:<22} {m['adr']:>8.0f} {m['rev']/1e4:>10.1f} {m['revpar']:>8.0f} {m['rns']:>8d} {m['occ']:>6.1f}% {premium:>+7.1f}%{flag}")

lines.append("")
lines.append("=" * 80)
lines.append("  【苏州希尔顿 vs 全国可比HH酒店 Top20】")
lines.append("=" * 80)
lines.append(f"{'排名':>3} {'酒店':<40} {'所在市场':<18} {'ADR':>8} {'Rev(万)':>10} {'RevPAR':>8} {'RNs':>7} {'Occ':>7}")
lines.append("-" * 100)
for i, h in enumerate(hh_hotels[:20], 1):
    flag = " <<<" if h == our else ""
    mkt_short = h['market'].split('/')[-1] if '/' in h['market'] else h['market']
    lines.append(f"{i:>3} {h['name']:<40} {mkt_short:<18} {h['adr']:>8.0f} {h['rev']/1e4:>10.1f} {h['revpar']:>8.0f} {h['rns']:>7d} {h['occ']:>6.1f}%{flag}")

outpath = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\gcm_ytd_analysis2.md'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"\nReport saved: {outpath}")
print('\n'.join(lines[-30:]))  # Show HH ranking tail
