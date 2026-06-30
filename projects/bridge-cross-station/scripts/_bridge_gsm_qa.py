# -*- coding: utf-8 -*-
"""GSM↔QA 跨站桥接
投诉分类/场景 → QA品牌标准（Section/标准）
每个投诉的背后 -> 哪个品牌标准没守住
"""
import json

with open('gsm_graph.json', encoding='utf-8') as f:
    gsm = json.load(f)
with open('qa_graph.json', encoding='utf-8') as f:
    qa = json.load(f)

bridge_count = 0

GSM_CATS = {e['id']: e for e in gsm['entities'] if e.get('type')=='complaint_category'}
GSM_SCENES = {e['id']: e for e in gsm['entities'] if e.get('type')=='gsm_scene'}
GSM_CASES = {e['id']: e for e in gsm['entities'] if e.get('type')=='risk_case'}

QA_STDS = {e['id']: e for e in qa['entities'] if e.get('type')=='qa_standard'}
QA_SECTIONS = {e['id']: e for e in qa['entities'] if e.get('type')=='qa_section'}

# =====================
# 桥1: 投诉分类 → QA Section（品类归属）
# =====================
cat_to_section = {
    'GSM_CAT_EFFICIENCY': 'QA_BS_200',       # 服务效率 → 宾客服务
    'GSM_CAT_ATTITUDE': 'QA_BS_100',          # 服务态度 → 品牌体验/好客精神
    'GSM_CAT_WATER': 'QA_BS_300',             # 水质水温 → 客房
    'GSM_CAT_CLEAN': 'QA_BS_300',             # 清洁卫生 → 客房
    'GSM_CAT_NOISE': 'QA_BS_300',             # 噪音 → 客房
    'GSM_CAT_ROOM_FAC': 'QA_BS_300',          # 设施设备 → 客房
    'GSM_CAT_AC_TEMP': 'QA_BS_700',           # 空调/温度 → 建筑运维
    'GSM_CAT_FACILITY': 'QA_BS_700',          # 设施设备 → 建筑运维
    'GSM_CAT_SAFETY_SECURITY': 'QA_BS_900',   # 安全隐私 → 安全安防
    'GSM_CAT_BILLING': 'QA_BS_800',           # 收费账单 → 品牌形象与销售
    'GSM_CAT_FOOD': 'QA_BS_400',              # 餐饮食品 → F&B
    'GSM_CAT_PARKING': 'QA_BS_700',           # 停车 → 建筑运维
    'GSM_CAT_LOST_ITEM': 'QA_BS_200',         # 遗留物品 → 宾客服务
    'GSM_CAT_HOUSEKEEPING': 'QA_BS_300',      # 清洁/客房 → 客房
}

for cid, section_id in cat_to_section.items():
    if cid not in GSM_CATS or section_id not in QA_SECTIONS:
        continue
    exists = any(r['source']==cid and r['target']==section_id for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': cid, 'target': section_id,
            'relation': 'RELATES_TO',
            'type': 'RELATES_TO',
            'properties': {'note': 'GSM投诉分类→QA品牌标准Section'}
        })
        bridge_count += 1

# =====================
# 桥2: 投诉场景 → QA Section（场景归属）
# =====================
scene_to_section = {
    'SCENE_POOL_FALL': 'QA_BS_500',       # 泳池 → 康体娱乐
    'SCENE_NOISE': 'QA_BS_300',           # 噪音 → 客房
    'SCENE_AC': 'QA_BS_700',              # 空调 → 建筑运维
    'SCENE_LOST': 'QA_BS_200',            # 失物 → 宾客服务(失物招领222)
    'SCENE_BILL': 'QA_BS_800',            # 账单 → 品牌形象
    'SCENE_ATTITUDE': 'QA_BS_100',        # 态度 → 品牌体验
    'SCENE_SAFETY': 'QA_BS_900',          # 安全 → 安全安防
    'SCENE_PARKING': 'QA_BS_700',         # 停车 → 建筑运维
}

for sid, section_id in scene_to_section.items():
    if sid not in GSM_SCENES:
        continue
    exists = any(r['source']==sid and r['target']==section_id for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': sid, 'target': section_id,
            'relation': 'BELONGS_TO_AREA',
            'type': 'BELONGS_TO_AREA',
            'properties': {'note': 'GSM投诉场景→QA Section区域'}
        })
        bridge_count += 1

# =====================
# 桥3: 投诉分类 → 具体QA标准（细粒度）
# =====================
cat_to_standard = {
    'GSM_CAT_EFFICIENCY': 'QA_BS_10600',        # 效率 → 品牌好客精神(含服务效率)
    'GSM_CAT_ATTITUDE': 'QA_BS_10800',          # 态度 → 团队成员标准(含态度)
    'GSM_CAT_WATER': 'QA_BS_30100',             # 水温 → 客房类型/设施
    'GSM_CAT_NOISE': 'QA_BS_251500',            # 噪音 → 隔音标准
    'GSM_CAT_SAFETY_SECURITY': 'QA_BS_90700',    # 安全 → 应急准备
    'GSM_CAT_BILLING': 'QA_BS_20400',           # 账单 → 前台(含收费)
    'GSM_CAT_FOOD': 'QA_BS_41200',              # 餐饮 → 餐饮卫生
    'GSM_CAT_LOST_ITEM': 'QA_BS_22200',         # 失物 → 失物招领
    'GSM_CAT_PARKING': 'QA_BS_70400',           # 停车 → 预防性维护
}

for cid, std_id in cat_to_standard.items():
    if cid not in GSM_CATS or std_id not in QA_STDS:
        continue
    exists = any(r['source']==cid and r['target']==std_id for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': cid, 'target': std_id,
            'relation': 'GOVERNED_BY',
            'type': 'GOVERNED_BY',
            'properties': {'note': 'GSM投诉分类→QA具体品牌标准'}
        })
        bridge_count += 1

# =====================
# 桥4: 投诉场景 → 具体QA标准
# =====================
scene_to_standard = {
    'SCENE_POOL_FALL': 'QA_BS_50100',     # 泳池摔倒 → 泳池标准
    'SCENE_LOST': 'QA_BS_22200',           # 失物 → 失物招领
    'SCENE_SAFETY': 'QA_BS_90400',         # 安全 → 安防系统
    'SCENE_PARKING': 'QA_BS_70400',        # 停车 → 预防性维护
    'SCENE_BILL': 'QA_BS_20400',           # 账单 → 前台
    'SCENE_AC': 'QA_BS_70900',             # 空调 → 酒店系统
}

for sid, std_id in scene_to_standard.items():
    if sid not in GSM_SCENES or std_id not in QA_STDS:
        continue
    exists = any(r['source']==sid and r['target']==std_id for r in qa['relationships'])
    if not exists:
        qa['relationships'].append({
            'source': sid, 'target': std_id,
            'relation': 'ALIGNED_WITH',
            'type': 'ALIGNED_WITH',
            'properties': {'note': 'GSM投诉场景→QA品牌标准'}
        })
        bridge_count += 1

# =====================
# 桥5: 投诉案例(名称中包含关键词) → QA Section
# =====================
case_to_section_map = {
    'QA_BS_200': ['前台','check-in','入住','服务','礼宾','行李','洗衣','门童','送餐','ird','客房服务'],
    'QA_BS_300': ['床','枕头','毛巾','马桶','浴室','洗浴','清洁','打扫','房间','噪音','吵','电视','空调','室温'],
    'QA_BS_400': ['餐','食','菜','酒','咖啡','早餐','餐饮','food','饮料','厨房'],
    'QA_BS_500': ['泳池','健身','康体','gym','pool'],
    'QA_BS_700': ['空调','电梯','停车','漏水','断电','维修','设施','设备','maintenance'],
    'QA_BS_800': ['账单','收费','账单','价格','会员','hh','积分','品牌','微信'],
    'QA_BS_900': ['安全','隐私','偷','盗','break','闯入','火灾','消防','火','报警','紧急'],
}

case_section_count = 0
for gsid, gs_e in GSM_CASES.items():
    gs_name = (gs_e.get('name_cn','') or gs_e.get('name','') or '').lower()
    if not gs_name or len(gs_name) < 3:
        continue
    matched_sec = None
    for sec_id, keywords in case_to_section_map.items():
        if any(kw.lower() in gs_name for kw in keywords):
            matched_sec = sec_id
            break
    if matched_sec:
        exists = any(r['source']==gsid and r['target']==matched_sec for r in qa['relationships'])
        if not exists:
            qa['relationships'].append({
                'source': gsid, 'target': matched_sec,
                'relation': 'EXEMPLIFIES',
                'type': 'EXEMPLIFIES',
                'properties': {'note': 'GSM投诉案例→体现QA品牌标准'}
            })
            case_section_count += 1

bridge_count += case_section_count

# =====================
# 桥6: GSM服务补救标准/流程 → QA 113.00服务补救标准
# =====================
qa_113 = next((e for e in qa['entities'] if e['id']=='QA_BS_11300'), None)
if qa_113:
    gsm_processes = [e for e in gsm['entities'] if e.get('type')=='gsm_process']
    for gp in gsm_processes:
        gp_name = (gp.get('name_cn','') or gp.get('name','') or gp['id']).lower()
        if '服务补救' in gp_name or 'service recovery' in gp_name or '补偿' in gp_name or '赔偿' in gp_name:
            exists = any(r['source']==gp['id'] and r['target']=='QA_BS_11300' for r in qa['relationships'])
            if not exists:
                qa['relationships'].append({
                    'source': gp['id'], 'target': 'QA_BS_11300',
                    'relation': 'GOVERNED_BY',
                    'type': 'GOVERNED_BY',
                    'properties': {'note': 'GSM流程→QA服务补救标准'}
                })
                bridge_count += 1
            break

# =====================
# 桥7: GSM成员培训 → QA 109.00培训标准
# =====================
gsm_training = [e for e in gsm['entities'] if e.get('type')=='gsm_training']
qa_109 = next((e for e in qa['entities'] if e['id']=='QA_BS_10900'), None)
if qa_109:
    for gt in gsm_training:
        gt_name = (gt.get('name_cn','') or gt.get('name','') or gt['id']).lower()
        exists = any(r['source']==gt['id'] and r['target']=='QA_BS_10900' for r in qa['relationships'])
        if not exists:
            qa['relationships'].append({
                'source': gt['id'], 'target': 'QA_BS_10900',
                'relation': 'ALIGNED_WITH',
                'type': 'ALIGNED_WITH',
                'properties': {'note': 'GSM培训→QA培训标准'}
            })
            bridge_count += 1

# =====================
# 桥8: 高频投诉分类 → GSM的相关流程对接到QA标准
# =====================
# GSM场景 → QA QTC检查项(FSAA相关已有补充)
# 补充：投诉场景→QA_FSAA标准
qa_fsaa_stds = [e for e in qa['entities'] if e.get('type')=='qa_standard' and 'QA_FSAA_' in e['id']]
scene_fsaa_map = {
    'SCENE_POOL_FALL': [s for s in qa_fsaa_stds if 'HYGIENE' in s['id'] or 'MAINT' in s['id']],
}

for sid, std_list in scene_fsaa_map.items():
    if sid not in GSM_SCENES:
        continue
    for std in std_list:
        exists = any(r['source']==sid and r['target']==std['id'] for r in qa['relationships'])
        if not exists:
            qa['relationships'].append({
                'source': sid, 'target': std['id'],
                'relation': 'RELEVANT_TO',
                'type': 'RELEVANT_TO',
                'properties': {'note': 'GSM投诉场景→QA食安标准'}
            })
            bridge_count += 1

# ====== 写回 ======
with open('qa_graph.json', 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)

print('GSM↔QA 桥接完成: +%d条跨站关系' % bridge_count)
print()
print('桥梁明细:')
print('  桥1: GSM投诉分类→QA Section (RELATES_TO)')
print('  桥2: GSM投诉场景→QA Section (BELONGS_TO_AREA)')
print('  桥3: GSM投诉分类→QA具体标准 (GOVERNED_BY)')
print('  桥4: GSM投诉场景→QA具体标准 (ALIGNED_WITH)')
print('  桥5: GSM投诉案例→QA Section (EXEMPLIFIES)')
print('  桥6: GSM服务补救→QA 113.00 (GOVERNED_BY)')
print('  桥7: GSM培训→QA 109.00 (ALIGNED_WITH)')
print('  桥8: GSM投诉场景→QA食安标准 (RELEVANT_TO)')
