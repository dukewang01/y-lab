"""FAQ新增：更换空调机组皮带安全工作系统（SSOW 3.12）"""
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
    'label': '更换空调机组皮带安全工作系统（SSOW 3.12）',
    'description': (
        '【更换空调机组皮带安全工作系统 — 基于希尔顿SSOW 3.12】\n\n'
        '仅年满18周岁、接受过培训的团队成员可以使用此设备。每年培训一次。\n\n'
        '一、作业前\n'
        '  · 告知经理你的位置\n'
        '  · 完成目视检查（设备状态+工具）\n'
        '  · 用锥形筒封闭工作区域\n'
        '  · 系统断电+上锁挂牌（LOTO），张贴"请勿接通电源"警告标志\n'
        '  · 确认工作区域无危险\n'
        '  · 不穿着宽松/臃肿衣物，防夹入运动部件\n\n'
        '二、佩戴PPE\n'
        '  · 手套\n'
        '  · 护目镜\n'
        '  · 护耳器（空调机房噪音通常≥85dB）\n'
        '  · 防护帽\n\n'
        '三、拆除\n'
        '  · 小心**夹点**——谨防手和手指被夹，尤其是皮带进入滑轮/链轮处\n'
        '  · 卸下防护罩，检查有无损坏\n'
        '  · 检查传动部件是否有磨损或摩擦痕迹→清洁并调整防护罩\n'
        '  · 检查皮带是否磨损或损坏→按需更换\n\n'
        '四、安装调整\n'
        '  · 检查皮带张力并按需调整\n'
        '  · 重新检查滑轮/链轮是否对准\n'
        '  · 重新安装皮带防护罩\n'
        '  · 如适用，重新安装外壳\n\n'
        '五、通电试运\n'
        '  · 重新接通电源\n'
        '  · 重新启动传动装置\n'
        '  · 观察并倾听是否有异常情况（异响/振动/异味）\n\n'
        '【红线】\n'
        '  · 严禁不LOTO即开始作业\n'
        '  · 严禁在皮带运转时调整/张紧\n'
        '  · 严禁未装回防护罩即通电试运\n'
        '  · 严禁宽松衣物/长发靠近运动部件\n\n'
        '【风险】夹伤（手指/手掌被皮带-滑轮回转夹入）、噪音（≥85dB）、封闭空间（机房）\n\n'
        '【PPE】手套 + 护目镜 + 护耳器 + 防护帽\n\n'
        '【培训要求】每年一次\n\n'
        '【责任部门】工程部'
    ),
    'category': 'ssow',
    'tags': ['空调', '空调机组', '皮带', 'AHU', '更换皮带', '传动', '工程部', 'SSOW', '三级SSOW'],
    'department': '工程部',
    'ppe_list': ['手套', '护目镜', '护耳器', '防护帽'],
    'hazards': ['夹伤  手指/手掌被皮带-滑轮回转夹入', '噪音  ≥85dB', '封闭空间  机房'],
    'step_count': 5
}
faq['entities'].append(e1)
faq['relationships'] = faq.get('relationships', [])
for t in set(e1['tags']):
    faq['relationships'].append({'source': e1['id'], 'target': t, 'relation': 'tagged_as'})

tmp = os.path.join(BASE, 'faq_graph.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)
shutil.move(tmp, os.path.join(BASE, 'faq_graph.json'))

print(f'新增更换空调机组皮带FAQ: {e1["id"]}')
print(f'FAQ总量: {len(faq["entities"])} 实体 / {len(faq["relationships"])} 关系')
