#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""导入虫害PCO报告到FSAA站"""
import sys, json, os, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp_fsaa = os.path.join(D, 'fsaa_graph.json')

fsaa = json.load(open(fp_fsaa, encoding='utf-8'))
fae = fsaa.get('entities', [])
far = fsaa.get('relationships', [])
e_map = {n['id']: n for n in fae}

existing = set()
for r in far:
    existing.add((r.get('source_id',''), r.get('type',''), r.get('target_id','')))

new_nodes = []
new_rels = []

# 服务整体节点
pco_id = 'PCO_20260506'
pco = {
    'id': pco_id,
    'name': '2026年5月6日虫害常规服务报告',
    'type': 'fsaa_pco_report',
    'properties': {
        'date': '2026-05-06',
        'provider': '浙江帮帮环境科技集团有限公司',
        'service_type': '常规服务',
        'technician': '丁杰',
        'phone': '15895568721',
        'next_followup': '2026-05-12',
        'status': '未完成'
    }
}
if pco_id not in e_map:
    new_nodes.append(pco)
    e_map[pco_id] = pco
    print('创建PCO报告节点: %s' % pco['name'])

# 问题节点
issues = [
    {
        'id': 'PCO_ISSUE_BANQUET_DISH_DRAIN',
        'name': '宴会厨房洗碗间排水沟积水',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '宴会厨房洗碗间',
            'issue': '排水沟内存有污水无法排出，已滋生蛾蠓',
            'severity': 'high',
            'action': '定期药物处理，及时清理',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    },
    {
        'id': 'PCO_ISSUE_WEST_RESTAURANT_PUDDLE',
        'name': '西餐厅明档水池下方积水',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '西餐厅明档',
            'issue': '水池下方存有积水，已滋生蛾蠓及幼虫',
            'severity': 'high',
            'action': '定期药物处理，及时清理',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    },
    {
        'id': 'PCO_ISSUE_3F_NOODLE_COCKROACH',
        'name': '3F面馆厨房灶台下方蟑螂活体',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '3F中厨房面馆',
            'issue': '灶台下方存有污垢未及时清理，发现蟑螂活体',
            'severity': 'high',
            'action': '定期药物处理，及时清理',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    },
    {
        'id': 'PCO_ISSUE_3F_FISH_MOTH',
        'name': '3F杀鱼间蛾蠓较多',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '3F杀鱼间',
            'issue': '蛾蠓较多，建议加装胶帘预防入侵厨房',
            'severity': 'medium',
            'action': '定期药物处理，建议加装胶帘或风幕机',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    },
    {
        'id': 'PCO_ISSUE_RECEIVING_DRAIN',
        'name': '收货平台排水槽积水异味',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '收货平台',
            'issue': '下方排水槽内有积水且已产生异味',
            'severity': 'medium',
            'action': '定期药物处理，建议及时清理',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    },
    {
        'id': 'PCO_ISSUE_BANQUET_LEAK',
        'name': '宴会厨房水池下隔渣池漏水',
        'type': 'fsaa_pco_finding',
        'properties': {
            'location': '宴会厨房',
            'issue': '水池下方隔渣池下方漏水',
            'severity': 'medium',
            'action': '定期药物处理，建议及时修复',
            'responsible': '管事部',
            'date': '2026-05-06',
            'status': '未完成'
        }
    }
]

for iss in issues:
    if iss['id'] not in e_map:
        new_nodes.append(iss)
        e_map[iss['id']] = iss
        print('创建问题节点: %s' % iss['name'])

# 关系
# 报告→每个问题
for iss in issues:
    rel = ('PCO_20260506', 'has_finding', iss['id'])
    if rel not in existing:
        new_rels.append({'source_id': rel[0], 'type': rel[1], 'target_id': rel[2]})
        existing.add(rel)

# 报告→FSAA_SERVICE_RECORDS（如果节点存在）
if 'FSAA_SERVICE_RECORDS' in e_map:
    rel = ('PCO_20260506', 'belongs_to', 'FSAA_SERVICE_RECORDS')
    if rel not in existing:
        new_rels.append({'source_id': rel[0], 'type': rel[1], 'target_id': rel[2]})
        existing.add(rel)

# 写入
if new_nodes or new_rels:
    bak_fp = fp_fsaa.replace('.json', '_before_pco0506.json')
    shutil.copy2(fp_fsaa, bak_fp)
    print('\n备份:', bak_fp)

    if new_nodes:
        fae.extend(new_nodes)
    if new_rels:
        far.extend(new_rels)
    
    fsaa['entities'] = fae
    fsaa['relationships'] = far
    json.dump(fsaa, open(fp_fsaa, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    
    print('新增节点: %d个' % len(new_nodes))
    print('新增关系: %d条' % len(new_rels))
    print('FSAA站: %d节点 / %d关系' % (len(fae), len(far)))
else:
    print('无新增')
