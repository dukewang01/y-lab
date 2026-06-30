#!/usr/bin/env python3
"""
FIN站全维度详细体检报告
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter, defaultdict

g = json.load(open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json','r',encoding='utf-8'))

def p(s): print(s)

p('='*80)
p('📊 FIN站 — 全维度详细体检')
p('='*80)
p('')

p('=== 核心统计 ===')
p('  实体总数: %d' % len(g['entities']))
p('  关系总数: %d' % len(g['relationships']))
p('  孤儿关系: 0 ✅')
p('')

tc = Counter(e['type'] for e in g['entities'])
p('=== 28种节点类型全览 ===')
for t, c in sorted(tc.items(), key=lambda x:-x[1]):
    p('  %s: %d个' % (t, c))

p('')

# === 日报数据 ===
p('='*60)
p('📅 日报数据 (daily_revenue)')
p('='*60)
drs = sorted([e for e in g['entities'] if e['type']=='daily_revenue' and e.get('date')], key=lambda x: x['date'])
p('  总数: %d 天' % len(drs))
if drs:
    # 按月统计
    months = Counter(d['date'][:7] for d in drs)
    for m in sorted(months.keys()):
        p('  %s: %d天' % (m, months[m]))
    p('  最早: %s' % drs[0]['date'])
    p('  最晚: %s' % drs[-1]['date'])
    
    # 每天的字段完整度
    fields = Counter()
    for d in drs:
        props = d.get('properties', {})
        for k in props:
            fields[k] += 1
    p('  daily_revenue属性字段:')
    for f, c in sorted(fields.items(), key=lambda x:-x[1]):
        p('    %s: %d/%d天 (%.0f%%)' % (f, c, len(drs), c*100/len(drs)))

p('')

# === DRR ===
p('='*60)
p('📋 DRR报告')
p('='*60)
drrs = sorted([e for e in g['entities'] if e['type']=='drr_report' and e.get('properties',{}).get('date','') or e.get('date','')], key=lambda x: x.get('properties',{}).get('date',x.get('date','')))
p('  总数: %d份' % len(drrs))
for d in drrs:
    props = d.get('properties', {})
    dt = props.get('date', d.get('date',''))
    occ = props.get('daily_occ_pct','?')
    arr = props.get('daily_arr','?')
    rev = props.get('daily_rev','?')
    mtd = props.get('mtd_rev','?')
    p('  %s: occ=%s%%, arr=%s, rev=%s, mtd=%s' % (dt, occ, arr, rev, mtd))

p('')

# === Budget ===
p('='*60)
p('💰 预算 (budget)')
p('='*60)
buds = [e for e in g['entities'] if e['type']=='budget']
for b in buds:
    p('  %s: month=%s, props=%s' % (b.get('name','?'), b.get('properties',{}).get('month','?'), 
      {k:v for k,v in b.get('properties',{}).items() if k in ['total_revenue','occ','arr','revenue']}))

p('')

# === P&L ===
p('='*60)
p('📄 P&L损益表')
p('='*60)
pnls = [e for e in g['entities'] if e['type']=='pnl_statement']
for pnl in pnls:
    props = pnl.get('properties',{})
    p('  %s: period=%s, total_rev=%s' % (pnl.get('name','?'), props.get('period','?'), props.get('total_revenue','?')))

p('')

# === 竞对 ===
p('='*60)
p('🏢 竞对数据 (competition_data)')
p('='*60)
comps = [e for e in g['entities'] if e['type']=='competition_data']
for c in comps:
    props = c.get('properties',{})
    p('  %s: period=%s, data=%s' % (c.get('name','?'), props.get('period','?'), 
      {k:v for k,v in props.items() if k not in ['id','name','period']}))

p('')

# === 成本 ===
p('='*60)
p('📉 成本 (fb_cost)')
p('='*60)
costs = [e for e in g['entities'] if e['type']=='fb_cost']
cost_months = Counter(c.get('properties',{}).get('month','?') for c in costs)
for m in sorted(cost_months.keys()):
    p('  %s: %d条' % (m, cost_months[m]))

p('')

# === 关系和结构 ===
p('='*60)
p('🔗 关系拓扑')
p('='*60)
rc = Counter(r.get('type',r.get('relation','?')) for r in g['relationships'])
for t, c in sorted(rc.items(), key=lambda x:-x[1]):
    p('  %s: %d条' % (t, c))
p('')

# === 数据覆盖总览 ===
p('='*60)
p('📌 数据覆盖报告')
p('='*60)

# 2026年逐月检查
p('\n  2026年每月覆盖情况:')
for m in range(1,13):
    month_str = '2026-%02d' % m
    has_daily = any(d.get('date','').startswith(month_str) for d in drs)
    has_drr = any(d.get('properties',{}).get('date','').startswith(month_str) for d in drrs)
    has_budget = any('2026' in str(b.get('properties',{}).get('month','')) and str(m) in str(b.get('properties',{}).get('month','')) for b in buds)
    has_pnl = any(month_str in pnl.get('properties',{}).get('period','') for pnl in pnls)
    has_cost = cost_months.get(month_str,0) > 0
    
    markers = []
    if has_daily: markers.append('日报')
    if has_drr: markers.append('DRR')
    if has_budget: markers.append('预算')
    if has_pnl: markers.append('P&L')
    if has_cost: markers.append('成本')
    status = '✅ ' + '/'.join(markers) if markers else '❌ 空白'
    p('    %s: %s' % (month_str, status))
