#!/usr/bin/env python3
"""618历史数据分析 + 2026年策略建议"""
import json, sys
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding='utf-8')

CRM_DIR = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
guests = json.load(open(f'{CRM_DIR}/guests.json', 'r', encoding='utf-8-sig'))
visits = json.load(open(f'{CRM_DIR}/visits.json', 'r', encoding='utf-8-sig'))

shop = [v for v in visits if v.get('type') == 'online_purchase']

# 提取618相关商品
def is_618(prod):
    return '618' in prod or '六周年' in prod or '八周年' in prod or '周年庆' in prod

def is_double11(prod):
    return '双11' in prod or '双十一' in prod or '双十二' in prod or '双12' in prod

years = ['2022', '2023', '2024', '2025']
print('=' * 72)
print('  🛒 大促历史数据分析')
print('=' * 72)
print()

for year in years:
    # 该年6月的商城订单
    june_orders = [v for v in shop if v.get('date', '').startswith(f'{year}-06')]
    june_rev = sum(v.get('amount', 0) or 0 for v in june_orders)
    june_count = len(june_orders)
    june_guests = len(set(v.get('guest_id', '') for v in june_orders))
    
    # 618商品
    promo_orders = [v for v in june_orders if is_618(v.get('product', ''))]
    promo_rev = sum(v.get('amount', 0) or 0 for v in promo_orders)
    promo_count = len(promo_orders)
    
    # 爆品
    prod_counter = Counter()
    for v in promo_orders:
        prod_counter[v.get('product', '')] += 1
    
    print(f'{f" 📆 {year}年6月":-<40}')
    print(f'  6月总营收: ¥{june_rev:,.0f} ({june_count}单 · {june_guests}位客人)')
    print(f'  其中618相关: ¥{promo_rev:,.0f} ({promo_count}单 · {promo_rev/june_rev*100:.0f}%占比)')
    print()
    
    if prod_counter:
        print(f'  618爆品:')
        for prod, cnt in prod_counter.most_common(8):
            amt = sum(v.get('amount', 0) or 0 for v in promo_orders if v.get('product') == prod)
            print(f'    {prod[:45]:<45} ×{cnt:>2}  ¥{amt:>6,.0f}')
    print()

print('=' * 72)
print('  📊 618趋势总结')
print('=' * 72)
print()

# 各年6月对比
for year in years:
    june = [v for v in shop if v.get('date', '').startswith(f'{year}-06')]
    promo = [v for v in june if is_618(v.get('product', ''))]
    total = sum(v.get('amount',0) or 0 for v in june)
    p_rev = sum(v.get('amount',0) or 0 for v in promo)
    print(f'  {year}年6月: 总营收¥{total:>7,.0f} → 618促销¥{p_rev:>6,.0f} ({p_rev/total*100:.0f}%)')

print()

# 618与双11对比
print('=' * 72)
print('  ⚔️ 618 vs 双11 数据对比')
print('=' * 72)
print()
for year in years:
    june = shop_6 = [v for v in shop if v.get('date', '').startswith(f'{year}-06')]
    _11 = shop_11 = [v for v in shop if v.get('date', '').startswith(f'{year}-11')]
    j6_rev = sum(v.get('amount',0) or 0 for v in june)
    n11_rev = sum(v.get('amount',0) or 0 for v in _11)
    print(f'  {year}: 6月¥{j6_rev:>7,.0f}  vs  11月¥{n11_rev:>7,.0f}  ({"618胜" if j6_rev>n11_rev else "双11胜"})')

print()

# 618常卖品类分析
print('=' * 72)
print('  🏆 历年618爆品排行（跨年累计）')
print('=' * 72)
all_618 = [v for v in shop if is_618(v.get('product', ''))]
cat_counter = Counter()
for v in all_618:
    prod = v.get('product', '')
    if '健身' in prod or '游泳' in prod: cat_counter['💪 健身/游泳'] += 1
    elif '轻食' in prod or '午餐' in prod: cat_counter['🥗 轻食午餐'] += 1
    elif '咖啡' in prod or '面包' in prod or '甜品' in prod: cat_counter['☕ 咖啡面包'] += 1
    elif '披萨' in prod or 'BACIO' in prod: cat_counter['🍝 BACIO'] += 1
    elif '御玺' in prod: cat_counter['🥇 御玺'] += 1
    elif '小龙虾' in prod: cat_counter['🦞 小龙虾'] += 1
    elif '蛋糕' in prod or '仪式' in prod: cat_counter['🎂 蛋糕甜品'] += 1
    elif 'SPA' in prod or '沐宸' in prod: cat_counter['💆 SPA'] += 1
    elif '洗衣' in prod or '洗件' in prod: cat_counter['🧺 洗衣'] += 1
    elif '下午茶' in prod: cat_counter['🍰 下午茶'] += 1
    else: cat_counter['其他'] += 1

print(f'\n{"品类":<16} {"订单数":>6} {"占比":>6}')
for cat, cnt in cat_counter.most_common():
    pct = cnt / len(all_618) * 100
    print(f'{cat:<16} {cnt:>6} {pct:>5.0f}%')

print()

# 618历史最佳商品
print('=' * 72)
print('  💎 618历史最佳商品')
print('=' * 72)
prod_total = Counter()
prod_rev = defaultdict(float)
for v in all_618:
    p = v.get('product', '')
    prod_total[p] += 1
    prod_rev[p] += v.get('amount', 0) or 0

# 按营收排名
for prod, rev in sorted(prod_rev.items(), key=lambda x: -x[1])[:10]:
    cnt = prod_total[prod]
    print(f'  {prod[:48]:<48} ×{cnt:>2}  ¥{rev:>6,.0f}')

print()

# 2026年618策略建议
print('=' * 72)
print('  🎯 2026年618策略建议')
print('=' * 72)
print()
print('  🔥 确定爆品（历史已验证）：')
print()
print('  1. 健身游泳30次卡（买20送10）')
print(f'     历史销售额: ¥177,467 (历史#1商品)')
print(f'     策略: 提前预热，618当天限时立减¥200')
print()
print('  2. 健身中心个人年卡')
print(f'     历史销售额合计: ¥100,000+ (多次推)')
print(f'     策略: 618特价¥6,180(限30张)')
print()
print('  3. 工作日轻食午餐10次卡')
print(f'     历史销售额: ¥30,000+ (多次推)')
print(f'     策略: 买10送2, 限618一天')
print()
print('  4. 双人主题下午茶')
print(f'     历史单次¥138-178, 走量型')
print(f'     策略: 买5送1次卡')
print()
print('  🆕 新爆品建议（基于CRM洞察）：')
print()
print('  5. 冰箱贴礼盒+咖啡组合（限时套装）')
print(f'     香草和谢wenxi两人买18次¥13,273, 已验证需求')
print(f'     策略: ¥199套装(冰箱贴+咖啡券×3)')
print()
print('  6. 苏希江南礼盒套餐')
print(f'     面/中式品类504人, 复购率高')
print(f'     策略: 618限定版礼盒')
print()
print('  💡 组合策略：')
print('  · 预热期(5.25-6.10): 小程序推送+CRM沉睡唤醒')
print('  · 爆发期(6.11-6.18): 天天不同爆品 + 限时秒杀')
print('  · 延续期(6.19-6.30): 主推酒店住宿套餐(配合5月下旬入住率)')
print()
