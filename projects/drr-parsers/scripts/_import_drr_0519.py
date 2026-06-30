import json, sys, shutil, os
sys.stdout.reconfigure(encoding='utf-8')

FIN_GRAPH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json'
BACKUP = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph_before_drr519.json'

# Backup
shutil.copy2(FIN_GRAPH, BACKUP)

with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    g = json.load(f)

nodes = g.get('nodes', [])
edges = g.get('edges', [])

# === 1. 更新 day_20260519 节点 ===
day_id = 'day_20260519'
target = None
for n in nodes:
    if n['id'] == day_id:
        target = n
        break

if target:
    # Update properties
    target['properties'] = {
        'rooms_sold': 387,
        'occupancy': 71.93,
        'adr': 669.26,
        'revpar': 481.42,
        'room_revenue': 233536.80,
        'net_room_revenue': 259002.80,
        'service_charge': 23545.90,
        'other_income': 1920.10,
        'guest_count': 490,  # from F&B total covers
        'weekday': 'Tuesday'
    }
    print(f'✅ Updated {day_id}')
else:
    print(f'❌ {day_id} not found, creating...')
    nodes.append({
        'id': day_id,
        'type': 'daily_revenue',
        'label': '2026-05-19',
        'properties': {
            'rooms_sold': 387,
            'occupancy': 71.93,
            'adr': 669.26,
            'revpar': 481.42,
            'room_revenue': 233536.80,
            'net_room_revenue': 259002.80,
            'service_charge': 23545.90,
            'other_income': 1920.10,
            'weekday': 'Tuesday'
        }
    })

# === 2. 更新/创建 MTD_MAY 汇总节点 ===
mtd_id = 'MTD_MAY_2026'
mtd = None
for n in nodes:
    if n['id'] == mtd_id:
        mtd = n
        break

if mtd:
    mtd['properties'] = {
        'rooms_sold': 7197,
        'occupancy': 70.41,
        'adr': 748.16,
        'revpar': 526.76,
        'net_room_revenue': 5384522.65,
        'f_b_total_revenue': 1828916.77
    }
    print(f'✅ Updated {mtd_id}')
else:
    nodes.append({
        'id': mtd_id,
        'type': 'FIN_MTD_SUMMARY',
        'label': '2026年5月MTD(1-19日)',
        'properties': {
            'rooms_sold': 7197,
            'occupancy': 70.41,
            'adr': 748.16,
            'revpar': 526.76,
            'net_room_revenue': 5384522.65,
            'f_b_total_revenue': 1828916.77
        }
    })
    print(f'✅ Created {mtd_id}')

# === 3. 创建 F&B outlet 日统计 ===
fb_nodes = [
    {'id': 'FB_OPEN_20260519', 'label': 'OPEN-5月19日', 'rev': 24360.57, 'covers': 66, 'avg_check': 75.30, 'mtd_rev': 417343.27},
    {'id': 'FB_YUXI_20260519', 'label': 'YUXI-5月19日', 'rev': 13662.66, 'covers': 29, 'avg_check': 326.22, 'mtd_rev': 271208.57},
    {'id': 'FB_BACIO_20260519', 'label': 'BACIO-5月19日', 'rev': 3208.22, 'covers': 13, 'avg_check': 230.90, 'mtd_rev': 30149.78},
    {'id': 'FB_YUAN_20260519', 'label': 'YUAN-5月19日', 'rev': 1819.62, 'covers': 7, 'avg_check': 264.89, 'mtd_rev': 23645.66},
    {'id': 'FB_STORE_20260519', 'label': 'STORE-5月19日', 'rev': 5021.71, 'covers': 65, 'avg_check': 143.68, 'mtd_rev': 18579.78},
    {'id': 'FB_IR_20260519', 'label': 'IR-5月19日', 'rev': 1019.80, 'covers': 8, 'avg_check': 128.76, 'mtd_rev': 25653.84},
    {'id': 'FB_TOTAL_20260519', 'label': 'F&B合计-5月19日', 'rev': 49092.58, 'covers': 100, 'avg_check': 208.09, 'mtd_rev': 1828916.77},
]

for fb in fb_nodes:
    exists = any(n['id'] == fb['id'] for n in nodes)
    if not exists:
        nodes.append({
            'id': fb['id'],
            'type': 'DAILY_FB_OUTLET',
            'label': fb['label'],
            'properties': {
                'revenue': fb['rev'],
                'covers': fb['covers'],
                'avg_check': fb['avg_check'],
                'mtd_revenue': fb['mtd_rev']
            }
        })

# === 4. 创建 MTD F&B 汇总 ===
fb_mtd = 'MTD_FB_MAY_2026'
if not any(n['id'] == fb_mtd for n in nodes):
    nodes.append({
        'id': fb_mtd,
        'type': 'FIN_FB_MTD',
        'label': '5月F&B MTD(1-19日)',
        'properties': {
            'total_revenue': 1828916.77,
            'days': 19
        }
    })

# === 5. 创建周同比分析节点 ===
wk_id = 'WOW_519_vs_512'
if not any(n['id'] == wk_id for n in nodes):
    nodes.append({
        'id': wk_id,
        'type': 'FIN_WOW_ANALYSIS',
        'label': '周同比: 5/12二 vs 5/19二',
        'properties': {
            'rooms_change': -51,
            'rooms_change_pct': -11.6,
            'occ_change': -9.48,
            'adr_change': 64.25,
            'adr_change_pct': 10.6,
            'net_revenue_change': -5991,
            'net_revenue_change_pct': -2.3,
            'summary': '量降价升，净收入微降2.3%，价格策略有效但流量不足'
        }
    })

# === 6. 关联边 ===
def add_edge(source, target, rel_type, props=None):
    eid = f'E_{source}_{rel_type}_{target}'
    if not any(e.get('id') == eid for e in edges):
        edge = {'id': eid, 'source': source, 'target': target, 'relation': rel_type}
        if props:
            edge['properties'] = props
        edges.append(edge)

# day_20260519 -> MTD_MAY_2026
add_edge(day_id, mtd_id, 'PART_OF')
# FB outlets -> day
for fb in ['FB_OPEN', 'FB_YUXI', 'FB_BACIO', 'FB_YUAN', 'FB_STORE', 'FB_IR', 'FB_TOTAL']:
    add_edge(f'{fb}_20260519', day_id, 'BELONGS_TO')
# FB total -> MTD FB
add_edge('FB_TOTAL_20260519', fb_mtd, 'PART_OF')
# 周同比从 day_20260512
add_edge(day_id, wk_id, 'HAS_WOW_ANALYSIS')
add_edge('day_20260512', wk_id, 'HAS_WOW_BASELINE')

# === Save ===
g['nodes'] = nodes
g['edges'] = edges
with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f'\n🏁 完成：{len(nodes)} 节点 | {len(edges)} 边')
print(f'备份: {BACKUP}')
