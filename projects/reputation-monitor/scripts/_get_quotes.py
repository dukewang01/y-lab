#!/usr/bin/env python3
"""Fetch and parse storage chip stock quotes from Tencent API."""
import urllib.request, re

url = 'https://qt.gtimg.cn/q=sh603986,sz301308,sh688525,sz300475,sh688766,sh688123,sh688110,sh688233,sz002409,sh688012,sz002371,sh688126,sh688019,sh600584,sz002156'

resp = urllib.request.urlopen(url, timeout=10)
raw = resp.read().decode('gbk')

names = {
    '603986':'兆易创新','301308':'江波龙','688525':'佰维存储','300475':'香农芯创',
    '688766':'普冉股份','688123':'聚辰股份','688110':'东芯股份','688233':'神工股份',
    '002409':'雅克科技','688012':'中微公司','002371':'北方华创','688126':'沪硅产业',
    '688019':'安集科技','600584':'长电科技','002156':'通富微电',
}

results = []
for line in raw.strip().split(';'):
    line = line.strip()
    if not line or line.find('="') < 0:
        continue
    eq = line.index('="')
    content = line[eq+2:-1]
    fields = content.split('~')
    if len(fields) < 40:
        continue
    code = fields[2]
    name = names.get(code, fields[1])
    price = float(fields[3])
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            chg = float(fields[i+1])
            chg_pct = float(fields[i+2])
            high = float(fields[i+3])
            low = float(fields[i+4])
            results.append((name, code, price, chg_pct, chg, high, low))
            break

results.sort(key=lambda x: x[3], reverse=True)

import sys
out = '\n'
header = f'{"名称":<10} {"代码":>8} {"现价":>10} {"涨幅%":>8} {"最高":>8} {"最低":>8}'
out += header + '\n'
out += '-' * 55 + '\n'
for name, code, price, cp, chg, high, low in results:
    out += f'{name:<10} {code:>8} {price:>8.2f} {cp:>+7.2f}% {high:>8.2f} {low:>8.2f}\n'
out += f'\n共 {len(results)} 只标的 | 数据时间: 2026-06-04 收盘\n'

with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\storage_quotes_0604.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(out, end='')
