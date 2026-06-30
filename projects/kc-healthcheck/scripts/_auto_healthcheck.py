"""
知识中心每日自检脚本
定时运行: 每天第一次启动时自动执行
"""
import json, os, sys
from datetime import datetime
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
now = datetime.now().strftime('%Y-%m-%d %H:%M')

issues = []

# 1. 检查图谱完整性
graphs = ['mep_graph','fsaa_graph','risk_graph','qa_graph','fin_graph','fb_graph','lib_graph','gsm_graph','faq_graph']
for g in graphs:
    fp = os.path.join(BASE, g + '.json')
    if not os.path.exists(fp):
        issues.append(f'[缺失] {g}.json')
        continue
    try:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            d = json.load(f)
        if not d.get('entities'):
            issues.append(f'[空实体] {g}')
        if not d.get('relations'):
            issues.append(f'[空关系] {g}')
    except:
        issues.append(f'[解析失败] {g}')

# 2. 检查日志存储健康度
log_dir = os.path.join(BASE, 'log_cases')
if os.path.exists(log_dir):
    total = sum(os.path.getsize(os.path.join(log_dir, f)) for f in os.listdir(log_dir) 
                if os.path.isfile(os.path.join(log_dir, f)))
    if total > 500 * 1024 * 1024:
        issues.append(f'[存储警告] log_cases 超过500MB: {total/1024/1024:.0f}MB')

# 3. 检查收件箱是否有积压
inbox_log = os.path.join(BASE, '_inbox_log.json')
if os.path.exists(inbox_log):
    with open(inbox_log, 'r', encoding='utf-8') as f:
        try:
            log = json.load(f)
            pending = [e for e in (log if isinstance(log, list) else []) if e.get('status') == 'pending']
            if pending:
                issues.append(f'[积压] 收件箱有 {len(pending)} 条待处理')
        except:
            pass

# 4. 检查CRM数据
crm_dir = os.path.join(BASE, 'fb_crm')
for f in ['guests.json', 'visits.json', 'preferences.json']:
    fp = os.path.join(crm_dir, f)
    if not os.path.exists(fp):
        issues.append(f'[缺失] CRM/{f}')

# 保存结果
report = {
    'check_time': now,
    'status': 'PASS' if not issues else 'ISSUES',
    'issues': issues
}

with open(os.path.join(BASE, '_healthcheck_result.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

if issues:
    print(f'[{now}] 健康检查: 发现 {len(issues)} 个问题')
    for i in issues:
        print(f'  {i}')
else:
    print(f'[{now}] 健康检查: ✅ 全部正常')
