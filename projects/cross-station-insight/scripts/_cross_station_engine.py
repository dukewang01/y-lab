#!/usr/bin/env python3
"""
跨站推理引擎 v0.3 �?深度搜索+智能意图识别
输入：任意中文问�?输出：跨站智能答�?"""
import json, sys, re, os
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r'C:\Users\Y\.openclaw\workspace'
GRAPH_DIR = os.path.join(WORKSPACE, 'knowledge_center')

# ====== 数据加载 ======
graphs = {}
graph_files = {
    'FIN': 'fin_graph.json', 'QA': 'qa_graph.json', 'MEP': 'mep_graph.json',
    'GSM': 'gsm_graph.json', 'FB': 'fb_graph.json', 'FSAA': 'fsaa_graph.json',
    'FAQ': 'faq_graph.json',
}
for name, fname in graph_files.items():
    path = os.path.join(GRAPH_DIR, fname)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        graphs[name] = {
            'entities': {e['id']: e for e in data.get('entities', [])},
            'edges': data.get('edges', []),
            'raw': data
        }
    else:
        graphs[name] = {'entities': {}, 'edges': [], 'raw': {'entities': [], 'edges': []}}

# ====== 深度搜索引擎 ======
def deep_search(q, max_per_source=10, max_total=50):
    """全属性深度搜索：name/label/description/type/properties(含嵌�?"""
    # 智能分词
    stop_words = {'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'一','一�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'着','没有','�?,'�?,'自己','�?,'�?,'�?,'�?,'�?,'�?,'什�?,'怎么','如何','�?,'�?,'�?,'�?,'呀','�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?,'�?}
    raw_kw = [w.strip() for w in re.split(r'[的吗了呢吧呀哦嗯·\s,，。！？、：�?"''（）()【】]+', q) if len(w.strip()) >= 2 and w.strip() not in stop_words]
    keywords = list(set(raw_kw + ([q] if len(q) >= 3 else [])))
    if not keywords:
        keywords = [q]
    
    source_order = ['QA','FSAA','GSM','MEP','FB','FAQ','FIN']
    all_hits = []
    
    for source in source_order:
        e_dict = graphs.get(source, {}).get('entities', {})
        source_hits = []
        for eid, e in e_dict.items():
            search_terms = [
                str(e.get('name', '')), str(e.get('label', '')),
                str(e.get('description', '')), str(e.get('type', '')),
            ]
            props = e.get('properties', {})
            if isinstance(props, dict):
                def collect_text(v):
                    if isinstance(v, str): search_terms.append(v)
                    elif isinstance(v, (int, float)): search_terms.append(str(v))
                    elif isinstance(v, dict):
                        for vv in v.values(): collect_text(vv)
                    elif isinstance(v, list):
                        for vv in v: collect_text(vv)
                for v in props.values():
                    collect_text(v)
            
            combined = ' '.join(search_terms).lower()
            score = 0
            match_detail = ''
            for kw in keywords:
                kwl = kw.lower()
                if kwl in combined:
                    if kwl in e.get('name','').lower() or kwl in e.get('label','').lower():
                        score += 3
                    elif kwl in e.get('description','').lower():
                        score += 2
                    else:
                        score += 1
                    if not match_detail:
                        # Find the matching value
                        match_detail = kw
            if score > 0:
                source_hits.append({
                    'source': source, 'eid': eid, 'name': e.get('name','') or eid,
                    'type': e.get('type',''), 'score': score,
                    'props': props
                })
        
        source_hits.sort(key=lambda x: -x['score'])
        for h in source_hits[:max_per_source]:
            all_hits.append(h)
        
    all_hits.sort(key=lambda x: -x['score'])
    return all_hits[:max_total]

# ====== 工具函数 ======
def get_entity(eid, source='FIN'):
    return graphs.get(source, {}).get('entities', {}).get(eid)

def prop(ent, key, default=''):
    p = ent.get('properties', {})
    v = p.get(key, default)
    return v if v != '' else default

# ====== 自然语言意图识别 ======
def classify_question(q):
    ql = q.lower()
    if any(kw in ql for kw in ['评分','扣分','qa','审计','检�?,'得分','graded']):
        return 'qa_score'
    if any(kw in ql for kw in ['成本�?,'成本','财务','盈利','收入','花费','利润','drr','收益']):
        if any(kw in ql for kw in ['酒水�?,'酒单','菜单','茅台','五粮�?,'红酒','白酒']):
            return 'beverage'
        if '成本' in ql and '�? in ql:
            return 'cost'
        return 'cost'
    if any(kw in ql for kw in ['空调','设备','维修','工单','mep','工程','给排�?,'排水','电梯','照明']):
        return 'mep'
    if any(kw in ql for kw in ['投诉','客诉','gsm','纠纷','赔偿','案例','客人不满�?]):
        return 'complaint'
    if any(kw in ql for kw in ['�?,'白酒','茅台','五粮�?,'红酒','啤酒','定价','酒单','菜单','菜品']):
        return 'beverage'
    if any(kw in ql for kw in ['客房','房间','入住','2606','房间�?]):
        return 'room'
    if any(kw in ql for kw in ['早餐','餐厅','厨房','fb','食品安全','fsaa']):
        return 'fb'
    return 'general'

# ====== 各模�?======
def module_qa_score(q):
    lines = ['', '='*65, '🏆 QA评分分析', '='*65]
    score = graphs['QA']['entities'].get('QA_2025_FULL_SCORE')
    if not score:
        return ['⚠️ QA评分数据未加�?]
    lines.append(f'📊 2025总分: {score.get("description","")}')
    areas = []
    for eid, e in graphs['QA']['entities'].items():
        if 'AREA' in eid and '2025' in eid:
            d = e.get('description','')
            m = re.search(r'Condition�?[0-9.]+)', d)
            if m: areas.append((float(m.group(1)), e.get('name',''), d))
    areas.sort(reverse=True)
    lines.append('\n🔴 扣分最多区�?')
    for pts, name, d in areas[:5]:
        clean = re.search(r'Cleanliness�?[0-9.]+)', d)
        cs = f' + 卫生扣{clean.group(1)}�? if clean else ''
        lines.append(f'  {name}: {pts}分{cs}')
    lines.append('\n🎯 结论: Condition扣分(89.80%)是最大问�?)
    return lines

def module_cost(q):
    lines = ['', '='*65, '💰 成本分析', '='*65]
    ql = q.lower()
    targets = []
    if '御玺' in ql or 'yuxi' in ql: targets.append('BEV_OUTLET_YUXI')
    if 'bacio' in ql: targets.append('BEV_OUTLET_BACIO')
    if 'open' in ql: targets.append('BEV_OUTLET_OPEN')
    if not targets:
        targets = ['BEV_OUTLET_YUXI','BEV_OUTLET_BANQUET','BEV_OUTLET_BACIO','BEV_OUTLET_OPEN','BEV_OUTLET_YUAN','BEV_OUTLET_IN_ROOM']
    for oid in targets:
        e = get_entity(oid, 'FIN')
        if not e: continue
        m3 = prop(e, '3月成本率','�?); m2 = prop(e, '2月成本率','�?); m1 = prop(e, '1月成本率','�?)
        budget = prop(e, '预算','�?)
        flag = '⚠️' if m3 and budget and isinstance(m3,(int,float)) and isinstance(budget,(int,float)) and m3 > budget else '�?
        lines.append(f'{flag} {e.get("name","")}: 1�?{m1}% �?2�?{m2}% �?3�?{m3}% (预算={budget}%)')
    return lines

def module_room(q):
    lines = ['', '='*65, '🏠 客房分析', '='*65]
    rm = re.search(r'(\d{4})', q)
    if rm:
        nr = rm.group(1)
        lines.append(f'🔍 房间 {nr}:')
        wo = get_entity(f'WO_{nr}_AC', 'MEP') or (get_entity('WO_2606_AC','MEP') if nr == '2606' else None)
        if wo: lines.append(f'  🔧 MEP: {wo.get("description","")[:120]}')
        gsm_hits = []
        for eid, e in graphs['GSM']['entities'].items():
            if nr in e.get('name','') or nr in e.get('description',''):
                gsm_hits.append(e)
        if gsm_hits:
            lines.append(f'\n  📋 客诉({len(gsm_hits)}�?:')
            for e in gsm_hits[:3]:
                lines.append(f'    �?{e.get("name","")}: {e.get("description","")[:80]}')
    else:
        for eid, e in graphs['QA']['entities'].items():
            if 'GUEST_ROOMS' in eid: lines.append(f'  📊 {e.get("description","")[:80]}')
    return lines

def module_complaint(q):
    lines = ['', '='*65, '📋 客诉分析', '='*65]
    ql = q.lower()
    kws = [w for w in ['空调','噪音','清洁','卫生','赔偿','态度','效率','设施'] if w in ql]
    if not kws: kws = ['案例']
    lines.append(f'🔍 搜索: {", ".join(kws)}')
    found = 0
    for eid, e in graphs['GSM']['entities'].items():
        n = e.get('name',''); d = e.get('description','')
        for kw in kws:
            if kw in n or kw in d:
                found += 1
                if found <= 8:
                    lines.append(f'  📌 {n}: {d[:100]}')
                break
    if found > 8: lines.append(f'  ...及{found-8}条更�?)
    lines.append(f'\n📊 GSM共{len(graphs["GSM"]["entities"])}�?)
    return lines

def module_beverage(q):
    lines = ['', '='*65, '🍷 酒水分析', '='*65]
    ql = q.lower()
    if '茅台' in ql:
        inv = get_entity('INV_MT_FEITIAN_53', 'FIN')
        if inv:
            c = prop(inv,'cost_price','?'); s = prop(inv,'stock_level','?')
            lines.append(f'🥃 飞天53°: ¥{c}/�?×{s}�?| 售价¥6,088+15%')
        else: lines.append('⚠️ 数据未录�?)
    elif '五粮�? in ql:
        for iid in ['INV_WULIANGYE_52','INV_WULIANGYE_39']:
            e = get_entity(iid,'FIN')
            if e: lines.append(f'🥃 {e.get("name","")}: ¥{prop(e,"cost_price","?")}/�?)
    else:
        lines.append('📊 定价: 高端白酒40-50% | House Wine ~50% | 整瓶20-25% | 软饮<10%')
        lines.append('💡 可查"茅台"�?五粮�?详情')
    return lines

def module_mep(q):
    lines = ['', '='*65, '🔧 MEP分析', '='*65]
    ql = q.lower()
    if any(kw in ql for kw in ['空调','hvac']):
        wo = get_entity('WO_2606_AC','MEP')
        if wo: lines.append(f'  🔴 2606: {wo.get("description","")[:120]}')
    elif any(kw in ql for kw in ['排水','�?]):
        wo = get_entity('WO_B1_DRAIN','MEP')
        if wo: lines.append(f'  🔴 B1排水: {wo.get("description","")[:100]}')
    else:
        lines.append('🔍 活跃工单:')
        for e in graphs['MEP']['entities'].values():
            d = e.get('description','')
            if any(kw in d for kw in ['未完�?,'异响','异常']):
                lines.append(f'  📌 {e.get("name","")}: {d[:100]}')
    return lines

def module_fb(q):
    lines = ['', '='*65, '🍽�?F&B分析', '='*65]
    ql = q.lower()
    if '早餐' in ql:
        lines.append('🥞 早餐标准: 热食�?3°C | 冷食�?°C | 6款热�?| 5款面�?)
        lines.append('  �?templates/QA_BREAKFAST_CHECKLIST.md')
    elif any(kw in ql for kw in ['fsaa','食品安全','卫生']):
        lines.append('🔴 FSAA食安�?')
        results = deep_search(ql, 5, 10)
        for r in results:
            lines.append(f'  📌 {r["source"]}/{r["name"]}')
    else:
        lines.append('📊 餐饮营业�?')
        for oid in ['OUTLET_OPEN','OUTLET_BQT','OUTLET_YUXI','OUTLET_BACIO','OUTLET_YUAN','OUTLET_ROOM_DINING']:
            e = get_entity(oid, 'FIN')
            if e:
                m3 = prop(e,'month_03_cost_pct','')
                rev = prop(e,'q1_revenue','')
                if m3:
                    lines.append(f'  {e.get("name","")}: 3月成本{float(m3)*100:.1f}% | Q1营收¥{float(rev)/10000:.0f}�?)
    return lines

def module_general(q):
    """深度全站搜索（v0.3升级版）"""
    lines = ['', '='*65, '🔍 全站深度搜索', '='*65]
    lines.append(f'  问题: "{q}"')
    
    results = deep_search(q, 8, 30)
    
    if not results:
        lines.append('\n⚠️ 未找到匹配结�?)
        # Show discoverable samples
        samples = []
        for src in ['QA','GSM','MEP','FB']:
            for e in list(graphs.get(src,{}).get('entities',{}).values())[:5]:
                n = e.get('name','')
                if n and len(n) >= 2 and n not in samples:
                    samples.append(n)
                    break
        lines.append(f'💡 试试: {" | ".join(samples[:8])}')
        lines.append(f'\n📊 搜索{sum(1 for s in graphs.values() if s["entities"])}�? 命中0�?)
        return lines
    
    # Group by source
    by_source = {}
    for r in results:
        by_source.setdefault(r['source'], []).append(r)
    
    source_names = {'FIN':'财务','QA':'质检','MEP':'工程','GSM':'客诉','FB':'餐饮','FSAA':'食安','FAQ':'问答'}
    for src, hits in by_source.items():
        lines.append(f'\n📂 {source_names.get(src,src)}�?{len(hits)}�?:')
        for h in hits[:5]:
            lines.append(f'  📌 {h["name"]}')
            # Show matching property value if available
            if h.get('props') and isinstance(h['props'], dict):
                for k, v in h['props'].items():
                    if isinstance(v, str) and any(kw.lower() in v.lower() for kw in [q]):
                        lines.append(f'     �?{v[:80]}')
                        break
    
    lines.append(f'\n📊 搜索{sum(1 for s in graphs.values() if s["entities"])}�? 命中{len(results)}�?)
    return lines

# ====== 入口 ======
DISPLAY_STARTUP = False

def answer(question):
    intent = classify_question(question)
    modules = {
        'qa_score': module_qa_score, 'cost': module_cost,
        'room': module_room, 'complaint': module_complaint,
        'beverage': module_beverage, 'mep': module_mep,
        'fb': module_fb, 'general': module_general,
    }
    return modules.get(intent, module_general)(question)

if __name__ == '__main__':
    print('='*60)
    print('🏗�? 跨站推理引擎 v0.3')
    print(f'   启动: {datetime.now().strftime("%H:%M")}')
    print(f'   数据�? {", ".join(k for k,v in graphs.items() if v["entities"])}')
    print('='*60)
    print('   输入问题�?exit退出，/debug看状�?)
    print('   示例: "咖啡机奶管残�? "游泳池水�? "早餐温度"')
    print('='*60)
    while True:
        try:
            q = input('\n�?').strip()
            if not q: continue
            if q.lower() in ('/exit','/quit','exit','quit'): break
            if q.lower() == '/debug':
                for k, v in graphs.items():
                    print(f'  {k}: {len(v["entities"])}实体')
                continue
            intent = classify_question(q)
            print(f'  �?意图: {intent}')
            result = answer(q)
            print('\n'.join(result))
        except KeyboardInterrupt: print('\nbye'); break
        except Exception as ex: print(f'\n⚠️ 错误: {ex}')
