import json, re

base = 'C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/'

# Update FAQ_LIB_HOW
faq = json.load(open(base + 'faq_graph.json', 'r', encoding='utf-8'))
for e in faq['entities']:
    if e['id'] == 'FAQ_LIB_HOW':
        answer_lines = [
            'Lib知识站（独立于MEP/FSAA/QA/RISK运营体系的书籍库，不局限酒店相关）：\n\n',
            '📚 当前藏书28本，涵盖10个分类：\n',
            '  管理/领导力（11本）| 心理学/沟通（4本）\n',
            '  自我提升/思维（7本）| 酒店运营（3本）\n',
            '  财务/收益管理（2本）| 其他（1本）\n\n',
            '🧠 另含10个思维模型（来自《100个思维模型》提炼）\n\n',
            '✅ 已读12本 | 📖 在读0本 | 📌 想读16本\n\n',
            '📂 数据文件：knowledge_center/lib_graph.json\n',
            '🔍 实体ID前缀：LIB_\n',
            '🏷️ 每本书有独立tags，搜书名关键词即可命中\n\n',
            '提示：Lib站独立运行不跨站关联，搜"图书馆""Lib""书名"均可命中。'
        ]
        e['answer'] = ''.join(answer_lines)
        print('FAQ_LIB_HOW 已更新')
        break

with open(base + 'faq_graph.json', 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)

# 污染检查
pat = re.compile(r'^LIB_')
for fn in ['mep_graph.json', 'fsaa_graph.json', 'risk_graph.json', 'qa_graph.json']:
    d = json.load(open(base + fn, 'r', encoding='utf-8'))
    ents = sum(1 for e in d['entities'] if pat.match(e.get('id', '')))
    all_rels = d.get('relations', []) + d.get('relationships', [])
    rels = sum(1 for r in all_rels if 'LIB_' in str(r) and 'CALIB' not in str(r))
    status = '无泄露' if ents + rels == 0 else '有泄露'
    print(f'  {fn[:12]:12s} | 实体泄露:{ents} 关系泄露:{rels} | {status}')
