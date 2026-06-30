#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FB站对齐7+2营业点结构"""
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')

fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])

e_map = {n['id']: n for n in fbe}

# 7+2营业点映射（品类→目标营业点ID）
OUTLET_7_2 = {
    # 堂食7店
    'OPEN': {
        'id': 'OUTLET_OPEN', 'name': 'OPEN全日餐厅',
        'cat': ['menu_main','menu_drink','menu_soup','menu_dessert',
                'menu_appetizer','menu_main_course','menu_cold_appetizer',
                'menu_steak','open_add','drink_list','wine_list',
                'menu_summary','promo_side','自助早餐','周末套餐',
                '酒店王炸','menu_buffet','menu_catering']
    },
    'YUXI': {
        'id': 'OUTLET_YUXI', 'name': '御玺中餐厅',
        'cat': ['yuxi_drink','白酒','洋酒','招牌海鲜','手工点心']
    },
    'BACIO': {
        'id': 'OUTLET_BACIO', 'name': 'BACIO意大利餐厅',
        'cat': ['bacio','bacio_wine']
    },
    'YUAN': {
        'id': 'OUTLET_YUAN', 'name': '大堂吧',
        'cat': ['lobby_tea','饮品','午茶-茶饮']
    },
    'BANQUET': {
        'id': 'OUTLET_BANQUET', 'name': 'BQT宴会厅',
        'cat': ['wedding','menu_catering','menu_buffet','menu_summary']
    },
    'ROOM_DINING': {
        'id': 'OUTLET_ROOM_DINING', 'name': 'IRD客房送餐',
        'cat': ['menu_room_service']
    },
    'BEER_SOCIETY': {
        'id': 'OUTLET_BEER_SOCIETY', 'name': '啤酒荟',
        'cat': ['menu_beer','menu_whisky','cocktail']
    },
    # 零售2类
    'TAKEOUT': {
        'id': 'OUTLET_TAKEOUT', 'name': '外卖（御玺+西厨房）',
        'cat': []
    },
    'BAZAAR': {
        'id': 'OUTLET_BAZAAR', 'name': '美食市集',
        'cat': []
    },
    # 竞对
    'COMPETITOR': {
        'id': 'OUTLET_COMPETITOR', 'name': '竞对酒店',
        'cat': ['outlet','hotel_competitor']
    },
}

# 品类→目标ID映射
CAT_TO_OID = {}
for key, info in OUTLET_7_2.items():
    for cat in info['cat']:
        CAT_TO_OID[cat] = info['id']

# 查找FB站已有outlet节点
existing_outlet_ids = set()
for n in fbe:
    if n.get('type') == 'outlet':
        existing_outlet_ids.add(n['id'])

# 需要创建的营业点节点
for key, info in OUTLET_7_2.items():
    if info['id'] not in existing_outlet_ids:
        fbe.append({
            'id': info['id'],
            'name': info['name'],
            'type': 'outlet',
            'properties': {}
        })
        print('  创建营业点节点: %s (%s)' % (info['id'], info['name']))

# 重建BELONGS_TO
products = [n for n in fbe if n.get('type') == 'product']
new_belongs = []
count_by_oid = {}
missed_cats = set()

for p in products:
    pid = p['id']
    cat = (p.get('properties', {}).get('category', '') or p.get('category', '')).lower().strip()
    target_id = CAT_TO_OID.get(cat)
    
    if not target_id:
        missed_cats.add(cat)
        continue
    
    new_belongs.append({'source_id': pid, 'type': 'BELONGS_TO', 'target_id': target_id})
    count_by_oid[target_id] = count_by_oid.get(target_id, 0) + 1

# 替换旧BELONGS_TO
old_count = sum(1 for r in fbr if r.get('type') == 'BELONGS_TO')
fbr[:] = [r for r in fbr if r.get('type') != 'BELONGS_TO']
fbr.extend(new_belongs)

# 备份+写入
bak_fp = fp.replace('.json', '_before_7_2.json')
shutil.copy2(fp, bak_fp)
print()
print('备份:', bak_fp)

fb['entities'] = fbe
fb['relationships'] = fbr
json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print()
print('=== 7+2营业点对齐完成! ===')
print('删除旧BELONGS_TO: %d条' % old_count)
print('新建BELONGS_TO: %d条' % len(new_belongs))
print()
print('营业点分配:')
for oid in ['OUTLET_OPEN','OUTLET_YUXI','OUTLET_BACIO','OUTLET_YUAN',
            'OUTLET_BANQUET','OUTLET_ROOM_DINING','OUTLET_BEER_SOCIETY',
            'OUTLET_TAKEOUT','OUTLET_BAZAAR','OUTLET_COMPETITOR']:
    cnt = count_by_oid.get(oid, 0)
    name = OUTLET_7_2.get(oid.replace('OUTLET_',''), {}).get('name', oid)
    if cnt > 0:
        print('  %-25s %4d个产品  %s' % (oid, cnt, name))

print()
print('未匹配品类: %d个' % len(missed_cats))
for mc in sorted(missed_cats):
    if mc: print('  %s' % mc[:25])

final_rels = sum(1 for r in fbr if r.get('type') == 'BELONGS_TO')
total_rels = len(fbr)
print()
print('BELONGS_TO: %d条  总关系: %d条  密度: %.2f' % (final_rels, total_rels, total_rels/len(fbe)))
