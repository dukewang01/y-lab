import json, openpyxl

xlsx = 'C:\\Users\\Duke Wang\\.openclaw\\knowledge_center\\media\\Daily_Revenue_Report_2026.05.06.xlsx'
wb = openpyxl.load_workbook(xlsx, data_only=True)

ws = wb['Actual']

def parse_row(ws, label_keyword, val_col_start=5, val_col_end=7):
    """在D列找标签，E-G列取值：今日/预算/上年"""
    for r in range(1, ws.max_row+1):
        a = str(ws.cell(r, 4).value or '').strip()
        if label_keyword.lower() in a.lower():
            vals = []
            for c in range(val_col_start, val_col_end+1):
                v = ws.cell(r, c).value
                vals.append(v if v is not None else None)
            return vals
    return None

data = {}

# === 客房数据 ===
data['rooms_sold'] = parse_row(ws, 'ROOM SOLD')
data['occupancy_pct'] = parse_row(ws, '% Occupancy')
data['revpar'] = parse_row(ws, 'REVPAR')
data['adr'] = parse_row(ws, 'AVERAGE ROOM RATE')
data['total_rooms_rev'] = parse_row(ws, 'TOTAL ROOMS REVENUE')
data['service_charge'] = parse_row(ws, 'SERVICE CHARGE')
data['room_revenue'] = parse_row(ws, 'ROOM REVENUE')
data['guest_count'] = parse_row(ws, 'GUEST COUNT')

# 找F&B餐厅数据
data['banquet_rev'] = parse_row(ws, 'BANQUET AND CONFERENCE')
data['open_rev'] = parse_row(ws, 'OPEN')  # 注意可能匹配到其他
data['yuxi_rev'] = parse_row(ws, 'YUXI')
data['bacio_rev'] = parse_row(ws, 'BACIO')
data['beer_rev'] = parse_row(ws, 'BEER SOCIETY')
data['yuan_rev'] = parse_row(ws, 'YUAN')
data['room_service_rev'] = parse_row(ws, 'ROOM SERVICE')
data['total_food_rev'] = parse_row(ws, 'TOTAL FOOD REVENUE')

# 找F&B的今日封面数
data['open_covers'] = parse_row(ws, 'OPEN')  # 会重复，需精确定位
data['banquet_covers'] = parse_row(ws, 'BANQUET AND CONFERENCE')
data['yuxi_covers'] = parse_row(ws, 'YUXI')
data['total_covers'] = parse_row(ws, 'TOTAL FOOD COVERS')

print('=== 5月6日营收数据 ===')
print()
print('--- 客房 ---')
for k in ['rooms_sold','occupancy_pct','revpar','adr','total_rooms_rev','service_charge','room_revenue','guest_count']:
    v = data.get(k)
    if v:
        print(f'  {k}: 今日={v[0]}, 预算={v[1]}, 上年={v[2]}')
    else:
        print(f'  {k}: 未找到')

print()
print('--- F&B (今日实际) ---')
for k in ['banquet_rev','open_rev','yuxi_rev','bacio_rev','beer_rev','yuan_rev','room_service_rev','total_food_rev']:
    v = data.get(k)
    if v:
        print(f'  {k}: {v[0]}')
    else:
        print(f'  {k}: 未找到')

print()
print('--- 封面数 ---')
data['total_covers'] = parse_row(ws, 'TOTAL FOOD COVERS')
if data['total_covers']:
    print(f'  total_covers: 今日={data["total_covers"][0]}')

# 也看F&B表
ws2 = wb['F&B']
print()
print('=== F&B汇总表摘录 ===')
for r in range(1, min(ws2.max_row+1, 50)):
    vals = []
    for c in range(1, min(ws2.max_column+1, 10)):
        v = ws2.cell(r, c).value
        vals.append(str(v)[:20] if v is not None else '')
    line = '\t'.join(vals)
    print(line)
