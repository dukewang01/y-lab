# -*- coding: utf-8 -*-
"""补QA站：自助餐明火操作安全标准"""
import json

with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

existing_ids = {e.get('id') for e in qa['entities']}

# 新标准
new_qa = [
    {
        'id': 'QA_BS_42008',
        'type': 'qa_standard',
        'name': '标准420.08 自助餐明火操作安全',
        'description': '自助餐区域酒精灯、煲仔炉、火焰上菜等明火设备的操作安全规范。包括：酒精灯加酒精须熄火操作、明火设备1米内无可燃物、火焰上菜须培训后操作、灭火毯须在明火区域2米范围内'
    },
    {
        'id': 'QTC_FIRE_CHAFING_01',
        'type': 'qa_check_item',
        'name': '酒精灯操作检查：加酒精前确认熄火',
        'description': '酒精灯/固体酒精炉加注燃料前，确认明火已完全熄灭，使用专用加注工具'
    },
    {
        'id': 'QTC_FIRE_CHAFING_02',
        'type': 'qa_check_item',
        'name': '明火区域安全距离检查',
        'description': '酒精灯、煲仔炉等明火设备与可燃物（桌布、菜单、装饰物）保持1米以上安全距离'
    },
    {
        'id': 'QTC_FIRE_CHAFING_03',
        'type': 'qa_check_item',
        'name': '灭火毯可用性检查',
        'description': '自助餐明火区域2米范围内配备灭火毯，每月检查无破损/在有效期内'
    },
    {
        'id': 'QTC_FIRE_CHAFING_04',
        'type': 'qa_check_item',
        'name': '明火设备操作人员培训记录',
        'description': '所有使用明火设备（酒精灯/煲仔炉/火焰上菜）的员工须经过培训考核，有记录可查'
    },
    {
        'id': 'QTC_FIRE_CHAFING_05',
        'type': 'qa_check_item',
        'name': '明火区域灭火器配置检查',
        'description': '自助餐明火烹饪区须配备ABC干粉灭火器，距明火操作点不超过10米'
    },
]

added_ct = 0
for ne in new_qa:
    if ne['id'] in existing_ids:
        print(f'[QA] 已存在: {ne["id"]}')
    else:
        qa['entities'].append(ne)
        added_ct += 1
        print(f'[QA] 新增: {ne["id"]} - {ne["name"]}')

# 关系
new_qa_rels = [
    # 标准归属
    ('QA_BS_42008', 'belongs_to_section', 'QA_BS_400'),
    # 标准→检查项
    ('QA_BS_42008', 'check_standard', 'QTC_FIRE_CHAFING_01'),
    ('QA_BS_42008', 'check_standard', 'QTC_FIRE_CHAFING_02'),
    ('QA_BS_42008', 'check_standard', 'QTC_FIRE_CHAFING_03'),
    ('QA_BS_42008', 'check_standard', 'QTC_FIRE_CHAFING_04'),
    ('QA_BS_42008', 'check_standard', 'QTC_FIRE_CHAFING_05'),
    # 安全关联
    ('QA_BS_42008', 'RELATES_TO', 'QA_BS_90200'),
    ('QA_BS_42008', 'RELATES_TO', 'QA_BS_90700'),
    ('QA_BS_42008', 'RELATES_TO', 'QA_BS_42006'),
]

existing_rels = set()
for r in qa['relationships']:
    existing_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
rel_added = 0
for s, rt, t in new_qa_rels:
    if (s, rt, t) in existing_rels:
        print(f'[QA关系] 已存在: {s} --{rt}--> {t}')
    else:
        qa['relationships'].append({'source': s, 'type': rt, 'target': t})
        rel_added += 1

# 跨站桥接到RISK
# 在RISK中加：检查项→预案的关系
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

existing_risk_rels = set()
for r in risk['relationships']:
    existing_risk_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))

risk_cross_rels = [
    ('R_CMPCMP-098', 'RELATES_TO', 'QTC_FIRE_CHAFING_01'),
    ('R_CMPCMP-098', 'RELATES_TO', 'QTC_FIRE_CHAFING_02'),
    ('R_CMPCMP-098', 'RELATES_TO', 'QTC_FIRE_CHAFING_03'),
    ('R_CMPCMP-098', 'RELATES_TO', 'QTC_FIRE_CHAFING_04'),
    ('R_CMPCMP-098', 'RELATES_TO', 'QTC_FIRE_CHAFING_05'),
    # 预案→SCENE_CHAFING_FIRE SSOW
    ('R_CMPCMP-098', 'HAS_SSOW', 'SCENE_CHAFING_FIRE'),
    # 已有SCENE_FIRE关联
    ('R_CMPCMP-098', 'REFERENCES', 'SCENE_FIRE'),
]

risk_rel_added = 0
for s, rt, t in risk_cross_rels:
    if (s, rt, t) in existing_risk_rels:
        print(f'[RISK跨站] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        risk_rel_added += 1
        print(f'[RISK跨站] 新增: {s} --{rt}--> {t}')

# 写入
with open('qa_graph.json', 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)
with open('risk_graph.json', 'w', encoding='utf-8') as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)

print(f'\n=== 写入完成 ===')
print(f'QA站: +{added_ct}实体, +{rel_added}关系')
print(f'RISK跨站: +{risk_rel_added}关系')
