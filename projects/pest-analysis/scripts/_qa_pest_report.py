"""
QA第三检查 · 虫害问题报告
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

from collections import Counter, defaultdict

BASE = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center'
fp = os.path.join(BASE, 'qa_graph.json')
with open(fp, 'r', encoding='utf-8-sig') as f:
    qa = json.load(f)

ents = qa['entities']
rels = qa.get('relations', [])

print('='*65)
print('    苏州希尔顿 · QA第三检查 · 虫害问题报告')
print('    分析日期: 2026-05-07')
print('='*65)
print()

# ====== 1. 虫害相关实体全搜索 ======
print('【一、QA站虫害相关实体】')

pest_kw = ['虫','pest','蟑螂','cockroach','老鼠','鼠','rat','蚂蚁','ant',
           '苍蝇','fly','蚊子','mosquito','消杀','pest control','虫害',
           '卫生','hygiene','sanitation','清洁','clean','消毒','disinfect',
           '防虫','灭虫','除虫']

pest_ents = []
for e in ents:
    eid = e.get('id','?')
    props = e.get('properties',{})
    text = eid + ' ' + json.dumps(props, ensure_ascii=False)
    matched = [kw for kw in pest_kw if kw.lower() in text.lower()]
    if matched:
        pest_ents.append((e, matched))

# 按类型归类
by_type = defaultdict(list)
for e, matches in pest_ents:
    t = e.get('type','?')
    by_type[t].append((e, matches))

for t, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
    print(f'\n  类型 {t}: {len(items)} 个')
    for e, matches in items[:5]:
        eid = e.get('id','?')
        props = e.get('properties',{})
        # 找到属性中有价值的内容
        desc = ''
        for k in ['name','title','section','description','标准','要求','检查项','频率','label']:
            v = props.get(k,'')
            if v:
                desc = str(v)[:80]
                break
        kw_str = ','.join(set(matches[:3]))
        print(f'    └ {eid} ({kw_str})')
        if desc:
            print(f'       {desc}')
print()

# ====== 2. 检查项分析 ======
print('【二、虫害检查项分布】')

# 结构: section -> module -> check_item -> standard
sections = [e for e in ents if e.get('type') == 'qa_section']
modules = [e for e in ents if e.get('type') == 'qa_module']
standards = [e for e in ents if e.get('type') == 'qa_standard']
check_items = [e for e in ents if e.get('type') == 'qa_check_item']

print(f'  Section（大章）: {len(sections)}')
for s in sections:
    print(f'    📂 {s["id"]}: {s.get("properties",{}).get("name","")}')

print(f'\n  Module（模块）: {len(modules)}')
# 找与虫害相关的模块
for m in modules:
    mid = m['id']
    name = m.get('properties',{}).get('name','')
    for kw in ['clean','卫生','虫','pest']:
        if kw.lower() in mid.lower() or kw.lower() in name.lower():
            print(f'    📋 {mid}: {name}')
            break
print()

# ====== 3. 虫害标准 ======
print('【三、虫害相关标准】')
pest_standards = []
for e in pest_ents:
    if e[0].get('type') in ('qa_standard', 'Standard'):
        pest_standards.append(e[0])

print(f'  虫害相关标准: {len(pest_standards)}')
for s in pest_standards:
    props = s.get('properties',{})
    name = props.get('name','') or props.get('标准','')
    section = props.get('section','')
    freq = props.get('frequency',props.get('频率',''))
    score = props.get('score',props.get('分值',''))
    print(f'    📏 {s["id"]}')
    if name: print(f'       标准: {str(name)[:60]}')
    if section: print(f'       章节: {section}')
    if freq: print(f'       频率: {freq}')
    if score: print(f'       分值: {score}')
print()

# ====== 4. 具体检查项 ======
print('【四、虫害检查细项】')
pest_checks = []
for e in pest_ents:
    if e[0].get('type') == 'qa_check_item':
        pest_checks.append(e[0])

print(f'  虫害检查项: {len(pest_checks)}')
for c in pest_checks[:15]:
    props = c.get('properties',{})
    check = props.get('检查项','') or props.get('description','') or props.get('name','')
    print(f'    ✅ {c["id"]}: {str(check)[:80]}')
print()

# ====== 5. QA站虫害关系 ======
print('【五、虫害知识关联】')
pest_ids = {e.get('id') for e,_ in pest_ents}
pest_rels = [r for r in rels if r.get('source') in pest_ids or r.get('target') in pest_ids]
print(f'  虫害实体间关系: {len(pest_rels)}')

# 关系类型
rel_types = Counter(r.get('type','?') for r in pest_rels)
for t, c in rel_types.most_common(10):
    print(f'    {t}: {c}')
print()

# ====== 6. QA vs FSAA 虫害标准对比 ======
print('【六、QA与FSAA虫害体系覆盖对比】')
fsaa_fp = os.path.join(BASE, 'fsaa_graph.json')
with open(fsaa_fp, 'r', encoding='utf-8-sig') as f:
    fsaa = json.load(f)

pest_fsaa = []
for e in fsaa['entities']:
    text = e.get('id','') + ' ' + json.dumps(e.get('properties',{}), ensure_ascii=False)
    for kw in ['pest','虫','消杀','卫生','hygiene']:
        if kw.lower() in text.lower():
            pest_fsaa.append(e)
            break

qa_pest_count = len(pest_ents)
fsaa_pest_count = len(pest_fsaa)
print(f'  QA站虫害相关: {qa_pest_count} 实体')
print(f'  FSAA站虫害相关: {fsaa_pest_count} 实体')
print(f'  差距: FSAA比QA多 {fsaa_pest_count - qa_pest_count} 个虫害实体')
print()
print(f'  QA站侧重领域:')
qa_areas = Counter(e.get('type','') for e,_ in pest_ents)
for area, cnt in qa_areas.most_common(10):
    print(f'    {area}: {cnt}')

print()
print(f'  FSAA站侧重领域:')
fsaa_areas = Counter(e.get('type','') for e in pest_fsaa)
for area, cnt in fsaa_areas.most_common(10):
    print(f'    {area}: {cnt}')

# ====== 7. 问题总结 ======
print(f'\n【七、发现的问题总结】')
issues = []
for e,_ in pest_ents:
    props = e.get('properties',{})
    desc = str(props.get('description','') or props.get('标准','') or props.get('检查项',''))
    for flag in ['问题','未达标','不符合','未发现','缺失','待整改','improve','fail','non-compliance','gap']:
        if flag.lower() in desc.lower():
            issues.append((e.get('id','?'), desc[:100]))
            break

if issues:
    print(f'  发现 {len(issues)} 个虫害相关问题记录:')
    for eid, desc in issues[:10]:
        print(f'    ⚠️ {eid}: {desc}')
else:
    print(f'  在QA站未发现明确的虫害未达标记录')
    print(f'  （可能问题记录在源文档中，图谱中未直接标注）')

print(f'\n{"="*65}')
print('报告完毕')
print(f'{"="*65}')
