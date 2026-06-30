#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Duke Wang\.config\ima\client_id').read().strip()
key = open(r'C:\Users\Duke Wang\.config\ima\api_key').read().strip()
h = {'ima-openapi-clientid': cid, 'ima-openapi-apikey': key, 'Content-Type': 'application/json'}
base = 'https://ima.qq.com/openapi/wiki/v1'

# 搜知识库名称含"酒店"的
print('=== 搜索知识库: query="酒店" ===')
r = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'酒店', 'limit':20}, timeout=10)
d = r.json()
if d.get('code') == 0:
    items = d['data'].get('info_list', [])
    for kb in items:
        print(f'  {kb["kb_name"]:20s} | {kb["content_count"]:>4}条 | {kb["creator"]} | {kb.get("description","")[:40]}')
else:
    print(f'错误: {d.get("msg")}')
    print(f'原始: {d}')

# 搜"希尔顿"
print('\n=== 搜索知识库: query="希尔顿" ===')
r2 = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'希尔顿', 'limit':20}, timeout=10)
d2 = r2.json()
if d2.get('code') == 0:
    items = d2['data'].get('info_list', [])
    for kb in items:
        print(f'  {kb["kb_name"]:20s} | {kb["content_count"]:>4}条')
else:
    print(f'错误: {d2.get("msg")}')

# 搜"收益管理"
print('\n=== 搜索知识库: query="收益管理" ===')
r3 = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'收益管理', 'limit':20}, timeout=10)
d3 = r3.json()
if d3.get('code') == 0:
    items = d3['data'].get('info_list', [])
    for kb in items:
        print(f'  {kb["kb_name"]:20s} | {kb["content_count"]:>4}条')
else:
    print(f'原始: {d3}')

# 搜更多关键词
print('\n=== 其他关键词 ===')
for q in ['餐饮管理','酒店运营','财务管理','旅游','饭店','Revenue','Management','行业报告']:
    r4 = requests.post(base+'/search_knowledge_base', headers=h, json={'query':q, 'limit':10}, timeout=10)
    d4 = r4.json()
    if d4.get('code') == 0:
        items = d4['data'].get('info_list', [])
        if items:
            names = ' | '.join(kb['kb_name'] for kb in items[:5])
            print(f'  "{q}": {names}')
    else:
        pass
