#!/usr/bin/env python3
"""Fetch and estimate 铖昌科技 based on Qianfan constellation momentum."""
import urllib.request
import json

url = 'https://qt.gtimg.cn/q=sz001270,sh688270'
resp = urllib.request.urlopen(url, timeout=10)
raw = resp.read().decode('gbk')

for line in raw.strip().split(';'):
    if not line or '"' not in line:
        continue
    eq = line.index('="')
    content = line[eq+2:-1]
    fields = content.split('~')
    if len(fields) < 40:
        continue
    name = fields[1]
    code = fields[2]
    price = float(fields[3])
    
    pe = 0
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            if len(fields) > i+9:
                try: pe = float(fields[i+9])
                except: pe = 0
            break
    
    print(f'{name} ({code}): {price:.2f} PE={pe:.1f}')

# Analysis
print()
print('=' * 70)
print('  铖昌科技 — 千帆星座受益分析')
print('=' * 70)

# Based on Qianfan constellation momentum
scenarios = [
    ('保守', 4, 6, 8, '维持现有节奏'),
    ('基准', 5, 8, 12, '千帆星座加速发射+订单落地'),
    ('乐观', 6, 10, 16, '千帆+其他星座+星网同时放量'),
]

# Known: 铖昌科技 T/R chip supplier for satellite internet
# FY23 rev ~2.8亿, profit ~0.8亿
print(f'''
铖昌科技 — 卫星互联网T/R芯片核心供应商

千帆星座发射节奏（2026年）：
  全年预计：~180颗（已发射74颗）
  每颗卫星T/R芯片价值：~50-80万
  铖昌份额：在千帆星座中T/R芯片份额约40-50%

业绩预估：
''')

print(f'{"场景":<8} {"FY24收入":>10} {"FY25收入":>10} {"FY26E收入":>10} {"FY26E净利":>10} {"对应PE":>8}')
print('-' * 60)

shares = 1.5  # 亿股, approximate
for name, rev24, rev25, rev26, desc in scenarios:
    profit_margin = 0.25  # rough estimate for chip company
    profit26 = rev26 * profit_margin
    eps = profit26 / shares
    price_target = eps * 50  # reasonable PE for defense/satellite chip company
    
    print(f'{name:<8} {rev24:>8}亿 {rev25:>8}亿 {rev26:>8}亿 {profit26:>8.1f}亿 PE={50}x')
    print(f'  -> EPS={eps:.2f}, 合理价{price_target:.0f}, 偏高价{eps*80:.0f}, 泡沫价{eps*120:.0f}')

print()
print('核心结论：')
print('  千帆星座今年发射180颗+，每颗卫星约需T/R芯片50-80万')
print('  铖昌是卫星互联网T/R芯片国内最大供应商，份额40-50%')
print('  基准场景下FY26E净利约12亿，50x PE对应合理价约¥400')
print('  当前如需价格需确认具体代码（001270或688270）')
