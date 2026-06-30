# -*- coding: utf-8 -*-
"""补查火灾/烧伤/自助餐链路"""
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

# 1. 查火灾相关投诉分类
print('=== GSM火灾/烧伤/安全投诉分类 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(x in eid.lower() for x in ['cat_fire','cat_burn','cat_safety','cat_food']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

# 2. RCASE火灾/烧伤相关的完整案例数据
print()
print('=== GSM火灾/烧伤/爆炸案例 ===')
fire_cases = []
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if e.get('type') == 'risk_case' and any(k in n for k in ['火警','火','烧','烫','烟感','冒火花','漏电','电']):
        fire_cases.append(eid)
        print(f'  {eid}: {e.get("name","?")}')
        for r in gsm['relationships']:
            if r.get('source') == eid:
                print(f'    → {r.get("type")} {r.get("target")}')
            if r.get('target') == eid:
                print(f'    ← {r.get("type")} {r.get("source")}')

# 3. R_CMPCMP-084火灾预案的完整关系
print()
print('=== R_CMPCMP-084 火灾/烟雾预警专项预案 ===')
for e in risk['entities']:
    if e.get('id','') == 'R_CMPCMP-084':
        print(f'  {e.get("id")}: {e.get("name","?")} (type={e.get("type","?")})')
        for r in risk['relationships']:
            if r.get('source') == 'R_CMPCMP-084':
                tname = name_of(risk, r.get('target'))
                print(f'    → {r.get("type")} {r.get("target")}: {tname}')
        break

# 4. SCENE_FIRE的SSOW
print()
print('=== SCENE_FIRE的完整链路 ===')
for e in risk['entities']:
    if e.get('id','') == 'SCENE_FIRE':
        print(f'  SCENE_FIRE: {e.get("name","?")}')
for r in risk['relationships']:
    if r.get('source') == 'SCENE_FIRE':
        tname = name_of(risk, r.get('target'))
        print(f'    → {r.get("type")} {r.get("target")}: {tname}')

# 5. 自助餐相关的标准
print()
print('=== QA自助餐+火灾标准 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if eid in ('QA_BS_42006','QA_BS_42007','QA_BS_90200','QA_BS_90700','QA_BS_90400','QA_BS_90402'):
        print(f'  {eid}: {e.get("name","?")}')
        for r in qa['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 6. FSAA ADD自助餐厅设备
print()
print('=== FSAA ADD厨房设备 ===')
for e in fsaa['entities']:
    eid = e.get('id','')
    if eid.startswith('ADD') or 'ADD' in eid:
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

# 7. 查看QA中最接近酒精灯/明火安全的标准
print()
print('=== QA 火灾安全标准详情 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if eid in ('QA_BS_90200','QA_BS_90700'):
        desc = e.get('description','') or e.get('name','')
        print(f'  {eid}: {desc[:200]}')
