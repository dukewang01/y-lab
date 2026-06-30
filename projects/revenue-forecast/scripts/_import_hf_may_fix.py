#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复FIN图谱数据: 将31天数据正确加入entities列表"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(BASE, "fin_graph.json")

fin = json.load(open(fp, 'r', encoding='utf-8'))
entities = fin.get("entities", [])
rels = fin.get("relationships", fin.get("edges", []))
edges = fin.get("edges", [])

print(f"现有 entities: {len(entities)}, rels: {len(rels)}, edges: {len(edges)}")

# 检查现有版本
vers = [e for e in entities if 'FIN_VER' in e.get('id','')]
print(f"版本节点: {len(vers)}")
for v in vers:
    print(f"  {v['id']} | {str(v.get('label',''))[:60]}")

# 检查是否有5月数据
may_days = [e for e in entities if e.get('id','').startswith('day_2026')]
print(f"现有天节点: {len(may_days)}")
for d in may_days[:5]:
    print(f"  {d['id']} | occ={d.get('occ')} | rev={d.get('room_revenue')}")

# ====== 全月31天数据 ======
DATA = [
    ("2026-05-01","Fri", 438, 81.04, 350321.40, 803.49, 90, "history"),
    ("2026-05-02","Sat", 491, 90.89, 463916.27, 948.70, 219, "history"),
    ("2026-05-03","Sun", 465, 86.06, 450831.29, 973.72, 286, "history"),
    ("2026-05-04","Mon", 330, 60.97, 240250.93, 732.47, 338, "history"),
    ("2026-05-05","Tue", 147, 26.95, 85628.43, 590.54, 234, "history"),
    ("2026-05-06","Wed", 258, 47.58, 149866.48, 585.42, 34, "history"),
    ("2026-05-07","Thu", 514, 95.17, 318575.69, 622.22, 93, "history"),
    ("2026-05-08","Fri", 464, 85.87, 279566.21, 605.12, 193, "history"),
    ("2026-05-09","Sat", 237, 43.68, 136633.41, 581.42, 341, "history"),
    ("2026-05-10","Sun", 232, 42.75, 131720.26, 572.70, 120, "history"),
    ("2026-05-11","Mon", 389, 71.93, 212253.07, 548.46, 47, "history"),
    ("2026-05-12","Tue", 437, 80.86, 248095.40, 570.33, 116, "history"),
    ("2026-05-13","Wed", 432, 79.93, 235112.60, 546.77, 172, "forecast"),
    ("2026-05-14","Thu", 354, 65.43, 194729.16, 553.21, 208, "forecast"),
    ("2026-05-15","Fri", 334, 61.71, 196393.95, 591.55, 189, "forecast"),
    ("2026-05-16","Sat", 425, 78.62, 356405.35, 842.57, 162, "forecast"),
    ("2026-05-17","Sun", 280, 51.67, 184459.43, 663.52, 266, "forecast"),
    ("2026-05-18","Mon", 214, 39.41, 129724.93, 611.91, 137, "forecast"),
    ("2026-05-19","Tue", 234, 42.57, 142189.72, 620.92, 33, "forecast"),
    ("2026-05-20","Wed", 223, 41.08, 135596.34, 613.56, 45, "forecast"),
    ("2026-05-21","Thu", 223, 41.08, 140213.09, 634.45, 47, "forecast"),
    ("2026-05-22","Fri", 160, 29.37, 102240.70, 647.09, 74, "forecast"),
    ("2026-05-23","Sat", 158, 29.00, 96490.50, 618.53, 51, "forecast"),
    ("2026-05-24","Sun", 134, 24.54, 70581.90, 534.71, 52, "forecast"),
    ("2026-05-25","Mon", 152, 27.88, 80165.65, 534.44, 30, "forecast"),
    ("2026-05-26","Tue", 158, 29.00, 83860.40, 537.57, 21, "forecast"),
    ("2026-05-27","Wed", 197, 36.25, 100517.57, 515.47, 32, "forecast"),
    ("2026-05-28","Thu", 192, 35.32, 99609.60, 524.26, 19, "forecast"),
    ("2026-05-29","Fri", 198, 36.43, 103845.30, 529.82, 40, "forecast"),
    ("2026-05-30","Sat", 211, 38.85, 111637.09, 534.15, 41, "forecast"),
    ("2026-05-31","Sun", 205, 37.73, 105907.60, 521.71, 51, "forecast"),
]

existing_ids = set(e.get('id','') for e in entities)
added = 0
new_rels = []

for datestr, dow, occ_nights, occ_pct, rev, adr, dep, kind in DATA:
    day_id = f"day_{datestr}"
    if day_id in existing_ids:
        # 更新forecast字段
        for e in entities:
            if e['id'] == day_id and kind == "forecast":
                e['forecast_occ'] = occ_pct
                e['forecast_rev'] = rev
                e['forecast_adr'] = adr
                e['forecast_kind'] = "forecast"
        continue
    
    entity = {
        "id": day_id,
        "type": "daily_revenue",
        "label": datestr,
        "dow": dow,
        "occ": occ_pct,
        "occ_nights": occ_nights,
        "room_revenue": rev,
        "adr": adr,
        "departures": dep,
        "kind": kind,
        "hotel": "hilton_suzhou",
        "month": "2026-05",
    }
    entities.append(entity)
    existing_ids.add(day_id)
    added += 1

print(f"新增entities: {added}")

# 更新版本号
for v in vers:
    entities.remove(v)
    print(f"  移除旧版本: {v['id']}")

ver_node = {
    "id": "FIN_VER_v5_5",
    "type": "version",
    "label": "FIN v5.5 - Full May HF 5.13 PDF import",
    "date": "2026-05-14",
    "source": "HF_5.13_PDF (OCR'd by Y)",
    "notes": "导入5月全月31天HF数据：12天实绩+19天预测",
    "entity_count": len(entities),
    "relation_count": len(rels)
}
entities.append(ver_node)

fin["entities"] = entities
fin["relationships"] = rels
if edges:
    fin["edges"] = edges

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print(f"\n写入完成!")
print(f"  实体: {len(entities)} | 关系: {len(rels)}")
print(f"  版本: FIN v5.5")
