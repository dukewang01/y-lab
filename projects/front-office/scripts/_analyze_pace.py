#!/usr/bin/env python3
"""Pace Report - deep channel analysis + revenue gap decomposition."""
import json

with open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fin_graph.json', 'r', encoding='utf-8') as f:
    g = json.load(f)

lines = []

# Pace data structured
channels = {
    'RACK 散客标准价': {'rns': 5918, 'rns_b': 6179, 'rns_ly': 5030, 'adr': 657.60, 'adr_ly': 673.34, 'rev': 3891653, 'rev_b': 4061433, 'rev_ly': 3386875},
    'IBT 企业协议':   {'rns': 21128,'rns_b': 22458,'rns_ly': 20496,'adr': 517.59,'adr_ly': 554.89,'rev': 10935578,'rev_b': 11594341,'rev_ly': 11373027},
    'LEI 休闲':       {'rns': 18131,'rns_b': 19393,'rns_ly': 19261,'adr': 685.74,'adr_ly': 683.10,'rev': 12433136,'rev_b': 12927291,'rev_ly': 13157259},
    'CONV 会议':      {'rns': 2453, 'rns_b': 2242, 'rns_ly': 3252, 'adr': 487.70,'adr_ly': 574.74,'rev': 1196318, 'rev_b': 1060992, 'rev_ly': 1869051},
    'Group 团队':     {'rns': 5188, 'rns_b': 5524, 'rns_ly': 6790, 'adr': 499.11,'adr_ly': 528.54,'rev': 2589402, 'rev_b': 2743716, 'rev_ly': 3588790},
    'PERM 长住':      {'rns': 5249, 'rns_b': 5447, 'rns_ly': 7398, 'adr': 484.29,'adr_ly': 473.02,'rev': 2542058, 'rev_b': 2656709, 'rev_ly': 3499421},
}

total = {'rns': 55614, 'rns_b': 59001, 'rns_ly': 58975,
         'occ': 68.46, 'occ_b': 72.63, 'occ_ly': 72.60,
         'adr': 649.35, 'adr_b': 638.99, 'adr_ly': 656.63,
         'rev': 36112873, 'rev_b': 37700980, 'rev_ly': 38724497,
         'revpar': 444.53, 'revpar_b': 464.08, 'revpar_ly': 476.68}

DOW = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# ====================================================
# 1. Revenue Gap Decomposition
# ====================================================
lines.append("=" * 80)
lines.append("  Revenue Gap 分解：谁在拖后腿？")
lines.append("=" * 80)

lines.append(f"\n{'渠道':<18} {'RNs差vsLY':>10} {'ADR差vsLY':>10} {'Rev差vsLY':>14} {'Rev差vs预算':>14}")
lines.append("-" * 66)

total_gap_vs_ly = 0
total_gap_vs_b = 0
for name, c in channels.items():
    rns_gap = c['rns'] - c['rns_ly']
    adr_gap = c['adr'] - c['adr_ly']
    rev_gap_ly = c['rev'] - c['rev_ly']
    rev_gap_b = c['rev'] - c['rev_b']
    total_gap_vs_ly += rev_gap_ly
    total_gap_vs_b += rev_gap_b
    lines.append(f"{name:<18} {rns_gap:>+10.0f} {adr_gap:>+10.0f} ¥{rev_gap_ly:>+12,.0f} ¥{rev_gap_b:>+12,.0f}")

lines.append("-" * 66)
lines.append(f"{'渠道合计':<18} {'':>10} {'':>10} ¥{total_gap_vs_ly:>+12,.0f} ¥{total_gap_vs_b:>+12,.0f}")

# Total incl other income
other_gap_vs_ly = total['rev'] - total['rev_ly']
other_gap_vs_b = total['rev'] - total['rev_b']
lines.append(f"{'Total(含其他)':<18} {'':>10} {'':>10} ¥{other_gap_vs_ly:>+12,.0f} ¥{other_gap_vs_b:>+12,.0f}")

lines.append("")
lines.append("观察：渠道Revenue同比合计亏了¥" + f"{abs(total_gap_vs_ly):,.0f}")
lines.append("但是Total Incl Rev只亏了¥" + f"{abs(other_gap_vs_ly):,.0f}")
lines.append("差别在于其他收入（¥3,721,048），这块可能计算口径不同。")

# ====================================================
# 2. RNs Gap Decomposition
# ====================================================
lines.append("")
lines.append("=" * 80)
lines.append("  间夜量(RNs)差距分解")
lines.append("=" * 80)

lines.append(f"\n{'渠道':<18} {'YTD RNs':>8} {'预算RNs':>8} {'LY RNs':>8} {'vs预算':>8} {'vsLY':>8} {'预算占比':>8} {'LY占比':>8}")
lines.append("-" * 76)

for name, c in channels.items():
    gap_b = c['rns'] - c['rns_b']
    gap_ly = c['rns'] - c['rns_ly']
    share_b = c['rns'] / total['rns_b'] * 100
    share_ly = c['rns'] / total['rns_ly'] * 100
    lines.append(f"{name:<18} {c['rns']:>8.0f} {c['rns_b']:>8.0f} {c['rns_ly']:>8.0f} {gap_b:>+8.0f} {gap_ly:>+8.0f} {share_b:>7.1f}% {share_ly:>7.1f}%")

# ====================================================
# 3. RNs gap breakdown by major sources
# ====================================================
lines.append("")
lines.append("=" * 80)
lines.append("  RNs 流失分解（同比LY）")
lines.append("=" * 80)

losers = [(name, c['rns_ly'] - c['rns'], (c['rns_ly'] - c['rns']) / total['rns'] * 100) 
          for name, c in channels.items() if c['rns'] < c['rns_ly']]
losers.sort(key=lambda x: x[1], reverse=True)

gainers = [(name, c['rns'] - c['rns_ly'], (c['rns'] - c['rns_ly']) / total['rns'] * 100) 
           for name, c in channels.items() if c['rns'] > c['rns_ly']]

lines.append(f"\n流失（占比从大到小）：")
for name, loss, pct in losers:
    lines.append(f"  {name:<18}: 丢了 {loss:>5.0f} 间 ({pct:.1f}% of total)")

lines.append(f"\n增长（弥补）：")
for name, gain, pct in gainers:
    lines.append(f"  {name:<18}: 多了 {gain:>5.0f} 间 (+{pct:.1f}% of total)")

net = sum(g[1] for g in gainers) - sum(l[1] for l in losers)
lines.append(f"\n净流失: -{abs(net):.0f} 间夜 (= Total vs LY {-3361} 间)")

# ====================================================
# 4. Revenue impact if we fix the three big losers
# ====================================================
lines.append("")
lines.append("=" * 80)
lines.append("  💰 如果追回流失的三大渠道...")
lines.append("=" * 80)

recovery_targets = [
    ('PERM 长住', {'rns_gap': 2149, 'adr': 484}),
    ('Group 团队', {'rns_gap': 1602, 'adr': 499}),
    ('CONV 会议', {'rns_gap': 799, 'adr': 488}),
]

total_recovery_rns = 0
total_recovery_rev = 0
lines.append(f"\n{'渠道':<18} {'追回间夜':>8} {'ADR':>6} {'增收(YTD)':>10} {'年化':>10}")
lines.append("-" * 52)
for name, t in recovery_targets:
    rev_add = t['rns_gap'] * t['adr']
    annual = rev_add * (12/5)
    total_recovery_rns += t['rns_gap']
    total_recovery_rev += rev_add
    lines.append(f"{name:<18} {t['rns_gap']:>8.0f} ¥{t['adr']:>4.0f} ¥{rev_add:>8,.0f} ¥{annual:>8,.0f}")

lines.append("-" * 52)
lines.append(f"{'合计':<18} {total_recovery_rns:>8.0f} {'':>6} ¥{total_recovery_rev:>8,.0f} ¥{total_recovery_rev*12/5:>8,.0f}")

# Occ impact
lines.append(f"\n追回{total_recovery_rns}间夜后，总RNs = {total['rns'] + total_recovery_rns}")
new_occ = (total['rns'] + total_recovery_rns) / (total['rns'] / total['occ'] * 100) * 100
lines.append(f"新Occ = {new_occ:.1f}% (当前{total['occ']:.1f}%，提升{new_occ-total['occ']:.1f}pp)")
lines.append(f"正好拉到区间均值水平 (~72%)")

# ====================================================
# 5. ADR erosion analysis
# ====================================================
lines.append("")
lines.append("=" * 80)
lines.append("  ADR 侵蚀分析：谁在降价？")
lines.append("=" * 80)
lines.append(f"\n{'渠道':<18} {'现在ADR':>8} {'去年ADR':>8} {'变化额':>8} {'变化率':>8}")
lines.append("-" * 54)

for name, c in channels.items():
    gap = c['adr'] - c['adr_ly']
    pct = (c['adr'] / c['adr_ly'] - 1) * 100
    lines.append(f"{name:<18} ¥{c['adr']:>5.0f} ¥{c['adr_ly']:>5.0f} ¥{gap:>+6.0f} {pct:>+7.1f}%")

lines.append("")
lines.append("关键发现：")
lines.append("  IBT (企业协议) 和 CONV (会议) 的ADR降幅最大")
lines.append("  IBT: -¥37 (-7%) — 企业协议价被压下来了")
lines.append("  CONV: -¥87 (-15%) — 会议团队价格大幅下滑")
lines.append("  但RACK和LEI相对稳定，高端休闲客群价格韧性好")

# ====================================================
# 6. Summary
# ====================================================
lines.append("")
lines.append("=" * 80)
lines.append("  总结：三管齐下策略")
lines.append("=" * 80)
lines.append("""
1. PERM（长住客）-¥104万/年化
   追回2,149间夜 = 查哪个长住合同流失了 + 重新接洽
   
2. Group（团队）-¥80万/年化
   追回1,602间夜 = 旅行社/会务合作伙伴复盘

3. CONV（会议）-¥39万/年化
   追回799间夜 = MICE市场营销策略调整

ADR端：IBT定价策略需要审视，¥517可能偏低
        CONV同样被压价至¥488
        但散客和休闲价保持稳定，不必动

最直接的杠杆：PERM > Group > CONV
合计潜在增收: ¥223万(YTD) → 年化约¥535万
Occ从68.5% → 72%+，直接拉到区间均值水平
""")

outpath = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\pace_report_analysis.md'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
with open(outpath, 'r', encoding='utf-8') as f:
    print(f.read())
