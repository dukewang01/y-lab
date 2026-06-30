# -*- coding: utf-8 -*-
"""GSM↔RISK 跨站桥接深化 Phase 2b
GSM的投诉分类/场景/法律/赔偿 → RISK的预案/控制措施/法律实体
"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

bridge_count = 0

# GSM索引
cats = {e['id']: e for e in gsm['entities'] if e.get('type')=='complaint_category'}
scenes = {e['id']: e for e in gsm['entities'] if e.get('type')=='gsm_scene'}
legal_fw = {e['id']: e for e in gsm['entities'] if e.get('type')=='gsm_legal_framework'}
levels = {e['id']: e for e in gsm['entities'] if e.get('type')=='approval_level'}
gsm_cases = {e['id']: e for e in gsm['entities'] if e.get('type')=='risk_case'}

# RISK索引
risk_plans = {e['id']: e for e in risk['entities'] if 'R_CMP' in e.get('id','') and 'case' not in e.get('id','').lower() and 'cmp-' not in e.get('id','').lower()}
risk_cases = {e['id']: e for e in risk['entities'] if e.get('type')=='risk_case'}
risk_ents = {e['id']: e for e in risk['entities'] if e.get('type')=='risk_entity'}
risk_cms = {e['id']: e for e in risk['entities'] if e.get('type')=='CONTROL_MEASURE'}
risk_regs = {e['id']: e for e in risk['entities'] if e.get('type')=='RISK_REGISTER'}
risk_eqs = {e['id']: e for e in risk['entities'] if e.get('type')=='Equipment'}

# =====================
# 桥1: GSM投诉分类 → RISK预案（投诉类型→对应预案）
# =====================
cat_to_plan = {
    'GSM_CAT_SAFETY_SECURITY': ['CMP-001','CMP-004','CMP-009','CMP-011','CMP-012','CMP-090','CMP-040','CMP-078','CMP-079','CMP-081'],
    'GSM_CAT_NOISE': ['CMP-036','CMP-037'],
    'GSM_CAT_AC_TEMP': ['CMP-038','CMP-039'],
    'GSM_CAT_WATER': ['CMP-014'],
    'GSM_CAT_FOOD': ['CMP-025','CMP-026','CMP-030','CMP-031','CMP-023'],
    'GSM_CAT_BILLING': ['CMP-035','CMP-027'],
    'GSM_CAT_LOST_ITEM': ['CMP-077','CMP-076'],
    'GSM_CAT_CLEAN': ['CMP-043','CMP-044','CMP-047'],
    'GSM_CAT_FACILITY': ['CMP-015','CMP-016','CMP-051','CMP-052','CMP-048'],
    'GSM_CAT_ROOM_FAC': ['CMP-015','CMP-016','CMP-048','CMP-051'],
    'GSM_CAT_PARKING': ['CMP-033','CMP-034','CMP-054','CMP-055','CMP-056'],
    'GSM_CAT_ATTITUDE': ['CMP-040','CMP-041'],
    'GSM_CAT_EFFICIENCY': ['CMP-040','CMP-041','CMP-042'],
    'GSM_CAT_HOUSEKEEPING': ['CMP-043','CMP-044','CMP-077'],
}

for cid, plan_ids in cat_to_plan.items():
    if cid not in cats:
        continue
    for pid_num in plan_ids:
        # 找到RISK中对应的预案ID
        found_plan = None
        for rpid in risk_plans:
            if pid_num.lower() in rpid.lower() or pid_num.replace('-','').lower() in rpid.lower():
                found_plan = rpid
                break
        if found_plan:
            exists = any(r['source']==cid and r['target']==found_plan for r in risk['relationships'])
            if not exists:
                risk['relationships'].append({
                    'source': cid, 'target': found_plan,
                    'relation': 'HAS_CONTINGENCY',
                    'type': 'HAS_CONTINGENCY',
                    'properties': {'note': 'GSM投诉分类→RISK应急预案'}
                })
                bridge_count += 1

# =====================
# 桥2: GSM投诉场景 → RISK预案（具体场景→预案）
# =====================
scene_to_plan = {
    'SCENE_POOL_FALL': ['CMP-020','CMP-013','CMP-053','CMP-057'],
    'SCENE_NOISE': ['CMP-036','CMP-037','CMP-081'],
    'SCENE_AC': ['CMP-038','CMP-039'],
    'SCENE_LOST': ['CMP-076','CMP-077','CMP-083'],
    'SCENE_BILL': ['CMP-035','CMP-027'],
    'SCENE_ATTITUDE': ['CMP-040','CMP-041'],
    'SCENE_SAFETY': ['CMP-001','CMP-004','CMP-078','CMP-079','CMP-081','CMP-090'],
    'SCENE_PARKING': ['CMP-033','CMP-034','CMP-054','CMP-055','CMP-056'],
}

for sid, plan_ids in scene_to_plan.items():
    if sid not in scenes:
        continue
    for pid_num in plan_ids:
        found_plan = None
        for rpid in risk_plans:
            if pid_num.lower() in rpid.lower():
                found_plan = rpid
                break
        if found_plan:
            exists = any(r['source']==sid and r['target']==found_plan for r in risk['relationships'])
            if not exists:
                risk['relationships'].append({
                    'source': sid, 'target': found_plan,
                    'relation': 'HAS_CONTINGENCY',
                    'type': 'HAS_CONTINGENCY',
                    'properties': {'note': 'GSM投诉场景→RISK应急预案'}
                })
                bridge_count += 1

# =====================
# 桥3: GSM法律框架 → RISK法律实体（法律→法律风险事件）
# =====================
legal_keywords = {
    'GSM_LAW_CONSUMER': ['消费','消费者','消法'],
    'GSM_LAW_CIVIL': ['侵权','民法典','民事'],
    'GSM_LAW_HOTEL': ['住宿','旅馆','酒店管理'],
    'GSM_LAW_FOOD_SAFETY': ['食品','食安','food'],
    'GSM_LAW_CONTRACT': ['合同','契约'],
    'GSM_LAW_PRIVACY': ['隐私','信息','personal'],
    'GSM_LAW_FIRE': ['消防','fire'],
}

for lid, kws in legal_keywords.items():
    if lid not in legal_fw:
        continue
    for re_id, re_ent in risk_ents.items():
        re_name = (re_ent.get('name_cn','') or re_ent.get('name','') or re_id).lower()
        if any(kw.lower() in re_name for kw in kws):
            exists = any(r['source']==lid and r['target']==re_id for r in risk['relationships'])
            if not exists:
                risk['relationships'].append({
                    'source': lid, 'target': re_id,
                    'relation': 'GOVERNED_BY',
                    'type': 'GOVERNED_BY',
                    'properties': {'note': 'GSM法律框架→RISK风险法律实体'}
                })
                bridge_count += 1

# =====================
# 桥4: GSM赔偿等级 → RISK Control Measure
# =====================
level_to_cm = {
    'GSM_AUTH_GSM_ONLY': ['CMP-040','CMP-041'],
    'GSM_AUTH_MOD': ['CMP-040','CMP-041'],
    'GSM_AUTH_DO': ['CMP-040','CMP-041','CMP-076'],
    'GSM_AUTH_GM': ['CMP-040','CMP-001','CMP-004'],
}

for lid, plan_ids in level_to_cm.items():
    if lid not in levels:
        continue
    for pid in plan_ids:
        # 找RISK的预案
        found = None
        for rpid in risk_plans:
            if pid.lower() in rpid.lower():
                found = rpid
                break
        if found:
            exists = any(r['source']==lid and r['target']==found for r in risk['relationships'])
            if not exists:
                risk['relationships'].append({
                    'source': lid, 'target': found,
                    'relation': 'APPLIES_TO',
                    'type': 'APPLIES_TO',
                    'properties': {'note': 'GSM赔偿等级→RISK预案适用范围'}
                })
                bridge_count += 1

# =====================
# 桥5: GSM投诉案例 → RISK风险设备/地点
# =====================
# 通过投诉内容匹配RISK中的Equipment
case_eq_map = {}
for gsid, gs_e in gsm_cases.items():
    gs_name = (gs_e.get('name_cn','') or gs_e.get('name','') or '').lower()
    if not gs_name:
        continue
    for eq_id, eq_e in risk_eqs.items():
        eq_name = (eq_e.get('name_cn','') or eq_e.get('name','') or eq_id).lower()
        # 火灾相关投诉→消防设备
        if ('火' in gs_name or 'fire' in gs_name) and ('fire' in eq_name or '消防' in eq_name):
            if gsid not in case_eq_map:
                case_eq_map[gsid] = eq_id
                break

for gsid, eqid in case_eq_map.items():
    if gsid in risk_ents:
        exists = any(r['source']==gsid and r['target']==eqid for r in risk['relationships'])
        if not exists:
            risk['relationships'].append({
                'source': gsid, 'target': eqid,
                'relation': 'INVOLVES',
                'type': 'INVOLVES',
                'properties': {'note': 'GSM投诉案例→RISK涉及设备'}
            })
            bridge_count += 1

# =====================
# 桥6: GSM投诉场景 → RISK风险分类(risk_category)
# =====================
scene_to_rcat = {
    'SCENE_POOL_FALL': 'RCAT_01', 'SCENE_NOISE': 'RCAT_02',
    'SCENE_AC': 'RCAT_02', 'SCENE_LOST': 'RCAT_07',
    'SCENE_BILL': 'RCAT_05', 'SCENE_ATTITUDE': 'RCAT_04',
    'SCENE_SAFETY': 'RCAT_08', 'SCENE_PARKING': 'RCAT_01',
}

for sid, rcat in scene_to_rcat.items():
    if sid not in scenes:
        continue
    exists = any(r['source']==sid and r['target']==rcat for r in risk['relationships'])
    if not exists:
        risk['relationships'].append({
            'source': sid, 'target': rcat,
            'relation': 'CATEGORIZED_AS',
            'type': 'CATEGORIZED_AS',
            'properties': {'note': 'GSM投诉场景→RISK风险分类'}
        })
        bridge_count += 1

# =====================
# 桥7: GSM投诉案例名称 → RISK关联的风险实体（通过名称匹配）
# =====================
case_keyword_map = {
    '泳池': 'R_POOL_ACCIDENT',
    '消防': 'R_FIRE_EMERGENCY',
    '火灾': 'R_FIRE_EMERGENCY',
    '噪音': 'R_NOISE_COMPLAINT',
    '空调': 'R_TEMP_COMPLAINT',
    '温度': 'R_TEMP_COMPLAINT',
    '冷': 'R_TEMP_COMPLAINT',
    '停车': 'R_PARKING_ACCIDENT',
    '丢失': 'R_LOST_ITEM',
    '食物': 'R_FOOD_POISONING',
    '食': 'R_FOOD_POISONING',
    '电梯': 'R_ELEVATOR_INCIDENT',
    '漏水': 'R_WATER_LEAK',
    '水': 'R_WATER_LEAK',
    '摔倒': 'R_SLIP_FALL',
    '受伤': 'R_GUEST_INJURY',
    '过敏': 'R_ALLERGEN_INCIDENT',
}

# 反向找：RISK中是否有这些名字
risk_doc_docs = {e['id']: e for e in risk['entities'] if e.get('type')=='risk_entity'}

case_risk_match = 0
for gsid, gs_e in gsm_cases.items():
    gs_name = (gs_e.get('name_cn','') or gs_e.get('name','') or '').lower()
    if not gs_name:
        continue
    for keyword, risk_entity_kw in case_keyword_map.items():
        if keyword.lower() in gs_name:
            # 找RISK中匹配的实体
            for rdoc_id, rdoc_e in risk_doc_docs.items():
                rdoc_name = (rdoc_e.get('name_cn','') or rdoc_e.get('name','') or rdoc_id).lower()
                if keyword.lower() in rdoc_name:
                    exists = any(r['source']==gsid and r['target']==rdoc_id for r in risk['relationships'])
                    if not exists:
                        risk['relationships'].append({
                            'source': gsid, 'target': rdoc_id,
                            'relation': 'RELATES_TO',
                            'type': 'RELATES_TO',
                            'properties': {'note': 'GSM投诉案例→RISK风险实体'}
                        })
                        case_risk_match += 1
                        break
            break

bridge_count += case_risk_match

# =====================
# 桥8: GSM安全红线 → RISK预案
# =====================
redlines = [e for e in gsm['entities'] if e.get('type')=='redline']
for rl in redlines:
    rl_name = (rl.get('name_cn','') or rl.get('name','') or rl['id']).lower()
    for rpid, rp_e in risk_plans.items():
        rp_name = (rp_e.get('name_cn','') or rp_e.get('name','') or rpid).lower()
        if '安全' in rl_name or 'safety' in rl_name:
            if '安全' in rp_name or 'safety' in rp_name or 'fire' in rp_name or '消防' in rp_name:
                exists = any(r['source']==rl['id'] and r['target']==rpid for r in risk['relationships'])
                if not exists:
                    risk['relationships'].append({
                        'source': rl['id'], 'target': rpid,
                        'relation': 'ALIGNED_WITH',
                        'type': 'ALIGNED_WITH',
                        'properties': {'note': 'GSM安全红线→RISK预案'}
                    })
                    bridge_count += 1
                break

# ====== 写回 ======
with open('risk_graph.json', 'w', encoding='utf-8') as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)

print('GSM↔RISK 桥接深化完成: +%d条跨站关系' % bridge_count)
print()
print('桥梁明细:')
print('  桥1: GSM投诉分类→RISK预案 (HAS_CONTINGENCY)')
print('  桥2: GSM投诉场景→RISK预案 (HAS_CONTINGENCY)')
print('  桥3: GSM法律框架→RISK法律实体 (GOVERNED_BY)')
print('  桥4: GSM赔偿等级→RISK预案 (APPLIES_TO)')
print('  桥5: GSM投诉案例→RISK设备 (INVOLVES)')
print('  桥6: GSM投诉场景→RISK风险分类 (CATEGORIZED_AS)')
print('  桥7: GSM投诉案例→RISK风险实体 (RELATES_TO)')
print('  桥8: GSM安全红线→RISK预案 (ALIGNED_WITH)')
