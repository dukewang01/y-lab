#!/usr/bin/env python3
"""Debug: print raw cell values from Actual sheet."""
import openpyxl
wb = openpyxl.load_workbook(r'media/inbound\Daily_Revenue_Report_2026.05.23---0ca44fc7-f465-4421-aff4-19d6f6aa52cd.xlsx', data_only=True)
ws = wb['Actual']
for r in range(1, 31):
    vals = []
    for c in [3,4,5,6,7,8,9,10]:
        v = ws.cell(r, c).value
        vals.append(f'{v!r}')
    print(f'R{r}: {" | ".join(vals)}')
