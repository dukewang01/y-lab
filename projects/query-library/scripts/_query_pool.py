# -*- coding: utf-8 -*-
"""泳池客人摔倒 — 全链路完整查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
with open('fsaa_graph.json', encoding='utf-8') as f:
    fsaa = json.load(f)
with open('mep_graph.json', encoding='utf-8') as f:
    mep = json.load(f)

def rels_of(data, entity_id, direction='out'):
    """找实体的关系"""
    results = []
    for r in data['relationships']:
        s = r.get('source','')
        t = r.get('target','')
        rt = r.get('type') or r.get('relation','')
        if direction == 'out' and s == entity_id:
            results.append((rt, t))
        if direction == 'in' and t == entity_id:
            results.append((rt, s))
        if direction == 'both' and (s == entity_id or t == entity_id):
            if s == entity_id:
                results.append((rt, t, '→'))
            else:
                results.append((rt, s, '←'))
    return results

def name_of(data, entity_id):
    for e in data['entities']:
        if e.get('id','') == entity_id:
            return e.get('name','?')
    return '?'

def entity_of(data, entity_id):
    for e in data['entities']:
        if e.get('id','') == entity_id:
            return e
    return None

# ============ 1. GSM站 - 泳池摔倒案例 ============
print('=' * 70)
print('一、GSM投诉站 — 泳池相关实体')
print('=' * 70)

pool_gsm_ids = ['RCASE_8358','RCASE_8740','RCASE_7472B','GSM_CAT_POOL',
                'SCENE_POOL_FALL','GSM_INSIGHT_LOW_POOL']
for pid in pool_gsm_ids:
    e = entity_of(gsm, pid)
    if not e:
        continue
    print(f'\n📌 {pid}: {e.get("name","?")} (type={e.get("type","?")})')
    outs = rels_of(gsm, pid, 'out')
    ins = rels_of(gsm, pid, 'in')
    for rt, tgt in outs:
        tn = name_of(gsm, tgt)
        print(f'    → [{rt}] {tgt}: {tn}')
    for rt, src in ins:
        sn = name_of(gsm, src)
        print(f'    ← [{rt}] {src}: {sn}')

# ============ 2. 赔偿等级 ============
print('\n' + '=' * 70)
print('二、GSM赔偿等级 — 泳池摔倒适用')
print('=' * 70)
# 找RCASE_8358的赔偿关联
for pid in ['RCASE_8358','RCASE_8740','RCASE_7384']:
    e = entity_of(gsm, pid)
    if not e: continue
    print(f'\n📌 {pid}: {e.get("name","?")}')
    # 找赔偿等级
    for r in gsm['relationships']:
        if r.get('source') == pid and 'APPROVAL' in (r.get('type') or r.get('relation','')).upper():
            print(f'    赔偿等级: {r.get("target")} ({r.get("type")})')

# ============ 3. RISK预案 - 滑倒/跌倒 ============
print('\n' + '=' * 70)
print('三、RISK风险管理 — 滑倒/跌倒专项预案')
print('=' * 70)

risk_pool_entities = ['R_CMPCMP-068','R_ROOM_SLIP_DISCOVER',
                      'R_ROOM_SLIP_EVIDENCE','R_ROOM_SLIP_LIABILITY',
                      'R_RISK_CATEGORY_SLIP','RCASE_7384','RCASE_7851',
                      'RCASE_7796','RCASE_7704','RCASE_8740','RCASE_7472B']
for pid in risk_pool_entities:
    e = entity_of(risk, pid)
    if not e: continue
    print(f'\n📌 {pid}: {e.get("name","?")} (type={e.get("type","?")})')
    outs = rels_of(risk, pid, 'out')
    ins = rels_of(risk, pid, 'in')
    for rt, tgt in outs:
        tn = name_of(risk, tgt)
        print(f'    → [{rt}] {tgt}: {tn}')
    for rt, src in ins:
        sn = name_of(risk, src)
        print(f'    ← [{rt}] {src}: {sn}')

# R_CMPCMP-068的SSOW完整链条
print('\n📋 R_CMPCMP-068 SSOW流程链:')
sow_ids = []
for r in risk['relationships']:
    if r.get('source') == 'R_CMPCMP-068' and 'SSOW' in str(r.get('type')):
        sow_ids.append(r.get('target'))
    elif r.get('target') == 'R_CMPCMP-068' and 'SSOW' in str(r.get('type')):
        sow_ids.append(r.get('source'))
for sid in sow_ids:
    sn = name_of(risk, sid)
    print(f'    SSOW: {sid}: {sn}')
    # SSOW下的步骤
    for r in risk['relationships']:
        if r.get('source') == sid and 'HAS' in str(r.get('type')):
            stn = name_of(risk, r.get('target'))
            print(f'      → {r.get("target")}: {stn}')

# ============ 4. QA泳池标准 ============
print('\n' + '=' * 70)
print('四、QA品牌标准 — 泳池标准501.00')
print('=' * 70)

for pid in ['QA_BS_50100','QA_BS_500']:
    e = entity_of(qa, pid)
    if not e: continue
    print(f'\n📌 {pid}: {e.get("name","?")} (type={e.get("type","?")})')
    outs = rels_of(qa, pid, 'out')
    ins = rels_of(qa, pid, 'in')
    for rt, tgt in outs:
        tn = name_of(qa, tgt)
        print(f'    → [{rt}] {tgt}: {tn}')
    for rt, src in ins:
        sn = name_of(qa, src)
        print(f'    ← [{rt}] {src}: {sn}')

# 找Section 500的相关标准
print('\n📋 Section 500 所有标准:')
for e in qa['entities']:
    eid = e.get('id','')
    if eid.startswith('QA_BS_50'):
        print(f'    {eid}: {e.get("name","?")}')

# ============ 5. FSAA泳池相关 ============
print('\n' + '=' * 70)
print('五、FSAA食安 — 可能与泳池相关')
print('=' * 70)
for e in fsaa['entities']:
    n = (e.get('name') or '').lower()
    if any(k in n for k in ['泳池','池','pool','水质','水处理']):
        print(f'  {e.get("id","?")}: {e.get("name","?")} (type={e.get("type","?")})')

# ============ 6. MEP泳池设备 ============
print('\n' + '=' * 70)
print('六、MEP工程 — 泳池设备')
print('=' * 70)
for e in mep['entities']:
    n = (e.get('name') or '').lower()
    if any(k in n for k in ['泳池','pool','游泳']):
        print(f'  {e.get("id","?")}: {e.get("name","?")} (type={e.get("type","?")})')
        # 关联的维护标准/参数
        outs = rels_of(mep, e.get('id',''), 'out')
        for rt, tgt in outs:
            tn = name_of(mep, tgt)
            print(f'      → [{rt}] {tgt}: {tn}')
        ins = rels_of(mep, e.get('id',''), 'in')
        for rt, src in ins:
            sn = name_of(mep, src)
            print(f'      ← [{rt}] {src}: {sn}')

# ============ 7. 跨站桥接链路 ============
print('\n' + '=' * 70)
print('七、跨站桥接 — 泳池摔倒的完整链路')
print('=' * 70)

# 查GSM→QA桥
print('\nGSM→QA 跨站关系:')
for r in qa['relationships']:
    rt = r.get('type') or r.get('relation','')
    if rt in ('RELATES_TO','ALIGNED_WITH','GOVERNED_BY','EXEMPLIFIES','BELONGS_TO_AREA'):
        src = r.get('source','')
        tgt = r.get('target','')
        if 'POOL' in src or 'POOL' in tgt or 'FALL' in src or 'FALL' in tgt:
            sn = name_of(qa, src)
            tn = name_of(qa, tgt)
            print(f'  {src}→{tgt} [{rt}]')

# 查GSM→RISK桥
print('\nGSM→RISK 跨站关系:')
for r in risk['relationships']:
    rt = r.get('type') or r.get('relation','')
    if rt in ('HAS_CONTINGENCY','APPLIES_TO','INVOLVES','CATEGORIZED_AS','RELATES_TO','GOVERNED_BY','ALIGNED_WITH'):
        src = r.get('source','')
        tgt = r.get('target','')
        if 'POOL' in src or 'POOL' in tgt or 'FALL' in src or 'FALL' in tgt:
            sn = name_of(risk, src)
            tn = name_of(risk, tgt)
            print(f'  {src}→{tgt} [{rt}]')

# 查FSAA→RISK桥
print('\nFSAA→RISK 跨站关系 (TRIGGERS_RISK):')
for r in risk['relationships']:
    rt = r.get('type') or r.get('relation','')
    if rt == 'TRIGGERS_RISK':
        src = r.get('source','')
        tgt = r.get('target','')
        sn = name_of(risk, src)
        tn = name_of(risk, tgt)
        print(f'  {src}→{tgt} [{rt}]')
