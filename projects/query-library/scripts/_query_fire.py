# -*- coding: utf-8 -*-
"""Open餐厅自助晚餐酒精灯爆炸着火查询"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)
with open('fsaa_graph.json', encoding='utf-8') as f:
    fsaa = json.load(f)

def rel_out(data, eid):
    return [(r.get('type') or r.get('relation',''), r.get('target')) for r in data['relationships'] if r.get('source') == eid]

def rel_in(data, eid):
    return [(r.get('type') or r.get('relation',''), r.get('source')) for r in data['relationships'] if r.get('target') == eid]

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# ---- 1. GSM - 查找火灾/爆炸/烧伤相关 ----
for kw in ['火','烧','烫','烧伤','灼伤','酒精','爆炸','灯','ignition','burn','fire','chafing','open餐厅','open kitchen','自助','晚餐','热菜']:
    for e in gsm['entities']:
        n = (e.get('name') or '').lower()
        eid = e.get('id','')
        etype = e.get('type','')
        if kw in n:
            print(f'[GSM] {eid}: {e.get("name","?")} (type={etype})')

print('\n---分隔---\n')

# ---- 2. 在RISK中查火灾/爆炸/烧伤 ----
for kw in ['火','烧','烧伤','灼伤','酒精','爆炸','灯','ignition','burn','fire','chafing']:
    for e in risk['entities']:
        n = (e.get('name') or '').lower()
        eid = e.get('id','')
        if kw in n:
            print(f'[RISK] {eid}: {e.get("name","?")} (type={e.get("type","?")})')

print('\n---RISK火灾类预案---\n')

# 看有哪些火灾类的预案（CMPCMP编号）
for e in risk['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if '火' in n and eid.startswith('R_CMP'):
        print(f'{eid}: {e.get("name","?")}')
        for rt, tgt in rel_out(risk, eid):
            tn = name_of(risk, tgt)
            print(f'  → [{rt}] {tgt}: {tn}')
        print()

print('\n---FSAA 明火/自助餐/保温相关---')
for e in fsaa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['火','酒精','保温','热菜','chafing','自助']):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

print('\n---QA 火灾/安全相关标准---')
for e in qa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['fire','火','烧伤','酒精','明火','open餐厅','自助']) and eid.startswith('QA'):
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')

print('\n---QA Section 900 安全相关标准---')
for e in qa['entities']:
    eid = e.get('id','')
    if eid.startswith('QA_BS_90'):
        print(f'  {eid}: {e.get("name","?")}')

print('\n---FSAA 防火/火灾相关NC---')
for e in fsaa['entities']:
    n = (e.get('name') or '').lower()
    eid = e.get('id','')
    if any(k in n for k in ['火','酒精','保温']) or 'NC_FIRE' in eid or 'NC_ALCOHOL' in eid:
        print(f'  {eid}: {e.get("name","?")} (type={e.get("type","?")})')
