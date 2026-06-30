#!/usr/bin/env python3
import pdfplumber, os, sys
sys.stdout.reconfigure(encoding='utf-8')

indir = r"C:\Users\Duke Wang\.openclaw\media\inbound"
# 从11月已知格式反查各月的餐饮分析页位置
f11 = "ä_ä_ä¼_è_2025.11---0d869b08-fc6b-48fe-ba4b-0f649ad79e64.pdf"
# 11月的餐饮成本率在第32页(0-index 31)
# 各出口营收在第29页(0-index 28)

# 检查10月同样位置
months = {
    "10": "ä_ä_ä¼_è_2025.10---771bd359-b132-4e75-9bd9-b66cd477cb40.pdf",
    "09": "ä_ä_ä¼_è_2025.09---73ad8885-eb4b-43e8-8919-54b2542e028c.pdf", 
    "08": "ä_ä_ä¼_è_2025.08---0524fb1e-5f7c-4ecf-9bb3-4f0ab99116f1.pdf",
    "07": "ä_ä_ä¼_è_2025.07---42562afa-6649-4d30-a7e3-42d5ba4ca502.pdf",
    "06": "ä_ä_ä¼_è_202506---ad98690b-21a5-4956-8307-d91d2cf91ec6.pdf",
}

for mid, fn in months.items():
    fp = os.path.join(indir, fn)
    if not os.path.exists(fp): continue
    pdf = pdfplumber.open(fp)
    # 扫描所有页找餐饮分析
    found = False
    for i in range(len(pdf.pages)):
        txt = pdf.pages[i].extract_text() or ''
        # 找食品成本率/各出口明细表
        if 'Food Cost' in txt and 'OPEN' in txt or ('食品成本率' in txt and '宴' in txt):
            print(f'\n{mid}月 第{i+1}页 食品成本率:')
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            for l in lines[:20]:
                print(f'  {l[:80]}')
            found = True
        # 找各出口收入
        if 'Covers' in txt and 'OPEN' in txt and 'Food Revenue' in txt:
            print(f'\n{mid}月 第{i+1}页 各出口收入:')
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            for l in lines[:20]:
                print(f'  {l[:80]}')
    if not found:
        print(f'\n{mid}月: 未找到餐饮明细页')
    pdf.close()
