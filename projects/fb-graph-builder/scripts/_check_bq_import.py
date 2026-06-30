import json
from collections import Counter

g = json.load(open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json', 'r', encoding='utf-8'))
print('FIN graph after import:')
print('  Entities:', len(g['entities']))
print('  Relationships:', len(g['relationships']))

ec = Counter(e.get('type','?') for e in g['entities'])
print('Entity types:')
for t,c in ec.most_common(15):
    print('  %s: %d' % (t,c))

bqs = [e for e in g['entities'] if e.get('type') == 'banquet_booking']
print('\nBanquet bookings:', len(bqs))
if bqs:
    p = bqs[0]['properties']
    print('  Sample:', bqs[0]['name'][:40], p['event_date'], p['start_time'], p['venue'], 'Exp:', p['expected_pax'])

bq_days = [e for e in g['entities'] if e.get('type') == 'bq_daily_summary']
bq_days.sort(key=lambda x: x.get('date',''))
print('Daily summaries:', len(bq_days))
for s in bq_days:
    p = s['properties']
    print('  %s: %d bookings (%dD/%dP/%dT) | %d pax' % (
        s['date'], p['total_bookings'], p['definite'],
        p['prospect'], p['tentative'], p['total_expected_pax']))

# Verify backup
bup = json.load(open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph_pre_bq_20260614.json', 'r', encoding='utf-8'))
print('\nBackup verified: %d entities, %d rels' % (len(bup['entities']), len(bup['relationships'])))
print('Difference: +%d entities, +%d rels' % (len(g['entities'])-len(bup['entities']), len(g['relationships'])-len(bup['relationships'])))
