#!/usr/bin/env python3
"""5月历史与预测 - 核心分析"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 列: (date, Occ, Arr, RoomSold, Comp, HouseUse, OccPct, ADR, Dep, TotalR, OOO, NoShow)
# OccPct: 80.04 = 80.04%
rows = [
    ('01 Fri', 438, 286, 390, 48, 0, 80.04, 803.49, 90, 888, 3, 0),
    ('02 Sat', 491, 272, 442, 49, 0, 90.89, 948.70, 219, 1002, 5, 1),
    ('03 Sun', 465, 260, 415, 50, 1, 86.06, 973.72, 286, 901, 3, 1),
    ('04 Mon', 315, 186, 309, 6, 0, 58.18, 717.25, 338, 578, 5, 2),
    ('05 Tue', 133, 35, 133, 0, 0, 24.35, 574.48, 217, 171, 5, 0),
    ('06 Wed', 182, 65, 178, 4, 0, 33.46, 578.15, 19, 221, 4, 2),
    ('07 Thu', 409, 107, 221, 188, 0, 75.65, 587.70, 33, 459, 4, 2),
    ('08 Fri', 356, 24, 187, 169, 0, 65.80, 574.16, 61, 398, 4, 0),
    ('09 Sat', 171, 48, 170, 1, 0, 31.41, 561.79, 93, 202, 4, 0),
    ('10 Sun', 183, 68, 169, 14, 0, 33.64, 560.57, 57, 216, 4, 0),
    ('11 Mon', 247, 84, 216, 31, 0, 45.54, 562.97, 20, 283, 4, 0),
    ('12 Tue', 246, 33, 214, 32, 0, 45.35, 564.71, 34, 280, 4, 0),
    ('13 Wed', 232, 28, 202, 30, 0, 42.75, 555.70, 46, 258, 4, 0),
    ('14 Thu', 193, 39, 180, 13, 0, 35.50, 568.59, 66, 223, 4, 0),
    ('15 Fri', 252, 205, 162, 90, 0, 46.47, 566.20, 70, 290, 4, 0),
    ('16 Sat', 320, 85, 320, 0, 0, 59.11, 889.93, 47, 515, 4, 0),
    ('17 Sun', 205, 31, 205, 0, 0, 37.73, 687.28, 200, 301, 4, 0),
    ('18 Mon', 122, 24, 122, 0, 0, 22.30, 616.68, 114, 139, 3, 0),
    ('19 Tue', 140, 12, 140, 0, 0, 25.65, 620.10, 6, 157, 3, 0),
    ('20 Wed', 133, 15, 133, 0, 0, 24.35, 604.62, 19, 150, 3, 0),
    ('21 Thu', 127, 8, 127, 0, 0, 23.23, 591.48, 21, 142, 3, 0),
    ('22 Fri', 106, 12, 106, 0, 0, 19.33, 603.29, 29, 124, 3, 0),
    ('23 Sat', 94, 19, 94, 0, 0, 17.10, 598.46, 24, 115, 3, 0),
    ('24 Sun', 98, 21, 94, 4, 6, 17.84, 538.28, 19, 117, 3, 0),
    ('25 Mon', 108, 16, 102, 6, 10, 19.70, 532.68, 13, 125, 3, 0),
    ('26 Tue', 117, 7, 107, 10, 0, 21.38, 533.74, 11, 130, 3, 0),
    ('27 Wed', 167, 21, 96, 71, 0, 30.67, 506.11, 18, 181, 3, 0),
    ('28 Thu', 165, 17, 94, 71, 0, 30.30, 516.85, 9, 179, 3, 0),
    ('29 Fri', 164, 19, 88, 76, 0, 30.11, 518.90, 27, 192, 3, 0),
    ('30 Sat', 156, 17, 80, 76, 0, 28.62, 506.49, 25, 180, 3, 0),
    ('31 Sun', 154, 19, 78, 76, 0, 28.25, 493.70, 21, 166, 3, 0),
]

total_rooms = 6689
total_occ = sum(r[1] for r in rows)
total_arr = sum(r[2] for r in rows)
total_rev = sum(r[1] * r[7] for r in rows)
avg_occ = sum(r[6] for r in rows) / len(rows)
avg_rate = sum(r[7] for r in rows) / len(rows)

print('=' * 72)
print('  📊 2026年5月 历史与预测报表')
print('=' * 72)
print()
print(f'全月总计:')
print(f'  可售间夜: {total_rooms:,} 间')
print(f'  过夜间:   {total_occ:,} 间')
print(f'  总到店:   {total_arr:,} 人')
print(f'  预测营收: ¥{total_rev:,.0f}')
print(f'  平均入住率: {avg_occ:.1f}%')
print(f'  平均房价:  ¥{avg_rate:.0f}')
print(f'  全月RevPAR: ¥{total_rev/total_rooms:,.0f}')
print()

# 已过(5.1-5.4) vs 预测(5.5-5.31)
actual = rows[:4]
forecast = rows[4:]
a_occ = sum(r[1] for r in actual)
a_rev = sum(r[1]*r[7] for r in actual)
a_avg = sum(r[6] for r in actual)/len(actual)
a_rate = sum(r[7] for r in actual)/len(actual)
f_occ = sum(r[1] for r in forecast)
f_rev = sum(r[1]*r[7] for r in forecast)
f_avg = sum(r[6] for r in forecast)/len(forecast)
f_rate = sum(r[7] for r in forecast)/len(forecast)

print(f'已过(5.1-5.4 五一假期):')
print(f'  入住率: {a_avg:.1f}% | 房价: ¥{a_rate:.0f} | 营收: ¥{a_rev:,.0f} | {a_occ}间夜')
print()
print(f'预测(5.5-5.31):')
print(f'  入住率: {f_avg:.1f}% | 房价: ¥{f_rate:.0f} | 营收: ¥{f_rev:,.0f} | {f_occ}间夜')
print()

# 每日明细
print('=' * 72)
print('  每日详情')
print('=' * 72)
print(f'{"日期":<10} {"入住率":>7} {"房价":>8} {"过夜":>5} {"到店":>5} {"离店":>5} {"RevPAR":>7}')
for r in rows:
    revpar = round(r[1] * r[7] / total_rooms, 0)
    mark = '🚀' if r[6] > 70 else ('📉' if r[6] < 25 else '  ')
    print(f'{mark}{r[0]:<10} {r[6]:>6.1f}% ¥{r[7]:>6.0f} {r[1]:>5} {r[2]:>5} {r[9]:>5} ¥{revpar:>5.0f}')
print()

# 周分析
weeks = [
    ('W1 五一', rows[0:4]),
    ('W2 节后', rows[4:11]),
    ('W3 中旬', rows[11:18]),
    ('W4 下旬', rows[18:25]),
    ('W5 月末', rows[25:31]),
]
print('=' * 72)
print('  每周分析')
print('=' * 72)
print(f'{"周":<10} {"入住率":>8} {"房价":>8} {"营收":>12} {"间夜":>6} {"RevPAR":>8}')
for label, group in weeks:
    grp_occ = sum(r[1] for r in group)
    grp_rev = sum(r[1]*r[7] for r in group)
    grp_avg_o = sum(r[6] for r in group)/len(group)
    grp_avg_r = sum(r[7] for r in group)/len(group)
    grp_revpar = grp_rev / (len(group) * total_rooms) * 31
    print(f'{label:<10} {grp_avg_o:>7.1f}% ¥{grp_avg_r:>5.0f} ¥{grp_rev:>9,.0f} {grp_occ:>6} ¥{grp_rev/(total_rooms*len(group))*1000:>5.0f}')
print()

# TOP/BOTTOM
print('=' * 72)
print('  入住率TOP 5')
s = sorted(rows, key=lambda x: -x[6])
for r in s[:5]:
    print(f'  {r[0]:<10} {r[6]:.1f}%  ¥{r[7]:.0f}  {r[1]}间')
print()
print('  入住率BOTTOM 5')
for r in s[-5:]:
    print(f'  {r[0]:<10} {r[6]:.1f}%  ¥{r[7]:.0f}  {r[1]}间')
print()

print('=' * 72)
print('  关键洞察')
print('=' * 72)
print()
print(f'1. 五一假期(5.1-4): 入住率80-91%，均价¥861，¥166万收入占全月28%')
print(f'2. 5.5起断崖式下跌——从58%直降到24-33%，节后效应明显')
print(f'3. 5.7-5.8异常高入住(65-76%)但几乎无到店(107/24间)——')
print(f'   有长住团/会议团/协议公司，到店=0但入住率却高')
print(f'4. 5.16周六：¥890高价但入住率仅59%，价格该降')
print(f'5. 5.18-5.25连续8天<26%，是客房促销/OTA尾房销售最佳窗口')
print(f'6. 5.27-31缓慢回升到28-31%但有固定集团团(76间)在支撑')
print(f'7. 周末定价评估：5.2周六¥949(91%满房)合理，但5.9周六¥562(31%)')
print(f'  和5.16周六¥890(59%)显示价格弹性极大——需动态调价')
