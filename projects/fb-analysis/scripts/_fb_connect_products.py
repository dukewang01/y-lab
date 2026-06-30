#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FB站图增强：建立BELONGS_TO关系连接孤立产品到营业点"""
import sys, json, os, datetime
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')

# 加载
fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])

# 营业点ID映射（FB站和FIN站都有）
OUTLET_MAP = {
    # 堂食6店
    'OPEN':         'OUTLET_OPEN',
    'YUXI':         'OUTLET_YUXI',
    'BACIO':        'OUTLET_BACIO',
    'YUAN':         'OUTLET_YUAN',
    'BQT':          'OUTLET_BANQUET',
    'IRD':          'OUTLET_ROOM_DINING',
    # 零售
    'BEER':         'OUTLET_BEER_SOCIETY',
    'BAZAAR':       'OUTLET_BAZAAR',
    # 通用
    'TAKEOUT':      'OUTLET_TAKEOUT',
    'COMPETITOR':   'OUTLET_COMPETITOR',
}

# 品类→营业点映射规则
CATEGORY_TO_OUTLET = {
    'wedding':          'BQT',
    'menu_catering':    'BQT',
    'menu_buffet':      'BQT',
    'menu_main':        'OPEN',
    'menu_drink':       'OPEN',
    'menu_soup':        'OPEN',
    'menu_dessert':     'OPEN',
    'menu_appetizer':   'OPEN',
    'menu_main_course': 'OPEN',
    'menu_cold_appetizer': 'OPEN',
    'menu_steak':       'OPEN',
    'open_add':         'OPEN',
    'menu_room_service': 'IRD',
    'bacio':            'BACIO',
    'bacio_wine':       'BACIO',
    'yuxi_drink':       'YUXI',
    'lobby_tea':        'YUAN',
    'drink_list':       'OPEN',
    'wine_list':        'OPEN',
    'menu_beer':        'BEER',
    'menu_whisky':      'BEER',
    'cocktail':         'BEER',
    'outlet':           'COMPETITOR',
    'hotel_competitor': 'COMPETITOR',
}

# 生成BELONGS_TO关系
new_rels = []
count_by_outlet = {k:0 for k in OUTLET_MAP}
count_missed = 0

existing = set()
for r in fbr:
    s = r.get('source_id', r.get('source', ''))
    t = r.get('target_id', r.get('target', ''))
    rtype = r.get('type', '')
    existing.add((s, rtype, t))

from collections import Counter

# 找FB站内的营业点节点
outlet_nodes = {n['id']: n for n in fbe if n.get('type') == 'outlet'}
print('FB站已有营业点节点:')
for oid, on in outlet_nodes.items():
    print('  %s: %s' % (oid, on.get('name', '')))

# 构建产品→营业点关系
products = [n for n in fbe if n.get('type') == 'product']
cat_stats = Counter()

for p in products:
    pid = p['id']
    cat = p.get('properties', {}).get('category', '') or p.get('category', '')
    cat_lower = cat.lower().strip()
    cat_stats[cat_lower] += 1
    
    # 匹配营业点
    outlet_key = CATEGORY_TO_OUTLET.get(cat_lower)
    if not outlet_key:
        count_missed += 1
        continue
    
    outlet_id = OUTLET_MAP.get(outlet_key)
    if not outlet_id:
        count_missed += 1
        continue
    
    # 检查是否已存在
    key = (pid, 'BELONGS_TO', outlet_id)
    if key in existing:
        continue
    
    new_rels.append({
        'source_id': pid,
        'type': 'BELONGS_TO',
        'target_id': outlet_id,
    })
    count_by_outlet[outlet_key] += 1

# 输出
print()
print('新生成的BELONGS_TO关系:')
total_new = sum(count_by_outlet.values())
for k, cnt in sorted(count_by_outlet.items(), key=lambda x: -x[1]):
    if cnt > 0:
        name = {'OPEN':'OPEN自助','YUXI':'御玺','BACIO':'BACIO','YUAN':'大堂吧','BQT':'宴会','IRD':'送餐','BEER':'啤酒荟','BAZAAR':'Bazaar','TAKEOUT':'外卖','COMPETITOR':'竞对'}.get(k, k)
        print('  %-10s → %s: %d条' % (k, name, cnt))
print('  未匹配品类: %d个' % count_missed)

print()
print('总计新增关系: %d条' % total_new)
print('当前总关系: %d条' % len(fbr))
print('新增后总关系: %d条' % (len(fbr) + total_new))
print('密度: %.2f → %.2f' % (len(fbr)/len(fbe), (len(fbr)+total_new)/len(fbe)))

# 确认
if total_new > 0:
    print()
    ans = input('是否写入文件？(y/n): ').strip().lower()
    if ans == 'y':
        fbr.extend(new_rels)
        fb['relationships'] = fbr
        # 备份
        bak_fp = fp.replace('.json', '_before_belongs_to.json')
        import shutil
        shutil.copy2(fp, bak_fp)
        print('备份: %s' % bak_fp)
        # 写入
        json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('写入完成! 新增%d条BELONGS_TO关系' % total_new)
        print('FB站: %d节点 / %d关系' % (len(fbe), len(fbr)))
    else:
        print('已取消写入')
else:
    print('没有需要新增的关系')
