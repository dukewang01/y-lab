# -*- coding: utf-8 -*-
"""FSAA↔QA 跨站桥接 Phase 2
把FSAA的结构化食安知识与QA的品牌标准体系联通
"""
import json

with open('fsaa_graph.json', encoding='utf-8') as f:
    fsaa = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

bridge_count = 0

# =====================
# 桥1: FSAA检查项 ↔ QA 412.00 餐饮卫生标准
# =====================
# QA 412.00餐饮卫生 ↔ FSAA检查项（温度/洗手/洗碗/储存）
temp_std_fsaa = [e for e in fsaa['entities'] if e.get('type')=='fsaa_temp_standard']
check_items = [e for e in fsaa['entities'] if e.get('type')=='fsaa_check_item']
fsaa_standards = [e for e in fsaa['entities'] if e.get('type')=='fsaa_standard']

qa_412 = 'QA_BS_41200'  # 标准412.00 餐饮卫生

qa_fsaa_standards = [
    'QA_FSAA_402_HYGIENE',      # 402.01-402.06 食品安全与卫生
    'QA_FSAA_402_STORAGE',      # 402.05 食品储存
    'QA_FSAA_402_MAINT',        # 402.06 定期维护
    'QA_FSAA_401_MENU',         # 401.02 菜单
    'QA_FSAA_401_TABLEWARE',    # 401.12 餐具
    'QA_FSAA_403_IRD',          # 403.00 客房送餐
    'QA_FSAA_413_LOUNGE',       # 413.08 行政酒廊
    'QA_FSAA_420_BREAKFAST',    # 420.00-420.07 早餐
]

# QA的FSAA引用标准 → FSAA检查项
fsaa_qa_std_map = {
    'QA_FSAA_402_HYGIENE': ['温度','洗手','消毒','手套','卫生','clean','sanitize','手洗','洗'],
    'QA_FSAA_402_STORAGE': ['储存','存储','storage','冷藏','冷冻','cool','chill','存放','标签'],
    'QA_FSAA_402_MAINT': ['设备','equipment','维护','保养','清洗','hood','排','抽'],
    'QA_FSAA_401_MENU': ['菜单','menu','过敏','allergen','菜'],
    'QA_FSAA_401_TABLEWARE': ['餐具','器皿','瓷器','不锈钢','玻璃','餐具','tableware','盘','杯','刀叉'],
    'QA_FSAA_403_IRD': ['客房送餐','ird','送餐','保温箱','木制搅拌'],
    'QA_FSAA_413_LOUNGE': ['行政酒廊','lounge','茶','酒廊'],
    'QA_FSAA_420_BREAKFAST': ['早餐','breakfast','蛋','面包','谷物','酸奶','水果','果汁','热菜','肉','咖啡','鸡蛋','油条','粥','牛肉面','羊角'],
}

# 建桥：QA_FSAA标准 → 匹配的FSAA检查项
for qa_std_id, keywords in fsaa_qa_std_map.items():
    for ci in check_items:
        ci_name = (ci.get('name_cn','') or ci.get('name','') or ci['id']).lower()
        if any(kw.lower() in ci_name for kw in keywords):
            # 检查重复
            exists = any(r['source']==qa_std_id and r['target']==ci['id'] for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': qa_std_id, 'target': ci['id'],
                    'relation': 'GOVERNED_BY',
                    'type': 'GOVERNED_BY',
                    'properties': {'note': 'QA品牌标准管控FSAA检查项'}
                })
                bridge_count += 1
            break  # 每个标准→检查项只连一条最匹配的

# =====================
# 桥2: FSAA检查项 ↔ QA QA_BS_41200 标准
# =====================
# 每个FSAA检查项 → 对应的QA标准
qa_412_clean = next((e for e in qa['entities'] if e['id']=='QA_BS_41200'), None)
if qa_412_clean:
    # FSAA温度相关
    temp_keywords = ['温度','temp','冷','chill','冷冻','冷藏','cool']
    for ci in check_items:
        ci_name = (ci.get('name_cn','') or ci.get('name','') or ci['id']).lower()
        if any(kw in ci_name for kw in temp_keywords):
            exists = any(r['source']==ci['id'] and r['target']=='QA_BS_41200' for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': ci['id'], 'target': 'QA_BS_41200',
                    'relation': 'ALIGNED_WITH',
                    'type': 'ALIGNED_WITH',
                    'properties': {'note': 'FSAA温度检查项→QA餐饮卫生标准'}
                })
                bridge_count += 1

# =====================
# 桥3: QA_BS_41300 清洁卫生 ↔ FSAA检查项（清洁相关）
# =====================
clean_keywords = ['清洁','clean','卫生','消毒','洗碗','sanitize','disinfect']
qa_413 = 'QA_BS_41300'
for ci in check_items:
    ci_name = (ci.get('name_cn','') or ci.get('name','') or ci['id']).lower()
    if any(kw in ci_name for kw in clean_keywords):
        exists = any(r['source']==ci['id'] and r['target']==qa_413 for r in qa['relationships'])
        if not exists:
            qa['relationships'].append({
                'source': ci['id'], 'target': qa_413,
                'relation': 'ALIGNED_WITH',
                'type': 'ALIGNED_WITH',
                'properties': {'note': 'FSAA清洁检查项→QA清洁卫生标准'}
            })
            bridge_count += 1

# =====================
# 桥4: FSAA过敏原 → QA 412.00
# =====================
allergens = [e for e in fsaa['entities'] if e.get('type')=='fsaa_allergen']
for a in allergens:
    exists = any(r['source']==a['id'] and r['target']=='QA_BS_41200' for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': a['id'], 'target': 'QA_BS_41200',
            'relation': 'RELEVANT_TO',
            'type': 'RELEVANT_TO',
            'properties': {'note': 'FSAA过敏原→QA餐饮卫生标准'}
        })
        bridge_count += 1

# =====================
# 桥5: FSAA温度标准 → QA早餐标准(BF6)
# =====================
bf_standards = ['QA_BF6_COFFEE','QA_BF6_EGG','QA_BF6_CROISSANT','QA_BF6_CONGEE',
                'QA_BF6_BEEF_NOODLE','QA_BF6_YOUTIAO','QA_BF_FOOD_HOT','QA_BF_FOOD_COLD']

bf_keywords_map = {
    'QA_BF6_COFFEE': ['咖啡','coffee'],
    'QA_BF6_EGG': ['蛋','egg'],
    'QA_BF_FOOD_HOT': ['热','hot','保温','温度'],
    'QA_BF_FOOD_COLD': ['冷','cold','冷藏','冷冻'],
}

for bf_id, bf_kws in bf_keywords_map.items():
    for ts in temp_std_fsaa:
        ts_name = (ts.get('name_cn','') or ts.get('name','') or ts['id']).lower()
        if any(kw in ts_name for kw in bf_kws):
            exists = any(r['source']==ts['id'] and r['target']==bf_id for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': ts['id'], 'target': bf_id,
                    'relation': 'RELEVANT_TO',
                    'type': 'RELEVANT_TO',
                    'properties': {'note': 'FSAA温度标准→QA早餐标准'}
                })
                bridge_count += 1
            break

# =====================
# 桥6: FSAA流程 → QA品牌标准（食品处理流程↔QA标准）
# =====================
processes = [e for e in fsaa['entities'] if e.get('type')=='fsaa_process']
qa_fsaa_standards_for_process = ['QA_FSAA_402_HYGIENE','QA_FSAA_402_STORAGE']

# 拿FSAA流程的名字，匹配QA FSAA标准
process_keywords = {
    'QA_FSAA_402_HYGIENE': ['洗手','消毒','clean','温度','temp','卫生','手套'],
    'QA_FSAA_402_STORAGE': ['存储','存放','label','标签','库存'],
    'QA_FSAA_402_MAINT': ['维护','清洗','清洁','设备'],
}

for qa_std_id, kws in process_keywords.items():
    for p in processes:
        p_name = (p.get('name_cn','') or p.get('name','') or p['id']).lower()
        if any(kw in p_name for kw in kws):
            exists = any(r['source']==p['id'] and r['target']==qa_std_id for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': p['id'], 'target': qa_std_id,
                    'relation': 'GOVERNED_BY',
                    'type': 'GOVERNED_BY',
                    'properties': {'note': 'FSAA操作流程→QA品牌标准'}
                })
                bridge_count += 1
            break

# =====================
# 桥7: QA Section 400 餐饮 → FSAA检查项
# =====================
section_400 = 'Section QA_BS_400'
section_400_qmod = 'QMOD_FB'

# Section 400 F&B → 所有FSAA餐饮相关的检查项
fb_ci_count = 0
for ci in check_items:
    ci_name = (ci.get('name_cn','') or ci.get('name','') or ci['id']).lower()
    # 所有FSAA检查项都与餐饮相关
    if fb_ci_count < 5:  # 只连5条代表
        exists = any(r['source']==ci['id'] and r['target']==section_400 for r in qa['relationships'])
        if not exists:
            qa['relationships'].append({
                'source': ci['id'], 'target': section_400,
                'relation': 'BELONGS_TO_AREA',
                'type': 'BELONGS_TO_AREA',
                'properties': {'note': 'FSAA检查项→QA餐饮Section'}
            })
            bridge_count += 1
            fb_ci_count += 1

# =====================
# 桥8: FSAA库存/保质期 → QA_BS_41200/722.00
# =====================
shelf_life = [e for e in fsaa['entities'] if e.get('type')=='fsaa_shelf_life']
qa_722 = next((e for e in qa['entities'] if e['id']=='QA_BS_72200'), None)

if qa_722:
    for sl in shelf_life[:10]:  # 10条代表
        sl_name = (sl.get('name_cn','') or sl.get('name','') or sl['id']).lower()
        if 'cook' in sl_name or '冷' in sl_name or '冻' in sl_name or '熟' in sl_name:
            exists = any(r['source']==sl['id'] and r['target']==qa_722['id'] for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': sl['id'], 'target': qa_722['id'],
                    'relation': 'MONITORED_BY',
                    'type': 'MONITORED_BY',
                    'properties': {'note': 'FSAA保质期→深度清洁标准'}
                })
                bridge_count += 1

# =====================
# 桥9: FSAA厨房 → QA 400系列
# =====================
kitchens = [e for e in fsaa['entities'] if e.get('type')=='fsaa_kitchen']
qa_bs_401 = 'QA_BS_40100'

for k in kitchens:
    k_name = (k.get('name_cn','') or k.get('name','') or k['id']).lower()
    exists = any(r['source']==k['id'] and r['target']==qa_bs_401 for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': k['id'], 'target': qa_bs_401,
            'relation': 'SERVES',
            'type': 'SERVES',
            'properties': {'note': 'FSAA厨房→QA 401.00餐厅标准'}
        })
        bridge_count += 1

# =====================
# 桥10: FSAA政策 → QA政策
# =====================
policies = [e for e in fsaa['entities'] if e.get('type')=='fsaa_policy']
qa_policy_standards_ids = [e['id'] for e in qa['entities'] if e.get('type')=='qa_standard' and 'QA_POLICY_' in e['id']]

for p in policies:
    p_name = (p.get('name_cn','') or p.get('name','') or p['id']).lower()
    for qps_id in qa_policy_standards_ids:
        qps_e = next((e for e in qa['entities'] if e['id']==qps_id), None)
        if qps_e:
            qps_name = (qps_e.get('name_cn','') or qps_e.get('name','') or '').lower()
            # 关键词匹配
            for kw in ['食品','food','卫生','hygiene','安全','safety','清洁','clean','过敏','allergen']:
                if kw in p_name and kw in qps_name:
                    exists = any(r['source']==p['id'] and r['target']==qps_id for r in qa['relationships'])
                    if not exists:
                        qa['relationships'].append({
                            'source': p['id'], 'target': qps_id,
                            'relation': 'ALIGNED_WITH',
                            'type': 'ALIGNED_WITH',
                            'properties': {'note': 'FSAA政策↔QA政策标准'}
                        })
                        bridge_count += 1
                    break
            if bridge_count % 10 == 0: pass

# ====== 写回 ======
with open('qa_graph.json', 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)

print('FSAA↔QA 桥接完成: +%d条跨站关系' % bridge_count)
print()
print('桥梁明细:')
print('  桥1: QA_FSAA标准 → FSAA检查项 (GOVERNED_BY)')
print('  桥2: FSAA检查项 → QA 412.00 (ALIGNED_WITH)')
print('  桥3: FSAA清洁检查 → QA 413.00 (ALIGNED_WITH)')
print('  桥4: FSAA过敏原 → QA 412.00 (RELEVANT_TO)')
print('  桥5: FSAA温度标准 → QA早餐BF6 (RELEVANT_TO)')
print('  桥6: FSAA流程 → QA_FSAA标准 (GOVERNED_BY)')
print('  桥7: FSAA检查项 → Section 400 (BELONGS_TO_AREA)')
print('  桥8: FSAA保质期 → QA 722.00 (MONITORED_BY)')
print('  桥9: FSAA厨房 → QA 401.00 (SERVES)')
print('  桥10: FSAA政策 → QA政策标准 (ALIGNED_WITH)')
