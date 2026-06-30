# -*- coding: utf-8 -*-
"""FB站BAZAAR菜品接入7+2 + 全部确认"""
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')

fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])
e_map = {n['id']: n for n in fbe}

existing = set()
for r in fbr:
    existing.add((r.get('source_id',''), r.get('type',''), r.get('target_id','')))

new_rels = []

# ==== BAZAAR菜品+分类 → OUTLET_BAZAAR ====
baz_nodes = [n for n in fbe if 'BAZAAR' in n.get('id','')]
print('BAZAAR相关节点: %d个' % len(baz_nodes))

# 分类节点→OUTLET_BAZAAR
baz_cat_ids = [n['id'] for n in baz_nodes if n.get('type') == 'bazaar_category']
for cid in baz_cat_ids:
    key = (cid, 'BELONGS_TO', 'OUTLET_BAZAAR')
    if key not in existing:
        new_rels.append({'source_id': cid, 'type': 'BELONGS_TO', 'target_id': 'OUTLET_BAZAAR'})
        existing.add(key)
print('  BAZAAR分类接入: %d个' % len(baz_cat_ids))

# BAZAAR_ITEM菜品→OUTLET_BAZAAR + 分类
baz_item_ids = [n['id'] for n in baz_nodes if n.get('type') in ('menu_item','bazaar_menu_item') and n['id'].startswith('BAZAAR_ITEM')]
print('  BAZAAR菜品: %d个' % len(baz_item_ids))

for iid in baz_item_ids:
    # 连到BAZAAR营业点
    key = (iid, 'BELONGS_TO', 'OUTLET_BAZAAR')
    if key not in existing:
        new_rels.append({'source_id': iid, 'type': 'BELONGS_TO', 'target_id': 'OUTLET_BAZAAR'})
        existing.add(key)

# 改menu_item类型为bazaar_menu_item（如果来自BAZAAR）
baz_item_nodes = [n for n in fbe if n['id'].startswith('BAZAAR_ITEM') and n.get('type') == 'menu_item']
if baz_item_nodes:
    for b in baz_item_nodes:
        b['type'] = 'bazaar_menu_item'
    print('  改类型menu_item→bazaar_menu_item: %d个' % len(baz_item_nodes))

# ==== 外卖汇总 → OUTLET_TAKEOUT ====
del_ids = [n['id'] for n in fbe if n.get('type') in ('delivery_summary','delivery_monthly')]
print()
print('外卖汇总接入: %d个' % len(del_ids))
for did in del_ids:
    key = (did, 'BELONGS_TO', 'OUTLET_TAKEOUT')
    if key not in existing:
        new_rels.append({'source_id': did, 'type': 'BELONGS_TO', 'target_id': 'OUTLET_TAKEOUT'})
        existing.add(key)

# 外卖平台节点
plat_ids = [n['id'] for n in fbe if n.get('type') == 'delivery_platform']
for pid in plat_ids:
    key = (pid, 'BELONGS_TO', 'OUTLET_TAKEOUT')
    if key not in existing:
        new_rels.append({'source_id': pid, 'type': 'BELONGS_TO', 'target_id': 'OUTLET_TAKEOUT'})
        existing.add(key)

# ==== 写入 ====
if new_rels:
    fbr.extend(new_rels)
    fb['entities'] = fbe
    fb['relationships'] = fbr
    shutil.copy2(fp, fp.replace('.json', '_before_bazaar_takeout.json'))
    json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print()
    print('新增BELONGS_TO: %d条' % len(new_rels))

# ==== 最终确认 ====
fb2 = json.load(open(fp, encoding='utf-8'))
fbe2 = fb2.get('entities', [])
fbr2 = fb2.get('relationships', [])
from collections import Counter
by_outlet = Counter()
for r in fbr2:
    if r.get('type') == 'BELONGS_TO':
        by_outlet[r.get('target_id','')] += 1

oid_name = {
    'OUTLET_OPEN':'OPEN全日','OUTLET_YUXI':'御玺','OUTLET_BACIO':'BACIO',
    'OUTLET_YUAN':'大堂吧','OUTLET_BANQUET':'宴会','OUTLET_ROOM_DINING':'送餐',
    'OUTLET_BEER_SOCIETY':'啤酒荟','OUTLET_TAKEOUT':'外卖','OUTLET_BAZAAR':'Bazaar',
    'OUTLET_COMPETITOR':'竞对',
}

print()
print('='*50)
print('7+2营业点最终产品分配:')
print('='*50)
total_b = 0
for oid in ['OUTLET_OPEN','OUTLET_YUXI','OUTLET_BACIO','OUTLET_YUAN',
            'OUTLET_BANQUET','OUTLET_ROOM_DINING','OUTLET_BEER_SOCIETY',
            'OUTLET_TAKEOUT','OUTLET_BAZAAR','OUTLET_COMPETITOR']:
    c = by_outlet.get(oid, 0)
    total_b += c
    print('  %-22s %4d个  %s' % (oid, c, oid_name.get(oid, '')))

print()
print('节点: %d  关系: %d  BELONGS_TO: %d  总密度: %.2f' % (len(fbe2), len(fbr2), total_b, len(fbr2)/len(fbe2)))
