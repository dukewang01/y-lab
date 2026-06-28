"""
y-lab — Y's Laboratory CLI
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
PROJECTS = {
    "menu-engine": {"status": "v0.1 dev", "desc": "市场感知菜单工程"},
    "cost-predictor": {"status": "v0.1 dev", "desc": "食材成本预测"},
    "complaint-classifier": {"status": "v0.1 dev", "desc": "投诉自动分类器"},
    "menu-advisor": {"status": "v0.1 dev", "desc": "菜单调整建议引擎"},
    "fsaa": {"status": "v0.1 dev", "desc": "食品安全审计"},
    "qa": {"status": "v0.1 dev", "desc": "品牌标准管理"},
    "mep": {"status": "v0.1 dev", "desc": "物业工程机电"},
    "crm": {"status": "v0.1 dev", "desc": "客户全生命周期管理"},
    "gsm": {"status": "v0.1 dev", "desc": "投诉管理/案例分析"},
    "risk": {"status": "v0.1 dev", "desc": "风险矩阵管理"},
    "revenue": {"status": "planning", "desc": "动态收益管理"},
    "staff": {"status": "planning", "desc": "智能排班优化"},
    "inventory": {"status": "planning", "desc": "库存预警系统"},
    "energy": {"status": "planning", "desc": "能耗追踪"},
    "reputation": {"status": "planning", "desc": "舆情监控"},
    "etl": {"status": "planning", "desc": "数据导入工具"},
    "quiz": {"status": "planning", "desc": "知识图谱问答器"},
    "forecast": {"status": "planning", "desc": "时间序列预测"},
    "anomaly": {"status": "planning", "desc": "异常检测"},
    "llm": {"status": "planning", "desc": "LLM查询桥接器"},
    "essays": {"status": "planning", "desc": "Y的思考随笔"},
    "patterns": {"status": "planning", "desc": "分析模式库"},
    "templates": {"status": "planning", "desc": "运营模板库"},
}


def status():
    """显示实验室概览"""
    print("=" * 48)
    print("  y-lab — Y's Laboratory")
    print("=" * 48)
    print(f"\n  Projects:")
    for name, info in PROJECTS.items():
        status_icon = "✅" if "dev" in info["status"] else "📋"
        print(f"    {status_icon} {name:25s} {info['desc']}")
        print(f"       {info['status']:>32s}")
    print(f"\n  Frameworks:")
    for fw in (ROOT / "frameworks").glob("*.md"):
        print(f"    📄 {fw.stem}")
    print()


def run(project: str = "menu-engine"):
    """运行指定项目"""
    if project not in PROJECTS:
        print(f"Unknown project: {project}")
        print(f"Available: {', '.join(PROJECTS.keys())}")
        return
    proj_dir = ROOT / "projects" / project
    if not proj_dir.exists():
        print(f"Project directory not found: {proj_dir}")
        return
    print(f"Running {project}...")
    demo = proj_dir / "demo" / "run.py"
    if demo.exists():
        import subprocess
        import sys
        subprocess.run([sys.executable, str(demo)], cwd=proj_dir)
    else:
        print(f"No demo found for {project}. Check {proj_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run(sys.argv[2] if len(sys.argv) > 2 else "menu-engine")
    else:
        status()
