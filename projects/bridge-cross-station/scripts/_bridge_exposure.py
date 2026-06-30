# -*- coding: utf-8 -*-
"""补知识缺口：负面舆情/网络曝光/短视频危机"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('risk_graph.json', encoding='utf-8') as f:
    risk = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

# ====== 1. GSM站新增实体 ======
new_gsm = [
    {
        'id': 'GSM_CAT_EXPOSURE',
        'type': 'complaint_category',
        'name': '网络曝光/负面舆情投诉',
        'description': '客人在短视频（抖音/快手/小红书）或社交媒体发布酒店负面内容的投诉分类。含事件已发生但信息不对称阶段的预警管控、事件后品牌声誉修复'
    },
    {
        'id': 'SCENE_SHORTVIDEO_CRISIS',
        'type': 'gsm_scene',
        'name': '短视频曝光/网络舆情危机场景',
        'description': '客人拍摄/发布酒店负面短视频（食安/安全/服务类问题）的全流程应对。5分钟黄金响应期、提前阻断vs事后灭火'
    },
    {
        'id': 'GSM_LAW_DEFAMATION',
        'type': 'gsm_legal_framework',
        'name': '民法典第1024条名誉权/反网络侵权',
        'description': '民法典第1024-1030条名誉权保护。网络传播不实信息的侵权追溯。酒店有权要求平台删除失实内容。但公共舆论vs商业名誉的司法权衡'
    },
    {
        'id': 'GSM_INSIGHT_CRISIS_SPEED',
        'type': 'gsm_insight',
        'name': '短视频时代危机扩散速度远超传统投诉处理周期',
        'description': '传统GSM投诉流程：事件→记录→汇报→调查→处理→反馈（小时级）。短视频传播：拍摄→发布→推荐→曝光→热议（分钟级）。GSM流程必须嵌入"舆情防火墙"机制'
    },
    {
        'id': 'GSM_AUTH_EXPOSURE_MOD',
        'type': 'gsm_approval',
        'name': '负面曝光快反授权（MOD/值班总监立即决策，¥2,000内免审批）',
        'description': '舆情快反期间，MOD有权在¥2,000额度内现场决策（免单/补偿/升级房型/送券），不需等GM审批。事后24h内补报。核心逻辑：止损速度优先于流程完美'
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
    ('GSM_CAT_EXPOSURE', 'HAS_CATEGORY', 'GSM_CAT_ROOT'),
    ('GSM_CAT_EXPOSURE', 'RELATES_TO', 'GSM_CAT_SAFETY_SECURITY'),
    ('GSM_CAT_EXPOSURE', 'RELATES_TO', 'GSM_CAT_FOOD'),
    ('GSM_CAT_EXPOSURE', 'RELATES_TO', 'GSM_CAT_EFFICIENCY'),
    # 场景关联
    ('GSM_CAT_EXPOSURE', 'RELATES_TO', 'SCENE_SHORTVIDEO_CRISIS'),
    ('GSM_CAT_EXPOSURE', 'MUST_MASTER', 'ROLE_GSM'),
    ('GSM_CAT_EXPOSURE', 'MUST_MASTER', 'ROLE_SAFETY'),
    # 场景属性
    ('SCENE_SHORTVIDEO_CRISIS', 'SCENE_OF', 'GSM_LIABILITY_SAFETY_PRIVACY'),
    ('SCENE_SHORTVIDEO_CRISIS', 'SCENE_OF', 'GSM_LIABILITY_COMMUNICATION'),
    ('SCENE_SHORTVIDEO_CRISIS', 'SCENE_OF', 'GSM_LIABILITY_SERVICE_DETAIL'),
    ('SCENE_SHORTVIDEO_CRISIS', 'HAS_PHASE', 'GSM_DETECT'),
    ('SCENE_SHORTVIDEO_CRISIS', 'HAS_PHASE', 'GSM_DEAL'),
    ('SCENE_SHORTVIDEO_CRISIS', 'HAS_PHASE', 'GSM_FOLLOW'),
    # 法律
    ('SCENE_SHORTVIDEO_CRISIS', 'RELATES_TO', 'GSM_LAW_CONSUMER'),
    ('SCENE_SHORTVIDEO_CRISIS', 'RELATES_TO', 'GSM_LAW_DEFAMATION'),
    # 审批——舆情快反
    ('SCENE_SHORTVIDEO_CRISIS', 'REQUIRES_APPROVAL', 'GSM_AUTH_EXPOSURE_MOD'),
    ('SCENE_SHORTVIDEO_CRISIS', 'REQUIRES_APPROVAL', 'GSM_AUTH_GM'),
    # 红线
    ('SCENE_SHORTVIDEO_CRISIS', 'RELATES_TO', 'GSM_REDLINE'),
    # 关联现有投诉升级预案
    ('SCENE_SHORTVIDEO_CRISIS', 'RELATES_TO', 'R_CMPCMP-069'),
    # 洞察
    ('SCENE_SHORTVIDEO_CRISIS', 'SCENE_OF', 'GSM_INSIGHT_CRISIS_SPEED'),
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

# ====== 2. RISK站：负面舆情快反预案 ======
new_risk = [
    {
        'id': 'R_CMPCMP-100',
        'type': 'risk_entity',
        'name': '负面舆情/短视频曝光应急快反预案',
        'description': '客人拍摄并发布酒店负面短视频/社交媒体内容的全流程处置预案。覆盖食安事件/安全事件/服务投诉等各类负面内容的阻断、应对、修复'
    },
    {
        'id': 'R_EXPOSURE_5MIN_GOLDEN',
        'type': 'risk_entity',
        'name': '5分钟黄金阻断流程',
        'description': '发现客人可能有拍摄行为的第1-5分钟关键动作：(1)确认是否已被发到平台(2)若未发=当面阻断(免单+诚意+记录)(3)若已发=第一时间记录链接+截屏(4)启动快反授权(MOD¥2k内免审批)(5)不威胁不施压——建立信任'
    },
    {
        'id': 'R_EXPOSURE_TRACE',
        'type': 'risk_entity',
        'name': '已发布内容监测与平台申诉流程',
        'description': '确认视频已发布后的应对链：(1)抖音/小红书/快手平台搜索关键词(2)截屏+录屏取证(3)判断是否涉及重大食安/安全(4)是→法务+平台投诉通道(5)否→酒店官方评论区正面回应(6)监控48h扩散趋势'
    },
    {
        'id': 'R_EXPOSURE_ATTITUDE',
        'type': 'risk_entity',
        'name': '舆情应对态度四原则',
        'description': '(1)承认不辩解——"非常抱歉给您带来不好的体验"(2)私信不公开——私下沟通解决方案，不在评论区辩论(3)速度>完美——先停损再谈流程(4)不威胁不施压——威胁删帖可能触发反向放大'
    },
    {
        'id': 'R_EXPOSURE_WATCH',
        'type': 'risk_entity',
        'name': '48小时舆情监控窗口',
        'description': '事件发生后48h密切监控：每2小时搜索一次散播情况。应对阶梯：无扩散→静默处理；<1万播放→官方评论留言；1-10万→联系平台申诉/投诉删除；>10万→法务+公关公司介入'
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
    # 预案关联
    ('R_CMPCMP-100', 'RELATES_TO', 'R_CMPCMP-069'),
    ('R_CMPCMP-100', 'RELATES_TO', 'R_CMPCMP-072'),
    ('R_CMPCMP-100', 'REFERENCES', 'GSM_LAW_DEFAMATION'),
    # 预案→流程节点
    ('R_CMPCMP-100', 'HAS_SSOW', 'SCENE_SHORTVIDEO_CRISIS'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_EXPOSURE_5MIN_GOLDEN'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_EXPOSURE_TRACE'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_EXPOSURE_ATTITUDE'),
    ('R_CMPCMP-100', 'REFERENCES', 'R_EXPOSURE_WATCH'),
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

# ====== 3. QA站：舆情管理标准 ======
new_qa = [
    {
        'id': 'QA_BS_11300',
        'type': 'qa_standard',
        'name': '标准113.00 服务质量补救与舆情预防',
        'description': '服务质量补救标准。含负面事件即时阻断、网络曝光预防、客人拍摄行为的应对话术。核心原则：先解决情绪再解决问题，速度优先于完美'
    },
    {
        'id': 'QTC_EXPOSURE_01',
        'type': 'qa_check_item',
        'name': '突发事件中客人拍摄行为的应对检查',
        'description': '突发事件（异物/摔倒/纠纷）发生时，一线人员是否掌握"不阻止不威胁、主动沟通、前置解决"的三不原则。客人已掏手机拍摄：不在镜头前争吵辩论，转私密环境沟通'
    },
    {
        'id': 'QTC_EXPOSURE_02',
        'type': 'qa_check_item',
        'name': '舆情快反授权机制检查',
        'description': 'MOD/值班总监是否具备舆情事件¥2,000内免审批现场决策权。GSM是否知晓"先停损再走流程"原则'
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
    # QA_BS_11300在GSM已有引用，这里建立本站关系
    ('QA_BS_11300', 'belongs_to_section', 'QA_BS_100'),
    ('QA_BS_11300', 'check_standard', 'QTC_EXPOSURE_01'),
    ('QA_BS_11300', 'check_standard', 'QTC_EXPOSURE_02'),
    # 关联已有标准
    ('QA_BS_11300', 'RELATES_TO', 'QA_BS_42010'),
    ('QA_BS_11300', 'RELATES_TO', 'QA_BS_90200'),
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

# ====== 4. 跨站桥接 ======
bridge_risk = [
    ('GSM_CAT_EXPOSURE', 'HAS_CONTINGENCY', 'R_CMPCMP-100'),
    ('SCENE_SHORTVIDEO_CRISIS', 'HAS_CONTINGENCY', 'R_CMPCMP-100'),
]
bridge_risk_added = 0
for s, rt, t in bridge_risk:
    if (s, rt, t) in existing_risk_rels:
        print(f'[RISK跨站] 已存在: {s} --{rt}--> {t}')
    else:
        risk['relationships'].append({'source': s, 'type': rt, 'target': t})
        bridge_risk_added += 1

bridge_qa = [
    ('GSM_CAT_EXPOSURE', 'GOVERNED_BY', 'QA_BS_11300'),
    ('SCENE_SHORTVIDEO_CRISIS', 'ALIGNED_WITH', 'QA_BS_11300'),
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
