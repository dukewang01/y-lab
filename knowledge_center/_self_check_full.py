import json, os

base = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
files_info = {}
for fn in os.listdir(base):
    if fn.endswith('_graph.json'):
        fp = os.path.join(base, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            d = json.load(f)
        ents = len(d.get('entities', []))
        rels = len(d.get('relations', [])) + len(d.get('relationships', []))
        size_kb = os.path.getsize(fp) / 1024
        files_info[fn] = {'entities': ents, 'relations': rels, 'size_kb': size_kb, 'data': d}

print('=' * 62)
print('  Y酒店运营体系 — 全链实战诊断')
print('=' * 62)
print()

# ---- 1. 基础统计 ----
print('━━━ 1. 基础规模统计')
total_ent = 0
total_rel = 0
total_kb = 0
for fn, info in sorted(files_info.items()):
    total_ent += info['entities']
    total_rel += info['relations']
    total_kb += info['size_kb']
    print(f'  {fn[:15]:15s}  实体:{info["entities"]:>5d}  关系:{info["relations"]:>5d}  {info["size_kb"]:>7.1f}KB')
print(f'  {"─"*48}')
print(f'  {"合计":>15s}  实体:{total_ent:>5d}  关系:{total_rel:>5d}  {total_kb:>7.1f}KB')
print()

# ---- 2. 跨站搜索测试 ----
print('━━━ 2. 跨站搜索测试 — 戒指丢失')

# FAQ -> search
d = files_info['faq_graph.json']['data']
found = [e for e in d['entities'] if 'FAQ_RISK_RING_LOST' in e.get('id', '')]
if found:
    e = found[0]
    print(f'  ✅ FAQ_RISK_RING_LOST: {e["label"]}')
    print(f'     标签: {e["tags"]}')
    print(f'     来源: {e["source"]}')
    # 追踪relations
    rels = d.get('relations', [])
    refs = [r for r in rels if r.get('source_id') == 'FAQ_RISK_RING_LOST']
    print(f'     关系({len(refs)}条):')
    for r in refs:
        print(f'       TAGGED_AS -> {r["target_id"]}')
else:
    print('  ❌ FAQ_RISK_RING_LOST 未找到')

# 搜"失物"
print()
d2 = files_info['faq_graph.json']['data']
lost_kws = ['失物', '丢失', '遗失', 'lost']
lost_hits = [e for e in d2['entities'] if any(k in (e.get('label', '') + e.get('answer', '')) for k in lost_kws)]
print(f'  搜"失物/丢失"命中: {len(lost_hits)}条')
for e in lost_hits[:6]:
    a = e.get('answer', '')[:60].replace('\n', ' ')
    print(f'    {e["id"]}: {e.get("label","")[:40]} | {a}')

# ---- 3. MEP -> FSAA -> Risk 跨站查询 ----
print()
print('━━━ 3. 跨站链路查询 — 厨房')

d_mep = files_info['mep_graph.json']['data']
d_fsaa = files_info['fsaa_graph.json']['data']
d_risk = files_info['risk_graph.json']['data']

# MEP厨房参数
mep_kitchen = [e for e in d_mep['entities'] if '厨房' in e.get('label', '')]
print(f'  MEP厨房参数: {len(mep_kitchen)}项')
for e in mep_kitchen[:10]:
    print(f'    {e["id"]}: {e["label"]}')

# FSAA厨房分布
fsaa_kitchen = [e for e in d_fsaa['entities'] if e.get('category') == 'area' and '厨房' in e.get('label', '')]
print()
print(f'  FSAA厨房区域: {len(fsaa_kitchen)}个')
for e in fsaa_kitchen:
    print(f'    {e["id"]}: {e["label"]} [{e.get("name_en","")}]')

# Risk餐饮预案
risk_food = [e for e in d_risk['entities'] if e.get('type') in ['security_procedure', 'emergency_plan'] and '食物' in e.get('name', '')]
print()
print(f'  RISK餐饮预案: {len(risk_food)}个')
for e in risk_food:
    print(f'    {e["id"]}: {e["name"]}')

# ---- 4. FAQ厨房搜索 ----
print()
print('━━━ 4. FAQ搜索 — 厨房')
d_faq = files_info['faq_graph.json']['data']
kitchen_faq = [e for e in d_faq['entities'] if 'kitchen' in e.get('tags', []) or '厨房' in e.get('label', '') or '餐厅' in e.get('label', '')]
print(f'  厨房/餐厅FAQ: {len(kitchen_faq)}条')
for e in kitchen_faq[:10]:
    a = e.get('answer', '')[:50].replace('\n', ' ')
    print(f'    {e["id"]}: {e.get("label","")[:40]}')

# ---- 5. QA SALT早餐数据 ----
print()
print('━━━ 5. QA SALT早餐趋势')
d_qa = files_info['qa_graph.json']['data']
salt_items = [e for e in d_qa['entities'] if e.get('category') == 'salt_data']
salt_names = set(e.get('name', '') for e in salt_items)
print(f'  SALT数据条目: {len(salt_items)}条')
for n in sorted(salt_names):
    print(f'    {n}')

# ---- 6. 模板文件 ----
print()
print('━━━ 6. 模板与产出')
templates_dir = os.path.join(base, 'templates')
templates = [f for f in os.listdir(templates_dir) if f.endswith('.md')] if os.path.isdir(templates_dir) else []
print(f'  模板文件: {len(templates)}个')
for t in templates:
    fsize = os.path.getsize(os.path.join(templates_dir, t))
    print(f'    {t} ({fsize}字节)')

# ---- 7. 自检摘要 ----
print()
print('=' * 62)
print('  自检结论')
print('=' * 62)
checks = [
    ('FAQ图谱健康', len(files_info.get('faq_graph.json', {}).get('data', {}).get('entities', [])) > 800),
    ('RISK图谱健康', len(files_info.get('risk_graph.json', {}).get('data', {}).get('entities', [])) > 800),
    ('FSAA图谱健康', len(files_info.get('fsaa_graph.json', {}).get('data', {}).get('entities', [])) > 800),
    ('MEP图谱健康', len(files_info.get('mep_graph.json', {}).get('data', {}).get('entities', [])) > 800),
    ('QA图谱健康', len(files_info.get('qa_graph.json', {}).get('data', {}).get('entities', [])) > 300),
    ('戒指FAQ条目', 'FAQ_RISK_RING_LOST' in [e.get('id','') for e in d['entities']]),
    ('厨房布局FAQ', 'FAQ_KITCHEN_LAYOUT' in [e.get('id','') for e in d_faq['entities']]),
    ('模板文件', len(templates) > 0),
    ('跨站引用', any('references' in str(r) for r in files_info['faq_graph.json']['data'].get('relationships', []))),
    ('SALT数据', len(salt_items) > 20),
]
for name, ok in checks:
    icon = '✅' if ok else '❌'
    print(f'  {icon} {name}')
print()
all_ok = all(c[1] for c in checks)
print(f'  通过率: {sum(1 for c in checks if c[1])}/{len(checks)}')
print(f'  综合结论: {"✅ 运营体系健康，全链可用" if all_ok else "⚠️ 部分节点需要关注"}')
