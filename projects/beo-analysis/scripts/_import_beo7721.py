"""2026-06-18: Import BEO #7721 - Mrs.Du's Grandson Ceremony Lunch"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

FB_GRAPH = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_graph.json'

with open(FB_GRAPH, 'r', encoding='utf-8') as f:
    fb = json.load(f)

existing_ids = set(e.get("id", "") for e in fb["entities"])

beo_id = "BEO_7721"
event_id = "BEO_7721_event"
menu_id = "BEO_7721_menu"
venue_id = "BEO_7721_venue"

added = 0

# BEO entity
if beo_id not in existing_ids:
    beo = {
        "id": beo_id,
        "type": "beo",
        "label": "杜老师孙子周岁午宴",
        "beo_number": 7721,
        "date": "2026-06-21",
        "dow": "Sunday",
        "time": "11:30-14:30",
        "setup_time": "07:00-11:00",
        "venue": "Function Room 3+4",
        "client": "Mrs. Du (杜老师)",
        "client_short": "杜老师",
        "event_type": "周岁午宴",
        "pax": 20,
        "pax_guaranteed": 20,
        "tables": 2,
        "table_type": "Round Tables of 10",
        "price_per_table": 3500,
        "total_revenue": 7000,
        "deposit": 0,
        "deposit_method": "无定金",
        "settlement": "挂账PM9078 (c#1305608)，杜主任午宴后结算",
        "contact": "Ms. Du",
        "sales": "Luisa Liu (刘艳)",
        "catering": "Luisa Liu (刘艳)",
        "service": "Luisa Liu (刘艳)",
        "menu_type": "中式宴会套餐",
        "menu_price": "CNY 3,500/桌",
        "beverage": "所有酒水饮料客户自带",
        "note": "当天中午赠送一只三磅水果鲜奶蛋糕，已签好的ENT当天给餐厅",
        "source_file": "BEO_7721_杜老师孙子周岁午宴.pdf"
    }
    fb["entities"].append(beo)
    added += 1
    print(f"  [ADD] {beo_id}")

# Event entity
if event_id not in existing_ids:
    event = {
        "id": event_id,
        "type": "beo_event",
        "name": "BEO #7721 杜老师孙子周岁午宴",
        "beo_number": 7721,
        "date": "2026-06-21",
        "time": "11:30-14:30",
        "venue": "Function Room 3+4",
        "total_revenue": 7000,
        "setup_req": "圆桌式摆台,2张圆桌*10人/桌共20人;标准午宴摆台;舞台(5.4m*2.4m*0.4m)贴着墙放;签到桌;桌布绿色,椅套白色,口布绿色;蛋糕推车一辆;三个宝宝椅",
        "av_req": "提前调试好会议室内投影设备(小米投屏+生日歌);提前调试好会议室内音响设备,准备2个无线话筒",
        "engineering_req": "提前打开空调并确保运作正常;提前开好空调面板确保客户抵达时室内温度凉爽无异味(客户工作跟暖通相关);梅雨天确保厅内无异味",
        "housekeeping_req": "确保会议室及盥洗室在活动期间及活动结束后保持干净",
        "security_req": "活动开始前客人有车辆停靠,安排地面/地下停车位并做好指引;活动公司21号早7点从B1收货平台进场,安排保安部同事办理施工证;活动开始前及结束后安排保安部同事协助检查",
        "front_office": "活动公司负责人预计21号早上7点至前台交人民币3,000作为布场押金,开押金单;活动结束后凭宴会厅/工程部/保安部三方签字押金单到前台退还押金",
        "finance_type": "Social",
        "all_departments": "工程部/客房部/前厅部/保安部/财务部需协调",
        "source_file": "BEO_7721_杜老师孙子周岁午宴.pdf"
    }
    fb["entities"].append(event)
    added += 1
    print(f"  [ADD] {event_id}")

# Menu entity
if menu_id not in existing_ids:
    menu_items = [
        "海派精致八小碟（津津鲍鱼卷，水晶肴肉，香菜鱼皮，麻辣口水鸡，蜜汁红枣，桂花糯米藕，蔬菜色拉，巧手拌笋丝）",
        "北京片皮鸭",
        "蒜蓉粉丝蒸波龙",
        "香芋南瓜椰香煲",
        "和风炭烧牛肉粒",
        "咸肉蛋饺全家福",
        "百叶结台湾卤肉",
        "蒜蓉粉丝蒸鲍鱼",
        "葱油开边桂花鱼",
        "鲜松茸炖老鸡汤",
        "莲藕西芹炒百合",
        "清炒时令油麦菜",
        "清炒鸡毛菜",
        "苏式红汤生日面",
        "苏式丝滑蛋挞",
        "红豆沙煮小圆子",
        "江南时令水果盘"
    ]
    menu = {
        "id": menu_id,
        "type": "beo_menu",
        "name": "BEO #7721 菜单 (中式宴会套餐CNY3,500/桌)",
        "beo_number": 7721,
        "menu_type": "中式宴会套餐",
        "items": menu_items,
        "price_per_table": 3500,
        "source_file": "BEO_7721_杜老师孙子周岁午宴.pdf"
    }
    fb["entities"].append(menu)
    added += 1
    print(f"  [ADD] {menu_id}")

# Relationships
new_count = 0
pairs = [
    (beo_id, "has_event", event_id),
    (beo_id, "has_menu", menu_id),
    (event_id, "held_at", venue_id),
]
for s, t, o in pairs:
    if not any(r.get("subject")==s and r.get("type")==t and r.get("object")==o for r in fb["relations"]):
        fb["relations"].append({"subject": s, "type": t, "object": o})
        new_count += 1
        print(f"  [REL] {s} ->[{t}]-> {o}")

# Update meta
fb["meta"]["version"] = "v4.34"
fb["meta"]["last_updated"] = "2026-06-18 13:40"
fb["meta"]["description"] = f"v4.33 + BEO#7721 (杜老师孙子周岁午宴)"

with open(FB_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(fb, f, ensure_ascii=False, indent=2)

print(f"\nFB站BEO #7721 导入完成!")
print(f"  新增: 实体{added} + 关系{new_count}")
print(f"  杜老师孙子周岁午宴 | ¥7,000 | 20人/2桌 | 中式宴会套餐(17道)")
print(f"  FB站总计: {len(fb['entities'])}实体 / {len(fb['relations'])}关系 / {fb['meta']['version']}")
