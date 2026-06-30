#!/usr/bin/env python3
"""Fetch real-time stock prices for key storage chip companies."""
import akshare as ak
import pandas as pd

codes = {
    '603986': '兆易创新',
    '301308': '江波龙',
    '688525': '佰维存储',
    '300475': '香农芯创',
    '688766': '普冉股份',
    '688123': '聚辰股份',
    '688110': '东芯股份',
    '688233': '神工股份',
    '002409': '雅克科技',
    '688012': '中微公司',
    '002371': '北方华创',
    '688126': '沪硅产业',
    '688019': '安集科技',
    '600584': '长电科技',
    '002156': '通富微电',
}

try:
    df = ak.stock_zh_a_spot_em()
    results = []
    for code, name in codes.items():
        match = df[df['代码'] == code]
        if not match.empty:
            row = match.iloc[0]
            results.append({
                '代码': code,
                '名称': name,
                '现价': row['最新价'],
                '涨跌幅': row['涨跌幅'],
                '涨跌额': row['涨跌额'],
                '成交量(万)': round(row.get('成交量', 0) / 10000, 1),
                '成交额(亿)': round(row.get('成交额', 0) / 100000000, 2),
                '市盈率': row.get('市盈率-动态', 'N/A'),
                '总市值(亿)': round(row.get('总市值', 0) / 100000000, 2) if pd.notna(row.get('总市值')) else 'N/A',
            })
    
    rdf = pd.DataFrame(results).sort_values('总市值(亿)', ascending=False)
    print(rdf.to_string(index=False))
    
except Exception as e:
    print(f"Spot market error: {e}")
    # Fallback: try individual stock history
    print("\nTrying individual quotes...")
    for code, name in list(codes.items())[:5]:
        try:
            df = ak.stock_zh_a_hist(symbol=code, period='daily', start_date='20260603', end_date='20260604', adjust='qfq')
            if not df.empty:
                r = df.iloc[-1]
                print(f"  {code} {name}: {r['收盘']} ({r['涨跌幅']}%)")
        except Exception as e2:
            print(f"  {code} {name}: error - {str(e2)[:60]}")
