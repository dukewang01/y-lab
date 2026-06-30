# -*- coding: utf-8 -*-
"""补知识缺口：赔偿协议/免责回执/保密协议机制"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

# ====== 1. GSM站（法律框架补充一版）====== 
new_gsm = [
    {
        'id': 'GSM_DOC_SETTLEMENT',
        'type': 'gsm_legal_framework',
        'name': '和解协议/赔偿确认函机制',
        'description': '涉及现金/房券/免单等超过¥500的补偿方案，必须签署书面和解协议。内容：(1)确认事件经过(2)明确赔偿金额/形式(3)客人放弃后续追责权利(4)保密条款约定。注意事项：不写"承认过错"，写"基于客户体验的善意补偿"。不要签"免责"写"和解"——法律效力相同但话术更软'
    },
    {
        'id': 'GSM_INSIGHT_SETTLEMENT_PAPER',
        'type': 'gsm_insight',
        'name': '现金赔偿不给签字=二次风险，客人拿了钱转身还能再发抖音',
        'description': '没有签收的现金赔偿等于白赔。客人收钱后反悔→说"酒店只是给了补偿我没有接受道歉"→法律上不受影响。签署和解协议=双方都获得确定性。协议中加保密条款=堵住网络曝光的风险。核心规则：¥500以上赔偿必须签字确认'
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
    ('GSM_DOC_SETTLEMENT', 'APPLIES_TO', 'GSM_CAT_FOOD'),
    ('GSM_DOC_SETTLEMENT', 'APPLIES_TO', 'GSM_CAT_SAFETY_SECURITY'),
    ('GSM_DOC_SETTLEMENT', 'APPLIES_TO', 'GSM_CAT_STEP_INJURY'),
    ('GSM_DOC_SETTLEMENT', 'APPLIES_TO', 'GSM_CAT_EXPOSURE'),
    ('GSM_INSIGHT_SETTLEMENT_PAPER', 'SCENE_OF', 'GSM_DEAL'),
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

# ====== 2. RISK站：协议模板实体 ======
new_risk = [
    {
        'id': 'R_DOC_SETTLEMENT_MEDIUM',
        'type': 'risk_entity',
        'name': '和解协议模板-中等事件（食安异物/轻微受伤）',
        'description': '适用于中餐钉子/早餐滑倒等事件。核心条款：(1)双方确认事件经过(2)酒店基于客户体验提供￥XXX善意补偿(3)客人确认补偿方案合理并放弃后续追究(4)双方对事件内容保密，不得发布网络(5)本协议不构成酒店对过错的承认。签署方式：一式两份，酒店+客人各执一份，双签留影'
    },
    {
        'id': 'R_DOC_SETTLEMENT_MAJOR',
        'type': 'risk_entity',
        'name': '和解协议模板-重大事件（入院就医/退一赔十/万元级）',
        'description': '需法务起草。核心条款同中等模板+增加：(1)赔偿金额双方确认一次性了结(2)客人删除已发布的网络内容(3)约定不得以同一事由再起诉(4)违约责任。签署方式：双签+酒店章+见证人在场'
    },
    {
        'id': 'R_DOC_LIABILITY_NOTE',
        'type': 'risk_entity',
        'name': '小额补偿签收条（¥500以下免协议）',
        'description': '适用于饮品券/果盘/小礼品等¥500以下补偿。简单签收即可："本人确认收到酒店提供的_____，对本次住宿体验满意。客人签名____  日期____"。书面记录即可，不需完整协议。核心：任何补偿都要有签收，哪怕是一杯饮料'
    },
    {
        'id': 'R_DOC_CONFIDENTIAL',
        'type': 'risk_entity',
        'name': '保密/不扩散条款核心话术',
        'description': '和解协议中的保密条款：(1)"双方确认对本事件的处理方案及涉及内容共同保密，不得向第三方披露"(2)"甲方（客人）确认不在任何社交媒体/短视频平台发布相关视频或文字"(3)违约方承担赔偿法律责任。话术tip：不要跟客人说"你不能发抖音"，转成"我们互相尊重这件事就到此为止，您签了这份协议，我们彼此都放心"'
    },
    {
        'id': 'R_PROC_SETTLEMENT_SIGN',
        'type': 'risk_entity',
        'name': '赔偿签收标准流程',
        'description': 'STEP1:达成赔偿共识后→打印协议/签收单→要求客人在酒店内(非大堂)签署。STEP2:当面宣读核心条款。STEP3:双签+各执一份+拍照留存(要拍签的过程)+30s内归档到财务。STEP4:签署后不得撤回补偿物(现金/券/房)。关键红线:坚决避免客人说"我先看看"带着补偿走。证据链:协议+签收照片+客人表示满意的话音记录'
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

new_risk_rels = [
    ('R_DOC_SETTLEMENT_MEDIUM', 'REFERENCES', 'R_DOC_LIABILITY_NOTE'),
    ('R_DOC_SETTLEMENT_MEDIUM', 'REFERENCES', 'R_DOC_CONFIDENTIAL'),
    ('R_DOC_SETTLEMENT_MAJOR', 'REFERENCES', 'R_DOC_CONFIDENTIAL'),
    ('R_DOC_SETTLEMENT_MAJOR', 'REFERENCES', 'R_FOOD_FOREIGN_OBJECT'),
    ('R_DOC_LIABILITY_NOTE', 'REFERENCES', 'R_PROC_SETTLEMENT_SIGN'),
    ('R_PROC_SETTLEMENT_SIGN', 'HAS_SSOW', 'SCENE_SHORTVIDEO_CRISIS'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_DOC_SETTLEMENT_MEDIUM'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_DOC_CONFIDENTIAL'),
    ('R_CMPCMP-072', 'REFERENCES', 'R_DOC_SETTLEMENT_MEDIUM'),
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

# ====== 3. QA站：补充到补救标准 ======
new_qa_rels = [
    ('QA_BS_11300', 'check_standard', 'QTC_EXPOSURE_PAPER'),
]
new_qa = [
    {
        'id': 'QTC_EXPOSURE_PAPER',
        'type': 'qa_check_item',
        'name': '赔偿协议签收机制检查',
        'description': '涉及¥500以上现金/房券/补救性消费的补偿是否签署书面和解协议。协议中是否包含保密/不扩散条款。签收是否拍照归档。¥500以下是否至少有客人签收记录'
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
