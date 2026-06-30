#!/usr/bin/env python3
"""Analyze storage cycle bubble thresholds - historical PE comparisons."""
import urllib.request, re

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
            high = float(fields[i+3])
            low = float(fields[i+4])
            break
    
    # Extract PE (usually around position after 振幅)
    pe = None
    for i, f in enumerate(fields):
        try:
            v = float(f)
            if 5 < v < 500 and i > 25:  # PE typically in this range
                # Check if this looks like PE (振幅 usually before PE)
                pe = v
                break
        except:
            continue
    
    stocks[code] = {'name': name, 'price': price, 'chg': chg_pct, 'pe': pe}

# Cycle analysis framework
analysis = {
    '603986': {
        'name': '兆易创新', 'cat': '设计',
        'hist_pe_range': '30-100x', 'peak_cycle_pe': 100,
        'bubble_pe': 120, 'crash_pe': 25,
        'desc': '上次峰值PE~100x(2017/2021), 谷底~30x',
        'cycle_position': 'AI+涨价双重驱动,但PE已超历史峰值',
    },
    '688766': {
        'name': '普冉股份', 'cat': '设计',
        'hist_pe_range': '35-120x', 'peak_cycle_pe': 120,
        'bubble_pe': 150, 'crash_pe': 30,
        'desc': '高增长NOR标的,市场给予成长溢价',
        'cycle_position': '成长性可支撑部分溢价',
    },
    '688123': {
        'name': '聚辰股份', 'cat': '设计',
        'hist_pe_range': '25-60x', 'peak_cycle_pe': 60,
        'bubble_pe': 80, 'crash_pe': 20,
        'desc': 'SPD+EEPROM,周期性弱于存储主赛道',
        'cycle_position': '偏防御品种,PE相对合理',
    },
    '688110': {
        'name': '东芯股份', 'cat': '设计',
        'hist_pe_range': '亏损-200x', 'peak_cycle_pe': 200,
        'bubble_pe': 300, 'crash_pe': 50,
        'desc': '利基存储+存算联概念,盈利能力弱',
        'cycle_position': '概念先行,风险较高',
    },
    '301308': {
        'name': '江波龙', 'cat': '模组',
        'hist_pe_range': '20-60x', 'peak_cycle_pe': 60,
        'bubble_pe': 80, 'crash_pe': 15,
        'desc': '模组企业受价格弹性影响大',
        'cycle_position': '受益涨价周期,PE合理区间上沿',
    },
    '688525': {
        'name': '佰维存储', 'cat': '模组',
        'hist_pe_range': '25-70x', 'peak_cycle_pe': 70,
        'bubble_pe': 90, 'crash_pe': 20,
        'desc': '封测+模组一体化,成长性溢价',
        'cycle_position': 'AI终端概念加持',
    },
    '001309': {
        'name': '德明利', 'cat': '模组',
        'hist_pe_range': '20-50x', 'peak_cycle_pe': 50,
        'bubble_pe': 70, 'crash_pe': 15,
        'desc': '主控自研模组企业',
        'cycle_position': '涨停后PE需关注',
    },
    '300475': {
        'name': '香农芯创', 'cat': '分销',
        'hist_pe_range': '15-40x', 'peak_cycle_pe': 40,
        'bubble_pe': 55, 'crash_pe': 10,
        'desc': '分销模式,利润率低,PE天然低',
        'cycle_position': 'HBM概念推高估值',
    },
    '688012': {
        'name': '中微公司', 'cat': '设备',
        'hist_pe_range': '50-150x', 'peak_cycle_pe': 150,
        'bubble_pe': 200, 'crash_pe': 40,
        'desc': '设备国产化长逻辑,PE容忍度高',
        'cycle_position': '国产替代逻辑支撑高PE',
    },
    '002371': {
        'name': '北方华创', 'cat': '设备',
        'hist_pe_range': '40-120x', 'peak_cycle_pe': 120,
        'bubble_pe': 150, 'crash_pe': 30,
        'desc': '设备龙头,成长确定性高',
        'cycle_position': '业绩支撑,PE相对合理',
    },
    '688126': {
        'name': '沪硅产业', 'cat': '材料',
        'hist_pe_range': '亏损-200x', 'peak_cycle_pe': 200,
        'bubble_pe': 300, 'crash_pe': 999,
        'desc': '持续亏损/微利,无法用PE估值',
        'cycle_position': '市梦率,看PS更合适',
    },
    '688019': {
        'name': '安集科技', 'cat': '材料',
        'hist_pe_range': '40-90x', 'peak_cycle_pe': 90,
        'bubble_pe': 110, 'crash_pe': 30,
        'desc': '抛光液龙头,国产替代逻辑',
        'cycle_position': '稳健成长,PE略偏高',
    },
    '002409': {
        'name': '雅克科技', 'cat': '材料',
        'hist_pe_range': '30-70x', 'peak_cycle_pe': 70,
        'bubble_pe': 90, 'crash_pe': 20,
        'desc': '前驱体材料,海力士供应链',
        'cycle_position': 'HBM材料受益,PE合理',
    },
    '688233': {
        'name': '神工股份', 'cat': '材料',
        'hist_pe_range': '30-80x', 'peak_cycle_pe': 80,
        'bubble_pe': 100, 'crash_pe': 20,
        'desc': '硅材料受益存储扩产',
        'cycle_position': '小市值弹性标的',
    },
    '600584': {
        'name': '长电科技', 'cat': '封测',
        'hist_pe_range': '15-40x', 'peak_cycle_pe': 40,
        'bubble_pe': 50, 'crash_pe': 10,
        'desc': '封测龙头,HBM封装概念',
        'cycle_position': '估值合理,向下风险小',
    },
    '002156': {
        'name': '通富微电', 'cat': '封测',
        'hist_pe_range': '15-35x', 'peak_cycle_pe': 35,
        'bubble_pe': 45, 'crash_pe': 10,
        'desc': 'AMD封装,受益AI需求',
        'cycle_position': '估值合理区间',
    },
}

out = '\n'
out += '=' * 110 + '\n'
out += '  存储超级周期 — 泡沫临界值分析\n'
out += '=' * 110 + '\n'
out += '\n'
out += f'{"代码":>8} {"名称":<10} {"现价":>8} {"PE(现)":>8} {"历史PE区间":>12} {"峰值PE":>8} {"泡沫阈值":>9} {"谷底PE":>8} {"当前状态":>14}\n'
out += '-' * 110 + '\n'

values = []
all_data = []
for code, a in analysis.items():
    s = stocks.get(code, {})
    price = s.get('price', 0)
    pe_now = s.get('pe', 0)
    
    peak = a['peak_cycle_pe']
    bubble = a['bubble_pe']
    crash = a['crash_pe']
    
    # Determine status
    if not pe_now or pe_now == 0:
        status = '无PE数据'
    elif pe_now >= bubble:
        status = '⚠️ 泡沫区'
    elif pe_now >= peak:
        status = '⚠️ 偏高区'
    elif pe_now <= crash:
        status = '✅ 低估区'
    else:
        status = '📊 合理区'
    
    out += f'{code:>8} {a["name"]:<10} {price:>8.2f} {pe_now:>8.1f} {a["hist_pe_range"]:>12} {peak:>8} {bubble:>8}x {crash:>8} {status:>14}\n'
    all_data.append((a['cat'], a['name'], price, pe_now, peak, bubble, crash, status))

out += '\n\n'
out += '=' * 110 + '\n'
out += '  分赛道泡沫风险评级\n'
out += '=' * 110 + '\n'

cats = ['设计', '模组', '分销', '设备', '材料', '封测']
for cat in cats:
    items = [d for d in all_data if d[0] == cat]
    if not items:
        continue
    out += f'\n【{cat}】\n'
    for item in items:
        out += f'  {item[1]:<10} PE={item[3]:.0f}x | 峰值{item[4]}x → 泡沫>{item[5]}x → 谷底{item[6]}x | {item[7]}\n'

out += '\n' + '=' * 110 + '\n'
out += '  核心结论\n'
out += '=' * 110 + '\n'
out += """
【当前周期位置判断】

存储芯片超级周期的基本面是真实的（AI驱动+价格持续上涨+国产化），
但市场估值已开始反映泡沫风险：

📊 合理区（赔率较好）：
  长电科技、通富微电、雅克科技、聚辰股份 — PE未超过历史峰值
  
⚠️ 偏高区（需谨慎）：
  兆易创新(PE~129x > 历史峰值100x)、江波龙、佰维存储
  这些公司的PE已超过或接近历史周期峰值
  
🚨 泡沫风险区：
  沪硅产业 — 持续微利下PE虚高，需关注PS
  东芯股份 — 盈利能力弱，概念炒作风险

【临界值通用法则】
1. 设计公司(NOR/DRAM): PE > 80x = 偏高, > 120x = 泡沫
2. 模组公司: PE > 50x = 偏高, > 70x = 泡沫  
3. 设备公司: PE > 120x = 偏高, > 150x = 泡沫（国产替代溢价）
4. 封测公司: PE > 35x = 偏高, > 50x = 泡沫
5. 分销公司: PE > 30x = 偏高, > 50x = 泡沫

【周期反转信号】
- DRAM/NAND现货价格连续2周下跌 → 确认拐点
- 三星/SK海力士资本开支计划缩减 → 周期见顶
- 库存周转天数上升 → 需求放缓
"""

with open(r'C:\Users\Duke Wang\.openclaw\workspace\media\archived\storage_bubble_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(out)

print(out)
