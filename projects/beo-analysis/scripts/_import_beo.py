"""Import BEO Daily Event-BQ report (5.10-6.30) into FIN and FB graphs"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

FIN_GRAPH = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json")
FB_GRAPH = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_graph.json")
BEO_DATA = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\_raw_beo.txt")

# ═══════════════════════════════════════════════════════
# Step 1: Parse the BEO text
# ═══════════════════════════════════════════════════════

with open(BEO_DATA, "r", encoding="utf-8") as f:
    txt = f.read()

# Split by date headers
date_blocks = re.split(r'Event Start Date: ', txt)
# Remove the header block (before first date)
event_blocks = []
for block in date_blocks:
    m = re.match(r'(\d{2}/\d{2}/\d{4}) \((\d+) records\)\n', block.strip())
    if m:
        date_str = m.group(1)
        record_count = int(m.group(2))
        # Parse day/month/year
        day, month, year = date_str.split('/')
        iso_date = f"20{year}-{month}-{day}"
        content = block[m.end():].strip()
        event_blocks.append((iso_date, record_count, content))

print(f"Found {len(event_blocks)} date blocks")

# Parse each event line
all_events = []
for iso_date, count, content in event_blocks:
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip date summary lines at the bottom
        if line.startswith('Event Start Date:') or line.startswith('Grand Totals'):
            continue
        
        # Line format: ChineseName EnglishName start end room type setup expected guaranteed status BEO_# owner service catering
        # Try to extract structured data
        
        # Find BEO pattern (BEO number or Definite/Tentative/Prospect)
        beo_match = re.search(r'(Definite|Tentative|Prospect)\s+([\w\s]+?)(?:\s+-\s+-|$)', line)
        if not beo_match:
            # Try alternate: BEO: 7660-Definite format
            beo_match = re.search(r':\s*\d+[-\s]*(Definite|Tentative|Prospect)\s+([\w\s]+?)(?:\s+-\s+-|$)', line)
        
        # Find time range (HH:MM HH:MM)
        time_match = re.findall(r'(\d{1,2}:\d{2})\s+(\d{1,2}:\d{2})', line)
        
        # Find room
        room_pattern = r'(Grand Ballroom(?:\s+\d\+?\d*)?|Function Room(?:\s+\d[\+\.]?\d*)?|Italian Resterant|Italian Restaurant|Boardroom|VIP Room|Rest Room/Bride Room|All Day Dining|OPEN|Outside Catering)'
        room_match = re.search(room_pattern, line)
        
        # Find setup
        setup_patterns = r'(Lunch Buffet|Wedding Dinner|Meeting|Lunch|Dinner|Dinner Round Tables|Setup|Break|Room Hold|Boxed Lunch|Coffee Station)'
        setup_match = re.search(setup_patterns, line)
        
        # Find expected/guaranteed numbers
        num_match = re.findall(r'(\d+)', line[line.find(' Room' if 'Room' in line else '00'):] if ' Room' in line or '00' in line else line)
        
        # Find English event name
        eng_match = re.search(r'(The (Wedding|Lunch|Dinner|Thanks|Birthday|dinner)\s+of\s+[\w\s.]+|Meeting|Lunch Buffet|Dinner|Citic Bank Meeting[\w\s]*|B\.Braun Meeting[\w\s]*|Samsung[\w\s]*|Doosan[\w\s]*|Shure[\w\s]*|MegaRobo[\w\s]*|Chamber[\w\s]*|BOXED LUNCH[\w\s]*)', line)
        
        # Find event owner
        owners = ['Elaine He', 'Luisa Liu', 'Lily Xie', 'Nico Lin', 'Cecily Hong', 'Catherine Xu']
        owner_match = None
        for o in owners:
            if o in line:
                owner_match = o
                break
        
        # Find status
        status = 'Definite'
        if 'Tentative' in line:
            status = 'Tentative'
        elif 'Prospect' in line:
            status = 'Prospect'
        
        start_time = time_match[0][0] + ':00' if time_match else ''
        end_time = time_match[0][1] + ':00' if len(time_match) > 0 else ''
        
        eng_name = eng_match.group(0) if eng_match else ''
        
        # Extract Chinese name (text between start of line and English name)
        chn_name = ''
        if eng_match:
            full_eng = eng_match.group(0)
            idx = line.find(full_eng)
            if idx > 0:
                # Everything before English name is Chinese name
                potential_chn = line[:idx].strip()
                # Filter out just real Chinese chars
                chn_chars = re.findall(r'[\u4e00-\u9fff]+', potential_chn)
                chn_name = ' '.join(chn_chars) if chn_chars else ''
        
        # BEO number
        beo_num = ''
        beo_num_match = re.search(r'(\d{4})[-\s]*(?:BEO|Definite)', line)
        if beo_num_match:
            beo_num = beo_num_match.group(1)
        
        all_events.append({
            'date': iso_date,
            'chinese_name': chn_name,
            'english_name': eng_name,
            'start': start_time,
            'end': end_time,
            'room': room_match.group(0) if room_match else '',
            'setup': setup_match.group(0) if setup_match else '',
            'status': status,
            'owner': owner_match or '',
            'beo': beo_num,
            'raw': line
        })

print(f"Parsed {len(all_events)} events")
for e in all_events:
    print(f"  {e['date']} | {e['chinese_name']:20s} | {e['english_name'][:30]:30s} | {e['start']}-{e['end']} | {e['room'][:20]:20s} | {e['status']}")

# Count by date
from collections import Counter
date_counts = Counter(e['date'] for e in all_events)
print(f"\nEvents by date ({len(date_counts)} dates):")
for d, c in sorted(date_counts.items()):
    print(f"  {d}: {c} events")

# ═══════════════════════════════════════════════════════
# Step 2: Import into FIN + FB graphs
# ═══════════════════════════════════════════════════════

# First backup
import shutil

# Load current graphs
with open(FIN_GRAPH, "r", encoding="utf-8") as f:
    fin = json.load(f)

with open(FB_GRAPH, "r", encoding="utf-8") as f:
    fb = json.load(f)

# Backup both
shutil.copy(FIN_GRAPH, FIN_GRAPH.with_suffix('.pre_beo_import.json'))
shutil.copy(FB_GRAPH, FB_GRAPH.with_suffix('.pre_beo_import.json'))
print(f"\n✅ Backups saved")

# Track uniqueness
def exists_in(entity_list, eid):
    return any(e.get('id') == eid for e in entity_list)

# ── FIN graph: BEO report entity ──
REPORT_ID = "BEO_20260510"
if not exists_in(fin['entities'], REPORT_ID):
    fin['entities'].append({
        "id": REPORT_ID,
        "name": "BEO Daily Event 5.10-6.30",
        "type": "fin_report",
        "date": "2026-05-10",
        "properties": {
            "report_label": "BEO_SZVTV",
            "hotel": "Hilton Suzhou",
            "report_date": "2026-05-10",
            "filter_from": "2026-05-10",
            "filter_to": "2026-06-30",
            "total_events": len(all_events),
            "generated_by": "Elaine He",
            "source_file": "5.10-6.30Report.pdf",
            "imported_at": "2026-05-10"
        }
    })
    print("✅ Created BEO report entity")

# Link to FIN_YEAR_2026
FIN_YEAR = "FIN_YEAR_2026"
if not exists_in(fin['entities'], FIN_YEAR):
    fin['entities'].append({
        "id": FIN_YEAR,
        "name": "2026年财务年度",
        "type": "fin_year",
        "date": "2026",
        "properties": {"year": 2026}
    })

rel_key = f"REL_{REPORT_ID}_belongs_to_{FIN_YEAR}"
if not any(r.get('id') == rel_key for r in fin['relationships']):
    fin['relationships'].append({
        "source_id": REPORT_ID,
        "target_id": FIN_YEAR,
        "relation": "BELONGS_TO",
        "id": rel_key,
        "type": "BELONGS_TO",
        "source": REPORT_ID,
        "target": FIN_YEAR
    })

# ── Handle events ──
known_rooms = set()  # Track rooms seen for this report
event_count_by_status = Counter(e['status'] for e in all_events)
event_count_by_room = Counter(e['room'] for e in all_events)

for e in all_events:
    # Create unique event ID
    safe_date = e['date'].replace('-', '')
    event_id = f"BEO_{safe_date}_{e['start'].replace(':','')}_{e['room'][:10].replace(' ','_')}"
    # Deduplicate with name
    short_name = e['english_name'][:30] if e['english_name'] else e['chinese_name'][:10]
    event_id = f"BEO_{safe_date}_{short_name[:10].replace('/','_').replace(' ','_')}"
    
    # Skip if already exists
    if exists_in(fin['entities'], event_id):
        continue
    
    # Create event entity
    fin['entities'].append({
        "id": event_id,
        "name": f"[BEO] {e['date']} {e['chinese_name']} {e['english_name'][:40]}",
        "type": "beo_event",
        "date": e['date'],
        "properties": {
            "date": e['date'],
            "event_date": e['date'],
            "chinese_name": e['chinese_name'],
            "english_name": e['english_name'],
            "start_time": e['start'],
            "end_time": e['end'],
            "room": e['room'],
            "setup": e['setup'],
            "status": e['status'],
            "owner": e['owner'],
            "beo_number": e['beo']
        }
    })
    
    # Link event -> BEO report
    event_rel = f"REL_{event_id}_belongs_to_{REPORT_ID}"
    if not any(r.get('id') == event_rel for r in fin['relationships']):
        fin['relationships'].append({
            "source_id": event_id,
            "target_id": REPORT_ID,
            "relation": "BELONGS_TO",
            "id": event_rel,
            "type": "BELONGS_TO",
            "source": event_id,
            "target": REPORT_ID
        })
    
    # Register rooms
    if e['room']:
        known_rooms.add(e['room'])

print(f"\n📊 BEO Import Summary:")
print(f"  Total events: {len(all_events)}")
print(f"  Definite: {event_count_by_status.get('Definite', 0)}")
print(f"  Tentative: {event_count_by_status.get('Tentative', 0)}")
print(f"  Prospect: {event_count_by_status.get('Prospect', 0)}")
print(f"  Unique rooms: {len(known_rooms)}")
print(f"  Date range: {event_blocks[0][0]} → {event_blocks[-1][0]}")

# ── Save both graphs ──
with open(FIN_GRAPH, "w", encoding="utf-8") as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print(f"\n✅ FIN graph saved ({len(fin['entities'])} entities, {len(fin['relationships'])} relationships)")
print(f"  FIN meta version updated to include BEO data")
