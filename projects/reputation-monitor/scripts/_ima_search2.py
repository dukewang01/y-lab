#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Y\.config\ima\client_id').read().strip()
key = open(r'C:\Users\Y\.config\ima\api_key').read().strip()
h = {'ima-openapi-clientid': cid, 'ima-openapi-apikey': key, 'Content-Type': 'application/json'}
base = 'https://ima.qq.com/openapi/wiki/v1'

r = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'','limit':20}, timeout=10)
d = r.json()
if d.get('code') != 0:
    print('错误:', d.get('msg'))
    exit()

all_kb = d['data']['info_list']
print('所有知识库:')
for kb in all_kb:
    print(f'  {kb["kb_name"]:15s} | {kb["content_count"]:>3}�?| {kb["creator"]}')

# DUKE-11
kid = 'SgvuxXP9ENLKXxPN0F-Ifea9BES58ehz_5kO7zOGFtg='
for kw in ['酒店','收益','餐饮','运营','希尔�?,'财务','成本','管理','数据','分析']:
    r2 = requests.post(base+'/search_knowledge', headers=h, json={'query':kw, 'knowledge_base_id':kid, 'cursor':''}, timeout=10)
    d2 = r2.json()
    items = d2['data'].get('info_list',[])
    if items:
        titles = [it['title'][:25] for it in items[:5]]
        print(f'\n"{kw}" �?{len(items)}�? {" | ".join(titles)}')
    else:
        print(f'\n"{kw}" �?0�?)
