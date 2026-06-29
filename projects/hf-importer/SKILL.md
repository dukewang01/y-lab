---
name: "hf-importer"
description: "Parse History & Forecast PDF, import daily data into FIN knowledge graph"
---

# HF Importer

Parses History & Forecast PDF files and imports the daily room data into the FIN knowledge graph.

## File Detection

HF files are at `media/inbound/` — named like `History_and_Forecast_6.27---*.pdf`.
They are identified by `history_and_forecast`, `hf_20`, or `hf-` in the filename.

## Data Format

The PDF contains daily data in this structure:

| Date | Day | Sold | Occ% | Revenue | ADR | Type |
|-----|-----|------|------|---------|-----|------|

Two sections: **history** (past days, actual) and **forecast** (future days, predicted).

## Workflow

### 1. Locate the HF file
- Scan `media/inbound/` for unprocessed HF PDFs
- Also check `media/incoming/` and `media/archived/`

### 2. Parse the PDF
Use pdfplumber to extract table data. Each row:
- Date (YYYY-MM-DD format)
- Day of week (Mon-Sun)
- Rooms Sold
- Occupancy %
- Revenue (RMB)
- ADR
- Type: "history" or "forecast"

### 3. Import to FIN graph
Using `kg-update` pattern:
- Load `fin_graph.json`
- Create daily entities: `{'id': 'HF_yyyy_mm_dd', 'name': '6月15日HF预测', 'type': 'hf_forecast', 'properties': {'date': '2026-06-15', 'sold': 380, 'occ': 0.706, 'revenue': 152164, 'adr': 613}}`
- Link to month entity HF_2026_06
- Calculate totals: history total revenue, forecast total revenue, full month total

### 4. Report
Output:
```
=== HF导入报告: {date} ===
  History {n}天: ¥{total:,.0f}
  Forecast {n}天: ¥{total:,.0f}
  全月合计: ¥{total:,.0f}
  均Occ (hist): {x}%
  均ADR (hist): ¥{x}
  均Occ (fcst): {x}%
  均ADR (fcst): ¥{x}
```

### 5. Archive
Move processed file to `media/archived/`.
Log in `_inbox_log.json`.
