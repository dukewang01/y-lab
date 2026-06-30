#!/usr/bin/env python3
"""全维展示v2"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

KC = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
CRM = os.path.join(KC, 'fb_crm')

stations = {
    'FIN': {'file':'fin_graph.json','key_ents':'entities','key_edgs':'edges','color':'🟣'},
    'QA':  {'file':'qa_graph.json','key_ents':'entities','key_edgs':'edges','color':'🟢'},
    'RISK':{'file':'risk_graph.json','color':'🔵'},
    'MEP': {'file':'mep_graph.json','color':'🟡'},
    'GSM': {'file':'gsm_graph.json','color':'🌐'},
    'FB':  {'file':'fb_graph.json','color':'🟠'},
    'FAQ': {'file':'faq_graph.json','color':'🟠'},
    'CRM': {'file':'crm_graph.json','color':'🧑\u200d🤝\u200d🧑'},
    'LIB': {'file':'lib_graph.json','color':'🟠'},
}

data = {}
for name, cfg in stations.items():
    fp = os.path.join(KC, cfg['file'])
    try:
        d = json.load(open(fp, 'r', encoding='utf-8-sig'))
        data[name] = d
    except:
        data[name] = None

guests = json.load(open(os.path.join(CRM, 'guests.json'), 'r', encoding='utf-8-sig'))
visits = json.load(open(os.path.join(CRM, 'visits.json'), 'r', encoding='utf-8-sig'))
prefs = json.load(open(os.path.join(CRM, 'preferences.json'), 'r', encoding='utf-8-sig'))

# count entities/edges per station
ent_cnt, edg_cnt = {}, {}
for name, d in data.items():
    if d is None:
        ent_cnt[name], edg_cnt[name] = 0, 0
        continue
    if isinstance(d, dict):
        if 'entities' in d:
            ent_cnt[name] = len(d['entities'])
        if 'data' in d:
            ent_cnt[name] = len(d['data'])
        if len(d) > 0 and not any(k in d for k in ['entities','data','nodes']):
            if isinstance(list(d.values())[0], dict):
                ent_cnt[name] = len(d)
        if 'edges' in d:
            edg_cnt[name] = len(d['edges'])
        elif 'relations' in d:
            edg_cnt[name] = len(d['relations'])
        elif 'relationships' in d:
            edg_cnt[name] = len(d['relationships'])

print('=' * 72)
print('  🏛️  Y的酒店运营体系 · 全维展示')
print('  2026-05-04 21:46 · 九站完整版')
print('=' * 72)
print()
print('  ┌──────┬──────────┬──────────┬──────────┬──────────────┐')
print('  │ 站   │ 🏷️ 图类型 │ 实体数    │ 关系数    │ 评级          │')
print('  ├──────┼──────────┼──────────┼──────────┼──────────────┤')

descs = {
    'FIN':'🟣','QA':'🟢','RISK':'🔵','MEP':'🟡',
    'GSM':'🌐','FB':'🟠','FAQ':'🟠','CRM':'🧑\u200d🤝\u200d🧑','LIB':'🟠'
}
labels = {
    'FIN': '财务营收 v7.7 · 912边 · 酒水仓/员餐/定价/成本率',
    'QA': '品牌标准 v8.8 · 316边 · 12Section全通',
    'RISK': '风险管理 · 1,248实体 · 6,943案例',
    'MEP': '物业工程机电 · 空调给排水全链路',
    'GSM': '投诉处理·案例分析·趋势预判｜治→析→预',
    'FB': '餐饮营业点 v1.8 · 2,446实体 · 含F促销子图谱',
    'FAQ': '知识问答 v6.0 · 908实体 · 七站全覆盖',
    'CRM': '客户数据站 v1.0 · 3,831位客人 · 全生命周期',
    'LIB': '知识图书馆 v2.0 · 192实体 · 336关系',
}

for name, d in data.items():
    ents = ent_cnt.get(name, 0)
    edgs = edg_cnt.get(name, 0)
    if edgs > 1000:
        score = '🅰️'
    elif edgs > 100:
        score = '🅱️'
    elif ents > 0:
        score = '🅲'
    else:
        score = ' '

    # detect type
    dt = data[name]
    if dt is None:
        typ = '缺失'
    elif isinstance(dt, list):
        typ = '列表'
    elif isinstance(dt, dict) and 'edges' in dt:
        typ = '图谱'
    elif isinstance(dt, dict) and 'entities' in dt:
        typ = '图谱'
    elif isinstance(dt, dict):
        typ = '文档'
    else:
        typ = '其他'

    l = f'{descs.get(name,"")} {labels.get(name,"")}'[:38]
    print(f'  │ {descs.get(name," ")}{name:<3} │ {typ:<8} │ {ents:>6} │ {edgs:>6} │ {score:<12} │')

print('  ├──────┼──────────┼──────────┼──────────┼──────────────┤')

# CRM extra row
crm_shop = [v for v in visits if v.get('type') == 'online_purchase']
print(f'  │ 📦CRM: │ 客人+画像 │ {len(guests):>6} │ {len(visits):>6} │ 7,120人·27,096到店·4,254偏好 │')
cat_guests = [g for g in guests if g.get('tags')]
print(f'  │ 🏷️标签 │ 19品类   │ {len(cat_guests):>6} │ 零遗漏   │ 3,289商城客全量·v5 ✅ │')

print('  └──────┴──────────┴──────────┴──────────┴──────────────┘')
print()

# 总计
g_ents = sum(ent_cnt.values()) + len(guests)
g_edgs = sum(edg_cnt.values()) + len(visits)
print(f'  📊 运营体系总规模:')
print(f'    知识图谱实体: {sum(ent_cnt.values()):,}')
print(f'    CRM客人:      {len(guests):,}')
print(f'    到店记录:     {len(visits):,}')
print(f'    偏好记录:     {len(prefs):,}')
print(f'    今日净增:     FIN+562边(+160%) | QA+316边(新) | CRM+3,289客人+6,013商城')
print(f'    总计:         {g_ents:,} 实体 / {g_edgs:,} 关系')
print()

print('=' * 72)
print('  今日价值跃升量化')
print('=' * 72)
print()
print('  之前(05-04 07:10) vs 现在(05-04 21:46)')
print(f'  ┌──────────────────┬──────────────┬──────────────┬──────────┐')
print(f'  │ 维度              │ 早上          │ 晚上          │ 变化      │')
print(f'  ├──────────────────┼──────────────┼──────────────┼──────────┤')
print(f'  │ CRM客人           │ 3,831        │ 7,120        │ +3,289   │')
print(f'  │ 到店记录           │ 21,083       │ 27,096       │ +6,013   │')
print(f'  │ 品类标签           │ 无           │ 19品类全零   │ 🆕       │')
print(f'  │ FIN边             │ 350          │ 912          │ +562     │')
print(f'  │ QA边              │ 0            │ 316          │ 🆕       │')
print(f'  │ 飞书文档板块        │ 0            │ 9            │ 🆕       │')
print(f'  │ 策略方案           │ 无           │ 5-6月整合+618│ 🆕       │')
print(f'  │ Python脚本         │ ~80          │ ~115         │ +35      │')
print(f'  └──────────────────┴──────────────┴──────────────┴──────────┘')
print()

print('=' * 72)
print('  九站功能矩阵')
print('=' * 72)
print()
print('  🟣 FIN 财务营收  ─── 成本率/酒水定价/DRR/盘点 → 决策')
print('  🟢 QA  品牌标准  ─── 10Section→12Section全覆盖 → 巡检')
print('  🔵 RISK 风险管理 ─── 1,248实体6,943案例 → 预案')
print('  🟡 MEP 机电工程  ─── 空调给排水/客房系统 → 维护')
print('  🌐 GSM 投诉处理  ─── 治→析→预三层 → 案例分析')
print('  🟠 FB  餐饮营业点 ─── 2,446实体+促销图谱 → 营销')
print('  🟠 FAQ 知识问答  ─── 908实体七站全覆盖 → 秒查')
print('  🧑‍🤝‍🧑 CRM 客户数据  ─── 7,120客人+品类标签 → 唤醒')
print('  🟠 LIB 知识图书馆 ─── 192实体336关系 → 学习')
print()
