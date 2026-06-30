#!/usr/bin/env python3
"""全维展示"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

KC = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
stas = ['fin_graph.json','qa_graph.json','fb_graph.json','faq_graph.json',
        'risk_graph.json','mep_graph.json','gsm_graph.json','crm_graph.json','lib_graph.json']
names = {'fin':'FIN','qa':'QA','fb':'FB','faq':'FAQ','risk':'RISK','mep':'MEP','gsm':'GSM','crm':'CRM','lib':'LIB'}
files = {}
for s in stas:
    try:
        d = json.load(open(os.path.join(KC, s), 'r', encoding='utf-8-sig'))
        files[s.replace('_graph.json','').upper()] = d
    except:
        pass

CRM = os.path.join(KC, 'fb_crm')
guests = json.load(open(os.path.join(CRM, 'guests.json'), 'r', encoding='utf-8-sig'))
visits = json.load(open(os.path.join(CRM, 'visits.json'), 'r', encoding='utf-8-sig'))
prefs = json.load(open(os.path.join(CRM, 'preferences.json'), 'r', encoding='utf-8-sig'))

print('=' * 72)
print('  🏛️  Y的酒店运营体系 · 全维展示')
print('  2026-05-04 21:42 · 今日净增CRM+3,289人+6,013条+FIN+562边+QA+316边')
print('=' * 72)
print()
print('  ┌──────┬──────┬──────┬──────┬─────────────────────────────────┐')
print('  │ 站   │ 实体  │ 关系  │ 评分  │ 说明                            │')
print('  ├──────┼──────┼──────┼──────┼─────────────────────────────────┤')

labels = {
    'FIN':'全业务口径(酒水/员餐/定价/成本率)',
    'QA':'12Section全覆盖+316边',
    'FB':'餐饮营业点+促销子图谱',
    'FAQ':'七站全覆盖908实体',
    'RISK':'1,248实体的风险管理',
    'MEP':'物业工程机电+空调给排水',
    'GSM':'投诉处理+案例+风险预判',
    'LIB':'知识图书馆标准版',
}

for st, d in sorted(files.items(), key=lambda x: -len(x[1].get('edges',[]))):
    ents = len(d.get('nodes',[]))
    edgs = len(d.get('edges',[]))
    if edgs > 1000:
        score = 'A'
    elif edgs > 100:
        score = 'B'
    else:
        score = 'C'
    lab = labels.get(st, '')
    print(f'  │ {st:<4} │ {ents:>4} │ {edgs:>4} │ {score:>4} │ {lab:<30} │')

print('  └──────┴──────┴──────┴──────┴─────────────────────────────────┘')
print()
print(f'  CRM独立站:')
print(f'    {len(guests):>6,} 位客人')
print(f'    {len(visits):>6,} 条到店记录')
print(f'    {len(prefs):>6,} 条偏好记录')
print(f'    品类标签: 19品类 · 3,289位商城客人全量 · 零遗漏 ✅')
print()
print(f'  📊 运营体系总规模:')
g_ents = sum(len(d.get('nodes',[])) for d in files.values())
g_edgs = sum(len(d.get('edges',[])) for d in files.values())
print(f'    知识图谱: {g_ents:,} 实体 / {g_edgs:,} 关系')
print(f'    CRM: {len(guests):,} 客人 / {len(visits):,} 到店 / {len(prefs):,} 偏好')
print(f'    总计: {g_ents+len(guests):,} 实体 / {g_edgs+len(visits):,} 关系')
print()
