#!/usr/bin/env python3
import json, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

f = json.load(open('fb_graph.json', 'r', encoding='utf-8'))
es = f.get('entities', [])
items = [e for e in es if e.get('type') == 'hoe_item']

cats = defaultdict(lambda: {'items': 0, 'qty': 0})
for item in items:
    c = item.get('category', '未分类')
    cats[c]['items'] += 1
    cats[c]['qty'] += item.get('qty', 0) or 0

total_qty = sum(d['qty'] for d in cats.values())
print('品类分布:')
print(f'{"品类":>10} | {"项数":>5} | {"数量":>9} | {"占比":>6} | 趋势')
print('-' * 55)
for c, d in sorted(cats.items(), key=lambda x: -x[1]['qty']):
    pct = d['qty'] / total_qty * 100
    bar = '█' * min(int(pct / 2), 30)
    print(f'  {c:>10} | {d["items"]:>5}项 | {d["qty"]:>8,}件 | {pct:>5.1f}% | {bar}')

print(f'\nHOE总计: {len(items)}项品目, {total_qty:,}件物资')
print(f'覆盖品类: {len(cats)}个')
