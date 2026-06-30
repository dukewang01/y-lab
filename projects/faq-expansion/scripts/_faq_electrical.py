"""FAQ新增：电力工程（内部）安全工作系统（SSOW 3.1）"""
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
    'label': '电力工程（内部）安全工作制度（SSOW 3.1）',
    'description': (
        '【电力工程（内部）安全工作制度 — 基于希尔顿SSOW 3.1】\n\n'
        '任何需要在带电电气装置或设备上完成的工作，都必须由合格电工在获得工作许可的情况下进行。\n'
        '每年接受培训。\n\n'
        '一、作业前（通用）\n'
        '  · 根据当地法律要求，完成风险评估中的相关控制措施\n'
        '  · 如适用，封锁工作区域，确保不让他人面临风险\n'
        '  · **关闭/切断并锁定电源（LOTO上锁挂牌）**\n'
        '  · 将工作计划告知主管\n'
        '  · 如需更多信息，参阅《希尔顿健康与安全手册》\n\n'
        '二、插头接线（仅限合格团队人员）\n'
        '  · 只能为两相设备接线（内部有3根电线）\n'
        '  · 所有电线必须连接到正确的端子上\n'
        '  · 接地线（绿/黄）必须正确连接到顶部引脚\n'
        '  · 必须根据设备类型为插头安装正确的保险丝\n\n'
        '三、更换灯泡\n'
        '  · 如需进入天花板区域→遵守**高空作业培训要求**\n'
        '  · 更换灯泡前，确认电源已切断\n'
        '  · 务必为灯具使用**正确瓦数**的灯泡\n\n'
        '四、作业后\n'
        '  · 确保区域安全\n'
        '  · 重新接通电源\n'
        '  · 移除任何安全标志/锥形筒\n\n'
        'PPE：因任务而异（根据风险评估确定）\n\n'
        '【红线】\n'
        '  · 严禁未经断电/LOTO即进行任何电气作业\n'
        '  · 严禁非合格人员操作电气设备\n'
        '  · 严禁带电作业（非紧急情况——紧急需工作许可）\n'
        '  · 严禁超过灯具额定瓦数更换灯泡\n\n'
        '【风险】触电/烧伤、火灾\n\n'
        '【PPE】因任务而异\n\n'
        '【培训要求】每年一次\n\n'
        '【责任部门】工程部'
    ),
    'category': 'ssow',
    'tags': ['电气', '电力工程', '电工', '带电', '插头接线', '换灯泡', '工程部', 'SSOW', '三级SSOW'],
    'department': '工程部',
    'ppe_list': ['因任务而异'],
    'hazards': ['触电/烧伤', '火灾'],
    'step_count': 4
}
faq['entities'].append(e1)
faq['relationships'] = faq.get('relationships', [])
for t in set(e1['tags']):
    faq['relationships'].append({'source': e1['id'], 'target': t, 'relation': 'tagged_as'})

tmp = os.path.join(BASE, 'faq_graph.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)
shutil.move(tmp, os.path.join(BASE, 'faq_graph.json'))

print(f'新增电力工程FAQ: {e1["id"]}')
print(f'FAQ总量: {len(faq["entities"])} 实体 / {len(faq["relationships"])} 关系')
