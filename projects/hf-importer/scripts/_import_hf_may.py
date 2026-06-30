"""Import 5月 HF v7 (History & Forecast) data into FIN graph (entities/relationships format)"""
import json, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

FIN_GRAPH = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json")
BACKUP = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\backup_20260510_hf_may_v7.json")
FIN_README = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\_FIN_README.md")

# ── Data from PDF extracted 2026-05-10 ──
# Fields: day, dow, total_occ, arr, comp, hu, ded_indiv, nd_indiv, ded_grp, nd_grp,
#         occ_pct, rev, adr, dep, du, noshow, ooo, alc
DAYS = [
    # History (5/1-5/8, shaded = actual)
    (1, "Fri", 438, 286, 0, 2, 390, 0, 48, 0, 81.04, 350321.40, 803.49, 90, 0, 0, 3, 888),
    (2, "Sat", 491, 272, 2, 2, 442, 0, 49, 0, 90.89, 463916.27, 948.70, 219, 1, 1, 5, 1002),
    (3, "Sun", 465, 260, 4, 2, 415, 0, 50, 0, 86.06, 450831.29, 973.72, 286, 1, 1, 3, 901),
    (4, "Mon", 330, 203, 0, 2, 324, 0, 6, 0, 60.97, 240250.93, 732.47, 338, 2, 1, 5, 614),
    (5, "Tue", 147, 51, 0, 2, 147, 0, 0, 0, 26.95, 85628.43, 590.54, 234, 0, 2, 5, 208),
    (6, "Wed", 258, 145, 0, 2, 253, 0, 5, 0, 47.58, 149866.48, 585.42, 34, 0, 5, 4, 340),
    (7, "Thu", 514, 349, 0, 2, 336, 0, 178, 0, 95.17, 318575.69, 622.22, 93, 4, 3, 5, 639),
    (8, "Fri", 464, 143, 0, 2, 318, 0, 146, 0, 85.87, 279566.21, 605.12, 193, 3, 3, 4, 602),
    # Forecast (5/9-5/31, white = prediction)
    (9, "Sat", 231, 104, 3, 2, 224, 0, 7, 0, 42.57, 129598.44, 565.93, 341, 0, 3, 3, 323),
    (10, "Sun", 213, 91, 0, 2, 200, 0, 13, 0, 39.22, 118345.25, 560.88, 107, 0, 3, 3, 265),
    (11, "Mon", 324, 143, 0, 2, 293, 0, 31, 0, 59.85, 179504.18, 557.47, 32, 0, 3, 3, 376),
    (12, "Tue", 326, 73, 0, 2, 295, 0, 31, 0, 60.22, 182781.66, 564.14, 69, 0, 3, 3, 371),
    (13, "Wed", 341, 63, 0, 2, 279, 0, 62, 0, 63.01, 186609.19, 550.47, 82, 0, 3, 3, 381),
    (14, "Thu", 285, 45, 0, 2, 235, 0, 50, 0, 52.60, 158144.47, 558.81, 104, 0, 3, 3, 329),
    (15, "Fri", 302, 57, 0, 2, 200, 0, 102, 0, 55.76, 172154.13, 573.85, 103, 0, 3, 3, 348),
    (16, "Sat", 379, 222, 0, 2, 364, 0, 15, 0, 70.07, 320624.03, 850.46, 58, 0, 3, 3, 597),
    (17, "Sun", 248, 108, 0, 2, 248, 0, 0, 0, 45.72, 163630.60, 665.17, 226, 0, 3, 3, 364),
    (18, "Mon", 159, 35, 0, 2, 157, 0, 2, 0, 29.18, 97309.03, 619.80, 124, 0, 2, 2, 186),
    (19, "Tue", 186, 38, 0, 5, 183, 0, 3, 0, 33.64, 112782.95, 623.11, 11, 0, 2, 2, 212),
    (20, "Wed", 178, 21, 0, 2, 174, 0, 4, 0, 32.71, 108013.63, 613.71, 29, 0, 2, 2, 203),
    (21, "Thu", 188, 42, 0, 2, 167, 0, 21, 0, 34.57, 118794.46, 638.68, 32, 0, 2, 2, 211),
    (22, "Fri", 140, 10, 0, 2, 120, 0, 20, 0, 25.65, 90600.62, 656.53, 58, 0, 2, 2, 166),
    (23, "Sat", 124, 34, 0, 2, 122, 0, 2, 0, 22.68, 74906.65, 613.99, 50, 0, 2, 2, 166),
    (24, "Sun", 118, 29, 1, 2, 114, 0, 4, 0, 21.56, 61750.32, 532.33, 39, 0, 2, 2, 145),
    (25, "Mon", 128, 33, 0, 2, 122, 0, 6, 0, 23.42, 67330.78, 534.37, 25, 0, 2, 2, 151),
    (26, "Tue", 141, 21, 0, 2, 131, 0, 10, 0, 25.84, 74836.92, 538.40, 12, 0, 2, 2, 163),
    (27, "Wed", 186, 9, 0, 2, 115, 0, 71, 0, 34.20, 94717.72, 514.77, 25, 0, 2, 2, 210),
    (28, "Thu", 183, 11, 0, 2, 112, 0, 71, 0, 33.64, 95106.65, 525.45, 14, 0, 2, 2, 209),
    (29, "Fri", 188, 37, 0, 2, 112, 0, 76, 0, 34.57, 98226.74, 528.10, 37, 0, 2, 2, 237),
    (30, "Sat", 204, 37, 0, 2, 113, 0, 91, 0, 37.55, 107688.74, 533.11, 36, 0, 2, 2, 252),
    (31, "Sun", 200, 31, 0, 2, 95, 0, 105, 0, 36.80, 103772.51, 524.10, 49, 0, 2, 2, 224),
]

# ── Load existing graph ──
with open(FIN_GRAPH, "r", encoding="utf-8") as f:
    graph = json.load(f)

entities = graph["entities"]
relationships = graph["relationships"]

meta = graph.get("meta", {})
meta["version"] = "5.2"
meta["updated"] = "2026-05-10"

# Backup
shutil.copy(FIN_GRAPH, BACKUP)
print(f"✅ Backup saved to {BACKUP}")

# ── Report ID ──
REPORT_ID = "report_5_7_HF"
exists = any(e["id"] == REPORT_ID for e in entities)

def exists_entity(eid):
    return any(e["id"] == eid for e in entities)

def exists_rel(rid):
    return any(r.get("id") == rid for r in relationships)

if not exists:
    # Create the HF report entity
    entities.append({
        "id": REPORT_ID,
        "name": "History_Forecast_5.7_HF",
        "type": "fin_report",
        "date": "2026-05-10",
        "properties": {
            "report_label": "5.7_HF",
            "hotel": "Hilton Suzhou",
            "header_date": "2026-05-10",
            "filter_from": "2026-05-01",
            "filter_to": "2026-05-31",
            "data_source": "History_Forecast_PDF",
            "source_file": "History_and_Forecast_7.pdf",
            "history_occ_pct": 71.82,
            "history_revenue": 2338956.70,
            "history_adr": 756.70,
            "history_subtotal": 3107,
            "forecast_occ_pct": 39.79,
            "forecast_revenue": 2917229.67,
            "forecast_adr": 592.57,
            "forecast_subtotal": 4972,
            "total_occ": 8079,
            "total_revenue": 5256186.37,
            "total_adr": 655.88,
            "total_occ_pct": 48.05,
            "generated_at": "2026-05-09 19:56",
            "imported_at": "2026-05-10"
        },
        "outlet": None,
        "hotel_name": None,
        "period": "2026-05"
    })
    print(f"✅ Created {REPORT_ID} (v7 HF report)")
else:
    print(f"ℹ️  {REPORT_ID} already exists, updating")
    for e in entities:
        if e["id"] == REPORT_ID:
            e["properties"]["history_occ_pct"] = 71.82
            e["properties"]["history_revenue"] = 2338956.70
            e["properties"]["forecast_occ_pct"] = 39.79
            e["properties"]["forecast_revenue"] = 2917229.67
            e["properties"]["source_file"] = "History_and_Forecast_7.pdf"
            e["properties"]["imported_at"] = "2026-05-10"
            break

# ── Create daily entities ──
created = 0
updated = 0
for d in DAYS:
    day, dow, total_occ, arr, comp, hu, ded_indiv, nd_indiv, ded_grp, nd_grp, occ_pct, rev, adr, dep, du, noshow, ooo, alc = d
    
    is_history = day <= 8
    etype = "fin_daily" if is_history else "fin_forecast"
    eid = f"{REPORT_ID}_day_2026-05-{day:02d}_{'history' if is_history else 'forecast'}_{dow}"
    
    props = {
        "date": f"2026-05-{day:02d}",
        "day_of_week": dow,
        "total_occ": total_occ,
        "arr_rooms": arr,
        "comp_rooms": comp,
        "house_use": hu,
        "deduct_indiv": ded_indiv,
        "nondeduct_indiv": nd_indiv,
        "deduct_group": ded_grp,
        "nondeduct_group": nd_grp,
        "occ_pct": occ_pct,
        "revenue": rev,
        "adr": adr,
        "dep": dep,
        "day_use": du,
        "noshow": noshow,
        "ooo": ooo,
        "adult_child": alc
    }
    
    if exists_entity(eid):
        for e in entities:
            if e["id"] == eid:
                e["properties"].update(props)
                break
        updated += 1
    else:
        entities.append({
            "id": eid,
            "name": f"2026-05-{day:02d} 5.7_HF {'history' if is_history else 'forecast'}",
            "type": etype,
            "date": f"2026-05-{day:02d}",
            "properties": props,
            "outlet": None,
            "hotel_name": None,
            "period": "2026-05"
        })
        created += 1
    
    # Relationship: day -> report
    rel_id = f"REL_{eid}_belongs_to_{REPORT_ID}"
    if not exists_rel(rel_id):
        relationships.append({
            "source_id": eid,
            "target_id": REPORT_ID,
            "relation": "BELONGS_TO",
            "id": rel_id,
            "type": "BELONGS_TO",
            "source": eid,
            "target": REPORT_ID
        })

# ── Link to FIN_YEAR_2026 ──
FIN_YEAR = "FIN_YEAR_2026"
if not exists_entity(FIN_YEAR):
    entities.append({
        "id": FIN_YEAR,
        "name": "2026年财务年度",
        "type": "fin_year",
        "date": "2026",
        "properties": {"year": 2026}
    })

rel_report_to_year = f"REL_{REPORT_ID}_belongs_to_{FIN_YEAR}"
if not exists_rel(rel_report_to_year):
    relationships.append({
        "source_id": REPORT_ID,
        "target_id": FIN_YEAR,
        "relation": "BELONGS_TO",
        "id": rel_report_to_year,
        "type": "BELONGS_TO",
        "source": REPORT_ID,
        "target": FIN_YEAR
    })

# ── Link to previous 5.8_DRR report ──
OLD_REPORT = "report_5_8_DRR"
if exists_entity(OLD_REPORT):
    rel_compare = f"REL_{REPORT_ID}_updated_from_{OLD_REPORT}"
    if not exists_rel(rel_compare):
        relationships.append({
            "source_id": REPORT_ID,
            "target_id": OLD_REPORT,
            "relation": "UPDATED_FROM",
            "id": rel_compare,
            "type": "UPDATED_FROM",
            "source": REPORT_ID,
            "target": OLD_REPORT
        })
        print(f"✅ Linked to previous report: {OLD_REPORT}")

# ── Save ──
with open(FIN_GRAPH, "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

# ── Update README ──
print(f"\n{'='*50}")
print(f"📊 FIN Graph Update Complete")
print(f"{'='*50}")
print(f"  Report: {REPORT_ID} (History & Forecast v7)")
print(f"  Entities: {len(entities)} (+{created} new, {updated} updated)")
print(f"  Relationships: {len(relationships)}")
print(f"  Version: {meta['version']} (was 5.1)")
print(f"\n📋 Data Summary:")
print(f"  History (5/1-5/8): 71.82% Occ / ¥2,338,957 Rev / ¥756.70 ADR")
print(f"  Forecast (5/9-5/31): 39.79% Occ / ¥2,917,230 Rev / ¥592.57 ADR")
print(f"  Total May: 48.05% Occ / ¥5,256,186 Rev / ¥655.88 ADR")
print(f"\n🔗 Now linked to: {FIN_YEAR}")
if exists_entity(OLD_REPORT):
    print(f"   Previous: {OLD_REPORT} (comparison edge added)")
