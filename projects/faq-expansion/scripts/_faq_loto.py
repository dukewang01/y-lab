"""FAQ新增：上锁挂牌（LOTO）安全工作系统（SSOW 3.18）"""
import json, shutil, os

BASE = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
faq = json.load(open(os.path.join(BASE, 'faq_graph.json'), encoding='utf-8'))

max_id = 0
for e in faq['entities']:
    eid = e.get('id', '')
    if eid.startswith('FAQ_'):
        try: n = int(eid.split('_')[-1]); max_id = max(max_id, n)
        except: pass

nk = max_id

e1 = {
    'id': f'FAQ_{nk+1}',
    'label': '上锁挂牌（LOTO）使用安全工作系统（SSOW 3.18）',
    'description': (
        '【上锁挂牌（LOTO）使用安全工作系统 — 基于希尔顿SSOW 3.18】\n\n'
        '上锁挂牌（LOTO）是一项重要的安全程序，旨在保护工作人员在设备维护或维修期间免受意外能量释放的伤害。\n'
        'LOTO能防止工作人员在接触电/水等危险能源时遭遇意外、受伤和死亡。\n\n'
        '仅接受过培训的团队成员可以完成需要LOTO隔离的任务。每年培训。\n'
        '开始工作前，可能需要工作许可。\n\n'
        '一、作业前（LOTO启动）\n'
        '  1. 审查承包商风险评估并确保其符合要求（如适用）\n'
        '  2. 确定设备并评估范围和危险\n'
        '  3. 向所有相关团队成员传达任务细节和LOTO程序\n'
        '  4. **关闭并断开所有能源**\n'
        '  5. 使用合适的上锁/挂牌装置，限制使用设备\n'
        '  6. 团队成员应熟悉潜在危险\n'
        '  7. 向受影响部门告知停工计划\n'
        '  8. **验证设备状态，安全疏散储存的能量**（验电/泄压/排水等）\n'
        '  9. 审查应急程序，确保应急设备可供使用\n'
        '  10. 签发必要的工作许可，概述工作范围\n\n'
        '二、执行任务期间\n'
        '  · 确认已有效断开所有能源\n'
        '  · 开始工作前，确认储存的能量已疏散\n'
        '  · 使用适当的PPE\n'
        '  · 按计划执行维护或维修任务\n'
        '  · 监控工作区域是否存在意外和相关危险\n'
        '  · 定期检查上锁/挂牌装置是否安全\n'
        '  · 向相关人员通报任何变化或问题\n'
        '  · 遵守既定的安全程序\n\n'
        '三、作业后（LOTO解除）\n'
        '  1. 验证维护或维修任务的完成情况\n'
        '  2. **拆除上锁/挂牌装置，恢复设备**\n'
        '  3. 如适用，停用工作许可\n'
        '  4. 告知所有人员，设备已恢复运行\n\n'
        '【红线】\n'
        '  · 严禁未接受LOTO培训的人员执行LOTO\n'
        '  · 严禁未验证能量释放即开始作业\n'
        '  · 严禁**单人拆除他人上锁**（必须由上锁人本人拆除）\n'
        '  · 严禁绕开/旁路上锁装置\n\n'
        '【风险】触电、夹伤、接触化学品、溺水、热暴露、气体/压力释放、噪音、爆炸\n\n'
        '【工具】适合任务的LOTO工具包（断水/断电/断气），LOTO标签+锁具\n'
        '【通讯】手机、对讲机\n\n'
        '【培训要求】每年一次\n\n'
        '【责任部门】工程部（涉及所有需要LOTO的部门）'
    ),
    'category': 'ssow',
    'tags': ['LOTO', '上锁挂牌', '注销', '锁具', '挂牌', '能量隔离', '工程部', 'SSOW', '三级SSOW'],
    'department': '工程部',
    'ppe_list': ['因任务而异'],
    'hazards': ['触电', '夹伤', '接触化学品', '溺水', '热暴露', '气体/压力释放', '噪音', '爆炸'],
    'step_count': 3
}
faq['entities'].append(e1)
faq['relationships'] = faq.get('relationships', [])
for t in set(e1['tags']):
    faq['relationships'].append({'source': e1['id'], 'target': t, 'relation': 'tagged_as'})

tmp = os.path.join(BASE, 'faq_graph.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)
shutil.move(tmp, os.path.join(BASE, 'faq_graph.json'))

print(f'新增LOTOFQA: {e1["id"]}')
print(f'FAQ总量: {len(faq["entities"])} 实体 / {len(faq["relationships"])} 关系')
