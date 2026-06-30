#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# FB相关类型统计
print('所有FB/成本相关类型:')
for t, c in Counter(e.get('type', '') for e in es).most_common(50):
    if any(k in t.lower() for k in ['fb', 'food', 'cost', 'promo', 'menu', 'purchase', 'inventory', 'beverage', 'outlet']):
        print(f'  {t}: {c}')

# 看每个月是否已经有fb_rev, fb_profit
months = [e for e in es if e.get('type') == 'fin_month' and e.get('id','').startswith('MONTH_2025')]
print(f'\n月份FB数据覆盖度:')
for m in sorted(months, key=lambda x: x.get('id','')):
    fb_rev = m.get('fb_rev', 0) or 0
    fb_profit = m.get('fb_profit', 0) or 0
    fb_margin = m.get('fb_margin', 0) or 0
    has_fb = 'YES' if fb_rev > 0 else 'EMPTY'
    print(f'  {m["id"]}: FB收入={fb_rev:>8,.0f} | FB利润={fb_profit:>7,.0f} | FB利润率={fb_margin:>5} | {has_fb}')

# fb_outlet_stats
outlets = [e for e in es if e.get('type') == 'fb_outlet_stats']
print(f'\nfb_outlet_stats: {len(outlets)}')
for o in outlets[:10]:
    print(f'  {o.get("id","")[:40]}: {str(o.get("label",""))[:30]}')
