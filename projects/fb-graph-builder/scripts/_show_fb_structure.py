#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# FB相关实体
fb_entities = [e for e in es if any(k in (e.get('type','') or '') for k in 
    ['fb_', 'food_', 'beverage', 'promo', 'menu', 'purchase', 'inventory', 
     'outlet', 'bazaar', 'bev_', 'drr_fb'])]

print(f'FB模块总实体: {len(fb_entities)}')
print()

# 按类型分组
by_type = {}
for e in fb_entities:
    t = e.get('type','unknown')
    if t not in by_type: by_type[t] = []
    by_type[t].append(e)

for t in sorted(by_type.keys()):
    items = by_type[t]
    print(f'\n=== {t} ({len(items)}个) ===')
    for item in items[:8]:
        eid = item.get('id','')[:35]
        label = str(item.get('label',''))[:30]
        # 展示关键数字
        extras = []
        for k in ['food_cost_pct','bev_cost_pct','fb_rev','fb_profit','fb_margin',
                   'food_rev','food_cost','bev_rev','bev_cost','total_rev','total_cost']:
            v = item.get(k)
            if v and v != 0:
                if 'pct' in k or 'margin' in k:
                    extras.append(f'{k}={v}')
                elif 'rev' in k or 'cost' in k or 'profit' in k:
                    extras.append(f'{k}={v/10000:.1f}万')
        extra_str = ' | ' + ' '.join(extras) if extras else ''
        print(f'    {eid:35s} | {label:30s}{extra_str}')
    if len(items) > 8:
        print(f'    ... 还有{len(items)-8}个')

# 结构总结
print('\n' + '='*60)
print('FB模块结构总结')
print('='*60)

# 按维度归组
dims = {
    '月度F&B损益': ['fin_month'],
    '出口成本率': ['fb_cost'],
    '酒水成本率': ['beverage_cost_report'],
    '出口营业统计': ['fb_outlet_stats', 'outlet', 'bev_outlet'],
    '食材采购分析': ['fb_purchase_analysis'],
    '促销数据': ['promotion_product', 'fb_seasonal_promotion', 'fb_promotion_roi'],
    '库存数据': ['fb_inventory'],
    '品类分类': ['fb_category', 'fb_outlet_category'],
    '餐饮工程': ['fb_menu_engineering'],
    'FY展望': ['fb_forecast_monthly'],
    '美食市集': ['bazaar_daily', 'bazaar_menu_item', 'bazaar_monthly'],
    '餐饮日报': ['drr_fb_daily'],
}

for dim_name, types_list in dims:
    items_in_dim = []
    for t in types_list:
        items_in_dim.extend(by_type.get(t, []))
    if items_in_dim:
        print(f'  {dim_name:12s} | {len(items_in_dim):>4d} 个')

# 有数据的月度看板
print('\nFB月度数据覆盖:')
for e in sorted([e for e in es if e.get('type')=='fin_month' and 'MONTH_2025' in e.get('id','')], key=lambda x: x['id']):
    fb_rev = e.get('fb_rev',0) or 0
    fb_profit = e.get('fb_profit',0) or 0
    fb_margin = e.get('fb_margin',0) or 0
    status = 'HAS FB' if fb_rev > 0 else 'NO FB'
    label = e['id'].replace('MONTH_2025_','').replace('_','月')
    margin_str = f'{fb_margin:.1f}%' if fb_margin else '-'
    print(f'  2025年{label:>2} | FB收入: {fb_rev/10000:>6.1f}万 | FB利润: {fb_profit/10000:>6.1f}万 | FB利润率: {margin_str:>6} | {status}')
