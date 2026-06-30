# -*- coding: utf-8 -*-
"""虚假宣传/工厂生产投诉查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
with open('fin_graph.json', encoding='utf-8') as f:
    fin = json.load(f)
with open('fb_graph.json', encoding='utf-8') as f:
    fb = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# 1. GSM查虚假宣传相关
print('=== GSM虚假宣传/标签相关实体 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n + eid for k in ['虚假','宣传','标签','广告','宣传','侵权','消费','矛盾','纠纷','手工','粽']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

# 2. GSM法律框架 - 消费者权益保护法 / 反不正当竞争法 / 广告法
print()
print('=== GSM法律框架 ===')
for e in gsm['entities']:
    if e.get('id','').startswith('GSM_LAW'):
        print(f'  {e["id"]}: {e.get("name","?")}')

# 3. 收费账单投诉分类详情
print()
print('=== GSM_CAT_BILLING 收费/账单争议 ===')
for r in gsm['relationships']:
    if r.get('source') == 'GSM_CAT_BILLING' or r.get('target') == 'GSM_CAT_BILLING':
        print(f'  {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 4. 查FB站粽子/节日产品
print()
print('=== FB站粽子/节日产品 ===')
for e in fb['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if '粽' in n or 'zongzi' in n or '节日' in n or '礼盒' in n:
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
        for r in fb['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 5. FIN站促销节庆产品
print()
print('=== FIN站粽子产品 ===')
for e in fin['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if '粽' in n or 'zongzi' in n or '端午' in n:
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
        for r in fin['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 6. QA品牌标准 - 标签标准
print()
print('=== QA标签/宣传相关标准 ===')
for e in qa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['标签','宣传','广告','包装','label','包装','质量','品牌']):
        print(f'  {eid}: {e.get("name","?")}')

# 7. QA 800 - 品牌形象与销售
print()
print('=== QA Section 800 品牌/销售标准 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if eid in ('QA_BS_800','QA_BS_80200'):
        print(f'  {eid}: {e.get("name","?")}')
        for r in qa['relationships']:
            if r.get('source') == eid or r.get('target') == eid:
                print(f'    {r.get("source")} --{r.get("type")}--> {r.get("target")}')

# 8. QA全部Section 800标准
print()
print('=== QA Section 800 所有标准 ===')
for e in qa['entities']:
    eid = e.get('id','')
    if eid.startswith('QA_BS_80') or eid.startswith('QA_BS_800'):
        print(f'  {eid}: {e.get("name","?")}')
