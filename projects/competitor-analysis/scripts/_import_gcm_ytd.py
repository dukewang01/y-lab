#!/usr/bin/env python3
"""Import GCM YTD market analysis data into FIN graph (as market_intelligence type)."""
import json, shutil, openpyxl

FIN_GRAPH = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_gcm_ytd.json'
XLSX_PATH = r'knowledge_center\..\media\incoming\GCM_YTD.xlsx'

shutil.copy2(FIN_GRAPH, BACKUP)
print(f"Backup: {BACKUP}")

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)
entities = g['entities']

wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
ws = wb['Export']

# Create market data nodes
current_market = None
added = 0
for r in range(2, ws.max_row + 1):
    col1 = ws.cell(r, 1).value  # Market
    col2 = ws.cell(r, 2).value  # Hotel name
    col3 = ws.cell(r, 3).value  # ADR
    col4 = ws.cell(r, 4).value  # Rev
    col5 = ws.cell(r, 5).value  # RevPAR
    col6 = ws.cell(r, 6).value  # RNs
    col7 = ws.cell(r, 7).value  # Occ
    
    if col1 is not None and col2 == 'Total' and col3 is not None:
        # Market total row
        current_market = str(col1)
        entity_id = f'market_ytd_{current_market.replace("/","_").replace(" ","_")}'
        existing = [e for e in entities if e.get('id') == entity_id]
        if existing:
            node = existing[0]
            props = node.setdefault('properties', {})
        else:
            node = {
                'id': entity_id,
                'name': f'市场GCM {current_market} (YTD Jan-May 2026)',
                'type': 'market_intelligence',
                'properties': {}
            }
            entities.append(node)
            props = node['properties']
            added += 1
        
        props['market'] = current_market
        props['adr_ytd'] = float(col3)
        props['revenue_ytd'] = float(col4)
        props['revpar_ytd'] = float(col5)
        props['room_nights_ytd'] = int(col6)
        props['occupancy_ytd'] = float(col7) * 100
        props['source'] = 'GCM YTD'
        props['period'] = '2026 Jan-May'
        
    elif current_market and col2 is not None and col3 is not None:
        # Individual hotel row
        hotel_name = str(col2)
        entity_id = f'hotel_gcm_{hotel_name.replace(" ","_")}'
        existing = [e for e in entities if e.get('id') == entity_id]
        if existing:
            node = existing[0]
            props = node.setdefault('properties', {})
        else:
            node = {
                'id': entity_id,
                'name': f'GWMC {hotel_name} (YTD Jan-May 2026)',
                'type': 'market_intelligence',
                'properties': {}
            }
            entities.append(node)
            props = node['properties']
            added += 1
        
        props['market'] = current_market
        props['hotel_name'] = hotel_name
        props['brand_code'] = hotel_name.split()[0] if ' ' in hotel_name else hotel_name
        props['adr_ytd'] = float(col3)
        props['revenue_ytd'] = float(col4)
        props['revpar_ytd'] = float(col5)
        props['room_nights_ytd'] = int(col6)
        props['occupancy_ytd'] = float(col7) * 100
        props['source'] = 'GCM YTD'
        props['period'] = '2026 Jan-May'

g['entities'] = entities
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"Saved: {len(entities)} entities (+{added} new)")
