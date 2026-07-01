#!/usr/bin/env python3
"""
QA图谱自检脚本 — 完整性自查 + 问题诊断 + 自动修复
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'[LOCAL_USER_PATH] Wang\.openclaw\workspace\knowledge_center\qa_graph.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

entities = d.get('entities', [])
edges = d.get('edges', [])
errors = []
warnings = []
fixes = []

entity_by_id = {e['id']: e for e in entities}
all_node_ids = set()
for e in edges:
    all_node_ids.add(e.get('source_id',''))
    all_node_ids.add(e.get('target_id',''))

# ============ 1. 孤岛实体检查 ============
# Which entities have key patterns that should be connected
section_ids = [e['id'] for e in entities if e.get('type') == 'qa_section']
standard_count_targets = {}
for e in entities:
    if e.get('type') == 'qa_section' and 'standard_count' in e.get('properties',{}):
        try:
            standard_count_targets[e['id']] = int(e['properties']['standard_count'])
        except:
            pass

print("="*60)
print("QA图谱自检报告")
print("="*60)

print(f"\n📊 基本统计")
print(f"  实体: {len(entities)}")
print(f"  关系: {len(edges)}")
print(f"  版本: {d['meta'].get('version','?')}")

# Section connection check
print(f"\n🔍 Section关联检查")
for sid in sorted(section_ids):
    conn_count = sum(1 for e in edges if e.get('source_id')==sid or e.get('target_id')==sid)
    target = standard_count_targets.get(sid, '?')
    status = "✅" if conn_count > 0 else "❌"
    e_name = entity_by_id.get(sid,{}).get('name','?')[:40]
    print(f"  {status} {sid} ({e_name}) → {conn_count} relations, expected ~{target} standards")

# ============ 2. 悬空引用检查 ============
print(f"\n🔍 悬空引用检查（边的端点不在实体列表中）")
orphan_refs = []
for e in edges:
    s = e.get('source_id','')
    t = e.get('target_id','')
    if s not in entity_by_id:
        orphan_refs.append((s, t, e.get('relation','')))
    if t not in entity_by_id:
        orphan_refs.append(('', t, e.get('relation','')))
if orphan_refs:
    print(f"  ⚠️ 发现 {len(orphan_refs)} 个悬空引用：")
    for s,t,r in orphan_refs[:10]:
        print(f"     {s or '?'} → {r} → {t}")
else:
    print(f"   ✅ 所有边的两端均在实体列表中")

# ============ 3. 重复边检查 ============
print(f"\n🔍 重复边检查")
seen_pairs = {}
dup_edges = []
for e in edges:
    key = (e.get('source_id',''), e.get('relation',''), e.get('target_id',''))
    if key in seen_pairs:
        dup_edges.append(key)
    seen_pairs[key] = True
if dup_edges:
    print(f"  ⚠️ 发现 {len(dup_edges)} 条重复边：")
    for k in dup_edges[:5]:
        print(f"     {k[0]} → {k[1]} → {k[2]}")
else:
    print(f"   ✅ 无重复边")

# ============ 4. 孤立Section关键实体检查 ============
print(f"\n🔍 Section关键实体存在性检查")
missing_entities = []
for eid in all_node_ids:
    if eid not in entity_by_id:
        missing_entities.append(eid)
if missing_entities:
    print(f"  ⚠️ 边中引用了 {len(missing_entities)} 个不存在于实体列表的ID（可能是其他站的实体）：")
    for me in missing_entities[:10]:
        print(f"     {me}")
else:
    print(f"   ✅ 所有引用ID都在实体列表中")

# ============ 5. 关系网络密度 ============
print(f"\n🔍 关系网络分析")
connected_entities = len(all_node_ids & set(entity_by_id.keys()))
isolated_entities = len(entity_by_id) - connected_entities
density = len(edges) / max(connected_entities, 1)
print(f"  已连接实体: {connected_entities}/{len(entities)} ({connected_entities/len(entities)*100:.1f}%)")
print(f"  孤立实体: {isolated_entities}")
print(f"  关系密度: {density:.2f} 边/节点")

# 检查每个模块的覆盖率
print(f"\n🔍 模块覆盖率")
modules = [e for e in entities if e.get('type') == 'qa_module']
print(f"  模块数: {len(modules)}")
for m in modules:
    mid = m['id']
    conn = [e for e in edges if e.get('source_id')==mid or e.get('target_id')==mid]
    print(f"    {mid} → {len(conn)} 条边")

# Check scoring entities
print(f"\n🔍 评分实体覆盖")
scores = [e for e in entities if e.get('type') == 'qa_score']
connected_scores = [s for s in scores if s['id'] in all_node_ids]
unconnected_scores = [s for s in scores if s['id'] not in all_node_ids]
print(f"  总分评实体: {len(scores)}")
print(f"  已关联: {len(connected_scores)} / 未关联: {len(unconnected_scores)}")
for us in unconnected_scores[:5]:
    print(f"    ❌ {us['id']}: {us.get('name','?')[:50]}")

# ============ 6. 操作卡映射检查 ============
print(f"\n🔍 操作卡关联检查")
checklist_files = [
    ('早餐', 'QA_BREAKFAST_CHECKLIST.md', ['QA_BS_42000','QA_BS_42001','QA_BS_42002','QA_BS_42003','QA_BS_42008','QA_BS_42009','QA_BS_42010']),
    ('康乐', 'QA_POOL_CHECKLIST.md', ['QA_BS_500','QA_BS_50100','QA_BS_50200','QMOD_POOL']),
    ('酒廊', 'QA_LOUNGE_CHECKLIST.md', ['QA_BS_41000','QA_BS_410','QA_BS_11100']),
    ('客房', 'QA_ROOM_CHECKLIST.md', ['QA_BS_200','QA_BS_300','QA_BS_700','QA_BS_30100','QA_BS_30400','QA_BS_30900']),
    ('品牌', 'QA_BRAND_CHECKLIST.md', ['QA_BS_100','QA_BS_10600','QA_BS_800','QA_BRAND_STANDARDS_2026']),
    ('会议', 'QA_MEETING_CHECKLIST.md', ['QA_BS_600','QA_BS_60100','QA_BS_60200']),
    ('安全', 'QA_SAFETY_CHECKLIST.md', ['QA_BS_900','QA_BS_90200','QA_BS_90400','QA_BS_90700','QA_BS_91000']),
]
for name, fname, core_ids in checklist_files:
    missing = [eid for eid in core_ids if eid not in entity_by_id]
    disconnected = []
    for eid in core_ids:
        if eid in entity_by_id:
            conn = sum(1 for e in edges if e.get('source_id')==eid or e.get('target_id')==eid)
            if conn == 0:
                disconnected.append(eid)
    if missing or disconnected:
        print(f"  ⚠️ {name}:")
        if missing: print(f"    缺失实体: {missing}")
        if disconnected: print(f"    孤岛实体: {disconnected}")
    else:
        print(f"   ✅ {name}: {fname} 关联正常")

# ============ 7. 关系类型分析 ============
print(f"\n🔍 关系类型分布")
rel_types = {}
for e in edges:
    rt = e.get('relation','unknown')
    rel_types[rt] = rel_types.get(rt,0) + 1
for rt, cnt in sorted(rel_types.items(), key=lambda x:-x[1]):
    print(f"   {rt}: {cnt}")

# ============ 8. 自我修正建议 ============
print(f"\n🔧 自我修正建议")
quality_score = 100
# 孤立实体扣分
if isolated_entities > 0:
    penalty = min(isolated_entities, 50)
    quality_score -= penalty
    print(f"  ❌ 孤立实体 {isolated_entities} 个 → 扣{penalty}分")
# 悬空引用扣分
if orphan_refs:
    penalty = min(len(orphan_refs), 20)
    quality_score -= penalty
    print(f"  ❌ 悬空引用 {len(orphan_refs)} 个 → 扣{penalty}分")
# 重复边扣分  
if dup_edges:
    penalty = min(len(dup_edges), 10)
    quality_score -= penalty
    print(f"  ❌ 重复边 {len(dup_edges)} 条 → 扣{penalty}分")
# 未关联评分实体
if unconnected_scores:
    print(f"  ❌ {len(unconnected_scores)}个评分实体未关联Section")
# 密度加分
if density >= 0.3:
    quality_score += 5
    print(f"  ✅ 关系密度 {density:.2f} ≥ 0.3 → +5分")
# Section全连加分
connected_sections = sum(1 for sid in section_ids if sid in all_node_ids)
if connected_sections == len(section_ids) and len(section_ids) > 0:
    quality_score += 10
    print(f"  ✅ 全部Section已连通 → +10分")

print(f"\n{'='*60}")
print(f"🏆 QA图谱质量评分: {max(0, quality_score)}/100")
print(f"{'='*60}")
