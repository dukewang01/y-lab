# -*- coding: utf-8 -*-
"""钉子/异物/食安投诉查询"""
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

# 1. 异物类投诉案例
print('=== GSM 异物/钉子/铁丝/食安类案例 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if e.get('type','') == 'risk_case' and any(k in n for k in ['异物','钉子','铁丝','金属','玻璃','食安','食物','中餐','菜品','虫']):
        print(f'  {eid}: {e.get("name","?")}')

# 2. GSM_CAT_FOOD 餐饮投诉分类
print()
print('=== GSM_CAT_FOOD 餐饮投诉分类范围 ===')
for r in gsm['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    if s == 'GSM_CAT_FOOD' or t == 'GSM_CAT_FOOD':
        if 'HAS_CATEGORY' in r.get('type','') or 'CATEGORIZED_AS' in r.get('type',''):
            print(f'  {s} --{r.get("type")}--> {t}')

# 3. 相关FSAA标准
print()
print('=== FSAA 异物控制/金属检测标准 ===')
for e in fsaa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['异物','金属','physical','物理','交叉','污染','食材查验']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

# 4. QA食安标准section
print()
print('=== QA食安标准 FSAA交叉 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if 'FSAA' in eid:
        desc = e.get('description','').replace('\n',' | ')[:150]
        print(f'  {eid}: {e.get("name","?")}')

# 5. MEP厨房加工区域
print()
print('=== MEP中厨房相关区域 ===')
with open('mep_graph.json', encoding='utf-8') as f:
    mep = json.load(f)
for e in mep['entities']:
    eid = e.get('id','')
    n = (e.get('name') or '').lower()
    if eid.startswith('ZONE_') and ('厨房' in n or 'kitchen' in n or '中餐' in n or '御玺' in n):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
