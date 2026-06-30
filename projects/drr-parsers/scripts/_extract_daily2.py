import json, openpyxl

xlsx = 'C:\\Users\\Y\\.openclaw\\knowledge_center\\media\\Daily_Revenue_Report_2026.05.06.xlsx'
wb = openpyxl.load_workbook(xlsx, data_only=True)

ws = wb['Actual']

print('=== Êâ´Êèè Actual Ë°?Ââ?0Ë°?===')
for r in range(1, min(ws.max_row+1, 35)):
    vals = []
    for c in range(1, min(ws.max_column+1, 8)):
        v = ws.cell(r, c).value
        vals.append(str(v)[:25] if v is not None else '')
    line = ' | '.join(vals)
    if any(v.strip() for v in vals):
        print(f'R{r}: {line}')
