# -*- coding: utf-8 -*-
"""补知识缺口：虚假宣传/标签争议/职业打假"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

def name_of(data, eid):
    for e in data['entities']:
        if e.get('id','') == eid:
            return e.get('name','?')
    return '?'

# ====== 1. 查RCASE_7471B虚假宣传儿童乐园案例 ======
print('=' * 60)
print('RCASE_7471B 虚假宣传儿童乐园投诉案例')
print('=' * 60)
for e in gsm['entities']:
    if e.get('id','') == 'RCASE_7471B':
        for k, v in e.items():
            print(f'  {k}: {v}')
        break
print()
print('关系：')
for r in gsm['relationships']:
    s = r.get('source','')
    t = r.get('target','')
    if s == 'RCASE_7471B' or t == 'RCASE_7471B':
        tn = name_of(gsm, t) if s == 'RCASE_7471B' else name_of(gsm, s)
        print(f'  {s} --{r.get("type")}--> {t}')
        if t != '?':
            pass

print()
print('—' * 60)

# ====== 2. GSM站新增实体：标签/广告争议 ======
new_gsm = [
    {
        'id': 'GSM_CAT_LABEL_FALSE',
        'type': 'complaint_category',
        'name': '标签/虚假宣传投诉',
        'description': '产品标签描述与实际不符、虚假宣传、广告误导等投诉分类。涉及消法退一赔三、广告法、职业打假等场景'
    },
    {
        'id': 'SCENE_LABEL_DISPUTE',
        'type': 'gsm_scene',
        'name': '食品标签/虚假宣传争议场景',
        'description': '客人质疑产品标签描述（如"手工"、原产地、成分）与实际情况不符，要求退一赔三的职业投诉场景'
    },
    {
        'id': 'GSM_LAW_AD',
        'type': 'gsm_legal_framework',
        'name': '广告法/反不正当竞争法',
        'description': '广告法第28条虚假广告认定标准。反不正当竞争法第8条禁止虚假宣传。最高法职业打假人不赔惩罚性赔偿的司法解释(2022)'
    },
    {
        'id': 'GSM_LAW_FOOD_LABEL',
        'type': 'gsm_legal_framework',
        'name': '食品标签管理规定/GB 7718',
        'description': 'GB 7718-2011 预包装食品标签通则。食品名称必须反映食品真实属性。手工/传统/古法等描述词需有依据'
    },
    {
        'id': 'GSM_AUTH_LABEL_GM',
        'type': 'gsm_approval',
        'name': '标签/虚假宣传赔偿审批（法务+GM联合）',
        'description': '涉及虚假宣传指控的赔偿方案，须法务审核+GM审批，不单独由值班经理决定'
    },
    {
        'id': 'GSM_INSIGHT_PRO_LABEL',
        'type': 'gsm_insight',
        'name': '标签类投诉案例少（但为高风险职业打假区域）',
        'description': '食品标签虚假宣传投诉量很少，但单案赔偿额极高，重点防御领域'
    },
    {
        'id': 'GSM_AUTH_LABEL_TIER1',
        'type': 'gsm_approval',
        'name': '标签投诉一级协商授权（法务审批，¥5,000内）',
        'description': '标签类投诉小额补偿权限：退剩余货品+¥5,000以内补偿，须法务确认不构成"认赔"证据'
    },
    {
        'id': 'GSM_AUTH_LABEL_TIER2',
        'type': 'gsm_approval',
        'name': '标签投诉二级协商授权（GM+法务联合，¥20,000内）',
        'description': '标签类投诉中等金额方案：退一赔一~退一赔二但不承认虚假，需法务起草书面条款'
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

# GSM关系
new_gsm_rels = [
    # 分类归属
    ('GSM_CAT_LABEL_FALSE', 'HAS_CATEGORY', 'GSM_CAT_ROOT'),
    ('GSM_CAT_LABEL_FALSE', 'RELATES_TO', 'GSM_CAT_BILLING'),
    ('GSM_CAT_LABEL_FALSE', 'RELATES_TO', 'GSM_CAT_FOOD'),
    # 场景关联
    ('GSM_CAT_LABEL_FALSE', 'RELATES_TO', 'SCENE_LABEL_DISPUTE'),
    ('GSM_CAT_LABEL_FALSE', 'MUST_MASTER', 'ROLE_GSM'),
    ('GSM_CAT_LABEL_FALSE', 'MUST_MASTER', 'ROLE_FOOD'),
    # 场景属性
    ('SCENE_LABEL_DISPUTE', 'SCENE_OF', 'GSM_LIABILITY_BILLING'),
    ('SCENE_LABEL_DISPUTE', 'SCENE_OF', 'GSM_LIABILITY_PRODUCT_QUALITY'),
    ('SCENE_LABEL_DISPUTE', 'HAS_PHASE', 'GSM_DETECT'),
    ('SCENE_LABEL_DISPUTE', 'HAS_PHASE', 'GSM_DEAL'),
    ('SCENE_LABEL_DISPUTE', 'HAS_PHASE', 'GSM_FOLLOW'),
    # 法律框架
    ('SCENE_LABEL_DISPUTE', 'RELATES_TO', 'GSM_LAW_CONSUMER'),
    ('SCENE_LABEL_DISPUTE', 'RELATES_TO', 'GSM_LAW_AD'),
    ('SCENE_LABEL_DISPUTE', 'RELATES_TO', 'GSM_LAW_FOOD_LABEL'),
    # 审批层级
    ('SCENE_LABEL_DISPUTE', 'REQUIRES_APPROVAL', 'GSM_AUTH_LABEL_GM'),
    ('SCENE_LABEL_DISPUTE', 'REQUIRES_APPROVAL', 'GSM_AUTH_LABEL_TIER1'),
    ('SCENE_LABEL_DISPUTE', 'REQUIRES_APPROVAL', 'GSM_AUTH_LABEL_TIER2'),
    # 红线
    ('SCENE_LABEL_DISPUTE', 'RELATES_TO', 'GSM_REDLINE'),
    # 标签→案例
    ('GSM_CAT_LABEL_FALSE', 'HAS_EXAMPLE', 'RCASE_7471B'),
    # 洞察
    ('SCENE_LABEL_DISPUTE', 'SCENE_OF', 'GSM_INSIGHT_PRO_LABEL'),
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

# ====== 3. RISK站：打假/标签争议预案 ======
new_risk = [
    {
        'id': 'R_CMPCMP-099',
        'type': 'risk_entity',
        'name': '食品标签/虚假宣传争议专项应急预案',
        'description': '客人投诉产品标签描述（手工/原产地/成分等）虚假宣传，要求消法退一赔三的专项处理流程。含职业打假人识别、法务介入、谈判底线机制'
    },
    {
        'id': 'R_LABEL_DISPUTE_DISCOVER',
        'type': 'risk_entity',
        'name': '标签投诉发现与初步评估',
        'description': '接诉后判断：是否涉及标签/宣传/广告问题。初步证据收集中：保留包装实物+拍照+录音。判断投诉人是否为职业打假（100盒批量购买）'
    },
    {
        'id': 'R_LABEL_DISPUTE_NEGOTIATE',
        'type': 'risk_entity',
        'name': '标签投诉谈判三阶策略',
        'description': 'Tier1:退剩余货品+小补偿(¥5k内)不谈虚假。Tier2:退一赔二不谈虚假+法务起草协议免责声明。Tier3:走法律渠道，法务接手不再前台沟通'
    },
    {
        'id': 'R_LABEL_DISPUTE_LAW',
        'type': 'risk_entity',
        'name': '标签投诉法律防御要点',
        'description': '1.工厂手工也是手工≠虚假。2.职业打假2022最高法司法解释不支持惩罚性赔偿。3.标签瑕疵不等于虚假宣传(食品安全法第148条)。4.消法55条退一赔三须主观故意'
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
    # 预案→关联
    ('R_CMPCMP-099', 'RELATES_TO', 'R_CMPCMP-076'),
    ('R_CMPCMP-099', 'RELATES_TO', 'R_CMPCMP-008'),
    ('R_CMPCMP-099', 'REFERENCES', 'GSM_LAW_CONSUMER'),
    ('R_CMPCMP-099', 'REFERENCES', 'GSM_LAW_AD'),
    ('R_CMPCMP-099', 'REFERENCES', 'GSM_LAW_FOOD_LABEL'),
    # 预案→流程节点
    ('R_CMPCMP-099', 'HAS_SSOW', 'SCENE_LABEL_DISPUTE'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_LABEL_DISPUTE_DISCOVER'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_LABEL_DISPUTE_NEGOTIATE'),
    ('R_CMPCMP-099', 'REFERENCES', 'R_LABEL_DISPUTE_LAW'),
    # 关联案例
    ('R_CMPCMP-099', 'HAS_CASE', 'RCASE_7471B'),
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

# ====== 4. QA站：标签合规标准 ======
new_qa = [
    {
        'id': 'QA_BS_42009',
        'type': 'qa_standard',
        'name': '标准420.09 食品宣传/标签合规',
        'description': '酒店销售食品（含礼盒/外卖/自助餐）的宣传用语和标签合规要求。手工/传统/古法/原产地/天然等描述词须有依据。标签须符合GB 7718。不得暗示与实际情况不符的产地/生产者/工艺'
    },
    {
        'id': 'QTC_LABEL_01',
        'type': 'qa_check_item',
        'name': '食品宣传用语合规检查',
        'description': '食品销售文案中"手工"、"传统"、"古法"、"农家"、"天然"等描述词，核实是否有生产依据或供应商证明。严禁未核实使用'
    },
    {
        'id': 'QTC_LABEL_02',
        'type': 'qa_check_item',
        'name': '食品包装标签合规检查',
        'description': '预包装食品标签须标注：生产者/地址/配料表/净含量/生产日期/保质期/执行标准/生产许可证编号。符合GB 7718'
    },
    {
        'id': 'QTC_LABEL_03',
        'type': 'qa_check_item',
        'name': '食品供应商宣传审核记录',
        'description': 'OEM/代工食品的宣传用语、包装文案须经酒店法务或品牌部门审核，留存审核记录'
    },
    {
        'id': 'QTC_LABEL_04',
        'type': 'qa_check_item',
        'name': '酒店自制食品宣传真实性检查',
        'description': '酒店厨房自产食品的宣传（如"大厨手工"）与实际生产情况和人员配置一致'
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

# QA关系
new_qa_rels = [
    ('QA_BS_42009', 'belongs_to_section', 'QA_BS_400'),
    ('QA_BS_42009', 'check_standard', 'QTC_LABEL_01'),
    ('QA_BS_42009', 'check_standard', 'QTC_LABEL_02'),
    ('QA_BS_42009', 'check_standard', 'QTC_LABEL_03'),
    ('QA_BS_42009', 'check_standard', 'QTC_LABEL_04'),
    ('QA_BS_42009', 'RELATES_TO', 'QA_BS_800'),
    ('QA_BS_42009', 'RELATES_TO', 'QA_BS_80200'),
    ('QA_BS_42009', 'RELATES_TO', 'QA_BS_200'),
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

# ====== 5. 跨站桥接 ======
bridge_risk = [
    ('GSM_CAT_LABEL_FALSE', 'HAS_CONTINGENCY', 'R_CMPCMP-099'),
    ('SCENE_LABEL_DISPUTE', 'HAS_CONTINGENCY', 'R_CMPCMP-099'),
    ('GSM_CAT_LABEL_FALSE', 'RELATES_TO', 'R_CMPCMP-076'),
]
bridge_risk_added = 0
for s, rt, t in bridge_risk:
    if (s, rt, t) in existing_risk_rels:
        print(f'[RISK跨站] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        bridge_risk_added += 1

bridge_qa = [
    ('GSM_CAT_LABEL_FALSE', 'GOVERNED_BY', 'QA_BS_42009'),
    ('GSM_CAT_LABEL_FALSE', 'GOVERNED_BY', 'QA_BS_80200'),
    ('SCENE_LABEL_DISPUTE', 'ALIGNED_WITH', 'QA_BS_42009'),
    ('GSM_CAT_LABEL_FALSE', 'RELATES_TO', 'QA_BS_800'),
]
bridge_qa_added = 0
for s, rt, t in bridge_qa:
    if (s, rt, t) in existing_qa_rels:
        print(f'[QA跨站] 已存在: {s} --{rt}--> {t}')
    else:
        qa['relationships'].append({'source': s, 'type': rt, 'target': t})
        bridge_qa_added += 1

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
print(f'  跨站桥接: RISK+{bridge_risk_added}, QA+{bridge_qa_added}')
