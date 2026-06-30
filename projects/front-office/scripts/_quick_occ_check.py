#!/usr/bin/env python3
"""Quick parse May 29-31 + June 3 DRR to get weekday pattern."""
import openpyxl
from datetime import datetime

DOW = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

files = {
    '2026-05-29': r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\Daily_Revenue_Report_2026.05.29---c1329915-79cd-478b-9c30-fbedb29e9306.xlsx',
    '2026-05-30': r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\Daily_Revenue_Report_2026.05.30---ffbd2edc-b5c1-4475-9ff6-52591ae40c1d.xlsx',
    '2026-05-31': r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\Daily_Revenue_Report_2026.05.31---eb64f155-0d9e-4d38-8217-a223e11dc178.xlsx',
}

results = []
for date_str, path in files.items():
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Actual']
    
    def n(r,c):
        v = ws.cell(r,c).value
        return float(v) if isinstance(v,(int,float)) else None
    
    sold = n(15,5)
    occ = n(22,5)
    adr = n(24,5)
    rev = n(26,5)
    comp = n(16,5)
    hu = n(17,5)
    
    dow = datetime.strptime(date_str, '%Y-%m-%d').weekday()
    occ_pct = occ * 100 if occ and occ < 1 else (occ or 0)
    
    results.append((date_str, DOW[dow], sold, occ_pct, adr, rev, comp, hu))

# Print table
print("=" * 85)
print("  May 29-Jun 3 — 每日数据（周度模式初探）")
print("=" * 85)
print(f"{'日期':<12} {'星期':>4} {'Sold':>6} {'Occ%':>7} {'ADR':>7} {'Rev':>10} {'Comp':>5} {'HU':>4}")
print("-" * 58)
for r in results:
    print(f"{r[0]:<12} {r[1]:>4} {r[2]:>6.0f} {r[3]:>6.1f}% {r[4]:>7.0f} {r[5]:>10,.0f} {r[6]:>5.0f} {r[7]:>4.0f}")

# June 3
print(f"{'2026-06-03':<12} {'Wed':>4} {'398':>6} {'74.0':>6}% {'578':>7} {'207,771':>10} {'0':>5} {'2':>4}")

# Now calculate weekday averages
print("\n")
print("=" * 85)
print("  周度模式分析")
print("=" * 85)

# Group by DOW
from collections import defaultdict
by_dow = defaultdict(list)
for r in results:
    by_dow[r[1]].append(r)

for d in DOW:
    if d in by_dow:
        items = by_dow[d]
        avg_occ = sum(x[3] for x in items) / len(items)
        avg_adr = sum(x[4] for x in items) / len(items)
        print(f"  {d}: {len(items)}天数据 | 平均Occ={avg_occ:.1f}% | 平均ADR={avg_adr:.0f}")

print("\n")
print("=" * 85)
print("  关键问题诊断")
print("=" * 85)
print("""
五月最后三天（周五-周日）的数据 + 周三（6月3日）的数据：
  - 周五 (5/29): ?% Occ — 通常是商务峰值
  - 周六 (5/30): ?% Occ — 休闲峰值
  - 周日 (5/31): ?% Occ — 过渡期
  - 周三 (6/3): 74.0% Occ — 周中商务日

但只有这4天的数据不足以做结构性判断。需要至少2-3周的数据
才能看清：Occ低的原因是周中商务需求不足，还是周末休闲不够。

现有线索：
  1. 周三Occ 74% — 其实不算差（北京Daxing 83%但这种有特殊性）
  2. GCM YTD 68.5% — 说明周中平均下来被拉了
  3. 6月MTD 3天只有61.8% — 说明6月1-2（周一-周二）可能很低

建议：导入更多的DRR数据（至少覆盖完整的一周），
以及：有没有酒店的"周度出租率分析"或"每日Occ明细"的报表？
""")
