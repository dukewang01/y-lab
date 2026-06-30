# -*- coding: utf-8 -*-
"""等房案例详情"""
import json
with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)

print('=== RCASE_7794 等房时间过长投诉案例 详情 ===')
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7794':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break

print()
print('关系：')
for r in gsm['relationships']:
    if r.get('source') == 'RCASE_7794' or r.get('target') == 'RCASE_7794':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')
