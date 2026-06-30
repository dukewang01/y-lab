#!/usr/bin/env python3
"""Final import of HF 5.25 data - correct token-based parsing."""
import json, shutil, pdfplumber, re

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_hf_final.json'
PDF_PATH = r'media/inbound\History_and_Forecast_5.25---c74c53cf-e12c-4239-85c9-53e52c50b33a.pdf'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

with pdfplumber.open(PDF_PATH) as pdf:
    text = '\n'.join(p.extract_text() for p in pdf.pages)

dow_map = {
    'Mon':'周一','Tue':'周二','Wed':'周三','Thu':'周四',
    'Fri':'周五','Sat':'周六','Sun':'周日'
}

daily_data = {}
date_pattern = r'(\d{2})\.(\d{2})\.(\d{2})\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'

for line in text.split('\n'):
    m = re.search(date_pattern, line)
    if not m:
        continue
    
    tokens = line.split()
    if len(tokens) < 15:
        continue
    
    # Parse: token[0]=date, [1]=DOW
    # token[2]=Total Occ, [3]=Deduct Indiv, [4]=Comp, [5]=House Use
    # token[6]=Non-Ded Indiv, [7]=?, [8]=Deduct Group, [9]=Non-Ded Group
    # token[10]=Occ% (remove '%'), [11]=Room Rev, [12]=Avg Rate (per total occ)
    # token[13]=Dep Rooms, [14]=OOO, [15:]=others
    
    def clean_float(s):
        return float(s.replace(',','').replace('%',''))
    
    day = int(m.group(1))
    month = int(m.group(2))
    year = int(m.group(3)) + 2000
    date_str = f'{year}-{month:02d}-{day:02d}'
    
    try:
        total_occ = int(tokens[2])        
        deduct_indiv = int(tokens[3])
        comp_rooms = int(tokens[4])
        house_use = int(tokens[5])
        non_ded_indiv = int(tokens[6])
        deduct_group = int(tokens[8]) if len(tokens) > 8 else 0
        non_ded_group = int(tokens[9]) if len(tokens) > 9 else 0
        occ_pct = clean_float(tokens[10])
        room_revenue = clean_float(tokens[11])
        avg_rate = clean_float(tokens[12])
        dep_rooms = int(tokens[13])
        ooo = int(tokens[14])
        
        # Remaining tokens (if any) = Day Use, No Show, Last Year data
        day_use = int(tokens[15]) if len(tokens) > 15 else 0
        no_show = int(tokens[16]) if len(tokens) > 16 else 0
        ly_ref = int(tokens[17]) if len(tokens) > 17 else 0
        
        daily_data[date_str] = {
            'total_occ_hf': total_occ,
            'deduct_indiv': deduct_indiv,
            'non_ded_indiv': non_ded_indiv,
            'deduct_group': deduct_group,
            'non_ded_group': non_ded_group,
            'comp_rooms_hf': comp_rooms,
            'house_use_hf': house_use,
            'occ_pct_hf': occ_pct,
            'room_revenue_hf': room_revenue,
            'avg_rate_hf': avg_rate,
            'dep_rooms': dep_rooms,
            'ooo_rooms_hf': ooo,
            'day_use': day_use,
            'dow_cn': dow_map.get(m.group(4), ''),
        }
    except (ValueError, IndexError) as ex:
        print(f"  ERROR {date_str}: {ex}")

print(f"Parsed {len(daily_data)} days")

# Import to graph
for date_str, data in sorted(daily_data.items()):
    day_id = f'day_{date_str}'
    existing = [e for e in entities if e.get('id') == day_id]
    node = existing[0] if existing else None
    
    if node:
        node.setdefault('properties', {})
        props = node['properties']
    else:
        node = {
            'id': day_id,
            'name': f'日报 {date_str}',
            'date': date_str,
            'type': 'daily_revenue',
            'properties': {}
        }
        entities.append(node)
        props = node['properties']
    
    for k, v in data.items():
        props[k] = v

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"Saved: {len(entities)} entities")

# Validation
print("\n=== Cross-Validation: HF vs DRR (0522-0524) ===")
print(f'  {"Date":12s} {"HF Occ%":>7s} {"DRR Occ%":>8s} {"Diff":>6s} {"HF Tot":>6s} {"DRR Sld":>8s} {"HF Rev":>10s} {"DRR Rev":>10s}')
print(f'  {"-"*67}')
for ds in ['2026-05-22','2026-05-23','2026-05-24']:
    did = f'day_{ds}'
    n = [e for e in entities if e.get('id') == did]
    if not n: continue
    p = n[0].get('properties', {})
    ho = p.get('occ_pct_hf')
    do = p.get('occ_pct')
    ht = p.get('total_occ_hf')
    dsold = p.get('room_sold')
    hv = p.get('room_revenue_hf')
    dv = p.get('room_revenue_total')
    diff_o = round(ho - do, 2) if ho and do else None
    print(f'  {ds:12s} {ho:>7.2f} {do:>7.1f}% {"":>1s} {diff_o:>+5.2f} {ht:>6d} {str(dsold):>8s} {hv:>10,.0f} {dv:>10,.0f}')

# Monthly totals
total_rev = sum(d['room_revenue_hf'] for d in daily_data.values())
total_occ = sum(d['total_occ_hf'] for d in daily_data.values())
total_rev_past = sum(d['room_revenue_hf'] for d in daily_data.values() if int(sorted(daily_data.keys())[0][8:10].lstrip('0') or '0') <= 24)
total_occ_past = sum(d['total_occ_hf'] for d in daily_data.values() if int(d['date_str'].split('-')[-1]) <= 24) if 'date_str' in daily_data else sum(d['total_occ_hf'] for d in list(daily_data.values())[:24])

# Calculate from keys
past_24 = [k for k in sorted(daily_data.keys()) if int(k.split('-')[-1]) <= 24]
fwd_7 = [k for k in sorted(daily_data.keys()) if int(k.split('-')[-1]) >= 25]
past_rev = sum(daily_data[k]['room_revenue_hf'] for k in past_24)
past_occ = sum(daily_data[k]['total_occ_hf'] for k in past_24)
fwd_rev = sum(daily_data[k]['room_revenue_hf'] for k in fwd_7)
fwd_occ = sum(daily_data[k]['total_occ_hf'] for k in fwd_7)

print(f"\nMay Monthly Totals (HF):")
print(f"  Total Room Revenue: {total_rev:,.0f}")
print(f"  Total Room Nights:  {total_occ}")
print(f"  Avg Occ%: {sum(d['occ_pct_hf'] for d in daily_data.values())/31:.1f}%")
print(f"  Avg Rate (Total Occ): {total_rev/total_occ:.0f}")
print(f"\n  Past (1-24): Rev={past_rev:,.0f} / Occ={past_occ}")
print(f"  Forecast (25-31): Rev={fwd_rev:,.0f} / Occ={fwd_occ}")
print(f"  Budget Gap Analysis:")
print(f"  Past ADR (HF): {past_rev/past_occ:.0f}  vs  DRR MTD ADR (0722): ~728")
