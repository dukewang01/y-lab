import json, openpyxl
from datetime import datetime

xlsx = 'C:\\Users\\Duke Wang\\.openclaw\\knowledge_center\\media\\Daily_Revenue_Report_2026.05.06.xlsx'
wb = openpyxl.load_workbook(xlsx, data_only=True)

# ===== 1. 从 Actual 表读取关键数据 =====
ws = wb['Actual']

def find_val(ws, row_start, row_end, label_keyword, col_idx=1):
    """在指定行范围内，按标签找值（第1列标签，第2列开始数据）"""
    for r in range(row_start, min(row_end+1, ws.max_row+1)):
        cell = str(ws.cell(r, 1).value or '').strip()
        if label_keyword.lower() in cell.lower():
            vals = []
            for c in range(2, min(ws.max_column+1, 10)):
                v = ws.cell(r, c).value
                vals.append(v if v is not None else '')
            return vals
    return None

# 定位关键行——基于报表的固定结构
data = {
    'date': '2026-05-06',
    'rooms': {},
    'food': {},
    'fb_total': {},
    'outlets': {}
}

# 手动解析行列（知道报表结构）
# ROOM行: 第12行左右
for r in range(1, ws.max_row+1):
    a = str(ws.cell(r, 1).value or '')
    b1 = ws.cell(r, 2).value  # 今日实际
    b2 = ws.cell(r, 3).value  # 今日预算
    b3 = ws.cell(r, 4).value  # 今日上年
    c1 = ws.cell(r, 5).value  # MTD实际
    c2 = ws.cell(r, 6).value  # MTD预算
    c3 = ws.cell(r, 7).value  # MTD上年
    
    if 'ROOM SOLD' in a:
        data['rooms']['sold'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'TOTAL ROOMS REVENUE' in a:
        data['rooms']['revenue'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif '% Occupancy' in a:
        data['rooms']['occupancy'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'AVERAGE ROOM RATE' in a:
        data['rooms']['adr'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'REVPAR' in a:
        data['rooms']['revpar'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'SERVICE CHARGE' in a and 'ROOM REVENUE' not in a and 'ROOM' not in a:
        pass
    elif 'ROOM REVENUE' in a and a.strip().startswith('ROOM'):
        data['rooms']['total_room'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'TOTAL FOOD REVENUE' in a or ('FOOD REVENUE' in a and 'TOTAL' in a):
        data['food']['total_food_revenue'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'TOTAL BEVERAGE REVENUE' in a or ('BEVERAGE REVENUE' in a and 'TOTAL' in a):
        data['food']['total_beverage_revenue'] = {'today': b1, 'budget': b2, 'ly': b3, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}
    elif 'TOTAL F&B  合计' in a or ('TOTAL F&B' in a and '合计' in a):
        data['fb_total'] = {'today': b1, 'mtd': c1, 'mtd_budget': c2, 'mtd_ly': c3}

print('=== 解析结果 ===')
for section, vals in data.items():
    if section == 'date':
        continue
    print(f'\n--- {section} ---')
    for k, v in vals.items():
        print(f'  {k}: {json.dumps(v)}')

# 确认房间营收
if 'revenue' in data.get('rooms', {}):
    r = data['rooms']['revenue']
    print(f'\n客房营收今日: {r.get("today")} / MTD: {r.get("mtd")}')
print(f'出租率今日: {data.get("rooms",{}).get("occupancy",{}).get("today")}')
print(f'ADR今日: {data.get("rooms",{}).get("adr",{}).get("today")}')
