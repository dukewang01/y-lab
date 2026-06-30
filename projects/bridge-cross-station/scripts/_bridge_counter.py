# -*- coding: utf-8 -*-
"""补知识缺口：反向报警/敲诈勒索维权/酒店反制机制"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

# ====== RISK站：反向维权+敲诈识别+报警路线 ======
new_risk = [
    {
        'id': 'R_COUNTER_EXTORTION',
        'type': 'risk_entity',
        'name': '敲诈勒索/恶意维权报警与反制流程',
        'description': '酒店自查确认无过错后，针对职业打假/恶意维权/敲诈勒索客人的反向报警路径。公安立案标准(¥2,000-¥5,000)、证据链构建、话术应对、法务介入触发点'
    },
    {
        'id': 'R_COUNTER_SELF_CHECK',
        'type': 'risk_entity',
        'name': '自查自证无过错流程',
        'description': '收到打假/投诉后，先自查自证：确认标签/宣发/产品是否确实有瑕疵(内部法务+QA联合审查)。若确认无实质瑕疵：(1)固定证据（包装/生产记录/供方资质）(2)书面记录投诉内容(3)法务函告客人：酒店无过错→不接受索赔(4)客人若进一步威胁（曝光/工商/媒体）→启动敲诈勒索报案路径'
    },
    {
        'id': 'R_COUNTER_EVIDENCE_CHAIN',
        'type': 'risk_entity',
        'name': '敲诈勒索证据链构建标准',
        'description': '刑事立案核心证据：(1)客人的索赔要求记录(文字/录音最好)(2)酒店无过错的证明材料(3)客人的威胁言辞(截图/录音——"你不赔我我就发抖音/我就去工商投诉")(4)索赔金额超出合理范围(5)客人批量购买/专业打假模式(同一批次/同一产品/同一话术)(6)通话录音/微信截屏连续完整。提示：法律规定录音不告知对方只要不公开仍可作证据(不违反公序良俗前提下)'
    },
    {
        'id': 'R_COUNTER_EXTORTION_THRESHOLD',
        'type': 'risk_entity',
        'name': '敲诈勒索立案门槛与报案路径',
        'description': '刑法第274条敲诈勒索罪：¥2,000-¥5,000(各地区有差异)=数额较大→刑事立案。立案条件：(1)存在威胁要挟(2)非法索取财物(3)酒店无实际过错。报案地点：酒店属地派出所（园区湖东派出所/或案发地派出所）。报案材料：投诉记录+证据链+自查报告+索赔要求文字记录。报警话术：明确说"对方以网络曝光为由要挟索赔，金额超出合理范围"。关键：不要等客人去举报了再报警——在谈判阶段客人的威胁言论本身就是证据'
    },
    {
        'id': 'R_COUNTER_PUBLIC_PRESSURE',
        'type': 'risk_entity',
        'name': '职业打假反向威慑话术',
        'description': '在确认无过错的前提下，与职业打假人谈判时的话术：(1)"我们已经自查确认产品合规，法务已介入"(2)"您指出的问题我们核实没有超标，如果您坚持，我们只能走法律渠道"(3)"提醒您，2022年最高法新规对食品标签领域职业打假的惩罚性赔偿有新的限制"(4)不说"你敲诈"而是说"我们觉得这件事可能需要法律来判断"(5)核心目的：让打假人知道你不好欺负，而不是让他觉得随便就能榨到钱'
    },
    {
        'id': 'R_COUNTER_CYBER_BLACKMAIL',
        'type': 'risk_entity',
        'name': '网络曝光式敲诈应对路线',
        'description': '客人说"不赔我就发抖音"。应对路线：STEP1:稳住——"这件事我一定给你一个满意的答复，不用发网上，我们私下解决"。STEP2:录音保留威胁言论。STEP3:评估酒店有无实质过错→有过错→谈和解(签保密协议)。无过错→告诉客人"酒店确认无过错，如果您坚持要发，我们保留追究法律责任的权利"——然后反手报警。STEP4:报警后向平台发函附报警回执要求下架。核心：不要因为害怕曝光就不报警——报警回执是让平台下架的最有力材料'
    },
    {
        'id': 'R_COUNTER_PRO_TACTICS',
        'type': 'risk_entity',
        'name': '职业打假人识别特征与专项策略',
        'description': '识别特征：(1)批量购买同一产品(2)购买后立即投诉(3)不接受退货只要求赔钱(4)熟悉消法/食安法条款(5)同时向多平台投诉(6)不接受实物补偿。专项策略：(1)只退不赔+法务函(2)要求对方提供身份信息+购买凭证(3)警惕"套路打假"——有些先买后藏进异物的，所以要查监控验证货品交付时的完整性(4)赔偿谈判只谈"退换"不谈"赔钱"(5)必要时反诉——诬告有成本'
    },
]

existing_risk_ids = {e.get('id') for e in risk['entities']}
risk_added = 0
for ne in new_risk:
    if ne['id'] in existing_risk_ids:
        print(f'[RISK] 已存在: {ne["id"]}')
    else:
        risk['entities'].append(ne)
        risk_added += 1
        print(f'[RISK] 新增: {ne["id"]} - {ne["name"]}')

# RISK关系
new_risk_rels = [
    # 核心预案→补充节点
    ('R_CMPCMP-099', 'REFERENCES', 'R_COUNTER_SELF_CHECK'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_COUNTER_EVIDENCE_CHAIN'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_COUNTER_EXTORTION_THRESHOLD'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_COUNTER_PUBLIC_PRESSURE'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_COUNTER_PRO_TACTICS'),
    # 跨领域关联
    ('R_COUNTER_CYBER_BLACKMAIL', 'REFERENCES', 'R_COUNTER_EVIDENCE_CHAIN'),
    ('R_COUNTER_CYBER_BLACKMAIL', 'REFERENCES', 'R_COUNTER_EXTORTION_THRESHOLD'),
    ('R_COUNTER_EXTORTION', 'REFERENCES', 'R_COUNTER_SELF_CHECK'),
    ('R_COUNTER_EXTORTION', 'REFERENCES', 'R_COUNTER_EVIDENCE_CHAIN'),
    ('R_COUNTER_EXTORTION', 'REFERENCES', 'R_COUNTER_EXTORTION_THRESHOLD'),
    # 关联现有法律框架
    ('R_COUNTER_PUBLIC_PRESSURE', 'REFERENCES', 'GSM_LAW_FOOD_LABEL'),
    ('R_COUNTER_EXTORTION_THRESHOLD', 'REFERENCES', 'GSM_LAW_CIVIL'),
    # 关联现有预案
    ('R_CMPCMP-100', 'REFERENCES', 'R_COUNTER_CYBER_BLACKMAIL'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_LABEL_DISPUTE_DISCOVER'),
]

existing_risk_rels = set()
for r in risk['relationships']:
    existing_risk_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
risk_rel_added = 0
for s, rt, t in new_risk_rels:
    if (s, rt, t) in existing_risk_rels:
        print(f'[RISK关系] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        risk_rel_added += 1
print(f'  RISK += {risk_added}实体, {risk_rel_added}关系')

# ====== GSM站：补充打假反向相关的法律和洞察 ======
new_gsm = [
    {
        'id': 'GSM_LAW_CRIMINAL_274',
        'type': 'gsm_legal_framework',
        'name': '刑法第274条敲诈勒索罪',
        'description': '刑法第274条：敲诈勒索公私财物，数额较大(¥2,000-¥5,000)或多次敲诈，处三年以下有期徒刑、拘役或管制，并处或单处罚金。数额巨大(¥5万-¥10万)→三到十年。数额特别巨大(¥5万-¥50万以上)→十年以上。酒店场景适用：以网络曝光/媒体举报/工商投诉为要挟，索取超额赔偿的行为。关键：敲诈勒索不以"是否实有过错"为前提——即使酒店确有瑕疵，以曝光威胁要挟超额赔偿仍可能构成敲诈勒索'
    },
    {
        'id': 'GSM_INSIGHT_COUNTER_POLICE',
        'type': 'gsm_insight',
        'name': '酒店主动报警比被动应诉更有利',
        'description': '酒店主动报警vs被敲诈者报警的本质区别。(1)主动报警=酒店是受害者→舆论站在酒店这边(2)被动报警=等对方去12315/媒体→酒店被定义成"欺负消费者的一方"(3)主动权在谁手里很重要。核心判断维度：酒店自查有无过错——无过错→直接硬刚不赔/反向报警。有过错→签和解/保密协议→不报警。关键红线：不要无过错也出钱——出钱=在舆论上认错'
    },
    {
        'id': 'GSM_INSIGHT_COUNTER_2022_JUDGE',
        'type': 'gsm_insight',
        'name': '2022最高法司法解释限制食品标签领域职业打假索赔',
        'description': '2022年最高法《关于审理食品药品惩罚性赔偿纠纷案件适用法律若干问题的解释》（征求意见稿）：食品标签、说明书存在瑕疵但不影响食品安全且不会对消费者造成误导的，不支持惩罚性赔偿。核心：标签/宣传的"形式瑕疵"≠不符合食品安全标准。职业打假人大量购买同一商品然后逐一索赔的模式，法院对此类"以牟利为目的"的索赔限制日益严格。酒店法务应掌握此条'
    },
]

existing_gsm_ids = {e.get('id') for e in gsm['entities']}
gsm_added = 0
for ne in new_gsm:
    if ne['id'] in existing_gsm_ids:
        print(f'[GSM] 已存在: {ne["id"]}')
    else:
        gsm['entities'].append(ne)
        gsm_added += 1
        print(f'[GSM] 新增: {ne["id"]} - {ne["name"]}')

new_gsm_rels = [
    ('GSM_LAW_CRIMINAL_274', 'APPLIES_TO', 'GSM_CAT_LABEL_FALSE'),
    ('GSM_LAW_CRIMINAL_274', 'APPLIES_TO', 'GSM_CAT_EXPOSURE'),
    ('GSM_INSIGHT_COUNTER_POLICE', 'SCENE_OF', 'GSM_DEAL'),
    ('GSM_INSIGHT_COUNTER_2022_JUDGE', 'SCENE_OF', 'GSM_LAW_FOOD_LABEL'),
]
existing_gsm_rels = set()
for r in gsm['relationships']:
    existing_gsm_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
gsm_rel_added = 0
for s, rt, t in new_gsm_rels:
    if (s, rt, t) in existing_gsm_rels:
        print(f'[GSM关系] 已存在: {s} --{rt}--> {t}')
    else:
        gsm['relationships'].append({'source': s, 'type': rt, 'target': t})
        gsm_rel_added += 1
print(f'  GSM += {gsm_added}实体, {gsm_rel_added}关系')

# ====== QA站：增加反制检查项 ======
new_qa = [
    {
        'id': 'QTC_COUNTER_01',
        'type': 'qa_check_item',
        'name': '打假/恶意投诉反向应对能力检查',
        'description': 'GSM/管理层是否掌握职业打假识别特征(批量购买+即投即诉+只索赔不退)。酒店是否已建立自查无过错后的反向报警路径。法务是否掌握2022最高法新规对打假索赔限制的最新条款'
    },
]
existing_qa_ids = {e.get('id') for e in qa['entities']}
qa_added = 0
for ne in new_qa:
    if ne['id'] in existing_qa_ids:
        print(f'[QA] 已存在: {ne["id"]}')
    else:
        qa['entities'].append(ne)
        qa_added += 1
        print(f'[QA] 新增: {ne["id"]} - {ne["name"]}')

new_qa_rels = [
    ('QA_BS_11300', 'check_standard', 'QTC_COUNTER_01'),
]
existing_qa_rels = set()
for r in qa['relationships']:
    existing_qa_rels.add((r.get('source',''), r.get('type') or r.get('relation',''), r.get('target','')))
qa_rel_added = 0
for s, rt, t in new_qa_rels:
    if (s, rt, t) in existing_qa_rels:
        print(f'[QA关系] 已存在: {s} --{rt}--> {t}')
    else:
        qa['relationships'].append({'source': s, 'type': rt, 'target': t})
        qa_rel_added += 1
print(f'  QA += {qa_added}实体, {qa_rel_added}关系')

# ====== 写入 ======
with open('gsm_graph.json', 'w', encoding='utf-8') as f:
    json.dump(gsm, f, ensure_ascii=False, indent=2)
with open('risk_graph.json', 'w', encoding='utf-8') as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)
with open('qa_graph.json', 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)

print()
print('=' * 60)
print('写入完成！')
print(f'  GSM站: +{gsm_added}实体, +{gsm_rel_added}关系')
print(f'  RISK站: +{risk_added}实体, +{risk_rel_added}关系')
print(f'  QA站: +{qa_added}实体, +{qa_rel_added}关系')
