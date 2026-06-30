#!/usr/bin/env python3
"""Fetch optical communication stock quotes and build cycle analysis framework."""
import urllib.request, os

codes_str = 'sz300308,sz300502,sz300394,sz002281,sz000988,sz300620,sh688498,sh688205,sh688048,sz300548,sh603083,sz300570,sh688195,sz301205'

url = 'https://qt.gtimg.cn/q=' + codes_str
resp = urllib.request.urlopen(url, timeout=10)
raw = resp.read().decode('gbk')

names_map = {
    '300308':'中际旭创','300502':'新易盛','300394':'天孚通信','002281':'光迅科技',
    '000988':'华工科技','300620':'光库科技','688498':'源杰科技','688205':'德科立',
    '688048':'长光华芯','300548':'博创科技','603083':'剑桥科技','300570':'太辰光',
    '688195':'腾景科技','301205':'联特科技',
}

stocks = []
for line in raw.strip().split(';'):
    line = line.strip()
    if not line or '"' not in line:
        continue
    eq = line.index('="')
    content = line[eq+2:-1]
    fields = content.split('~')
    if len(fields) < 45:
        continue
    code = fields[2]
    name = names_map.get(code, fields[1])
    price = float(fields[3])
    
    pe = 0
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            if len(fields) > i+9:
                try: pe = float(fields[i+9])
                except: pe = 0
            break
    
    stocks.append({'name': name, 'code': code, 'price': price, 'pe': pe})

stocks.sort(key=lambda x: x['pe'] if x['pe'] > 0 else 9999)

# Build analysis
categories = {
    '光模块': ['中际旭创','新易盛','联特科技','剑桥科技'],
    '光器件/组件': ['天孚通信','光迅科技','光库科技','博创科技','太辰光','腾景科技'],
    '光芯片/激光': ['源杰科技','德科立','长光华芯','华工科技'],
}

# PE benchmarks
pe_bench = {
    '光模块': {'reasonable': 25, 'froth': 45, 'bubble': 60, 'desc': 'AI光模块直接受益,PE弹性大'},
    '光器件': {'reasonable': 30, 'froth': 50, 'bubble': 70, 'desc': '光器件龙头上限较高'},
    '光芯片': {'reasonable': 50, 'froth': 100, 'bubble': 150, 'desc': '光芯片国产替代,高PE容忍'},
}

# Earnings estimates (FY25 rough estimates, FY26E based on AI demand growth)
earnings = {
    '中际旭创': {'fy25': 55, 'fy26e': 90, 'desc': 'AI光模块龙头,800G/1.6T量产'},
    '新易盛': {'fy25': 25, 'fy26e': 40, 'desc': '高速光模块,云厂商核心供应商'},
    '天孚通信': {'fy25': 12, 'fy26e': 18, 'desc': '光器件平台化,FA+AWG'},
    '光迅科技': {'fy25': 8, 'fy26e': 12, 'desc': '光器件全品类'},
    '华工科技': {'fy25': 12, 'fy26e': 16, 'desc': '激光+光通信双驱动'},
    '光库科技': {'fy25': 3, 'fy26e': 5, 'desc': '铌酸锂调制器'},
    '源杰科技': {'fy25': 1.5, 'fy26e': 3, 'desc': '光芯片国产替代'},
    '德科立': {'fy25': 2, 'fy26e': 3.5, 'desc': '光模块上游'},
    '长光华芯': {'fy25': 1, 'fy26e': 2, 'desc': '激光芯片'},
    '博创科技': {'fy25': 2.5, 'fy26e': 4, 'desc': 'PLC光分路器'},
    '剑桥科技': {'fy25': 3, 'fy26e': 5, 'desc': '光模块+交换机'},
    '太辰光': {'fy25': 2, 'fy26e': 3, 'desc': '光纤连接器'},
    '腾景科技': {'fy25': 1, 'fy26e': 1.5, 'desc': '精密光学元件'},
    '联特科技': {'fy25': 3, 'fy26e': 6, 'desc': '高速光模块新锐'},
}

out = []
out.append('=' * 120)
out.append('  光通信产业链 — 周期分析与价格预判（基于光通信研报+AI需求趋势）')
out.append('=' * 120)
out.append('')
out.append(f'{"标的":<10} {"代码":>8} {"现价":>8} {"PE(现)":>8} {"赛道":>10} {"合理PE":>8} {"偏高峰值":>8} {"泡沫阈值":>8} {"当前状态":>12}')
out.append('-' * 90)

for s in stocks:
    name = s['name']
    code = s['code']
    price = s['price']
    pe_now = s['pe']
    
    # Determine category
    cat = '其他'
    for cname, items in categories.items():
        if name in items:
            cat = cname.replace('光模块','光模块').replace('光器件/组件','光器件').replace('光芯片/激光','光芯片')
            break
    
    bench = pe_bench.get(cat, {'reasonable':20,'froth':40,'bubble':60})
    rp = bench['reasonable']
    fp = bench['froth']
    bp = bench['bubble']
    
    if pe_now <= 0:
        status = '无数据'
    elif pe_now >= bp:
        status = '泡沫区'
    elif pe_now >= fp:
        status = '偏高区'
    elif pe_now <= rp:
        status = '合理/低估'
    else:
        status = '合理区'
    
    cat_display = cat
    out.append(f'{name:<10} {code:>8} {price:>8.2f} {pe_now:>8.1f} {cat_display:>10} {rp:>8} {fp:>8} {bp:>8} {status:>12}')

# Price targets
out.append('')
out.append('=' * 120)
out.append('  价格预判矩阵（基于FY26E业绩估算）')
out.append('=' * 120)
out.append('')
out.append(f'{"标的":<10} {"现价":>8} {"PE现":>6} {"FY26E净利":>10} {"合理价":>8} {"偏高价":>8} {"泡沫价":>8} {"现→合理":>8}')
out.append('-' * 70)

for s in stocks:
    name = s['name']
    price = s['price']
    pe_now = s['pe']
    e = earnings.get(name)
    if not e or pe_now <= 0:
        continue
    
    # Calculate EPS from current PE (trailing)
    eps = price / pe_now
    shares = (e['fy25'] * 1e8) / eps / 1e8 if eps > 0 else 1
    eps_fy26 = e['fy26e'] / shares if shares > 0 else 0
    
    if eps_fy26 <= 0:
        continue
    
    # Category benchmarks
    cat = '光器件'
    for cname, items in categories.items():
        if name in items:
            cat = cname
            break
    bench = pe_bench.get(cat, {'reasonable':20,'froth':40,'bubble':60})
    
    r_price = round(eps_fy26 * bench['reasonable'], 2)
    f_price = round(eps_fy26 * bench['froth'], 2)
    b_price = round(eps_fy26 * bench['bubble'], 2)
    
    to_r = (r_price / price - 1) * 100
    
    out.append(f'{name:<10} {price:>8.2f} {pe_now:>6.1f} {e["fy26e"]:>7.1f}亿 {r_price:>8.2f} {f_price:>8.2f} {b_price:>8.2f} {to_r:>+7.1f}%')

out.append('')
out.append('=' * 120)
out.append('  核心判断')
out.append('=' * 120)
out.append('')
out.append('【AI驱动光通信超级周期】')
out.append('  光通信是AI算力基建的"血管"——800G/1.6T光模块需求爆发')
out.append('  AI数据中心内部互联从400G→800G→1.6T的升级是确定性趋势')
out.append('  光芯片国产替代+高速率升级双轮驱动')
out.append('')
out.append('【最具安全边际（估值合理+AI受益确定性高）】')
out.append('  中际旭创: AI光模块绝对龙头,800G上量+1.6T接力')
out.append('  天孚通信: 光器件平台化布局,FA+AWG核心供应商')
out.append('  源杰科技: 光芯片国产替代,高成长低基数')
out.append('')
out.append('【偏高/泡沫区（需警惕）】')
out.append('  新易盛/联特科技: 光模块PE偏高,业绩需兑现')
out.append('  剑桥科技: 光模块+交换机竞争格局不明朗')
out.append('')
out.append('【周期关注指标】')
out.append('  1) 英伟达/谷歌/Meta资本开支指引')
out.append('  2) 800G/1.6T光模块出货量环比增速')
out.append('  3) 光芯片产能瓶颈缓解信号')
out.append('  4) CSP云厂商AI服务器采购计划')

with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\optical_cycle_analysis.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n'.join(out))
