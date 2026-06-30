#!/usr/bin/env python3
"""FSAA 每日状态检查脚本"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fsaa_graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

entities = data.get('entities', [])
rels = data.get('relationships', [])

print("FSAA 图谱概览")
print("=" * 40)
print(f"实体: {len(entities)}")
print(f"关系: {len(rels)}")

from collections import Counter
types = Counter()
for e in entities:
    t = e.get('type', 'unknown')
    types[t] += 1
print("\n类型分布:")
for t, c in types.most_common():
    print(f"  {t}: {c}")

kitchen = [e for e in entities if '厨房' in str(e.get('name',''))]
print(f"\n厨房实体 ({len(kitchen)}):")
for e in kitchen:
    print(f"  - {e.get('name','')}")

nc = [e for e in entities if e.get('name','').startswith('NC_')]
print(f"\n不符合项 ({len(nc)}):")
for e in nc:
    print(f"  - {e.get('name','')}")

al = [e for e in entities if '过敏' in str(e.get('name','')) or 'allerg' in str(e.get('name','')).lower()]
print(f"\n过敏原相关 ({len(al)}):")
for e in al:
    print(f"  - {e.get('name','')}")

hygiene = [e for e in entities if any(k in str(e.get('name','')).lower() for k in ['卫生','洗手','hygiene','hand','清洁','clean','消毒'])]
print(f"\n卫生检查点 ({len(hygiene)}):")
for e in hygiene[:20]:
    print(f"  - {e.get('name','')}")

# find last update info 
print(f"\n关系类型分布:")
rel_types = Counter()
for r in rels:
    t = r.get('type', 'unknown')
    rel_types[t] += 1
for t, c in rel_types.most_common():
    print(f"  {t}: {c}")
