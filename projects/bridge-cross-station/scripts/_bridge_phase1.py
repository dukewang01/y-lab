# -*- coding: utf-8 -*-
"""跨站联动建桥工程 Phase 1
桥1: FSAA↔RISK — 食安不符合项→风险事件
桥2: FIN↔FB — 促销联动营收 + 外卖跨站统一
桥3: FSAA↔MEP — 厨房设备→工程维护
"""

import json

def load(station):
    path = station.lower() + '_graph.json'
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save(station, data):
    path = station.lower() + '_graph.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==============================
# 桥1: FSAA↔RISK
# 食安不符合项(NC) → 风险事件(risk_case)
# 逻辑：FSAA的每个NC是一个具体风险类型，RISK里有对应的事故案例
# ==============================
print('桥1: FSAA↔RISK — 食安→风险')
fsaa = load('fsaa')
risk = load('risk')

# FSAA的NC和PCO
fsaa_ncs = [e for e in fsaa['entities'] if e.get('type')=='fsaa_nc']
fsaa_pco = [e for e in fsaa['entities'] if e.get('type')=='fsaa_pco_finding']

# RISK的风险案例
risk_cases = [e for e in risk['entities'] if e.get('type')=='risk_case']
risk_ents = [e for e in risk['entities'] if e.get('type')=='risk_entity']

print('  FSAA NCs: %d个, PCO发现: %d个' % (len(fsaa_ncs), len(fsaa_pco)))
print('  RISK案例: %d个, 风险实体: %d个' % (len(risk_cases), len(risk_ents)))

# 构建NC→风险实体映射：通过名称/主题匹配
bridge_fsaa_risk = 0
for nc in fsaa_ncs:
    nc_name = (nc.get('name_cn','') or nc.get('name','') or nc['id']).lower()
    for re in risk_ents:
        re_name = (re.get('name_cn','') or re.get('name','') or re['id']).lower()
        # 匹配关键词
        keywords = []
        if '温度' in nc_name or 'temp' in nc_name: keywords = ['温度','temp','制冷','冷藏','冷冻','保温']
        if '清洁' in nc_name or 'clean' in nc_name: keywords = ['清洁','clean','卫生','消毒']
        if '储存' in nc_name or 'storage' in nc_name: keywords = ['储存','storage','存放']
        if '虫害' in nc_name or 'pco' in nc_name: keywords = ['虫害','pco','老鼠','蟑螂']
        if '过敏' in nc_name or 'allergen' in nc_name: keywords = ['过敏','allergen']
        if '标签' in nc_name or 'label' in nc_name: keywords = ['标签','label','标识']
        if '设备' in nc_name or 'equip' in nc_name: keywords = ['设备','equip','维护']
        if '消毒' in nc_name or 'disinfect' in nc_name: keywords = ['消毒','disinfect','sanitize']
        
        for kw in keywords:
            if kw in re_name:
                rel = {
                    'source': nc['id'],
                    'target': re['id'],
                    'type': 'TRIGGERS_RISK',
                    'relation': 'TRIGGERS_RISK',
                    'properties': {'note': '食安不符合项→风险事件类型'}
                }
                risk['relationships'].append(rel)
                bridge_fsaa_risk += 1
                break
        if bridge_fsaa_risk % 50 == 0 and bridge_fsaa_risk > 0:
            pass

save('risk', risk)
print('  桥接: +%d条 TRIGGERS_RISK' % bridge_fsaa_risk)

# ==============================
# 桥2: FIN↔FB — 促销→营收 + 外卖统一 + 竞品对齐
# ==============================
print()
print('桥2: FIN↔FB — 促销→营收 + 外卖统一')
fin = load('fin')
fb = load('fb')

# 2a: promotion_product在两站间ID重叠36个→建CROSS_REFERENCE
fb_promos = {e['id']: e for e in fb['entities'] if e.get('type')=='promotion_product'}
fin_promos = {e['id']: e for e in fin['entities'] if e.get('type')=='promotion_product'}

fb_promo_ids = set(fb_promos.keys())
fin_promo_ids = set(fin_promos.keys())
promo_overlap = fb_promo_ids & fin_promo_ids

# 将FIN的promotion→FIN的daily_revenue（关联销售额数据）
promo_rev_bridge = 0
for pid in promo_overlap:
    # 在FIN中，这个promotion关联到哪些daily_revenue
    fin_rels = [r for r in fin['relationships'] 
                if r.get('source')==pid or r.get('target')==pid]
    
    # 如果FIN的promotion还没关联到daily_revenue，找该促销名称中的关键词
    promo_ent = fin_promos[pid]
    promo_name = (promo_ent.get('name_cn','') or promo_ent.get('name','') or pid).lower()
    
    # 找匹配的daily_revenue（同月/同类）
    for dr in fin['entities']:
        if dr.get('type')=='daily_revenue':
            dr_name = (dr.get('name_cn','') or dr.get('name','') or dr['id']).lower()
            # 促销名含"5MAY" → 找5月的日报
            for month_word in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec',
                               '1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']:
                if month_word in promo_name and month_word in dr_name:
                    # 检查是否已有关系
                    existing = any(r['source']==pid and r['target']==dr['id'] for r in fin['relationships'])
                    if not existing:
                        rel = {
                            'source': pid,
                            'target': dr['id'],
                            'type': 'CONTRIBUTES_TO',
                            'relation': 'CONTRIBUTES_TO',
                            'properties': {'note': '促销产品贡献营收'}
                        }
                        fin['relationships'].append(rel)
                        promo_rev_bridge += 1
                    break

# 2b: 外卖数据统一（delivery_monthly在两站间建桥）
fb_dm_ids = set(e['id'] for e in fb['entities'] if e.get('type')=='delivery_monthly')
fin_dm_ids = set(e['id'] for e in fin['entities'] if e.get('type')=='delivery_monthly')
dm_overlap = fb_dm_ids & fin_dm_ids

dm_bridge = 0
for did in dm_overlap:
    existing = any(r['source']==did for r in fin['relationships'])
    if not existing:
        rel = {
            'source': did,
            'target': did,
            'type': 'SHARED_RECORD',
            'relation': 'SHARED_RECORD',
            'properties': {'note': '外卖数据跨站共享'}
        }
        # 跨站引用：FIN的外卖→FB的外卖
        fin['relationships'].append(rel)
        dm_bridge += 1

# 2c: FB的competition_data→FIN的competition_data/other_hotel_product
fb_comp_ids = set(e['id'] for e in fb['entities'] if e.get('type')=='competition_data')
fin_comp_ids = set(e['id'] for e in fin['entities'] if e.get('type')=='competition_data')
comp_overlap = fb_comp_ids & fin_comp_ids

comp_bridge = 0
for cid in comp_overlap:
    existing = any(r.get('type')=='CROSS_REFERENCE' and r['source']==cid for r in fin['relationships'])
    if not existing:
        rel = {
            'source': cid,
            'target': cid,
            'type': 'CROSS_REFERENCE',
            'relation': 'CROSS_REFERENCE',
            'properties': {'note': '竞品数据跨站引用'}
        }
        fin['relationships'].append(rel)
        comp_bridge += 1

# 2d: FIN的menu_item→FB的menu_item
fin_menu_ids = set(e['id'] for e in fin['entities'] if e.get('type')=='menu_item')
fb_menu_ids = set(e['id'] for e in fb['entities'] if e.get('type')=='menu_item')
menu_overlap = fin_menu_ids & fb_menu_ids

menu_bridge = 0
for mid in menu_overlap:
    existing = any(r.get('type')=='SHARED_RECORD' and r['source']==mid for r in fin['relationships'])
    if not existing:
        rel = {
            'source': mid,
            'target': mid,
            'type': 'SHARED_RECORD',
            'relation': 'SHARED_RECORD',
            'properties': {'note': '菜品数据跨站引用'}
        }
        fin['relationships'].append(rel)
        menu_bridge += 1

save('fin', fin)
save('fb', fb)
print('  促销→营收: +%d条 CONTRIBUTES_TO' % promo_rev_bridge)
print('  外卖跨站: +%d条 SHARED_RECORD' % dm_bridge)
print('  竞品跨站: +%d条 CROSS_REFERENCE' % comp_bridge)
print('  菜品跨站: +%d条 SHARED_RECORD' % menu_bridge)

# ==============================
# 桥3: FSAA↔MEP
# 厨房设备 → 工程维护标准
# ==============================
print()
print('桥3: FSAA↔MEP — 食安设备→工程')
mep = load('mep')
# 重新加载（之前撤销了fsaa的save）
fsaa = load('fsaa')

# FSAA食安设备 ↔ MEP工程空间/标准
fsaa_equip = [e for e in fsaa['entities'] if e.get('type')=='fsaa_equipment']
mep_equip = [e for e in mep['entities'] if e.get('type')=='Equipment']
mep_spaces = [e for e in mep['entities'] if e.get('type')=='Space']
mep_standards = [e for e in mep['entities'] if e.get('type')=='Standard']

print('  FSAA设备: %d个, MEP设备: %d个, MEP空间: %d个' % (len(fsaa_equip), len(mep_equip), len(mep_spaces)))

# 通过名称匹配：FSAA的手洗台/MEP里的洗手设备
equip_bridge = 0
for fe in fsaa_equip:
    fe_name = (fe.get('name_cn','') or fe.get('name','') or fe['id']).lower()
    for me in mep_equip:
        me_name = (me.get('name_cn','') or me.get('name','') or me['id']).lower()
        # 关键词匹配
        match = False
        if ('wash' in fe_name or '洗手' in fe_name or 'hand' in fe_name) and \
           ('wash' in me_name or '洗手' in me_name or 'hand' in me_name):
            match = True
        if ('cool' in fe_name or 'chill' in fe_name or '冷藏' in fe_name or '冷冻' in fe_name or '冷' in fe_name) and \
           ('chill' in me_name or 'cool' in me_name or 'fridge' in me_name or '冷' in me_name):
            match = True
        if ('oven' in fe_name or '烤' in fe_name) and ('oven' in me_name or '烤' in me_name):
            match = True
        if ('fry' in fe_name or '炸' in fe_name) and ('fry' in me_name or '炸' in me_name):
            match = True
        if ('hood' in fe_name or '抽' in fe_name or '排' in fe_name) and \
           ('hood' in me_name or '抽' in me_name or '排' in me_name):
            match = True
        
        if match:
            rel = {
                'source': fe['id'],
                'target': me['id'],
                'type': 'LINKED_TO_EQUIPMENT',
                'relation': 'LINKED_TO_EQUIPMENT',
                'properties': {'note': 'FSAA设备→MEP工程设备'}
            }
            existing = any(r['source']==fe['id'] and r['target']==me['id'] for r in fsaa['relationships'])
            if not existing:
                fsaa['relationships'].append(rel)
                equip_bridge += 1
            break

save('fsaa', fsaa)
print('  设备桥接: +%d条 LINKED_TO_EQUIPMENT' % equip_bridge)

print()
print('=== 桥接工程 Phase 1 完成 ===')
total = bridge_fsaa_risk + promo_rev_bridge + dm_bridge + comp_bridge + menu_bridge + equip_bridge
print('总计新增跨站关系: %d条' % total)
