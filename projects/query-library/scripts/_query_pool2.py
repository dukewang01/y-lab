# -*- coding: utf-8 -*-
"""补查R_CMPCMP-068和SSOW"""
import json

with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

print('R_CMPCMP-068 所有关系:')
for r in risk['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    rt = r.get('type') or r.get('relation','')
    if s == 'R_CMPCMP-068' or t == 'R_CMPCMP-068':
        print(f'  {s} --[{rt}]--> {t}')

print()
print('所有SSOW流程:')
for r in risk['relationships']:
    rt = r.get('type') or r.get('relation','')
    if 'SSOW' in rt:
        print(f'  {r.get("source")} --[{rt}]--> {r.get("target")}')

print()
print('SSOW关联实体:')
ssow_ids = set()
for r in risk['relationships']:
    rt = r.get('type') or r.get('relation','')
    if 'SSOW' in rt:
        ssow_ids.add(r.get('source',''))
        ssow_ids.add(r.get('target',''))
for e in risk['entities']:
    if e.get('id','') in ssow_ids:
        print(f'  {e.get("id")}: {e.get("name","?")} (type={e.get("type","?")})')
