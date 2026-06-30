"""2026-06-18: Import BEO #7720 - Ms. Yu Birthday Lunch"""
import json, os, shutil

FB_GRAPH = r'C:\Users\Y\.openclaw\workspace\knowledge_center\fb_graph.json'
FIN_GRAPH = r'C:\Users\Y\.openclaw\workspace\knowledge_center\fin_graph.json'

# ===== BEO #7720 Data =====
beo_data = {
    "beo_number": 7720,
    "date": "2026-06-20",
    "dow": "Saturday",
    "time": "11:30-14:00",
    "venue": "Function Room 3+4",
    "venue_cn": "多功能厅3+4",
    "client": "Ms. Yu",
    "client_short": "俞女�?,
    "event_type": "生日午宴",
    "event_type_cn": "中式午餐",
    "pax_guaranteed": 40,
    "pax_expected": 40,
    "tables": 4,
    "table_type": "Round Tables of 10",
    "table_type_cn": "圆桌10�?,
    "price_per_table": 3200,
    "price_food": 3000,
    "price_beverage": 100,
    "price_cake": 100,
    "total_revenue": 12800,
    "deposit": 6400,
    "deposit_method": "定金",
    "settlement": "挂账PM9085 (#1305133)�?�?0日信用卡/现金",
    "contact": "Zhe Yu (+86 134 0007 3760)",
    "on_site_contact": "Zhe Yu",
    "on_site_mobile": "+86 134 0007 3760",
    "sales": "Elaine He",
    "catering": "",
    "service": "",
    "menu_type": "中式套餐",
    "beverage": "可乐、雪碧、橙汁畅饮；其他酒水自带，收开瓶服务费",
    "note": "凭餐券进�?,
    "special_requirements": "红色台布打底、白色台布、白色椅套和台布、红色蝴蝶结；厅内需�?张长条桌作工作台；清洁物料当天带来，注意回收与保管；带一个蛋糕准备摆�?拍照台，搭配鲜花装饰",
    "setup_req": "中式摆台�?�?,
    "av_req": "请提前调试好会议室内投影设备、话筒设备，设备2�?,
    "engineering": "提前打开地毯、空调确保运作正常；10:30前备一�?升热水壶待用",
    "housekeeping": "确保会议室及洗手间在活动期间及活动结束后保持干净",
    "security": "活动开始前客人有车辆辗录，请安排地�?车库车位并协助指引；活动开始前有水果运送，请安排保安协助卸�?,
    "finance": "Social (社交活动)",
    "menu_items": [
        "晖港式烧味拼�?,
        "高汤松茸花胶�?,
        "咖喱洋葱焗香�?,
        "吊烧脆皮芝麻�?,
        "皇徽莲藕牛肉�?,
        "如绿红烧状元�?,
        "芬式脆皮炸子�?,
        "福果百合炒西�?,
        "上汤浸时令蔬�?,
        "广式干烧炒伊�?,
        "美点/糖水绿豆�?,
        "江南时令水果�?
    ],
    "source_file": "BEO_7720_俞女士生日午�?pdf"
}

# ===== Import to FB Graph =====
with open(FB_GRAPH, 'r', encoding='utf-8') as f:
    fb = json.load(f)

existing_ids = set(e.get("id", "") for e in fb["entities"])

beo_id = f"BEO_{beo_data['beo_number']}"
event_id = f"BEO_{beo_data['beo_number']}_event"
menu_id = f"BEO_{beo_data['beo_number']}_menu"
venue_id = f"BEO_{beo_data['beo_number']}_venue"

added = 0

# 1. BEO entity
if beo_id not in existing_ids:
    beo_entity = {
        "id": beo_id,
        "type": "beo",
        "label": f"俞女士生日午�?,
        "beo_number": beo_data["beo_number"],
        "date": beo_data["date"],
        "dow": beo_data["dow"],
        "time": beo_data["time"],
        "venue": beo_data["venue"],
        "client": beo_data["client"],
        "client_short": beo_data["client_short"],
        "event_type": beo_data["event_type"],
        "pax": beo_data["pax_expected"],
        "pax_guaranteed": beo_data["pax_guaranteed"],
        "tables": beo_data["tables"],
        "price_per_table": beo_data["price_per_table"],
        "price_food": beo_data["price_food"],
        "price_beverage": beo_data["price_beverage"],
        "deposit": beo_data["deposit"],
        "deposit_method": beo_data["deposit_method"],
        "settlement": beo_data["settlement"],
        "contact": beo_data["contact"],
        "sales": beo_data["sales"],
        "catering": beo_data["catering"],
        "menu": beo_data["menu_type"],
        "beverage": beo_data["beverage"],
        "note": beo_data["note"],
        "source_file": beo_data["source_file"]
    }
    fb["entities"].append(beo_entity)
    added += 1
    print(f"  [ADD] {beo_id}")

# 2. Event entity (for detail data not fitting in beo entity)
if event_id not in existing_ids:
    event_entity = {
        "id": event_id,
        "type": "beo_event",
        "name": f"BEO #{beo_data['beo_number']} 俞女士生日午�?,
        "beo_number": beo_data["beo_number"],
        "date": beo_data["date"],
        "time": beo_data["time"],
        "venue": beo_data["venue"],
        "total_revenue": beo_data["total_revenue"],
        "setup_req": beo_data["setup_req"],
        "av_req": beo_data["av_req"],
        "engineering_req": beo_data["engineering"],
        "housekeeping_req": beo_data["housekeeping"],
        "security_req": beo_data["security"],
        "finance_type": beo_data["finance"],
        "special_requirements": beo_data["special_requirements"],
        "menu_items": "; ".join(beo_data["menu_items"]),
        "source_file": beo_data["source_file"]
    }
    fb["entities"].append(event_entity)
    added += 1
    print(f"  [ADD] {event_id}")

# 3. Menu entity
if menu_id not in existing_ids:
    menu_entity = {
        "id": menu_id,
        "type": "beo_menu",
        "name": f"BEO #{beo_data['beo_number']} 菜单",
        "beo_number": beo_data["beo_number"],
        "menu_type": beo_data["menu_type"],
        "items": beo_data["menu_items"],
        "price_per_table": beo_data["price_per_table"],
        "source_file": beo_data["source_file"]
    }
    fb["entities"].append(menu_entity)
    added += 1
    print(f"  [ADD] {menu_id}")

# 4. Add relationships
new_rels = []
# BEO -> has_event
if beo_id in existing_ids or beo_id not in existing_ids:
    # Always add if not exists
    if not any(r.get("subject")==beo_id and r.get("type")=="has_event" and r.get("object")==event_id for r in fb["relations"]):
        new_rels.append({"subject": beo_id, "type": "has_event", "object": event_id})
        new_rels.append({"subject": beo_id, "type": "has_menu", "object": menu_id})

# Event -> held_at -> venue
if not any(r.get("subject")==event_id and r.get("type")=="held_at" and r.get("object")==venue_id for r in fb["relations"]):
    new_rels.append({"subject": event_id, "type": "held_at", "object": venue_id})

# BEO -> belongs_to -> outlet (多功能厅3+4)
# Check if venue entity exists for Function Room 3+4
venue_entity = None
for e in fb["entities"]:
    if e.get("name") == "Function Room 3+4" or e.get("venue") == "Function Room 3+4":
        venue_entity = e
        break

if new_rels:
    fb["relations"].extend(new_rels)
    added += len(new_rels)
    for r in new_rels:
        print(f"  [REL] {r['subject']} ->[{r['type']}]-> {r['object']}")

# Update meta
fb["meta"]["version"] = "v4.33"
fb["meta"]["last_updated"] = "2026-06-18 10:25"
fb["meta"]["description"] = f"v4.32 + BEO#{beo_data['beo_number']} ({beo_data['client_short']})"

# Save
with open(FB_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(fb, f, ensure_ascii=False, indent=2)

print(f"\nFB站BEO #{beo_data['beo_number']} 导入完成!")
print(f"  新增: 实体{3 if beo_id not in existing_ids else '0'} + 关系{len(new_rels)}")
print(f"  BEO: {beo_data['client_short']} | ¥{beo_data['total_revenue']} | {beo_data['pax_expected']}�?| {beo_data['menu_type']}")
print(f"  FB站总计: {len(fb['entities'])}实体 / {len(fb['relations'])}关系 / {fb['meta']['version']}")
