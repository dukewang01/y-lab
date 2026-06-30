import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')
fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])

OUTLET_MAP = {
    'OPEN': 'OUTLET_OPEN', 'YUXI': 'OUTLET_YUXI', 'BACIO': 'OUTLET_BACIO',
    'YUAN': 'OUTLET_YUAN', 'BQT': 'OUTLET_BANQUET', 'IRD': 'OUTLET_ROOM_DINING',
    'BEER': 'OUTLET_BEER_SOCIETY', 'BAZAAR': 'OUTLET_BAZAAR',
    'TAKEOUT': 'OUTLET_TAKEOUT', 'COMPETITOR': 'OUTLET_COMPETITOR',
}
CATEGORY_TO_OUTLET = {
    'wedding':'BQT', 'menu_catering':'BQT', 'menu_buffet':'BQT', 'menu_summary':'BQT',
    'menu_main':'OPEN', 'menu_drink':'OPEN', 'menu_soup':'OPEN', 'menu_dessert':'OPEN',
    'menu_appetizer':'OPEN', 'menu_main_course':'OPEN', 'menu_cold_appetizer':'OPEN',
    'menu_steak':'OPEN', 'open_add':'OPEN', 'drink_list':'OPEN', 'wine_list':'OPEN',
    'menu_room_service':'IRD', 'bacio':'BACIO', 'bacio_wine':'BACIO',
    'yuxi_drink':'YUXI', 'lobby_tea':'YUAN',
    'menu_beer':'BEER', 'menu_whisky':'BEER', 'cocktail':'BEER',
    'outlet':'COMPETITOR', 'hotel_competitor':'COMPETITOR',
    'promo_side':'OPEN', '饮品':'YUAN', '午茶-茶饮':'YUAN',
    '白酒':'YUXI', '洋酒':'YUXI', '招牌海鲜':'YUXI', '酒店王炸':'OPEN',
    '手工点心':'YUXI', '自助早餐':'OPEN', '周末套餐':'OPEN',
}

existing = set()
for r in fbr:
    s = r.get('source_id', r.get('source', ''))
    t = r.get('target_id', r.get('target', ''))
    existing.add((s, r.get('type', ''), t))

products = [n for n in fbe if n.get('type') == 'product']
count_by_outlet = {}
missed = []
new_rels = []

for p in products:
    pid = p['id']
    cat = (p.get('properties', {}).get('category', '') or p.get('category', '')).lower().strip()
    outlet_key = CATEGORY_TO_OUTLET.get(cat)
    if not outlet_key:
        missed.append(cat)
        continue
    oid = OUTLET_MAP[outlet_key]
    key = (pid, 'BELONGS_TO', oid)
    if key in existing:
        continue
    new_rels.append({'source_id': pid, 'type': 'BELONGS_TO', 'target_id': oid})
    count_by_outlet[outlet_key] = count_by_outlet.get(outlet_key, 0) + 1

total_new = len(new_rels)

# 备份
bak_fp = fp.replace('.json', '_before_belongs_to.json')
shutil.copy2(fp, bak_fp)
print('备份:', bak_fp)

fbr.extend(new_rels)
fb['relationships'] = fbr
json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print()
print('=== 写入完成! ===')
print('新增BELONGS_TO: %d条' % total_new)
for k, cnt in sorted(count_by_outlet.items(), key=lambda x: -x[1]):
    name = {'OPEN':'OPEN','YUXI':'御玺','BACIO':'BACIO','YUAN':'大堂吧','BQT':'宴会','IRD':'送餐','BEER':'啤酒荟','COMPETITOR':'竞对'}.get(k, k)
    print('  %s → %s: %d' % (name, OUTLET_MAP[k], cnt))
print('未匹配品类: %d个 (大部分可ROUTING)' % len(set(missed)))
print('当前: %d节点 / %d关系 / 密度%.2f' % (len(fbe), len(fbr), len(fbr)/len(fbe)))
