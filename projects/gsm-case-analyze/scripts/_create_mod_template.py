#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

# ====== MOD模板设计 ======
template = {
    "template_id": "TEMPLATE_MOD_REPORT_v1",
    "template_name": "MOD值班检查报告模板",
    "version": "v1.0",
    "created": "2026-05-14",
    "source": "MOD_report_20260510.xlsx",
    
    "structure": {
        "header": {
            "mod_name": "string (值班主任姓名)",
            "date": "date (值班日期)",
            "shift": "string (班次: 17:30-08:30)"
        },
        
        "guest_area": {
            "description": "宾客区巡检",
            "default_time": "19:00",
            "locations": [
                {"name": "Entrance/Lobby/Front Office", "label": "大堂/前台"},
                {"name": "YUAN Lounge", "label": "YUAN大堂吧"},
                {"name": "Open Restaurant", "label": "OPEN全日餐厅"},
                {"name": "YUXI", "label": "御玺中餐厅"},
                {"name": "BACIO", "label": "BACIO意大利餐厅"},
                {"name": "Executive Lounge", "label": "行政酒廊"},
                {"name": "Fitness Center & Pool", "label": "健身中心/泳池"},
                {"name": "Public Restrooms", "label": "公共卫生间"},
            ],
            "check_items": [
                "Clean, organized, operational (清洁/有序/运营正常)",
                "Lighting at comfortable setting (灯光舒适度)",
                "P/A music system maintained (背景音乐正常)",
                "A/C or heating at comfort level (空调温度舒适)",
                "Team Member properly groomed (员工仪容仪表)",
                "Promotional material maintained (促销物料状态)",
                "Service standards maintained (服务标准执行)",
            ]
        },
        
        "back_of_house": {
            "description": "后区巡检",
            "default_time": "20:00",
            "locations": [
                {"name": "Team Member Entrance", "label": "员工通道"},
                {"name": "Garbage Room & Receiving", "label": "垃圾房/收货区"},
                {"name": "Kitchen", "label": "厨房"},
                {"name": "Storage Rooms", "label": "库房"},
                {"name": "Laundry", "label": "洗衣房"},
                {"name": "Engineering Workshop", "label": "工程部"},
            ],
            "check_items": [
                "Clean and organized (整洁有序)",
                "No slip/trip hazards (无滑倒/绊倒隐患)",
                "Security access controlled (门禁管控)",
                "Emergency exits clear (应急通道畅通)",
                "Fire extinguishers maintained (灭火器正常)",
                "Refrigeration temp logs checked (冰箱温度记录)",
            ]
        },
        
        "room_inspection": {
            "description": "客房抽查",
            "default_time": "23:00",
            "min_rooms": 2,
            "check_categories": [
                {"name": "Entrance Door", "label": "入口门", "items": ["门锁","门闩","消防逃生图","DND/清理牌","猫眼"]},
                {"name": "Wardrobe", "label": "衣柜", "items": ["浴袍/拖鞋","衣架","熨斗/熨板","保险箱"]},
                {"name": "Minibar", "label": "迷你吧", "items": ["品种齐全","价目表干净","冰箱/冰桶干净"]},
                {"name": "Bathroom", "label": "浴室", "items": ["清洁度","毛巾/备品","水压/排水","门锁/五金"]},
                {"name": "Bedroom", "label": "卧室", "items": ["床品状态","窗帘","电视/遥控器","电源/USB口","空调控制"]},
                {"name": "Furniture & Fixtures", "label": "家具设施", "items": ["沙发/桌椅","灯具","垃圾桶","电话"]},
            ]
        },
        
        "food_tasting": {
            "description": "食品试餐",
            "items": [
                {"field": "food_item", "label": "菜品名称", "type": "string"},
                {"field": "temperature", "label": "温度评分(1-10)", "type": "score"},
                {"field": "presentation", "label": "摆盘评分(1-10)", "type": "score"},
                {"field": "taste", "label": "口味评分(1-10)", "type": "score"},
                {"field": "overall", "label": "综合评分(1-10)", "type": "score"},
            ]
        },
        
        "safety_security": {
            "description": "安全安保检查",
            "checkpoints": [
                {"name": "Fire Central Control Room", "label": "消控中心"},
                {"name": "Fire Pumps Room", "label": "消防泵房"},
                {"name": "Kitchen Ansull System", "label": "厨房安素系统"},
                {"name": "Large Events", "label": "大型活动"},
                {"name": "Fire Evacuation Routes", "label": "消防疏散通道"},
                {"name": "ERT Response", "label": "ERT应急响应"},
                {"name": "Car Park", "label": "停车场"},
                {"name": "Hotel Perimeter", "label": "酒店周边"},
            ]
        },
        
        "issues_found": {
            "description": "发现的问题",
            "fields": [
                {"field": "location", "label": "位置", "type": "string"},
                {"field": "description", "label": "问题描述", "type": "text"},
                {"field": "severity", "label": "严重程度", "type": "select", "options": ["minor", "moderate", "critical"]},
                {"field": "reported_to", "label": "报告给", "type": "string"},
                {"field": "status", "label": "状态", "type": "select", "options": ["open", "in_progress", "resolved"]},
                {"field": "resolution_date", "label": "解决日期", "type": "date"},
            ]
        }
    }
}

# ====== 保存模板 ======
fp = os.path.join(BASE, "templates", "TEMPLATE_MOD_REPORT_v1.json")
os.makedirs(os.path.dirname(fp), exist_ok=True)
json.dump(template, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'MOD模板已保存: {fp}')

# ====== 导入GSM图谱 ======
gsm_fp = os.path.join(BASE, "gsm_graph.json")
gsm = json.load(open(gsm_fp, 'r', encoding='utf-8'))
entities = gsm.get("nodes", gsm.get("entities", []))
rels = gsm.get("edges", gsm.get("relationships", []))

existing_ids = set(e.get('id','') for e in entities)

# MOD模板节点
tid = "TEMPLATE_MOD_REPORT_v1"
if tid not in existing_ids:
    entities.append({
        "id": tid,
        "type": "template",
        "label": "MOD值班检查报告模板 v1.0",
        "template_type": "MOD_report",
        "version": "1.0",
        "created": "2026-05-14",
        "file": "templates/TEMPLATE_MOD_REPORT_v1.json",
        "source": "MOD_report_20260510.xlsx"
    })

# MOD报告实例节点（5/10 Duke值日）
mod_id = "MOD_2026_05_10_DUKE"
if mod_id not in existing_ids:
    issues = [
        {"location": "Room 3226 Bathroom", "description": "浴室门锁松动，关门困难", 
         "severity": "minor", "reported_to": "工程部", "status": "open"}
    ]
    entities.append({
        "id": mod_id,
        "type": "mod_report",
        "label": "2026-05-10 MOD检查报告 (Duke Wang)",
        "mod_name": "Duke Wang",
        "date": "2026-05-10",
        "shift": "17:30-08:30",
        "guest_area_inspected": "Entrance/Lobby, YUAN Lounge, Kitchen",
        "back_of_house_inspected": "TM Entrance, Garbage Room, Kitchen, Storage",
        "rooms_inspected": ["3223", "3226"],
        "room_issues": ["3226浴室门锁松动"],
        "food_tasting": None,
        "issues_count": 1,
        "issues": issues,
        "source": "MOD_report_20260510.xlsx"
    })

# 更新版本
if "gsm" in gsm_fp:
    # GSM站的版本追踪
    vers = [e for e in entities if e.get('type') == 'version' and 'GSM_VER' in e.get('id','')]
    for v in vers: entities.remove(v)
    entities.append({
        "id": "GSM_VER_v5_0_MOD",
        "type": "version",
        "label": "GSM v5.0 - 加入MOD报告模板&实例",
        "created": "2026-05-14"
    })

# 保存
gsm["nodes"] = gsm.get("nodes", entities) 
gsm["entities"] = entities
gsm["edges"] = rels
gsm["relationships"] = rels

json.dump(gsm, open(gsm_fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'GSM图谱更新: {len(entities)} 实体, {len(rels)} 关系')

print(f'\n=== MOD报告体系已建立 ===')
print(f'模板: TEMPLATE_MOD_REPORT_v1.json')
print(f'实例: MOD_2026_05_10_DUKE (5/10 Duke值日)')
print(f'问题: 1个 (3226浴室门锁-待处理)')
print(f'\n下次值MOD时填写模板即可自动归档到GSM站')
