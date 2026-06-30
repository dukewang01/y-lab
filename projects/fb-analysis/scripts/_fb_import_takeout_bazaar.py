# -*- coding: utf-8 -*-
"""FB站接入外�?BAZAAR产品�?+2营业�?""
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Users\Y\.openclaw\workspace\knowledge_center'
fp_fb = os.path.join(D, 'fb_graph.json')
fp_fin = os.path.join(D, 'fin_graph.json')

fb = json.load(open(fp_fb, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])
fin = json.load(open(fp_fin, encoding='utf-8'))
fine = fin.get('entities', [])
e_map_fb = {n['id']: n for n in fbe}

existing = set()
for r in fbr:
    existing.add((r.get('source_id',''), r.get('type',''), r.get('target_id','')))

new_nodes = []
new_rels = []

# ==== 1. 接入外卖产品 ====
print('=== 外卖接入 ===')
deliveries = [n for n in fbe if 'delivery' in n.get('type','').lower()]
print('已有外卖节点: %d�? % len(deliveries))

# 外卖月汇总→按月份拆成产品连�?del_summaries = [n for n in fbe if n.get('type') in ('delivery_summary','delivery_monthly')]
print('外卖汇�? %d�? % len(del_summaries))
for d in del_summaries:
    did = d['id']
    name = d.get('name','')
    # 连接到OUTLET_TAKEOUT
    key = (did, 'BELONGS_TO', 'OUTLET_TAKEOUT')
    if key not in existing:
        new_rels.append({'source_id': did, 'type': 'BELONGS_TO', 'target_id': 'OUTLET_TAKEOUT'})
        existing.add(key)
        print('  接入: %s �?OUTLET_TAKEOUT' % name[:30])

# ==== 2. 接入BAZAAR菜品 ====
print()
print('=== BAZAAR接入 ===')
# FIN站的bazaar_menu_items
baz_items = [n for n in fine if n.get('type') == 'bazaar_menu_item']
print('FIN站BAZAAR菜品: %d�? % len(baz_items))

# FB站已有bazaar_category节点
baz_cats = {n['id']: n for n in fbe if n.get('type') == 'bazaar_category'}
print('FB站BAZAAR分类: %d�? % len(baz_cats))

# 已有bazaar_menu_item类型的node
fb_baz_items = [n for n in fbe if n.get('is_bazaar') or n.get('type') == 'bazaar_menu_item']
print('FB站已有bazaar_menu_item: %d�? % len(fb_baz_items))

# 检查FB站是否有type=menu_item的节�?menu_items = [n for n in fbe if n.get('type') == 'menu_item']
print('FB站menu_item: %d�? % len(menu_items))

# 看具体的BAZAAR菜品结构
if baz_items:
    for b in baz_items[:5]:
        print('  %s: %s' % (b['id'][:25], b.get('name','')[:25]))
        print('    type:', b.get('type',''))
        print('    props:', {k:str(v)[:20] for k,v in b.get('properties',{}).items()})

print()
print('=== FB站bazaar_category ===')
print('现有BAZAAR分类节点:')
for bid, bn in baz_cats.items():
    print('  %s: %s' % (bid, bn.get('name','')[:30]))

print()
print('=== 检查FB站是否有BAZAAR_ITEM节点 ===')
baz_refs = [n for n in fbe if 'BAZAAR' in n.get('id','')]
print('BAZAAR相关节点: %d�? % len(baz_refs))
for b in baz_refs:
    print('  %s (%s): %s' % (b['id'][:30], b.get('type',''), b.get('name','')[:30]))
