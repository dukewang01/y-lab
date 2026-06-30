"""2026-06-18: Import History & Forecast (6月全�? into FIN station"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

FIN_GRAPH = r'C:\Users\Y\.openclaw\workspace\knowledge_center\fin_graph.json'
with open(FIN_GRAPH, 'r', encoding='utf-8') as f:
    fin = json.load(f)

existing_ids = set(e.get("id", "") for e in fin["entities"])

# ===== History Data (June 1-17 actuals) =====
history_days = [
    {"date":"2026-06-01","dow":"Mon","arr":158,"rooms_sold":290,"occ":51.67,"revenue":146623.27,"adr":527.42,"dep":197,"avail":371},
    {"date":"2026-06-02","dow":"Tue","arr":147,"rooms_sold":326,"occ":60.22,"revenue":174119.88,"adr":537.41,"dep":111,"avail":416},
    {"date":"2026-06-03","dow":"Wed","arr":205,"rooms_sold":400,"occ":73.98,"revenue":208799.79,"adr":524.62,"dep":131,"avail":522},
    {"date":"2026-06-04","dow":"Thu","arr":210,"rooms_sold":384,"occ":71.00,"revenue":205732.43,"adr":538.57,"dep":226,"avail":474},
    {"date":"2026-06-05","dow":"Fri","arr":114,"rooms_sold":246,"occ":45.35,"revenue":136710.40,"adr":560.29,"dep":252,"avail":340},
    {"date":"2026-06-06","dow":"Sat","arr":170,"rooms_sold":285,"occ":52.60,"revenue":157477.51,"adr":556.46,"dep":131,"avail":442},
    {"date":"2026-06-07","dow":"Sun","arr":100,"rooms_sold":227,"occ":41.82,"revenue":125112.59,"adr":556.06,"dep":158,"avail":307},
    {"date":"2026-06-08","dow":"Mon","arr":175,"rooms_sold":326,"occ":60.04,"revenue":174470.98,"adr":540.16,"dep":76,"avail":414},
    {"date":"2026-06-09","dow":"Tue","arr":171,"rooms_sold":375,"occ":69.14,"revenue":203331.15,"adr":546.59,"dep":122,"avail":471},
    {"date":"2026-06-10","dow":"Wed","arr":200,"rooms_sold":417,"occ":76.95,"revenue":222890.73,"adr":538.38,"dep":158,"avail":525},
    {"date":"2026-06-11","dow":"Thu","arr":273,"rooms_sold":488,"occ":90.15,"revenue":256497.48,"adr":528.86,"dep":202,"avail":607},
    {"date":"2026-06-12","dow":"Fri","arr":239,"rooms_sold":473,"occ":87.55,"revenue":245511.44,"adr":521.26,"dep":254,"avail":626},
    {"date":"2026-06-13","dow":"Sat","arr":188,"rooms_sold":400,"occ":73.98,"revenue":215796.91,"adr":542.20,"dep":261,"avail":611},
    {"date":"2026-06-14","dow":"Sun","arr":125,"rooms_sold":260,"occ":47.96,"revenue":138661.15,"adr":537.45,"dep":265,"avail":354},
    {"date":"2026-06-15","dow":"Mon","arr":194,"rooms_sold":380,"occ":70.26,"revenue":199376.16,"adr":527.45,"dep":74,"avail":486},
    {"date":"2026-06-16","dow":"Tue","arr":173,"rooms_sold":395,"occ":73.05,"revenue":208195.43,"adr":529.76,"dep":158,"avail":492},
    {"date":"2026-06-17","dow":"Wed","arr":166,"rooms_sold":393,"occ":72.68,"revenue":208869.32,"adr":534.19,"dep":168,"avail":488},
]

# ===== Forecast Data (June 18-30) =====
forecast_days = [
    {"date":"2026-06-18","dow":"Thu","arr":87,"rooms_sold":240,"occ":44.24,"revenue":133539.47,"adr":561.09,"dep":242,"avail":326},
    {"date":"2026-06-19","dow":"Fri","arr":107,"rooms_sold":255,"occ":47.03,"revenue":150615.44,"adr":595.32,"dep":92,"avail":383},
    {"date":"2026-06-20","dow":"Sat","arr":107,"rooms_sold":270,"occ":49.81,"revenue":158488.11,"adr":591.37,"dep":92,"avail":406},
    {"date":"2026-06-21","dow":"Sun","arr":53,"rooms_sold":174,"occ":31.97,"revenue":89200.89,"adr":518.61,"dep":149,"avail":211},
    {"date":"2026-06-22","dow":"Mon","arr":81,"rooms_sold":304,"occ":56.13,"revenue":146716.25,"adr":485.82,"dep":23,"avail":334},
    {"date":"2026-06-23","dow":"Tue","arr":42,"rooms_sold":313,"occ":57.81,"revenue":152972.60,"adr":491.87,"dep":29,"avail":345},
    {"date":"2026-06-24","dow":"Wed","arr":50,"rooms_sold":306,"occ":56.51,"revenue":154064.39,"adr":506.79,"dep":49,"avail":342},
    {"date":"2026-06-25","dow":"Thu","arr":32,"rooms_sold":237,"occ":43.68,"revenue":122175.61,"adr":519.90,"dep":66,"avail":267},
    {"date":"2026-06-26","dow":"Fri","arr":65,"rooms_sold":190,"occ":34.94,"revenue":102257.43,"adr":543.92,"dep":87,"avail":239},
    {"date":"2026-06-27","dow":"Sat","arr":118,"rooms_sold":263,"occ":48.51,"revenue":155956.08,"adr":597.53,"dep":55,"avail":390},
    {"date":"2026-06-28","dow":"Sun","arr":26,"rooms_sold":145,"occ":26.58,"revenue":73881.36,"adr":516.65,"dep":134,"avail":176},
    {"date":"2026-06-29","dow":"Mon","arr":37,"rooms_sold":159,"occ":29.18,"revenue":81935.76,"adr":521.88,"dep":23,"avail":187},
    {"date":"2026-06-30","dow":"Tue","arr":28,"rooms_sold":162,"occ":29.93,"revenue":87541.50,"adr":543.74,"dep":46,"avail":183},
]

# Create HF Report entity
hf_id = "HF_REPORT_20260618"
if hf_id not in existing_ids:
    hf_report = {
        "id": hf_id,
        "type": "hf_report",
        "date": "2026-06-18",
        "period": "2026-06-01 to 2026-06-30",
        "total_history_rooms": 6065,
        "total_history_occ": 65.79,
        "total_history_revenue": 3228176.62,
        "total_history_adr": 536.51,
        "total_forecast_rooms": 3018,
        "total_forecast_occ": 42.79,
        "total_forecast_revenue": 1609344.89,
        "total_forecast_adr": 537.70,
        "total_month_rooms": 9083,
        "total_month_occ": 55.82,
        "total_month_revenue": 4837521.51,
        "total_month_adr": 536.91,
        "source_file": "History_and_Forecast_15.pdf"
    }
    fin["entities"].append(hf_report)
    print(f"  [ADD] {hf_id}")

# Create daily records for history days
history_added = 0
for d in history_days:
    day_id = f"HF_DAY_{d['date']}"
    if day_id not in existing_ids:
        ent = {
            "id": day_id,
            "type": "hf_daily",
            "date": d["date"],
            "dow": d["dow"],
            "arrivals": d["arr"],
            "rooms_sold": d["rooms_sold"],
            "occupancy_pct": d["occ"],
            "room_revenue": d["revenue"],
            "adr": d["adr"],
            "departures": d["dep"],
            "available": d["avail"],
            "data_type": "history",
            "source_file": "History_and_Forecast_15.pdf"
        }
        fin["entities"].append(ent)
        history_added += 1

# Create daily records for forecast days
forecast_added = 0
for d in forecast_days:
    day_id = f"HF_DAY_{d['date']}"
    if day_id not in existing_ids:
        ent = {
            "id": day_id,
            "type": "hf_daily",
            "date": d["date"],
            "dow": d["dow"],
            "arrivals": d["arr"],
            "rooms_sold": d["rooms_sold"],
            "occupancy_pct": d["occ"],
            "room_revenue": d["revenue"],
            "adr": d["adr"],
            "departures": d["dep"],
            "available": d["avail"],
            "data_type": "forecast",
            "source_file": "History_and_Forecast_15.pdf"
        }
        fin["entities"].append(ent)
        forecast_added += 1

# Update meta
fin["meta"]["version"] = "v8.14"
fin["meta"]["updated"] = "2026-06-18 20:40"
fin["meta"]["description"] = "v8.13 + History & Forecast (6月全�?0天数�?"

with open(FIN_GRAPH, 'w', encoding='utf-8') as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print(f"\nFIN�?History & Forecast 导入完成!")
print(f"  新增HF报告: 1 + 历史�? {history_added} + 预测�? {forecast_added} = {1+history_added+forecast_added}实体")
print(f"  FIN站总计: {len(fin['entities'])}实体 / {len(fin['relations'])}关系 / {fin['meta']['version']}")
print(f"\n📊 6月实�?1-17�?: 6,065�?| Occ 65.79% | Rev ¥322.8�?| ADR ¥536.51")
print(f"📊 6月预�?18-30�?: 3,018�?| Occ 42.79% | Rev ¥160.9�?| ADR ¥537.70")
print(f"📊 6月全月合�?     9,083�?| Occ 55.82% | Rev ¥483.8�?| ADR ¥536.91")
