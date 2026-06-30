#!/usr/bin/env python3
import json, os, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(BASE, "fb_graph.json")
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# 提取所有HOE实体
hoe_contracts = [e for e in es if e.get('type') == 'hoe_contract']
hoe_vendors = [e for e in es if e.get('type') == 'hoe_vendor']
hoe_items = [e for e in es if e.get('type') == 'hoe_item']
hoe_cats = [e for e in es if e.get('type') == 'hoe_category']
fa_items = [e for e in es if e.get('type') == 'fixed_asset_item']
fa_depts = [e for e in es if e.get('type') == 'fixed_asset_dept']

print('=' * 70)
print('  🏨 苏州希尔顿酒店 — 餐饮HOE全资产报告')
print('  2026-05-14 15:56')
print('=' * 70)

# ====== 1. 合同全景 ======
print(f'\n📋 一、HOE合同总览（{len(hoe_contracts)}份）')
print(f'{"合同编号":>15} | {"品项":>5} | {"总数量":>8} | {"核心品牌"}')
print('-' * 60)
grand_items = 0
grand_qty = 0
for c in sorted(hoe_contracts, key=lambda x: x.get('id','')):
    cid = c['id']
    items = c.get('items_count', 0) or 0
    qty = c.get('total_qty', 0) or 0
    # 从该合同的实际item数
    actual_items = sum(1 for e in hoe_items if e.get('contract_id') == cid)
    actual_qty = sum(e.get('qty',0) or 0 for e in hoe_items if e.get('contract_id') == cid)
    
    label = c.get('label','')[:25]
    # 找品牌
    brand_set = set()
    for item in hoe_items:
        if item.get('contract_id') == cid and item.get('brand',''):
            brand_set.add(item['brand'])
    brands = ', '.join(list(brand_set)[:3])
    
    display_items = actual_items or items
    display_qty = actual_qty or qty
    grand_items += display_items
    grand_qty += display_qty
    
    print(f'{label:15s} | {display_items:>5} | {display_qty:>8,} | {brands}')

print('-' * 60)
print(f'{"合计":>15} | {grand_items:>5} | {grand_qty:>8,}')

# ====== 2. 品牌供应链透视 ======
print(f'\n🏷️ 二、品牌供应链透视')
# 按品牌聚合各合同
brand_contracts = defaultdict(lambda: defaultdict(int))
for item in hoe_items:
    brand = item.get('brand','') or '未知'
    cid = item.get('contract_id','')
    qty = item.get('qty',0) or 0
    brand_contracts[brand][cid] += qty

total_brand_qty = Counter()
for brand, contracts in brand_contracts.items():
    total_brand_qty[brand] = sum(contracts.values())

print(f'Top 15 品牌（按数量）:')
print(f'{"品牌":>18} | {"数量":>8} | {"涉及合同":>8} | {"品类"}')
print('-' * 65)
brand_cat_map = defaultdict(set)
for item in hoe_items:
    b = item.get('brand','') or '未知'
    # 通过合同ID映射到品类
    for c in hoe_contracts:
        if c['id'] == item.get('contract_id',''):
            pass

for brand, qty in total_brand_qty.most_common(15):
    contracts = brand_contracts[brand]
    contract_names = []
    for cid in contracts:
        for c in hoe_contracts:
            if c['id'] == cid:
                contract_names.append(c['label'][:15])
                break
    cat_guess = ''
    if 'WMF' in brand: cat_guess = '餐具'
    elif 'Eurochef' in brand: cat_guess = '厨具'
    elif 'Tiger' in brand: cat_guess = '自助餐'
    elif 'Riedel' in brand or 'C&S' in brand or 'Stolzle' in brand: cat_guess = '玻璃器皿'
    elif '金宝' in brand or 'trust' in brand or '苏荣' in brand: cat_guess = '管事用品'
    elif '林广' in brand: cat_guess = '不锈钢'
    elif '中金' in brand: cat_guess = '瓷器'
    elif '塚一郎' in brand: cat_guess = '日料刀具'
    elif '和式' in brand: cat_guess = '日韩餐具'
    elif '日升' in brand or '振能' in brand: cat_guess = '中厨'
    elif 'Lucky' in brand: cat_guess = '餐具'
    elif 'Pufei' in brand or 'JW' in brand: cat_guess = '酒吧'
    
    print(f'{brand:>18} | {qty:>8,} | {len(contracts):>8}份 | {cat_guess}')

# ====== 3. 按品类聚合 ======
print(f'\n📦 三、品类结构')
category_map = {
    '玻璃器皿': ['Riedel','C&S','Stolzle','Arcoroc','bormioli'],
    '西厨设备': ['Eurochef','Sirman','robot coupe','hatco'],
    '自助餐': ['Tiger','vollrath'],
    '中厨房': ['日升','振能','东兴','三能','HEC'],
    '管事/清洁': ['苏荣','乐柏美','金宝','trust','3M','ETTORE'],
    '餐具(刀叉)': ['WMF','livos'],
    '瓷器': ['中金','高档','定制'],
    '日韩餐具': ['和式','塚一郎','龙虾牌'],
    '酒吧': ['Pufei','JW','林广'],
    '宴会家具': ['北京西科'],
    '不锈钢容器': ['林广'],
}

cat_qty = {}
for cat, brands in category_map.items():
    qty = 0
    for item in hoe_items:
        for b in brands:
            if b.lower() in (item.get('brand','') or '').lower():
                qty += item.get('qty',0) or 0
                break
    if qty > 0:
        cat_qty[cat] = qty

for cat, qty in sorted(cat_qty.items(), key=lambda x: -x[1]):
    bar = '█' * min(int(qty/500), 40)
    print(f'  {cat:12s} | {qty:>8,}件 | {bar}')

# ====== 4. 固定资产关联 ======
print(f'\n💰 四、固定资产（2020年8月盘点）')
print(f'{"部门":>10} | {"金额":>10} | {"项数":>5} | {"典型资产"}')
print('-' * 55)
fa_total = 0
for d in sorted(fa_depts, key=lambda x: -(x.get('total_amount',0) or 0)):
    dept = d.get('label','')[:8]
    amt = d.get('total_amount',0) or 0
    cnt = d.get('asset_count',0) or 0
    fa_total += amt
    # 找典型资产
    dept_items = [e for e in fa_items if e.get('location','') and dept[:2] in e.get('location','')]
    samples = [e.get('label','')[:15] for e in dept_items[:2]] if dept_items else ['']
    sample_str = ', '.join(samples)
    print(f'  {dept:>8} | ¥{amt:>8,.0f} | {cnt:>4}项 | {sample_str}')

print(f'  {"合计":>8} | ¥{fa_total:>8,.0f} |')

# ====== 5. 关键洞察 ======
print(f'\n🔑 五、关键洞察')
print(f'  1. 酒店餐饮HOE覆盖：11份合同，{grand_items}项品目，约{grand_qty:,}件物资')
print(f'  2. 固定资产原值¥{fa_total:,.0f}，餐饮部占¥149万')
print(f'  3. 品牌集中度：WMF(餐具)、Eurochef(厨具)、日升(中厨)三强鼎立')
print(f'  4. 国产vs进口：数量上国产为主，但Riedel/WMF等进口品牌单价高')
print(f'  5. 从后厨到餐桌全链路覆盖：厨具→餐具→器皿→家具→清洁')
print(f'  6. 固定资产与HOE合同有交叉引用（备注栏含HOE编号）')

print(f'\n{"="*70}')
print(f'  FB-HOE图谱: {len(es)} 实体 | 今日从0建成')
print(f'{"="*70}')
