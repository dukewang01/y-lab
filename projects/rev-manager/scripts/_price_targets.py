#!/usr/bin/env python3
"""Calculate price targets - FIXED share calc. Use PE = price / EPS -> EPS = price / PE."""
import urllib.request

url = 'https://qt.gtimg.cn/q=sh603986,sz301308,sh688525,sz300475,sh688766,sh688123,sh688110,sh688233,sz002409,sh688012,sz002371,sh688126,sh688019,sh600584,sz002156,sz001309'

resp = urllib.request.urlopen(url, timeout=10)
raw = resp.read().decode('gbk')

stocks = {}
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
    name = fields[1]
    price = float(fields[3])
    pe = 0
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            if len(fields) > i+9:
                try: pe = float(fields[i+9])
                except: pe = 0
            break
    stocks[code] = {'name': name, 'price': price, 'pe': pe}

# Company data
data = {
    '603986': {'name': '兆易创新', 'cat': '设计', 'fy25': 22.0, 'fy26e': 40.5, 'rp': 60, 'fp': 100, 'bp': 120, 'note': 'DRAM+车规'},
    '688766': {'name': '普冉股份', 'cat': '设计', 'fy25': 3.5, 'fy26e': 7.1, 'rp': 70, 'fp': 120, 'bp': 150, 'note': 'NOR高成长'},
    '688123': {'name': '聚辰股份', 'cat': '设计', 'fy25': 3.2, 'fy26e': 4.7, 'rp': 35, 'fp': 60, 'bp': 80, 'note': 'SPD稳健'},
    '688110': {'name': '东芯股份', 'cat': '设计', 'fy25': 1.2, 'fy26e': 1.9, 'rp': 80, 'fp': 200, 'bp': 300, 'note': '利基+存算联'},
    '301308': {'name': '江波龙', 'cat': '模组', 'fy25': 8.0, 'fy26e': 13.8, 'rp': 35, 'fp': 60, 'bp': 80, 'note': '全产业链'},
    '688525': {'name': '佰维存储', 'cat': '模组', 'fy25': 7.0, 'fy26e': 12.9, 'rp': 40, 'fp': 70, 'bp': 90, 'note': '封测一体化'},
    '001309': {'name': '德明利', 'cat': '模组', 'fy25': 4.0, 'fy26e': 6.9, 'rp': 30, 'fp': 50, 'bp': 70, 'note': '主控自研'},
    '300475': {'name': '香农芯创', 'cat': '分销', 'fy25': 6.0, 'fy26e': 9.6, 'rp': 25, 'fp': 40, 'bp': 55, 'note': 'HBM分销'},
    '688012': {'name': '中微公司', 'cat': '设备', 'fy25': 18.0, 'fy26e': 25.0, 'rp': 80, 'fp': 150, 'bp': 200, 'note': '刻蚀龙头'},
    '002371': {'name': '北方华创', 'cat': '设备', 'fy25': 55.0, 'fy26e': 76.5, 'rp': 70, 'fp': 120, 'bp': 150, 'note': '薄膜沉积'},
    '688126': {'name': '沪硅产业', 'cat': '材料', 'fy25': 2.5, 'fy26e': 3.7, 'rp': 80, 'fp': 200, 'bp': 300, 'note': '大硅片'},
    '688019': {'name': '安集科技', 'cat': '材料', 'fy25': 5.0, 'fy26e': 7.4, 'rp': 55, 'fp': 90, 'bp': 110, 'note': '抛光液'},
    '002409': {'name': '雅克科技', 'cat': '材料', 'fy25': 8.0, 'fy26e': 11.8, 'rp': 40, 'fp': 70, 'bp': 90, 'note': '前驱体'},
    '688233': {'name': '神工股份', 'cat': '材料', 'fy25': 2.0, 'fy26e': 3.0, 'rp': 40, 'fp': 80, 'bp': 100, 'note': '硅材料'},
    '600584': {'name': '长电科技', 'cat': '封测', 'fy25': 22.0, 'fy26e': 27.9, 'rp': 25, 'fp': 40, 'bp': 50, 'note': '封测龙头'},
    '002156': {'name': '通富微电', 'cat': '封测', 'fy25': 12.0, 'fy26e': 14.9, 'rp': 20, 'fp': 35, 'bp': 45, 'note': 'AMD封装'},
}

lines = []
lines.append('=' * 120)
lines.append('  存储超级周期 — 三段价格预判 (基于FY26E业绩)')
lines.append('=' * 120)
lines.append('')

# Calculate shares from PE: EPS_trailing = price / PE, then shares = fy25_profit / EPS_trailing
for code, d in data.items():
    s = stocks.get(code)
    if not s or s['pe'] <= 0:
        d['shares'] = 1  # fallback
        continue
    # Trailing EPS = price / current PE (this is FY25 based)
    eps_ttm = s['price'] / s['pe']
    if eps_ttm > 0:
        d['shares'] = (d['fy25'] * 100000000) / eps_ttm / 100000000  # 亿股
    else:
        d['shares'] = 1
    # EPS estimate for FY26E
    eps_fy26e = (d['fy26e'] * 100000000) / (d['shares'] * 100000000) if d['shares'] > 0 else 0
    d['eps'] = eps_fy26e

cats = [('设计', ['603986','688766','688123','688110']),
        ('模组', ['301308','688525','001309']),
        ('分销', ['300475']),
        ('设备', ['688012','002371']),
        ('材料', ['688126','688019','002409','688233']),
        ('封测', ['600584','002156'])]

for cat_name, cat_codes in cats:
    lines.append(f'\n[{cat_name}]')
    h = f'{"标的":<10} {"现价":>8} {"PE现":>6} {"FY26E净利":>10} {"26EEPS":>7} {"合理价":>8} {"偏低%":>8} {"偏高价":>8} {"泡沫价":>8} {"状态":>8}'
    lines.append(h)
    lines.append('-' * 90)
    
    for code in cat_codes:
        d = data.get(code)
        s = stocks.get(code)
        if not d or not s:
            continue
        price = s['price']
        pe_now = s['pe']
        eps = d.get('eps', 0)
        if eps <= 0:
            lines.append(f'{d["name"]:<10} {price:>8.2f} {pe_now:>6.1f} -- 微利股无法估值')
            continue
        
        rp = d['rp']; fp = d['fp']; bp = d['bp']
        r_price = round(eps * rp, 2)
        f_price = round(eps * fp, 2)
        b_price = round(eps * bp, 2)
        
        downside_r = (r_price / price - 1) * 100
        
        if pe_now <= rp:
            status = '合理'
        elif pe_now <= fp:
            status = '偏高'
        else:
            status = '泡沫'
        
        lines.append(f'{d["name"]:<10} {price:>8.2f} {pe_now:>6.1f} {d["fy26e"]:>7.1f}亿 {eps:>6.2f} {r_price:>8.2f} {downside_r:>+7.1f}% {f_price:>8.2f} {b_price:>8.2f} {status:>8}')

# Key insights
lines.append('')
lines.append('=' * 120)
lines.append('  关键价格锚点（最关注的几只）')
lines.append('=' * 120)
lines.append('')
lines.append(f'{"标的":<10} {"现价":>8} {"合理价":>8} {"偏高(警戒)":>10} {"泡沫(出货)":>10} {"现→合理":>10} {"现→偏高":>10} {"现→泡沫":>10}')
lines.append('-' * 78)

focus = ['603986','688525','001309','301308','300475','002371','688012','600584']
for code in focus:
    d = data.get(code)
    s = stocks.get(code)
    if not d or not s:
        continue
    eps = d.get('eps', 0)
    if eps <= 0:
        continue
    price = s['price']
    rp = d['rp']; fp = d['fp']; bp = d['bp']
    rp_ = eps * rp
    fp_ = eps * fp
    bp_ = eps * bp
    
    to_r = (rp_ / price - 1) * 100
    to_f = (fp_ / price - 1) * 100
    to_b = (bp_ / price - 1) * 100
    
    lines.append(f'{d["name"]:<10} {price:>8.2f} {rp_:>8.2f} {fp_:>10.2f} {bp_:>10.2f} {to_r:>+9.1f}% {to_f:>+9.1f}% {to_b:>+9.1f}%')

lines.append('')
lines.append('=' * 120)
lines.append('  综合判断')
lines.append('=' * 120)
lines.append('')
lines.append('当前周期位置：基本面(涨价+AI)还在上半场，但部分标的PE已到泡沫区')
lines.append('')
lines.append('最具安全边际（合理价 < 现价 < 偏高价的区间最大）：')
lines.append('  德明利: 合理¥xx → 现¥681 → 偏高¥xx → 泡沫¥xx')
lines.append('  佰维存储: 合理¥xx → 现¥341 → 偏高¥xx → 泡沫¥xx')
lines.append('')
lines.append('最需警惕（已经处于泡沫区）：')
lines.append('  兆易创新(PE 129x > 泡沫120x) — FY26E增长可消化部分')
lines.append('  长电科技(PE 87x > 泡沫50x) — 封测溢价过度')
lines.append('')
lines.append('周期反转信号清单（出现3条即减仓）：')
lines.append('  1. DRAM/NAND现货价连续2周下跌')
lines.append('  2. SK海力士/三星资本开支缩减')
lines.append('  3. 云厂商CSP资本开支增速放缓')
lines.append('  4. 存储模组厂毛利率见顶回落')
lines.append('  5. 下游客户库存周转天数上升')

out = '\n'.join(lines)
with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\storage_price_targets.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(out)
