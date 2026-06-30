#!/usr/bin/env python3
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

cid = open(r'C:\Users\Duke Wang\.config\ima\client_id','r').read().strip()
key = open(r'C:\Users\Duke Wang\.config\ima\api_key','r').read().strip()

def ima_api(path, body_dict):
    url = f'https://ima.qq.com/{path}'
    headers = {
        'ima-openapi-clientid': cid,
        'ima-openapi-apikey': key,
        'Content-Type': 'application/json'
    }
    r = requests.post(url, headers=headers, json=body_dict, timeout=10)
    return r.json()

# 搜全部知识库
print('=== 所有知识库 ===')
res = ima_api('openapi/wiki/v1/search_knowledge_base', {'query': '', 'cursor': '', 'limit': 50})
if res.get('code') != 0:
    print('错误:', res.get('msg',''))
else:
    for kb in res['data']['info_list']:
        name = kb['kb_name']
        cnt = kb['content_count']
        creator = kb['creator']
        desc = kb.get('description','') or '(无描述)'
        print(f'  {name:15s} | {cnt:>3}条内容 | {creator} | {desc}')

# 在DUKE-11里搜索酒店相关
print(f'\n=== 搜索DUKE-11知识库: "酒店" ===')
kb_id = 'SgvuxXP9ENLKXxPN0F-Ifea9BES58ehz_5kO7zOGFtg='
# 先查查这个KB详情
res2 = ima_api('openapi/wiki/v1/get_knowledge_base', {'ids': [kb_id]})
if res2.get('code') == 0:
    info = res2['data']['infos'].get(kb_id, {})
    print(f'  名称: {info.get(\"name\",\"\")}')
    print(f'  内容数: {info.get(\"content_count\",\"\")}')
    print(f'  推荐问题: {info.get(\"recommended_questions\",\"\")}')

# 搜索
print(f'\n=== 搜索: "酒店" ===')
res3 = ima_api('openapi/wiki/v1/search_knowledge', {'query': '酒店', 'knowledge_base_id': kb_id, 'cursor': ''})
if res3.get('code') == 0:
    items = res3['data'].get('info_list', [])
    print(f'  找到: {len(items)} 条')
    for item in items[:10]:
        title = item.get('title','')
        highlight = item.get('highlight_content','')[:80]
        print(f'    {title}')
        if highlight:
            print(f'      {highlight}')
else:
    print(f'  搜索失败: {res3}')

# 搜收益管理
print(f'\n=== 搜索: "收益管理" ===')
res4 = ima_api('openapi/wiki/v1/search_knowledge', {'query': '收益管理', 'knowledge_base_id': kb_id, 'cursor': ''})
if res4.get('code') == 0:
    items = res4['data'].get('info_list', [])
    print(f'  找到: {len(items)} 条')
    for item in items[:10]:
        print(f'    {item.get(\"title\",\"\")}')
