#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

# 5/14 最新数据
hist = [
    ("2026-05-01","Fri",438,81.04,350321.40,803.49,"history"),
    ("2026-05-02","Sat",491,90.89,463916.27,948.70,"history"),
    ("2026-05-03","Sun",465,86.06,450831.29,973.72,"history"),
    ("2026-05-04","Mon",330,60.97,240250.93,732.47,"history"),
    ("2026-05-05","Tue",147,26.95,85628.43,590.54,"history"),
    ("2026-05-06","Wed",258,47.58,149866.48,585.42,"history"),
    ("2026-05-07","Thu",514,95.17,318575.69,622.22,"history"),
    ("2026-05-08","Fri",464,85.87,279566.21,605.12,"history"),
    ("2026-05-09","Sat",237,43.68,136633.41,581.42,"history"),
    ("2026-05-10","Sun",232,42.75,131720.26,572.70,"history"),
    ("2026-05-11","Mon",389,71.93,212253.07,548.46,"history"),
    ("2026-05-12","Tue",437,80.86,248095.40,570.33,"history"),
    ("2026-05-13","Wed",441,81.60,240903.68,548.76,"history"),
]
fcst = [
    ("2026-05-14","Thu",414,76.58,229594.29,557.27,"forecast"),
    ("2026-05-15","Fri",373,68.96,219714.97,592.22,"forecast"),
    ("2026-05-16","Sat",446,82.53,370173.52,833.72,"forecast"),
    ("2026-05-17","Sun",295,54.46,193511.83,660.45,"forecast"),
    ("2026-05-18","Mon",246,45.35,147129.38,602.99,"forecast"),
    ("2026-05-19","Tue",269,49.07,160752.41,608.91,"forecast"),
    ("2026-05-20","Wed",288,53.16,167757.14,586.56,"forecast"),
    ("2026-05-21","Thu",337,62.27,195227.97,582.77,"forecast"),
    ("2026-05-22","Fri",265,48.88,151076.22,574.43,"forecast"),
    ("2026-05-23","Sat",263,48.51,145610.97,557.90,"forecast"),
    ("2026-05-24","Sun",235,43.31,117514.38,504.35,"forecast"),
    ("2026-05-25","Mon",249,45.91,125070.74,506.36,"forecast"),
    ("2026-05-26","Tue",251,46.28,126931.67,509.77,"forecast"),
    ("2026-05-27","Wed",236,43.49,120508.76,514.99,"forecast"),
    ("2026-05-28","Thu",250,46.10,128321.94,517.43,"forecast"),
    ("2026-05-29","Fri",249,45.91,129953.30,526.13,"forecast"),
    ("2026-05-30","Sat",240,44.24,125768.64,528.44,"forecast"),
    ("2026-05-31","Sun",235,43.31,120282.12,516.23,"forecast"),
]

all_data = hist + fcst
hist_total_rev = sum(r[4] for r in hist)
fcst_total_rev = sum(r[4] for r in fcst)
total_rev = hist_total_rev + fcst_total_rev

print(f'5/14 HF入库:')
print(f'  History 13天: ¥{hist_total_rev:,.0f}')
print(f'  Forecast 18天: ¥{fcst_total_rev:,.0f}')
print(f'  全月合计: ¥{total_rev:,.0f}')

# 入库FIN
fin_fp = os.path.join(BASE, "fin_graph.json")
fin = json.load(open(fin_fp, 'r', encoding='utf-8'))
es = fin.get('entities', [])
existing_ids = set(e.get('id','') for e in es)

# 清理旧的day_开头的5月节点
es[:] = [e for e in es if not (e.get('id','').startswith('day_2026-05') and e.get('type')=='daily_revenue')]
existing_ids = set(e.get('id','') for e in es)

added = 0
for datestr, dow, occ_val, occ_pct, rev, adr, kind in all_data:
    day_id = f"day_{datestr}"
    if day_id not in existing_ids:
        es.append({
            "id": day_id, "type": "daily_revenue", "label": datestr,
            "dow": dow, "occ": occ_pct, "occ_nights": occ_val,
            "room_revenue": rev, "adr": adr, "kind": kind,
            "source": "HF_5.14_PDF"
        })
        existing_ids.add(day_id)
        added += 1

# 版本
for v in [e for e in es if e.get('type')=='version' and 'FIN_VER' in e.get('id','')]:
    es.remove(v)
es.append({'id':'FIN_VER_v5_21','type':'version','label':'FIN v5.21 - 导入HF 5/14最新预测','total_entities':len(es)})

fin['entities'] = es
json.dump(fin, open(fin_fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\nFIN: {len(es)} 实体 | v5.21')
print(f'+新增{added}天数据')
