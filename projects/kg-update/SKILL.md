---
name: "kg-update"
description: "Update Y's 9-station knowledge graph: add entities, relations, backups"
---

# Knowledge Graph Updater

Automates updating Y's nine-station knowledge graph (knowledge_center/). When new data needs to be added to any station (FIN, FB, GSM, RISK, FSAA, MEP, QA, FAQ, LIB, CRM), this skill generates, validates, and applies the correct JSON mutation.

## Stations & Files

| Station | File | Entity keys | Core relation keys |
|---------|------|-------------|-------------------|
| FIN | `fin_graph.json` | id, name, type, properties | source_id, target_id, type |
| FB | `fb_graph.json` | id, name, year, month, properties | source_id, target_id, relation, id, type |
| FAQ | `faq_graph.json` | id, label, answer, tags, category | source, target, relation |
| GSM | `gsm_graph.json` | id, name, description, properties | source, type, target |
| RISK | `risk_graph.json` | id, label, category, description | source, relation, target |
| FSAA | `fsaa_graph.json` | id, label, name_en, category, description | source, type, target |
| MEP | `mep_graph.json` | id, label, name_en, category | source_id, target_id, relation |
| QA | `qa_graph.json` | id, label, name_cn, category, description | source_id, target_id, relation |
| LIB | `lib_graph.json` | id, label, type, name | source_id, target_id, relation |
| CRM | `fb_crm/crm_graph.json` | Check actual file | Check actual file |

## Workflow

### 1. Identify the target station
Based on what the user wants to add, determine which graph file(s) to modify.

### 2. Locate the graph file
All graph files are at `{workspace}/knowledge_center/{filename}`.

### 3. Generate the update code
Create a temporary Python script that:
- Loads the JSON file
- Adds new entities (checking for duplicates by id)
- Adds relations
- **Creates a backup** before writing: `{file}.bak.{timestamp}.json`
- Writes the updated JSON back
- Prints a summary (what was added, total sizes)

### 4. Validate
- Parse the JSON file before and after
- Verify new entities are present
- Verify new relations are present
- Print before/after entity and relation counts

### 5. Apply
Run the generated script. Confirm success.

## Code Template

```python
import json, os, shutil, datetime

workspace = r'C:\Users\Duke Wang\.openclaw\workspace'
kc = os.path.join(workspace, 'knowledge_center')
file_path = os.path.join(kc, '{filename}')

# Load
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entities = data.get('entities', [])
relations = data.get('relations', [])

# Backup
backup = f'{file_path}.bak.{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy2(file_path, backup)
print(f'Backup saved: {backup}')

# === ADD ENTITIES ===
new_entities = [...]
added_ents = 0
for ne in new_entities:
    if not any(e.get('id') == ne['id'] for e in entities):
        entities.append(ne)
        added_ents += 1

# === ADD RELATIONS ===
new_relations = [...]
added_rels = 0
for nr in new_relations:
    # check for duplicates
    is_dup = False
    for r in relations:
        if all(r.get(k) == nr.get(k) for k in nr.keys() if k != 'id'):
            is_dup = True
            break
    if not is_dup:
        relations.append(nr)
        added_rels += 1

data['entities'] = entities
data['relations'] = relations

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Added {added_ents} entities, {added_rels} relations')
print(f'Total: {len(entities)} entities, {len(relations)} relations')
```

## Safety Rules

1. **ALWAYS** create a timestamped backup before writing
2. **ALWAYS** check for duplicate entity IDs before adding
3. **ALWAYS** check for duplicate relations before adding
4. Print a clear summary of what changed
5. If the file can't be parsed, abort — don't overwrite

## Common Entity Templates

```python
# FIN station entity
{'id': 'DAILY_2026_06_15', 'name': '6月15日营收日报', 'type': 'daily_report', 'properties': {...}}

# FB station entity
{'id': 'MENU_ITEM_001', 'name': '红烧牛肉面', 'year': 2026, 'month': 6, 'period': 'dinner', 'properties': {'price': 68, 'cost': 22}}

# FAQ station entity
{'id': 'FAQ_001', 'label': '如何办理入住？', 'answer': '客人可在大堂前台办理入住...', 'tags': ['front', 'checkin'], 'category': 'faq'}

# GSM station entity
{'id': 'CASE_001', 'name': '客人投诉空调噪音', 'description': '深夜23:00...', 'properties': {...}}
```
