import json

f = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/faq_graph.json', 'r', encoding='utf-8')
d = json.load(f)

new_entry = {
    'id': 'FAQ_RISK_RING_LOST',
    'label': '客人在房间丢了戒指怎么办？处理流程和模板',
    'category': 'faq',
    'answer': (
        '客人在房间丢失戒指/首饰/贵重物品的标准处理流程（基于CMP-077+7个真实案例）：\n\n'
        '第一步·接报：安抚客人，询问房号/物品/最后一次见到的时间和位置，提醒"先别翻动，我们马上到"。\n\n'
        '第二步·到场：GSM+安保+客房主管三方到现场，当着客人的面共同查找。查找区域包括：床头柜/洗漱台/保险箱/行李箱/枕套床单/浴室地漏/垃圾车/真空吸尘器袋等。\n\n'
        '第三步·取证：读取电子门锁记录+调取走廊CCTV。门锁记录和监控是酒店自保的唯一证据。\n\n'
        '第四步·判定：找到→致歉安抚；未找到→"不是认定盗窃，是确认物品未能找到"。\n\n'
        '第五步·方案（收益保护优先）：\n'
        '- 无酒店过失 → 人文关怀（倾听+查找+解释），不换房不赔偿，避免主动背责\n'
        '- 有明确证据/金额大 → 客人自己决定是否报警，酒店配合提供资料\n'
        '- 酒店有明确过失 → 报告总经理决定补偿方案\n\n'
        '⚠️ 话术红线：不说"你是不是记错了？" / "我们的员工绝对不会这样" / 无责任时主动提议换房或赔偿\n\n'
        '📋 完整模板见：templates/TEMPLATE_RING_LOST_v1.md\n'
        '📎 关联预案：CMP-077 客房安全投诉/事件专项应急预案\n'
        '📎 关联案例：RCASE_8258 Tiffany戒指 / RCASE_8317 ￥60万戒指 / RCASE_8153 耳钉争议 / RCASE_8157 护肤品被怀疑'
    ),
    'tags': ['risk', 'global', 'loss', 'guest', 'lost'],
    'source': 'Y酒店运营体系 RISK工作站 + CMP-077'
}

entries = d.get('entities', [])
# 检查是否已存在
for e in entries:
    if e.get('id') == 'FAQ_RISK_RING_LOST':
        print('已存在，跳过')
        break
else:
    entries.append(new_entry)
    d['entities'] = entries

# 加relations
rels = d.get('relations', [])
rels.append({'source_id': 'FAQ_RISK_RING_LOST', 'target_id': 'TAG_RISK', 'relation': 'TAGGED_AS'})
rels.append({'source_id': 'FAQ_RISK_RING_LOST', 'target_id': 'TAG_GLOBAL', 'relation': 'TAGGED_AS'})

# 加relationships（references）
rels2 = d.get('relationships', [])
rels2.append({'source': 'FAQ_RISK_RING_LOST', 'target': 'CMP-077', 'relation': 'references'})
rels2.append({'source': 'FAQ_RISK_RING_LOST', 'target': 'RCASE_8258', 'relation': 'references'})
rels2.append({'source': 'FAQ_RISK_RING_LOST', 'target': 'RCASE_8317', 'relation': 'references'})

d['relations'] = rels
d['relationships'] = rels2

# 确保TAG实体存在
all_ids = set(e.get('id', '') for e in entries)
if 'TAG_RISK' not in all_ids:
    entries.append({'id': 'TAG_RISK', 'label': '风险', 'category': 'tag', 'tags': [], 'source': 'auto'})
if 'TAG_GLOBAL' not in all_ids:
    entries.append({'id': 'TAG_GLOBAL', 'label': '全局', 'category': 'tag', 'tags': [], 'source': 'auto'})
d['entities'] = entries

g = open('C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/faq_graph.json', 'w', encoding='utf-8')
json.dump(d, g, ensure_ascii=False, indent=2)
g.close()

print('FAQ条目已添加: FAQ_RISK_RING_LOST')
print('当前实体总数:', len(entries))
print('relations:', len(rels), 'relationships:', len(rels2))
