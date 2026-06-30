"""
知识中心优化脚本 v1.0
1. 清理冗余备份/快照
2. 压缩/清理日志案例
3. 修正日报数据标签
4. 统计最终效果
"""

import json, os, shutil, gzip, glob
from datetime import datetime
from collections import Counter

BASE = 'C:\\Users\\Duke Wang\\.openclaw\\workspace\\knowledge_center'
now = datetime.now().strftime('%Y-%m-%d %H:%M')

# ====== 统计优化前 ======
print(f'=== 知识中心优化报告 ===')
print(f'执行时间: {now}')
print()

def dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except:
                pass
    return total

before_total = 0

# ====== 1. 清理冗余备份/快照 ======
print('--- 1. 清理冗余备份/快照 ---')
backup_dirs = [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d)) and 
               ('backup' in d or 'snapshot' in d or 'restore' in d)]
print(f'发现备份/快照目录: {len(backup_dirs)} 个')

# 保留策略：最新1个snapshot + 最新1个backup
keep = {
    'snapshot_v5.0': True,  # 最新快照
    'backup_20260501_1047': True,  # 最新备份
}

deleted_dirs = []
for d in sorted(backup_dirs):
    full = os.path.join(BASE, d)
    sz = dir_size(full)
    before_total += sz
    if d not in keep:
        # 不是要保留的，移动到备份或删除
        if sz < 10 * 1024 * 1024:  # 小于10MB直接删
            print(f'  删除 {d}: {sz/1024:.0f} KB')
            os.system(f'rmdir /s /q "{full}"')
            deleted_dirs.append(d)
        else:
            # 大于10MB的打包压缩
            archive_name = os.path.join(BASE, f'_archived_{d}.zip')
            print(f'  压缩 {d}: {sz/1024:.0f} KB -> {archive_name}')
            shutil.make_archive(os.path.join(BASE, f'_archived_{d}'), 'zip', full)
            os.system(f'rmdir /s /q "{full}"')
            deleted_dirs.append(d)

print(f'  清理了 {len(deleted_dirs)} 个目录')
print()

# ====== 2. 检查日志案例 ======
print('--- 2. 日志案例清理 ---')
log_cases_dir = os.path.join(BASE, 'log_cases')
if os.path.exists(log_cases_dir):
    log_size = dir_size(log_cases_dir)
    print(f'  log_cases 当前大小: {log_size/1024:.0f} KB ({log_size/1024/1024:.1f} MB)')
    
    # 列出大文件
    large_files = []
    for f in os.listdir(log_cases_dir):
        fp = os.path.join(log_cases_dir, f)
        if os.path.isfile(fp):
            sz = os.path.getsize(fp)
            large_files.append((f, sz))
    
    large_files.sort(key=lambda x: -x[1])
    print(f'  最大文件 Top 5:')
    for name, sz in large_files[:5]:
        print(f'    {name}: {sz/1024:.0f} KB')
    
    # 压缩超过5MB的JSON文件
    compressed = 0
    saved = 0
    for f in os.listdir(log_cases_dir):
        fp = os.path.join(log_cases_dir, f)
        if os.path.isfile(fp) and f.endswith('.json') and os.path.getsize(fp) > 5 * 1024 * 1024:
            gz_path = fp + '.gz'
            if not os.path.exists(gz_path):
                with open(fp, 'rb') as fin:
                    with gzip.open(gz_path, 'wb', compresslevel=6) as fout:
                        fout.write(fin.read())
                orig = os.path.getsize(fp)
                compressed_size = os.path.getsize(gz_path)
                saved += orig - compressed_size
                print(f'  已压缩 {f}: {orig/1024:.0f} KB -> {compressed_size/1024:.0f} KB (节省{(orig-compressed_size)/1024:.0f} KB)')
                compressed += 1
                # 删除原文件
                os.remove(fp)
    
    print(f'  共压缩 {compressed} 个文件，节省 {saved/1024:.0f} KB')
else:
    print('  log_cases 目录不存在')
print()

# ====== 3. 修正日报数据标签 ======
print('--- 3. 修正日报数据标签 ---')

# 先把5月1-5日PDF中提取的实际数据标为"actual"
# 把5月6日xlsx解析的数据标为"actual"（当前是"预测"）
fin_file = os.path.join(BASE, 'fin_graph.json')
with open(fin_file, 'r', encoding='utf-8-sig') as f:
    graph = json.load(f)

fixed = 0
for e in graph['entities']:
    if e.get('type') == 'daily_revenue':
        eid = e.get('id', '')
        props = e.get('properties', {})
        source = props.get('data_type', props.get('source', ''))
        
        # 5月1-5日: PDF历史实际数据
        if any(f'2026_05_0{d}' in eid for d in [1,2,3,4,5]):
            if 'actual' not in source.lower() and 'history' in source.lower() or source == 'unknown':
                props['data_type'] = 'actual'
                props['data_source'] = 'PDF_History_and_Forecast'
                fixed += 1
        
        # 5月6日: 实际日报xlsx数据
        if '2026_05_06' in eid:
            old_type = props.get('data_type', '')
            props['data_type'] = 'actual'
            props['data_source'] = 'Daily_Revenue_Report_xlsx'
            if old_type == 'forecast' or old_type == '预测':
                fixed += 1

if fixed > 0:
    with open(fin_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f'  修正 {fixed} 个日报节点标签')
else:
    print(f'  (无需修正)')
print()

# ====== 4. 统计优化后效果 ======
print('--- 最终统计 ---')
after_total = 0
for dirpath, dirnames, filenames in os.walk(BASE):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        try:
            after_total += os.path.getsize(fp)
        except:
            pass

print(f'  优化前预估: {before_total/1024/1024:.1f} MB')
print(f'  优化后: {after_total/1024/1024:.1f} MB')
print(f'  节省: {(before_total - after_total)/1024/1024:.1f} MB')

# 验证fin_graph
with open(fin_file, 'r', encoding='utf-8-sig') as f:
    g = json.load(f)
ents = g['entities']
rels = g['relations']
print(f'  图谱: {len(ents)} 实体, {len(rels)} 关系 (未变动)')

print()
print('✅ 优化完成!')
