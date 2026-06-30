#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fsaa_graph.json','r',encoding='utf-8') as f:
    d = json.load(f)

es = d.get('entities',[])
rels = d.get('relationships',[])

print("=== FSAA 专项查询 ===")
print(f"总实体: {len(es)}, 总关系: {len(rels)}")

# Find entity names containing 2026/4月 etc
for e in es:
    n = e.get('name','')
    if '2026' in n or '4月' in n or 'April' in n or '22' in n:
        print(f"  [{e.get('type','')}] {n}")

# Look for all fsaa_entity types
print("\n=== fsaa_entity 列表 ===")
for e in es:
    if e.get('type') == 'fsaa_entity':
        print(f"  - {e.get('name','')}")

# Look for audit_scope 
print("\n=== audit_scope 列表 ===")
for e in es:
    if e.get('type') == 'audit_scope':
        print(f"  - {e.get('name','')}")

# Find last 10 entities by name alphabetical 
print("\n=== 最后10个实体名 ===")
names = sorted([e.get('name','') for e in es])
for n in names[-10:]:
    print(f"  - {n}")
