import json, os

BASE = 'C:\\Users\\Y\\.openclaw\\workspace\\knowledge_center'

graphs = ['mep_graph','fsaa_graph','risk_graph','qa_graph','fin_graph','fb_graph','lib_graph','gsm_graph','faq_graph']

print('=== 图谱健康�?===')
issues = []
for g in graphs:
    fp = os.path.join(BASE, g+'.json')
    with open(fp,'r',encoding='utf-8-sig') as f:
        d = json.load(f)
    ents = len(d.get('entities',[]))
    rels = d.get('relations',[]) or d.get('relationships',[])
    rels_count = len(rels)
    sz = os.path.getsize(fp)/1024
    
    # 检查关系键�?    if rels:
        sample = rels[0]
        has_source = 'source' in sample
        has_from = 'from' in sample
        has_target = 'target' in sample
        has_to = 'to' in sample
        key_info = 'OK' if (has_source or has_from) else 'WARN'
    else:
        key_info = 'NO_RELS'
    
    # 实体类型分布 - 使用d.get('entities',[])
    type_counts = {}
    for e in d.get('entities',[]):
        t = e.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f'  {g:<12s}: {ents:>5}实体  {rels_count:>6}关系  {sz:>7.0f}KB  schema:{key_info}')

print()
print('=== CRM �?===')
crm_dir = os.path.join(BASE, 'fb_crm')
if os.path.exists(crm_dir):
    crm_files = os.listdir(crm_dir)
    print(f'  {len(crm_files)} 个文�?)
    for fname in sorted(crm_files):
        fp = os.path.join(crm_dir, fname)
        if os.path.isfile(fp):
            sz = os.path.getsize(fp)
            if sz > 0:
                ext = os.path.splitext(fname)[1].lower()
                if ext == '.json':
                    with open(fp,'r',encoding='utf-8') as f:
                        d = json.load(f)
                    if isinstance(d, list):
                        detail = f'{len(d):,} 条记�?
                    elif isinstance(d, dict):
                        detail = f'{len(d):,} 个键'
                    else:
                        detail = '?'
                else:
                    detail = ''
                print(f'    {fname:<30s}: {sz/1024:>8.0f}KB  {detail}')

print()
print('=== source_files 目录 ===')
sf = os.path.join(BASE, 'source_files')
total_sf = 0
for root, dirs, files in os.walk(sf):
    for f in files:
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        total_sf += sz
        rel = os.path.relpath(fp, BASE)
        print(f'  {rel:<55s}: {sz/1024:>8.0f}KB')
print(f'  source_files 总计: {total_sf/1024:.0f}KB ({total_sf/1024/1024:.1f}MB)')

print()
print('=== 发现的问�?===')
# 空类�?for g in graphs:
    fp = os.path.join(BASE, g+'.json')
    with open(fp,'r',encoding='utf-8-sig') as f:
        d = json.load(f)
    no_type = [e for e in d.get('entities',[]) if not e.get('type')]
    if no_type:
        issues.append(f'{g}: {len(no_type)} 实体缺少type字段')

if not issues:
    issues.append('(暂无重大问题)')
for i in issues:
    print(f'  {i}')
