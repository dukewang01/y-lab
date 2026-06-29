---
name: "kc-healthcheck"
description: "Health checks on all KG files: size, integrity, orphans, anomalies"
---

# Knowledge Center Health Check

Runs comprehensive health checks on all knowledge graph files in `knowledge_center/`. Detects issues, tracks trends over time, and provides actionable maintenance recommendations.

## Checks Performed

### 1. Size & Scale
For each graph file:
- File size (KB/MB)
- Entity count
- Relation count
- Entity/relation ratio

### 2. Integrity Check
- Missing `id` fields on entities
- Missing `source`/`target` on relations
- Duplicate entity IDs
- Relations pointing to non-existent entities (orphans)
- Relations pointing to deleted entities

### 3. Station Coverage
- Entity type distribution within each station
- Domain coverage (are all required types present?)
- Comparison to previous health scan

### 4. Cross-Station Consistency
- `fin_graph.json` ↔ `fb_graph.json`: do revenue figures match?
- `gsm_graph.json` ↔ `risk_graph.json`: are complaint cases mirrored in risk?
- `faq_graph.json`: does every FAQ reference an existing entity?

### 5. Recommendations
- Which files need compaction (too many backups?)
- Which types are under-represented
- Orphan cleanup suggestions

## Output Format

```
============================================================
  知识图谱健康扫描报告
  {date}
============================================================

📊 整体规模
  总文件: {n}
  总实体: {n}
  总关系: {n}
  总大小: {n}MB

🏛️ 各站状态
  {station}: {n}实体 / {n}关系 / {size}KB — ✅/⚠️/❌
  ...

🔍 发现的问题 ({n})
  ❌ {n}个孤立关系（指向不存在的实体）
  ⚠️ {n}个重复实体ID
  ⚠️ {n}个缺少类型字段的实体
  ...

📈 趋势变化（vs上次扫描）
  实体增长: +{n}
  关系增长: +{n}

💡 建议
  ...
```

## Script Template

```python
import json, os

BASE = 'knowledge_center'
graphs = ['mep_graph','fsaa_graph','risk_graph','qa_graph','fin_graph','fb_graph','lib_graph','gsm_graph','faq_graph']

print('=== 知识图谱健康度扫描 ===')
issues = []
for g in graphs:
    fp = os.path.join(BASE, g+'.json')
    if not os.path.exists(fp):
        print(f'  {g}: NOT FOUND ❌')
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ents = data.get('entities', [])
    rels = data.get('relations', []) + data.get('relationships', [])
    sz = os.path.getsize(fp) / 1024
    
    # Check for issues...
    missing_ids = [e for e in ents if not e.get('id')]
    ...

print(f'{len(issues)} issues found')
```
