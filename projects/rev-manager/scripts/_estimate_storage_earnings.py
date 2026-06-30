#!/usr/bin/env python3
"""Estimate storage chip stocks' earnings based on super-cycle analysis."""
import urllib.request, re

# Fetch latest prices and PE data
url = 'https://qt.gtimg.cn/q=sh603986,sz301308,sh688525,sz300475,sh688766,sh688123,sh688110,sh688233,sz002409,sh688012,sz002371,sh688126,sh688019,sh600584,sz002156,sz001309'

resp = urllib.request.urlopen(url, timeout=10)
raw = resp.read().decode('gbk')

stocks = {}
for line in raw.strip().split(';'):
    line = line.strip()
    if not line or line.find('="') < 0:
        continue
    eq = line.index('="')
    content = line[eq+2:-1]
    fields = content.split('~')
    if len(fields) < 45:
        continue
    code = fields[2]
    name = fields[1]
    price = float(fields[3])
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            chg = float(fields[i+1])
            chg_pct = float(fields[i+2])
            break
    # Total market cap (field ~45 area)
    mc = 0
    for f in fields[40:50]:
        try:
            mc = float(f)
            if mc > 1:
                break
        except:
            continue
    
    stocks[code] = {'name': name, 'price': price, 'change': chg_pct, 'mc': mc}

# Known market cap from the data (or calculate from price)
# Let me calculate from the total market cap field in the data

# Earnings estimates based on super-cycle analysis
estimates = {
    '603986': {'name': '兆易创新', 'cat': '设计', 'desc': 'NOR Flash全球18.5%份额, 车规35%, DRAM布局',
               'fy2025_rev': 88, 'fy2025_profit': 22, 'growth_2026': '60-80%', 'pe_bench': '45-55x'},
    '301308': {'name': '江波龙', 'cat': '模组', 'desc': '全产业链布局, 企业级突破, 自研UFS4.1主控',
               'fy2025_rev': 85, 'fy2025_profit': 8, 'growth_2026': '50-70%', 'pe_bench': '35-45x'},
    '688525': {'name': '佰维存储', 'cat': '模组', 'desc': '研发封测一体化, AI眼镜+嵌入式, 授权品牌覆盖广',
               'fy2025_rev': 65, 'fy2025_profit': 7, 'growth_2026': '60-80%', 'pe_bench': '40-50x'},
    '300475': {'name': '香农芯创', 'cat': '分销', 'desc': 'SK海力士合作海普存储, HBM分销稀缺资源',
               'fy2025_rev': 120, 'fy2025_profit': 6, 'growth_2026': '40-60%', 'pe_bench': '30-40x'},
    '001309': {'name': '德明利', 'cat': '模组', 'desc': '主控芯片自研, 企业级存储切入, 智能工厂',
               'fy2025_rev': 35, 'fy2025_profit': 4, 'growth_2026': '50-70%', 'pe_bench': '30-40x'},
    '688766': {'name': '普冉股份', 'cat': '设计', 'desc': 'NOR Flash新星, 存储+战略, 消费/工业/汽车',
               'fy2025_rev': 18, 'fy2025_profit': 3.5, 'growth_2026': '70-100%', 'pe_bench': '50-65x'},
    '688123': {'name': '聚辰股份', 'cat': '设计', 'desc': 'SPD全球第三, EEPROM汽车电子, 音圈马达驱动',
               'fy2025_rev': 12, 'fy2025_profit': 3.2, 'growth_2026': '30-50%', 'pe_bench': '35-45x'},
    '688110': {'name': '东芯股份', 'cat': '设计', 'desc': '利基存储, 存算联布局, 投资上海砺算GPU',
               'fy2025_rev': 8, 'fy2025_profit': 1.2, 'growth_2026': '40-60%', 'pe_bench': '80-120x'},
    '688233': {'name': '神工股份', 'cat': '材料', 'desc': '刻蚀用单晶硅材料龙头, 硅零部件',
               'fy2025_rev': 8, 'fy2025_profit': 2, 'growth_2026': '30-50%', 'pe_bench': '40-60x'},
    '002409': {'name': '雅克科技', 'cat': '材料', 'desc': '前驱体供应商, 进入海力士长鑫供应链',
               'fy2025_rev': 45, 'fy2025_profit': 8, 'growth_2026': '30-50%', 'pe_bench': '30-40x'},
    '688012': {'name': '中微公司', 'cat': '设备', 'desc': 'ICP刻蚀覆盖DRAM/3D NAND 95%场景',
               'fy2025_rev': 75, 'fy2025_profit': 18, 'growth_2026': '25-40%', 'pe_bench': '45-60x'},
    '002371': {'name': '北方华创', 'cat': '设备', 'desc': '薄膜沉积PVD/CVD龙头, 12英寸外延全覆盖',
               'fy2025_rev': 270, 'fy2025_profit': 55, 'growth_2026': '25-40%', 'pe_bench': '40-55x'},
    '688126': {'name': '沪硅产业', 'cat': '材料', 'desc': '大尺寸硅片龙头, 300mm量产',
               'fy2025_rev': 35, 'fy2025_profit': 2.5, 'growth_2026': '30-50%', 'pe_bench': '80-150x'},
    '688019': {'name': '安集科技', 'cat': '材料', 'desc': '存储芯片抛光液, 长江存储核心供应商',
               'fy2025_rev': 18, 'fy2025_profit': 5, 'growth_2026': '30-50%', 'pe_bench': '40-55x'},
    '600584': {'name': '长电科技', 'cat': '封测', 'desc': '封测龙头, Chiplet/3D堆叠/HBM封装',
               'fy2025_rev': 320, 'fy2025_profit': 22, 'growth_2026': '15-30%', 'pe_bench': '25-35x'},
    '002156': {'name': '通富微电', 'cat': '封测', 'desc': 'AMD封装合作伙伴, 先进封装布局',
               'fy2025_rev': 220, 'fy2025_profit': 12, 'growth_2026': '15-25%', 'pe_bench': '20-30x'},
}

# Estimated 2026 earnings based on cycle
import sys
out = '\n'
out += '=' * 100 + '\n'
out += '  存储芯片超级周期 — 各标的业绩估算（2026E）\n'
out += '=' * 100 + '\n'
out += f'\n{"代码":>8} {"名称":<10} {"现价":>8} {"涨跌%":>7} {"FY25营收":>10} {"FY25净利":>10} {"FY26E营收":>10} {"FY26E净利":>10} {"PE(TTM)":>8}\n'
out += '-' * 100 + '\n'

categories = ['设计', '模组', '分销', '材料', '设备', '封测']
cat_results = {}
for cat in categories:
    cat_results[cat] = []

total_company_count = 0
for code, est in estimates.items():
    s = stocks.get(code, {})
    price = s.get('price', 'N/A')
    chg = s.get('change', 0)
    
    if isinstance(price, str):
        continue
    
    # Estimate 2026E revenue and profit based on cycle
    growth_str = est['growth_2026']
    low, high = growth_str.replace('%','').split('-')
    growth_mid = (float(low) + float(high)) / 2 / 100
    
    rev_2025 = est['fy2025_rev']
    profit_2025 = est['fy2025_profit']
    
    rev_2026e = round(rev_2025 * (1 + growth_mid), 1)
    profit_2026e = round(profit_2025 * (1 + growth_mid * 1.2), 1)  # Operating leverage
    
    # PE based on current price / estimated 2026 profit
    mc_est = price * (rev_2025 / profit_2025 * 0.8)  # rough MC estimate
    pe_ttm = round(price * 0.1, 1)  # placeholder
    
    pe_2026e = round(mc_est / (profit_2026e * 100000000) * 100, 1) if profit_2026e > 0 else 0
    
    out += f'{code:>8} {est["name"]:<10} {price:>8.2f} {chg:>+6.2f}% {rev_2025:>8.0f}亿 {profit_2025:>8.1f}亿 {rev_2026e:>8.0f}亿 {profit_2026e:>8.1f}亿\n'
    
    cat_results.setdefault(est['cat'], []).append({
        'name': est['name'], 'price': price, 'chg': chg,
        'rev_25': rev_2025, 'profit_25': profit_2025,
        'rev_26e': rev_2026e, 'profit_26e': profit_2026e
    })
    total_company_count += 1

out += '-' * 100 + '\n'
out += f'{"":>8} {"合计":>10} {"":>8} {"":>7}'
out += f' {sum(e["fy2025_rev"] for e in estimates.values()):>8.0f}亿'
out += f' {sum(e["fy2025_profit"] for e in estimates.values()):>8.1f}亿'
# Sum 2026E
rev_26e_total = sum(round(e['fy2025_rev'] * (1 + (float(e['growth_2026'].replace("%","").split("-")[0]) + float(e['growth_2026'].replace("%","").split("-")[1])) / 2 / 100), 1) for e in estimates.values())
profit_26e_total = sum(round(e['fy2025_profit'] * (1 + (float(e['growth_2026'].replace("%","").split("-")[0]) + float(e['growth_2026'].replace("%","").split("-")[1])) / 2 / 100 * 1.2), 1) for e in estimates.values())
out += f' {rev_26e_total:>8.0f}亿 {profit_26e_total:>8.1f}亿\n'

out += f'\n共 {total_company_count} 只标的 | 数据时间: 2026-06-04\n'

# Category summary
out += '\n\n' + '=' * 100 + '\n'
out += '  分赛道汇总\n'
out += '=' * 100 + '\n'
for cat in categories:
    items = cat_results.get(cat, [])
    if not items:
        continue
    out += f'\n【{cat}】{len(items)}只\n'
    for item in items:
        out += f'  {item["name"]:<10} ¥{item["price"]:>7.2f} {item["chg"]:>+6.2f}% | FY25: {item["rev_25"]}亿/{item["profit_25"]}亿 | FY26E: {item["rev_26e"]}亿/{item["profit_26e"]}亿\n'

with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\storage_earnings_estimate.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(out)
