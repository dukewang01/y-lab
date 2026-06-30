#!/usr/bin/env python3
"""导入4月F&B成本报告的BEV酒水成本到FIN站"""
import sys, json, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

FIN_GRAPH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json'
fin = json.load(open(FIN_GRAPH, 'r', encoding='utf-8'))

fp = r'C:\Users\Duke Wang\.openclaw\media\inbound\é_æ_ä_åº_æ_é_é_æ_æ_å_2026å¹_04æ---e1479070-427f-45b8-bb8d-d89119149318.xlsx'
wb = openpyxl.load_workbook(fp, read_only=True, data_only=True)

# BEV酒水成本
ws = wb['BEV（2）']
outlets = {4:'Beverage Store', 5:'OPEN', 6:'BQT/宴会', 7:'YUXI', 8:'BACIO', 9:'YUAN', 10:'Beer Society'}

node_id = 'COST_BEV_2026_04'
if not any(e['id'] == node_id for e in fin['entities']):
    bev_data = {'type': 'beverage_cost_report', 'month': '2026-04'}
    for col, name in outlets.items():
        try:
            bev_data[name+'_gross_rev'] = ws.cell(8, col).value
            bev_data[name+'_net_rev'] = ws.cell(10, col).value
            bev_data[name+'_opening_inv'] = ws.cell(11, col).value
            bev_data[name+'_direct_purchase'] = ws.cell(12, col).value
            bev_data[name+'_transfer'] = ws.cell(13, col).value
            bev_data[name+'_closing_inv'] = ws.cell(14, col).value
            bev_data[name+'_cost'] = ws.cell(15, col).value
        except:
            pass
    
    fin['entities'].append({
        'id': node_id,
        'name': '4月酒水成本报告',
        'type': 'beverage_cost_report',
        'date': '2026-04-30',
        'properties': bev_data
    })
    print('✅ 4月BEV成本节点已添加')
    
    # 关联到4月FIN
    for e in fin['entities']:
        if e.get('type') == 'month' and e.get('date') == '2026-04':
            fin['relationships'].append({
                'source': node_id, 'target': e['id'],
                'type': 'BELONGS_TO_MONTH', 'relation': 'BELONGS_TO_MONTH'
            })
            print('  已关联到2026-04月份')
            break
else:
    print('4月BEV成本节点已存在')

# 也导入食品成本
ws2 = wb['202604 FOOD（1）']
fnode_id = 'COST_FOOD_2026_04'
if not any(e['id'] == fnode_id for e in fin['entities']):
    food_data = {'type': 'food_cost_report', 'month': '2026-04'}
    for col, name in outlets.items():
        try:
            food_data[name+'_gross_rev'] = ws2.cell(8, col).value
            food_data[name+'_net_rev'] = ws2.cell(10, col).value
            food_data[name+'_opening_inv'] = ws2.cell(11, col).value
            food_data[name+'_purchase'] = ws2.cell(12, col).value
        except:
            pass
    
    fin['entities'].append({
        'id': fnode_id,
        'name': '4月食品成本报告',
        'type': 'food_cost_report',
        'date': '2026-04-30',
        'properties': food_data
    })
    print('✅ 4月食品成本节点已添加')
else:
    print('4月食品成本节点已存在')

# Average Covers
ws3 = wb['Average 平均消费']
print('\n=== 4月平均消费(OPEN为例) ===')
for r in [8, 9, 10, 11]:
    label = ws3.cell(r, 1).value
    cover = ws3.cell(r, 2).value
    avg = ws3.cell(r, 8).value
    if label and cover:
        print('  %s: %s人, 平均¥%s' % (str(label)[:20], cover, avg))

# 保存
json.dump(fin, open(FIN_GRAPH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
wb.close()
print('\n✅ 全部导入完成！')
