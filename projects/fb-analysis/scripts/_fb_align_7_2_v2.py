# -*- coding: utf-8 -*-
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Y\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')

fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])

existing = set()
for r in fbr:
    existing.add((r.get('source_id', ''), r.get('type', ''), r.get('target_id', '')))

# 补充品类映射
EXTRA = {
    'menu_pasta': 'OUTLET_BACIO', 'menu_pizza': 'OUTLET_BACIO',
    'menu_oyster': 'OUTLET_BACIO', 'menu_starter': 'OUTLET_BACIO',
    'menu_specialty': 'OUTLET_BACIO', 'menu_signature': 'OUTLET_BACIO',
    'menu_sandwich': 'OUTLET_BACIO', 'menu_wine': 'OUTLET_BACIO',
    'menu_set': 'OUTLET_BACIO', 'menu_hotstarter': 'OUTLET_BACIO',
    'menu_spirit': 'OUTLET_BACIO', 'menu_salad': 'OUTLET_BACIO',
    'menu_side': 'OUTLET_BACIO', 'menu_salad': 'OUTLET_BACIO',
    # 酒水
    'red_wine': 'OUTLET_OPEN', 'white_wine': 'OUTLET_OPEN',
    'beer': 'OUTLET_BEER_SOCIETY', 'mocktail': 'OUTLET_BEER_SOCIETY',
    # 轻食系列
    'menu_lunch_light': 'OUTLET_OPEN',
}

# 关键词映�?KW_MAP = {
    'promo': {
        'beer': 'OUTLET_BEER_SOCIETY', 'cake': 'OUTLET_YUAN',
        'lobster': 'OUTLET_OPEN', 'seafood': 'OUTLET_OPEN',
        'hotpot': 'OUTLET_OPEN', 'bbq': 'OUTLET_OPEN',
        'dessert': 'OUTLET_YUAN', 'christmas': 'OUTLET_YUAN',
        'tea': 'OUTLET_YUAN', 'gift': 'OUTLET_YUAN',
        'event': 'OUTLET_BANQUET', 'party': 'OUTLET_BANQUET',
        'dinner': 'OUTLET_OPEN', 'buffet': 'OUTLET_OPEN',
        'drink': 'OUTLET_OPEN',
    },
    'light_food': 'OUTLET_OPEN', 'cold_dish': 'OUTLET_YUXI',
    'soup': 'OUTLET_YUXI', 'salad': 'OUTLET_BACIO',
    'main_staple': 'OUTLET_YUXI', 'beef_brisket': 'OUTLET_YUXI',
    'dessert_sweet': 'OUTLET_YUAN', 'mushroom_veg': 'OUTLET_YUXI',
    'huangjiu': 'OUTLET_YUXI',
}

# 中文品类→英文标识映射（用于KEYWORD匹配�?CN_CAT_MAP = {
    u'\u51b7\u83dc': 'cold_dish', u'\u6c64\u7fb9': 'soup',
    u'\u6c99\u62c9': 'salad', u'\u7279\u8272\u4e3b\u98df': 'main_staple',
    u'\u7279\u8272\u725b\u8158\u7096': 'beef_brisket',
    u'\u7cbe\u7f8e\u751c\u54c1': 'dessert_sweet',
    u'\u83cc\u83c7\u7d20\u83dc': 'mushroom_veg',
    u'\u9ec4\u9152': 'huangjiu',
    u'\u7ea2\u9152': 'red_wine', u'\u767d\u8461\u8404\u9152': 'white_wine',
    u'\u5564\u9152': 'beer',
    u'\u8f7b\u98df': 'light_food', u'\u8f7b\u98df\u4e3b\u98df': 'light_food',
    u'\u8f7b\u98df\u51b7\u83dc': 'light_food', u'\u8f7b\u98df\u6c64\u54c1': 'light_food',
    u'\u8f7b\u98df\u6c99\u62c9': 'light_food', u'\u8f7b\u98df\u70b9\u5fc3': 'light_food',
    u'\u8f7b\u98df\u70ed\u83dc': 'light_food', u'\u8f7b\u98df\u996e\u54c1': 'light_food',
    u'\u5564\u9152': 'beer',
}

products = [n for n in fbe if n.get('type') == 'product']
new_rels = []
still_missed = {}
fixed_cats = {}

for p in products:
    pid = p['id']
    cat = (p.get('properties', {}).get('category', '') or p.get('category', '')).lower().strip()
    name = p.get('name', '')
    
    # 跳过已匹配的
    if any(r.get('source_id') == pid and r.get('type') == 'BELONGS_TO' for r in fbr):
        continue
    
    target = None
    
    # 1. 精确品类匹配
    target = EXTRA.get(cat)
    
    # 2. 中文品类映射
    if not target:
        cn_en = CN_CAT_MAP.get(cat)
        if cn_en:
            target = KW_MAP.get(cn_en)
            if isinstance(target, str):
                pass  # 已经是ID
            else:
                target = None
    
    # 3. 促销品类→按name关键�?    if not target and cat.startswith('promo'):
        name_lower = name.lower()
        for kw, oid in KW_MAP.get('promo', {}).items():
            if kw in name_lower:
                target = oid
                break
    
    # 4. 兜底
    if not target:
        for kw, oid in [('rice', 'OUTLET_YUXI'), ('noodle', 'OUTLET_YUXI'),
                        ('fish', 'OUTLET_YUXI'), ('shrimp', 'OUTLET_YUXI'),
                        ('steak', 'OUTLET_BACIO'), ('sweet', 'OUTLET_YUAN'),
                        ('bread', 'OUTLET_YUAN'), ('cake', 'OUTLET_YUAN')]:
            if kw in name.lower():
                target = oid
                break
    
    if target:
        key = (pid, 'BELONGS_TO', target)
        if key not in existing:
            new_rels.append({'source_id': pid, 'type': 'BELONGS_TO', 'target_id': target})
            existing.add(key)
            fixed_cats[cat] = fixed_cats.get(cat, 0) + 1
    else:
        still_missed[cat] = still_missed.get(cat, 0) + 1

if new_rels:
    fbr.extend(new_rels)
    fb['relationships'] = fbr
    shutil.copy2(fp, fp.replace('.json', '_before_7_2_fix.json'))
    json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('补充BELONGS_TO: %d�? % len(new_rels))
else:
    print('无需补充')

print('修复品类: %d�? % len(fixed_cats))
for c, cnt in sorted(fixed_cats.items(), key=lambda x: -x[1])[:10]:
    print('  %s: %d' % (c[:20], cnt))
print()
print('剩余未匹�? %d个品�? % len(still_missed))
for c, cnt in sorted(still_missed.items(), key=lambda x: -x[1])[:10]:
    print('  %s: %d' % (c[:20], cnt))

# 最终确�?fb3 = json.load(open(fp, encoding='utf-8'))
fbe3 = fb3.get('entities', [])
fbr3 = fb3.get('relationships', [])
belongs = sum(1 for r in fbr3 if r.get('type') == 'BELONGS_TO')
print()
print('最�? %d节点 / %d关系 / %d条BELONGS_TO / 密度%.2f' % (len(fbe3), len(fbr3), belongs, belongs / len(fbe3)))
