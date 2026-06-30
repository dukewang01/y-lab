#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import full May HF (5/1-5/31) into FIN graph v5.5 upgrade"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json, os, copy
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# ====== 全月31天数据 ======
HISTORY = [
    ("2026-05-01 Fri", 438, 81.04, 350321.40, 803.49, 90, "history"),
    ("2026-05-02 Sat", 491, 90.89, 463916.27, 948.70, 219, "history"),
    ("2026-05-03 Sun", 465, 86.06, 450831.29, 973.72, 286, "history"),
    ("2026-05-04 Mon", 330, 60.97, 240250.93, 732.47, 338, "history"),
    ("2026-05-05 Tue", 147, 26.95, 85628.43, 590.54, 234, "history"),
    ("2026-05-06 Wed", 258, 47.58, 149866.48, 585.42, 34, "history"),
    ("2026-05-07 Thu", 514, 95.17, 318575.69, 622.22, 93, "history"),
    ("2026-05-08 Fri", 464, 85.87, 279566.21, 605.12, 193, "history"),
    ("2026-05-09 Sat", 237, 43.68, 136633.41, 581.42, 341, "history"),
    ("2026-05-10 Sun", 232, 42.75, 131720.26, 572.70, 120, "history"),
    ("2026-05-11 Mon", 389, 71.93, 212253.07, 548.46, 47, "history"),
    ("2026-05-12 Tue", 437, 80.86, 248095.40, 570.33, 116, "history"),
]

FORECAST = [
    ("2026-05-13 Wed", 432, 79.93, 235112.60, 546.77, 172, "forecast"),
    ("2026-05-14 Thu", 354, 65.43, 194729.16, 553.21, 208, "forecast"),
    ("2026-05-15 Fri", 334, 61.71, 196393.95, 591.55, 189, "forecast"),
    ("2026-05-16 Sat", 425, 78.62, 356405.35, 842.57, 162, "forecast"),
    ("2026-05-17 Sun", 280, 51.67, 184459.43, 663.52, 266, "forecast"),
    ("2026-05-18 Mon", 214, 39.41, 129724.93, 611.91, 137, "forecast"),
    ("2026-05-19 Tue", 234, 42.57, 142189.72, 620.92, 33, "forecast"),
    ("2026-05-20 Wed", 223, 41.08, 135596.34, 613.56, 45, "forecast"),
    ("2026-05-21 Thu", 223, 41.08, 140213.09, 634.45, 47, "forecast"),
    ("2026-05-22 Fri", 160, 29.37, 102240.70, 647.09, 74, "forecast"),
    ("2026-05-23 Sat", 158, 29.00, 96490.50, 618.53, 51, "forecast"),
    ("2026-05-24 Sun", 134, 24.54, 70581.90, 534.71, 52, "forecast"),
    ("2026-05-25 Mon", 152, 27.88, 80165.65, 534.44, 30, "forecast"),
    ("2026-05-26 Tue", 158, 29.00, 83860.40, 537.57, 21, "forecast"),
    ("2026-05-27 Wed", 197, 36.25, 100517.57, 515.47, 32, "forecast"),
    ("2026-05-28 Thu", 192, 35.32, 99609.60, 524.26, 19, "forecast"),
    ("2026-05-29 Fri", 198, 36.43, 103845.30, 529.82, 40, "forecast"),
    ("2026-05-30 Sat", 211, 38.85, 111637.09, 534.15, 41, "forecast"),
    ("2026-05-31 Sun", 205, 37.73, 105907.60, 521.71, 51, "forecast"),
]

ALL_DAYS = HISTORY + FORECAST

# ====== 加载当前fin图谱 ======
fp = os.path.join(BASE, "fin_graph.json")
fin = json.load(open(fp, 'r', encoding='utf-8'))
nodes = fin.get("nodes", [])
edges = fin.get("edges", fin.get("relationships", []))

# 找出已有版本号
version_node = [n for n in nodes if n.get("id","").startswith("FIN_VER")]
ver = "v5.5"
for vn in version_node:
    old_ver = vn.get("id","")
    old_ver_num = old_ver.replace("FIN_VER_","").replace("_",".")
    ver = f"v5.5 (from {old_ver_num})"
    break

print(f"FIN图谱当前版本: {version_node[0]['id'] if version_node else 'unknown'}")
print(f"升级至: {ver}")
print(f"现有节点: {len(nodes)}, 边: {len(edges)}")

# 检查哪些day已经存在
existing_days = set()
for n in nodes:
    if n.get("type") in ("daily_revenue","day","DRR_day") or "05." in n.get("id",""):
        existing_days.add(n.get("id",""))

# 只导入新数据
existing = set()
for d, occ_val, occ_pct, rev, adr, dep, kind in ALL_DAYS:
    day_id = d[:10].replace("-","")
    nid = f"day_{day_id}"
    if any(nid in n.get("id","") for n in nodes):
        existing.add(day_id)

to_add = [d for d in ALL_DAYS if d[0][:10].replace("-","") not in existing]
print(f"\n已有日: {len(existing)}天, 需新增: {len(to_add)}天")

# 如果没有新增，也需要更新forecast数据
if not to_add:
    print("所有日子已存在，更新已有节点的forecast字段")
    # 更新forecast类型
    for n in nodes:
        for d, occ_val, occ_pct, rev, adr, dep, kind in FORECAST:
            day_id = d[:10].replace("-","")
            if day_id in n.get("id","") and kind == "forecast":
                n["forecast_occ"] = occ_pct
                n["forecast_rev"] = rev
                n["forecast_adr"] = adr
                n["forecast_kind"] = "forecast"
    print("forecast字段已更新")
else:
    # 构建新节点
    new_nodes = []
    new_edges = []
    
    # 找到酒店节点
    hotel_node = [n for n in nodes if "Suzhou" in n.get("id","") or "hilton" in n.get("label","").lower() or "希尔顿" in str(n.get("label",""))]
    hotel_id = hotel_node[0]["id"] if hotel_node else "hotel_hilton_suzhou"
    
    # 找到May月节点
    may_node = [n for n in nodes if n.get("id","") == "month_202605" or n.get("label","") == "2026年5月"]
    
    for d, occ_val, occ_pct, rev, adr, dep_nodes, kind in to_add:
        day_id = d[:10].replace("-","")
        dow = d[11:14]
        nid = f"day_{day_id}"
        
        node = {
            "id": nid,
            "type": "daily_revenue",
            "label": d[:10],
            "dow": dow,
            "occ": occ_pct,
            "occ_nights": occ_val,
            "room_revenue": rev,
            "adr": adr,
            "departures": dep_nodes,
            "kind": kind,
            "hotel": "hilton_suzhou",
            "month": "2026-05",
        }
        new_nodes.append(node)
        
        # 边：day -> hotel
        new_edges.append({
            "source": nid,
            "target": hotel_id,
            "type": "belongs_to_hotel",
            "label": f"{d[:10]} belongs to Hilton Suzhou"
        })
        
        # 如果有月节点就链接
        if may_node:
            new_edges.append({
                "source": nid,
                "target": may_node[0]["id"],
                "type": "belongs_to_month",
                "label": f"{d[:10]} belongs to 2026-05"
            })
    
    nodes.extend(new_nodes)
    edges.extend(new_edges)
    print(f"+{len(new_nodes)} 节点, +{len(new_edges)} 边")

# 更新版本号
old_vers = [n for n in nodes if n.get("type","").startswith("version") or n.get("id","").startswith("FIN_VER_")]
for ov in old_vers:
    nodes.remove(ov)
    print(f"  移除旧版本: {ov['id']}")

ver_node = {
    "id": f"FIN_VER_v5_5",
    "type": "version",
    "label": f"FIN v5.5 - Full May HF import ({datetime.now().strftime('%m-%d %H:%M')})",
    "date": "2026-05-14",
    "source": "HF_5.13_PDF",
    "notes": "导入5月全月31天HF数据（12天实绩+19天预测）",
    "days": 31,
    "history_days": 12,
    "forecast_days": 19
}
nodes.append(ver_node)

# 写回
fin["nodes"] = nodes
fin["edges"] = edges
fin["relationships"] = edges  # 兼容命名

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print(f"\n写入完成!")
print(f"  FIN图谱: {len(nodes)} 节点, {len(edges)} 边")
print(f"  版本: {ver}")
