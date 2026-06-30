#!/usr/bin/env python3
"""Parse History_and_Forecast_5.25 PDF and import daily data."""
import json, shutil, pdfplumber, re

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_hist_forecast_0525.json'
PDF_PATH = r'C:\Users\Duke Wang\.openclaw\media\inbound\History_and_Forecast_5.25---c74c53cf-e12c-4239-85c9-53e52c50b33a.pdf'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

# Extract text
with pdfplumber.open(PDF_PATH) as pdf:
    text = '\n'.join(p.extract_text() for p in pdf.pages)

lines = text.split('\n')

# Find the data section — look for dates 01.05.26 to 31.05.26
# Format: Date | Total Occ | Arr Rooms | Comp | HU | ... | Rate
# The data starts after a line containing the column headers

# Let's find where the daily data starts
data_start = None
for i, line in enumerate(lines):
    if '01.05.26' in line and 'Fri' in line:
        data_start = i
        break

if data_start is None:
    print("Could not find data start!")
    import sys; sys.exit(1)

print(f"Data starts at line {data_start}")

# The columns appear to be space-separated. Let's parse them.
# Looking at the raw text, each day has these columns:
# Date | Day | Total Occ | Arr Rooms | Comp | HU | Deduct Indiv | Non-Ded Indiv | Deduct Group | Non-Ded Group | Rate | Dep Rooms | OOO | ... | Occ% | Room Revenue

# Actually the text is very compressed. Let me try a different approach.

# The data is in a table format. Let's find all date lines
date_pattern = r'(\d{2}\.\d{2}\.\d{2})\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
daily_entries = []

for i, line in enumerate(lines):
    m = re.search(date_pattern, line)
    if m:
        date_str = m.group(1)
        dow = m.group(2)
        # The rest of the line has numbers
        numbers = re.findall(r'[\d,]+(?:\.\d+)?', line)
        if len(numbers) >= 13:
            daily_entries.append({
                'date_raw': date_str,
                'dow': dow,
                'line_idx': i,
                'nums': numbers,
                'raw': line
            })

print(f"Found {len(daily_entries)} daily entries")

# Print them out for inspection
for e in daily_entries:
    print(f"  {e['date_raw']} {e['dow']:3s} | nums={len(e['nums']):2d} | first 15: {e['nums'][:15]}")
    if len(e['nums']) > 15:
        print(f"    remaining: {e['nums'][15:]}")

# Extract key numbers for each date
# Based on the OnQ HF report column layout:
# Total Occ, Arr Rooms, Comp, House Use, Deduct Indiv, Non-Ded Indiv, Deduct Group, Non-Ded Group, 
# Average Rate, Dep Rooms, OOO Rooms, ..., Occ%, Room Revenue

# Let's map known values:
# From the header line: 
# "Date Total Occ. Arr. Rooms Comp. Rooms House Use Deduct Indiv. Non-Ded. Indiv. Deduct Group Non-Ded. Group Average Rate Dep. Rooms OOO Rooms Adl. & Chl. Occ.% Room Revenue"
#
# Then from data row:
# 01.05.26 Fri 438 390 0 48 0 0 888 3 81.04% 803.49 350321.40

print("\n\nDetailed extraction:")
for e in daily_entries:
    nums = e['nums']
    date_ymd = f"2026-{e['date_raw'][3:5]}-{e['date_raw'][:2]}"
    
    # Parse column by column (positional, based on OnQ HF format)
    # Total Occ = nums[0], Arr Rooms = nums[1], Comp = nums[2], HU = nums[3]
    # Deduct Indiv = nums[4], Non-Ded Indiv = nums[5], Deduct Group = nums[6], Non-Ded Group = nums[7]
    # There may be additional middle columns...
    
    # Let's find Occ% (a % value) and Room Revenue (largest number near end)
    occ_pct = None
    room_rev = None
    rate = None
    
    for v in nums:
        if '%' in str(v) or ('.' in str(v) and v.count('.') == 1 and float(v) < 100):
            occ_pct_str = str(v).replace('%','')
            try:
                occ_candidate = float(occ_pct_str)
                if 10 <= occ_candidate <= 100:
                    occ_pct = occ_candidate
            except:
                pass
    
    # Find rate value (between 400-1500)
    rates = [float(v) for v in nums if 400 <= float(v) <= 1500]
    if rates:
        rate = rates[0]
    
    # Find room revenue (values between 50000-5000000)
    revs = [float(v) for v in nums if 80000 <= float(v) <= 5000000]
    if revs:
        room_rev = revs[0] if len(revs) == 1 else revs[-1]  # Usually the last big number
    
    # Total occ (rooms occupied) - first number after date, should be 100-500
    occ_rooms = [float(v) for v in nums if 100 <= float(v) <= 550]
    total_occ = occ_rooms[0] if occ_rooms else None
    
    print(f"  {date_ymd} {e['dow']:3s} | occ_rooms={total_occ} | occ%={occ_pct} | rate={rate} | room_rev={room_rev}")
