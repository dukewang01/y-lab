import json

# ===== 1. FSAA 更新 =====
f = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/fsaa_graph.json', 'r', encoding='utf-8')
d = json.load(f)
ent = d['entities']
rels = d.get('relations', [])

new_entities = [
    # 2F: 啤酒荟厨房
    {
        'id': 'KITCHEN_BEER',
        'label': '啤酒荟厨房(2F)',
        'name_en': 'Beer Society Kitchen 2F',
        'category': 'area',
        'description': '啤酒荟出品厨房，含简餐/小食/酒水吧台'
    },
    # 3F: 面馆厨房（外包）
    {
        'id': 'KITCHEN_NOODLE_3F',
        'label': '3F面馆厨房(外包)',
        'name_en': '3F Noodle Kitchen (Outsourced)',
        'category': 'area',
        'description': '3F面馆外包厨房，主营苏式面/馄饨/浇头'
    },
    # 6F: 烧腊间
    {
        'id': 'KITCHEN_BBQ_6F',
        'label': '6F烧腊间',
        'name_en': '6F BBQ Room',
        'category': 'area',
        'description': '宴会烧腊出品间，烧鹅/叉烧/乳猪/烧肉'
    },
    # 6F: 点心房
    {
        'id': 'KITCHEN_DIMSUM_6F',
        'label': '6F点心房',
        'name_en': '6F Dim Sum Room',
        'category': 'area',
        'description': '宴会点心出品间，蒸点/炸点/肠粉/煎炸'
    },
    # 6F: 烤鸭间
    {
        'id': 'KITCHEN_ROAST_DUCK_6F',
        'label': '6F烤鸭间',
        'name_en': '6F Roast Duck Room',
        'category': 'area',
        'description': '北京烤鸭/片皮鸭专用烤制间'
    },
    # 2F啤酒厨房checklist
    {
        'id': 'CHECK_BEER_KITCHEN',
        'label': '啤酒荟厨房卫生检查',
        'name_en': 'Beer Kitchen Hygiene Check',
        'category': 'checklist',
        'description': '啤酒荟厨房/吧台卫生、温度、食材保质期检查'
    },
    # 3F面馆checklist
    {
        'id': 'CHECK_NOODLE_KITCHEN_3F',
        'label': '3F面馆厨房卫生检查',
        'name_en': '3F Noodle Kitchen Hygiene Check',
        'category': 'checklist',
        'description': '面馆厨房温度/汤底/浇头/面食加工/外包方健康证检查'
    },
    # 6F烧腊间checklist
    {
        'id': 'CHECK_BBQ_6F',
        'label': '6F烧腊间卫生检查',
        'name_en': '6F BBQ Room Hygiene Check',
        'category': 'checklist',
        'description': '烧腊间温度/腌制/烤制/冷却/展示卫生检查'
    },
    # 6F点心房checklist
    {
        'id': 'CHECK_DIMSUM_6F',
        'label': '6F点心房卫生检查',
        'name_en': '6F Dim Sum Room Hygiene Check',
        'category': 'checklist',
        'description': '点心房蒸点/炸点/馅料/温度/标签检查'
    },
    # 6F烤鸭间checklist
    {
        'id': 'CHECK_ROAST_DUCK_6F',
        'label': '6F烤鸭间卫生检查',
        'name_en': '6F Roast Duck Room Hygiene Check',
        'category': 'checklist',
        'description': '烤鸭腌制/挂炉/片鸭/保温/鸭架处理检查'
    },
]

# 检查是否已存在
existing_ids = set(e.get('id', '') for e in ent)
added = 0
for ne in new_entities:
    if ne['id'] not in existing_ids:
        ent.append(ne)
        added += 1

# 添加relations
new_rels = [
    {'source_id': 'KITCHEN_BEER', 'target_id': 'FLR_2F', 'relation': 'LOCATED_IN'},
    {'source_id': 'KITCHEN_NOODLE_3F', 'target_id': 'FLR_3F', 'relation': 'LOCATED_IN'},
    {'source_id': 'KITCHEN_BBQ_6F', 'target_id': 'FLR_6F', 'relation': 'LOCATED_IN'},
    {'source_id': 'KITCHEN_DIMSUM_6F', 'target_id': 'FLR_6F', 'relation': 'LOCATED_IN'},
    {'source_id': 'KITCHEN_ROAST_DUCK_6F', 'target_id': 'FLR_6F', 'relation': 'LOCATED_IN'},
    # 外包标识
    {'source_id': 'KITCHEN_NOODLE_3F', 'target_id': 'OUTLET_YUXI', 'relation': 'SUB_OF'},
]

for nr in new_rels:
    rels.append(nr)

d['entities'] = ent
d['relations'] = rels

g = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/fsaa_graph.json', 'w', encoding='utf-8')
json.dump(d, g, ensure_ascii=False, indent=2)
g.close()
print(f'FSAA 更新完成: +{added}实体, +{len(new_rels)}关系')
print(f'当前FSAA实体: {len(ent)}, 关系: {len(rels)}')


# ===== 2. 更新FAQ图谱 =====
f2 = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/faq_graph.json', 'r', encoding='utf-8')
d2 = json.load(f2)
faq_ent = d2['entities']

# 更新厨房分布FAQ
faq_kitchen_layout = {
    'id': 'FAQ_KITCHEN_LAYOUT',
    'label': '酒店有哪些厨房？分布在哪？',
    'category': 'faq',
    'answer': (
        '苏州希尔顿酒店厨房分布（11个出品厨房）：\n\n'
        'B1层：员工餐厅厨房\n'
        '2F：啤酒荟厨房（简餐/小食/吧台）\n'
        '3F：御玺中餐厅厨房（热菜/冷菜/海鲜活鲜）+ 面馆厨房（外包，苏式面/馄饨/浇头）\n'
        '5F：ADD全日制主厨房（开放式/面档/煎蛋/冷房/寿司/饼房/巧克力间）+ BACIO意大利厨房\n'
        '6F：宴会厨房 + 烧腊间 + 点心房 + 烤鸭间\n'
        '42F：行政酒廊备餐间\n\n'
        '另有送餐部(5F)、各楼层洗碗间配套。'
    ),
    'tags': ['mep', 'fsaa', 'global', 'kitchen', 'restaurant'],
    'source': 'FK Y酒店运营体系 厨房布局v1.1'
}

existing_faq_ids = set(e.get('id', '') for e in faq_ent)
if faq_kitchen_layout['id'] not in existing_faq_ids:
    faq_ent.append(faq_kitchen_layout)

d2['entities'] = faq_ent

g2 = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/faq_graph.json', 'w', encoding='utf-8')
json.dump(d2, g2, ensure_ascii=False, indent=2)
g2.close()
print(f'FAQ更新完成: +1条目（FAQ_KITCHEN_LAYOUT）')
