"""FAQ新增：体液/血液/呕吐物处理规范（基于官方SSOW 2.6）"""
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
    'label': '体液/血液/呕吐物处理安全工作系统（SSOW 2.6）',
    'description': (
        '【体液/血液/呕吐物处理安全工作系统 — 基于希尔顿SSOW 2.6】\n\n'
        '一、作业前准备\n'
        '  · 限制进入该区域，放置"清洁中"警示牌\n'
        '  · 穿戴PPE：一次性手套 + 塑料围裙 + 口罩\n'
        '  · 确认体液溢出工具包位置（＿＿＿＿＿＿＿）\n\n'
        '二、硬表面（地砖/台面/墙面）\n'
        '  1. 用纸巾/吸水材料覆盖液体和有机物\n'
        '  2. 将废物装入双层医疗废物袋，立即丢弃\n'
        '  3. 使用杀菌消毒剂覆盖剩余区域，遵守标签标注的接触时间（通常5-10分钟）\n'
        '  4. 用一次性毛巾擦拭消毒区域，放入双层袋丢弃\n'
        '  5. 用热水+消毒剂清洗该区域，自然风干\n'
        '  6. 呕吐物周围2米范围内的所有食物→立即丢弃\n'
        '  7. 彻底消毒门把手/水龙头/开关等附近硬表面\n\n'
        '三、软表面（地毯/布艺/床品）\n'
        '  1. 被污染的床单→按传染性床单处理（使用可溶性床单袋）\n'
        '  2. 地毯→按硬表面处理程序操作（吸水→消毒→擦拭→风干）\n'
        '  3. 室内装潢/软装饰→按硬表面处理，污染严重则丢弃\n'
        '  4. 严重污染的织物→可考虑蒸汽清洗\n'
        '  5. 衣物→立即高温清洗并熨烫，或双层袋装丢弃\n\n'
        '四、PPE摘除与手部卫生\n'
        '  1. 摘手套→摘围裙→摘口罩（顺序不能反）\n'
        '  2. 七步洗手法：皂液+流动水≥20秒\n\n'
        '【红线】\n'
        '  · 严禁裸手接触任何体液/血液/呕吐物\n'
        '  · 严禁将污染废物丢入普通垃圾桶（必须双层医疗废物袋）\n'
        '  · 呕吐物2米范围内食物→全部丢弃，不可筛选\n\n'
        '【风险】传染性物质污染（HIV/乙肝/诺如/其他病原体）\n\n'
        '【PPE】一次性手套 + 塑料围裙 + 口罩\n\n'
        '【培训要求】每年接受培训\n\n'
        '【责任部门】客房清洁部 / 健身俱乐部·Spa / 值班经理\n\n'
        '【工具包位置】＿＿＿＿＿＿＿（由HOD确定并放置）'
    ),
    'category': 'ssow',
    'tags': ['体液', '血液', '呕吐物', '传染性', '医疗废物', 'SSOW', '二级SSOW', 'PA', '客房', '健身'],
    'department': '客房清洁部/健身俱乐部/值班经理'
}
faq['entities'].append(e1)
faq['relationships'] = faq.get('relationships', [])
for t in set(e1['tags']):
    faq['relationships'].append({'source': e1['id'], 'target': t, 'relation': 'tagged_as'})

tmp = os.path.join(BASE, 'faq_graph.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(faq, f, ensure_ascii=False, indent=2)
shutil.move(tmp, os.path.join(BASE, 'faq_graph.json'))

print(f'新增: {e1["id"]}')
print(f'FAQ总量: {len(faq["entities"])} 实体 / {len(faq["relationships"])} 关系')

# 归档原文件
import datetime, shutil
src = r'C:\Users\Duke Wang\.openclaw\media\inbound\2.6_ä½_æ_²ç_å_ç_å_å_å_ä½_ç³_ç---c9ab34bb-a452-45c8-8975-3e1eafc68c69.pdf'
import os.path as osp
fname = os.path.basename(src)
dst_dir = osp.join(BASE, '..', 'media', 'archived')
dst = osp.join(dst_dir, fname)
if osp.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)
    os.remove(src)
    print(f'归档: {fname}')
