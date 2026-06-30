# -*- coding: utf-8 -*-
"""补知识缺口：谈判协议/免责文件/保密协议机制"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

# 现有有没有协议相关的
print('=== 现有RISK协议/文件/条款相关 ===')
for e in risk['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id', '')
    desc = (e.get('description') or '').lower()
    if any(k in n + desc for k in ['协议','免责','保密','NDA','agreement','回执','确认函','签字','承诺书']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
        print(f'    {e.get("description","")[:200]}')

print()
print('=== GSM法律框架相关 ===')
for e in gsm['entities']:
    if 'GSM_LAW' in e.get('id',''):
        print(f'  {e["id"]}: {e.get("name","?")}')
