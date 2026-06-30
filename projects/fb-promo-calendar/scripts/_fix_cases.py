#!/usr/bin/env python3
"""
Fix missing relationships for cases that were imported without category links.
Also re-import any cases that don't exist yet.
"""
import json

GRAPH_PATH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\gsm_graph.json'

# Corrected category mappings
CASE_CATEGORY_MAP = {
    "RCASE_8454": "设施设备投诉",    # 浴室大理石挡板脱落
    "RCASE_8453": "安全隐私投诉",    # 工程部仓管员受伤就医
    "RCASE_8452": "设施设备投诉",    # 房间断电
    "RCASE_8451": "停车投诉",       # 车库剐蹭消防喷淋头
    "RCASE_8450": "设施设备投诉",    # 花洒断裂砸脚
    "RCASE_8449": "安全隐私投诉",    # 客人浴室滑倒摔伤
    "RCASE_8448": "设施设备投诉",    # 房门反锁打不开
    "RCASE_8447": "设施设备投诉",    # 天花墙皮脱落
    "RCASE_8446": "设施设备投诉",    # 手指被水龙头刮破
    "RCASE_8445": "设施设备投诉",    # 房间灯自动亮5次-RCU故障
    "RCASE_8444": "设施设备投诉",    # 小茶几烫损客损
    "RCASE_8443": "餐饮食品投诉",    # 面馆菜品客诉+房间烟味
    "RCASE_8442": "空调/温度投诉",  # 客诉房间热要求全免房费
    "RCASE_8441": "安全隐私投诉",    # 员工13号电梯故障
    "RCASE_8410": "清洁卫生投诉",   # 卫生间卫生投诉
}

with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build category lookup by name
cat_map = {}
for e in data['entities']:
    if e.get('type') == 'complaint_category':
        cat_map[e['name']] = e

print("=== 投诉分类 ===")
for name, ent in cat_map.items():
    print(f"  {ent['id']}: {name}")

# Build existing relationships lookup
existing_rels = set()
for r in data['relationships']:
    if r.get('type') == 'case_category':
        key = (r['source_id'], r['target_id'])
        existing_rels.add(key)

# Find max relationship ID
max_rel_id = 0
for r in data['relationships']:
    rid = r.get('id', '')
    if rid.startswith('R') and rid[1:].isdigit():
        num = int(rid[1:])
        if num > max_rel_id:
            max_rel_id = num

# Check which cases exist
existing_case_ids = set(e['id'] for e in data['entities'])

new_rels_added = 0
new_entities_added = 0

# Case data for any cases that don't exist yet
CASE_DATA = {
    "RCASE_8454": ("浴室大理石挡板脱落", "2026-05-31", "Ms.Castillo Adriana & Mr.Rizzi Louis", "2005->1910", "客人来前台展示手机图片，房间浴室的大理石挡板面整个脱落。前台经理向客人表示歉意，客人没有受伤，也表示这个自己突然脱落了。前台经理为客人升级到了1910房间。客人换走后，gsm进现场进行了查看拍照，也同步通知到了客房和工程。GSM为客人的新房间赠送了水果+红酒。"),
    "RCASE_8453": ("工程部仓管员受伤就医", "2026-05-28", "/", "/", "5/28 10:40am，接到工程部上报，仓管人员潘靖在仓库不慎摔伤。左侧眉骨处出现表皮擦伤，伴随少量出血；员工本人自述右肩酸痛、略有头晕。事发时正在仓库整理木条，不慎被地面木条绊倒。倒地时手部先行撑地缓冲，头部仍不慎磕碰地面。GSM已开通就医绿色通道，由工程部同事陪同前往九龙医院就诊。"),
    "RCASE_8452": ("房间断电", "2026-05-28", "Mr.Xu Lie", "3515", "5.28 凌晨4:10，客人致电前台告知房间突然断电，灯全部都灭了。前台立刻致歉并表示可以先安排一间同层的房间先休息，行李可以继续放在房间。客人表示没事，只是反馈一下，不影响休息，随后挂断电话。GSM已交接同事关注客人服务。"),
    "RCASE_8451": ("车库剐蹭消防喷淋头", "2026-05-23", "Ms Xu Xiang Hong / Ms Zhou Ling / Ms Xu Huan Huan / Ms Zhou Yuan Yuan", "4205/4207/4210", "14:56接礼宾通知，B2车库管道漏水。GSM和安保工程前往查看，为客人车辆剐蹭到消防喷淋头导致爆管。客人第一时间报警，交警及物业已到达现场处理车库地面大面积积水。客人预订了但还没入住，刚停车就发生了事件。后安保孙经理协助客人将车辆停在地面车位。"),
    "RCASE_8450": ("花洒断裂砸脚", "2026-05-20", "Mr.Zhao Yang", "3001", "23:45，RM3001客人致电总机反馈洗澡时花洒断了砸到脚。总机同事提出帮客人换房或通知工程同事维修，或直接帮客人转接GSM。客人说时间太晚了，不想折腾了，今晚不要打扰他，希望到次日退房时酒店能给个说法。总机同事将此事汇报给GSM。因客人不希望被打扰，GSM没能到现场查看拍照。已通知安保主管。已交接次日GSM跟进。"),
    "RCASE_8449": ("客人浴室滑倒摔伤", "2026-05-17", "Ms.Zhou Yue", "3005", "2:50接到前台反馈，客人在房间摔伤，需要碘伏棉签。GSM和安保主管一同前往房间查看，客人右脚小腿受伤，客人表示是洗澡出来，未穿鞋，地面有水滑倒导致。GSM协助客人处理了伤口，客人表示感谢。GSM持续关注。"),
    "RCASE_8448": ("房门反锁打不开", "2026-05-16", "Ms.Yang Fan & Ms.Wang Yan Xin", "2116", "23:19接到礼宾反馈，2116房门反锁，房卡无法开启。GSM使用MK也无法开启。通知工程和安保一同到现场查看。杨女士是看完演唱会回房，房间仅有小朋友在，应该是睡着了。门锁是反锁状态，多次尝试MK无法打开，工程使用特殊工具进行强开，开门后确认小朋友是睡着了，无异常。客人对酒店表示感谢。"),
    "RCASE_8447": ("天花墙皮脱落", "2026-05-16", "Mr.kang Xiaoyang", "4119", "8:20总机通知GSM，4119客人反映天花墙皮脱落，人没事，但砸到了他的物品。GSM到房间看到写字台上方的墙皮脱落了大概一平方米左右。掉落的墙皮粉末砸在写字台上的笔记本、手机和私人物品上。客人讲昨晚半夜听到东西掉落的声响，以为是背包掉地上就继续睡了，早上起来才发现。GSM对房间墙皮脱落进行了拍照取证，已通知工程处理。"),
    "RCASE_8446": ("手指被水龙头刮破", "2026-05-15", "Mr.Zeng Yiming", "2610", "23:40客人致电总机反馈，手指被水龙头刮破，需要送创可贴。GSM立即送创可贴和碘伏棉签到RM2610，客人说房间淋浴头把手很锋利，手指被刮破。因女朋友在洗澡，不方便去淋浴间查看，GSM只拍了客人手指的照片。客人对GSM表示感谢。已通知安保主管。"),
    "RCASE_8445": ("房间灯自动亮5次-RCU故障", "2026-05-14", "Ms.Teoh Bee Fang & Ms.Chan Jeh Huei", "3122(原3120)", "5.14凌晨4点半，客人反馈3120房间的灯夜里自动亮了5次。RCU面板有问题，先给客人锁了3122休息。5.14下午三点客人告知想直接换新房间，并就此事要求补偿。房间已赠送店红两瓶以及致歉水果，客人已安抚好。3120房间为RCU主板故障，工程已维修完毕。"),
    "RCASE_8444": ("小茶几烫损客损", "2026-05-08", "Mr.Gao Ming & Ms.Yan Li Ying", "2208", "5月8日16:04，客房部上报客房内小茶几被烫损。GSM、客房部和工程部一同入房现场核查。房间内发现打火机及香烟，但未找到对应烟头。因同行有女士，洗漱台摆放两支卷发棒，疑似卷发棒高温所致。19:34客房部提交工程维修报价单，维修费用合计545元。"),
    "RCASE_8443": ("面馆菜品客诉+房间烟味", "2026-05-07", "Ms.Long Yu Han", "3815", "20:22客人到前台反馈在3楼面馆用餐，香菇是酸的且里面都是沙子。面馆已告知客人面馆是独立运营非酒店运营。面馆给客人退了香菇和葱油拌面的费用。客人随后又反馈房间有烟味。GSM赠送了2张早餐券。提出换房客人拒绝。City Ledger减免133.00。"),
    "RCASE_8442": ("客诉房间热要求全免房费", "2026-05-05", "Mr.Liu Sulin / Ms.Fan Yanchun", "3127", "凌晨00:33客人投诉房间温度偏高无法正常入睡。工程部实测室温22-23℃，已增补薄被。上午09:53客人再次反馈房间偏热，自述夜间休息不佳要求处理方案。GSM协同工程部人员至房间现场核查，房间入住两大两小，实测温度22.9℃-24℃，空调出风口约17℃，GSM及工程师体感均偏凉爽。"),
    "RCASE_8441": ("员工13号电梯故障", "2026-05-03", "N/A", "N/A", "23:17，GSM和安保乘坐13号电梯时，电梯运行至36楼时突然断电骤停，继而抖动。几秒钟后恢复正常运行。随即联系工程并通知通力维保维修。23:33维保人员到达，检查后确定是继电器损坏，更换继电器后电梯恢复正常运行。"),
    "RCASE_8410": ("卫生间卫生投诉(排泄物未清理)", "2026-05-02", "Ms.Cao Min & Mr.Tang Fei", "3618", "5/2 22:59GSM接到总机通知，3618客人反馈卫生间地面有排泄物，没清理干净。GSM立即和客房主管一同赶往现场。在马桶间，马桶正前方地面确有黄褐色污渍，和排泄物高度相似，且污渍已风干。GSM和客房主管一同向客人致歉。GSM提议给客人换房，但客人表示已经洗漱过不想再换房。为表歉意，GSM赠送客人第二天的早餐。客房对卫生间马桶区域进行彻底清洁及全面消毒处理。"),
}

for cid, cat_name in CASE_CATEGORY_MAP.items():
    # 1. Ensure case entity exists
    if cid not in existing_case_ids:
        issue, date, guest, room, desc = CASE_DATA[cid]
        entity = {
            "id": cid,
            "name": f"{issue} - {guest}",
            "type": "complaint_case",
            "description": f"【真实案例】{cid} - {issue}（{date}）\n\n客人：{guest}\n房间：{room}\n日期：{date}\n问题：{issue}\n\n{desc}"
        }
        data['entities'].append(entity)
        existing_case_ids.add(cid)
        new_entities_added += 1
        print(f"[NEW ENTITY] {cid}")

    # 2. Find category
    target_cat = cat_map.get(cat_name)
    if not target_cat:
        print(f"[ERROR] No category found for '{cat_name}'")
        continue

    # 3. Check if relationship already exists
    rel_key = (cid, target_cat['id'])
    if rel_key in existing_rels:
        print(f"[SKIP] {cid} -> {cat_name} (already exists)")
        continue

    # 4. Create relationship
    max_rel_id += 1
    rel = {
        "id": f"R{max_rel_id}",
        "source_id": cid,
        "target_id": target_cat['id'],
        "relation": "HAS_CASE",
        "type": "case_category"
    }
    data['relationships'].append(rel)
    existing_rels.add(rel_key)
    new_rels_added += 1
    print(f"[ADD REL] {cid} -> {cat_name} ({target_cat['id']})")

# Update meta
data['meta']['last_updated'] = '2026-06-01 10:15'
data['meta']['description'] = 'GSM运营站 v6.11 - 新增2026年5月15个投诉/事件案例'

# Write
with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count by category
cat_stats = {}
for r in data['relationships']:
    if r.get('type') == 'case_category':
        for e in data['entities']:
            if e['id'] == r['target_id']:
                cat_stats[e['name']] = cat_stats.get(e['name'], 0) + 1
                break

print(f"\n{'='*50}")
print(f"修复完成")
print(f"{'='*50}")
print(f"新增实体: {new_entities_added}")
print(f"新增关系: {new_rels_added}")
print(f"当前总实体数: {len(data['entities'])}")
print(f"当前总关系数: {len(data['relationships'])}")

print(f"\n新导入的15个case列表:")
for cid in CASE_CATEGORY_MAP:
    issue, date, guest, _, _ = CASE_DATA[cid]
    print(f"  {cid}: {issue} ({date}, {guest})")

print(f"\n分类统计:")
for cn in sorted(cat_stats.keys()):
    print(f"  {cn}: {cat_stats[cn]}个案例")
