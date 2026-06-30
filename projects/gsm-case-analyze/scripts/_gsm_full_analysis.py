"""
GSM站全维分析 - 投诉处理知识体系
数据源: GSM知识图谱 + FAQ图谱
"""
import json, os
from collections import Counter, defaultdict

BASE = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center'

# 1. GSM图谱
with open(os.path.join(BASE, 'gsm_graph.json'), 'r', encoding='utf-8-sig') as f:
    gsm = json.load(f)

# 2. FAQ图谱（含投诉FAQ）
with open(os.path.join(BASE, 'faq_graph.json'), 'r', encoding='utf-8-sig') as f:
    faq = json.load(f)

print('=' * 60)
print('    苏州希尔顿 GSM投诉处理体系 · 全维分析')
print('    分析日期: 2026-05-07')
print('=' * 60)
print()

# ===== 实体分析 =====
entities = gsm['entities']
relations = gsm.get('relations', [])
rels_gsm = relations

print(f'【一、GSM站总览】')
print(f'  实体总数: {len(entities)}')
print(f'  关系总数: {len(rels_gsm)}')
print(f'  实体/关系比: {len(rels_gsm)/len(entities):.1f}')
print()

# 实体类型分布
type_counts = Counter()
for e in entities:
    t = e.get('type', 'unknown')
    type_counts[t] += 1

print(f'【二、实体类型分布】')
for t, c in type_counts.most_common():
    bar = '█' * (c // 10) if c > 0 else ''
    print(f'  {t:<15s}: {c:>4}  {bar}')

# 投诉类别分析
print(f'\n【三、投诉分类树】')
cats = Counter()
subcats = defaultdict(Counter)
for e in entities:
    props = e.get('properties', {})
    cat = props.get('category', props.get('投诉类别', ''))
    sub = props.get('subcategory', props.get('投诉子类别', ''))
    if cat:
        cats[cat] += 1
    if cat and sub:
        subcats[cat][sub] += 1

for cat, cnt in cats.most_common():
    print(f'\n  📂 {cat} ({cnt} 条)')
    if cat in subcats:
        for sub, scnt in subcats[cat].most_common(5):
            print(f'      └ {sub}: {scnt}')

# SOP分析
print(f'\n【四、SOP标准流程】')
sops = [e for e in entities if e.get('type') == 'sop']
print(f'  SOP总数: {len(sops)}')
for s in sops:
    props = s.get('properties', {})
    title = props.get('title', s.get('id', '?'))
    desc = str(props.get('description', ''))[:60]
    print(f'  📋 {title}: {desc}')

# 关系类型分析
print(f'\n【五、关系图谱分析】')
rel_types = Counter()
for r in rels_gsm:
    rt = r.get('type', r.get('relation', 'unknown'))
    rel_types[rt] += 1

for rt, cnt in rel_types.most_common(10):
    bar = '▅' * (cnt // 30)
    print(f'  {rt:<20s}: {cnt:>4}  {bar}')

# 跨站联动分析
print(f'\n【六、跨站联动能力】')
# 找连接到其他站的实体
# 从关系找目标实体类型
target_types = Counter()
all_ent_types = {e['id']: e.get('type', '?') for e in entities}
for r in rels_gsm:
    tid = r.get('target', '')
    if tid in all_ent_types:
        tt = all_ent_types[tid]
    else:
        tt = 'external'
    target_types[tt] += 1

print(f'  关联的实体类型:')
for tt, cnt in target_types.most_common(10):
    print(f'    → {tt:<15s}: {cnt} 次')

# 法律法规关联
print(f'\n【七、法律法规框架】')
laws = [e for e in entities if e.get('type') in ('regulation', 'law', 'legal')]
print(f'  关联法律法规: {len(laws)} 条')
for l in laws:
    props = l.get('properties', {})
    name = props.get('name', l.get('id', '?'))
    print(f'  ⚖️ {name}')

# 投诉趋势分析（从案例中提取关键词）
print(f'\n【八、投诉趋势洞察】')
case_keywords = Counter()
for e in entities:
    if e.get('type') == 'case':
        desc = str(e.get('properties', {}).get('description', ''))
        for kw in ['噪音', '空调', '态度', '效率', '设施', '清洁', '水质', '虫害', 
                    '电梯', '漏水', '停车', '行李', '泳池', '赔偿', '投诉']:
            if kw in desc:
                case_keywords[kw] += 1

print(f'  案例高频词:')
for kw, cnt in case_keywords.most_common():
    print(f'    {kw}: {cnt} 次')

print(f'\n【九、FAQ知识覆盖】')
# FAQ中与投诉相关的
faq_ents = faq.get('entities', [])
complaint_faqs = [e for e in faq_ents if '投诉' in str(e.get('properties', {})) or 'GSM' in str(e.get('id',''))]
print(f'  投诉相关FAQ: {len(complaint_faqs)} 条')

# 整体评分
print(f'\n【十、GSM站综合评分】')
scores = {
    '实体完整性':     min(100, len(entities) // 8 * 10),
    '关系密度':       min(100, int(len(rels_gsm) / len(entities) * 30)),
    'SOP覆盖度':      min(100, len(sops) * 15),
    '法律框架':       min(100, len(laws) * 20),
    '分类体系':       min(100, len(cats) * 15),
    '跨站联动':       min(100, len(target_types) * 15),
}
total = sum(scores.values()) / len(scores)
print(f'  {"项目":<15s} {"评分":>5s} {"状态"}')
print(f'  {"":-<25s}')
for k, v in scores.items():
    bar = '🟢' if v >= 70 else ('🟡' if v >= 40 else '🔴')
    print(f'  {k:<15s}: {v:>3d}  {bar}')
print(f'  {"综合评分":<15s}: {total:.1f}  {"A" if total>=80 else "B" if total>=60 else "C"}级运营可用')

print(f'\n{"="*60}')
print(f'分析完毕')
print(f'{"="*60}')
