import json

with open('C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center\\fin_graph.json', 'r', encoding='utf-8-sig') as f:
    d = json.load(f)

may = []
for e in d['entities']:
    if e.get('type') == 'daily_revenue':
        eid = e.get('id','')
        if '2026_05' in eid:
            props = e.get('properties', {})
            day = int(eid.split('_')[-1])
            source = props.get('data_type', props.get('source', 'unknown'))
            rev = props.get('room_revenue', props.get('room_revenue_total', 0))
            sold = props.get('rooms_sold', props.get('room_sold', 0))
            occ_raw = props.get('occupancy_pct', props.get('occ_pct', 0))
            adr = props.get('adr', 0)
            
            # 归一化出租率
            occ = float(occ_raw) if occ_raw else 0
            if occ > 1: occ = occ / 100
            
            may.append({
                'day': day,
                'source': str(source)[:15],
                'revenue': float(rev) if rev else 0,
                'sold': int(float(sold)) if sold else 0,
                'occ': occ,
                'adr': float(adr) if adr else 0
            })

may.sort(key=lambda x: x['day'])

print('=== 5月日报数据审计 ===')
print()
print('日报节点总数:', len(may))
print()
print('日期    | 数据类型          | 收入(RMB)       | 售房  | 出租率   | ADR')
print('-' * 70)
for m in may:
    rev_str = f'{m["revenue"]:>12,.0f}' if m['revenue'] > 0 else '     -'
    sold_str = f'{m["sold"]:>4d}' if m['sold'] > 0 else '   -'
    occ_str = f'{m["occ"]*100:>6.2f}%' if m['occ'] > 0 else '     -'
    adr_str = f'{m["adr"]:>8.2f}' if m['adr'] > 0 else '       -'
    print(f'5月{m["day"]:02d} | {m["source"]:<18s} | {rev_str} | {sold_str} | {occ_str} | {adr_str}')

print()
print('=== 结论 ===')
# 检查哪些是实际数据
actual_days = [m for m in may if 'actual' in m['source'].lower() or 'forecast' not in m['source'].lower()]
forecast_days = [m for m in may if 'forecast' in m['source'].lower()]
unknown_days = [m for m in may if 'forecast' not in m['source'].lower() and 'actual' not in m['source'].lower()]

print(f'实际数据(Actual): {len(actual_days)} 天')
for m in actual_days: print(f'  5月{m["day"]:02d}')
print(f'预测数据(Forecast): {len(forecast_days)} 天')
for m in forecast_days: print(f'  5月{m["day"]:02d}')
print(f'未知类型: {len(unknown_days)} 天')
for m in unknown_days: print(f'  5月{m["day"]:02d} ({m["source"]})')

print()
print('=== 5月1-5日五一期间实际数据 ===')
for m in may:
    if m['day'] <= 5:
        print(f'  5月{m["day"]:02d}: type={m["source"]}, 收入={m["revenue"]:.0f}, 售房={m["sold"]}, 出租率={m["occ"]*100:.1f}%, ADR={m["adr"]:.2f}')
