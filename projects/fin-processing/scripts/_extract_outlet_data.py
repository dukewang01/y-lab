#!/usr/bin/env python3
"""Extract outlet revenue data from 10月 and 9月 PDFs"""
import pdfplumber, os, sys
sys.stdout.reconfigure(encoding='utf-8')

indir = r"C:\Users\Duke Wang\.openclaw\media\inbound"
months = {
    "10": "ä_ä_ä¼_è_2025.10---771bd359-b132-4e75-9bd9-b66cd477cb40.pdf",
    "09": "ä_ä_ä¼_è_2025.09---73ad8885-eb4b-43e8-8919-54b2542e028c.pdf",
    "08": "ä_ä_ä¼_è_2025.08---0524fb1e-5f7c-4ecf-9bb3-4f0ab99116f1.pdf",
    "07": "ä_ä_ä¼_è_2025.07---42562afa-6649-4d30-a7e3-42d5ba4ca502.pdf",
    "06": "ä_ä_ä¼_è_202506---ad98690b-21a5-4956-8307-d91d2cf91ec6.pdf",
}

for month_id, fn in months.items():
    fp = os.path.join(indir, fn)
    if not os.path.exists(fp):
        print(f'{month_id}月文件不存在')
        continue
    pdf = pdfplumber.open(fp)
    print(f'\n=== {month_id}月 业主会议 (共{len(pdf.pages)}页) ===')
    for i in range(len(pdf.pages)):
        txt = pdf.pages[i].extract_text() or ''
        # 找餐饮/收入/成本相关页面
        if any(k in txt for k in ['食品成本率','酒水成本率','F&B','餐饮','收入','Profit','Cost']):
            lines = [l for l in txt.split('\n') if l.strip()][:15]
            clean = ' | '.join(l.strip()[:60] for l in lines)
            print(f'  第{i+1}页: {clean[:300]}')
            break
    pdf.close()
