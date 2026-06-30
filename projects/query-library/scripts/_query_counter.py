# -*- coding: utf-8 -*-
"""反向报警/维权路径查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

# 1. 排查现有标签/打假相关实体
print('=== 现有打假/标签相关 ===')
for e in risk['entities']:
    eid = e.get('id','')
    if 'LABEL' in eid:
        print(f'  {eid}: {e.get("name","?")}')
        desc = e.get('description','')
        print(f'    {desc[:300]}')

print()
# 2. R_CMPCMP-099 标签预案
print('=== R_CMPCMP-099 标签预案全貌 ===')
for e in risk['entities']:
    if e.get('id','') == 'R_CMPCMP-099':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in risk['relationships']:
    if r.get('source') == 'R_CMPCMP-099' or r.get('target') == 'R_CMPCMP-099':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

print()
# 3. 法律框架里关于勒索/敲诈的
print('=== 法律框架中可反向维权的 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    if any(k in n for k in ['敲诈','勒索','诈骗','欺诈','诽谤','诬告']):
        print(f'  {e["id"]}: {e.get("name","?")}')
        print(f'    {e.get("description","")[:200]}')
