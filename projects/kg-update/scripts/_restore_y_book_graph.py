import json

base = 'C:/Users/Duke Wang/.openclaw/workspace/knowledge_center/'
lib = json.load(open(base + 'lib_graph.json', 'r', encoding='utf-8'))
existing_ids = set(e.get('id', '') for e in lib['entities'])

max_id = 0
for e in lib['entities']:
    eid = e.get('id', '')
    if eid.startswith('LIB_'):
        try:
            n = int(eid.replace('LIB_', ''))
            if n > max_id:
                max_id = n
        except:
            pass

n = max_id + 1

def add(title, cat, status, rating, tags, notes, src='', subtitle='', author=''):
    global n
    bid = 'LIB_' + str(n).zfill(4)
    ent = {
        'id': bid, 'title': title, 'author_names': author, 'category': cat,
        'status': status, 'rating': rating, 'tags': tags, 'notes': notes,
        'type': 'book'
    }
    if subtitle:
        ent['subtitle'] = subtitle
    if src:
        ent['source_file'] = src
    lib['entities'].append(ent)
    for e in lib['entities']:
        if e.get('type') == 'category' and e.get('label', '') == cat:
            lib['relations'].append({'source_id': bid, 'target_id': e['id'], 'relation': 'in_category'})
            break
    smap = {'已读': 'LIB_STAT_READ', '在读': 'LIB_STAT_READING', '想读': 'LIB_STAT_WISHLIST'}
    if status in smap:
        lib['relations'].append({'source_id': bid, 'target_id': smap[status], 'relation': 'has_status'})
    n += 1
    return bid

added = []

# 缺的6本
added.append(add('《运动改造大脑》', '自我提升/思维', '已读', 4.0,
    ['脑科学', '运动', '健康', '神经'],
    '运动对大脑的积极影响：提升注意力、记忆力、情绪。有笔记。',
    'workspace/笔记_运动改造大脑.md', author='John J. Ratey'))

added.append(add('《他人的力量》', '心理学/沟通', '已读', 4.0,
    ['人际关系', '心理', '成长'],
    '人际关系中的四种力量：隔离, 连接, 赋能, 支持。有笔记。',
    'workspace/笔记_他人的力量.md', author='Henry Cloud'))

added.append(add('《原则》', '管理/领导力', '已读', 4.5,
    ['原则', '决策', '达利欧', '系统'],
    '桥水基金创始人瑞达利欧的生活和工作原则：激进的事实, 透明度, 可信度加权决策。有笔记。',
    'workspace/笔记_原则.md', subtitle='Principles', author='Ray Dalio'))

added.append(add('《顶级思维法7册合集》', '自我提升/思维', '已读', 4.0,
    ['思维', '方法', '合集', '7册'],
    '7本思维方法合集：表达, 影响, 领导, 合作, 筛选, 理解, 行动。完整思维技能链。有笔记。',
    'workspace/笔记_顶级思维法7册.md', author='多作者'))

added.append(add('《穷查理宝典》', '管理/领导力', '已读', 5.0,
    ['芒格', '价值投资', '思维模型', '误判心理学'],
    '芒格毕生智慧集大成：多元思维模型, 人类误判心理学, 检查清单。36万字/954页。有笔记。Duke推荐书。',
    'workspace/笔记_穷查理宝典.md', subtitle='查理芒格智慧箴言录', author='Peter Kaufman / 查理芒格'))

added.append(add('《芒格投资思想》', '财务/收益管理', '已读', 4.0,
    ['投资', '芒格', '价值', '思想'],
    '芒格核心投资思想和格栅理论。有笔记。',
    'workspace/笔记_芒格投资思想.md', author='查理芒格'))

# 5大合集
added.append(add('《世界管理学圣经18册》', '管理/领导力', '想读', 0,
    ['管理', '合集', '18册', '管理学圣经'],
    '18本管理学经典合集。有笔记摘要。',
    'workspace/笔记_世界管理学圣经18册.md', author='多作者'))

added.append(add('《思维认知书系10册》', '自我提升/思维', '想读', 0,
    ['思维', '认知', '合集', '10册'],
    '10本思维认知类书籍合集。有笔记摘要。',
    'workspace/笔记_思维认知书系10册.md', author='多作者'))

added.append(add('《诺贝尔经济学奖合集13册》', '财务/收益管理', '想读', 0,
    ['诺贝尔', '经济学', '合集', '13册'],
    '13本诺贝尔经济学奖得主著作合集。有笔记摘要。',
    'workspace/笔记_诺贝尔经济学奖合集13册.md', author='多作者'))

added.append(add('《中国社会学经典文库13册》', '心理学/沟通', '想读', 0,
    ['社会学', '中国', '合集', '13册'],
    '13本中国社会学经典著作合集。有笔记摘要。',
    'workspace/笔记_中国社会学经典文库13册.md', author='多作者'))

added.append(add('《商业入门经典4册》', '管理/领导力', '想读', 0,
    ['商业', '入门', '合集', '4册'],
    '4本商业入门经典合集。有笔记摘要。',
    'workspace/笔记_商业入门经典4册.md', author='多作者'))

# Duke推荐5本 (思考快与慢已存在LIB_0006)
added.append(add('《富兰克林传》', '传记/商业史', '想读', 0,
    ['传记', '富兰克林', '艾萨克森', 'Duke推荐'],
    '本杰明富兰克林传记，艾萨克森作品。13项美德, 自我完善。Duke推荐书。',
    author='沃尔特艾萨克森'))

# 思考快与慢已存在
print('(思考快与慢: 已在LIB_0006, 跳过)')

added.append(add('《枪炮、病菌与钢铁》', '心理学/沟通', '想读', 0,
    ['人类', '文明', '地理', '演化', 'Duke推荐'],
    '人类社会发展的终极解释：地理决定论。不同大陆文明的差异根源。Duke推荐书。',
    author='Jared Diamond'))

added.append(add('《系统之美》', '管理/领导力', '想读', 0,
    ['系统', '思维', '反馈', '杠杆', 'Duke推荐'],
    '系统思考入门经典：存量, 流量, 反馈, 杠杆点。系统思维理论框架。Duke推荐书。',
    author='Donella Meadows'))

added.append(add('《断舍离》', '自我提升/思维', '想读', 0,
    ['整理', '极简', '生活', '心灵', 'Duke推荐'],
    '断=断绝不需要的, 舍=舍弃多余的, 离=脱离执念。Duke推荐书。',
    author='山下英子'))

# 保存
with open(base + 'lib_graph.json', 'w', encoding='utf-8') as f:
    json.dump(lib, f, ensure_ascii=False, indent=2)

# 更新FAQ
faq = json.load(open(base + 'faq_graph.json', 'r', encoding='utf-8'))
for e in faq['entities']:
    if e['id'] == 'FAQ_LIB_HOW':
        answer = (
            'Lib知识站（独立于MEP/FSAA/QA/RISK运营体系的书籍库，不局限酒店相关）：\n\n'
            '📚 当前藏书45本，涵盖10个分类：\n'
            '  管理/领导力（17本）| 自我提升/思维（11本）\n'
            '  心理学/沟通（9本）| 财务/收益管理（4本）\n'
            '  酒店运营（3本）| 传记/商业史（1本）\n\n'
            '🧠 另含10个思维模型（来自《100个思维模型》提炼）\n\n'
            '✅ 已读22本 | 📖 在读0本 | 📌 想读23本\n\n'
            '📂 数据文件：knowledge_center/lib_graph.json\n'
            '🔍 实体ID前缀：LIB_\n'
            '🏷️ 每本书有独立tags，搜书名关键词即可命中\n\n'
            '提示：Lib站独立运行不跨站关联，搜"图书馆""Lib""书名"均可命中。'
        )
        e['answer'] = answer
        break

with open(base + 'faq_graph.json', 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)

print()
print('完成。新增15本:')
for bid in added:
    print('  ' + bid)

print()
book_cnt = len([e for e in lib['entities'] if e.get('type') == 'book'])
mdl_cnt = len([e for e in lib['entities'] if e.get('type') == 'thought_model'])
print('Lib站总计: 书籍' + str(book_cnt) + '本 | 思维模型' + str(mdl_cnt) + '个 | 总实体' + str(len(lib['entities'])))
