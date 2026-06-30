"""Import BEO version comparison (v1=4/26, v2=5/2, v3=5/10) into FIN graph"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

FIN_GRAPH = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json")
BACKUP = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\backup_20260510_beo_versions.json")

# ═══════════════════════════════════════════════════════
# Version metadata from PDF analysis
# ═══════════════════════════════════════════════════════

VERSIONS = {
    "BEO_V1_0426": {
        "name": "BEO Daily Event 4.26-6.30 (v1)",
        "report_date": "2026-04-26",
        "generated_by": "Elaine He",
        "filter_from": "2026-04-26",
        "filter_to": "2026-06-30",
        "total_events": 99,
        "source_file": "4.26-6.30Report.pdf"
    },
    "BEO_V2_0502": {
        "name": "BEO Daily Event 5.2-6.30 (v2)",
        "report_date": "2026-05-02",
        "generated_by": "Elaine He",
        "filter_from": "2026-05-02",
        "filter_to": "2026-06-30",
        "total_events": 105,
        "source_file": "5.2-6.30Report.pdf"
    },
    "BEO_V3_0510": {
        "name": "BEO Daily Event 5.10-6.30 (v3)",
        "report_date": "2026-05-10",
        "generated_by": "Elaine He",
        "filter_from": "2026-05-10",
        "filter_to": "2026-06-30",
        "total_events": 98,
        "source_file": "5.10-6.30Report.pdf"
    }
}

# ── Key event status changes tracked across versions ──
# Format: (eng_name, date, chn_name, v1_status, v2_status, v3_status, room, guests, note)
EVENT_TRACKING = [
    # ── 五一黄金周 events ──
    ("The Wedding of Mr. Yin and Ms. Wu", "2026-04-26", "殷晟&吴宇玮婚宴", "Definite", "N/A", "N/A", "Grand Ballroom", 400, "v1 only, 五一前"),
    ("The Wedding of Mr. Shen and Ms. Gao", "2026-05-02", "沈嘉程&高雨晨婚宴", "Definite", "Definite", "N/A", "Grand Ballroom", 250, "五一定单"),
    ("The Wedding of Mr, Li and Ms. Sun", "2026-05-03", "李杨&孙静媛婚宴", "Definite", "Definite", "N/A", "Grand Ballroom", 400, "五一定单"),
    ("JS Xinghua Ella Concert", "2026-05-03", "江苏星华Ella演唱会", "Definite", "Definite", "N/A", "Grand Ballroom 1+2", 75, "五一定单"),
    ("The Wedding of Mr. Xue and Ms. Yang", "2026-05-04", "薛文飞&杨凌栏婚宴", "Definite", "Definite", "N/A", "Grand Ballroom", 330, "五一定单"),
    ("Samsung Electronics Meeting", "2026-05-05", "三星电子会议", "Definite", "Definite", "N/A", "FR3+4/FR1", 60, "五一定单"),
    
    # ── 5/10 张辰炜婚宴 ──
    ("The Wedding of Mr. Zhang and Ms. Li", "2026-05-10", "张辰炜&李梦婷婚宴", "Prospect", "Prospect", "Definite", "Grand Ballroom", "190→200", "Prospect→Definite ✅"),
    
    # ── 5/11 中信银行 ──
    ("Citic Bank Meeting", "2026-05-11", "中信银行会议", "Tentative", "Tentative", "Definite", "FR3+4", 63, "Tentative→Definite"),
    
    # ── 5/12-14 三星半导体+斗山 ──
    ("Samsung Electronics Meeting", "2026-05-12", "三星半导体会议", "Definite", "Definite", "Definite", "FR1", 40, "三版不变"),
    ("Doosan meeting", "2026-05-12", "斗山会议", "Definite", "Definite", "Definite", "FR6", 40, "三版不变"),
    ("China Pacific Life Insurance", "2026-05-12", "太平人寿会议", "Prospect", "Prospect", "Tentative", "FR3+4/GB", "100→60", "缩水"),
    ("Thermo Fisher Meeting", "2026-05-12", "赛默飞会议", "Prospect", "Prospect", "消失", "FR", 50, "未成单 ❌"),
    
    # ── 5/16 附一院+陈逸凡 ──
    ("SZ First Affiliated Meeting", "2026-05-16", "苏州附一院结肠直外科会议", "Tentative", "Tentative", "Definite", "GB1/FR", 100, "追单成功 ✅"),
    ("The Wedding of Mr. Chen and Ms. Li", "2026-05-16", "陈逸凡&李妍婚宴", "Definite", "Definite", "Definite", "GB2+3", 140, "三版不变"),
    ("The Lunch of Mr.Cai", "2026-05-16", "蔡先生午宴", "Definite", "Definite", "Definite", "FR1", 50, "三版不变"),
    
    # ── 5/21 友邦 ──
    ("AIA Meeting & Dinner", "2026-05-21", "友邦表彰大会", "Tentative", "Tentative", "Tentative", "Grand Ballroom", "300→280", "保持Tentative"),
    
    # ── 5/23-24 婚宴集中 ──
    ("The Wedding of Mr.shen", "2026-05-23", "沈先生婚宴", "Definite", "Definite", "Definite", "GB2+3", 120, "三版不变"),
    ("The Wedding of Mr. Xu and Ms. Jin", "2026-05-24", "徐晟&金洋婚宴", "Definite", "Definite", "Definite", "GB2+3", 120, "三版不变"),
    
    # ── 5/26 韩国领事馆 ──
    ("Consulate general of Korea in Shanghai", "2026-05-26", "大韩民国驻上海领事馆", "Definite", "Definite", "Definite", "FR3+4", 60, "新单"),
    
    # ── 5/28-29 下旬 ──
    ("Zhongke Kandian Meeting", "2026-05-28", "中科看点活动", "Tentative", "Tentative", "保留", "GB3", 120, "保持Tentative"),
    ("SHA ZHINENG Guidao Group", "2026-05-29", "上海智能轨道交通", "Tentative", "Tentative", "Tentative", "Grand Ballroom", 500, "大单保持"),
    ("Nanjing Haiwei Meeting", "2026-05-29", "南京海维医药科技", "Definite", "Definite", "Definite", "FR3+4", 63, "三版Definite"),
    
    # ── 5/30 史品懿 ──
    ("The Wedding of Mr. Shi and Ms. Feng", "2026-05-30", "史品懿&冯铄涵婚宴", "Definite", "Definite", "Definite", "Grand Ballroom", 190, "三版Definite"),
    
    # ── 6月展望 ──
    ("The Wedding of Mr. Yu", "2026-06-05", "余意先生婚宴", "Definite", "Definite", "Definite", "Grand Ballroom", 250, "三版Definite"),
    ("Architectural Structure Magazine", "2026-06-12", "建筑结构杂志社会议", "Tentative", "Tentative", "Tentative", "Grand Ballroom", 300, "大单保持"),
    ("The Wedding of Mr. Wang and Ms. Shi", "2026-06-13", "王浩&史雪晨婚宴", "Tentative", "Tentative", "Definite", "GB1", 60, "升格 ✅"),
    ("The Wedding of Mr. Bao and Ms. Jiang", "2026-06-14", "鲍承祖&姜文静婚宴", "Definite", "Definite", "Definite", "GB2+3", 180, "三版Definite"),
    ("Tientai Management Meeting", "2026-06-17", "天泰焊材管理层会议", "Prospect", "Prospect", "Prospect", "FR", 40, "三版Prospect未成"),
    ("Black and Decker Meeting", "2026-06-20", "百得苏州会议", "Prospect", "Prospect", "Prospect", "Boardroom", 40, "三版Prospect"),
    
    # ── 消失的活动 ──
    ("TA &A Ultra Clean Meeting", "2026-05-23", "天华超净会议", "Prospect", "Prospect", "消失", "GB1", 100, "未成单 ❌"),
    ("New Channel Study", "2026-05-28", "新航道培训", "Prospect", "Prospect", "消失", "GB1+2", 200, "未成单 ❌"),
    ("Avantor Meeting", "2026-05-22", "艾万拓会议", "Prospect", "N/A", "N/A", "GB3", 60, "v1仅出现"),
    ("Siemens Suzhou Branch", "2026-05-17", "西门子会议", "Prospect", "Prospect", "保留", "FR3+4", 60, "Prospect保级"),
]

# ═══════════════════════════════════════════════════════
# Step 2: Update the graph
# ═══════════════════════════════════════════════════════
import shutil

with open(FIN_GRAPH, "r", encoding="utf-8") as f:
    fin = json.load(f)

shutil.copy(FIN_GRAPH, BACKUP)
print(f"Backup saved to {BACKUP}")

entities = fin["entities"]
relationships = fin["relationships"]

def exists(eid):
    return any(e.get("id") == eid for e in entities)

def rel_exists(rid):
    return any(r.get("id") == rid for r in relationships)

# ── Create version report entities ──
for vid, v in VERSIONS.items():
    if not exists(vid):
        entities.append({
            "id": vid,
            "name": v["name"],
            "type": "beo_version",
            "date": v["report_date"],
            "properties": {
                "report_label": vid,
                "report_date": v["report_date"],
                "generated_by": v["generated_by"],
                "filter_from": v["filter_from"],
                "filter_to": v["filter_to"],
                "total_events": v["total_events"],
                "source_file": v["source_file"],
                "imported_at": "2026-05-10"
            }
        })
        print(f"Created {vid}")

# ── Create version comparison summary ──
CMP_ID = "BEO_VERSION_CMP"
if not exists(CMP_ID):
    entities.append({
        "id": CMP_ID,
        "name": "BEO三版快照对比 (4/26→5/2→5/10)",
        "type": "beo_comparison",
        "date": "2026-05-10",
        "properties": {
            "versions_tracked": 3,
            "v1_id": "BEO_V1_0426",
            "v2_id": "BEO_V2_0502",
            "v3_id": "BEO_V3_0510",
            "v1_total": 99,
            "v2_total": 105,
            "v3_total": 98,
            "events_tracked": len(EVENT_TRACKING),
            "newly_confirmed_v3": sum(1 for e in EVENT_TRACKING if "Definite" in e[6] and "Prospect" in e[3]),
            "lost_leads": sum(1 for e in EVENT_TRACKING if "消失" in e[6] or "未成" in e[6]),
            "imported_at": "2026-05-10"
        }
    })
    print(f"Created {CMP_ID}")

# ── Create tracked event entities + relationships ──
for evt in EVENT_TRACKING:
    eng_name, date, chn_name, v1s, v2s, v3s, room, guests, note = evt
    
    safe_id = f"BEO_TRACK_{date.replace('-','')}_{eng_name[:10].replace(' ','_').replace(',','')}"
    
    props = {
        "date": date,
        "chinese_name": chn_name,
        "english_name": eng_name,
        "room": room,
        "guests": str(guests),
        "v1_status": v1s,
        "v2_status": v2s,
        "v3_status": v3s,
        "note": note
    }
    
    if not exists(safe_id):
        entities.append({
            "id": safe_id,
            "name": f"[BEO跟踪] {date} {chn_name}",
            "type": "beo_tracked_event",
            "date": date,
            "properties": props
        })
    
    # Link to comparison
    rel_cmp = f"REL_{safe_id}_belongs_to_{CMP_ID}"
    if not rel_exists(rel_cmp):
        relationships.append({
            "source_id": safe_id,
            "target_id": CMP_ID,
            "relation": "BELONGS_TO",
            "id": rel_cmp,
            "type": "BELONGS_TO",
            "source": safe_id,
            "target": CMP_ID
        })
    
    # Link to specific versions where applicable
    version_map = {"V1_0426": v1s, "V2_0502": v2s, "V3_0510": v3s}
    for vkey, vstatus in version_map.items():
        if vstatus not in ("N/A", "消失", "v1 only"):
            vid = f"BEO_{vkey}"
            if exists(vid):
                rel_v = f"REL_{safe_id}_tracked_in_{vid}"
                if not rel_exists(rel_v):
                    relationships.append({
                        "source_id": safe_id,
                        "target_id": vid,
                        "relation": "TRACKED_IN",
                        "id": rel_v,
                        "type": "TRACKED_IN",
                        "source": safe_id,
                        "target": vid,
                        "properties": {"status": vstatus}
                    })

# ── Version chain (v1 → v2 → v3) ──
for prev, nxt in [("BEO_V1_0426", "BEO_V2_0502"), ("BEO_V2_0502", "BEO_V3_0510")]:
    if exists(prev) and exists(nxt):
        rel_chain = f"REL_{prev}_updated_to_{nxt}"
        if not rel_exists(rel_chain):
            relationships.append({
                "source_id": prev,
                "target_id": nxt,
                "relation": "UPDATED_TO",
                "id": rel_chain,
                "type": "UPDATED_TO",
                "source": prev,
                "target": nxt
            })

# Link V3 (0510) to the existing BEO_20260510 report
if exists("BEO_V3_0510") and exists("BEO_20260510"):
    rel_link = f"REL_BEO_V3_0510_corresponds_to_BEO_20260510"
    if not rel_exists(rel_link):
        relationships.append({
            "source_id": "BEO_V3_0510",
            "target_id": "BEO_20260510",
            "relation": "CORRESPONDS_TO",
            "id": rel_link,
            "type": "CORRESPONDS_TO",
            "source": "BEO_V3_0510",
            "target": "BEO_20260510"
        })

# Link comparison to FIN_YEAR_2026
if exists(CMP_ID) and exists("FIN_YEAR_2026"):
    rel_fy = f"REL_{CMP_ID}_belongs_to_FIN_YEAR_2026"
    if not rel_exists(rel_fy):
        relationships.append({
            "source_id": CMP_ID,
            "target_id": "FIN_YEAR_2026",
            "relation": "BELONGS_TO",
            "id": rel_fy,
            "type": "BELONGS_TO",
            "source": CMP_ID,
            "target": "FIN_YEAR_2026"
        })

# ── Save ──
with open(FIN_GRAPH, "w", encoding="utf-8") as f:
    json.dump(fin, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"✅ BEO Version Comparison Import Complete")
print(f"{'='*50}")
print(f"  Entities: {len(entities)}")
print(f"  Relationships: {len(relationships)}")
print(f"  Versions tracked: 3 (4/26 → 5/2 → 5/10)")
print(f"  Events tracked: {len(EVENT_TRACKING)}")
print(f"  Newly confirmed in v3: {sum(1 for e in EVENT_TRACKING if '升格' in e[7] or '✅' in e[7])}")
print(f"  Lost leads: {sum(1 for e in EVENT_TRACKING if '❌' in e[7] or '消失' in e[7])}")
