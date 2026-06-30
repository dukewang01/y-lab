#!/usr/bin/env python3
"""Log BEO #7683 change into FIN graph + save BEO PDF."""
import json, shutil, os

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_beo7683.json'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
ents = g['entities']
rels = g.get('relations', [])

# Archive PDF
src = r'C:\Users\Duke Wang\.openclaw\media\inbound\2026.5.29_å_äº_æµ_ç_æ_å_è_ä¼_è_BEO_7683_Changelog1---b393f69d-ab3f-414f-8abd-a9354e827e5e.pdf'
dst = r'C:\Users\Duke Wang\.openclaw\media\archived\BEO7683_南京海维医药会议_Changelog1.pdf'
shutil.copy2(src, dst)
print(f"Archived: {dst}")

# Create BEO event node
beo_id = 'BEO_7683'
beo = {
    'id': beo_id,
    'name': 'BEO#7683 南京海维医药会议',
    'type': 'beo_event',
    'labels': ['宴会', '会议', 'BEO'],
    'properties': {
        'beo_number': 7683,
        'event_date': '2026-05-29',
        'booking_name': '南京海维医药会议',
        'catering_manager': 'Luisa Liu',
        'service_manager': 'Luisa Liu',
        'change_log': 'Change 1: 下午茶歇40人→20人，菜单不变。其他不变。',
        'change_date': '2026-05-26',
        'created_by': 'Luisa Liu',
        'source': 'BEO Changelog PDF',
        'archived_pdf': 'BEO7683_南京海维医药会议_Changelog1.pdf',
    }
}

existing = [e for e in ents if e.get('id') == beo_id]
if existing:
    idx = ents.index(existing[0])
    ents[idx] = beo
    print(f"Updated: {beo_id}")
else:
    ents.append(beo)
    print(f"Created: {beo_id}")

# Link event to day node
day_id = 'day_2026-05-29'
rel_id = f'E_{beo_id}_HELD_ON_{day_id}'
if not any(r.get('id') == rel_id for r in rels):
    rels.append({'id': rel_id, 'source': beo_id, 'target': day_id, 'relation': 'HELD_ON'})

# Create function rooms/sessions
sessions = [
    ('Meeting', 'Function Room 3+4', '08:00-18:00', 'Classroom布置'),
    ('Break AM', 'Function Room Foyer', '10:00-10:30', '咖啡站'),
    ('Lunch Buffet', 'BACIO意大利餐厅', '12:00-13:30', '自助午餐'),
    ('Break PM', 'Function Room Foyer', '15:00-15:30', '咖啡站·20人（原40人）'),
]

for i, (sname, room, time, note) in enumerate(sessions):
    sess_id = f'{beo_id}_SESS_{i+1}'
    if not any(e.get('id') == sess_id for e in ents):
        ents.append({
            'id': sess_id,
            'name': sname,
            'type': 'beo_session',
            'labels': ['宴会时段'],
            'properties': {
                'room': room,
                'time': time,
                'setup': note,
                'beo': 7683,
            }
        })
    
    rel_s = f'E_{sess_id}_PART_OF_{beo_id}'
    if not any(r.get('id') == rel_s for r in rels):
        rels.append({'id': rel_s, 'source': sess_id, 'target': beo_id, 'relation': 'PART_OF'})

g['entities'] = ents
g['relations'] = rels
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nSaved: {len(ents)} entities, {len(rels)} relations")
print("Done!")
