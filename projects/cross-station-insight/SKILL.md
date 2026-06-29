---
name: "cross-station-insight"
description: "Cross-station reasoning engine: connect FIN/FB/GSM/FSAA/MEP/QA for insights"
---

# Cross-Station Insight

Connects data across all knowledge stations to generate non-obvious, synthetic insights that no single station can provide alone. The "aha" engine.

## Core Concept

Each station is a silo. The most valuable insights live at the **intersections**.

## Built-in Reasoning Chains

### Chain 1: Cost → Menu → Pricing → Guest Sentiment
```
FIN (cost up) → FB (menu prices) → GSM (complaints about pricing)
```
When raw material costs rise (FIN), check if menu prices were adjusted (FB), and whether price complaints spiked (GSM).

### Chain 2: PCO Finding → Guest Complaint → Risk Level → Maintenance Action
```
FSAA (roach found in kitchen) → GSM (pest complaint in room) → RISK (escalate) → MEP (schedule fumigation)
```
When PCO finds pests in kitchen, check GSM for related guest complaints, update risk level in RISK, and trigger MEP maintenance.

### Chain 3: Revenue Drop → F&B Promo → Effectiveness
```
FIN (revenue below budget) → FB (active promotions) → FIN (promo ROI) → Recommendation
```
When revenue drops, check if FB promos are running, calculate their ROI from FIN data, suggest changes.

### Chain 4: Complaints → QA Standards → MEP Fix
```
GSM (AC complaint spike) → QA (air quality standard) → MEP (AC maintenance log) → Resolution
```
When AC complaints spike (GSM), check QA standards for compliance, consult MEP maintenance logs, recommend action.

### Chain 5: VIP Guest → Preferences → Spend Trend → Risk
```
CRM (guest profile) + FB (preferences) + FIN (spend history) + GSM (complaints) → Action
```
For each VIP guest, cross-reference across all four stations.

## Workflow

### 1. Identify the signal
User asks a question or mentions an event (e.g., "6月营收不好", "最近投诉很多").

### 2. Map to reasoning chains
Which chain(s) apply? Extract intent keywords:
- Cost/pricing → Chain 1
- Pest/insect → Chain 2
- Revenue/low → Chain 3
- AC/noise/hotel → Chain 4
- Guest name/VIP → Chain 5

### 3. Execute multi-station query
Load and query each relevant graph.

### 4. Synthesize
Generate the cross-station insight and recommendation.

## Query Examples

User: "最近BACIO生意不好"
→ Chain 1 + 3: FIN check BACIO revenue trends → FB check menu/pricing → GSM check complaints → suggest

User: "为什么6月周末Occ这么低"
→ Chain 3: FIN check weekend Occ → FB check if promos covered weekends → GSM check if events/competition → insight

User: "林先生好久没来了"
→ Chain 5: CRM check last visit → GSM check past complaints → FIN check spend trend → recall plan

## Output Format

```
============================================================
  [Cross-Station Insight]
============================================================

🔗 推理链: {chain name}

📊 数据汇聚:
  FIN: {finding}
  FB:  {finding}  
  GSM: {finding}
  ... 

💡 洞察:
  {synthesized insight}

🎯 建议:
  - {action 1}
  - {action 2}
```
