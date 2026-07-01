"""
_daily_revenue_parser.py â€?è´¢åŠ¡æ—¥æŠ¥è‡ªåŠ¨è§£æžå¼•æ“Ž
ç”¨æ³•: å°†Daily Revenue Report xlsxæ”¾å…¥ media/incoming/ åŽè¿è¡?      python _daily_revenue_parser.py [æ–‡ä»¶è·¯å¾„]
      (æ— å‚æ•°åˆ™è‡ªåŠ¨æ‰«æ incoming/ ä¸­æœ€æ–°æœªå¤„ç†çš„æ—¥æŠ?
"""
import json, os, sys, re, openpyxl, datetime
from pathlib import Path

BASE = Path(__file__).parent.resolve()
GRAPH_PATH = BASE / 'finance_graph.json'
INCOMING = Path(r'media/inbound')
ARCHIVE = Path(r'media\archived')
PROCESSED_LOG = BASE / '.finance_processed.log'

# å·²å¤„ç†æ ‡è®?processed = set()
if PROCESSED_LOG.exists():
    processed = set(PROCESSED_LOG.read_text().splitlines())

def load_graph():
    if GRAPH_PATH.exists():
        return json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
    return {"meta":{"name":"Yçš„è´¢åŠ¡ç»è¥ç«™","display_name":"è‹å·žå¸Œå°”é¡¿é…’åº—è´¢åŠ¡ç»è¥ç«™","hotel":"è‹å·žå¸Œå°”é¡¿é…’åº?(Hotel-A)","description":"è‹å·žå¸Œå°”é¡¿è¥æ”¶æ—¥æŠ?,"version":"1.0","created":datetime.date.today().isoformat(),"last_updated":datetime.date.today().isoformat(),"source":"Daily Revenue Report (OnQç³»ç»Ÿ)","entity_count":0,"relation_count":0},"entities":[],"relations":[],"index":{"by_date":{},"by_type":{}}}

def save_graph(g):
    g['meta']['entity_count'] = len(g['entities'])
    g['meta']['relation_count'] = len(g['relations'])
    g['meta']['last_updated'] = datetime.date.today().isoformat()
    GRAPH_PATH.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')

def extract_date(filename):
    """ä»Žæ–‡ä»¶åæå–æ—¥æœŸï¼Œå¦‚ Daily_Revenue_Report_2026.04.28 â†?2026-04-28"""
    m = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', filename)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None

def parse_actual_sheet(ws, date_str):
    """è§£æžActual sheetï¼ˆå«ç¼“å­˜å€¼ï¼‰"""
    rmap = {}  # label â†?{field}
    for r in range(15, 33):
        label = ws.cell(r, 4).value
        if not label: continue
        label = str(label).strip()
        # å½“æ—¥/é¢„ç®—/ä¸Šå¹´/MTD/MTDé¢„ç®—/MTDä¸Šå¹´
        rmap[label] = {
            'today': ws.cell(r, 5).value,
            'budget': ws.cell(r, 6).value,
            'ly': ws.cell(r, 7).value,
            'mtd': ws.cell(r, 8).value,
            'mtd_budget': ws.cell(r, 9).value,
            'mtd_ly': ws.cell(r, 10).value,
        }

    # æž„å»ºæ ¸å¿ƒè¡?    def safe(label):
        d = rmap.get(label, {})
        return d

    # entity_id
    eid = f"DAILY_{date_str.replace('-','_')}"
    
    # å½“æ—¥å®žä½“
    today_entity = {
        "id": eid,
        "type": "DAILY_SNAPSHOT",
        "name": f"æ—¥æŠ¥ {date_str}",
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
    
    # å­—æ®µç®€åŒ–åˆ«å?    # trendsç”¨field_mapçš„å®žé™…å­—æ®µå
    trends_fields = {
        'room_sold': 'å”®å‡º', 'occ_pct': 'å‡ºç§ŸçŽ?', 'arr': 'å‡ä»·', 
        'revpar': 'RevPAR', 'net_room_revenue': 'å‡€æ”¶å…¥'
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
    
    # æœˆå®ŒæˆçŽ‡
    if props.get('mtd_net_revenue') and props.get('mtd_net_budget'):
        props['mtd_achievement_pct'] = round(props['mtd_net_revenue'] / props['mtd_net_budget'] * 100, 2)
    
    props['hotel'] = 'è‹å·žå¸Œå°”é¡¿é…’åº?(Hotel-A)'
    today_entity['properties'] = props
    return today_entity

def parse_fb_sheet(ws, date_str):
    """è§£æžF&B sheetï¼Œç”Ÿæˆé¤é¥®å½“æ—¥å¿«ç…?""
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
        
        # æ¸…ç†æ ‡ç­¾
        clean_label = label.replace('\n',' ').replace('\r','').strip()
        eid = f"FB_{date_str.replace('-','_')}_{clean_label[:6].upper()}"
        
        ent = {
            "id": eid,
            "type": "FB_DAILY",
            "name": f"é¤é¥® {clean_label} {date_str}",
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
    """æž„å»ºå…³ç³»"""
    relations = []
    eid = room_entity['id']
    
    # æ—¥æŠ¥ä¹‹é—´é“¾å¼å…³ç³»ï¼šå‰ä¸€æ—?â†?å½“æ—¥
    relations.append({
        "source_id": eid,
        "type": "DAILY_SNAPSHOT"
    })
    
    # æ—¥æŠ¥ â†?é¤é¥®
    for fb in fb_entities:
        relations.append({
            "source_id": eid,
            "target_id": fb['id'],
            "type": "INCLUDES_FB"
        })
    
    return relations

def process_one(filepath):
    """å¤„ç†å•ä¸ªæ—¥æŠ¥"""
    fname = os.path.basename(filepath)
    date_str = extract_date(fname)
    if not date_str:
        print(f"  âš?æ— æ³•ä»Žæ–‡ä»¶åæå–æ—¥æœŸ: {fname}")
        return False
    
    print(f"\nðŸ“„ è§£æž: {fname} â†?æ—¥æœŸ: {date_str}")
    
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        print(f"  â?æ— æ³•æ‰“å¼€æ–‡ä»¶: {e}")
        return False
    
    # è§£æž
    ws = wb['Actual']
    room_entity = parse_actual_sheet(ws, date_str)
    
    fb_entities = []
    if 'F&B' in wb.sheetnames:
        fb_entities = parse_fb_sheet(wb['F&B'], date_str)
    
    # åŠ è½½å›¾è°±
    g = load_graph()
    
    # æ£€æŸ¥æ˜¯å¦å·²æœ‰è¯¥æ—¥æœŸ
    existing = [e for e in g['entities'] if e['id'] == room_entity['id']]
    if existing:
        print(f"  âš?æ—¥æœŸ {date_str} å·²å­˜åœ¨ï¼Œè¦†ç›–æ›´æ–°")
        g['entities'] = [e for e in g['entities'] if e['id'] != room_entity['id']]
        g['relations'] = [r for r in g['relations'] if r.get('source_id') != room_entity['id']]
    
    # è¿½åŠ 
    g['entities'].append(room_entity)
    g['index']['by_date'][date_str] = room_entity['id']
    g['index']['by_type'].setdefault('DAILY_SNAPSHOT', []).append(room_entity['id'])
    
    for fb in fb_entities:
        g['entities'].append(fb)
        g['index']['by_type'].setdefault('FB_DAILY', []).append(fb['id'])
    
    # å…³ç³»
    relations = build_relations(date_str, room_entity, fb_entities)
    g['relations'].extend(relations)
    
    # ä¿å­˜
    save_graph(g)
    
    # ç®€è¦è¾“å‡?    props = room_entity['properties']
    print(f"  âœ?{date_str}: å‡ºç§ŸçŽ‡{props.get('occ','-')}% | "
          f"å‡ä»·Â¥{props.get('arr',0):,.0f} | "
          f"å‡€æ”¶å…¥Â¥{props.get('net_room_revenue',0):,.0f} | "
          f"MTDå®ŒæˆçŽ‡{props.get('mtd_achievement_pct','-')}%")
    if fb_entities:
        fb_total = sum(fb.get('properties',{}).get('revenue',0) for fb in fb_entities if isinstance(fb.get('properties',{}).get('revenue',0), (int,float)))
        print(f"  ðŸ½ é¤é¥®å½“æ—¥æ€»è¥æ”? Â¥{fb_total:,.0f} ({len(fb_entities)}ä¸ªé¤åŽ?")
    
    return True

def scan_incoming():
    """æ‰«æincomingæœ€æ–°æœªå¤„ç†æ–‡ä»¶"""
    if not INCOMING.exists():
        print("incomingç›®å½•ä¸å­˜åœ?)
        return
    
    xlsx_files = sorted(INCOMING.glob('Daily_Revenue_Report_*.xlsx'), key=lambda f: f.name)
    if not xlsx_files:
        print("æœªæ‰¾åˆ°æ—¥æŠ¥æ–‡ä»?)
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
    """ç”Ÿæˆè¶‹åŠ¿æ‘˜è¦"""
    snapshots = [e for e in g['entities'] if e['type'] == 'DAILY_SNAPSHOT']
    snapshots.sort(key=lambda e: e.get('date',''))
    
    if len(snapshots) < 2:
        print("\nðŸ“Š è¶‹åŠ¿: æ•°æ®ä¸è¶³2å¤?)
        return
    
    print(f"\n{'='*60}")
    print(f"ðŸ“Š è¶‹åŠ¿åˆ†æž ({len(snapshots)}å¤?")
    print(f"{'='*60}")
    print(f"{'æ—¥æœŸ':<12} {'å‡ºç§ŸçŽ?':>8} {'å‡ä»·':>8} {'RevPAR':>8} {'å‡€æ”¶å…¥':>10} {'å®ŒæˆçŽ?:>8}")
    print(f"{'â”€'*60}")
    
    ft = {'occ_pct':0,'arr':0,'revpar':0,'net':0,'mtd':0}
    for e in snapshots:
        p = e.get('properties',{})
        occ = p.get('occ_pct','-')
        arr = f"Â¥{p.get('arr',0):,.0f}" if p.get('arr') else '-'
        rev = f"Â¥{p.get('revpar',0):,.0f}" if p.get('revpar') else '-'
        net = f"Â¥{p.get('net_room_revenue',0):,.0f}" if p.get('net_room_revenue') else '-'
        ach = p.get('mtd_achievement_pct','-')
        ach_s = f"{ach}%" if isinstance(ach,(int,float)) else '-'
        occ_s = f"{occ}%" if isinstance(occ,(int,float)) else '-'
        print(f"{e.get('date','?'):<12} {occ_s:>8} {arr:>8} {rev:>8} {net:>10} {ach_s:>8}")
        if isinstance(p.get('occ_pct'),(int,float)): ft['occ_pct'] += p['occ_pct']
        if isinstance(p.get('arr'),(int,float)): ft['arr'] += p['arr']
        if isinstance(p.get('revpar'),(int,float)): ft['revpar'] += p['revpar']
        if isinstance(p.get('net_room_revenue'),(int,float)): ft['net'] += p['net_room_revenue']
    
    n = len(snapshots)
    print(f"{'â”€'*60}")
    avg_occ = ft['occ_pct'] / n if ft['occ_pct'] else 0
    print(f"{'å¹³å‡':<12} {avg_occ:>7.1f}% Â¥{ft['arr']/n:>7,.0f} Â¥{ft['revpar']/n:>7,.0f} Â¥{ft['net']/n:>9,.0f}")

if __name__ == '__main__':
    print("ðŸ¨ Y è´¢åŠ¡æ—¥æŠ¥è§£æžå¼•æ“Ž v1.0")
    
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        process_one(sys.argv[1])
    else:
        scan_incoming()
    
    # å‡ºè¶‹åŠ?    g = load_graph()
    if g.get('entities'):
        trend_summary(g)
    
    print(f"\nðŸ“Š è´¢åŠ¡ç»è¥ç«? {g['meta']['entity_count']}å®žä½“, {g['meta']['relation_count']}å…³ç³»")
