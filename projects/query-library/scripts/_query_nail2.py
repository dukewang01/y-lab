# -*- coding: utf-8 -*-
"""钉子异物详细比对"""
import json
with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)

# RCASE_7798 沙发钉子扎破手
print('=== RCASE_7798 沙发钉子扎破手案例 详情 ===')
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7798':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in gsm['relationships']:
    if r.get('source') == 'RCASE_7798' or r.get('target') == 'RCASE_7798':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

print()
# RCASE_7541 酒廊食物异物吞下
print('=== RCASE_7541 酒廊食物异物吞下案例 详情 ===')
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7541':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in gsm['relationships']:
    if r.get('source') == 'RCASE_7541' or r.get('target') == 'RCASE_7541':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

print()
# RCASE_7465B 欢迎饮料小飞虫
print('=== RCASE_7465B 欢迎饮料小飞虫案例 详情 ===')
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7465B':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in gsm['relationships']:
    if r.get('source') == 'RCASE_7465B' or r.get('target') == 'RCASE_7465B':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 食安法 相关
print()
print('=== 食安相关法律/红线 ===')
for e in gsm['entities']:
    if e.get('id','') == 'GSM_LAW_FOOD_SAFETY':
        print(f'  {e["id"]}: {e.get("name","?")}')
        print(f'  {e.get("description","")[:200]}')
        break
