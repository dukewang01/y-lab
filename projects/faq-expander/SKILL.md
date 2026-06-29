---
name: "faq-expander"
description: "Auto-generate FAQ entries from station knowledge for FAQ graph"
---

# FAQ Expander

Automatically generates FAQ (Q&A) entries for the FAQ knowledge graph based on existing entities in other stations. Takes station entities and converts them into natural-language question-answer pairs.

## Data Source

- FAQ graph: `knowledge_center/faq_graph.json`
- Source stations: FB, FIN, GSM, FSAA, RISK, MEP, QA, LIB graphs
- Cross-references existing FAQ entries to avoid duplicates

## Workflow

### 1. Select target station(s)
User specifies which station's knowledge to FAQ-ize: FB, FIN, GSM, etc.

### 2. Extract source entities
Load the station graph and pull entities that would make good FAQs:
- FB: menu items, products, promotions
- FIN: revenue metrics, budget data, DRR insights
- GSM: case categories, SOPs, procedures
- FSAA: check items, standards
- RISK: risk items, mitigation plans
- MEP: maintenance schedules, equipment
- QA: brand standards, audit items
- LIB: book summaries, key concepts

### 3. Generate Q&A pairs
For each entity, create:
- `id`: `FAQ_{STATION}_{TOPIC}`
- `label`: Natural language question
- `answer`: Structured answer with key facts
- `tags`: Station + relevant tags
- `category`: `faq`

### 4. Add to FAQ graph
- Check for duplicates by `label` (similarity check)
- Add entity to `entities`
- Add `TAGGED_AS` relations to station tags
- Add `references` relations to source entities

### 5. Report
```
=== FAQ扩充报告 ===
来源: {station}站
新增FAQ: {n}条
总FAQ: {n}条
新增关系: {n}条

示例:
  Q: {question}
  A: {answer[:80]}...
```

## Q&A Generation Templates

For **FB** station (menu/products):
- "Q: 酒店有哪些{category}?" / "A: ..."
- "Q: {product}价格是多少?" / "A: ..."
- "Q: 什么时间提供{service}?" / "A: ..."

For **FIN** station (revenue):
- "Q: {month}月营收是多少?" / "A: ..."
- "Q: {metric}预算完成率?" / "A: ..."
- "Q: 最好的{period}是哪天?" / "A: ..."

For **GSM** station (complaints):
- "Q: 遇到{issue}怎么处理?" / "A: ..."
- "Q: {issue}的赔偿标准是什么?" / "A: ..."
