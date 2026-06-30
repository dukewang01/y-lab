# -*- coding: utf-8 -*-
"""补SCENE_SLIPPER在GSM站的结构性缺陷 + 早餐防滑安全标准"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
with open('fsaa_graph.json', encoding='utf-8') as f:
    fsaa = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# ====== 1. GSM站：补SCENE_SLIPPER场景关系 ======
print('= 1. GSM站：SCENE_SLIPPER场景补关系 =')
new_gsm_rels = [
    # 场景→投诉分类
    ('SCENE_SLIPPER', 'CATEGORIZED_AS', 'GSM_CAT_STEP_INJURY'),
    ('SCENE_SLIPPER', 'CATEGORIZED_AS', 'GSM_CAT_SAFETY_SECURITY'),
    ('SCENE_SLIPPER', 'RELATES_TO', 'GSM_CAT_FOOD'),
    # 场景→责任维度
    ('SCENE_SLIPPER', 'SCENE_OF', 'GSM_LIABILITY_SAFETY_PRIVACY'),
    ('SCENE_SLIPPER', 'SCENE_OF', 'GSM_LIABILITY_FACILITY'),
    ('SCENE_SLIPPER', 'SCENE_OF', 'GSM_LIABILITY_POLICY'),
    # 场景→3阶段
    ('SCENE_SLIPPER', 'HAS_PHASE', 'GSM_DETECT'),
    ('SCENE_SLIPPER', 'HAS_PHASE', 'GSM_DEAL'),
    ('SCENE_SLIPPER', 'HAS_PHASE', 'GSM_FOLLOW'),
    # 场景→法律
    ('SCENE_SLIPPER', 'RELATES_TO', 'GSM_LAW_CIVIL'),
    ('SCENE_SLIPPER', 'RELATES_TO', 'GSM_LAW_CONSUMER'),
    # 场景→审批
    ('SCENE_SLIPPER', 'REQUIRES_APPROVAL', 'GSM_AUTH_GM'),
    ('SCENE_SLIPPER', 'REQUIRES_APPROVAL', 'GSM_AUTH_DO'),
    # 场景→红线
    ('SCENE_SLIPPER', 'RELATES_TO', 'GSM_REDLINE'),
    # 场景→关键案例
    ('SCENE_SLIPPER', 'HAS_EXAMPLE', 'RCASE_7365'),
    # 关联拖鞋劝阻预案
    ('SCENE_SLIPPER', 'RELATES_TO', 'R_CMPCMP-081'),
    # 关联滑倒预案（已补SSOW链）
    ('SCENE_SLIPPER', 'RELATES_TO', 'R_CMPCMP-068'),
]

existing_gsm_rels = set()
for r in gsm['relationships']:
    existing_gsm_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))

added = 0
for s, rt, t in new_gsm_rels:
    if (s, rt, t) in existing_gsm_rels:
        print(f'  [GSM] 已存在: {s} --{rt}--> {t}')
    else:
        gsm['relationships'].append({'source': s, 'type': rt, 'target': t})
        added += 1
        print(f'  [GSM] 新增: {s} --{rt}--> {t}')
print(f'  GSM += {added}关系')

# ====== 2. RISK站：补充R_CMPCMP-081（拖鞋劝阻）到早餐/防滑 ======
print()
print('= 2. RISK站：R_CMPCMP-081早餐防滑补充 =')
new_risk_rels = [
    # 拖鞋劝阻预案→SCENE_SLIPPER（现有的是在GSM方向，这里做RISK内连接）
    ('R_CMPCMP-081', 'HAS_SSOW', 'SCENE_SLIPPER'),
    # 拖鞋劝阻→关联已补SSOW的滑倒预案
    ('R_CMPCMP-081', 'RELATES_TO', 'R_CMPCMP-068'),
    # 拖鞋劝阻→自助餐/早餐区域
    ('R_CMPCMP-081', 'RELATES_TO', 'R_DEPT_F&B'),
    ('R_CMPCMP-081', 'REFERENCES', 'SIGN_WET_FLOOR'),
]

existing_risk_rels = set()
for r in risk['relationships']:
    existing_risk_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))

risk_added = 0
for s, rt, t in new_risk_rels:
    if (s, rt, t) in existing_risk_rels:
        print(f'  [RISK] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        risk_added += 1
        print(f'  [RISK] 新增: {s} --{rt}--> {t}')
print(f'  RISK += {risk_added}关系')

# ====== 3. QA站：早餐防滑安全标准 + 防滑检查项 ======
print()
print('= 3. QA站：早餐防滑标准 =')
new_qa_entities = [
    {
        'id': 'QA_BS_42010',
        'type': 'qa_standard',
        'name': '标准420.10 早餐区域防滑与安全',
        'description': '自助早餐高峰时段餐厅地面防滑管理标准。含地面湿滑快速响应、防滑提示牌放置、防滑垫铺设、地面干燥维护、穿拖鞋客人劝阻程序'
    },
    {
        'id': 'QTC_SLIP_BF_01',
        'type': 'qa_check_item',
        'name': '早餐高峰地面干燥检查（9:00-10:00关键时段）',
        'description': '早餐高峰时段（尤其8:00-10:00满场期），每15分钟巡查自助餐区域地面，检查取餐区/咖啡茶饮区/汤面区地面有无水渍、油渍、酱汁滴落'
    },
    {
        'id': 'QTC_SLIP_BF_02',
        'type': 'qa_check_item',
        'name': '防滑提示牌放置检查',
        'description': '湿滑地面区域须立即放置黄色防滑警示牌。取餐区、饮品站、蛋品台周边地面须有防滑垫。地面湿滑时醒目标识'
    },
    {
        'id': 'QTC_SLIP_BF_03',
        'type': 'qa_check_item',
        'name': '穿拖鞋/赤脚客人劝阻程序',
        'description': '餐厅工作人员发现客人穿酒店拖鞋/赤脚进入餐厅，须礼貌劝阻并提供替代鞋。劝阻话术标准化。若客人坚持，安排全程陪同协助取餐'
    },
    {
        'id': 'QTC_SLIP_BF_04',
        'type': 'qa_check_item',
        'name': '早餐时段地面保洁频次检查',
        'description': '早餐运营期间地面清洁频次：取餐区每10分钟一次，座区每30分钟一次。高峰期配备专职地面清洁人员'
    },
    {
        'id': 'QTC_SLIP_BF_05',
        'type': 'qa_check_item',
        'name': '防滑地垫配置与维护',
        'description': '自助餐取餐线、饮品站、汤面档口等易湿滑区域须铺设防滑地垫。地垫每月清洗更换，破损即换'
    },
]

existing_qa_ids = {e.get('id') for e in qa['entities']}
qa_added = 0
for ne in new_qa_entities:
    if ne['id'] in existing_qa_ids:
        print(f'  [QA] 已存在: {ne["id"]}')
    else:
        qa['entities'].append(ne)
        qa_added += 1
        print(f'  [QA] 新增: {ne["id"]} - {ne["name"]}')

# QA关系
new_qa_rels = [
    # 标准归属
    ('QA_BS_42010', 'belongs_to_section', 'QA_BS_400'),
    # 标准→检查项
    ('QA_BS_42010', 'check_standard', 'QTC_SLIP_BF_01'),
    ('QA_BS_42010', 'check_standard', 'QTC_SLIP_BF_02'),
    ('QA_BS_42010', 'check_standard', 'QTC_SLIP_BF_03'),
    ('QA_BS_42010', 'check_standard', 'QTC_SLIP_BF_04'),
    ('QA_BS_42010', 'check_standard', 'QTC_SLIP_BF_05'),
    # 跨标准关联
    ('QA_BS_42010', 'RELATES_TO', 'QA_BS_41300'),
    ('QA_BS_42010', 'RELATES_TO', 'QA_BS_42000'),
    ('QA_BS_42010', 'RELATES_TO', 'QA_BS_90200'),
]

existing_qa_rels = set()
for r in qa['relationships']:
    existing_qa_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))

qa_rel_added = 0
for s, rt, t in new_qa_rels:
    if (s, rt, t) in existing_qa_rels:
        print(f'  [QA关系] 已存在: {s} --{rt}--> {t}')
    else:
        qa['relationships'].append({'source': s, 'type': rt, 'target': t})
        qa_rel_added += 1

# ====== 4. 跨站桥接 ======
print()
print('= 4. 跨站桥接 =')

# RISK侧：GSM跨站桥接
bridge_risk = [
    ('GSM_CAT_STEP_INJURY', 'HAS_CONTINGENCY', 'R_CMPCMP-068'),
    ('GSM_CAT_SAFETY_SECURITY', 'HAS_CONTINGENCY', 'R_CMPCMP-068'),
    ('GSM_CAT_FOOD', 'HAS_CONTINGENCY', 'R_CMPCMP-081'),
]
bridge_risk_added = 0
for s, rt, t in bridge_risk:
    if (s, rt, t) in existing_risk_rels:
        print(f'  [RISK跨站] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        bridge_risk_added += 1
        print(f'  [RISK跨站] 新增: {s} --{rt}--> {t}')

# QA侧：GSM跨站桥接
bridge_qa = [
    ('SCENE_SLIPPER', 'ALIGNED_WITH', 'QA_BS_42010'),
    ('SCENE_SLIPPER', 'ALIGNED_WITH', 'QA_BS_41300'),
    ('GSM_CAT_STEP_INJURY', 'GOVERNED_BY', 'QA_BS_90200'),
    ('GSM_CAT_STEP_INJURY', 'GOVERNED_BY', 'QA_BS_42010'),
]
bridge_qa_added = 0
for s, rt, t in bridge_qa:
    if (s, rt, t) in existing_qa_rels:
        print(f'  [QA跨站] 已存在: {s} --{rt}--> {t}')
    else:
        qa['relationships'].append({'source': s, 'type': rt, 'target': t})
        bridge_qa_added += 1
        print(f'  [QA跨站] 新增: {s} --{rt}--> {t}')

# ====== 写入 ======
with open('gsm_graph.json', 'w', encoding='utf-8') as f:
    json.dump(gsm, f, ensure_ascii=False, indent=2)
with open('risk_graph.json', 'w', encoding='utf-8') as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)
with open('qa_graph.json', 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)

print()
print('=' * 60)
print('写入完成！')
print(f'  GSM站: +{added}关系')
print(f'  RISK站: +{risk_added}关系（内有跨站）')
print(f'  QA站: +{qa_added}实体, +{qa_rel_added}关系')
print(f'  跨站桥接: RISK+{bridge_risk_added}, QA+{bridge_qa_added}')
