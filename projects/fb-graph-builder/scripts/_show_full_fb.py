#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# FB相关
fb_types = ['fb_','food_','beverage','promo','menu','purchase','inventory','outlet','bazaar','bev_','drr_fb']
fb = [e for e in es if any(k in (e.get('type','') or '') for k in fb_types)]
print(f'FB模块总实体: {len(fb)}')
print()

# 维度展示
from collections import defaultdict

sections = defaultdict(list)
for e in fb:
    t = e.get('type','unknown')
    sections[t].append(e)

header = True
for t in sorted(sections.keys()):
    items = sections[t]
    desc = {
        'bazaar_daily': '美食市集 逐日销售',
        'bazaar_menu_item': '美食市集 菜单品项',
        'bazaar_monthly': '美食市集 月度汇总',
        'fb_outlet_stats': '各出口月度营收统计',
        'fb_cost': '出口食品成本率',
        'beverage_cost_report': '出口酒水成本率',
        'promotion_product': '商城促销产品',
        'fb_menu_engineering': '菜单工程分析',
        'fb_inventory': '库存/周转数据',
        'fb_promotion_roi': '促销ROI分析',
        'fb_category': 'FB分类',
        'fb_outlet_category': '出口分类',
        'fb_seasonal_promotion': '季节性促销',
        'fb_forecast_monthly': 'FB月度展望',
        'food_cost_report': '食品成本报告',
        'outlet': '出口主节点',
        'bev_outlet': '酒水出口',
        'drr_fb_daily': 'FB日报',
        'fb_purchase_analysis': '采购分析',
        'fin_month': '月度F&B损益',
        'fin_year': '年度F&B汇总',
        'fin_report': 'FB品牌费用/其他',
    }.get(t, t)
    
    # 查看数据丰富度
    has_data = 0
    for item in items:
        if any(v for k,v in item.items() if k not in ('id','type','label','source','hotel') and v):
            has_data += 1
    
    pct = has_data/len(items)*100 if items else 0
    bar = '#' * int(pct/5)
    space = ' ' * (20 - int(pct/5))
    
    print(f'{desc:20s} | {len(items):>4d} 个 | 数据填充率 {pct:>5.1f}% | [{bar}{space}]')

# ====== 月度F&B数据全景 ======
print(f'\n{"="*60}')
print(f'  月度F&B损益一览')
print(f'{"="*60}')
print(f'{"月份":>6} | {"FB收入":>8} | {"FB利润":>8} | {"利润率":>7} | {"各出口数据":>12}')
print('-'*60)
months_order = [f'MONTH_2025_{m:02d}' for m in range(1,13)]
labels = {f'MONTH_2025_{m:02d}':f'{m}月' for m in range(1,13)}
for mid in months_order:
    for e in es:
        if e.get('id') == mid:
            fb_rev = e.get('fb_rev',0) or 0
            fb_profit = e.get('fb_profit',0) or 0
            fb_margin = e.get('fb_margin',0) or 0
            # 检查该月有多少出口数据
            outlet_count = sum(1 for x in fb if x.get('type')=='fb_outlet_stats' and x.get('month')==mid.replace('MONTH_','').replace('_','-'))
            outlet_str = f'{outlet_count}个出口' if outlet_count > 0 else '-'
            rev_str = f'{fb_rev/10000:.1f}万' if fb_rev else '-'
            profit_str = f'{fb_profit/10000:.1f}万' if fb_profit else '-'
            margin_str = f'{fb_margin:.1f}%' if fb_margin else '-'
            print(f'{labels[mid]:>6} | {rev_str:>8} | {profit_str:>8} | {margin_str:>7} | {outlet_str:>12}')
            break

# ====== 出口成本率矩阵 ======
print(f'\n{"="*60}')
print(f'  各出口食品成本率月度矩阵 (%)')
print(f'{"="*60}')
outlet_order = ['OPEN','YUXI','BANQUET','BACIO','ROOM_SVC','YUAN','BEER']
month_labels = ['6月','7月','8月','9月','10月','11月']
print(f'{"出口":>10}', end='')
for ml in month_labels:
    print(f' | {ml:>5}', end='')
print()
print('-' * (12 + len(month_labels)*8))

for o in outlet_order:
    print(f'{o:>10}', end='')
    for mid in ['06','07','08','09','10','11']:
        v = '-'
        for e in es:
            if e.get('type')=='fb_outlet_stats' and e.get('outlet')==o and e.get('month')==f'2025-{mid}':
                p = e.get('food_cost_pct',0) or 0
                if p: v = f'{p:.1f}'
                break
        print(f' | {v:>5}', end='')
    print()

# ====== 酒水成本率 ======
print(f'\n{"="*60}')
print(f'  各出口酒水成本率 (%)')
print(f'{"="*60}')
print(f'{"出口":>10}', end='')
for ml in ['6月','7月','11月','YTD']:
    print(f' | {ml:>5}', end='')
print()
print('-' * (12 + 4*8))

for o in outlet_order:
    print(f'{o:>10}', end='')
    for mid in ['06','07','11']:
        v = '-'
        for e in es:
            if e.get('type')=='beverage_cost_report' and e.get('outlet')==o and e.get('month')==f'2025-{mid}':
                p = e.get('bev_cost_pct',0) or 0
                if p: v = f'{p:.1f}'
                break
        print(f' | {v:>5}', end='')
    # YTD
    v = '-'
    for e in es:
        if e.get('type')=='beverage_cost_report' and e.get('outlet')==o and e.get('period')=='YTD_11':
            p = e.get('bev_cost_pct',0) or 0
            if p: v = f'{p:.1f}'
            break
    print(f' | {v:>5}')

# 年度汇总
total_fb_rev = sum(e.get('fb_rev',0) or 0 for e in es if e.get('type')=='fin_month' and 'MONTH_2025' in e.get('id',''))
total_fb_profit = sum(e.get('fb_profit',0) or 0 for e in es if e.get('type')=='fin_month' and 'MONTH_2025' in e.get('id',''))
print(f'\n{"="*60}')
print(f'  2025年度FB汇总')
print(f'{"="*60}')
print(f'  FB总收入:    ¥{total_fb_rev/10000:>8.1f}万')
print(f'  FB总利润:    ¥{total_fb_profit/10000:>8.1f}万')
print(f'  平均利润率:   {total_fb_profit/total_fb_rev*100:>5.1f}%')
print(f'  FB模块实体:  {len(fb)}个')
print(f'  FIN版本:     v5.15')
