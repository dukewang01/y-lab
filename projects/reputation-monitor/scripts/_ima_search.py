#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Duke Wang\.config\ima\client_id').read().strip()
key = open(r'C:\Users\Duke Wang\.config\ima\api_key').read().strip()
h = {'ima-openapi-clientid': cid, 'ima-openapi-apikey': key, 'Content-Type': 'application/json'}
base = 'https://ima.qq.com/openapi/wiki/v1'

print('IMA知识库探索')
print('='*40)

# 所有知识库
r = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'','limit':50}, timeout=10)
d = r.json()
print('\n所有知识库:')
raw = d.get('data',{})
items = raw.get('info_list',[]) or raw.get('knowledge_base_list',[]) or raw.get('list',[])
for kb in items:
    print(f'  {kb["kb_name"]:15s} | {kb["content_count"]:>3}条 | {kb["creator"]}')

# DUKE-11搜索
kid = 'SgvuxXP9ENLKXxPN0F-Ifea9BES58ehz_5kO7zOGFtg='
for kw in ['酒店','收益','餐饮','运营','希尔顿','财务','成本']:
    r2 = requests.post(base+'/search_knowledge', headers=h, json={'query':kw, 'knowledge_base_id':kid, 'cursor':''}, timeout=10)
    d2 = r2.json()
    items = d2['data'].get('info_list',[])
    content = ' | '.join(item['title'][:30] for item in items[:5]) if items else '无'
    print(f'\n"{kw}" → {len(items)}条: {content}')
