#!/usr/bin/env python3
"""Fix bubble analysis file."""
p = r'C:\Users\Y\.openclaw\workspace\knowledge_center\_bubble_analysis.py'
c = open(p, 'r', encoding='utf-8').read()
c = c.replace("crash_pe': '-',", "crash_pe': 999,")
open(p, 'w', encoding='utf-8').write(c)
print('Fixed')
