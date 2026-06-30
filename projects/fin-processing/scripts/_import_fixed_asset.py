#!/usr/bin/env python3
import openpyxl, json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
indir = r'C:\Users\Duke Wang\.openclaw\media\inbound'
fn = [f for f in os.listdir(indir) if 'HOE' in f and ('b2ac6208' in f or '盘点' in f)][0]
fp = os.path.join(indir, fn)
wb = openpyxl.load_workbook(fp, data_only=True)

# 入库到FB中专门的fixed_asset类型
fb_fp = os.path.join(BASE, "fb_graph.json")
fb = json.load(open(fb_fp, 'r', encoding='utf-8'))
es = fb.get('entities', [])
existing_ids = set(e.get('id','') for e in es)

# 清理旧资产数据
for prefix in ['FA_DEPT_', 'FA_ITEM_', 'FA_SUMMARY']:
    es[:] = [e for e in es if not e.get('id','').startswith(prefix)]
existing_ids = set(e.get('id','') for e in es)

# 1. 总表入库
summary_sheets = {
    '客房部': {'sheet': '客房部', 'total': 0},
    '餐饮部': {'sheet': '餐饮部', 'total': 0},
    '前厅部': {'sheet': '前厅部', 'total': 0},
    '工程部': {'sheet': '工程部', 'total': 0},
    '商务发展部': {'sheet': '商务发展部', 'total': 0},
    '人事部': {'sheet': '人事部', 'total': 0},
    '财务部': {'sheet': '财务部', 'total': 0},
    'IT': {'sheet': 'IT', 'total': 0},
    '行政办': {'sheet': '行政办', 'total': 0},
    '安全保障部': {'sheet': '安全保障部', 'total': 0},
}

all_items = []
grand_total = 0

for dept_name, info in summary_sheets.items():
    ws = wb[info['sheet']]
    dept_items = []
    dept_total = 0
    
    for r in range(4, ws.max_row+1):
        name = str(ws.cell(r, 2).value or '').strip()
        if not name or name == '合计' or len(name) < 2: continue
        qty = ws.cell(r, 5).value or 0
        price = ws.cell(r, 6).value or 0
        amount = ws.cell(r, 7).value or 0
        try:
            qty = int(float(str(qty)))
            price = float(str(price).replace(',',''))
            amount = float(str(amount).replace(',',''))
        except:
            continue
        if qty == 0 and amount == 0: continue
        
        brand = str(ws.cell(r, 3).value or '').strip()
        model = str(ws.cell(r, 4).value or '').strip()
        location = str(ws.cell(r, 11).value or '').strip()
        hoe_ref = str(ws.cell(r, 14).value or '').strip()
        
        dept_items.append({
            'name': name, 'brand': brand, 'model': model,
            'qty': qty, 'unit_price': round(price,2),
            'amount': round(amount,2),
            'location': location, 'hoe_ref': hoe_ref
        })
        dept_total += amount
    
    info['total'] = round(dept_total, 2)
    info['count'] = len(dept_items)
    grand_total += dept_total
    all_items.extend(dept_items)

# 部门汇总节点
for dept_name, info in summary_sheets.items():
    eid = f"FA_DEPT_{info['sheet']}"
    if eid not in existing_ids:
        es.append({
            "id": eid, "type": "fixed_asset_dept",
            "label": f"{dept_name}固定资产",
            "department": dept_name,
            "asset_count": info.get('count', 0),
            "total_amount": info['total'],
            "source": "HOE固定资产盘点202008"
        })
        existing_ids.add(eid)

# 全域汇总节点
grand_total = round(grand_total, 2)
total_items = len(all_items)
fa_summary = {
    "id": "FA_SUMMARY_202008",
    "type": "fixed_asset_summary",
    "label": "2020年8月酒店固定资产盘点汇总",
    "total_amount": grand_total,
    "total_items": total_items,
    "department_count": len(summary_sheets),
    "date": "2020-08",
    "source": "HOE固定资产盘点202008.xlsx"
}
if fa_summary['id'] not in existing_ids:
    es.append(fa_summary)
    existing_ids.add(fa_summary['id'])

# 各条资产明细
for i, item in enumerate(all_items):
    eid = f"FA_ITEM_{i+1:05d}"
    if eid not in existing_ids:
        es.append({
            "id": eid, "type": "fixed_asset_item",
            "label": item['name'][:40],
            "brand": item['brand'], "model": item['model'][:40],
            "qty": item['qty'], "unit_price": item['unit_price'],
            "amount": item['amount'], "location": item['location'][:30],
            "hoe_ref": item['hoe_ref'][:30],
        })
        existing_ids.add(eid)

# 版本
for v in [e for e in es if e.get('type')=='version' and 'FIN_VER' in e.get('id','')]:
    es.remove(v)
es.append({'id':'FIN_VER_v5_19_FIXED_ASSET','type':'version','label':'FIN v5.19 - HOE固定资产盘点全量入库'})

fb['entities'] = es
json.dump(fb, open(fb_fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'=== 固定资产盘点入库完成 ===')
print(f'总资产: ¥{grand_total:,.2f}')
print(f'总条目: {total_items}条')
print(f'FB-HOE总实体: {len(es)}')
print(f'\n各部门分布:')
for dept_name, info in sorted(summary_sheets.items(), key=lambda x: -x[1]['total']):
    print(f'  {dept_name:8s}: ¥{info["total"]:>8,.2f}  ({info.get("count",0)}项)')
