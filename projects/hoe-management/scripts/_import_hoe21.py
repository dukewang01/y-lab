#!/usr/bin/env python3
import openpyxl, json, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
indir = r'C:\Users\Duke Wang\.openclaw\media\inbound'
fn = [f for f in os.listdir(indir) if 'HOE00021' in f or '7e7d8a5d' in f][0]
fp = os.path.join(indir, fn)
wb = openpyxl.load_workbook(fp, data_only=True)
ws = wb.active

items = []
for r in range(4, ws.max_row+1):
    seq = ws.cell(r, 1).value
    if not seq and not ws.cell(r, 2).value: continue
    name = str(ws.cell(r, 2).value or '').strip()
    if not name or name == '合计：': continue
    brand = str(ws.cell(r, 3).value or '').strip()
    spec = str(ws.cell(r, 4).value or '').strip()
    maker = str(ws.cell(r, 5).value or '').strip()
    qty_str = str(ws.cell(r, 6).value or '0').strip()
    try: qty = int(float(qty_str))
    except: qty = 0
    if qty > 0 or name:
        items.append({'name': name, 'brand': brand, 'spec': spec, 'maker': maker, 'qty': qty})

total_qty = sum(item['qty'] for item in items)
print(f'中厨房合同: {len(items)}项, {total_qty}件')

brands = Counter()
for item in items:
    brands[item['brand']] += item['qty']
print(f'\n品牌Top 10:')
for b, q in brands.most_common(10):
    print(f'  {b:12s}: {q}件')

makers = Counter()
for item in items:
    makers[item['maker']] += item['qty']
print(f'\n供应商Top 10:')
for m, q in makers.most_common(10):
    print(f'  {m[:20]:20s}: {q}件')

# 分类
cats = Counter()
for item in items:
    n = item['name']
    if any(k in n for k in ['刀','剑','刃','刨','刮','锉']): cat = '刀具'
    elif any(k in n for k in ['锅','鼎','平底']): cat = '锅具'
    elif any(k in n for k in ['盆','碗','碟','盘','盅','壶','杯']): cat = '容器'
    elif any(k in n for k in ['筛','漏','滤','网']): cat = '筛漏'
    elif any(k in n for k in ['盒','箱','桶','筐','篮']): cat = '储物'
    elif any(k in n for k in ['勺','铲','匙','夹','钳','叉','签']): cat = '厨具'
    elif any(k in n for k in ['机','器','炉','柜','车']): cat = '设备'
    elif any(k in n for k in ['板','垫','布','纸','膜']): cat = '耗材'
    elif any(k in n for k in ['架','挂']): cat = '架子'
    elif any(k in n for k in ['模','印']): cat = '模具'
    else: cat = '其他'
    cats[cat] += item['qty']
print(f'\n分类:')
for c, q in cats.most_common():
    print(f'  {c:6s}: {q}件')

# 入库
fb_fp = os.path.join(BASE, "fb_graph.json")
fb = json.load(open(fb_fp, 'r', encoding='utf-8'))
es = fb.get('entities', [])
existing_ids = set(e.get('id','') for e in es)

# 清理之前可能存在的
for prefix in ['HOE_VENDOR_CHINESE_', 'HOE_CONTRACT_CHINESE_', 'HOE_ITEM_CHINESE_']:
    es[:] = [e for e in es if not e.get('id','').startswith(prefix)]
existing_ids = set(e.get('id','') for e in es)

hoes = [
    {"id": "HOE_VENDOR_CHINESE_001", "type": "hoe_vendor", "label": "中厨房综合供应商",
     "category": "设备器具", "status": "合作中", "import_date": "2026-05-14"},
    {"id": "HOE_CONTRACT_CHINESE_001", "type": "hoe_contract", "label": "HOE00021 中厨房合同清单",
     "vendor_id": "HOE_VENDOR_CHINESE_001", "contract_type": "供应合同",
     "category": "设备器具", "status": "合作中", "items_count": len(items),
     "total_qty": total_qty, "file": "HOE00021中厨房合同清单.xlsx", "import_date": "2026-05-14"},
]
for h in hoes:
    es.append(h); existing_ids.add(h['id'])

for i, item in enumerate(items):
    iid = f"HOE_ITEM_CHINESE_{i+1:03d}"
    es.append({
        "id": iid, "type": "hoe_item", "label": item['name'][:40],
        "contract_id": "HOE_CONTRACT_CHINESE_001",
        "vendor_id": "HOE_VENDOR_CHINESE_001",
        "brand": item['brand'], "spec": item['spec'][:60],
        "maker": item['maker'][:40], "qty": item['qty'],
    })

fb['entities'] = es
json.dump(fb, open(fb_fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\nFB-HOE总实体: {len(es)}')
print(f'+ 2 + {len(items)} = {2+len(items)}')
