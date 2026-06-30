"""GSM站 自动备份保险脚本 — 每次操作前/后自动执行"""
import json, shutil, subprocess, os
from datetime import datetime

# ===== 配置 =====
WORKSPACE = r'C:\Users\Duke Wang\.openclaw\workspace'
GSM_FILE = os.path.join(WORKSPACE, r'knowledge_center\gsm_graph.json')
BACKUP_DIR = os.path.join(WORKSPACE, r'knowledge_center')
GIT_DIR = WORKSPACE

def auto_backup_gsm():
    """三保险：本地备份 + 命名版本 + Git提交"""
    now = datetime.now()
    ts = now.strftime('%Y%m%d_%H%M')
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M')
    
    print(f'[{time}] ===== GSM站 三保险备份 =====')
    
    # ===== 保险1: 本地备份 =====
    bak_path = os.path.join(BACKUP_DIR, f'gsm_graph_backup.json')
    shutil.copy2(GSM_FILE, bak_path)
    print(f'  ✅ 保险1: 本地备份 → {bak_path}')
    
    # ===== 保险2: 版本命名备份 =====
    # 读取版本号
    with open(GSM_FILE, 'r', encoding='utf-8') as f:
        gsm = json.load(f)
    ver = gsm.get('meta', {}).get('version', '0.0') or '0.0'
    ver_bak = os.path.join(BACKUP_DIR, f'gsm_graph_v{ver}_backup.json')
    shutil.copy2(GSM_FILE, ver_bak)
    print(f'  ✅ 保险2: 版本备份 → gsm_graph_v{ver}_backup.json')
    
    # ===== 保险3: Git提交 =====
    try:
        subprocess.run(['git', 'add', '-A'], cwd=GIT_DIR, capture_output=True, text=True)
        r = subprocess.run(
            ['git', 'commit', '--allow-empty', '-m', f'GSM站 v{ver} 三保险备份 [{date} {time}]'],
            cwd=GIT_DIR, capture_output=True, text=True
        )
        if r.returncode == 0:
            print(f'  ✅ 保险3: Git提交 ✅')
            if r.stdout:
                print(f'     {r.stdout.strip()}')
        else:
            print(f'  ⚠️ Git提交错误: {r.stderr.strip()[:100]}')
    except Exception as ex:
        print(f'  ⚠️ Git不可用: {ex}')
    
    print(f'  📊 版本: v{ver} | 实体: {len(gsm.get("entities",[]))} | 关系: {len(gsm.get("relationships", gsm.get("relations",[])))}')
    print(f'  ===== 完毕 =====')

if __name__ == '__main__':
    auto_backup_gsm()
