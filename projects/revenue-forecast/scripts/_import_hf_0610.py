#!/usr/bin/env python3
"""2026-06-11: Import History and Forecast 6.10 into FIN station.
   Source file: History_and_Forecast_6.10---1e3a974a-a420-4caa-a3a7-fc86e441e470.pdf
   Generated: 2026-06-10 19:55 (Oracle Reports)
"""
import json, shutil

FP = r'knowledge_center\fin_graph.json'
BACKUP = r'knowledge_center\fin_graph_pre_0610_hf.json'

# ---- Step 1: Backup ----
shutil.copy2(FP, BACKUP)
print(f"Backup saved: {BACKUP}")

with open(FP, 'r', encoding='utf-8') as f:
    g = json.load(f)

entities = g['entities']

# ---- Step 2: Data from H&F 6.10 PDF (extracted 2026-06-11) ----
# Generated: 2026-06-10 19:55 | Hotel: Hotel-A | Source: Oracle Reports

HISTORY_DAYS = [
    # date, dow, arr, occ, comp, hu, deduct_indiv, nondeduct_indiv, deduct_group, nondeduct_group, occ_pct, rev, adr, dep, du, ns, ooo, chl
    ("2026-06-01", "Mon", 290, 158, 0, 12, 286, 0, 4, 0, 51.67, 146623.27, 527.42, 197, 0, 4, 11, 371),
    ("2026-06-02", "Tue", 326, 147, 3, 2, 326, 0, 0, 0, 60.22, 174119.88, 537.41, 111, 2, 3, 12, 416),
    ("2026-06-03", "Wed", 400, 205, 0, 2, 356, 0, 44, 0, 73.98, 208799.79, 524.62, 131, 1, 4, 9, 522),
    ("2026-06-04", "Thu", 384, 210, 1, 2, 375, 0, 9, 0, 71.00, 205732.43, 538.57, 226, 4, 1, 5, 474),
    ("2026-06-05", "Fri", 246, 114, 0, 2, 236, 0, 10, 0, 45.35, 136710.40, 560.29, 252, 0, 2, 7, 340),
    ("2026-06-06", "Sat", 285, 170, 0, 2, 270, 0, 15, 0, 52.60, 157477.51, 556.46, 131, 3, 1, 8, 442),
    ("2026-06-07", "Sun", 227, 100, 0, 2, 214, 0, 13, 0, 41.82, 125112.59, 556.06, 158, 0, 1, 7, 307),
    ("2026-06-08", "Mon", 326, 175, 0, 3, 326, 0, 0, 0, 60.04, 174470.98, 540.16, 76, 0, 1, 7, 414),
    ("2026-06-09", "Tue", 375, 171, 0, 3, 375, 0, 0, 0, 69.14, 203331.15, 546.59, 122, 0, 2, 8, 471),
]

FORECAST_DAYS = [
    ("2026-06-10", "Wed", 415, 197, 2, 3, 385, 0, 30, 0, 76.58, 218887.96, 531.28, 158, 0, 0, 9, 516),
    ("2026-06-11", "Thu", 414, 199, 1, 3, 326, 0, 88, 0, 76.39, 215497.43, 524.32, 200, 0, 0, 9, 476),
    ("2026-06-12", "Fri", 375, 106, 1, 2, 239, 0, 136, 0, 69.33, 191909.78, 514.50, 184, 0, 0, 7, 438),
    ("2026-06-13", "Sat", 278, 58, 0, 2, 199, 0, 79, 0, 51.30, 146695.46, 531.51, 143, 0, 0, 4, 336),
    ("2026-06-14", "Sun", 182, 63, 0, 2, 181, 0, 1, 0, 33.46, 95842.62, 532.46, 133, 0, 0, 4, 219),
    ("2026-06-15", "Mon", 229, 80, 0, 2, 229, 0, 0, 0, 42.19, 119989.92, 528.59, 32, 0, 0, 4, 272),
    ("2026-06-16", "Tue", 210, 34, 0, 2, 210, 0, 0, 0, 38.66, 110546.66, 531.47, 53, 0, 0, 4, 247),
    ("2026-06-17", "Wed", 183, 26, 0, 2, 183, 0, 0, 0, 33.64, 97704.69, 539.80, 53, 0, 0, 3, 216),
    ("2026-06-18", "Thu", 154, 26, 0, 2, 154, 0, 0, 0, 28.25, 83344.40, 548.32, 55, 0, 0, 3, 184),
    ("2026-06-19", "Fri", 173, 58, 0, 2, 173, 0, 0, 0, 31.78, 100634.68, 588.51, 39, 0, 0, 3, 229),
    ("2026-06-20", "Sat", 198, 74, 0, 2, 194, 0, 4, 0, 36.43, 115738.04, 590.50, 49, 0, 0, 3, 279),
    ("2026-06-21", "Sun", 140, 34, 0, 2, 128, 0, 12, 0, 25.65, 71207.89, 516.00, 92, 0, 0, 3, 166),
    ("2026-06-22", "Mon", 158, 27, 0, 2, 146, 0, 12, 0, 29.00, 79944.08, 512.46, 9, 0, 0, 3, 181),
    ("2026-06-23", "Tue", 171, 25, 0, 2, 159, 0, 12, 0, 31.41, 86878.52, 514.07, 12, 0, 0, 3, 196),
    ("2026-06-24", "Wed", 168, 26, 0, 2, 156, 0, 12, 0, 30.86, 87537.44, 527.33, 29, 1, 0, 3, 196),
    ("2026-06-25", "Thu", 142, 19, 0, 2, 142, 0, 0, 0, 26.02, 74630.21, 533.07, 45, 0, 0, 3, 170),
    ("2026-06-26", "Fri", 142, 42, 0, 2, 142, 0, 0, 0, 26.02, 77948.52, 556.78, 42, 0, 0, 3, 192),
    ("2026-06-27", "Sat", 219, 104, 0, 2, 219, 0, 0, 0, 40.33, 132633.36, 611.21, 27, 0, 0, 3, 339),
    ("2026-06-28", "Sun", 104, 10, 0, 2, 104, 0, 0, 0, 18.96, 54047.17, 529.87, 125, 0, 0, 3, 126),
    ("2026-06-29", "Mon", 112, 22, 0, 2, 112, 0, 0, 0, 20.45, 58296.70, 529.97, 14, 0, 0, 3, 133),
    ("2026-06-30", "Tue", 122, 19, 0, 1, 106, 0, 16, 0, 22.49, 65847.27, 544.19, 25, 0, 0, 3, 138),
]

# ---- Step 3: Remove old HF_20260609 report entity ----
entities = [e for e in entities if e.get('id') != 'HF_20260609']

# Remove old HF_DAY_202606* nodes (from 6.9 version)
entities = [e for e in entities if not e.get('id', '').startswith('HF_DAY_202606')]

# ---- Step 4: Create new HF report entity ----
HF_REPORT = {
    "id": "HF_20260610",
    "type": "hf_report",
    "generated": "2026-06-10 19:55",
    "period": "2026-06-01 to 2026-06-30",
    "history_days": 9,
    "forecast_days": 21,
    "history_occ_pct": 58.43,
    "history_adr": 541.67,
    "history_revenue": 1532378.00,
    "history_rooms_sold": 2859,
    "forecast_occ_pct": 37.58,
    "forecast_adr": 538.33,
    "forecast_revenue": 2285762.80,
    "forecast_rooms_sold": 4289,
    "total_occ_pct": 43.84,
    "total_room_rev": 3818140.80,
    "avg_rate": 539.67,
    "total_arrivals": 7148,
    "dep_use": 2923,
    "no_show": 11,
    "ooo_total": 19,
    "source": "History_and_Forecast_6.10.pdf"
}
entities.append(HF_REPORT)

# ---- Step 5: Create daily HF_DAY nodes ----
def build_hf_day(date_str, dow, arr, occ, comp, hu, deduct_indiv, nondeduct_indiv, deduct_group, nondeduct_group, occ_pct, rev, adr, dep, du, ns, ooo, chl):
    hid = f"HF_DAY_{date_str.replace('-', '')}"
    return {
        "id": hid,
        "type": "hf_day",
        "date": date_str,
        "dow": dow,
        "arrivals": arr,
        "occupied": occ,
        "comp": comp,
        "house_use": hu,
        "deduct_indiv": deduct_indiv,
        "nondeduct_indiv": nondeduct_indiv,
        "deduct_group": deduct_group,
        "nondeduct_group": nondeduct_group,
        "occ_pct": occ_pct,
        "room_revenue": rev,
        "average_rate": adr,
        "departures": dep,
        "day_use": du,
        "no_show": ns,
        "ooo": ooo,
        "children": chl,
        "source": "HF_20260610"
    }

for day_data in HISTORY_DAYS + FORECAST_DAYS:
    entities.append(build_hf_day(*day_data))

# ---- Step 6: Meta update ----
g['meta']['version'] = 'v9.0'
g['meta']['updated'] = '2026-06-11 09:30'
g['meta']['description'] = 'v8.3 + HF_20260610 (History 6/1-9 + Forecast 6/10-30, replaced old HF_20260609)'

# ---- Step 7: Save ----
g['entities'] = entities
with open(FP, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\n=== H&F 6.10 导入完成 ===")
print(f"源文件: History_and_Forecast_6.10.pdf (2026-06-10 19:55)")
print(f"HF报告: HF_20260610")
print(f"HF天数据: {len(HISTORY_DAYS) + len(FORECAST_DAYS)} 天")
print(f"  历史 ({len(HISTORY_DAYS)}天): Occ 58.43% | ADR 541.67 | Rev {1532378:,.0f} (CNY) | Rooms 2,859")
print(f"  预报 ({len(FORECAST_DAYS)}天): Occ 37.58% | ADR 538.33 | Rev {2285763:,.0f} (CNY) | Rooms 4,289")
print(f"  全月: Occ 43.84% | ADR 539.67 | Rev {3818141:,.0f} (CNY) | Rooms 7,148")
print(f"当前FIN站总计: 实体{len(g['entities'])} / 关系{len(g.get('relations', []))}")
print(f"版本: v9.0")
