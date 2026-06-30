#!/usr/bin/env python3
"""计算西厨房汇总表金额"""
import sys, openpyxl, os, json
sys.stdout.reconfigure(encoding='utf-8')
inb = r'C:\Users\Duke Wang\.openclaw\media\inbound'
FIN = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json'
fin = json.load(open(FIN, 'r', encoding='utf-8'))

for key, month, nid in [
    ('91146bef', '2026-01', 'FB_TAKEOUT_OP_2026_01'),
    ('137da460', '2026-02', 'FB_TAKEOUT_OP_2026_02'),
    ('293b2f91', '2026-03', 'FB_TAKEOUT_OP_2026_03'),
]:
    files = [f for f in os.listdir(inb) if key in f]
    if not files:
        print(f'{key}: 文件未找到')
        continue
    wb = openpyxl.load_workbook(os.path.join(inb, files[0]), read_only=True, data_only=True)
    t = 0; d = 0
    for sn in wb.sheetnames:
        ws = wb[sn]
        dt = 0
        for r in range(3, ws.max_row + 1):
            price = ws.cell(r, 3).value
            if not isinstance(price, (int, float)) or price <= 0:
                continue
            for c in range(4, 40):
                qty = ws.cell(r, c).value
                hdr = ws.cell(2, c).value
                if isinstance(qty, (int, float)) and qty > 0 and hdr and '2026' in str(hdr):
                    dt += qty * price
        if dt > 0:
            t += dt
            d += 1
    wb.close()
    avg = round(t / d, 2) if d else 0
    print(f'{month}: 总¥{t:.0f} {d}天 日均¥{avg:.0f}')
    
    for e in fin['entities']:
        if e['id'] == nid:
            old = e['properties'].get('total_revenue', 0)
            if old == 0:
                e['properties']['total_revenue'] = round(t, 2)
                e['properties']['days'] = d
                e['properties']['avg_daily_rev'] = avg
                e['properties']['platforms'] = {'美团': round(t, 2)}
                e['properties']['status'] = '已填'
                print(f'  ✅ 已入库')
            else:
                e['properties']['total_revenue'] = round(t, 2)
                e['properties']['days'] = d
                e['properties']['avg_daily_rev'] = avg  
                e['properties']['status'] = '已填(更新)'
                print(f'  ✅ 已更新(原¥{old:.0f}→¥{t:.0f})')
            break

json.dump(fin, open(FIN, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\n完成! {len(fin["entities"])}节点 / {len(fin["relationships"])}关系')
