# Excel Attachment Parser

Generic parser for Feishu-uploaded Excel (.xlsx) attachments.
Detects file type by name pattern, extracts data, saves to correct knowledge_center station, and archives the original.

## File Landing

Files from Feishu �?`C:\Users\Y\media\inbound\{original_filename}---{uuid}.xlsx`

## Step 1: Find New Files
```powershell
Get-ChildItem -Path "$env:USERPROFILE\media\inbound\" -Filter "*.xlsx" | Sort-Object LastWriteTime -Descending
```

## Step 2: Detect File Type
```python
def detect_file_type(filename):
    name = filename.lower()
    if 'drr' in name or 'daily_revenue' in name:
        return 'DRR', 'FIN'
    if 'hf' in name or 'history' in name or 'forecast' in name:
        return 'HF', 'FIN'
    if 'beo' in name or 'beo76' in name:
        return 'BEO', 'FB'
    if 'owner' in name:
        return 'OWNER', 'FIN'
    if 'inventory' in name or '盘点' in name:
        return 'INVENTORY', 'FB(HOE)'
    if 'pco' in name:
        return 'PCO', 'FSAA'
    if 'audit' in name or 'brand' in name or 'qa' in name or 'standard' in name:
        return 'AUDIT', 'QA'
    if 'mood' in name or '满意' in name or 'survey' in name:
        return 'MOOD', 'GSM'
    if 'log_case' in name or '投诉' in name or 'complaint' in name:
        return 'CASE', 'RISK'
    if 'summary_of_changes' in name:
        return 'CHANGELOG', 'QA'
    return 'UNKNOWN', 'ASK'
```

## Step 3: Explore Excel Structure
```python
import openpyxl

def explore_excel(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    info = {'sheets': []}
    for sn in wb.sheetnames:
        ws = wb[sn]
        data_rows = []
        for r in range(1, min(ws.max_row + 1, 60)):
            vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
            if any(v is not None for v in vals):
                data_rows.append(vals)
        info['sheets'].append({'name': sn, 'rows': ws.max_row, 'cols': ws.max_column, 'data': data_rows[:30]})
    return info
```

## Step 4: Save to Station & Archive
```python
import shutil, os, json, datetime

INBOUND = r'C:\Users\Y\media\inbound'
ARCHIVED = r'C:\Users\Y\.openclaw\workspace\media\archived'
KC = r'C:\Users\Y\.openclaw\workspace\knowledge_center'
LOG_FILE = os.path.join(KC, '_inbox_log.json')

def archive_file(filepath, station):
    basename = os.path.basename(filepath)
    clean_name = basename.rsplit('---', 1)[0]  # strip UUID
    dest = os.path.join(ARCHIVED, clean_name)
    shutil.copy2(filepath, dest)
    os.remove(filepath)
    # Log it
    log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log = json.load(f)
    log.append({'file': clean_name, 'type': station, 'timestamp': datetime.datetime.now().isoformat()})
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return dest
```

## Quick Scan Command
```powershell
python -c "import os; d=r'$env:USERPROFILE\media\inbound'; files=[f for f in os.listdir(d) if f.endswith('.xlsx') and f!='.gitkeep']; [print(f'  {f}') for f in files] if files else print('No files.')"
```

## Station Import Paths
| Station | Import Dir |
|:--------|:-----------|
| FIN | `knowledge_center/fin/imports/` |
| FB | `knowledge_center/fb/imports/` |
| FSAA | `knowledge_center/fsaa/imports/` |
| QA | `knowledge_center/qa/imports/` |
| GSM | `knowledge_center/gsm/imports/` |
| RISK | `knowledge_center/risk/imports/` |
