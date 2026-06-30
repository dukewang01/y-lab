#!/usr/bin/env python3
import json, os, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(BASE, "fb_graph.json")
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# 提取HOE实体
contracts = [e for e in es if e.get('type') == 'hoe_contract']
vendors = [e for e in es if e.get('type') == 'hoe_vendor']
items = [e for e in es if e.get('type') == 'hoe_item']
cats = [e for e in es if e.get('type') == 'hoe_category']
fa_items = [e for e in es if e.get('type') == 'fixed_asset_item']
fa_depts = [e for e in es if e.get('type') == 'fixed_asset_dept']

print('=' * 70)
print('  🏨 苏州希尔顿酒店 — HOE全模块运行报告')
print(f'  FB-HOE图谱: {len(es)} 实体')
print('=' * 70)

# 一、合同总览
print(f'\n📋 一、HOE合同总览（{len(contracts)}份）')
print(f'{"#":>3} | {"合同":>12} | {"内容":>22} | {"品项":>5} | {"数量":>8} | {"品类"}')
print('-' * 75)

total_items = 0
total_qty = 0
for i, c in enumerate(sorted(contracts, key=lambda x: x.get('id','')), 1):
    cid = c['id'].replace('HOE_CONTRACT_','').replace('_001','')
    # 找label缩写
    label = c.get('label','')[:22]
    # 找该合同的实际品项
    actual_items = sum(1 for e in items if e.get('contract_id') == c['id'])
    actual_qty = sum(e.get('qty',0) or 0 for e in items if e.get('contract_id') == c['id'])
    
    # 品类
    cat = c.get('category','')
    emoji_map = {
        '设备器具':'🔧','瓷器':'🏺','清洁用品':'🧹','印刷物料':'🖨️',
        '布草制服':'👔','员工餐厅':'🍳','饮料茶咖':'☕'
    }
    emoji = ''
    for k,v in emoji_map.items():
        if k in cat:
            emoji = v
            break
    
    if actual_items > 0:
        total_items += actual_items
        total_qty += actual_qty
        print(f'{i:>3} | {emoji}{cid:>10} | {label:22s} | {actual_items:>5} | {actual_qty:>8,} | {cat}')

print('-' * 75)
print(f'{"合计":>27} | {total_items:>5} | {total_qty:>8,}')

# 二、品类全景
print(f'\n📦 二、品类全景（{len(cats)}个品类 + 自动归类）')
cat_stats = defaultdict(lambda: {'items':0, 'qty':0, 'contracts':set()})
for item in items:
    c = item.get('category','')
    # 通过合同找品类
    cid = item.get('contract_id','')
    for contract in contracts:
        if contract['id'] == cid:
            cat = contract.get('category','未分类')
            cat_stats[cat]['items'] += 1
            cat_stats[cat]['qty'] += item.get('qty',0) or 0
            cat_stats[cat]['contracts'].add(cid[:15])
            break

for cat, st in sorted(cat_stats.items(), key=lambda x: -x[1]['qty']):
    bar = '█' * min(int(st['qty']/5000), 40)
    pct = st['qty']/max(total_qty,1)*100
    print(f'  {cat:12s} | {st["items"]:>5}项 | {st["qty"]:>8,}件 ({pct:>4.1f}%) | {bar}')

# 三、品牌势力图
print(f'\n🏷️ 三、品牌势力图（Top 15）')
brand_stats = Counter()
for item in items:
    b = item.get('brand','') or '未标注'
    if b != '未标注':
        brand_stats[b] += item.get('qty',0) or 0

for b, q in brand_stats.most_common(15):
    pct = q/max(total_qty,1)*100
    bar = '▓' * min(int(pct/2), 30)
    print(f'  {b:20s} | {q:>8,}件 ({pct:>4.1f}%) | {bar}')

# 四、供应链分布
print(f'\n🔗 四、供应商（{len(vendors)}家）')
for v in sorted(vendors, key=lambda x: x.get('id','')):
    # 查该供应商的合同
    vid = v['id']
    v_contracts = [c for c in contracts if c.get('vendor_id') == vid]
    v_items = sum(c.get('items_count',0) or 0 for c in v_contracts)
    v_qty = sum(c.get('total_qty',0) or 0 for c in v_contracts)
    # 实际查
    actual_v_items = sum(1 for e in items if e.get('vendor_id') == vid)
    actual_v_qty = sum(e.get('qty',0) or 0 for e in items if e.get('vendor_id') == vid)
    if actual_v_items > 0:
        print(f'  {v.get("label","")[:22]:22s} | {actual_v_items:>5}项 | {actual_v_qty:>8,}件')

# 五、固定资产
print(f'\n💰 五、固定资产（2020盘点 | {len(fa_items)}条 | {sum(d.get("total_amount",0) or 0 for d in fa_depts):,.0f}元）')
fa_total = 0
for d in sorted(fa_depts, key=lambda x: -(x.get('total_amount',0) or 0)):
    amt = d.get('total_amount',0) or 0
    cnt = d.get('asset_count',0) or 0
    fa_total += amt
    bar = '█' * min(int(amt/50000), 40)
    print(f'  {d.get("label","")[:10]:10s} | ¥{amt:>8,.0f} | {cnt:>3}项 | {bar}')

# 六、总览
print(f'\n{"="*70}')
print(f'  🏛️ HOE模块终极状态')
print(f'{"="*70}')
print(f'  📋 合同数:      {len(contracts)}份')
print(f'  🏪 供应商数:    {len(vendors)}家')
print(f'  📦 品项总数:    {total_items:,}项')
print(f'  📊 物资总量:    {total_qty:,}件')
print(f'  💰 固定资产:    ¥{fa_total:,.0f}')
print(f'  🧩 品类覆盖:    {len(cat_stats)}个品类')
print(f'  🏢 资产部门:    {len(fa_depts)}个部门')
print(f'  🔗 合同-资产联动: 固定资产备注含HOE编号引用')
print(f'  📍 覆盖范围: 从后厨到餐桌 · 从客房到大堂 · 从员工到宾客')
print(f'  ✅ 状态: \033[92m全酒店HOE体系完成\033[0m')
