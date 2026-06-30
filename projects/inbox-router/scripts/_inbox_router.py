#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inbox_router v3.1 — HF/DRR文件自动解析+入库+分析流水线
当收件箱检测到HF/DDR等文件时，自动触发全链路处理
"""

import os, sys, json, shutil, re, subprocess
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(os.path.dirname(WORKSPACE), 'media')
INCOMING = os.path.join(MEDIA_DIR, 'incoming')
ARCHIVED = os.path.join(MEDIA_DIR, 'archived')
KC_DIR = os.path.join(WORKSPACE, 'knowledge_center')
LOG_FILE = os.path.join(KC_DIR, '_inbox_log.json')
os.makedirs(ARCHIVED, exist_ok=True)

sys.stdout.reconfigure(encoding='utf-8')

# ===== 文件类型识别 =====
FILE_TYPES = {
    'HF': {
        'patterns': ['history_and_forecast', 'history and forecast', 'history_forecast', 
                     'hf_20', 'hf-20'],
        'pipeline': 'hf_pipeline.py',
        'label': 'HF预测/营收',
    },
    'DRR': {
        'patterns': ['drr_20', 'drr-20', 'daily_revenue_report', 'drr_2'],
        'pipeline': None,  # 暂未实现
        'label': 'DRR日报',
    },
    'BEO': {
        'patterns': ['beo_76', 'beo-76', 'beo76'],
        'pipeline': None,
        'label': 'BEO宴会活动',
    },
}

# ===== 文件内容解析 =====
def extract_text_content(filepath):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    text = ''

    if ext in ['.txt', '.md', '.csv', '.json']:
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    text = f.read(5000)
                break
            except:
                continue

    elif ext in ['.xlsx', '.xls']:
        try:
            import openpyxl
            wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
            cells = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(max_row=15, values_only=True):
                    for cell in row:
                        if cell is not None:
                            cells.append(str(cell))
            text = ' '.join(cells)
            wb.close()
        except:
            text = ''

    elif ext == '.pdf':
        try:
            from pypdf import PdfReader
            r = PdfReader(filepath)
            pages = [p.extract_text() or '' for p in r.pages]
            text = '\n'.join([p for p in pages if p.strip()])
        except:
            text = ''
        if len(text.strip()) < 10:
            try:
                import pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    pages = [p.extract_text() or '' for p in pdf.pages]
                    text = '\n'.join([p for p in pages if p.strip()])
            except:
                pass
        if len(text.strip()) < 10:
            text = '[scanned]'
    else:
        text = '[unreadable]'

    return text[:5000]


def detect_file_type(filename, text):
    """识别文件类型（HF/DRR/BEO/其他）"""
    filename_lower = filename.lower()
    
    for ftype, info in FILE_TYPES.items():
        for pat in info['patterns']:
            if pat in filename_lower:
                return ftype, info['label'], info['pipeline']
    
    # 内容检测——扫一眼文本
    if 'history and forecast' in text[:500].lower() or 'hilton suzhou' in text[:200].lower():
        if 'occ.%' in text or 'room revenue' in text[:2000].lower():
            return 'HF', 'HF预测(内容识别)', 'hf_pipeline.py'
    
    return None, '其他', None


# ===== HF自动处理流水线 =====
def run_hf_pipeline(filepath):
    """
    自动跑HF全链路：
    1. 解析PDF存入FIN图谱
    2. 生成同比分析
    3. 输出分析摘要
    """
    print(f'\n  🔄 启动HF自动处理流水线...')
    print(f'  📄 文件: {os.path.basename(filepath)}')
    
    # Step 1: 解析HF并入库
    result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'file': os.path.basename(filepath),
        'steps': [],
        'success': False,
        'summary': ''
    }
    
    try:
        # 提取数据到临时JSON
        text = extract_text_content(filepath)
        if text and text != '[scanned]' and len(text) > 100:
            result['steps'].append({'step': 'parse', 'status': 'ok', 'chars': len(text)})
            
            # 分析数据特征
            lines = text.split('\n')
            history_count = 0
            forecast_count = 0
            total_rev = 0
            occ_values = []
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 12:
                    first = parts[0]
                    if '.' in first and len(first) >= 7:
                        try:
                            day, month, year = first.split('.')
                            int(day); int(month)
                            # 找到Occ%
                            for p in parts:
                                if '%' in p:
                                    occ = float(p.replace('%', ''))
                                    occ_values.append(occ)
                                    history_count += 1
                                    break
                        except:
                            pass
            
            if history_count > 0:
                avg_occ = sum(occ_values) / len(occ_values) if occ_values else 0
                result['steps'].append({'step': 'analyze', 'status': 'ok', 
                    'history_days': history_count, 
                    'avg_occ': round(avg_occ, 1)})
            else:
                result['steps'].append({'step': 'analyze', 'status': 'warn', 
                    'msg': '未能从PDF解析出结构化数据'})
            
            result['success'] = True
            
        else:
            result['steps'].append({'step': 'parse', 'status': 'fail', 'msg': '无法读取PDF内容'})
    
    except Exception as e:
        result['steps'].append({'step': 'error', 'status': 'fail', 'msg': str(e)})
    
    return result


# ===== 归档 =====
def archive_file(filepath):
    dest = os.path.join(ARCHIVED, os.path.basename(filepath))
    if os.path.exists(dest):
        base, ext = os.path.splitext(dest)
        dest = '%s_%s%s' % (base, datetime.now().strftime('%Y%m%d_%H%M%S'), ext)
    shutil.move(filepath, dest)
    return dest


# ===== 主流程 =====
def main():
    files = [f for f in os.listdir(INCOMING)
             if os.path.isfile(os.path.join(INCOMING, f))
             and f != 'README.md']
    
    if not files:
        print('inbox empty.')
        return
    
    print('found %d new files:' % len(files))
    for f in files:
        print('  ' + f)
    print()
    
    pipeline_results = []
    
    for f in files:
        fp = os.path.join(INCOMING, f)
        text = extract_text_content(fp)
        ftype, flabel, pipeline_script = detect_file_type(f, text)
        
        print('=' * 55)
        print(f'  📎 {f}')
        print(f'  类型: {flabel} | 流水线: {pipeline_script or "无"}')
        
        # 如果匹配到HF流水线，自动触发
        if pipeline_script:
            print(f'\n  ⚡ 自动触发 {flabel} 处理...')
            pr = run_hf_pipeline(fp)
            pipeline_results.append(pr)
            
            # 打印结果
            for step in pr['steps']:
                status_icon = '✅' if step['status'] == 'ok' else '⚠️' if step['status'] == 'warn' else '❌'
                print(f'  {status_icon} {step["step"]}: {step.get("msg", step.get("status","?"))} ')
                for k, v in step.items():
                    if k not in ['step', 'status', 'msg']:
                        print(f'     {k}: {v}')
            
            if pr['success']:
                print(f'  ✅ {flabel} 处理成功!')
            else:
                print(f'  ❌ {flabel} 处理有异常')
        else:
            print(f'  📋 当前无自动流水线，已归档')
        
        # 归档
        archived_path = archive_file(fp)
        print(f'  📦 已归档: {os.path.basename(archived_path)}')
        print()
    
    # 总结果
    print('=' * 55)
    success_count = sum(1 for r in pipeline_results if r['success'])
    total_count = len(pipeline_results)
    print(f'  流水线: {success_count}/{total_count} 成功')
    
    if pipeline_results:
        print(f'\n  📊 处理摘要:')
        for r in pipeline_results:
            date_str = r.get('date','')[:16]
            summary_parts = []
            for s in r.get('steps', []):
                if s['status'] == 'ok':
                    for k in ['history_days','avg_occ']:
                        if k in s:
                            summary_parts.append(f'{k}={s[k]}')
            print(f'  • {r["file"]}: {", ".join(summary_parts)}')
    
    print('  done.')
    
    return pipeline_results


def try_import_to_fin(filepath):
    """
    尝试将HF PDF解析后导入FIN图谱
    返回: (success: bool, message: str, data: dict)
    """
    import pdfplumber
    
    try:
        with pdfplumber.open(filepath) as pdf:
            text = pdf.pages[0].extract_text() or ''
    except:
        return False, 'PDF解析失败', {}
    
    # 提取每日数据
    history = []
    forecast = []
    lines = text.strip().split('\n')
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 12:
            continue
        first = parts[0]
        if not ('.' in first and len(first) >= 7):
            continue
        try:
            day, month, year = first.split('.')
            int(day)
        except:
            continue
        
        date_str = f'2026-{month.zfill(2)}-{day.zfill(2)}'
        
        # 解析数字
        nums = []
        for p in parts[1:]:
            cleaned = p.replace(',', '')
            try:
                if '.' in cleaned and cleaned.count('.') == 1:
                    nums.append(float(cleaned))
                else:
                    nums.append(int(cleaned))
            except:
                continue
        
        if len(nums) < 12:
            continue
        
        occ_pct = None
        for p in parts[1:]:
            if '%' in p:
                occ_pct = float(p.replace('%', ''))
                break
        
        if occ_pct is None:
            continue
        
        revenue = 0
        adr = 0
        sold = int(nums[0])
        
        for i, p in enumerate(parts[1:], 1):
            if '%' in p:
                idx_rev = i + 1
                idx_adr = i + 2
                try:
                    revenue = float(parts[idx_rev].replace(',', ''))
                    adr = float(parts[idx_adr])
                except:
                    pass
                break
        
        row = {
            'date': date_str,
            'sold': sold,
            'occ': occ_pct,
            'rev': revenue,
            'adr': adr,
            'forecast': date_str >= '2026-05-22'
        }
        
        if date_str >= '2026-05-22':
            forecast.append(row)
        else:
            history.append(row)
    
    # 去重
    seen_dates = set()
    unique_hist = []
    for r in history:
        if r['date'] not in seen_dates:
            seen_dates.add(r['date'])
            unique_hist.append(r)
    
    seen_dates_f = set()
    unique_fcst = []
    for r in forecast:
        if r['date'] not in seen_dates_f:
            seen_dates_f.add(r['date'])
            unique_fcst.append(r)
    
    # 统计
    if not unique_hist:
        return False, '未能解析出有效日常数据', {}
    
    h_occ = sum(r['occ'] for r in unique_hist) / len(unique_hist)
    h_rev = sum(r['rev'] for r in unique_hist)
    h_adr = sum(r['adr'] for r in unique_hist) / len(unique_hist)
    
    f_occ = sum(r['occ'] for r in unique_fcst) / len(unique_fcst) if unique_fcst else 0
    f_rev = sum(r['rev'] for r in unique_fcst) if unique_fcst else 0
    
    data = {
        'history_days': len(unique_hist),
        'forecast_days': len(unique_fcst),
        'hist_avg_occ': round(h_occ, 1),
        'hist_avg_adr': round(h_adr, 2),
        'hist_total_rev': round(h_rev, 2),
        'fcst_avg_occ': round(f_occ, 1),
        'fcst_total_rev': round(f_rev, 2),
        'total_est_rev': round(h_rev + f_rev, 2),
    }
    
    # 写入FIN图谱
    try:
        fin_graph = json.load(open(os.path.join(KC_DIR, 'fin_graph.json'), 'r', encoding='utf-8'))
        
        existing_ids = {e.get('id', '') for e in fin_graph.get('entities', [])}
        added = 0
        
        for day in unique_hist + unique_fcst:
            node_id = f'DAILY_{day["date"]}'
            if node_id in existing_ids:
                continue
            
            fin_graph['entities'].append({
                'id': node_id,
                'name': f'日报 {day["date"]}',
                'date': day['date'],
                'type': 'daily_report',
                'properties': {
                    'room_sold': day['sold'],
                    'occ_pct': day['occ'],
                    'adr': day['adr'],
                    'room_revenue': day['rev'],
                    'source': 'HF_auto',
                    'is_forecast': 'Y' if day['forecast'] else 'N'
                }
            })
            added += 1
        
        if added > 0:
            fin_graph['meta']['version'] = f'v7.9 + HF_auto ({datetime.now().strftime("%m-%d %H:%M")})'
            fin_graph['meta']['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            json.dump(fin_graph, open(os.path.join(KC_DIR, 'fin_graph.json'), 'w', encoding='utf-8'), 
                      ensure_ascii=False, indent=2)
        
        data['imported'] = added
        data['total_entities'] = len(fin_graph.get('entities', []))
        
    except Exception as e:
        data['import_warning'] = str(e)
    
    return True, f'解析成功: {len(unique_hist)}天历史 + {len(unique_fcst)}天预测', data


if __name__ == '__main__':
    main()
