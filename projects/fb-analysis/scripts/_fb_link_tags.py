#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""连接FB产品 ↔ CRM偏好标签"""
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
CRM = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
fp = os.path.join(D, 'fb_graph.json')

fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])
prefs = json.load(open(os.path.join(CRM, 'preferences.json'), encoding='utf-8'))

from collections import Counter

e_map = {n['id']: n for n in fbe}

# ====== 1. 建立CRM偏好标签映射 ======
# 偏好value → FB站crm_tag节点类型的ID映射
PREF_TO_FB_TAG = {
    '海鲜':          'CRM_PREF_SEAFOOD',
    '素食健康':      'CRM_PREF_VEGAN',
    '甜品类':        'CRM_PREF_DESSERT',
    '甜品':          'CRM_PREF_DESSERT',
    '牛排肉食':      'CRM_PREF_MEAT',
    '牛排/肉食':     'CRM_PREF_MEAT',
    '酒饮':          'CRM_PREF_DRINK',
    '辣味':          'CRM_PREF_SPICY',
    '辣':            'CRM_PREF_SPICY',
    '清淡':          'CRM_PREF_LIGHT',
}

# 已有的crm_tag节点
tag_nodes = {n['id']: n for n in fbe if n.get('type') == 'crm_tag'}
print('已有CRM标签节点:')
for tid, tn in tag_nodes.items():
    print('  %s: %s' % (tid, tn.get('name', '')))

# 需要创建的标签
need_create = set()
for pref_val, fb_id in PREF_TO_FB_TAG.items():
    if fb_id not in e_map:
        need_create.add(fb_id)
        print('  需创建: %s (%s)' % (fb_id, pref_val))

# 新增crm_tag节点
new_nodes = []
for nid in need_create:
    # 根据ID推导名称
    name_map = {'CRM_PREF_SEAFOOD':'海鲜', 'CRM_PREF_VEGAN':'素食/健康',
                'CRM_PREF_DESSERT':'甜品/甜点', 'CRM_PREF_MEAT':'牛排/肉食',
                'CRM_PREF_DRINK':'酒饮/红酒', 'CRM_PREF_SPICY':'辣味',
                'CRM_PREF_LIGHT':'清淡'}
    new_nodes.append({
        'id': nid, 'name': name_map.get(nid, nid),
        'type': 'crm_tag', 'properties': {}
    })
    print('  创建: %s -> %s' % (nid, name_map.get(nid, '')))

if new_nodes:
    fbe.extend(new_nodes)
    e_map = {n['id']: n for n in fbe}
    print('新增crm_tag节点: %d个' % len(new_nodes))

# ====== 2. 构建产品→CRM标签链 ======
# 品类→CRM标签映射
CAT_TO_TAG = {
    'menu_steak':       'CRM_PREF_MEAT',
    'menu_appetizer':   'CRM_PREF_LIGHT',
    'menu_main':        'CRM_PREF_MEAT',
    'menu_soup':        'CRM_PREF_LIGHT',
    'menu_dessert':     'CRM_PREF_DESSERT',
    'bacio':            'CRM_PREF_MEAT',
    'bacio_wine':       'CRM_PREF_DRINK',
    'drink_list':       'CRM_PREF_DRINK',
    'wine_list':        'CRM_PREF_DRINK',
    'yuxi_drink':       'CRM_PREF_DRINK',
    'menu_beer':        'CRM_PREF_DRINK',
    'menu_whisky':      'CRM_PREF_DRINK',
    'cocktail':         'CRM_PREF_DRINK',
    '白酒':              'CRM_PREF_DRINK',
    '洋酒':              'CRM_PREF_DRINK',
    '招牌海鲜':          'CRM_PREF_SEAFOOD',
    'handcraft':        'CRM_PREF_DESSERT',
    '甜品':              'CRM_PREF_DESSERT',
    '面包蛋糕':          'CRM_PREF_DESSERT',
    '手工点心':          'CRM_PREF_LIGHT',
    '轻食':              'CRM_PREF_LIGHT',
    '素食':              'CRM_PREF_VEGAN',
    '辣':                'CRM_PREF_SPICY',
}

# 关键词匹配（额外补充）
KEYWORD_TO_TAG = {
    '牛排': 'CRM_PREF_MEAT', '牛肉': 'CRM_PREF_MEAT', '肉': 'CRM_PREF_MEAT',
    '海鲜': 'CRM_PREF_SEAFOOD', '虾': 'CRM_PREF_SEAFOOD', '鱼': 'CRM_PREF_SEAFOOD',
    '素食': 'CRM_PREF_VEGAN', '蔬菜': 'CRM_PREF_VEGAN', '沙拉': 'CRM_PREF_VEGAN',
    '甜': 'CRM_PREF_DESSERT', '蛋糕': 'CRM_PREF_DESSERT', '冰淇淋': 'CRM_PREF_DESSERT',
    '酒': 'CRM_PREF_DRINK', '茅台': 'CRM_PREF_DRINK', '红酒': 'CRM_PREF_DRINK',
    '辣': 'CRM_PREF_SPICY', '麻辣': 'CRM_PREF_SPICY', '香辣': 'CRM_PREF_SPICY',
    '清淡': 'CRM_PREF_LIGHT', '清蒸': 'CRM_PREF_LIGHT', '白灼': 'CRM_PREF_LIGHT',
}

existing = set()
for r in fbr:
    existing.add((r.get('source_id',''), r.get('type',''), r.get('target_id','')))

products = [n for n in fbe if n.get('type') == 'product']
new_rels = []
tagged_count = Counter()

for p in products:
    pid = p['id']
    cat = (p.get('properties', {}).get('category', '') or p.get('category', '')).lower().strip()
    name = p.get('name', '')
    tags = set()
    
    # 品类匹配
    tag_id = CAT_TO_TAG.get(cat)
    if tag_id:
        tags.add(tag_id)
    
    # 关键词匹配
    for kw, tid in KEYWORD_TO_TAG.items():
        if kw in name:
            tags.add(tid)
    
    # 创建关系
    for tid in tags:
        key = (pid, 'RECOMMENDED_FOR', tid)
        if key not in existing:
            new_rels.append({
                'source_id': pid, 'type': 'RECOMMENDED_FOR', 'target_id': tid
            })
            existing.add(key)
        tagged_count[tid] += 1

total_new = len(new_rels)
print()
print('新增RECOMMENDED_FOR关系: %d条' % total_new)
for tid, cnt in tagged_count.most_common():
    nm = e_map.get(tid, {}).get('name', tid)
    print('  %-16s → %d个产品' % (nm[:16], cnt))

print()
print('当前: %d节点 / %d关系 / 密度%.2f' % (len(fbe), len(fbr) + total_new, (len(fbr)+total_new)/len(fbe)))

# ====== 3. 写入 ======
import shutil
bak_fp = fp.replace('.json', '_before_tag_link.json')
shutil.copy2(fp, bak_fp)
print('备份:', bak_fp)

fbr.extend(new_rels)
fb['entities'] = fbe
fb['relationships'] = fbr
json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('写入完成! 密度: 0.08 → %.2f' % ((len(fbr))/len(fbe)))
