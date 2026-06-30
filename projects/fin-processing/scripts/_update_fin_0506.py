import json, openpyxl, copy

# 读图谱
fin_file = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center\\fin_graph.json'
with open(fin_file, 'r', encoding='utf-8-sig') as f:
    graph = json.load(f)

ents = graph['entities']
rels = graph['relations']

# 5月6日日报节点ID
daily_id = 'DAILY_2026_05_06'

# 找现有节点
daily_node = None
for e in ents:
    if e['id'] == daily_id:
        daily_node = e
        break

# 营收数据
daily_data = {
    'rooms_sold': 256,
    'occupancy_pct': 0.4758,
    'revpar': 306.42,
    'adr': 643.96,
    'total_rooms_revenue': 148431.54,
    'service_charge': 14986.62,
    'room_revenue': 164853.10,
    'guest_count': 340,
    
    # F&B - 从F&B表取值（非Actual表的封面数）
    'fb': {
        'banquet': {'revenue': 0, 'covers': 0, 'avg_check': 0},
        'open': {'revenue': 17838.70, 'covers': 261, 'avg_check': 68.35},
        'yuxi': {'revenue': 2621.11, 'covers': 5, 'avg_check': 524.22},
        'bacio': {'revenue': 1008.87, 'covers': 4, 'avg_check': 252.22},
        'beer': {'revenue': 0, 'covers': 0, 'avg_check': 0},
        'yuan': {'revenue': 569.35, 'covers': 3, 'avg_check': 189.78},
        'food_store': {'revenue': 0, 'covers': 0, 'avg_check': 0},
        'room_service': {'revenue': 388.39, 'covers': 4, 'avg_check': 97.10},
        'total_fb': {'revenue': 22426.42, 'covers': 277, 'avg_check': 80.96}
    }
}

# 更新节点属性
if daily_node:
    old_props = daily_node.get('properties', {})
    print(f'找到现有节点: {daily_node["name"]}')
    print(f'现有属性: {json.dumps(old_props, ensure_ascii=False)[:200]}')
    
    # 合并
    new_props = {
        'rooms_sold': daily_data['rooms_sold'],
        'occupancy_pct': daily_data['occupancy_pct'],
        'revpar': daily_data['revpar'],
        'adr': daily_data['adr'],
        'total_rooms_revenue': daily_data['total_rooms_revenue'],
        'service_charge': daily_data['service_charge'],
        'room_revenue': daily_data['room_revenue'],
        'guest_count': daily_data['guest_count'],
        'fb_data': json.dumps(daily_data['fb'], ensure_ascii=False)
    }
    # 保留旧的没覆盖的
    for k, v in old_props.items():
        if k not in new_props:
            new_props[k] = v
    
    daily_node['properties'] = new_props
    print(f'更新后属性数量: {len(new_props)}')
else:
    print(f'未找到节点 {daily_id}，创建新节点')
    new_ent = {
        'id': daily_id,
        'name': '日报 2026-05-06',
        'type': 'daily_revenue',
        'date': '2026-05-06',
        'properties': daily_data
    }
    ents.append(new_ent)

# 保存
with open(fin_file, 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

print(f'\n✅ 已更新 fin_graph.json')
print(f'   总实体: {len(ents)}, 总关系: {len(rels)}')
