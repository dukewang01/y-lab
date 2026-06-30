#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
fin = json.load(open(fp, 'r', encoding='utf-8'))
es = fin.get('entities', [])
existing_ids = set(e['id'] for e in es)
added = 0

# ====== 1. 月度出口统计（11月各Outlet P&L）=====
# 来源: 第29页餐饮分出口收入表
# 7大出口：OPEN, YUXI, BANQUET, BACIO, ROOM SVC, YUAN, BEER
outlet_stats_11 = [
    ('OPEN', 14326, 1281847, 1173618, 81150, 389000, 33.60, '11月', '2025-11'),
    ('YUXI', 1300, 475234, 389653, 85581, 296000, 33.61, '11月', '2025-11'),
    ('BANQUET', 2734, 1625070, 1124025, 501045, 411000, 28.16, '11月', '2025-11'),
    ('BACIO', 42, 102453, 77606, 24847, 183000, 33.03, '11月', '2025-11'),
    ('ROOM_SVC', 28, 38668, 28969, 9699, 104000, 32.12, '11月', '2025-11'),
    ('YUAN', 376, 117223, 67601, 49622, 182200, 32.04, '11月', '2025-11'),
    ('BEER', 60, 37034, 35930, 1104, 113300, 31.61, '11月', '2025-11'),
]

for outlet, covers, total_rev, food_rev, bev_rev, avg_check, food_cost_pct, period, month_id in outlet_stats_11:
    eid = f'FB_STATS_{outlet}_{month_id.replace("-","_")}'
    if eid not in existing_ids:
        es.append({
            'id': eid, 'type': 'fb_outlet_stats', 'label': f'{outlet} {period}营收统计',
            'outlet': outlet, 'month': month_id, 'period': period,
            'covers': covers, 'total_revenue': total_rev,
            'food_revenue': food_rev, 'beverage_revenue': bev_rev,
            'avg_check': avg_check, 'food_cost_pct': food_cost_pct,
            'source': '业主会议2025.11'
        })
        existing_ids.add(eid); added += 1
        print(f'  + {outlet:>10} | {period} | 人数{covers} | 收入{total_rev/10000:.1f}万')

# ====== 2. 年累计出口食品成本率 ======
food_costs_ytd = [
    ('OPEN', 9094944, 3585119, 39.41),
    ('YUXI', 4385203, 1465912, 33.43),
    ('BANQUET', 10430530, 2968092, 28.46),
    ('BACIO', 552938, 173638, 31.40),
    ('ROOM_SVC', 359277, 115578, 32.17),
    ('YUAN', 688756, 221880, 32.22),
    ('BEER', 193845, 65530, 33.80),
]

for outlet, rev, cost, pct in food_costs_ytd:
    eid = f'FB_COST_{outlet}_2025_YTD'
    if eid not in existing_ids:
        es.append({
            'id': eid, 'type': 'fb_cost', 'label': f'{outlet} 2025年累食品成本率',
            'outlet': outlet, 'food_cost_pct': round(pct,1),
            'food_rev': rev, 'food_cost': cost, 'period': 'YTD_11',
            'source': '业主会议2025.11'
        })
        existing_ids.add(eid); added += 1

# ====== 3. 年累计酒水成本率 ======
bev_costs_ytd = [
    ('OPEN', 256453, 37873, 14.77),
    ('YUXI', 145501, 25662, 17.64),
    ('BANQUET', 440644, 47490, 10.78),
    ('BACIO', 76169, 11934, 15.67),
    ('ROOM_SVC', 49226, 5685, 11.55),
    ('YUAN', 147006, 20264, 13.78),
    ('BEER', 28368, 3050, 10.75),
]

for outlet, rev, cost, pct in bev_costs_ytd:
    eid = f'FB_BEV_{outlet}_2025_YTD'
    if eid not in existing_ids:
        es.append({
            'id': eid, 'type': 'beverage_cost_report', 'label': f'{outlet} 2025年累酒水成本率',
            'outlet': outlet, 'bev_cost_pct': round(pct,1),
            'bev_rev': rev, 'bev_cost': cost, 'period': 'YTD_11',
            'source': '业主会议2025.11'
        })
        existing_ids.add(eid); added += 1

# ====== 4. 更新月度节点：补上各出口年度累计汇总 ======
# 已有FY_2025节点里加FB明细
for e in es:
    if e['id'] == 'FY_2025':
        e['fb_outlets_count'] = 7
        e['fb_banquet_pct'] = '28.5%'
        e['fb_open_pct'] = '39.4%'
        e['fb_yuxi_pct'] = '33.4%'
        break

# ====== 5. Bazaar标签补充 ======
# 从已有数据看，Bazaar节点label全空，需要从id提取
# 但数据量太大(366个)，先放放

# 版本
for v in [e for e in es if e.get('type')=='version' and 'FIN_VER' in e.get('id','')]:
    es.remove(v)
es.append({'id':'FIN_VER_v5_13','type':'version','label':'FIN v5.13 - 补全11月出口统计+年累成本率',
           'total_entities':len(es),'added':added})

fin['entities'] = es
json.dump(fin, open(fp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\n=== 完成! ===')
print(f'FIN: {len(es)} 实体 | v5.13')
print(f'新增: {added} 个')

# 展示补全结果
print('\n11月各出口营收统计:')
print(f'  {"出口":>10} | {"人数":>5} | {"总收入":>8} | {"食品收入":>8} | {"食品成本率":>8}')
print('  ' + '-'*45)
for o, c, tr, fr, br, ac, fcp, p, m in outlet_stats_11:
    print(f'  {o:>10} | {c:>5} | {tr/10000:>6.1f}万 | {fr/10000:>6.1f}万 | {fcp:>7.1f}%')

print('\n出口年度食品成本率排行:')
food_costs_ytd_sorted = sorted(food_costs_ytd, key=lambda x: x[2])
for outlet, rev, cost, pct in food_costs_ytd_sorted:
    bar = '*' * int(pct/2)
    print(f'  {outlet:>10}: {pct:.1f}% | {bar}')

print('\n缺口分析:')
print(f'  Bazaar label待补: 366个')
print(f'  月度出口统计(其他月份): 还有空白')
