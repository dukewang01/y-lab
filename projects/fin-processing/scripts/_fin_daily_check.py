import json, re

with open('C:\\Users\\Y\\.openclaw\\workspace\\knowledge_center\\fin_graph.json', 'r', encoding='utf-8-sig') as f:
    d = json.load(f)

# 找所有日报节�?dates = set()
for e in d['entities']:
    if e.get('type') == 'daily_revenue':
        name = e.get('name','')
        eid = e.get('id','')
        # 从name或id提取日期
        m = re.search(r'(\d{4})[-_](\d{1,2})[-_](\d{1,2})', name + ' ' + eid)
        if m:
            dates.add(f'{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}')

dates = sorted(dates)
print(f'现有日报节点: {len(dates)} �?)
print('全部日报列表:')
for d in dates:
    print(f'  {d}')

print()
target = ['2026-04-30','2026-05-01','2026-05-02','2026-05-03','2026-05-04','2026-05-05','2026-05-06']
print('目标区间: 4/30 - 5/6')
missing = []
for t in target:
    ok = t in dates
    if ok:
        print(f'  {t} -> 已有')
    else:
        print(f'  {t} -> 缺失')
        missing.append(t)

print()
if missing:
    print(f'缺失 {len(missing)} �? {", ".join(missing)}')
else:
    print('全部齐全!')
