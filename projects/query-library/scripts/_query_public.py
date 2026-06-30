# -*- coding: utf-8 -*-
"""补知识缺口：负面舆情/网络曝光预防机制"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

# ====== 现有实体中有没有舆情相关的 ======
print('=== 现有GSM舆情相关实体 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n + eid for k in ['舆情','曝光','抖音','社交','媒体','social','video','短视频','网络','投诉升级','曝光']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
        for r in gsm['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

print()
print('=== 现有RISK舆情相关 ===')
for e in risk['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['舆情','曝光','社交','社会','media','短视频','网爆']):
        print(f'  {eid}: {e.get("name","?")}')

print()
print('=== 现有QA舆情相关 ===')
for e in qa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['舆情','曝光','社交','社会','social','危机','公关','危机']):
        print(f'  {eid}: {e.get("name","?")}')
