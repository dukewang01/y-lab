#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the new History and Forecast 5.13 PDF and compare with existing FIN graph"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ====== 新PDF数据 (parsed from PDF text above) ======
history = [
    ("01.05.26 Fri", 438, 286, 0, 2, 390, 0, 48, 0, 81.04, 350321.40, 803.49, 90, 0, 0, 3, 888),
    ("02.05.26 Sat", 491, 272, 2, 2, 442, 0, 49, 0, 90.89, 463916.27, 948.70, 219, 1, 1, 5, 1002),
    ("03.05.26 Sun", 465, 260, 4, 2, 415, 0, 50, 0, 86.06, 450831.29, 973.72, 286, 1, 1, 3, 901),
    ("04.05.26 Mon", 330, 203, 0, 2, 324, 0, 6, 0, 60.97, 240250.93, 732.47, 338, 2, 1, 5, 614),
    ("05.05.26 Tue", 147, 51, 0, 2, 147, 0, 0, 0, 26.95, 85628.43, 590.54, 234, 0, 2, 5, 208),
    ("06.05.26 Wed", 258, 145, 0, 2, 253, 0, 5, 0, 47.58, 149866.48, 585.42, 34, 0, 5, 4, 340),
    ("07.05.26 Thu", 514, 349, 0, 2, 336, 0, 178, 0, 95.17, 318575.69, 622.22, 93, 4, 3, 5, 639),
    ("08.05.26 Fri", 464, 143, 0, 2, 318, 0, 146, 0, 85.87, 279566.21, 605.12, 193, 3, 3, 4, 602),
    ("09.05.26 Sat", 237, 114, 2, 2, 233, 0, 4, 0, 43.68, 136633.41, 581.42, 341, 1, 3, 3, 343),
    ("10.05.26 Sun", 232, 115, 0, 2, 222, 0, 10, 0, 42.75, 131720.26, 572.70, 120, 2, 3, 3, 304),
    ("11.05.26 Mon", 389, 204, 0, 2, 360, 0, 29, 0, 71.93, 212253.07, 548.46, 47, 0, 1, 3, 485),
    ("12.05.26 Tue", 437, 165, 0, 2, 407, 0, 30, 0, 80.86, 248095.40, 570.33, 116, 1, 0, 7, 539),
]

forecast = [
    ("13.05.26 Wed", 432, 167, 1, 2, 371, 0, 61, 0, 79.93, 235112.60, 546.77, 172, 0, 0, 7, 506),
    ("14.05.26 Thu", 354, 129, 1, 2, 303, 0, 51, 0, 65.43, 194729.16, 553.21, 208, 0, 0, 7, 416),
    ("15.05.26 Fri", 334, 159, 0, 2, 245, 0, 89, 0, 61.71, 196393.95, 591.55, 189, 0, 0, 6, 409),
    ("16.05.26 Sat", 425, 253, 0, 2, 398, 0, 27, 0, 78.62, 356405.35, 842.57, 162, 0, 0, 5, 678),
    ("17.05.26 Sun", 280, 128, 0, 2, 276, 0, 4, 0, 51.67, 184459.43, 663.52, 266, 0, 0, 4, 408),
    ("18.05.26 Mon", 214, 66, 0, 2, 203, 0, 11, 0, 39.41, 129724.93, 611.91, 137, 0, 0, 3, 251),
    ("19.05.26 Tue", 234, 53, 0, 5, 222, 0, 12, 0, 42.57, 142189.72, 620.92, 33, 0, 0, 3, 271),
    ("20.05.26 Wed", 223, 31, 0, 2, 208, 0, 15, 0, 41.08, 135596.34, 613.56, 45, 0, 0, 2, 257),
    ("21.05.26 Thu", 223, 48, 0, 2, 191, 0, 32, 0, 41.08, 140213.09, 634.45, 47, 0, 0, 2, 255),
    ("22.05.26 Fri", 160, 11, 0, 2, 129, 0, 31, 0, 29.37, 102240.70, 647.09, 74, 0, 0, 2, 195),
    ("23.05.26 Sat", 158, 52, 0, 2, 148, 0, 10, 0, 29.00, 96490.50, 618.53, 51, 0, 0, 2, 220),
    ("24.05.26 Sun", 134, 32, 1, 2, 130, 0, 4, 0, 24.54, 70581.90, 534.71, 52, 0, 0, 2, 171),
    ("25.05.26 Mon", 152, 46, 0, 2, 146, 0, 6, 0, 27.88, 80165.65, 534.44, 30, 0, 0, 2, 181),
    ("26.05.26 Tue", 158, 23, 0, 2, 148, 0, 10, 0, 29.00, 83860.40, 537.57, 21, 0, 0, 2, 187),
    ("27.05.26 Wed", 197, 10, 0, 2, 126, 0, 71, 0, 36.25, 100517.57, 515.47, 32, 0, 0, 2, 227),
    ("28.05.26 Thu", 192, 14, 0, 2, 121, 0, 71, 0, 35.32, 99609.60, 524.26, 19, 0, 0, 2, 223),
    ("29.05.26 Fri", 198, 41, 0, 2, 122, 0, 76, 0, 36.43, 103845.30, 529.82, 40, 0, 0, 2, 257),
    ("30.05.26 Sat", 211, 39, 0, 2, 120, 0, 91, 0, 38.85, 111637.09, 534.15, 41, 0, 0, 2, 270),
    ("31.05.26 Sun", 205, 31, 0, 2, 100, 0, 105, 0, 37.73, 105907.60, 521.71, 51, 0, 0, 2, 237),
]

print("=" * 70)
print("  2026\u5e745\u6708 HF\u62a5\u544a \u2014 History(\u5b9e\u7ee9) + Forecast(\u9884\u6d4b) \u89e3\u8bfb")
print("=" * 70)

# History summary
hist_total_occ = sum(r[1] for r in history)
hist_total_rev = sum(r[10] for r in history)
hist_avg_occ = sum(r[9] for r in history) / len(history)
hist_avg_adr = sum(r[11] for r in history) / len(history)
print()
print("[HISTORY \u5df2\u8fc7\u5929\u6570] 5/1-5/12 \u516112\u5929")
print(f"  \u603b\u5165\u4f4f\u95f4\u591c: {hist_total_occ:,}")
print(f"  \u603b\u5ba2\u623f\u6536\u5165: {hist_total_rev:,.2f}")
print(f"  \u65e5\u5747\u5165\u4f4f:   {hist_total_occ/12:,.0f}")
print(f"  \u65e5\u5747\u6536\u5165:   {hist_total_rev/12:,.2f}")
print(f"  \u5e73\u5747Occ%:   {hist_avg_occ:.1f}%")
print(f"  \u5e73\u5747ADR:    {hist_avg_adr:.2f}")

# 五一4天
print()
print("[\u4e94\u4e00\u9ec4\u91d1\u5468 5/1-5/4]")
may1_4 = [r for r in history if r[0][:5] in ("01.05", "02.05", "03.05", "04.05")]
for r in may1_4:
    tag = r[0].split()[1]
    print(f"  {tag:>3s}: Occ={r[9]:.1f}% | ADR={r[11]:.2f} | Rev={r[10]:,.2f} | Arr={r[2]}")
may1_4_rev = sum(r[10] for r in may1_4)
print(f"  \u5408\u8ba1: Occ\u5747\u503c {sum(r[9] for r in may1_4)/4:.1f}% | ADR\u5747\u503c {sum(r[11] for r in may1_4)/4:.2f} | \u603b\u6536\u5165 {may1_4_rev:,.2f}")

# Peak vs Valley
print()
print("[\u5cf0\u503c\u5bf9\u6bd4]")
best = max(history, key=lambda r: r[10])
worst = min(history, key=lambda r: r[10])
print(f"  \u6700\u9ad8\u65e5: {best[0]} | Occ={best[9]:.1f}% | Rev={best[10]:,.2f} | ADR={best[11]:.2f}")
print(f"  \u6700\u4f4e\u65e5: {worst[0]} | Occ={worst[9]:.1f}% | Rev={worst[10]:,.2f} | ADR={worst[11]:.2f}")
print(f"  \u5cf0\u8c37\u5dee: {best[10]-worst[10]:,.2f} ({(best[10]-worst[10])/worst[10]*100:.0f}%!)")

# 上周谜团
print()
print("[\u4e0a\u5468\u8c1c\u56e2 - 5/9(\u516d) \u6df1\u5ea6\u8ffd\u8e2a]")
may9 = [r for r in history if "09.05" in r[0]][0]
may8 = [r for r in history if "08.05" in r[0]][0]
may10 = [r for r in history if "10.05" in r[0]][0]
may7 = [r for r in history if "07.05" in r[0]][0]
print(f"  5/7(\u56db): Occ={may7[9]:.1f}% | Rev={may7[10]:,.2f} | ADR={may7[11]:.2f}")
print(f"  5/8(\u4e94): Occ={may8[9]:.1f}% | Rev={may8[10]:,.2f} | ADR={may8[11]:.2f}")
print(f"  5/9(\u516d): Occ={may9[9]:.1f}% | Rev={may9[10]:,.2f} | ADR={may9[11]:.2f}")
print(f"  5/10(\u65e5): Occ={may10[9]:.1f}% | Rev={may10[10]:,.2f} | ADR={may10[11]:.2f}")

# Forecast
print()
print("[FORECAST 5/13-5/31 \u9884\u6d4b]")
fc_total_occ = sum(r[1] for r in forecast)
fc_total_rev = sum(r[10] for r in forecast)
fc_avg_occ = sum(r[9] for r in forecast) / len(forecast)
fc_avg_adr = sum(r[11] for r in forecast) / len(forecast)
print(f"  \u603b\u5165\u4f4f: {fc_total_occ:,}")
print(f"  \u603b\u6536\u5165: {fc_total_rev:,.2f}")
print(f"  \u65e5\u5747Occ: {fc_avg_occ:.1f}%")
print(f"  \u65e5\u5747ADR: {fc_avg_adr:.2f}")
print(f"  \u65e5\u5747\u6536\u5165: {fc_total_rev/19:,.2f}")

weekends_fc = [r for r in forecast if r[0].split()[1] in ("Sat","Sun")]
weekdays_fc = [r for r in forecast if r[0].split()[1] not in ("Sat","Sun")]
print(f"  \u5468\u672b(F/Sat+Sun): {len(weekends_fc)}\u5929 | \u5747Occ={sum(r[9] for r in weekends_fc)/len(weekends_fc):.1f}% | \u5747ADR={sum(r[11] for r in weekends_fc)/len(weekends_fc):.2f}")
print(f"  \u5e73\u65e5(Mon-Fri): {len(weekdays_fc)}\u5929 | \u5747Occ={sum(r[9] for r in weekdays_fc)/len(weekdays_fc):.1f}% | \u5747ADR={sum(r[11] for r in weekdays_fc)/len(weekdays_fc):.2f}")

# 全月综合
print()
print("[5\u6708\u5168\u6708\u7efc\u5408]")
all_days = history + forecast
total_occ = sum(r[1] for r in all_days)
total_rev = sum(r[10] for r in all_days)
avg_occ = sum(r[9] for r in all_days) / 31
avg_adr = sum(r[11] for r in all_days) / 31
print(f"  \u5168\u6708Occ: {avg_occ:.1f}%")
print(f"  \u5168\u6708ADR: {avg_adr:.2f}")
print(f"  \u5168\u6708\u5ba2\u623f\u6536\u5165: {total_rev:,.2f}")
print(f"  (H)5/1-12: {hist_total_rev:,.2f} | (F)5/13-31: {fc_total_rev:,.2f}")

# 关键预警
print()
print("[关键预警]")
low_weekends = [r for r in forecast if r[9] < 35 and r[0].split()[1] in ("Sat","Sun")]
for r in low_weekends:
    print(f"  !! {r[0]}: Occ仅{r[9]:.1f}% | Rev仅{r[10]:,.0f} | 预测入住{r[1]}间")

low_stretch = [r for r in forecast if r[9] < 40]
print(f"  预测Occ<40%的天数: {len(low_stretch)}天")
for r in low_stretch:
    print(f"    {r[0][:10]}: Occ={r[9]:.1f}% | ADR={r[11]:.2f} | Rev={r[10]:,.0f}")

# 对比已有图谱
print()
print("[对比昨日HF (5/12版)]")
print("  5/13-31 forecast vs 图谱已有版本 — 差异较小时说明预测稳定")
print("  建议将此完整HF导入FIN图谱")
