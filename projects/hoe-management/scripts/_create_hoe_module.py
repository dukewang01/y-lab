#!/usr/bin/env python3
import json, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

# ====== 1. 在FB图谱中建HOE模块 ======
fb_fp = os.path.join(BASE, "fb_graph.json")
fb = json.load(open(fb_fp, 'r', encoding='utf-8'))
es = fb.get('entities', [])
rels = fb.get('relationships', fb.get('edges', []))
existing_ids = set(e.get('id','') for e in es)

hoe_entities = []

# 分类节点
categories = [
    ("HOE_CATEGORY_DRINK", "饮料茶咖", "饮品供应类"),
    ("HOE_CATEGORY_FOOD", "食品原料", "食材/食品原料类"),
    ("HOE_CATEGORY_EQUIPMENT", "设备器具", "厨房/吧台设备类"),
    ("HOE_CATEGORY_CLEANING", "清洁用品", "清洁/消毒类"),
    ("HOE_CATEGORY_UNIFORM", "员工制服", "布草/制服类"),
    ("HOE_CATEGORY_PRINTING", "印刷物料", "菜单/宣传品类"),
    ("HOE_CATEGORY_MAINTENANCE", "维保服务", "设备维保/技术支持类"),
    ("HOE_CATEGORY_OTHERS", "其他", "其他经营物资"),
]
for cid, cname, cdesc in categories:
    if cid not in existing_ids:
        hoe_entities.append({"id": cid, "type": "hoe_category", "label": cname, "description": cdesc})

# 合同类型
contract_types = [
    ("HOE_CTYPE_SUPPLY", "供应合同", "定期供货类"),
    ("HOE_CTYPE_LEASE", "租赁合同", "设备租赁类"),
    ("HOE_CTYPE_MAINTENANCE", "维保合同", "维修保养类"),
    ("HOE_CTYPE_SERVICE", "服务合同", "技术服务类"),
]
for cid, cname, cdesc in contract_types:
    if cid not in existing_ids:
        hoe_entities.append({"id": cid, "type": "hoe_contract_type", "label": cname, "description": cdesc})

# 供应商状态
vendor_statuses = [
    ("HOE_STATUS_ACTIVE", "合作中", "合同有效期内"),
    ("HOE_STATUS_EXPIRING", "即将到期", "30天内到期"),
    ("HOE_STATUS_EXPIRED", "已到期", "合同已过期"),
    ("HOE_STATUS_RENEWING", "续约中", "正在洽谈续约"),
]
for sid, sname, sdesc in vendor_statuses:
    if sid not in existing_ids:
        hoe_entities.append({"id": sid, "type": "hoe_status", "label": sname, "description": sdesc})

# 咖啡合同占位（先搭框架，具体内容后面填）
coffee_vendor_id = "HOE_VENDOR_COFFEE_001"
coffee_contract_id = "HOE_CONTRACT_COFFEE_SUPPLY_001"
coffee_equip_id = "HOE_CONTRACT_COFFEE_EQUIP_001"

hoe_entities.append({
    "id": "HOE_VENDOR_COFFEE_001",
    "type": "hoe_vendor",
    "label": "咖啡供应商（待定）",
    "category": "饮料茶咖",
    "status": "待录入",
    "import_date": "2026-05-14",
    "file": "咖啡制品供应合同&咖啡设备使用合同.pdf",
})

hoe_entities.append({
    "id": "HOE_CONTRACT_COFFEE_SUPPLY_001",
    "type": "hoe_contract",
    "label": "咖啡制品供应合同",
    "vendor_id": coffee_vendor_id,
    "contract_type": "供应合同",
    "category": "饮料茶咖",
    "status": "待录入",
    "import_date": "2026-05-14",
    "file": "咖啡制品供应合同&咖啡设备使用合同.pdf",
})

hoe_entities.append({
    "id": "HOE_CONTRACT_COFFEE_EQUIP_001",
    "type": "hoe_contract",
    "label": "咖啡设备使用合同",
    "vendor_id": coffee_vendor_id,
    "contract_type": "租赁合同",
    "category": "设备器具",
    "status": "待录入",
    "import_date": "2026-05-14",
    "file": "咖啡制品供应合同&咖啡设备使用合同.pdf",
})

# 模块总览节点
hoe_module = {
    "id": "FB_HOE_MODULE",
    "type": "fB_category",
    "label": "HOE模块 - 酒店经营物资管理",
    "description": "管理酒店运营设备和物料的合同/供应商/物资台账",
    "created": "2026-05-14",
    "entity_count": len(hoe_entities) + 8,  # 含分类
}
if hoe_module["id"] not in existing_ids:
    hoe_entities.append(hoe_module)

# 写入FB图谱
for e in hoe_entities:
    if e['id'] not in existing_ids:
        es.append(e)
        existing_ids.add(e['id'])

fb['entities'] = es
fb['relationships'] = rels
json.dump(fb, open(fb_fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 更新MEMORY（短标注）
memory_fp = os.path.join(BASE, "..", "MEMORY.md")
with open(memory_fp, 'a', encoding='utf-8') as mf:
    mf.write(f"\n### **2026年5月14日 — HOE模块建立** ✅\n")
    mf.write(f"在FB站内创建HOE模块，用于管理酒店经营物资合同/供应商。\n")
    mf.write(f"首批：8个品类 + 4种合同类型 + 4种供应商状态 + 咖啡合同占位\n")

print(f'FB图谱: {len(es)} 实体 | {len(rels)} 关系')
print(f'\n=== HOE模块已建立 ===')
print(f'品类:')
for _, cn, _ in categories:
    print(f'  📦 {cn}')
print(f'\n合同类型:')
for _, cn, _ in contract_types:
    print(f'  📄 {cn}')
print(f'\n首批待录入:')
print(f'  ☕ 咖啡供应商 → 咖啡制品供应合同')
print(f'  ☕ 咖啡供应商 → 咖啡设备使用合同')
print(f'\n接下来你把合同文件发过来，我解析条款入库。')
