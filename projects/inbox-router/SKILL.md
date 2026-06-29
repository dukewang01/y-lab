---
name: "inbox-router"
description: "Route inbox files to correct station, trigger pipelines, archive originals"
---

# Inbox Smart Router

When files arrive in `media/incoming/`, automatically identify their type and route them to the correct station pipeline.

## Workflow

### 1. Scan incoming folder
Check `media/incoming/` for new files (exclude README.md).

### 2. Identify file type
Extract text content from the file (supports .xlsx, .pdf, .txt, .md, .csv, .json).

Match against known patterns:

| File Type | Name Patterns | Pipeline |
|-----------|---------------|----------|
| **HF** (History & Forecast) | history_and_forecast, hf_20, hf-20 | Parse + import to FIN graph |
| **DRR** (Daily Revenue Report) | drr_20, drr-20, daily_revenue_report | Analyze via drr-analyze skill + import to FIN |
| **BEO** (宴会活动) | beo_76, beo-76, beo76, BEO | Import to FB graph |
| **OE/盘点** | inventory, 盘点, oe_report | Import to HOE module in FB graph |
| **FSAA/PCO** | pco_ | Import to FSAA graph |
| **QA/audit** | audit, brand_standard, 品牌标准 | Import to QA graph |
| **MOOD** | mood, 满意度 | Route to GSM graph |
| **RISK/cases** | log_cases, complaint, 投诉 | Route to RISK or GSM |
| **OA/公文** | notification, 通知, government | Archive for reference |
| **Photo/image** | .jpg, .png, .gif | Route to references |
| **Unknown** | — | Ask user which station |
| **Already processed** | filename in _inbox_log.json | Skip with notice |

### 3. Trigger pipeline
For HF and DRR files, trigger the full import pipeline:
- Parse the data
- Generate entities and relations
- Call `kg-update` to add to the knowledge graph
- Update `knowledge_center/README.md` status

### 4. Archive the original
Move processed files to `media/archived/` with a timestamp prefix.
Log the operation in `knowledge_center/_inbox_log.json`.

### 5. Report results
Tell the user what was found, what was processed, and any issues.

## Utility Commands

```python
# Scan incoming
python knowledge_center/_inbox_router.py

# Or manually check incoming
import os
files = [f for f in os.listdir('media/incoming/') if f != 'README.md']
```

## Log Format

_inbox_log.json structure:
```json
{
  "processed": [
    {
      "file": "Daily_Revenue_Report_2026.06.15.xlsx",
      "type": "DRR",
      "date": "2026-06-15",
      "station": "FIN",
      "archived_to": "media/archived/...",
      "pipeline_result": "success",
      "timestamp": "2026-06-15T14:30:00"
    }
  ]
}
```
