# -*- coding: utf-8 -*-
"""补知识缺口：酒精灯/明火/自助餐安全事故"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
with open('fsaa_graph.json', encoding='utf-8') as f:
    fsaa = json.load(f)

# ======= 步骤1: 在GSM站新增实体 =======
new_gsm_entities = [
    {
        'id': 'GSM_CAT_BURN_FIRE',
        'type': 'complaint_category',
        'name': '明火/烧伤/烫伤投诉',
        'description': '餐厅明火设备（酒精灯/煲仔炉/火焰上菜）导致客人烧伤或烫伤的投诉分类'
    },
    {
        'id': 'SCENE_CHAFING_FIRE',
        'type': 'gsm_scene',
        'name': '自助餐明火/酒精炉事故场景',
        'description': 'Open餐厅/ADD自助晚餐酒精灯、煲仔炉等明火设备起火爆炸伤人场景'
    },
    {
        'id': 'GSM_INSIGHT_CHAFING_LOW',
        'type': 'gsm_insight',
        'name': '明火设备投诉案例少（但单案风险极高）',
        'description': '明火设备投诉虽少，但一旦出事属于高赔偿/高舆情风险，需专项培训'
    },
    {
        'id': 'GSM_AUTH_FIRE_EMERGENCY',
        'type': 'gsm_approval',
        'name': '明火事故应急赔偿审批（GM+保险联合审批）',
        'description': '酒精灯等明火事故导致客人烧伤，赔偿需GM审批+保险公司介入'
    },
]

# 已有实体（检查重复）
existing_gsm_ids = {e.get('id') for e in gsm['entities']}
gsm_added_ct = 0
for ne in new_gsm_entities:
    if ne['id'] in existing_gsm_ids:
        print(f'[GSM] 已存在: {ne["id"]}')
    else:
        gsm['entities'].append(ne)
        gsm_added_ct += 1
        print(f'[GSM] 新增: {ne["id"]} - {ne["name"]}')

# ======= 步骤2: 新增GSM站关系 =======
new_gsm_rels = [
    # 投诉分类归属
    ('GSM_CAT_BURN_FIRE', 'HAS_CATEGORY', 'GSM_CAT_ROOT'),
    # 分类间关联
    ('GSM_CAT_BURN_FIRE', 'RELATES_TO', 'GSM_CAT_FIRE_SMOKE'),
    ('GSM_CAT_BURN_FIRE', 'RELATES_TO', 'GSM_CAT_FOOD'),
    ('GSM_CAT_BURN_FIRE', 'RELATES_TO', 'GSM_CAT_SAFETY_SECURITY'),
    # 场景关联
    ('SCENE_CHAFING_FIRE', 'SCENE_OF', 'GSM_LIABILITY_SAFETY_PRIVACY'),
    ('SCENE_CHAFING_FIRE', 'SCENE_OF', 'GSM_LIABILITY_FACILITY'),
    ('SCENE_CHAFING_FIRE', 'SCENE_OF', 'GSM_LIABILITY_SERVICE_DETAIL'),
    # 场景-分类关联
    ('GSM_CAT_BURN_FIRE', 'RELATES_TO', 'SCENE_CHAFING_FIRE'),
    # 场景流程
    ('SCENE_CHAFING_FIRE', 'HAS_PHASE', 'GSM_DETECT'),
    ('SCENE_CHAFING_FIRE', 'HAS_PHASE', 'GSM_DEAL'),
    ('SCENE_CHAFING_FIRE', 'HAS_PHASE', 'GSM_FOLLOW'),
    # 审批要求
    ('SCENE_CHAFING_FIRE', 'REQUIRES_APPROVAL', 'GSM_AUTH_FIRE_EMERGENCY'),
    ('SCENE_CHAFING_FIRE', 'REQUIRES_APPROVAL', 'GSM_AUTH_GM'),
    # 法律框架
    ('SCENE_CHAFING_FIRE', 'RELATES_TO', 'GSM_LAW_CIVIL'),
    ('SCENE_CHAFING_FIRE', 'RELATES_TO', 'GSM_LAW_CONSUMER'),
    # 红线
    ('SCENE_CHAFING_FIRE', 'RELATES_TO', 'GSM_REDLINE'),
    # 角色要求
    ('GSM_CAT_BURN_FIRE', 'MUST_MASTER', 'ROLE_GSM'),
    ('GSM_CAT_BURN_FIRE', 'MUST_MASTER', 'ROLE_SAFETY'),
    # 洞察
    ('SCENE_CHAFING_FIRE', 'SCENE_OF', 'GSM_INSIGHT_CHAFING_LOW'),
    # 案例关联（如果存在的话——用ADD自助餐相关案例）
]

existing_gsm_rels = set()
for r in gsm['relationships']:
    existing_gsm_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
gsm_rel_added = 0
for s, rt, t in new_gsm_rels:
    if (s, rt, t) in existing_gsm_rels:
        print(f'[GSM关系] 已存在: {s} --{rt}--> {t}')
    else:
        gsm['relationships'].append({'source': s, 'type': rt, 'target': t})
        gsm_rel_added += 1

# ======= 步骤3: RISK站新增预案 =======
new_risk_entities = [
    {
        'id': 'R_CMPCMP-098',
        'type': 'risk_entity',
        'name': '自助餐明火/酒精炉事故专项应急预案',
        'description': 'Open餐厅/ADD等自助餐区域酒精灯、煲仔炉、火焰上菜等明火设备起火爆炸伤人的应急处理流程'
    },
]

existing_risk_ids = {e.get('id') for e in risk['entities']}
risk_added_ct = 0
for ne in new_risk_entities:
    if ne['id'] in existing_risk_ids:
        print(f'[RISK] 已存在: {ne["id"]}')
    else:
        risk['entities'].append(ne)
        risk_added_ct += 1
        print(f'[RISK] 新增: {ne["id"]} - {ne["name"]}')

# RISK站新增关系
new_risk_rels = [
    # 预案→业务关联
    ('R_CMPCMP-098', 'RELATES_TO', 'R_CMPCMP-084'),    # 关联火灾预案
    ('R_CMPCMP-098', 'RELATES_TO', 'R_CMPCMP-008'),    # 关联人伤通用预案
    ('R_CMPCMP-098', 'REFERENCES', 'FIRE_EXTINGUISHER'),   # 关联灭火器
    ('R_CMPCMP-098', 'REFERENCES', 'FIRE_KITCHEN_WET_CHEM'),  # 关联厨房灭火系统
    ('R_CMPCMP-098', 'REFERENCES', 'SCENE_FIRE'),       # 关联火灾场景
    # 预案→SSOW（需新建场景）
    # SSOW通过SCENE_CHAFING_FIRE连接
]

existing_risk_rels = set()
for r in risk['relationships']:
    existing_risk_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
risk_rel_added = 0
for s, rt, t in new_risk_rels:
    if (s, rt, t) in existing_risk_rels:
        print(f'[RISK关系] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        risk_rel_added += 1

# ======= 步骤4: QA站 - 如果不存在则添加 =======
# 先查有没有明火相关的标准
has_burn_std = any('明火' in (e.get('name','') or '') and e.get('id','').startswith('QA_BS') for e in qa['entities'])
has_fire_safety_std = any('908' in e.get('id','') for e in qa['entities'])

print()
print(f'QA站是否有明火安全标准: {"有" if has_burn_std else "无，可补"}')
print(f'QA站是否有908明火操作标准: {"有" if has_fire_safety_std else "无，可加"}')

# ======= 步骤5: 跨站桥接 =======
# GSM→RISK
gsm_risk_bridge = [
    ('GSM_CAT_BURN_FIRE', 'RISK', 'R_CMPCMP-098', 'HAS_CONTINGENCY', '投诉分类→明火应急预案'),
    ('SCENE_CHAFING_FIRE', 'RISK', 'R_CMPCMP-098', 'HAS_CONTINGENCY', '投诉场景→明火应急预案'),
    ('GSM_CAT_BURN_FIRE', 'RISK', 'R_CMPCMP-084', 'RELATES_TO', '烧伤投诉→火灾预案'),
]

# GSM→QA
gsm_qa_bridge = [
    ('GSM_CAT_BURN_FIRE', 'QA', 'QA_BS_90700', 'GOVERNED_BY', '明火投诉→应急准备标准'),
    ('GSM_CAT_BURN_FIRE', 'QA', 'QA_BS_90200', 'GOVERNED_BY', '明火投诉→消防安全标准'),
    ('GSM_CAT_BURN_FIRE', 'QA', 'QA_BS_42006', 'RELATES_TO', '明火投诉→自助餐出品标准'),
    ('SCENE_CHAFING_FIRE', 'QA', 'QA_BS_90700', 'ALIGNED_WITH', '明火场景→应急准备标准'),
]

print()
print('=== 跨站桥接计划 ===')
for s, st, t, rt, desc in gsm_risk_bridge + gsm_qa_bridge:
    print(f'  {s} --[{rt}]--> {st}:{t}  ({desc})')

# ======= 写入文件 =======
with open('gsm_graph.json', 'w', encoding='utf-8') as f:
    json.dump(gsm, f, ensure_ascii=False, indent=2)
with open('risk_graph.json', 'w', encoding='utf-8') as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)

print(f'\n=== 写入完成 ===')
print(f'GSM站: +{gsm_added_ct}实体, +{gsm_rel_added}关系')
print(f'RISK站: +{risk_added_ct}实体, +{risk_rel_added}关系')
