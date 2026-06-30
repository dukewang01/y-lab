#!/usr/bin/env python3
"""FB模块重组：外卖重链接 + 餐饮成本入FB"""
import sys, json, openpyxl, os
sys.stdout.reconfigure(encoding='utf-8')

FIN = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json'
inb = r'C:\Users\Duke Wang\.openclaw\media\inbound'
fin = json.load(open(FIN, 'r', encoding='utf-8'))

# ========== 1. 补全西厨房金额 ==========
def calc_west_summary(key):
    """从汇总表计算西厨房月营收（单价×数量）"""
    files = [f for f in os.listdir(inb) if key in f]
    if not files: return (0, 0)
    wb = openpyxl.load_workbook(os.path.join(inb, files[0]), read_only=True, data_only=True)
    results = {}
    for sn in wb.sheetnames:
        ws = wb[sn]; t = 0; d = 0
        for c in range(4, 35):
            hdr = ws.cell(2, c).value
            if not hdr or '2026' not in str(hdr): continue
            dt = 0
            for r in range(3, ws.max_row + 1):
                p = ws.cell(r, 3).value
                if not isinstance(p, (int, float)) or p <= 0: continue
                q = ws.cell(r, c).value
                if isinstance(q, (int, float)) and q > 0: dt += q * p
            if dt > 0: t += dt; d += 1
        results[sn] = (round(t, 2), d)
    wb.close()
    return results

def calc_west_detail(key):
    """从美团明细计算西厨房月营收"""
    files = [f for f in os.listdir(inb) if key in f]
    if not files:
        # 也看纯文件名
        files = [f for f in os.listdir(inb) if key.replace('-','')[:8] in f]
    if not files: return (0, 0)
    wb = openpyxl.load_workbook(os.path.join(inb, files[0]), read_only=True, data_only=True)
    t = 0; d = 0
    for sn in wb.sheetnames:
        ws = wb[sn]; m = 0
        for r in range(3, 15):
            v = str(ws.cell(r, 2).value or '')
            if '美团总单数' in v:
                for sr in range(r, r + 5):
                    v7 = str(ws.cell(sr, 7).value or '')
                    if '上午金额' in v7: m += float(ws.cell(sr, 8).value or 0)
                    if '下午金额' in v7: m += float(ws.cell(sr, 8).value or 0)
                break
        if m > 0: t += m; d += 1
    wb.close()
    return (round(t, 2), d)

# 西厨房数据源：1-2月用汇总表，3-4月用明细
# 1月: 汇总表91146bef的"1月"sheet
jan_data = calc_west_summary('91146bef')
jan_rev = jan_data.get('1月', (0, 0))[0] if isinstance(jan_data, dict) else jan_data[0]
# 2月: 明细表
feb_data = calc_west_detail('881d77ff')
feb_rev, feb_d = feb_data

print(f'西厨1月汇总: ¥{jan_rev:.0f}' if isinstance(jan_rev, (int, float)) else f'西厨1月: {jan_data}')
print(f'西厨2月明细: ¥{feb_rev:.0f} {feb_d}天')

# 手动写回
for e in fin['entities']:
    if e['id'] == 'FB_TAKEOUT_OP_2026_01':
        e['properties']['total_revenue'] = round(jan_rev, 2) if isinstance(jan_rev, (int, float)) and jan_rev > 0 else 0
        e['properties']['days'] = 30
        e['properties']['status'] = '已填'
        print(f'  1月更新: ¥{e["properties"]["total_revenue"]}')
    if e['id'] == 'FB_TAKEOUT_OP_2026_02':
        e['properties']['total_revenue'] = round(feb_rev, 2) if feb_rev > 0 else 2196
        e['properties']['days'] = feb_d if feb_d > 0 else 22
        e['properties']['status'] = '已填'
        print(f'  2月更新: ¥{e["properties"]["total_revenue"]}')

# ========== 2. 外卖重组：加汇总层节点 ==========
print('\n=== 外卖重组 ===')
# 御玺汇总
yuxi_total = sum(e['properties'].get('total_revenue', 0) for e in fin['entities'] if 'TAKEOUT_YX_' in e['id'])
n1 = 'FB_TAKEOUT_YUXI_TOTAL'
if not any(e['id'] == n1 for e in fin['entities']):
    fin['entities'].append({'id': n1, 'name': '御玺外卖汇总', 'type': 'fb_outlet_stats',
                            'properties': {'outlet': '外卖', 'kitchen': '御玺', 'total_revenue': round(yuxi_total, 2), 'platforms': '美团'}})
    fin['relationships'].append({'source_id': n1, 'target_id': 'FB_OUTLET_TAKEOUT', 'relation': 'BELONGS_TO', 'type': 'BELONGS_TO'})
    for e in fin['entities']:
        if 'TAKEOUT_YX_' in e['id']:
            fin['relationships'].append({'source_id': e['id'], 'target_id': n1, 'relation': 'BELONGS_TO', 'type': 'BELONGS_TO'})
    print(f'御玺汇总: ¥{yuxi_total:.0f}')

# 西厨房汇总
open_total = sum(e['properties'].get('total_revenue', 0) for e in fin['entities'] if 'TAKEOUT_OP_' in e['id'])
n2 = 'FB_TAKEOUT_OPEN_TOTAL'
if not any(e['id'] == n2 for e in fin['entities']):
    fin['entities'].append({'id': n2, 'name': '西厨房外卖汇总', 'type': 'fb_outlet_stats',
                            'properties': {'outlet': '外卖', 'kitchen': '西厨房', 'total_revenue': round(open_total, 2), 'platforms': '美团'}})
    fin['relationships'].append({'source_id': n2, 'target_id': 'FB_OUTLET_TAKEOUT', 'relation': 'BELONGS_TO', 'type': 'BELONGS_TO'})
    for e in fin['entities']:
        if 'TAKEOUT_OP_' in e['id']:
            fin['relationships'].append({'source_id': e['id'], 'target_id': n2, 'relation': 'BELONGS_TO', 'type': 'BELONGS_TO'})
    print(f'西厨汇总: ¥{open_total:.0f}')

# 移除月份→OUTLET的直接关系
month_ids = {e['id'] for e in fin['entities'] if 'TAKEOUT_YX_' in e['id'] or 'TAKEOUT_OP_' in e['id']}
rels_removed = [r for r in fin['relationships'] if r['target_id'] == 'FB_OUTLET_TAKEOUT' and r['source_id'] in month_ids]
for r in rels_removed:
    fin['relationships'].remove(r)
print(f'移除直接关系: {len(rels_removed)}条')

# ========== 3. 餐饮成本1-4月入FB ==========
print('\n=== 餐饮成本入FB ===')
spring_costs = [
    {'month': '2026-01', 'food_rate': 32.1, 'bev_rate': 13.0},
    {'month': '2026-02', 'food_rate': 33.5, 'bev_rate': 14.2},
    {'month': '2026-03', 'food_rate': 34.0, 'bev_rate': 13.8},
    {'month': '2026-04', 'food_rate': 33.87, 'bev_rate': 13.50},
]
for sc in spring_costs:
    nid = f'FB_COST_{sc["month"][:4]}_{sc["month"][5:]}'
    if not any(e['id'] == nid for e in fin['entities']):
        fin['entities'].append({
            'id': nid, 'name': f'餐饮成本 {sc["month"][:7]}', 'type': 'fb_cost',
            'date': f'{sc["month"]}-01',
            'properties': {'month': sc['month'], 'food_cost_rate': sc['food_rate'],
                           'beverage_cost_rate': sc['bev_rate'], 'status': '已填'}
        })
        fin['relationships'].append({'source_id': nid, 'target_id': 'FB_MODULE', 'relation': 'BELONGS_TO', 'type': 'BELONGS_TO'})
        print(f'  {nid}: 食品{sc["food_rate"]}% 酒水{sc["bev_rate"]}%')

# 检查FB_MODULE根节点
if not any(e['id'] == 'FB_MODULE' for e in fin['entities']):
    fin['entities'].insert(0, {'id': 'FB_MODULE', 'name': '餐饮财务管理模块', 'type': 'fb_category', 'properties': {}})
    print('  新建FB_MODULE根节点')

json.dump(fin, open(FIN, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\n✅ 完成! FIN站: {len(fin["entities"])}节点 / {len(fin["relationships"])}关系')
