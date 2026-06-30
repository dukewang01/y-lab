"""
_drr_monthly_parser.py — DRR月度横表解析器
处理"DRR(分餐段)YYYYMM数值版.xlsx"格式（整月数据横排）
入库到 finance_graph.json 作为 DAILY_SNAPSHOT
"""
import json, os, sys, re, openpyxl
from pathlib import Path
from datetime import datetime, date

BASE = Path(__file__).parent.resolve()
GRAPH_PATH = BASE / 'finance_graph.json'

def load_graph():
    if GRAPH_PATH.exists():
        return json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
    return {
        "meta": {
            "name": "Y的财务经营站",
            "hotel": "苏州希尔顿酒店 (Hilton Suzhou)",
            "description": "苏州希尔顿营收日报",
            "version": "1.0",
            "created": date.today().isoformat(),
            "last_updated": date.today().isoformat(),
            "source": "Daily Revenue Report (OnQ系统)"
        },
        "entities": [],
        "relations": []
    }

def save_graph(g):
    GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')

def parse_monthly(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    
    # 找到正确的sheet：匹配年份+月份的sheet名，或最后一个非Sheet1的sheet
    fname = Path(filepath).name
    match = re.search(r'(20\d{2})(\d{2})', fname)
    ym_target = match.group(1) + match.group(2) if match else None
    
    sheet = None
    for sn in wb.sheetnames:
        if sn == ym_target:
            sheet = wb[sn]
            break
    if sheet is None and ym_target:
        # fallback: 读第一个非Sheet1的sheet
        for sn in wb.sheetnames:
            if sn.lower() != 'sheet1':
                sheet = wb[sn]
                break
    if sheet is None:
        sheet = wb[wb.sheetnames[0]]
    
    print('  Sheet: %s' % sheet.title)

    # 读日期: Row 3, 列D起
    dates = []
    for c in range(4, sheet.max_column + 1):
        v = sheet.cell(3, c).value
        if isinstance(v, datetime):
            dates.append(v)
        elif isinstance(v, str):
            try:
                dates.append(datetime.strptime(v.strip()[:10], '%Y-%m-%d'))
            except:
                continue
        elif isinstance(v, (int, float)):
            if v > 40000:  # Excel serial date
                from datetime import datetime as dt2
                try:
                    dates.append(dt2.fromordinal(dt2(1899,12,30).toordinal() + int(v)))
                except:
                    continue
        else:
            if len(dates) > 3:
                break  # 连续空列后停止
    if len(dates) < 2:
        print('⚠ 未找到日期列')
        return []
    print('  日期范围: %s ~ %s (%d天)' % (dates[0].strftime('%m/%d'), dates[-1].strftime('%m/%d'), len(dates)))

    # 行标签映射
    row_map = {}
    for r in range(5, sheet.max_row + 1):
        label = sheet.cell(r, 4).value
        if label and isinstance(label, str):
            row_map[label.strip()] = r

    # 字段映射（支持别名）
    field_map = [
        ('ROOM SOLD', 'room_sold', lambda v: int(v) if v else 0),
        ('% Occupancy', 'occ', lambda v: round(v*100, 2) if v else 0),
        ('AVERAGE ROOM RATE', 'arr', lambda v: round(float(v), 2) if v else 0),
        ('REVPAR', 'revpar', lambda v: round(float(v), 2) if v else 0),
        ('NET ROOM REVENUE', 'net_room_revenue', lambda v: round(float(v), 2) if v else 0),
        ('ROOM REVENUE', 'net_room_revenue', lambda v: round(float(v), 2) if v else 0),
        ('TOTAL ROOMS REVENUE', 'room_revenue_total', lambda v: round(float(v), 2) if v else 0),
    ]

    results = []
    for i, d in enumerate(dates):
        col = 4 + i
        props = {
            'date': d.strftime('%Y-%m-%d'),
            'hotel': '苏州希尔顿酒店 (Hilton Suzhou)',
        }
        for label, field, conv in field_map:
            r = row_map.get(label)
            if r:
                v = sheet.cell(r, col).value
                try:
                    props[field] = conv(v)
                except:
                    pass
        results.append((d, props))
    return results

def process_one(filepath):
    print('📄 解析: %s' % Path(filepath).name)
    
    g = load_graph()
    existing = {e.get('date','') for e in g['entities'] if e.get('type') == 'DAILY_SNAPSHOT'}
    
    entries = parse_monthly(filepath)
    if not entries:
        return 0
    
    new_n, upd_n = 0, 0
    for d, props in entries:
        eid = 'DAILY_%s' % d.strftime('%Y_%m_%d')
        date_str = d.strftime('%Y-%m-%d')
        
        if date_str in existing:
            found = False
            for e in g['entities']:
                if e.get('id') == eid:
                    # 只更新空值字段，保留已有值
                    for k, v in props.items():
                        if v and (k not in e['properties'] or not e['properties'].get(k)):
                            e['properties'][k] = v
                    found = True
                    break
            if found:
                upd_n += 1
            else:
                # 记录存在但实体缺失（异常情况），直接追加
                g['entities'].append({
                    'id': eid, 'type': 'DAILY_SNAPSHOT',
                    'name': '日报 %s' % date_str, 'date': date_str,
                    'properties': props,
                })
                new_n += 1
        else:
            g['entities'].append({
                'id': eid, 'type': 'DAILY_SNAPSHOT',
                'name': '日报 %s' % date_str, 'date': date_str,
                'properties': props,
            })
            existing.add(date_str)
            new_n += 1
    
    g['meta']['last_updated'] = date.today().isoformat()
    g['meta']['entity_count'] = len(g['entities'])
    save_graph(g)
    
    sold = [p.get('room_sold', 0) for _, p in entries if p.get('room_sold')]
    revs = [p.get('net_room_revenue', 0) for _, p in entries if p.get('net_room_revenue')]
    arrs = [p.get('arr', 0) for _, p in entries if p.get('arr')]
    
    avg_s = sum(sold)/len(sold) if sold else 0
    avg_a = sum(arrs)/len(arrs) if arrs else 0
    tot_r = sum(revs) if revs else 0
    
    print('  ✅ %d天 (新%d/更新%d) | 均售%.0f间 | 均价¥%.0f | 月总¥%.0f' % (
        len(entries), new_n, upd_n, avg_s, avg_a, tot_r))
    return len(entries)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_one(sys.argv[1])
