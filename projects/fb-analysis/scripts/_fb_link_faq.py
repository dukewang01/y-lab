# -*- coding: utf-8 -*-
"""FB站营业点嵌入FAQ引用索引"""
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp_fb = os.path.join(D, 'fb_graph.json')
fp_faq = os.path.join(D, 'faq_graph.json')

fb = json.load(open(fp_fb, encoding='utf-8'))
fbe = fb.get('entities', [])
faq = json.load(open(fp_faq, encoding='utf-8'))
fqe = faq.get('entities', faq.get('nodes', []))

# 找到餐饮相关的FAQ
outlet_keywords = {
    'OPEN': ['自助','早餐','午餐','OPEN','全日','ADD','5F','餐厅','restaurant'],
    'YUXI': ['御玺','中餐','中餐厅','yuxi','包间','包厢','宴请'],
    'BACIO': ['BACIO','意大利','bacio','pasta','披萨','西餐'],
    'YUAN': ['大堂吧','YUAN','yuan','下午茶','下午茶','甜品','lobby','lounge'],
    'BANQUET': ['宴会','婚宴','会议','宴会厅','bqt','BQT','BALLROOM'],
    'ROOM_DINING': ['送餐','IRD','ird','客房','送餐','room service'],
    'BEER_SOCIETY': ['啤酒','啤酒荟','beer','酒吧','微醺','酒单'],
    'TAKEOUT': ['外卖','外送','delivery','美团','饿了么'],
    'BAZAAR': ['bazaar','BAZAAR','市集','美食市集','面包','甜品站'],
}

# 扫描FAQ
faq_map = {n['id']: n for n in fqe}
faq_by_outlet = {k: [] for k in outlet_keywords.keys()}
faq_general_fb = []  # 通用的餐饮FAQ

for nid, n in faq_map.items():
    name = n.get('name', '')
    desc = n.get('description', '')
    text = (name + ' ' + desc).lower()
    matched = False
    
    for outlet, keywords in outlet_keywords.items():
        for kw in keywords:
            if kw.lower() in text:
                faq_by_outlet[outlet].append(nid)
                matched = True
                break
        if matched:
            break
    
    if not matched:
        # 通用餐饮关键词
        fb_kw = ['餐饮','果汁','咖啡','饮料','水','酒','菜品','菜单','厨房','食材','过敏']
        if any(kw in text for kw in fb_kw):
            faq_general_fb.append(nid)

print('FAQ站餐饮关联分析:')
for outlet, faqs in faq_by_outlet.items():
    print('  %-15s %d条覆盖' % (outlet, len(set(faqs))))
print('  通用餐饮: %d条' % len(faq_general_fb))

# 嵌入到营业点节点
outlet_map = {
    'OPEN': 'OUTLET_OPEN', 'YUXI': 'OUTLET_YUXI', 'BACIO': 'OUTLET_BACIO',
    'YUAN': 'OUTLET_YUAN', 'BANQUET': 'OUTLET_BANQUET',
    'ROOM_DINING': 'OUTLET_ROOM_DINING', 'BEER_SOCIETY': 'OUTLET_BEER_SOCIETY',
    'TAKEOUT': 'OUTLET_TAKEOUT', 'BAZAAR': 'OUTLET_BAZAAR',
}

updated_count = 0
for n in fbe:
    if n.get('type') != 'outlet':
        continue
    nid = n['id']
    # 反向查找outlet_key
    outlet_key = None
    for ok, oid in outlet_map.items():
        if oid == nid:
            outlet_key = ok
            break
    if not outlet_key:
        continue
    
    faq_ids = list(set(faq_by_outlet.get(outlet_key, [])))
    if 'properties' not in n:
        n['properties'] = {}
    n['properties']['faq_refs'] = faq_ids
    n['properties']['faq_count'] = len(faq_ids)
    updated_count += 1
    print('  %s → %d条FAQ引用' % (nid, len(faq_ids)))

# 通用餐饮FAQ嵌入到FB_OUTLET_STANDARD
for n in fbe:
    if n.get('id') == 'FB_OUTLET_STANDARD' and n.get('type') == 'outlet':
        n['properties']['faq_refs'] = faq_general_fb[:100]
        n['properties']['faq_count'] = min(len(faq_general_fb), 100)
        print('  FB_OUTLET_STANDARD → %d条通用FAQ' % min(len(faq_general_fb), 100))
        break

# 写入
shutil.copy2(fp_fb, fp_fb.replace('.json', '_before_faq_refs.json'))
fb['entities'] = fbe
json.dump(fb, open(fp_fb, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print()
print('写入完成! %d个营业点更新了faq_refs' % updated_count)
