# -*- coding: utf-8 -*-
"""早餐拖鞋滑倒 - 关键案例和SSOW"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# 1. RCASE_7365 - 最接近的案例
print('=== RCASE_7365 赤脚进餐厅经典案例 ===')
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7365':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print('关系：')
for r in gsm['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    if s == 'RCASE_7365' or t == 'RCASE_7365':
        print(f'  {s} --{r.get("type")}--> {t}')

# 2. SCENE_SLIPPER在GSM站（结构性缺失）
print()
print('=== GSM站 SCENE_SLIPPER 关系 ===')
found = False
for r in gsm['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    if s == 'SCENE_SLIPPER' or t == 'SCENE_SLIPPER':
        print(f'  {s} --{r.get("type")}--> {t}')
        found = True
if not found:
    print('  ❌ 在GSM站中无关系——结构性缺失')

# 3. 早餐时段滑倒 - 检查现有的SSOW
print()
print('=== 早餐滑倒的SSOW路径（R_CMPCMP-068已补SCENE_SLIP） ===')
print('R_CMPCMP-068 -> SCENE_SLIP -> 关键SSOW:')
for r in risk['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    rt = r.get('type')
    if s == 'R_CMPCMP-068' and rt == 'HAS_SSOW':
        print(f'  R_CMPCMP-068 --{rt}--> {t}')
        # 再查下一层SSOW
        for r2 in risk['relationships']:
            s2 = r2.get('source','')
            if s2 == t and 'SSOW' in r2.get('type',''):
                print(f'    {s2} --{r2.get("type")}--> {r2.get("target")}')

# 4. 相关案例完整列表
print()
print('=== 穿拖鞋/滑倒破皮类案例 ===')
for e in gsm['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if e.get('type') == 'risk_case' and any(k in n for k in ['滑倒','拖鞋','赤脚','slip','摔倒','磕破','破皮']):
        print(f'  {eid}: {e.get("name","?")}')
        # 找赔偿等级
        for r in gsm['relationships']:
            if r.get('source') == eid:
                print(f'    -> {r.get("type")} {r.get("target")}')

# 5. QA早餐时段地面安全标准
print()
print('=== QA早餐安全/防滑检查项 ===')
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
for e in qa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['防滑','地面','clean','清洁','滑','slip','安全','湿']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
