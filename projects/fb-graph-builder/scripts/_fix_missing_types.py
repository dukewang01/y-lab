"""修复实体缺少type字段"""
import json

BASE = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center'

for name in ['risk_graph', 'gsm_graph']:
    fp = f'{BASE}\\{name}.json'
    with open(fp, 'r', encoding='utf-8-sig') as f:
        d = json.load(f)
    
    fixed = 0
    for e in d.get('entities', []):
        if not e.get('type'):
            # 根据节点id推断类型
            eid = e.get('id', '').lower()
            if 'case' in eid or 'cmp' in eid:
                e['type'] = 'case'
            elif 'faq' in eid:
                e['type'] = 'faq'
            elif 'sop' in eid:
                e['type'] = 'sop'
            elif 'rule' in eid:
                e['type'] = 'rule'
            elif 'law' in eid:
                e['type'] = 'regulation'
            elif 'risk' in eid:
                e['type'] = 'risk_factor'
            elif 'person' in eid or 'staff' in eid:
                e['type'] = 'person'
            else:
                e['type'] = 'concept'
            fixed += 1
    
    if fixed > 0:
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f'{name}: 修复 {fixed} 个实体')
    else:
        print(f'{name}: 无需修复')

print('完成!')
