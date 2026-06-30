#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Duke Wang\.config\ima\client_id').read().strip()
key = open(r'C:\Users\Duke Wang\.config\ima\api_key').read().strip()
h = {'ima-openapi-clientid': cid, 'ima-openapi-apikey': key, 'Content-Type': 'application/json'}
base = 'https://ima.qq.com/openapi/wiki/v1'

# 可加入的知识库
r = requests.post(base+'/get_addable_knowledge_base_list', headers=h, json={'limit':20}, timeout=10)
d = r.json()
print('=== 看看有哪些知识库可以加入 ===')
print(json.dumps(d, ensure_ascii=False, indent=2)[:2000])
if d.get('code') == 0:
    items = d['data'].get('list', [])
    for kb in items[:15]:
        n = kb.get('kb_name','')
        c = kb.get('content_count',0)
        p = kb.get('creator','')
        d2 = kb.get('description','')[:50]
        print(f'  {n:20s} | {c:>4}条 | {p} | {d2}')
else:
    print('响应:', json.dumps(d, ensure_ascii=False, indent=2)[:500])
