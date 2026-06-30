#!/usr/bin/env python3
import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')
pdf = pdfplumber.open(r'media/inbound\ä_ä_ä¼_è_2025.01-02---1069cc0e-7a39-484c-a76c-af4401554330.pdf')
print(f'页数: {len(pdf.pages)}')
for i in range(min(8, len(pdf.pages))):
    txt = pdf.pages[i].extract_text() or ''
    clean = txt[:500].replace('\n',' | ')
    print(f'第{i+1}�? {clean}')
    print()
