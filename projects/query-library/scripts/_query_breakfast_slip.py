# -*- coding: utf-8 -*-
"""早餐/拖鞋/滑倒事件查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# 1. 穿拖鞋滑倒 - 拖鞋场景
print('=== GSM穿拖鞋场景 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if '拖鞋' in n or 'slip' in n.lower() or '滑倒' in n:
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

# 2. 裸脚滑倒场景SCENE_SLIPPER
print()
print('=== SCENE_SLIPPER 拖鞋/滑倒场景 ===')
for e in gsm['entities']:
    if e.get('id','') == 'SCENE_SLIPPER':
        for k,v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in gsm['relationships']:
    if r.get('source') == 'SCENE_SLIPPER' or r.get('target') == 'SCENE_SLIPPER':
        tn = name_of(gsm, r.get('target')) if r.get('source') == 'SCENE_SLIPPER' else name_of(gsm, r.get('source'))
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 3. RISK SCENE_SLIPPER / 滑倒SSOW
print()
print('=== RISK SCENE_SLIPPER ===')
for e in risk['entities']:
    if e.get('id','') == 'SCENE_SLIPPER':
        print(f'  {e.get("id")}: {e.get("name","?")} (type={e.get("type","?")})')
        for r in risk['relationships']:
            if r.get('source') == 'SCENE_SLIPPER' or r.get('target') == 'SCENE_SLIPPER':
                tn = name_of(risk, r.get('target') if r.get('source') == 'SCENE_SLIPPER' else r.get('source'))
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')
        break

# 4. 早餐相关场景
print()
print('=== GSM 自助早餐相关场景/分类 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['早餐','breakfast','自助','buffet','餐厅','餐厅']):
        etype = e.get('type','')
        if etype in ('gsm_scene','complaint_category','risk_case'):
            print(f'  {eid}: {e.get("name","?")} (type={etype})')

# 5. QA 早餐/自助/防滑标准
print()
print('=== QA 早餐+防滑标准 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if eid in ('QA_BS_42000','QA_BS_42006','QA_BS_42007','QA_BS_200','QA_BS_300'):
        print(f'  {eid}: {e.get("name","?")}')
        for r in qa['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 6. 自助餐地面/拖鞋安全 - 找现有的
print()
print('=== 所有滑倒/拖鞋相关关系(跨站) ===')
for r in risk['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    rt = r.get('type')
    if 'SLIP' in s or 'SLIP' in t or 'SLIPPER' in s or 'SLIPPER' in t:
        tn = name_of(risk, t) if s in ('SCENE_SLIP','SCENE_SLIPPER') else name_of(risk, s)
        print(f'  {s} --{rt}--> {t}')

# 7. 相关的赔偿等级
print()
print('=== 赔偿等级 ==')
approval_ids = [e.get('id') for e in gsm['entities'] if e.get('id','').startswith('GSM_AUTH_') and e.get('type','') in ('gsm_approval','')]
for aid in sorted(approval_ids):
    e = [x for x in gsm['entities'] if x.get('id') == aid]
    if e:
        print(f'  {aid}: {e[0].get("name","?")}')
        for r in gsm['relationships']:
            if r.get('target') == aid:
                print(f'    ← {r.get("source")} ({r.get("type")})')
