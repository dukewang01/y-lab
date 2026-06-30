#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小程序商城客户全维分析"""
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
guests = json.load(open(os.path.join(D, 'guests.json'), encoding='utf-8'))
visits = json.load(open(os.path.join(D, 'visits.json'), encoding='utf-8'))
prefs = json.load(open(os.path.join(D, 'preferences.json'), encoding='utf-8'))

from collections import Counter, defaultdict

wx_guests = [g for g in guests if '小程序' in g.get('source', '')]
wx_ids = set(g['id'] for g in wx_guests)
wx_visits = [v for v in visits if v.get('guest_id', '') in wx_ids]

# ======== 基本盘 ========
print('=' * 74)
print('  小程序商城CRM全维分析')
print('  2022.03 ~ 2026.05  |  HILTON SUZHOU')
print('=' * 74)

print()
print('━' * 74)
print('  一、基本盘')
print('━' * 74)
print()
print('  商城订单: %s单 / ¥%s' % (
    '{:,}'.format(len(wx_visits)),
    '{:,}'.format(int(sum(v.get('spend', 0) or 0 for v in wx_visits)))))
print('  CRM客人: %d位 (占全部7,120位客人的%.1f%%)' % (
    len(wx_guests), len(wx_guests) / len(guests) * 100))
print('  通过商城首次识别的: %d位(100%%)' % len(wx_guests))
print('  跨越时间: 2022-03-25 → 2026-05-04(%d年)' % 4)
print()
print('  商城客户人均消费: ¥%.0f' % (
    sum(g.get('total_spend', 0) or 0 for g in wx_guests) / len(wx_guests)))

# ======== 消费力分层 ========
print()
print('━' * 74)
print('  二、客户价值分层')
print('━' * 74)
print()
spend_ranges = defaultdict(list)
for g in wx_guests:
    s = g.get('total_spend', 0) or 0
    if s >= 5000: spend_ranges['¥5K+'].append(g)
    elif s >= 2000: spend_ranges['¥2K-¥5K'].append(g)
    elif s >= 1000: spend_ranges['¥1K-¥2K'].append(g)
    elif s >= 500: spend_ranges['¥500-¥1K'].append(g)
    else: spend_ranges['<¥500'].append(g)

tiers = ['¥5K+', '¥2K-¥5K', '¥1K-¥2K', '¥500-¥1K', '<¥500']
for r in tiers:
    gs = spend_ranges[r]
    total = sum(g.get('total_spend', 0) or 0 for g in gs)
    bar = '█' * int(len(gs) / len(wx_guests) * 100 / 2)
    print('  %-8s %4d人 (%5.1f%%) ¥%-10s 人均¥%.0f %s' % (
        r, len(gs), len(gs) / len(wx_guests) * 100,
        '{:,}'.format(int(total)), total / len(gs) if gs else 0, bar))
print()
high_val = spend_ranges['¥5K+'] + spend_ranges['¥2K-¥5K']
print('  高价值(¥2K+): %d人(%.1f%%) 贡献¥%s (%.1f%%)' % (
    len(high_val),
    len(high_val) / len(wx_guests) * 100,
    '{:,}'.format(int(sum(g.get('total_spend', 0) or 0 for g in high_val))),
    sum(g.get('total_spend', 0) or 0 for g in high_val) / sum(
        g.get('total_spend', 0) or 0 for g in wx_guests) * 100))

# ======== 偏好 ========
print()
print('━' * 74)
print('  三、品类偏好')
print('━' * 74)
print()
tag_all = Counter()
for g in wx_guests:
    for t in g.get('tags', []):
        tag_all[t] += 1
total = len(wx_guests)
for t, c in tag_all.most_common(15):
    bar = '█' * int(c / total * 20)
    print('  %-14s %4d人 (%5.1f%%) %s' % (t[:14], c, c / total * 100, bar))

# ======== 高价值客户偏好 ========
print()
print('━' * 74)
print('  四、高价值客户(¥2K+)深度分析  %d人' % len(high_val))
print('━' * 74)
print()
hv_tags = Counter()
for g in high_val:
    for t in g.get('tags', []):
        hv_tags[t] += 1
for t, c in hv_tags.most_common(10):
    bar = '█' * int(c / len(high_val) * 20)
    print('  %-14s %3d人 (%5.1f%%) %s' % (t[:14], c, c / len(high_val) * 100, bar))
print()

# 高价值TOP20
print('  TOP20客户:')
sorted_hv = sorted(high_val, key=lambda g: -(g.get('total_spend', 0) or 0))
for i, g in enumerate(sorted_hv[:20], 1):
    n = g.get('name', '?')
    s = g.get('total_spend', 0) or 0
    tags = ', '.join(g.get('tags', [])[:4])
    print('  %2d. %-12s ¥%-8s  %s' % (i, n[:12], '{:,}'.format(int(s)), tags[:40]))

# ======== 复购与活跃 ========
print()
print('━' * 74)
print('  五、复购与活跃度')
print('━' * 74)
print()
visit_dist = Counter()
gid_cnt = Counter()
for v in wx_visits:
    gid_cnt[v.get('guest_id', '')] += 1
for c in gid_cnt.values():
    if c >= 20: visit_dist['20+次'] += 1
    elif c >= 10: visit_dist['10-19次'] += 1
    elif c >= 5: visit_dist['5-9次'] += 1
    elif c >= 2: visit_dist['2-4次'] += 1
    else: visit_dist['1次'] += 1

for r in ['20+次', '10-19次', '5-9次', '2-4次', '1次']:
    n = visit_dist.get(r, 0)
    bar = '█' * int(n / len(wx_guests) * 100 / 2) if len(wx_guests) else ''
    print('  %-6s %4d人 (%5.1f%%) %s' % (r, n, n / len(wx_guests) * 100, bar))
print()

# 年度活跃
yr_set = defaultdict(set)
yr_spend = defaultdict(float)
for v in wx_visits:
    d = str(v.get('date', ''))[:4]
    if d and len(d) == 4:
        yr_set[d].add(v.get('guest_id', ''))
        yr_spend[d] += v.get('spend', 0) or 0
print('  年度活跃:')
for y in sorted(yr_set.keys()):
    bar = '█' * int(len(yr_set[y]) / max(len(s) for s in yr_set.values()) * 20)
    print('  %-4s %3d位客户  ¥%-7s %s' % (y, len(yr_set[y]),
          '{:,}'.format(int(yr_spend[y])), bar))

# ======== 热销产品TOP ========
print()
print('━' * 74)
print('  六、热销产品TOP15(按购买次数)')
print('━' * 74)
print()
prod_c = Counter()
for v in wx_visits:
    p = v.get('order_items', '')
    if isinstance(p, list):
        for item in p:
            if isinstance(item, str):
                prod_c[item] += 1
            elif isinstance(item, dict):
                prod_c[item.get('name', str(item)[:20])] += 1
    elif p:
        prod_c[str(p)[:30]] += 1
for p, c in prod_c.most_common(15):
    print('  %-30s %3d次' % (p[:30], c))

# ======== 2026年趋势 ========
print()
print('━' * 74)
print('  七、2026年趋势(1-4月)')
print('━' * 74)
print()
mo_active = defaultdict(set)
mo_rev = defaultdict(float)
for v in wx_visits:
    d = str(v.get('date', ''))
    if d[:4] == '2026':
        mo_active[d[:7]].add(v.get('guest_id', ''))
        mo_rev[d[:7]] += v.get('spend', 0) or 0

max_active = max(len(s) for s in mo_active.values()) if mo_active else 1
for m in sorted(mo_active.keys()):
    bar = '█' * int(len(mo_active[m]) / max_active * 20)
    print('  %-7s %2d位客户  ¥%-6s %s' % (m, len(mo_active[m]),
          '{:,}'.format(int(mo_rev[m])), bar))

print()
print('━' * 74)
print('  八、CRM桥接 — FB产品推荐链路')
print('━' * 74)
print()
print('  FB站产品库(1,965个菜品) → CRM偏好匹配 → 智能推荐')
print()
print('  现有偏好覆盖:')
cat_map = {'自助晚餐': 'OPEN自助餐厅', '健身': '健身中心', '御玺中餐': '御玺中餐厅',
           'BACIO西餐': 'BACIO意大利餐厅', '面包甜品': '面包坊/甜品',
           '轻食午餐': '轻食吧', '下午茶': '大堂吧YUAN', '咖啡饮品': '咖啡吧'}
for tag, outlet in cat_map.items():
    n = tag_all.get(tag, 0)
    bar = '█' * int(n / total * 20)
    print('  %-10s %3d人 %5.1f%% → %s %s' % (tag, n, n / total * 100, outlet[:22], bar))

print()
print('━' * 74)
print('  九、洞察与建议')
print('━' * 74)
print()
print('  📌 核心发现:')
print('    ① 小程序商城是CRM第一大客源(3,289人,46.2%%)')
print('    ② 自助晚餐是绝对王牌(44.6%%)，但单品类依赖度高')
print('    ③ 健身(15.7%%)是第二增长曲线，且客户忠诚度最高')
print('    ④ 仅6.0%%客户到店超5次 — 沉睡比例高(94.0%%)需激活')
print('    ⑤ 头部20人贡献¥456K(人均¥22.8K) — 极不均匀')
print('    ⑥ 2026年3月是近13个月最高活跃(106位/$84K)')
print()
print('  📌 建议行动:')
print('    ① 自助晚餐老客定向推送·精细运营防流失')
print('    ② 健身客户交叉推荐面包甜品/轻食午餐(关联度最高)')
print('    ③ 高价值¥2K+客户建立VIP回访计划(尤其沉睡的→530人中唤醒)')
print('    ④ 1次性客户(2,371人)通过小程序活动(拼团/限时)激活二次下单')
print('    ⑤ 面包甜品+咖啡+礼品伴手(香草的天空型)有稳定复购群')
print('   ================================================')
print('   小程序商城是CRM的活水源头，关键是把"买一次"变成"买一辈子"')
print('   ================================================')
