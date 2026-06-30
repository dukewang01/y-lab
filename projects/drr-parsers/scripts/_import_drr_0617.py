"""2026-06-18: Import DRR 2026.06.17 data into FIN station"""
import json, os

fp = r'C:\Users\Y\.openclaw\workspace\knowledge_center\fin_graph.json'
g = json.load(open(fp, 'r', encoding='utf-8'))

DRR_DATE = "2026-06-17"
EXISTING_IDS = set(e.get("id", "") for e in g["entities"])

# ===== Core Room Data (from DRR Actual sheet, 2026.06.17) =====
room_data = {
    "room_sold": 389,
    "complimentary": 2,
    "house_use": 2,
    "out_of_order": 5,
    "out_of_service": 6,
    "vacant": 134,
    "available": 538,
    "occupancy_pct": 0.723,
    "revpar": 429.38,
    "arr": 593.85,
    "guest_count": 483,
    "total_rooms_revenue": 208345.93,
    "other_income": 1659.90,
    "service_charge": 21000.63,
    "net_room_revenue": 231006.46,
    "condo_room_sold": 29,
    "condo_net_room_revenue": 15017.53,
    "condo_arr": 517.85,
}

# ===== F&B Data (from DRR Actual sheet) =====
# Covers and avg_check from rows 34-50
banquet_covers = 34
banquet_revenue = 34 * 517.54  # avg_check * covers �?17596

fb_outlets = {
    "OPEN": {"covers": 410, "avg_check": 60.61},
    "YUXI": {"covers": 49, "avg_check": 278.23},
    "BACIO": {"covers": 12, "avg_check": 268.24},
    "BEER_SOCIETY": {"covers": 0, "avg_check": 0},
    "YUAN": {"covers": 1, "avg_check": 0},
    "FOOD_STORE": {"covers": 0, "avg_check": 0},
    "ROOM_SERVICE": {"covers": 10, "avg_check": 0},
    "MINI_BAR": {"covers": 0, "avg_check": 0},
}

# Calculate revenue from covers * avg_check where possible
# For now, I'll omit individual outlet revenues since Actual sheet doesn't show them directly
# We'd need Data sheet for detailed breakdown

total_fb_covers = 516  # from row 44
total_fb_revenue = None  # Not directly extracted, skip for now

# ===== Create Hotel Day Entity =====
hid = "HOTEL_DAY_20260617"
if hid not in EXISTING_IDS:
    hotel_day = {
        "id": hid,
        "type": "hotel_day",
        "date": DRR_DATE,
        "day_of_week": "Wednesday",
        "room_sold": room_data["room_sold"],
        "available": room_data["available"],
        "occupancy_pct": room_data["occupancy_pct"],
        "arr": room_data["arr"],
        "revpar": room_data["revpar"],
        "net_room_revenue": room_data["net_room_revenue"],
        "total_rooms_revenue": room_data["total_rooms_revenue"],
        "total_fb_covers": total_fb_covers,
        "guest_count": room_data["guest_count"],
        "source": "DRR_2026.06.17"
    }
    g["entities"].append(hotel_day)
    print(f"Added: {hid}")
else:
    print(f"Exists: {hid}")

# ===== Create DRR Entry Entity =====
did = "DRR_20260617"
if did not in EXISTING_IDS:
    drr = {
        "id": did,
        "type": "drr_entry",
        "date": DRR_DATE,
        "net_room_revenue": room_data["net_room_revenue"],
        "room_sold": room_data["room_sold"],
        "occupancy": room_data["occupancy_pct"],
        "arr": room_data["arr"],
        "revpar": room_data["revpar"],
        "total_fb_covers": total_fb_covers,
        "source": "DRR_2026.06.17"
    }
    g["entities"].append(drr)
    print(f"Added: {did}")
else:
    print(f"Exists: {did}")

# ===== Create F&B Outlet Stats =====
for outlet_name, data in fb_outlets.items():
    oid = f"FB_OUTLET_20260617_{outlet_name}"
    if oid not in EXISTING_IDS:
        entry = {
            "id": oid,
            "type": "fb_outlet_stats",
            "date": DRR_DATE,
            "outlet": outlet_name,
            "covers": data["covers"],
            "avg_check": data["avg_check"],
            "source": "DRR_2026.06.17"
        }
        g["entities"].append(entry)
        print(f"Added: {oid}")

# ===== Update meta =====
g["meta"]["version"] = "v8.13"
g["meta"]["updated"] = "2026-06-18 09:20"
g["meta"]["description"] = "v8.12 + DRR_2026.06.17 import (hotel_day + drr_entry + 8 fb_outlets)"

# Save
with open(fp, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print()
print("FIN站DRR导入完成!")
added = 0
if hid not in EXISTING_IDS: added += 1
if did not in EXISTING_IDS: added += 1
added += sum(1 for o in fb_outlets if f"FB_OUTLET_20260617_{o}" not in EXISTING_IDS)
print(f"  新增实体: {added}")
print(f"  当前FIN站总计: 实体{len(g['entities'])} / 关系{len(g['relations'])}")
print(f"  版本: v8.13")
