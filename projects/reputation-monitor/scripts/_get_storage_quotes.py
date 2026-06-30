#!/usr/bin/env python3
"""Fetch and display storage chip stock quotes."""
import urllib.request

url = 'https://qt.gtimg.cn/q=sh603986,sz301308,sh688525,sz300475,sh688766,sh688123,sh688110,sh688233'
names = {
    '603986': '兆易创新', '301308': '江波龙', '688525': '佰维存储',
    '300475': '香农芯创', '688766': '普冉股份', '688123': '聚辰股份',
    '688110': '东芯股份', '688233': '神工股份',
}

try:
    resp = urllib.request.urlopen(url, timeout=10)
    data = resp.read().decode('gbk')
except:
    # Use cached data
    data = open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\_parse_storage_stocks.py', 'r', encoding='utf-8').read()
    # Find the raw_data section
    start = data.find('raw_data = """')
    end = data.find('""";', start)
    data = data[start+14:end]

import re
results = []
for line in data.split('";'):
    if '~' not in line:
        continue
    m = re.search(r'="(.+)"', line)
    if not m:
        continue
    content = m.group(1)
    fields = content.split('~')
    if len(fields) < 30:
        continue
    
    name = fields[1]
    code = fields[2]
    price = float(fields[3])
    prev = float(fields[4])
    
    for i, f in enumerate(fields):
        if f.startswith('2026'):
            change = float(fields[i+1])
            change_pct = float(fields[i+2])
            high = float(fields[i+3])
            low = float(fields[i+4])
            results.append((name, code, price, change, change_pct, high, low))
            break

results.sort(key=lambda x: x[4], reverse=True)

print()
print(f"{'名称':<10} {'代码':>8} {'现价':>10} {'涨幅%':>8} {'涨跌额':>8} {'最高':>8} {'最低':>8}")
print("-" * 62)
for name, code, price, change, change_pct, high, low in results:
    emoji = "🟢" if change_pct >= 0 else "🔴"
    print(f"{name:<10} {code:>8} ¥{price:>7.2f} {change_pct:>+7.2f}% {change:>+8.2f} ¥{high:>6.2f} ¥{low:>6.2f} {emoji}")

print()
print("其他核心标的（需单独查询）：")
print("  中微公司(688012) / 北方华创(002371) / 沪硅产业(688126)")
print("  安集科技(688019) / 长电科技(600584) / 通富微电(002156)")
print("  雅克科技(002409) / 德明利")
