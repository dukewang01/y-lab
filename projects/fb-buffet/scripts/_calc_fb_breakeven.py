#!/usr/bin/env python3
"""
FB_BE 餐饮日保本监测
=====================
每次DRR入库后执行：
  python _calc_fb_breakeven.py
  
自动从图谱读取最新FB数据，计算当日/当月保本情况
"""

import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

KG = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
FB_GRAPH = os.path.join(KG, 'fb_graph.json')

# --- 模型参数 ---
FOOD_COST_RATE = 0.33
GROSS_MARGIN = 0.67

def load_graph():
    with open(FB_GRAPH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_q1_be(graph):
    """从图谱读取Q1保本基线"""
    for e in graph['entities']:
        if e.get('id') == 'BE_2026_Q1':
            return e
    return None

def calculate_be(current_monthly_rev, fixed_cost=None):
    """
    计算当前保本情况
    fixed_cost: 如果不传，使用Q1基准¥1,147,591
    """
    fc = fixed_cost or 1147591
    
    # 月度保本
    be_monthly = fc / GROSS_MARGIN
    
    # 季节调整（夏季+5%能耗）
    import datetime
    month = datetime.datetime.now().month
    if month in [6, 7, 8, 9]:
        fc_adjusted = fc * 1.05
    else:
        fc_adjusted = fc
    
    be_daily = (fc_adjusted / GROSS_MARGIN) / 30
    
    # 如果传入了实际月收入，计算盈亏
    if current_monthly_rev:
        profit = current_monthly_rev * GROSS_MARGIN - fc_adjusted
        margin = profit / current_monthly_rev * 100 if current_monthly_rev > 0 else 0
        return {
            'current_monthly_rev': round(current_monthly_rev),
            'current_daily_rev': round(current_monthly_rev / 30),
            'be_monthly': round(be_monthly),
            'be_daily': round(be_daily),
            'daily_gap': round(current_monthly_rev / 30 - be_daily),
            'est_monthly_profit': round(profit),
            'est_profit_margin_pct': round(margin, 1),
            'status': '盈利' if profit > 0 else '亏损' if profit < 0 else '平衡',
            'season_adjustment': '夏季(×1.05)' if month in [6,7,8,9] else '标准',
            'fixed_cost_used': round(fc_adjusted)
        }
    
    return {
        'be_monthly': round(be_monthly),
        'be_daily': round(be_daily),
        'season_adjustment': '夏季(×1.05)' if month in [6,7,8,9] else '标准',
        'fixed_cost_used': round(fc_adjusted)
    }

def report(current_monthly_fb_rev=None):
    """输出报告"""
    graph = load_graph()
    q1 = get_q1_be(graph)
    
    lines = []
    lines.append('=' * 50)
    lines.append('  餐饮日保本监测报告')
    lines.append('=' * 50)
    
    if q1:
        lines.append(f'\n📊 Q1基线:')
        lines.append(f'  月均固定成本: ¥{q1.get("fixed_costs_monthly_avg", 0):,.0f}')
        lines.append(f'  食材成本率: {q1.get("food_cost_rate", 0.33)*100:.0f}%')
        lines.append(f'  保本线: ¥{q1.get("breakeven_daily", 0):,.0f}/日')
    
    result = calculate_be(current_monthly_fb_rev)
    
    lines.append(f'\n📈 当前保本线:')
    lines.append(f'  季节调整: {result["season_adjustment"]}')
    lines.append(f'  保本: ¥{result["be_daily"]:,}/日')
    
    if current_monthly_fb_rev:
        lines.append(f'\n💵 当前业绩:')
        lines.append(f'  月收入: ¥{result["current_monthly_rev"]:,}')
        lines.append(f'  日均: ¥{result["current_daily_rev"]:,}')
        gap = result['daily_gap']
        lines.append(f'  距离保本: {"超¥" if gap > 0 else "差¥"}{abs(gap):,}/日')
        lines.append(f'  预估月利润: ¥{result["est_monthly_profit"]:,}')
        lines.append(f'  利润率: {result["est_profit_margin_pct"]}%')
        lines.append(f'  状态: {result["status"]}')
    
    print('\n'.join(lines))
    return result

if __name__ == '__main__':
    # 可从参数传入当月餐饮收入
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rev', type=float, help='当月餐饮收入MTD推算')
    args = parser.parse_args()
    
    report(args.rev)
    print()
