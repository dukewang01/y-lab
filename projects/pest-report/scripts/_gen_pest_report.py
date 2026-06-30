#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虫控报告全维分析文档"""
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

D = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center'
fsaa = json.load(open(os.path.join(D, 'fsaa_graph.json'), encoding='utf-8'))
fae = fsaa.get('entities', [])
far = fsaa.get('relationships', [])
from collections import Counter, defaultdict

reports = sorted([n for n in fae if n.get('type') == 'fsaa_pco_report'],
                 key=lambda x: str(x.get('properties', {}).get('date', '')))
findings = [n for n in fae if n.get('type') == 'fsaa_pco_finding']

fp_out = os.path.join(D, '_pest_report_full_20260509.md')
with open(fp_out, 'w', encoding='utf-8') as fh:
    w = lambda s='': fh.write(s + '\n')
    
    w('# 苏州希尔顿 · 虫控报告全维分析')
    w('> 报告日期: 2026-05-09 | 数据来源: FSAA站 | 7份帮帮虫控报告 | 84个问题点')
    w()
    w('## 一、报告时间线')
    w()
    w('| 日期 | 服务轮次 | 问题数 | 🔴高危 | 🟡中危 | ❌未完成 | 下次跟进 |')
    w('|:---:|:---|---:|:---:|:---:|:---:|:---|')
    for r in reports:
        p = r.get('properties', {})
        rid = r['id']
        fids = [rel['target_id'] for rel in far if rel.get('source_id') == rid and rel.get('type') == 'has_finding']
        highs = sum(1 for f in findings if f['id'] in fids and f.get('properties', {}).get('severity') == 'high')
        meds = sum(1 for f in findings if f['id'] in fids and f.get('properties', {}).get('severity') == 'medium')
        unc = sum(1 for f in findings if f['id'] in fids and f.get('properties', {}).get('status') == '未完成')
        w('| %s | %s | %d | %d | %d | %d | %s |' % (
            p.get('date', ''), p.get('service_round', ''), len(fids),
            highs, meds, unc, p.get('next_followup', '') or '-'))
    
    w()
    w('## 二、各报告详细问题')
    w()
    for r in reports:
        p = r.get('properties', {})
        rid = r['id']
        fids = [rel['target_id'] for rel in far if rel.get('source_id') == rid and rel.get('type') == 'has_finding']
        w('### %s - %s' % (p.get('date', ''), p.get('service_round', '')))
        w()
        w('| 严重度 | 问题 | 位置 | 跟进部门 | 状态 |')
        w('|:---:|:---|:---|:---:|:---:|')
        for f in findings:
            if f['id'] in fids:
                fp2 = f.get('properties', {})
                sev = '🔴 高' if fp2.get('severity') == 'high' else '🟡 中'
                stat = '❌ 未完成' if fp2.get('status') == '未完成' else ('✅ 已完成' if fp2.get('status') == '已完成' else '—')
                w('| %s | %s | %s | %s | %s |' % (
                    sev, f.get('name', '')[:35], fp2.get('location', '')[:15],
                    fp2.get('responsible', '')[:10], stat))
        w()
    
    w('## 三、高频问题区域TOP10')
    w()
    loc_c = Counter()
    for f in findings:
        loc_c[f.get('properties', {}).get('location', '')] += 1
    for loc, cnt in loc_c.most_common(10):
        if loc:
            w('1. **%s** - %d次' % (loc[:20], cnt))
    
    w()
    w('## 四、责任部门压力')
    w()
    dept_c = Counter()
    dept_h = Counter()
    for f in findings:
        d = f.get('properties', {}).get('responsible', '')
        dept_c[d] += 1
        if f.get('properties', {}).get('severity') == 'high':
            dept_h[d] += 1
    for d, c in dept_c.most_common():
        if d:
            w('- **%s**: %d个问题(🔴%d个)' % (d, c, dept_h.get(d, 0)))
    
    w()
    w('## 五、反复出现的问题')
    w()
    repeat = defaultdict(list)
    for f in findings:
        key = f.get('properties', {}).get('issue', '')[:20]
        if key:
            repeat[key].append(f)
    for iss, fs in sorted(repeat.items(), key=lambda x: -len(x[1])):
        if len(fs) >= 2:
            dates = [f.get('properties', {}).get('date', '') for f in fs]
            locs = list(set(f.get('properties', {}).get('location', '') for f in fs))
            w('- **%s**: %d次(%s)，%s' % (iss[:30], len(fs), '->'.join(dates), locs[0][:15]))
    
    w()
    w('## 六、严重度与完成状态')
    w()
    sev = Counter()
    st = Counter()
    for f in findings:
        sev[f.get('properties', {}).get('severity', '未标注')] += 1
        st[f.get('properties', {}).get('status', '未标注')] += 1
    w('- 🔴 高危: %d个(含未标注)' % (sev.get('high', 0) + sev.get('', 0)))
    w('- 🟡 中危: %d个' % sev.get('medium', 0))
    w('- ❌ 未完成: %d个' % st.get('未完成', 0))
    w('- ✅ 已完成: %d个' % st.get('已完成', 0))
    
    w()
    w('## 七、结论与建议')
    w()
    w('### 🔴 高风险区TOP3')
    w('1. **意大利厨房**（排水淤积+蟑螂+披萨烤炉）— 持续4个月未根治')
    w('2. **西餐厅明档**（铁板残渣+水池积水）— 管事部清洁制度问题')
    w('3. **3F面馆**（蟑螂活体）— 灶台卫生死角')
    w()
    w('### 📌 建议优先闭环')
    w('1. 意大利厨房洗碗间排水系统修复')
    w('2. 3F杀鱼间加装胶帘/风幕机（已拖1个月）')
    w('3. 管事部建立明档每日清洁检查制度')
    w()
    w('### ✅ 已完成好案例')
    w('- 叫花鸡展示间油污（2025.10.14→10.21，1周闭环）')
    w()
    w('---')
    w('*报告由Y自动生成 | 2026-05-09 | 数据来源: FSAA站(1,216节点/1,733关系)*')

print('文档已生成: _pest_report_full_20260509.md')
print('大小:', os.path.getsize(fp_out), '字节')
