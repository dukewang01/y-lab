"""FAQ新增：风机盘管装置阀门更换安全工作系统（SSOW 3.16）"""
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
    'label': '风机盘管装置阀门更换安全工作系统（SSOW 3.16）',
    'description': (
        '【风机盘管装置阀门更换安全工作系统 — 基于希尔顿SSOW 3.16】\n\n'
        '仅年满18周岁、接受过培训的团队成员可执行。每年培训。\n\n'
        '一、作业前\n'
        '  · 检查所有设备状况\n'
        '  · **将房间停用**（客人在房→协调换房或等退房）\n'
        '  · 在门上挂好"作业中"标牌\n'
        '  · **为风机盘管装置断电**\n'
        '  · 清理工作区域，将架梯安全放置在适合作业位置\n'
        '  · 为流量和回流管道断水\n'
        '  · 在更换阀下方放置托盘，用于盛放多余的水\n\n'
        '二、佩戴PPE\n'
        '  · 安全鞋\n'
        '  · 手套\n'
        '  · 护目镜\n\n'
        '三、执行\n'
        '  · 从阀门上取下激活器，放在一边\n'
        '  · 将多余的水排入托盘\n'
        '  · **缓慢**松开阀门连接——避免热水爆裂喷溅\n\n'
        '四、安装验证\n'
        '  · 更换阀门后，**缓慢**打开流量阀，检查有无泄漏\n'
        '  · 无泄漏→完全打开流量阀+回流阀，再检漏\n'
        '  · 安全取出托盘并清空\n'
        '  · 维修完成→打开风机盘管装置，检查加热和冷却温度是否正常\n\n'
        '五、作业后\n'
        '  · 清洁和整理工作场所\n'
        '  · 移除标牌\n'
        '  · 向前台接待处和客房清洁部报告任务已完成\n\n'
        '【红线】\n'
        '  · 严禁未断电断水即拆卸阀门\n'
        '  · 严禁未放置接水托盘（水漫天花/客赔）\n'
        '  · 严禁快速开启阀门（水锤爆管/烫伤）\n'
        '  · 严禁作业后忘记通知前台/客房部（客人回房发现拆了一半→投诉）\n\n'
        '【风险】高处坠落（架梯作业）、设备坠落（阀门掉落）、热水爆裂/烫伤（≤60°C供暖水）、水流/滑倒\n\n'
        '【PPE】安全鞋 + 手套 + 护目镜\n'
        '【工具】适高架梯 + 安全标牌 + 维修工具钥匙 + 头灯 + 托盘 + 温度计\n\n'
        '【培训要求】每年一次\n\n'
        '【责任部门】工程部'
    ),
    'category': 'ssow',
    'tags': ['风机盘管', 'FCU', '阀门更换', '空调', '客房维修', '工程部', 'SSOW', '三级SSOW'],
    'department': '工程部',
    'ppe_list': ['安全鞋', '手套', '护目镜'],
    'hazards': ['高处坠落  架梯作业', '设备坠落  阀门掉落', '热水爆裂/烫伤  ≤60°C供暖水', '水流/滑倒'],
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

print(f'新增FCU阀门更换FAQ: {e1["id"]}')
print(f'FAQ总量: {len(faq["entities"])} 实体 / {len(faq["relationships"])} 关系')
