#!/usr/bin/env python3
import os, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
indir = r'C:\Users\Duke Wang\.openclaw\media\inbound'
import sys
pdfs = [(f, os.path.getmtime(os.path.join(indir,f))) for f in os.listdir(indir) if f.endswith('.pdf')]
pdfs.sort(key=lambda x: -x[1])
for f, mt in pdfs[:10]:
    dt = datetime.datetime.fromtimestamp(mt).strftime('%H:%M')
    sz = os.path.getsize(os.path.join(indir,f)) // 1024
    safe = f.encode('utf-8', errors='replace').decode('utf-8')
    print(f'{dt}  {sz:>4}KB  {safe}')
