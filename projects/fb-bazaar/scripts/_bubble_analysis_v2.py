#!/usr/bin/env python3
"""Analyze storage cycle bubble thresholds - FIXED PE extraction."""
import urllib.request, re

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
    
    # Find the date marker and extract PE 9 fields after it
    pe = 0
    chg_pct = 0
    high = 0
    low = 0
    for i, f in enumerate(fields):
        if f.startswith('20260604'):
            chg_pct = float(fields[i+2])
            high = float(fields[i+3])
            low = float(fields[i+4])
            # PE is typically at i+9 (after date, change, chg%, high, low, combined, vol, turnover, 换手率)
            if len(fields) > i+9:
                try:
                    pe = float(fields[i+9])
                except:
                    pe = 0
            break
    
    stocks[code] = {'name': name, 'price': price, 'chg': chg_pct, 'pe': pe}

analysis = {
    '603986': {'name': '兆易创新','cat': '设计','hist_pe_range': '30-100x','peak_cycle_pe': 100,'bubble_pe': 120,'crash_pe': 25,'desc': '上次峰值PE~100x(2017/2021),谷底~30x'},
    '688766': {'name': '普冉股份','cat': '设计','hist_pe_range': '35-120x','peak_cycle_pe': 120,'bubble_pe': 150,'crash_pe': 30,'desc': '高增长NOR标的'},
    '688123': {'name': '聚辰股份','cat': '设计','hist_pe_range': '25-60x','peak_cycle_pe': 60,'bubble_pe': 80,'crash_pe': 20,'desc': 'SPD+EEPROM'},
    '688110': {'name': '东芯股份','cat': '设计','hist_pe_range': '亏损-200x','peak_cycle_pe': 200,'bubble_pe': 300,'crash_pe': 50,'desc': '利基存储'},
    '301308': {'name': '江波龙','cat': '模组','hist_pe_range': '20-60x','peak_cycle_pe': 60,'bubble_pe': 80,'crash_pe': 15,'desc': '模组龙头'},
    '688525': {'name': '佰维存储','cat': '模组','hist_pe_range': '25-70x','peak_cycle_pe': 70,'bubble_pe': 90,'crash_pe': 20,'desc': '封测一体化'},
    '001309': {'name': '德明利','cat': '模组','hist_pe_range': '20-50x','peak_cycle_pe': 50,'bubble_pe': 70,'crash_pe': 15,'desc': '主控自研'},
    '300475': {'name': '香农芯创','cat': '分销','hist_pe_range': '15-40x','peak_cycle_pe': 40,'bubble_pe': 55,'crash_pe': 10,'desc': '分销+HBM概念'},
    '688012': {'name': '中微公司','cat': '设备','hist_pe_range': '50-150x','peak_cycle_pe': 150,'bubble_pe': 200,'crash_pe': 40,'desc': '刻蚀设备'},
    '002371': {'name': '北方华创','cat': '设备','hist_pe_range': '40-120x','peak_cycle_pe': 120,'bubble_pe': 150,'crash_pe': 30,'desc': '薄膜沉积'},
    '688126': {'name': '沪硅产业','cat': '材料','hist_pe_range': '亏损-200x','peak_cycle_pe': 200,'bubble_pe': 300,'crash_pe': 999,'desc': '大硅片'},
    '688019': {'name': '安集科技','cat': '材料','hist_pe_range': '40-90x','peak_cycle_pe': 90,'bubble_pe': 110,'crash_pe': 30,'desc': '抛光液'},
    '002409': {'name': '雅克科技','cat': '材料','hist_pe_range': '30-70x','peak_cycle_pe': 70,'bubble_pe': 90,'crash_pe': 20,'desc': '前驱体'},
    '688233': {'name': '神工股份','cat': '材料','hist_pe_range': '30-80x','peak_cycle_pe': 80,'bubble_pe': 100,'crash_pe': 20,'desc': '硅材料'},
    '600584': {'name': '长电科技','cat': '封测','hist_pe_range': '15-40x','peak_cycle_pe': 40,'bubble_pe': 50,'crash_pe': 10,'desc': '封测龙头'},
    '002156': {'name': '通富微电','cat': '封测','hist_pe_range': '15-35x','peak_cycle_pe': 35,'bubble_pe': 45,'crash_pe': 10,'desc': 'AMD封装'},
}

lines = []
lines.append('=' * 110)
lines.append('  存储超级周期 — 泡沫临界值分析 (PE数据修正版)')
lines.append('=' * 110)
lines.append('')
lines.append(f'{"代码":>8} {"名称":<10} {"现价":>8} {"PE(现)":>8} {"历史PE区间":>12} {"峰值PE":>8} {"泡沫阈值":>9} {"谷底PE":>8} {"当前状态":>14}')
lines.append('-' * 110)

for code, a in sorted(analysis.items()):
    s = stocks.get(code)
    if not s:
        continue
    price = s.get('price', 0)
    pe_now = s.get('pe', 0)
    
    peak = a['peak_cycle_pe']
    bubble = a['bubble_pe']
    crash = a['crash_pe']
    
    if pe_now == 0:
        status = '无PE数据'
    elif pe_now >= bubble:
        status = '泡沫区'
    elif pe_now >= peak:
        status = '偏高区'
    elif pe_now <= crash:
        status = '低估区'
    else:
        status = '合理区'
    
    lines.append(f'{code:>8} {a["name"]:<10} {price:>8.2f} {pe_now:>8.1f} {a["hist_pe_range"]:>12} {peak:>8} {bubble:>8}x {crash:>8} {status:>14}')

lines.append('')
lines.append('')
lines.append('=' * 110)
lines.append('  分赛道风险评级')
lines.append('=' * 110)

cats = ['设计', '模组', '分销', '设备', '材料', '封测']
for cat in cats:
    items = [(code, a) for code, a in analysis.items() if a['cat'] == cat]
    if not items:
        continue
    lines.append(f'\n[{cat}]')
    for code, a in items:
        s = stocks.get(code)
        if not s:
            continue
        pe = s.get('pe', 0)
        status = '泡沫' if pe >= a['bubble_pe'] else ('偏高' if pe >= a['peak_cycle_pe'] else ('低估' if pe <= a['crash_pe'] else '合理'))
        lines.append(f'  {a["name"]:<10} PE={pe:.0f}x | 峰值{a["peak_cycle_pe"]}x >泡沫{a["bubble_pe"]}x >谷底{a["crash_pe"]}x | {status}')

lines.append('')
lines.append('=' * 110)
lines.append('  核心结论')
lines.append('=' * 110)
lines.append('')
lines.append('【合理区】低估或合理——赔率较好：')
for code, a in analysis.items():
    s = stocks.get(code)
    if not s:
        continue
    pe = s.get('pe', 0)
    if pe < a['peak_cycle_pe'] and pe > a['crash_pe']:
        lines.append(f'  {a["name"]}(PE={pe:.0f}x)')
    if pe <= a['crash_pe']:
        lines.append(f'  {a["name"]}(PE={pe:.0f}x) -- 低于历史谷底')

lines.append('')
lines.append('【偏高区】PE超过历史周期峰值——需警惕回调风险：')
for code, a in analysis.items():
    s = stocks.get(code)
    if not s:
        continue
    pe = s.get('pe', 0)
    if a['peak_cycle_pe'] <= pe < a['bubble_pe']:
        lines.append(f'  {a["name"]}(PE={pe:.0f}x > 历史峰值{a["peak_cycle_pe"]}x)')

lines.append('')
lines.append('【泡沫区】PE远高于合理范围——周期拐点风险最大：')
for code, a in analysis.items():
    s = stocks.get(code)
    if not s:
        continue
    pe = s.get('pe', 0)
    if pe >= a['bubble_pe']:
        lines.append(f'  {a["name"]}(PE={pe:.0f}x > 泡沫阈值{a["bubble_pe"]}x)')

lines.append('')
lines.append('【临界值通用法则】')
lines.append('  设计公司(NOR/DRAM): PE>80x偏高, >120x泡沫')
lines.append('  模组公司: PE>50x偏高, >70x泡沫')
lines.append('  设备公司: PE>120x偏高, >150x泡沫')
lines.append('  封测公司: PE>35x偏高, >50x泡沫')
lines.append('  分销公司: PE>30x偏高, >50x泡沫')

lines.append('')
lines.append('【周期反转先行信号】')
lines.append('  1) DRAM/NAND现货价连续2周下跌')
lines.append('  2) 三星/SK海力士资本开支缩减')
lines.append('  3) 下游客户库存周转天数上升')
lines.append('  4) 存储模组厂毛利率见顶回落')
lines.append('  5) CSPs(云厂商)资本开支增速放缓')

out = '\n'.join(lines)
with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\storage_bubble_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(out)
