# -*- coding: utf-8 -*-
import json

with open("fin_graph.json", encoding="utf-8") as f:
    fin = json.load(f)

ents = fin["entities"]
rels = fin["relationships"]

# 实体ID前缀 → 类型映射
PREFIX_TYPE = {
    "W": "competition_data",
    "PP": "competition_data",
    "CP": "competition_data",
    "PARK": "competition_data",
    "ICI": "other_hotel_product",
    "PNL": "pnl_statement",
    "HLT": "promotion_product",
    "COMP": "competition_data",
    "DRR": "drr_report",
    "REV": "revenue_summary",
    "OUT": "outlet",
    "PLATFORM": "delivery_platform",
    "DELIVERY": "delivery_monthly",
    "MENU": "menu_item",
    "BUDGET": "budget",
    "FINANCIAL": "FINANCIAL",
    "HU": "fin_kpi",
}

ent_fix = 0
for e in ents:
    t = e.get("type") or ""
    if t.strip():
        continue
    pid = e["id"].split("_")[0]
    if pid in PREFIX_TYPE:
        e["type"] = PREFIX_TYPE[pid]
        ent_fix += 1

rel_fix = 0
for r in rels:
    t = r.get("type") or ""
    if t.strip():
        continue
    src = r.get("source", "")
    tgt = r.get("target", "")
    src_t = next((x.get("type", "?") for x in ents if x["id"] == src), "?")
    tgt_t = next((x.get("type", "?") for x in ents if x["id"] == tgt), "?")

    # 关系类型规则
    if (src_t, tgt_t) == ("promotion_product", "competition_data") or \
       (src_t, tgt_t) == ("competition_data", "promotion_product") or \
       (src_t, tgt_t) == ("competition_data", "competition_data"):
        r["type"] = "COMPETES_WITH"
    elif (src_t, tgt_t) in [("promotion_product", "promotion_product"),
                            ("other_hotel_product", "other_hotel_product")]:
        r["type"] = "RELATES_TO"
    elif src_t == "promotion_product" and "HOTEL_MAIN" in tgt:
        r["type"] = "OFFERED_AT"
    elif tgt_t == "outlet" or "OUTLET" in tgt:
        r["type"] = "LOCATED_AT"
    elif src_t == "daily_revenue":
        if tgt_t == "revenue_summary":
            r["type"] = "CONTRIBUTES_TO"
        elif tgt_t == "outlet_revenue":
            r["type"] = "AGGREGATES_INTO"
        elif tgt_t == "date":
            r["type"] = "FOR_DATE"
        elif tgt_t == "budget":
            r["type"] = "AGAINST_BUDGET"
        elif tgt_t == "fb_daily_total":
            r["type"] = "PART_OF"
        else:
            r["type"] = "RELATES_TO"
    elif src_t == "outlet_revenue" and tgt_t == "revenue_period":
        r["type"] = "IN_PERIOD"
    elif src_t == "fnb_daily_total" and tgt_t == "revenue_period":
        r["type"] = "COVERS"
    elif src_t == "date" and tgt_t == "date":
        r["type"] = "NEXT_DATE"
    elif src_t == "delivery_monthly" and tgt_t == "outlet":
        r["type"] = "AT_OUTLET"
    elif src_t == "promotion_product":
        r["type"] = "OFFERED_AT"
    elif src_t == "budget" and tgt_t == "daily_revenue":
        r["type"] = "BUDGET_FOR"
    elif src_t == "FINANCIAL" and tgt_t == "daily_revenue":
        r["type"] = "HAS_DATA"
    else:
        r["type"] = "RELATES_TO"

    if "properties" not in r:
        r["properties"] = {}
    rel_fix += 1

# 保存
with open("fin_graph.json", "w", encoding="utf-8") as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print("FIN站标注完成")
print("  实体type补齐: %d个" % ent_fix)
print("  关系type标注: %d条" % rel_fix)
print("  总实体: %d, 总关系: %d" % (len(ents), len(rels)))

# 验证空type清零
empty_rel = sum(1 for r in rels if not r.get("type") or not r.get("type").strip())
print("  剩余空type关系: %d（应为0）" % empty_rel)

empty_ent = sum(1 for e in ents if not e.get("type") or not e.get("type").strip())
print("  剩余空type实体: %d（应为0）" % empty_ent)
