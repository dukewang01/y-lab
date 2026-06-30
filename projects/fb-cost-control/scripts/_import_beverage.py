#!/usr/bin/env python3
"""
导入酒水仓盘点表到FIN站 + FB站
源：2025年11月26日酒水仓盘点PDF
"""
import sys, json, pdfplumber
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

PDF = r'C:\Users\Duke Wang\.openclaw\media\inbound\é_æ_ä---5bb9070f-cb2c-4227-a55c-cba117361c49.pdf'
FIN_GRAPH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json'
FB_GRAPH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_graph.json'

# 解析PDF
categories = defaultdict(list)
current_group = ''
current_type = ''

with pdfplumber.open(PDF) as pdf:
    for page in pdf.pages:
        text = page.extract_text() or ''
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '组 ' in line and len(line) < 30:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == '组' and i+1 < len(parts):
                        current_group = parts[i+1]
            if '类型 ' in line and len(line) < 40:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == '类型' and i+1 < len(parts):
                        current_type = parts[i+1]
            
            if line and line[0].isdigit() and len(line) > 10:
                parts = line.split()
                if len(parts) >= 7:
                    try:
                        qty = float(parts[-2])
                        price = float(parts[-1])
                        name_parts = parts[1:-2]
                        name = ' '.join(name_parts[:3])
                        categories[current_group].append({
                            'code': parts[0],
                            'name': name,
                            'qty': qty,
                            'price': price,
                            'total': qty * price
                        })
                    except:
                        pass

# ===== 1. 导入FIN站 =====
fin = json.load(open(FIN_GRAPH, 'r', encoding='utf-8'))

# 创建盘点汇总节点
beverage_inv_id = 'BEVERAGE_INV_2025_11'
fin['entities'].append({
    'id': beverage_inv_id,
    'name': '酒水仓盘点 2025-11-26',
    'type': 'inventory_report',
    'date': '2025-11-26',
    'properties': {
        'type': 'beverage_inventory',
        'total_items': sum(len(v) for v in categories.values()),
        'total_value': round(sum(i['total'] for items in categories.values() for i in items), 2),
        'location': '5378BEV BEVERAGE STORE',
        'source': '酒水仓盘点表_20251126.pdf'
    }
})

# 按大类创建子节点
group_map = {'BEER':'啤酒','REDWINE':'红葡萄酒','WHTEWINE':'白葡萄酒','SPKLWINE':'气泡酒','SPIRITS':'烈酒','SOFTDRK':'软饮'}
new_nodes = []
for group, items in categories.items():
    subtotal = sum(i['total'] for i in items)
    gid = f'BEV_CATE_{group}_{202511}'
    fin['entities'].append({
        'id': gid,
        'name': f'酒水仓 {group_map.get(group, group)}',
        'type': 'inventory_category',
        'properties': {
            'group': group,
            'item_count': len(items),
            'total_value': round(subtotal, 2),
            'date': '2025-11-26'
        }
    })
    new_nodes.append(gid)
    
    # BELONGS_TO 关系
    fin['relationships'].append({
        'source': gid,
        'target': beverage_inv_id,
        'type': 'BELONGS_TO',
        'relation': 'BELONGS_TO',
        'context': 'beverage_inventory'
    })

# 关联到2025年11月的fin节点（如果有）
for e in fin.get('entities', []):
    if e.get('type') in ['month','date']:
        if '2025-11' in str(e.get('date','')) or e.get('name','') == '2025-11':
            fin['relationships'].append({
                'source': beverage_inv_id,
                'target': e['id'],
                'type': 'HAS_INVENTORY',
                'relation': 'HAS_INVENTORY',
                'context': 'cross_station'
            })
            break

# 保存FIN站
json.dump(fin, open(FIN_GRAPH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('✅ FIN站: %d新节点, %d新关系' % (len(categories)+1, len(categories)+1))

# ===== 2. 导入FB站 =====
fb = json.load(open(FB_GRAPH, 'r', encoding='utf-8'))

# FB站建立详细的酒水产品节点
bev_store_id = 'BEV_STORE_5378'
fb['entities'].append({
    'id': bev_store_id,
    'name': '5378BEV 酒水仓',
    'type': 'beverage_store',
    'properties': {
        'cost_center': '5378BEV',
        'location': 'B1',
        'date': '2025-11-26',
        'total_value': round(sum(i['total'] for items in categories.values() for i in items), 2)
    }
})

# 为每款酒水建节点
fb_rels = 0
for group, items in categories.items():
    for item in items:
        item_id = f'BEV_{item["code"]}'
        # 去重
        if not any(e['id'] == item_id for e in fb.get('entities',[])):
            fb['entities'].append({
                'id': item_id,
                'name': item['name'][:40],
                'type': 'beverage_product',
                'properties': {
                    'code': item['code'],
                    'group': group,
                    'category': group_map.get(group, group),
                    'unit_price': item['price'],
                    'qty': item['qty'],
                    'total_value': round(item['total'], 2),
                    'unit': '瓶/罐',
                    'store': '5378BEV'
                }
            })
        # 酒水产品 → 酒水仓关系
        fb['relationships'].append({
            'source': item_id,
            'target': bev_store_id,
            'type': 'STORED_AT',
            'relation': 'STORED_AT'
        })
        fb_rels += 1

# 酒水仓 → FIN站成本关系（跨站）
fin_inv_id = beverage_inv_id
fb['relationships'].append({
    'source': bev_store_id,
    'target': fin_inv_id,
    'type': 'HAS_INVENTORY_REPORT',
    'relation': 'HAS_INVENTORY_REPORT',
    'context': 'cross_station'
})

json.dump(fb, open(FB_GRAPH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
fb_new_items = sum(1 for items in categories.values() for i in items)
print('✅ FB站: ~%d新节点, %d新关系' % (fb_new_items, fb_rels + 1))
print()
print('入库完成！酒水仓盘点表已导入两站')
