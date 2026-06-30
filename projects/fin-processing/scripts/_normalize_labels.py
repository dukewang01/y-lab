"""统一5月日报数据类型标签为英文"""
import json

fp = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center\\fin_graph.json'
with open(fp, 'r', encoding='utf-8-sig') as f:
    g = json.load(f)

fixed = 0
label_map = {
    '实际': 'actual',
    '预测': 'forecast',
}

for e in g['entities']:
    if e.get('type') == 'daily_revenue' and '2026_05' in e.get('id', ''):
        props = e.setdefault('properties', {})
        old = props.get('data_type', '')
        if old in label_map:
            props['data_type'] = label_map[old]
            fixed += 1
            print(f'  修正 {e["id"]}: {old} -> {label_map[old]}')

if fixed > 0:
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f'\n共修正 {fixed} 个节点')
else:
    print('无需修正')
