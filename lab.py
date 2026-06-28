"""
y-lab — Y's Laboratory CLI
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
PROJECTS = {
    "menu-engine": {"status": "v0.1 dev", "desc": "市场感知菜单工程"},
    "cost-predictor": {"status": "planning", "desc": "食材成本预测"},
    "complaint-classifier": {"status": "planning", "desc": "投诉自动分类器"},
    "menu-advisor": {"status": "planning", "desc": "菜单调整建议引擎"},
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
