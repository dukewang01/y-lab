#!/usr/bin/env python3
"""Retry CRM bridge for OPEN dinner menu items."""
import json

with open(r'knowledge_center\fb_graph.json', 'r', encoding='utf-8') as f:
    g = json.load(f)

ents = g['entities']
rels = g.get('relations', [])

# Find all OPEN dinner menu items
menu_items = [e for e in ents if e.get('id','').startswith('ITEM_OPEN_DIN_')]
print(f'OPEN dinner items found: {len(menu_items)}')

# Tag mapping
tag_mapping = {
    '\u5c0f\u9f99\u867e': ['\u6d77\u9c9c\u7231\u597d\u8005', '\u8fa3\u5473\u504f\u597d', '\u590f\u5b63\u65f6\u4ee4'],
    '\u6d77\u9c9c': ['\u6d77\u9c9c\u7231\u597d\u8005', '\u54c1\u8d28\u8ffd\u6c42'],
    '\u523a\u8eab': ['\u65e5\u6599\u7231\u597d\u8005', '\u6d77\u9c9c\u7231\u597d\u8005'],
    '\u5bff\u53f8': ['\u65e5\u6599\u7231\u597d\u8005'],
    '\u725b\u8089': ['\u8089\u98df\u7231\u597d\u8005', '\u54c1\u8d28\u8ffd\u6c42'],
    '\u70e4\u9e2d': ['\u4e2d\u9910\u504f\u597d', '\u8089\u98df\u7231\u597d\u8005'],
    '\u5496\u55b1': ['\u4e1c\u5357\u4e9a\u504f\u597d', '\u8fa3\u5473\u504f\u597d'],
    '\u751c\u54c1': ['\u751c\u54c1\u7231\u597d\u8005'],
    '\u51b0\u6dc7\u6dcb': ['\u751c\u54c1\u7231\u597d\u8005', '\u4eb2\u5b50\u5ba2\u7fa4'],
    '\u6c64\u9762': ['\u4e2d\u9910\u504f\u597d', '\u8f7b\u98df\u504f\u597d'],
    '\u6c99\u62c9': ['\u8f7b\u98df\u504f\u597d', '\u5065\u5eb7\u996e\u98df'],
    '\u78b3\u70e4': ['\u8089\u98df\u7231\u597d\u8005', '\u793e\u4ea4\u805a\u9910'],
    '\u70e7\u9e2d': ['\u4e2d\u9910\u504f\u597d'],
    '\u86cb\u7cd5': ['\u751c\u54c1\u7231\u597d\u8005', '\u4e0b\u5348\u8336\u5ba2\u7fa4'],
    '\u5e03\u4e01': ['\u751c\u54c1\u7231\u597d\u8005', '\u4eb2\u5b50\u5ba2\u7fa4'],
    '\u7cd6\u6c34': ['\u751c\u54c1\u7231\u597d\u8005', '\u4e2d\u9910\u504f\u597d'],
    '\u829d\u58eb': ['\u751c\u54c1\u7231\u597d\u8005', '\u54c1\u8d28\u8ffd\u6c42'],
    '\u5de7\u514b\u529b': ['\u751c\u54c1\u7231\u597d\u8005', '\u4eb2\u5b50\u5ba2\u7fa4'],
    '\u70e4\u751f\u82a5': ['\u6d77\u9c9c\u7231\u597d\u8005', '\u70e7\u70e4\u504f\u597d'],
    '\u7f8a\u8089': ['\u8089\u98df\u7231\u597d\u8005', '\u70e7\u70e4\u504f\u597d'],
    '\u9c7c': ['\u6d77\u9c9c\u7231\u597d\u8005', '\u5065\u5eb7\u996e\u98df'],
    '\u9e21': ['\u8089\u98df\u7231\u597d\u8005'],
    '\u7334\u6843': ['\u75de\u5b50\u5ba2\u7fa4'],
    '\u68a8': ['\u5065\u5eb7\u996e\u98df'],
    '\u897f\u74dc': ['\u5065\u5eb7\u996e\u98df', '\u5bb6\u5ead\u5ba2\u7fa4'],
}

# Find existing CRM preference tags in FB graph
crm_tag_ids = set()
for e in ents:
    if e.get('type') == 'crm_preference_tag':
        crm_tag_ids.add(e['id'])

print(f'Existing CRM tags: {len(crm_tag_ids)}')

new_rels = 0
new_tags = 0

for item in menu_items:
    item_name = item.get('name', '')
    for keyword, tags in tag_mapping.items():
        if keyword in item_name:
            for tag_name in tags:
                tag_id = f'CRM_TAG_{tag_name}'
                
                # Create tag if not exists
                if tag_id not in crm_tag_ids:
                    ents.append({
                        'id': tag_id,
                        'name': tag_name,
                        'type': 'crm_preference_tag',
                        'labels': ['CRM\u504f\u597d\u6807\u7b7e'],
                        'properties': {}
                    })
                    crm_tag_ids.add(tag_id)
                    new_tags += 1
                
                # Create RECOMMENDED_FOR
                rel_id = f'E_{item["id"]}_RECOMMENDED_FOR_{tag_id}'
                if not any(r.get('id') == rel_id for r in rels):
                    rels.append({
                        'id': rel_id,
                        'source': item['id'],
                        'target': tag_id,
                        'relation': 'RECOMMENDED_FOR'
                    })
                    new_rels += 1

# Save
g['entities'] = ents
g['relations'] = rels
with open(r'knowledge_center\fb_graph.json', 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f'New tags created: {new_tags}')
print(f'New RECOMMENDED_FOR relationships: {new_rels}')
print(f'Total: {len(ents)} entities, {len(rels)} relations')
print('Done!')
