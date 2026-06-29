---
name: "beo-importer"
description: "Parse BEO PDFs, import banquet event data into FIN + FB graphs"
---

# BEO Importer

Parses BEO (Banquet Event Order) files and imports banquet/event data into both FIN (revenue) and FB (product/menu) knowledge graphs.

## File Detection

BEO files are at `media/inbound/` — named like `2026.7.2_Shanghai_Sai_Fu_meeting_BEO_7736---*.pdf`.
Identified by `beo_76`, `beo-76`, `beo76`, or `BEO` in the filename.

## Data Format

From text extraction, each BEO contains:
- BEO number (#7736, #7737, etc.)
- Event date and time
- Guest count
- Menu items
- Revenue: food, beverage, total
- Room/venue setup

## Workflow

### 1. Locate BEO file
Scan `media/inbound/` or `media/incoming/` for BEO PDFs.

### 2. Extract text
Use pdfplumber to extract text from PDF.
Fallback: use PyMuPDF (fitz) if pdfplumber yields empty text.

### 3. Parse BEO fields
Extract key fields:
- BEO ID (from filename, e.g. BEO_7736)
- Event date
- Function room
- Guest count / setup
- Menu items
- Revenue (food/beverage/total)
- Special instructions

### 4. Import to knowledge graph
**FB graph** (`fb_graph.json`):
- Create BEO entity: `{'id': 'BEO_7736', 'name': 'BEO #7736 上海赛福会议', 'year': 2026, 'month': 7, 'properties': {...}}`
- Link to Banquet category
- Link menu items and pricing

**FIN graph** (`fin_graph.json`):
- Create revenue entity: `{'id': 'BEO_7736_REVENUE', 'name': 'BEO #7736营收', 'type': 'banquet_revenue', 'properties': {...}}`
- Link to monthly financial data

### 5. Report
```
=== BEO导入报告 ===
  BEO #{n}: {event_name}
  日期: {date} | 人数: {n} | 厅: {room}
  F&B收入: ¥{x} | 总营收: ¥{x}
  FB图谱: {n}实体, {k}关系
  FIN图谱: {n}实体, {k}关系
```

## Existing Data

Already imported BEOs (from `_raw_beo.txt`): BEO #7683, #7720, #7721, #7715, #7716, etc.
New BEOs should check for duplicates by BEO ID before importing.
