#!/usr/bin/env python3
"""RevPAR efficiency deep dive for HH Suzhou."""
import openpyxl, math

path = r'C:\Users\Y\.openclaw\workspace\media\archived\GCM_YTD.xlsx'
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb['Export']

markets = {}
hotels = {}
current_market = None
for r in range(2, ws.max_row + 1):
    c1 = ws.cell(r, 1).value; c2 = ws.cell(r, 2).value
    c3 = ws.cell(r, 3).value; c4 = ws.cell(r, 4).value
    c5 = ws.cell(r, 5).value; c6 = ws.cell(r, 6).value; c7 = ws.cell(r, 7).value
    if c1 is not None and c2 == 'Total' and c3 is not None:
        current_market = str(c1)
        markets[current_market] = {'adr': float(c3), 'rev': float(c4), 'revpar': float(c5), 'rns': int(c6), 'occ': float(c7)*100}
        hotels[current_market] = []
    elif current_market and c2 is not None and c3 is not None:
        hotels.setdefault(current_market, []).append({'name': str(c2), 'adr': float(c3), 'rev': float(c4), 'revpar': float(c5), 'rns': int(c6), 'occ': float(c7)*100})

hh_all = []
for mkt, hlist in hotels.items():
    for h in hlist:
        if h['name'].startswith('HH '):
            hh_all.append({'market': mkt, **h})

lines = []

# Find our hotel
our = None
for h in hh_all:
    if 'HH Suzhou' in h['name'] and 'New' not in h['name'] and 'Yinshan' not in h['name'] and 'Wuzhong' not in h['name']:
        our = h
        break

# Filter to core properties
core_hh = [h for h in hh_all if h['occ'] > 30 and h['rns'] > 5000]

# ============================================================
# 1. RevPAR Efficiency Quadrants
# ============================================================
lines.append("=" * 80)
lines.append("  RevPAR 效率四象限分�?)
lines.append("=" * 80)
lines.append("  (横轴: ADR | 纵轴: Occ | 面积: RevPAR)")
lines.append("")
lines.append("  【第一象限: 高ADR+高Occ �?王者区间�?)
lines.append(f"  {'酒店':<38} {'ADR':>8} {'Occ':>8} {'RevPAR':>8} {'RNs':>8}")
lines.append("  " + "-" * 72)
q1 = sorted([h for h in core_hh if h['adr'] >= 800 and h['occ'] >= 75], key=lambda h: h['revpar'], reverse=True)
for h in q1[:10]:
    mkt = h['market'].split('/')[-1]
    lines.append(f"  {h['name']:<38} {h['adr']:>8.0f} {h['occ']:>7.1f}% {h['revpar']:>8.0f} {h['rns']:>8d}")

lines.append("")
lines.append("  【第二象�? 中ADR+高Occ �?效率标兵（我们该学谁）�?)
lines.append(f"  {'酒店':<38} {'ADR':>8} {'Occ':>8} {'RevPAR':>8} {'RNs':>8}")
lines.append("  " + "-" * 72)
q2 = sorted([h for h in core_hh if 550 <= h['adr'] < 800 and h['occ'] >= 75], key=lambda h: h['revpar'], reverse=True)
for h in q2[:10]:
    mkt = h['market'].split('/')[-1]
    flag = " <<<" if h == our else ""
    lines.append(f"  {h['name']:<38} {h['adr']:>8.0f} {h['occ']:>7.1f}% {h['revpar']:>8.0f} {h['rns']:>8d}{flag}")

lines.append("")
lines.append("  【我们的位置�?)
lines.append(f"  HH Suzhou           ADR: {our['adr']:.0f} | Occ: {our['occ']:.1f}% | RevPAR: {our['revpar']:.0f}")
lines.append(f"  属于: 第三象限（中ADR+中Occ�?)

# ============================================================
# 2. Top Occ hotels in our ADR bracket
# ============================================================
lines.append("")
lines.append("=" * 80)
lines.append("  ADR ¥600-700 区间效率排名（我们同区间对手�?)
lines.append("=" * 80)
lines.append(f"{'排名':>3} {'酒店':<38} {'市场':<14} {'ADR':>8} {'RevPAR':>8} {'Occ':>7} {'效率':>8} {'RNs':>8}")
lines.append("-" * 88)
same_adr = sorted([h for h in core_hh if 600 <= h['adr'] <= 700], key=lambda h: h['revpar'], reverse=True)
for i, h in enumerate(same_adr, 1):
    eff = h['revpar'] / h['adr']
    mkt = h['market'].split('/')[-1]
    flag = " <<<" if h == our else ""
    lines.append(f"{i:>3} {h['name']:<38} {mkt:<14} {h['adr']:>8.0f} {h['revpar']:>8.0f} {h['occ']:>6.1f}% {eff:>7.2f} {h['rns']:>8d}{flag}")
    
# Rank of HH Suzhou
our_rank = next(i for i, h in enumerate(same_adr, 1) if h == our)
lines.append(f"\n  苏州希尔顿在该区间排�? {our_rank}/{len(same_adr)}")

# ============================================================
# 3. RevPAR gap decomposition
# ============================================================
lines.append("")
lines.append("=" * 80)
lines.append("  RevPAR 差距分解（�?00-700 ADR区间�?)
lines.append("=" * 80)

# Peer average (same ADR bracket, good hotels)
peers = [h for h in hh_all if 600 <= h['adr'] <= 700 and h['occ'] > 60 and h['rns'] > 20000]
peer_avg_occ = sum(h['occ'] for h in peers) / len(peers)
peer_avg_adr = sum(h['adr'] for h in peers) / len(peers)
peer_avg_revpar = sum(h['revpar'] for h in peers) / len(peers)

# Top 3 performers in bracket
top3 = sorted(peers, key=lambda h: h['revpar'], reverse=True)[:3]
top3_avg_occ = sum(h['occ'] for h in top3) / 3
top3_avg_adr = sum(h['adr'] for h in top3) / 3
top3_avg_revpar = sum(h['revpar'] for h in top3) / 3

# Bottom 30% in bracket
peers_sorted_revpar = sorted(peers, key=lambda h: h['revpar'])
bottom3 = peers_sorted_revpar[:3]

my_occ_pct = our['occ']
lines.append(f"\n{'指标':<24} {'苏州希尔�?:>12} {'区间均�?:>10} {'TOP3均�?:>10}")
lines.append("-" * 56)
lines.append(f"{'ADR':<24} {our['adr']:>12.0f} {peer_avg_adr:>10.0f} {top3_avg_adr:>10.0f}")
lines.append(f"{'Occ (%)':<24} {my_occ_pct:>12.1f} {peer_avg_occ:>10.1f} {top3_avg_occ:>10.1f}")
lines.append(f"{'RevPAR':<24} {our['revpar']:>12.0f} {peer_avg_revpar:>10.0f} {top3_avg_revpar:>10.0f}")

occ_gap = top3_avg_occ - my_occ_pct
lines.append(f"\n--- Occ差距 ({top3_avg_occ:.1f}% - {my_occ_pct:.1f}% = {occ_gap:+.1f}pp) ---")
lines.append(f"拉平Occ = 多卖 {our['rns']/my_occ_pct*100*occ_gap/100:,.0f} 间夜")
lines.append(f"         = 增收 ¥{our['adr'] * our['rns']/my_occ_pct*100*occ_gap/100 / 1e4:,.0f} 万（YTD半年�?)

lines.append(f"\nADR差距 ({top3_avg_adr:.0f} - {our['adr']:.0f} = {top3_avg_adr-our['adr']:+.0f}):")
lines.append(f"拉平ADR = 增收 ¥{(top3_avg_adr-our['adr']) * our['rns'] / 1e4:,.0f} 万（仅YTD�?)

lines.append(f"\n双管齐下（ADR拉平TOP3 + Occ拉平TOP3�? 增收 ¥{(top3_avg_adr-our['adr']) * our['rns']/my_occ_pct*100*occ_gap/100 + top3_avg_adr*our['rns']/my_occ_pct*100*occ_gap/100 / 1e4:,.0f} �?)

# Bottom 3 in same bracket for comparison
lines.append("")
lines.append("--- 区间底部表现 ---")
for h in bottom3:
    mkt = h['market'].split('/')[-1]
    lines.append(f"  {h['name']:<38} {h['adr']:>8.0f} {h['occ']:>6.1f}% RevPAR {h['revpar']:.0f} RNs {h['rns']}")

# ============================================================
# 4. The "Golden Ratio" analysis
# ============================================================
lines.append("")
lines.append("=" * 80)
lines.append("  🏆 最优效率模型：谁是RevPAR王者？")
lines.append("=" * 80)
lines.append("RevPAR = ADR × Occ，两者乘积最大化的酒店：")
lines.append("")
lines.append(f"{'排名':>3} {'酒店':<38} {'ADR':>8} {'Occ':>8} {'RevPAR':>8} {'ADR×Occ':>12}")
lines.append("-" * 76)

by_product = sorted(core_hh, key=lambda h: h['adr'] * h['occ']/100, reverse=True)
for i, h in enumerate(by_product[:15], 1):
    product = h['adr'] * h['occ']/100
    mkt = h['market'].split('/')[-1]
    flag = " <<<" if h == our else ""
    lines.append(f"{i:>3} {h['name']:<38} {h['adr']:>8.0f} {h['occ']:>6.1f}% {h['revpar']:>8.0f} {product:>10.0f}{flag}")

our_product = our['adr'] * our['occ']/100
our_rank_by_product = next(i for i, h in enumerate(by_product, 1) if h == our)
lines.append(f"\n  苏州希尔顿：ADR×Occ = {our_product:.0f}，排�?{our_rank_by_product}/{len(by_product)}")

# ============================================================
# 5. Key takeaway
# ============================================================
lines.append("")
lines.append("=" * 80)
lines.append("  核心结论")
lines.append("=" * 80)
lines.append(f"""
1. 我们在�?00-700 ADR区间排第{our_rank}/{len(same_adr)}（按RevPAR�?2. 同等ADR对手的平均Occ {peer_avg_occ:.1f}%，我们{my_occ_pct:.1f}% �?差{peer_avg_occ-my_occ_pct:.1f}pp
3. ADR我们¥{our['adr']:.0f} vs 区间均值¥{peer_avg_adr:.0f} �?其实还高于均值！
4. 所以核心问题是Occ，不是ADR

最直接的改善路径：
  1️⃣ 短期：拉Occ到区间均值{peer_avg_occ:.0f}% �?RevPAR¥{our['adr']*peer_avg_occ/100:.0f}�?¥{our['adr']*peer_avg_occ/100-our['revpar']:.0f}�?  2️⃣ 中期：拉Occ到区间TOP3水平{top3_avg_occ:.0f}% �?￥{our['adr']*top3_avg_occ/100:.0f}
  3️⃣ 长期：ADR+Occ双管齐下 �?￥{top3_avg_adr*top3_avg_occ/100:.0f}（TOP3平均RevPAR�?""")

outpath = r'C:\Users\Y\.openclaw\workspace\knowledge_center\revpar_deep_analysis.md'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
with open(outpath, 'r', encoding='utf-8') as f:
    print(f.read())
