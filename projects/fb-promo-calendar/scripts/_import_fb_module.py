#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
fin = json.load(open(fp, 'r', encoding='utf-8'))
es = fin.get('entities', [])
existing_ids = set(e['id'] for e in es)

# FB月度数据（1-5月从全年推算，6-12月来自业主会议P&L）
fb_data = [
    ('MONTH_2025_01', 2694793, 610000, 22.64),
    ('MONTH_2025_02', 2496976, 580000, 23.23),
    ('MONTH_2025_03', 2945341, 720000, 24.45),
    ('MONTH_2025_04', 2610200, 670000, 25.67),
    ('MONTH_2025_05', 2411235, 600000, 24.88),
    ('MONTH_2025_06', 2223754, 380544, 17.11),
    ('MONTH_2025_07', 2307815, 448837, 19.45),
    ('MONTH_2025_08', 3341204, 1003106, 30.02),
    ('MONTH_2025_09', 2218606, 523647, 23.60),
    ('MONTH_2025_10', 4604252, 1659813, 36.05),
    ('MONTH_2025_11', 3677528, 1408384, 38.30),
    ('MONTH_2025_12', 3126446, 910653, 29.13),
]

for mid, rev, profit, margin in fb_data:
    for e in es:
        if e['id'] == mid:
            e['fb_rev'] = rev
            e['fb_profit'] = profit
            e['fb_margin'] = margin
            break

fb_total_rev = sum(d[1] for d in fb_data)
fb_total_profit = sum(d[2] for d in fb_data)
print('FB 1-12月入库完成')
print('  FB总收入: ' + str(fb_total_rev) + ' (参考: 36,053,887)')
print('  FB总利润: ' + str(fb_total_profit))
print('  FB利润率: ' + '{:.1f}%'.format(fb_total_profit/fb_total_rev*100))

# 全年FB汇总到FY_2025
for e in es:
    if e['id'] == 'FY_2025':
        e['fb_revenue_annual'] = fb_total_rev
        e['fb_profit_annual'] = fb_total_profit
        e['fb_margin_annual'] = fb_total_profit/fb_total_rev*100
        break

# 11月出口食品成本率
food_costs = [
    ('FB_COST_OPEN_2025_11', 'OPEN 11月食品成本率', 'OPEN', 39.0, 1173618, 457715),
    ('FB_COST_YUXI_2025_11', 'YUXI 11月食品成本率', 'YUXI', 33.6, 389653, 130147),
    ('FB_COST_BANQUET_2025_11', 'BANQUET 11月食品成本率', 'BANQUET', 28.2, 1124025, 316475),
    ('FB_COST_BACIO_2025_11', 'BACIO 11月食品成本率', 'BACIO', 33.0, 77606, 24545),
    ('FB_COST_ROOMSVC_2025_11', 'ROOM SVC 11月食品成本率', 'ROOM_SVC', 32.1, 28969, 9296),
    ('FB_COST_YUAN_2025_11', 'YUAN 11月食品成本率', 'YUAN', 32.0, 67601, 21642),
    ('FB_COST_BEER_2025_11', 'BEER 11月食品成本率', 'BEER', 31.6, 35930, 11357),
]
# 11月出口酒水成本率
bev_costs = [
    ('FB_BEV_OPEN_2025_11', 'OPEN 11月酒水成本率', 'OPEN', 17.4, 45657, 7920),
    ('FB_BEV_YUXI_2025_11', 'YUXI 11月酒水成本率', 'YUXI', 12.4, 11118, 1381),
    ('FB_BEV_BANQUET_2025_11', 'BANQUET 11月酒水成本率', 'BANQUET', 12.1, 36115, 4363),
    ('FB_BEV_BACIO_2025_11', 'BACIO 11月酒水成本率', 'BACIO', 15.8, 17514, 2768),
    ('FB_BEV_ROOMSVC_2025_11', 'ROOM SVC 11月酒水成本率', 'ROOM_SVC', 10.1, 4673, 471),
    ('FB_BEV_YUAN_2025_11', 'YUAN 11月酒水成本率', 'YUAN', 12.3, 19866, 2433),
    ('FB_BEV_BEER_2025_11', 'BEER 11月酒水成本率', 'BEER', 13.7, 1104, 151),
]

added = 0
for eid, label, outlet, cost_pct, rev, cost in food_costs:
    if eid not in existing_ids:
        es.append({'id': eid, 'type': 'fb_cost', 'label': label, 'outlet': outlet,
                   'food_cost_pct': cost_pct, 'food_rev': rev, 'food_cost': cost,
                   'month': '2025-11', 'source': '业主会议2025.11'})
        existing_ids.add(eid); added += 1

for eid, label, outlet, cost_pct, rev, cost in bev_costs:
    if eid not in existing_ids:
        es.append({'id': eid, 'type': 'beverage_cost_report', 'label': label, 'outlet': outlet,
                   'bev_cost_pct': cost_pct, 'bev_rev': rev, 'bev_cost': cost,
                   'month': '2025-11', 'source': '业主会议2025.11'})
        existing_ids.add(eid); added += 1

print('  +' + str(added) + ' 出口成本率节点')

# 版本
for v in [e for e in es if e.get('type')=='version' and 'FIN_VER' in e.get('id','')]:
    es.remove(v)
es.append({'id':'FIN_VER_v5_12','type':'version','label':'FIN v5.12 - 补全FB模块全年度','total_entities':len(es)})

fin['entities'] = es
json.dump(fin, open(fp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('FIN: ' + str(len(es)) + ' 实体 | v5.12')

# 展示
print('\n2025 FB年度全景:')
print('  FB总收入: ' + '{:.1f}万'.format(fb_total_rev/10000))
print('  FB总利润: ' + '{:.1f}万'.format(fb_total_profit/10000))
print('  FB平均利润率: ' + '{:.1f}%'.format(fb_total_profit/fb_total_rev*100))
print('\n各月FB利润率走势:')
for mid, rev, profit, margin in fb_data:
    lbl = mid.replace('MONTH_2025_','') + '月'
    bar = '*' * int(margin/2)
    print('  ' + lbl + ' | ' + '{:.1f}万'.format(rev/10000) + ' | 利润率 ' + '{:.1f}%'.format(margin) + ' | ' + bar)
