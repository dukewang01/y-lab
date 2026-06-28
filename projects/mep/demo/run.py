"""
y-mep Demo — 设备状态监控模拟
===============================
模拟 5 台设备，显示每台当前维保状态。
纯 Python，零外部依赖。
"""

import io
import sys

from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ── 设备数据（模拟） ──────────────────────────────────────────

# 当前基准日期
_TODAY = date.today()

EQUIPMENT = [
    {
        "id": "LIFT-001",
        "name": "电梯",
        # 上次保养在 365 天前 => 刚好今天到期
        "last_service": _TODAY - timedelta(days=365),
        "interval_days": 365,
    },
    {
        "id": "HVAC-002",
        "name": "空调",
        # 上次保养在 364 天前 => 明天到期（正常）
        "last_service": _TODAY - timedelta(days=364),
        "interval_days": 365,
    },
    {
        "id": "BOILER-003",
        "name": "锅炉",
        # 上次保养在 362 天前 => 3 天前到期（到期保养）
        "last_service": _TODAY - timedelta(days=362),
        "interval_days": 365,
    },
    {
        "id": "PUMP-004",
        "name": "水泵",
        # 上次保养在 380 天前 => 15 天前到期（已过期）
        "last_service": _TODAY - timedelta(days=380),
        "interval_days": 365,
    },
    {
        "id": "GEN-005",
        "name": "发电机",
        # 上次保养在 100 天前 => 265 天后到期（正常）
        "last_service": _TODAY - timedelta(days=100),
        "interval_days": 365,
    },
]


# ── 状态检查函数 ─────────────────────────────────────────────

def check_status(equip, today):
    """返回 (状态文本, 下次保养日期, 超期天数)"""
    next_due = equip["last_service"] + timedelta(days=equip["interval_days"])
    overdue = (today - next_due).days

    if overdue < 0:
        return "正常", next_due, 0
    elif overdue <= 3:
        return "到期保养", next_due, overdue
    else:
        return "已过期", next_due, overdue


# ── 表格渲染 ─────────────────────────────────────────────────

def render_row(index, equip, status, next_due, overdue):
    """渲染单行显示"""
    status_display = {
        "正常":     "\033[32m正常\033[0m",       # 绿色
        "到期保养": "\033[33m到期保养\033[0m",    # 黄色
        "已过期":   "\033[31m已过期\033[0m",      # 红色
    }.get(status, status)

    suffix = f" ⚠️" if status == "已过期" else ""

    if overdue > 0:
        detail = f"已超期: +{overdue} 天"
    else:
        detail = f"下次保养: {next_due}"

    return f" {index}. {equip['name']} {equip['id']:>10s}  [{status_display:>10s}]  {detail}{suffix}"


# ── 主程序 ───────────────────────────────────────────────────

def main():
    today = date.today()
    summary = {"正常": 0, "到期保养": 0, "已过期": 0}

    print()
    print("━━━ y-mep 设备状态监控 Demo ━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"    基准日期: {today}")
    print()

    for idx, equip in enumerate(EQUIPMENT, start=1):
        status, next_due, overdue = check_status(equip, today)
        summary[status] += 1
        line = render_row(idx, equip, status, next_due, overdue)
        print(line)

    print()
    print("━━━ 摘要 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for status, count in [("正常", summary["正常"]),
                           ("到期保养", summary["到期保养"]),
                           ("已过期", summary["已过期"])]:
        marker = "  ← 需要立即处理" if status == "已过期" and count > 0 else ""
        print(f" {status:>8s} : {count} 台{marker}")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    # 如果有已过期的设备，给出行动建议
    if summary["已过期"] > 0:
        print(" 🛑 已过期设备:")
        for equip in EQUIPMENT:
            status, next_due, overdue = check_status(equip, today)
            if status == "已过期":
                print(f"    - {equip['name']} ({equip['id']}) 逾期 {overdue} 天")
        print()
        print(" 💡 建议: 立即安排保养，避免设备故障影响运营。")
        print()


if __name__ == "__main__":
    main()
