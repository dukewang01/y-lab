# -*- coding: utf-8 -*-
"""入住高峰/等房/不满 查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# 1. 等房类案例
print('=== 等房/打扫/入住慢案例 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if e.get('type','') == 'risk_case' and any(k in n for k in ['等房','入住','打扫','没房','房间慢','等房间','clean','housekeeping','提前入住']):
        print(f'  {eid}: {e.get("name","?")}')

# 2. 效率投诉
print()
print('=== GSM_CAT_EFFICIENCY 效率投诉 ===')
for r in gsm['relationships']:
    if 'EFFICIENCY' in r.get('source','') or 'EFFICIENCY' in r.get('target',''):
        if 'CAT' in r.get('source','') or 'CAT' in r.get('target',''):
            print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

print('效率分类下案例：')
for r in gsm['relationships']:
    if r.get('type','') == 'CATEGORIZED_AS' and r.get('target') == 'GSM_CAT_EFFICIENCY':
        s = r.get('source','')
        for e in gsm['entities']:
            if e.get('id') == s:
                print(f'  {s}: {e.get("name","?")}')

# 3. 客房打扫相关
print()
print('=== GSM_CAT_HOUSEKEEPING 客房清洁投诉 ===')
for e in gsm['entities']:
    if e.get('id','') == 'GSM_CAT_HOUSEKEEPING':
        print(f'  {e["id"]}: {e.get("name","?")}')
        for r in gsm['relationships']:
            if r.get('source') == 'GSM_CAT_HOUSEKEEPING' or r.get('target') == 'GSM_CAT_HOUSEKEEPING':
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')
        break

# 4. 情绪不满 - GSMCAT_ATTITUDE
print()
print('=== GSM_CAT_ATTITUDE 态度/情绪投诉 ===')
for r in gsm['relationships']:
    if r.get('source') == 'GSM_CAT_ATTITUDE' or r.get('target') == 'GSM_CAT_ATTITUDE':
        if r.get('type') == 'HAS_CATEGORY' or r.get('type') == 'CATEGORIZED_AS':
            print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 5. 审批等级
print()
print('=== 审批阶梯 ===')
for e in gsm['entities']:
    if e.get('id','') in ['GSM_AUTH_FRONT','GSM_AUTH_SUPERVISOR','GSM_AUTH_GSM','GSM_AUTH_DO','GSM_AUTH_GM']:
        desc = e.get('description','').replace('\n',' | ')[:120]
        print(f'  {e["id"]}: {e.get("name","?")}')

# 6. 4D决策模型
print()
print('=== 4D决策模型维度 ===')
for r in gsm['relationships']:
    if 'BELONGS_TO_DIMENSION' in r.get('type',''):
        print(f'  {r.get("source")} -> {r.get("target")}')

# 7. 客房打扫预案
print()
print('=== RISK 客房打扫/入住相关 ===')
for e in risk['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['打扫','入住','check','clean','housekeep','room','房态']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
