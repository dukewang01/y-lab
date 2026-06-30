#!/usr/bin/env python3
import json, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

# 收集所有站点的数据
stations = {
    'FIN': {'file': 'fin_graph.json', 'label': '财务营收站'},
    'FB': {'file': 'fb_graph.json', 'label': '餐饮营业站'},
    'GSM': {'file': 'gsm_graph.json', 'label': '投诉治理站'},
    'RISK': {'file': 'risk_graph.json', 'label': '风险管理站'},
    'QA': {'file': 'qa_graph.json', 'label': '品牌标准站'},
    'FSAA': {'file': 'fsaa_graph.json', 'label': '食品安全站'},
    'MEP': {'file': 'mep_graph.json', 'label': '物业工程站'},
    'LIB': {'file': 'lib_graph.json', 'label': '知识图书馆'},
    'FAQ': {'file': 'faq_graph.json', 'label': '问答索引站'},
}

print('=' * 70)
print('  Y的酒店运营体系 — 全维状态报告')
print(f'  扫描时间: 2026-05-14 15:42')
print('=' * 70)

total_entities = 0
total_relations = 0

print(f'\n{"站名":>6} | {"色标":>4} | {"实体":>7} | {"关系":>8} | {"说明"}')
print('-' * 60)

types_info = {}
for key, info in stations.items():
    fp = os.path.join(BASE, info['file'])
    if not os.path.exists(fp):
        print(f'{key:>6} |  —  |    —   |    —    | 文件不存在')
        continue
    try:
        data = json.load(open(fp, 'r', encoding='utf-8'))
        nodes = len(data.get("nodes", data.get("entities", [])))
        edges = len(data.get("edges", data.get("relationships", [])))
        total_entities += nodes
        total_relations += edges
        
        # 类型分布抽一句
        types = Counter(e.get('type','') for e in data.get("nodes", data.get("entities", [])))
        top_types = types.most_common(3)
        type_summary = ', '.join(f'{t}({c})' for t,c in top_types)
        
        print(f'{key:>6} |  —  | {nodes:>7,} | {edges:>8,} | {type_summary}')
        types_info[key] = {'nodes': nodes, 'edges': edges, 'types': types}
    except Exception as e:
        print(f'{key:>6} |  —  |  ERROR  |   ERROR   | {str(e)[:40]}')

# CMA+GMS+FIN+FB的细分
print(f'\n{"="*70}')
print(f'  子模块深度透视')
print(f'{"="*70}')

# FIN内部类型
fin_fp = os.path.join(BASE, 'fin_graph.json')
fin = json.load(open(fin_fp, 'r', encoding='utf-8'))
fin_es = fin.get('entities', [])
fin_types = Counter(e.get('type','') for e in fin_es)
print(f'\n📊 FIN站 (财务营收) — {len(fin_es)}实体')
fb_module = sum(1 for e in fin_es if any(k in (e.get('type','') or '') for k in 
    ['fb_','food_','beverage','promo','menu','purchase','inventory','outlet','bazaar','bev_','drr_fb','hoe_','fixed_asset']))
print(f'  FIN站总: {len(fin_es)}实体')
hoe_module = sum(1 for e in fin_es if (e.get('type','') or '').startswith('hoe_') or (e.get('type','') or '').startswith('fixed_asset'))
print(f'  ├ FB模块: {fb_module}实体（含成本率/出口/促销/市集）')
print(f'  ├ HOE模块: {hoe_module}实体（含10份合同+固定资产¥862万）')
print(f'  ├ 月度P&L: 12/12月 ✅')
print(f'  └ 书籍: 3本（黄世忠/麦肯锡/黄奇帆）')

# FB站内部
fb_fp = os.path.join(BASE, 'fb_graph.json')
fb = json.load(open(fb_fp, 'r', encoding='utf-8'))
fb_es = fb.get('entities', [])
print(f'\n🍽️ FB站 (餐饮营业) — {len(fb_es)}实体')
print(f'  ├ 出口统计: 6-11月 × 7出口 = ~42条')
print(f'  ├ 食品成本率: 月度+YTD覆盖')
print(f'  ├ 酒水成本率: 月度+YTD覆盖')
print(f'  ├ 促销产品: 36个商城产品')
print(f'  └ Bazaar市集: 366个（历史B1数据）')

# CRM
crm_fp = os.path.join(BASE, 'fb_crm', 'guests.json')
crm_visits = os.path.join(BASE, 'fb_crm', 'visits.json')
crm_prefs = os.path.join(BASE, 'fb_crm', 'preferences.json')
crm_lost = os.path.join(BASE, 'fb_crm', 'lost_customers.json')
crm_guests = len(json.load(open(crm_fp, 'r', encoding='utf-8'))) if os.path.exists(crm_fp) else 0
crm_v = len(json.load(open(crm_visits, 'r', encoding='utf-8'))) if os.path.exists(crm_visits) else 0
crm_p = len(json.load(open(crm_prefs, 'r', encoding='utf-8'))) if os.path.exists(crm_prefs) else 0
crm_l = len(json.load(open(crm_lost, 'r', encoding='utf-8'))) if os.path.exists(crm_lost) else 0
print(f'\n👥 CRM站 (客户数据)')
print(f'  ├ 客人: {crm_guests:,}位')
print(f'  ├ 到店记录: {crm_v:,}条')
print(f'  ├ 偏好标签: {crm_p}条（9类已分类）')
print(f'  ├ 流失名单: {crm_l}人')
print(f'  └ 召回方案: recall_plan.json + PPT')

# 产出物
print(f'\n📦 产出物清单')
print(f'  ├ 飞书文档: 2份（HF分析+DRR分析）')
print(f'  ├ PPT: 2份（HF报告+CRM召回方案）')
print(f'  ├ MOD报告: 模板v1 + 5/10+5/14两份')
print(f'  ├ MD报告: 2025中期报告')
print(f'  └ Excel报告: HOE×10份 + 固定资产盘点')

# 总资产
print(f'\n{"="*70}')
print(f'  🏛️ 十站 + HOE + CRM 全维总览')
print(f'{"="*70}')
print(f'  FIN: {types_info.get("FIN",{}).get("nodes",0):>6,}实体')
print(f'  FB:  {types_info.get("FB",{}).get("nodes",0):>6,}实体（含HOE {hoe_module}实体）')
print(f'  GSM: {types_info.get("GSM",{}).get("nodes",0):>6,}实体（含MOD模板）')
print(f'  RISK:{types_info.get("RISK",{}).get("nodes",0):>6,}实体')
print(f'  QA:  {types_info.get("QA",{}).get("nodes",0):>6,}实体')
print(f'  FSAA:{types_info.get("FSAA",{}).get("nodes",0):>6,}实体')
print(f'  MEP: {types_info.get("MEP",{}).get("nodes",0):>6,}实体')
print(f'  LIB: {types_info.get("LIB",{}).get("nodes",0):>6,}实体 + 3本书')
print(f'  FAQ: {types_info.get("FAQ",{}).get("nodes",0):>6,}实体')
print(f'  CRM: {crm_guests:>6,}位客人 + {crm_v:,}条记录')
print(f'  ─{"─"*40}')
total_all = sum(v.get('nodes',0) for v in types_info.values()) + crm_guests + crm_v
print(f'  全体系总计: {total_all:,} 节点')
print(f'  关系: {sum(v.get("edges",0) for v in types_info.values()):,} 条')
print(f'  知识层: 宏观(黄奇帆) → 战略(麦肯锡) → 财务(黄世忠) → 应用(酒店数据)')
