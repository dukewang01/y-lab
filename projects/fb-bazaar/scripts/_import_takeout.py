#!/usr/bin/env python3
"""导入2026年美团外卖数据到FIN站FB模块"""
import sys, json, openpyxl, os
sys.stdout.reconfigure(encoding="utf-8")

FIN = r'C:\Users\Y\.openclaw\workspace\knowledge_center\fin_graph.json'
inb = r'media/inbound'
fin = json.load(open(FIN, "r", encoding="utf-8"))

def parse_yuxi(fp):
    wb = openpyxl.load_workbook(fp,read_only=True,data_only=True)
    t,d = 0,0
    for sn in wb.sheetnames:
        ws=wb[sn];dt=0
        for r in range(3,ws.max_row+1):
            a=ws.cell(r,4).value
            if isinstance(a,(int,float)) and a>0: dt+=a
            b=ws.cell(r,8).value
            if isinstance(b,(int,float)) and b>0: dt+=b
        if dt>0: t+=dt;d+=1
    wb.close()
    return round(t,2), d

def parse_open(fp):
    wb=openpyxl.load_workbook(fp,read_only=True,data_only=True)
    t,d=0,0
    for sn in wb.sheetnames:
        ws=wb[sn];am,pm=0,0
        for r in range(3,min(ws.max_row+1,15)):
            v=str(ws.cell(r,1).value or "")
            if "上午金额" in v: am=float(ws.cell(r,8).value or 0)
            if "下午金额" in v: pm=float(ws.cell(r,8).value or 0)
        dt=am+pm
        if dt>0: t+=dt;d+=1
    wb.close()
    return round(t,2), d

# 御玺
yuxi = [("2026-01","430f8db3"),("2026-02","cea53b41"),("2026-03","8b98ce4b"),("2026-04","3c5463ab")]
print("=== 御玺美团 ===")
for m,k in yuxi:
    for f in os.listdir(inb):
        if k in f:
            t,d = parse_yuxi(os.path.join(inb,f))
            avg = round(t/d,2) if d else 0
            nid = f"FB_TAKEOUT_YUXI_{m[:4]}_{m[5:]}"
            if not any(e["id"]==nid for e in fin["entities"]):
                fin["entities"].append({
                    "id":nid,"name":f"御玺外卖 {m}","type":"fb_outlet_stats",
                    "date":f"{m}-01","properties":{"outlet":"外卖","kitchen":"御玺","platform":"美团",
                        "month":m,"total_revenue":t,"days":d,"avg_daily_rev":avg,"status":"已填"}
                })
                fin["relationships"].append({"source":nid,"target":"FB_OUTLET_TAKEOUT","type":"BELONGS_TO","relation":"BELONGS_TO"})
            print(f"  {m}: 总¥{t:.0f} {d}�?日均¥{avg:.0f} �?)
            break

# 西厨�?open_k = [("2026-01","91146bef"),("2026-02","137da460"),("2026-03","293b2f91"),("2026-04","c33fafe7")]
print("\n=== 西厨房美�?===")
for m,k in open_k:
    for f in os.listdir(inb):
        if k in f:
            t,d = parse_open(os.path.join(inb,f))
            avg = round(t/d,2) if d else 0
            nid = f"FB_TAKEOUT_OPEN_{m[:4]}_{m[5:]}"
            if not any(e["id"]==nid for e in fin["entities"]):
                fin["entities"].append({
                    "id":nid,"name":f"西厨房外�?{m}","type":"fb_outlet_stats",
                    "date":f"{m}-01","properties":{"outlet":"外卖","kitchen":"西厨�?,"platform":"美团",
                        "month":m,"total_revenue":t,"days":d,"avg_daily_rev":avg,"status":"已填"}
                })
                fin["relationships"].append({"source":nid,"target":"FB_OUTLET_TAKEOUT","type":"BELONGS_TO","relation":"BELONGS_TO"})
            print(f"  {m}: 总¥{t:.0f} {d}�?日均¥{avg:.0f} �?)
            break

json.dump(fin, open(FIN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n�?FIN站外卖数据全量导入完�? (当前{len(fin['entities'])}节点/{len(fin['relationships'])}关系)")
