# -*- coding: utf-8 -*-
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fp = os.path.join(D, 'fb_graph.json')
fb = json.load(open(fp, encoding='utf-8'))
fbe = fb.get('entities', [])
fbr = fb.get('relationships', [])

existing = set()
for r in fbr:
    existing.add((r.get('source_id',''), r.get('type',''), r.get('target_id','')))

products = [n for n in fbe if n.get('type') == 'product']
unprod = [p for p in products if not any(r.get('source_id')==p['id'] and r.get('type')=='BELONGS_TO' for r in fbr)]

print('剩余未匹配: %d个' % len(unprod))

# 兜底映射
CAT_FALLBACK = {
    'promo_giftbox': 'OUTLET_YUAN',      # 礼盒→大堂吧
    'promo_seafood': 'OUTLET_OPEN',       # 海鲜→OPEN
    'promo_hotpot': 'OUTLET_OPEN',        # 火锅→OPEN
    'promo_tea': 'OUTLET_YUAN',           # 下午茶→大堂吧
    'promo_feature': 'OUTLET_OPEN',       # 特色→OPEN
    'promo_buffet': 'OUTLET_BANQUET',     # 自助→宴会
    'promo_bar': 'OUTLET_BEER_SOCIETY',   # 酒吧→啤酒荟
    'promo_dinner': 'OUTLET_OPEN',        # 晚餐→OPEN
    'promo_drink': 'OUTLET_OPEN',         # 饮品→OPEN
    'promo_event': 'OUTLET_BANQUET',      # 活动→宴会
    'promo_party': 'OUTLET_BANQUET',      # 派对→宴会
    'promo_cake': 'OUTLET_YUAN',          # 蛋糕→大堂吧
    'promo_seasonal': 'OUTLET_OPEN',      # 季节→OPEN
    'promo_bbq': 'OUTLET_OPEN',           # 烧烤→OPEN
    'promo_package': 'OUTLET_OPEN',       # 套餐→OPEN
}

# 关键词逻辑
KW_FALLBACK = {
    '粽子': 'OUTLET_YUAN', '礼盒': 'OUTLET_YUAN', '礼品': 'OUTLET_YUAN',
    '礼篮': 'OUTLET_YUAN', '伴手': 'OUTLET_YUAN',
    '火锅': 'OUTLET_OPEN', '海鲜': 'OUTLET_OPEN', '小龙虾': 'OUTLET_OPEN',
    '龙虾': 'OUTLET_OPEN', '蟹': 'OUTLET_OPEN', '虾': 'OUTLET_OPEN',
    '啤酒': 'OUTLET_BEER_SOCIETY', '青岛': 'OUTLET_BEER_SOCIETY',
    '雪花': 'OUTLET_BEER_SOCIETY', '喜力': 'OUTLET_BEER_SOCIETY',
    '红酒': 'OUTLET_OPEN', '干红': 'OUTLET_OPEN', '解百纳': 'OUTLET_OPEN',
    '下午茶': 'OUTLET_YUAN', '甜品': 'OUTLET_YUAN',
    '蛋糕': 'OUTLET_YUAN', '面包': 'OUTLET_YUAN',
    '轻食': 'OUTLET_OPEN', '沙拉': 'OUTLET_OPEN', '果汁': 'OUTLET_OPEN',
    '鲜榨': 'OUTLET_OPEN', '柠檬水': 'OUTLET_OPEN', '冰美式': 'OUTLET_OPEN',
    '南瓜汤': 'OUTLET_OPEN', '番茄浓汤': 'OUTLET_OPEN',
    '鸡胸': 'OUTLET_OPEN', '三文鱼': 'OUTLET_OPEN', '牛蛙': 'OUTLET_OPEN',
    '小笼': 'OUTLET_YUXI', '生煎': 'OUTLET_YUXI', '春卷': 'OUTLET_YUXI',
    '熏鱼': 'OUTLET_YUXI', '白肉': 'OUTLET_YUXI', '蚕豆': 'OUTLET_YUXI',
    '炒饭': 'OUTLET_YUXI', '拌面': 'OUTLET_YUXI', '意面': 'OUTLET_OPEN',
    '跨年': 'OUTLET_OPEN', '情人节': 'OUTLET_OPEN', '女神节': 'OUTLET_OPEN',
    '除夕': 'OUTLET_BANQUET',
}

new_rels = []
still_missed = []

for p in unprod:
    pid = p['id']
    cat = (p.get('properties',{}).get('category','') or p.get('category','')).lower().strip()
    name = p.get('name','')
    
    target = CAT_FALLBACK.get(cat)
    
    if not target:
        for kw, oid in KW_FALLBACK.items():
            if kw in name:
                target = oid
                break
    
    if not target:
        # 竞对/财务类数据不归属营业点
        if any(x in cat for x in ['outlet_ptd','segment_ptd','financial','analysis','daily','policy','honor','tag','italian']):
            still_missed.append((cat, name))
            continue
        # IC酒店名
        if '洲际' in name or '柏悦' in name or 'W酒店' in name or '皇冠' in name:
            target = 'OUTLET_COMPETITOR'
        # 啤酒兜底
        elif '啤酒' in name or '青岛' in name or '雪花' in name or '喜力' in name:
            target = 'OUTLET_BEER_SOCIETY'
        # 红酒兜底
        elif '红酒' in name or '干红' in name or '长城' in name:
            target = 'OUTLET_OPEN'
        else:
            still_missed.append((cat, name))
            continue
    
    key = (pid, 'BELONGS_TO', target)
    if key not in existing:
        new_rels.append({'source_id': pid, 'type': 'BELONGS_TO', 'target_id': target})
        existing.add(key)

if new_rels:
    fbr.extend(new_rels)
    fb['relationships'] = fbr
    shutil.copy2(fp, fp.replace('.json', '_before_final_fix.json'))
    json.dump(fb, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('补充: %d条' % len(new_rels))
else:
    print('无需补充')

print('仍跳过(非营业点产品): %d个' % len(still_missed))
for cat, name in still_missed[:10]:
    print('  %s / %s' % (cat[:15], name[:20]))

# 最终确认
fb2 = json.load(open(fp, encoding='utf-8'))
fbe2 = fb2.get('entities', [])
fbr2 = fb2.get('relationships', [])
belongs = sum(1 for r in fbr2 if r.get('type') == 'BELONGS_TO')
total_rel = len(fbr2)
print()
print('=== 最终状态 ===')
print('节点: %d  关系: %d  BELONGS_TO: %d  密度: %.2f' % (len(fbe2), total_rel, belongs, total_rel/len(fbe2)))

from collections import Counter
by_outlet = Counter()
for r in fbr2:
    if r.get('type') == 'BELONGS_TO':
        by_outlet[r.get('target_id','')] += 1

print()
print('7+2营业点产品分配:')
oid_name = {
    'OUTLET_OPEN':'OPEN全日','OUTLET_YUXI':'御玺','OUTLET_BACIO':'BACIO',
    'OUTLET_YUAN':'大堂吧','OUTLET_BANQUET':'宴会','OUTLET_ROOM_DINING':'送餐',
    'OUTLET_BEER_SOCIETY':'啤酒荟','OUTLET_TAKEOUT':'外卖','OUTLET_BAZAAR':'Bazaar',
    'OUTLET_COMPETITOR':'竞对',
}
for oid in ['OUTLET_OPEN','OUTLET_YUXI','OUTLET_BACIO','OUTLET_YUAN',
            'OUTLET_BANQUET','OUTLET_ROOM_DINING','OUTLET_BEER_SOCIETY',
            'OUTLET_TAKEOUT','OUTLET_BAZAAR','OUTLET_COMPETITOR']:
    c = by_outlet.get(oid, 0)
    print('  %-22s %4d个  %s' % (oid, c, oid_name.get(oid, '')))
