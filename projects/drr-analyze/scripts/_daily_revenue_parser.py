"""
_daily_revenue_parser.py — 财务日报自动解析引擎
用法: 将Daily Revenue Report xlsx放入 media/incoming/ 后运行
      python _daily_revenue_parser.py [文件路径]
      (无参数则自动扫描 incoming/ 中最新未处理的日报)
"""
import json, os, sys, re, openpyxl, datetime
from pathlib import Path

BASE = Path(__file__).parent.resolve()
GRAPH_PATH = BASE / 'finance_graph.json'
INCOMING = Path(r'C:\Users\Duke Wang\.openclaw\media\inbound')
ARCHIVE = Path(r'C:\Users\Duke Wang\.openclaw\media\archived')
PROCESSED_LOG = BASE / '.finance_processed.log'

# 已处理标记
processed = set()
if PROCESSED_LOG.exists():
    processed = set(PROCESSED_LOG.read_text().splitlines())

def load_graph():
    if GRAPH_PATH.exists():
        return json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
    return {"meta":{"name":"Y的财务经营站","display_name":"苏州希尔顿酒店财务经营站","hotel":"苏州希尔顿酒店 (Hilton Suzhou)","description":"苏州希尔顿营收日报","version":"1.0","created":datetime.date.today().isoformat(),"last_updated":datetime.date.today().isoformat(),"source":"Daily Revenue Report (OnQ系统)","entity_count":0,"relation_count":0},"entities":[],"relations":[],"index":{"by_date":{},"by_type":{}}}

def save_graph(g):
    g['meta']['entity_count'] = len(g['entities'])
    g['meta']['relation_count'] = len(g['relations'])
    g['meta']['last_updated'] = datetime.date.today().isoformat()
    GRAPH_PATH.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')

def extract_date(filename):
    """从文件名提取日期，如 Daily_Revenue_Report_2026.04.28 → 2026-04-28"""
    m = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', filename)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None

def parse_actual_sheet(ws, date_str):
    """解析Actual sheet（含缓存值）"""
    rmap = {}  # label → {field}
    for r in range(15, 33):
        label = ws.cell(r, 4).value
        if not label: continue
        label = str(label).strip()
        # 当日/预算/上年/MTD/MTD预算/MTD上年
        rmap[label] = {
            'today': ws.cell(r, 5).value,
            'budget': ws.cell(r, 6).value,
            'ly': ws.cell(r, 7).value,
            'mtd': ws.cell(r, 8).value,
            'mtd_budget': ws.cell(r, 9).value,
            'mtd_ly': ws.cell(r, 10).value,
        }

    # 构建核心行
    def safe(label):
        d = rmap.get(label, {})
        return d

    # entity_id
    eid = f"DAILY_{date_str.replace('-','_')}"
    
    # 当日实体
    today_entity = {
        "id": eid,
        "type": "DAILY_SNAPSHOT",
        "name": f"日报 {date_str}",
        "date": date_str,
        "properties": {}
    }

    # row mapping
    field_map = {
        'ROOM SOLD': 'room_sold', 'COMPLIMENTARY': 'comp_rooms', 'HOUSE USE': 'house_use',
        'OUT OF ORDER': 'ooo_rooms', 'VACANT': 'vacant_rooms', 'AVAILABLE': 'available_rooms',
        '% Occupancy': 'occ_pct', 'REVPAR': 'revpar', 'AVERAGE ROOM RATE': 'arr',
        'TOTAL ROOMS REVENUE': 'room_revenue_total', 'OTHER INCOME': 'other_income',
        'SERVICE CHARGE': 'service_charge', 'ROOM REVENUE': 'net_room_revenue',
        '- INCLUDE CONDO ROOM SOLD': 'condo_sold', '- INCLUDE CONDO ROOM REVE': 'condo_revenue',
        'GUEST COUNT': 'guest_count',
    }
    
    # 字段简化别名
    # trends用field_map的实际字段名
    trends_fields = {
        'room_sold': '售出', 'occ_pct': '出租率%', 'arr': '均价', 
        'revpar': 'RevPAR', 'net_room_revenue': '净收入'
    }

    props = {}
    for label, field in field_map.items():
        d = rmap.get(label, {})
        v = d.get('today')
        if v is not None:
            if isinstance(v, (int, float)) and label in ('% Occupancy',):
                props[field] = round(v * 100, 2)
            else:
                props[field] = round(v, 2) if isinstance(v, float) else (int(v) if isinstance(v, int) else v)
        # also store budget/ly if available
        for suffix, src in [('_budget','budget'), ('_ly','ly')]:
            sv = d.get(src)
            if sv is not None:
                ps = field + suffix
                if isinstance(sv, (int, float)) and label in ('% Occupancy',):
                    props[ps] = round(sv * 100, 2)
                else:
                    props[ps] = round(sv, 2) if isinstance(sv, float) else (int(sv) if isinstance(sv, int) else sv)
    
    props['mtd_net_revenue'] = round(rmap.get('ROOM REVENUE',{}).get('mtd') or 0, 2)
    props['mtd_net_budget'] = round(rmap.get('ROOM REVENUE',{}).get('mtd_budget') or 0, 2)
    props['mtd_net_ly'] = round(rmap.get('ROOM REVENUE',{}).get('mtd_ly') or 0, 2)
    
    # 月完成率
    if props.get('mtd_net_revenue') and props.get('mtd_net_budget'):
        props['mtd_achievement_pct'] = round(props['mtd_net_revenue'] / props['mtd_net_budget'] * 100, 2)
    
    props['hotel'] = '苏州希尔顿酒店 (Hilton Suzhou)'
    today_entity['properties'] = props
    return today_entity

def parse_fb_sheet(ws, date_str):
    """解析F&B sheet，生成餐饮当日快照"""
    entities = []
    for r in range(11, 25):
        label = ws.cell(r, 2).value
        if not label or not isinstance(label, str): continue
        label = label.strip()
        if len(label) < 3: continue
        rev = ws.cell(r, 3).value
        cov = ws.cell(r, 4).value
        avg = ws.cell(r, 5).value
        if rev is None: continue
        
        # 清理标签
        clean_label = label.replace('\n',' ').replace('\r','').strip()
        eid = f"FB_{date_str.replace('-','_')}_{clean_label[:6].upper()}"
        
        ent = {
            "id": eid,
            "type": "FB_DAILY",
            "name": f"餐饮 {clean_label} {date_str}",
            "date": date_str,
            "outlet": clean_label,
            "properties": {
                "revenue": round(rev, 2) if isinstance(rev, float) else rev,
                "covers": int(cov) if isinstance(cov, (int,float)) else cov,
                "avg_check": round(avg, 2) if isinstance(avg, float) else avg,
            }
        }
        entities.append(ent)
    return entities

def build_relations(date_str, room_entity, fb_entities):
    """构建关系"""
    relations = []
    eid = room_entity['id']
    
    # 日报之间链式关系：前一日 → 当日
    relations.append({
        "source_id": eid,
        "type": "DAILY_SNAPSHOT"
    })
    
    # 日报 → 餐饮
    for fb in fb_entities:
        relations.append({
            "source_id": eid,
            "target_id": fb['id'],
            "type": "INCLUDES_FB"
        })
    
    return relations

def process_one(filepath):
    """处理单个日报"""
    fname = os.path.basename(filepath)
    date_str = extract_date(fname)
    if not date_str:
        print(f"  ⚠ 无法从文件名提取日期: {fname}")
        return False
    
    print(f"\n📄 解析: {fname} → 日期: {date_str}")
    
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        print(f"  ❌ 无法打开文件: {e}")
        return False
    
    # 解析
    ws = wb['Actual']
    room_entity = parse_actual_sheet(ws, date_str)
    
    fb_entities = []
    if 'F&B' in wb.sheetnames:
        fb_entities = parse_fb_sheet(wb['F&B'], date_str)
    
    # 加载图谱
    g = load_graph()
    
    # 检查是否已有该日期
    existing = [e for e in g['entities'] if e['id'] == room_entity['id']]
    if existing:
        print(f"  ⚠ 日期 {date_str} 已存在，覆盖更新")
        g['entities'] = [e for e in g['entities'] if e['id'] != room_entity['id']]
        g['relations'] = [r for r in g['relations'] if r.get('source_id') != room_entity['id']]
    
    # 追加
    g['entities'].append(room_entity)
    g['index']['by_date'][date_str] = room_entity['id']
    g['index']['by_type'].setdefault('DAILY_SNAPSHOT', []).append(room_entity['id'])
    
    for fb in fb_entities:
        g['entities'].append(fb)
        g['index']['by_type'].setdefault('FB_DAILY', []).append(fb['id'])
    
    # 关系
    relations = build_relations(date_str, room_entity, fb_entities)
    g['relations'].extend(relations)
    
    # 保存
    save_graph(g)
    
    # 简要输出
    props = room_entity['properties']
    print(f"  ✅ {date_str}: 出租率{props.get('occ','-')}% | "
          f"均价¥{props.get('arr',0):,.0f} | "
          f"净收入¥{props.get('net_room_revenue',0):,.0f} | "
          f"MTD完成率{props.get('mtd_achievement_pct','-')}%")
    if fb_entities:
        fb_total = sum(fb.get('properties',{}).get('revenue',0) for fb in fb_entities if isinstance(fb.get('properties',{}).get('revenue',0), (int,float)))
        print(f"  🍽 餐饮当日总营收: ¥{fb_total:,.0f} ({len(fb_entities)}个餐厅)")
    
    return True

def scan_incoming():
    """扫描incoming最新未处理文件"""
    if not INCOMING.exists():
        print("incoming目录不存在")
        return
    
    xlsx_files = sorted(INCOMING.glob('Daily_Revenue_Report_*.xlsx'), key=lambda f: f.name)
    if not xlsx_files:
        print("未找到日报文件")
        return
    
    for fp in xlsx_files:
        if fp.name in processed:
            continue
        # skip non-April files (some are old format or PDF)
        if '2026.04' not in fp.name:
            continue
        ok = process_one(str(fp))
        if ok:
            with open(PROCESSED_LOG, 'a') as f:
                f.write(fp.name + '\n')
            processed.add(fp.name)

def trend_summary(g):
    """生成趋势摘要"""
    snapshots = [e for e in g['entities'] if e['type'] == 'DAILY_SNAPSHOT']
    snapshots.sort(key=lambda e: e.get('date',''))
    
    if len(snapshots) < 2:
        print("\n📊 趋势: 数据不足2天")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 趋势分析 ({len(snapshots)}天)")
    print(f"{'='*60}")
    print(f"{'日期':<12} {'出租率%':>8} {'均价':>8} {'RevPAR':>8} {'净收入':>10} {'完成率':>8}")
    print(f"{'─'*60}")
    
    ft = {'occ_pct':0,'arr':0,'revpar':0,'net':0,'mtd':0}
    for e in snapshots:
        p = e.get('properties',{})
        occ = p.get('occ_pct','-')
        arr = f"¥{p.get('arr',0):,.0f}" if p.get('arr') else '-'
        rev = f"¥{p.get('revpar',0):,.0f}" if p.get('revpar') else '-'
        net = f"¥{p.get('net_room_revenue',0):,.0f}" if p.get('net_room_revenue') else '-'
        ach = p.get('mtd_achievement_pct','-')
        ach_s = f"{ach}%" if isinstance(ach,(int,float)) else '-'
        occ_s = f"{occ}%" if isinstance(occ,(int,float)) else '-'
        print(f"{e.get('date','?'):<12} {occ_s:>8} {arr:>8} {rev:>8} {net:>10} {ach_s:>8}")
        if isinstance(p.get('occ_pct'),(int,float)): ft['occ_pct'] += p['occ_pct']
        if isinstance(p.get('arr'),(int,float)): ft['arr'] += p['arr']
        if isinstance(p.get('revpar'),(int,float)): ft['revpar'] += p['revpar']
        if isinstance(p.get('net_room_revenue'),(int,float)): ft['net'] += p['net_room_revenue']
    
    n = len(snapshots)
    print(f"{'─'*60}")
    avg_occ = ft['occ_pct'] / n if ft['occ_pct'] else 0
    print(f"{'平均':<12} {avg_occ:>7.1f}% ¥{ft['arr']/n:>7,.0f} ¥{ft['revpar']/n:>7,.0f} ¥{ft['net']/n:>9,.0f}")

if __name__ == '__main__':
    print("🏨 Y 财务日报解析引擎 v1.0")
    
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        process_one(sys.argv[1])
    else:
        scan_incoming()
    
    # 出趋势
    g = load_graph()
    if g.get('entities'):
        trend_summary(g)
    
    print(f"\n📊 财务经营站: {g['meta']['entity_count']}实体, {g['meta']['relation_count']}关系")
