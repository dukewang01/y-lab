"""
y-fsaa 极简可运行原型
酒店食品安全审计模拟 — 无需外部依赖
"""

import random
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


# ─── 数据模型 ───────────────────────────────────────

@dataclass
class AuditItem:
    """单个检查项"""
    name: str         # 检查项名称
    area: str         # 区域
    result: bool      # True=通过, False=未通过
    severity: str     # 严重/中等/轻微
    person: str       # 责任人
    suggestion: str   # 整改建议


@dataclass
class AuditReport:
    """审计报告"""
    title: str
    date: str
    items: List[AuditItem] = field(default_factory=list)
    passed: int = 0
    failed: int = 0

    @property
    def total(self) -> int:
        return self.passed + self.failed

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.passed / self.total * 100, 1)

    def to_text(self) -> str:
        """输出纯文本报告"""
        sep = "═" * 45
        out = [
            f"╔{sep}╗",
            f"║      y-fsaa 食品安全审计 - 演示报告      ║",
            f"╠{sep}╣",
            f"║ 标题:    {self.title:<34}║",
            f"║ 日期:    {self.date:<34}║",
            f"╠{sep}╣",
            f"║ 检查项总数: {self.total:<5}                    ║",
            f"║ 通过:       {self.passed:<5}                    ║",
            f"║ 未通过:     {self.failed:<5}                    ║",
            f"║ 通过率:    {self.pass_rate:<5}%                  ║",
            f"╠{sep}╣",
        ]

        failed_items = [it for it in self.items if not it.result]
        if failed_items:
            out.append(f"║ ❌ 问题项 ({len(failed_items)}):                     ║")
            for i, it in enumerate(failed_items, 1):
                out.append(f"║ {'':>41}║")
                out.append(f"║ {i}. {it.name:<38} ║")
                out.append(f"║    区域: {it.area:<34} ║")
                out.append(f"║    等级: {it.severity:<4} | 责任人: {it.person:<8}    ║")
                out.append(f"║    建议: {it.suggestion:<34} ║")

        out.append(f"╚{sep}╝")
        return "\n".join(out)


# ─── 模拟数据 ───────────────────────────────────────

def simulate_checklist() -> List[AuditItem]:
    """模拟5个检查项：3通过2未通过"""
    return [
        AuditItem(
            name="冰箱温度正常",
            area="冷库",
            result=True,
            severity="—",
            person="—",
            suggestion="—"
        ),
        AuditItem(
            name="食材标签完整",
            area="粗加工间",
            result=True,
            severity="—",
            person="—",
            suggestion="—"
        ),
        AuditItem(
            name="冰箱温度异常",
            area="冷库",
            result=False,
            severity="严重",
            person="张三",
            suggestion="调整温控设备，增加每日2次温度记录"
        ),
        AuditItem(
            name="餐具消毒达标",
            area="洗碗间",
            result=True,
            severity="—",
            person="—",
            suggestion="—"
        ),
        AuditItem(
            name="员工健康证过期",
            area="热菜间",
            result=False,
            severity="中等",
            person="李四",
            suggestion="健康证到期前30天启动续期流程"
        ),
    ]


# ─── 主入口 ────────────────────────────────────────

def main():
    title = "中厨房6月第二次专项审计"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    items = simulate_checklist()
    passed = sum(1 for it in items if it.result)
    failed = sum(1 for it in items if not it.result)

    report = AuditReport(
        title=title,
        date=date,
        items=items,
        passed=passed,
        failed=failed,
    )

    print(report.to_text())

    # 统计附加
    print()
    print("── 整改追踪 ──")
    for it in items:
        if not it.result:
            print(f"  [🔴] {it.name} — 责任人: {it.person}")
            print(f"       建议: {it.suggestion}")
            print(f"       状态: ⏳ 待整改")
    print()
    print("✨ 演示完成 — 集成飞书/数据库后即可投入生产使用")


if __name__ == "__main__":
    main()
