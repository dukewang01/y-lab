#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Y\.config\ima\client_id').read().strip()
key = open(r'C:\Users\Y\.config\ima\api_key').read().strip()
h = {'ima-openapi-clientid': cid, 'ima-openapi-apikey': key, 'Content-Type': 'application/json'}
base = 'https://ima.qq.com/openapi/wiki/v1'

r = requests.post(base+'/search_knowledge_base', headers=h, json={'query':'','limit':50}, timeout=10)
print('原始响应:')
print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:2000])
