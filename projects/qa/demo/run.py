"""
y-qa Demo -- 品牌标准模拟自查+评分+差距分析

模拟5个希尔顿品牌标准检查项，展示完整闭环：
  自查输入 -> 加权评分 -> 合格判定 -> 差距分析 -> 整改建议

零外部依赖，仅用标准库。
"""

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class CheckItem:
    """单个品牌标准检查项"""
    name: str           # 检查项名称
    score: float        # 实际得分 (0-100)
    weight: float       # 权重 (0.0 - 1.0)，单项之和不一定为1
    pass_line: float    # 合格线

    def is_pass(self) -> bool:
        return self.score >= self.pass_line

    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class AuditResult:
    """一次自查的结果"""
    hotel: str
    area: str
    items: List[CheckItem]

    def total_weight(self) -> float:
        return sum(i.weight for i in self.items)

    def overall_score(self) -> float:
        """加权综合得分（已归一化）"""
        raw = sum(i.weighted_score() for i in self.items)
        tw = self.total_weight()
        return raw / tw if tw > 0 else 0.0

    def pass_rate(self) -> float:
        """合格项占比"""
        if not self.items:
            return 0.0
        passed = sum(1 for i in self.items if i.is_pass())
        return passed / len(self.items)

    def summary(self) -> dict:
        return {
            "hotel": self.hotel,
            "area": self.area,
            "overall_score": round(self.overall_score(), 1),
            "pass_rate": round(self.pass_rate() * 100, 1),
            "total_items": len(self.items),
            "passed": sum(1 for i in self.items if i.is_pass()),
        }


# ---------------------------------------------------------------------------
# 差距分析
# ---------------------------------------------------------------------------

@dataclass
class Gap:
    """单个差距项"""
    item: str
    actual: float
    required: float
    deficit: float
    severity: str  # CRITICAL / NEEDS / PASS

    def __post_init__(self):
        if self.deficit > 20:
            self.severity = "[CRITICAL]"
        elif self.deficit > 0:
            self.severity = "[NEEDS]"
        else:
            self.severity = "[PASS]"

    def suggestion(self) -> str:
        if self.deficit > 20:
            return f"[URGENT] {self.item} 距合格线差 {self.deficit:.0f} 分，建议立即整改并安排复查"
        elif self.deficit > 0:
            return f"{self.item} 距合格线差 {self.deficit:.0f} 分，下次巡检前重点改进"
        return f"{self.item} 已达标，保持现状"


def analyze_gaps(result: AuditResult) -> List[Gap]:
    """将得分与合格线逐项对比，返回差距列表"""
    gaps = []
    for item in result.items:
        deficit = item.pass_line - item.score
        if deficit < 0:
            deficit = 0.0  # 达标不记为负差距，也不记为需改进
        gaps.append(Gap(item.name, item.score, item.pass_line, deficit, ""))
    return gaps


# ---------------------------------------------------------------------------
# 整改建议生成
# ---------------------------------------------------------------------------

def generate_actions(gaps: List[Gap]) -> List[str]:
    """根据差距生成可执行的整改建议"""
    actions = []
    for gap in gaps:
        if gap.deficit > 0:
            actions.append(gap.suggestion())
    if not actions:
        actions.append("全部达标，继续保持")
    return actions


# ---------------------------------------------------------------------------
# 展示
# ---------------------------------------------------------------------------

BORDER = "=" * 52


def show_result(result: AuditResult) -> None:
    """打印自查结果报告"""
    print(f"\n{BORDER}")
    print(f"  y-qa 品牌标准自查报告")
    print(f"  酒店：{result.hotel}  |  区域：{result.area}")
    print(BORDER)

    # 表头
    header = f"{'检查项':<12} {'得分':>5} {'权重':>5} {'合格线':>6} {'加权':>6} {'状态':>8}"
    print(f"\n{header}")
    print("-" * 48)

    for item in result.items:
        status = "[PASS]" if item.is_pass() else "[FAIL]"
        print(f"{item.name:<12} {item.score:>5.0f} {item.weight:>5.2f} "
              f"{item.pass_line:>6.0f} {item.weighted_score():>6.1f} {status:>8}")

    print("-" * 48)
    summary = result.summary()
    print(f"{'综合得分':<12} {summary['overall_score']:>5.1f} / 100")
    print(f"{'合格率':<12} {summary['pass_rate']:>5.1f}%  "
          f"({summary['passed']}/{summary['total_items']})")

    # 差距分析
    print(f"\n  [GAPS] 差距分析")
    print("-" * 48)
    gaps = analyze_gaps(result)
    for g in gaps:
        bar_len = int(g.actual / 10) if g.actual >= 0 else 1
        bar = "#" * bar_len + "." * (10 - bar_len)
        print(f"  {bar} {g.item:<10} {g.actual:>3.0f}/{g.required:>3.0f}  {g.severity}")

    # 整改建议
    print(f"\n  [ACTIONS] 整改建议")
    print("-" * 48)
    actions = generate_actions(gaps)
    for a in actions:
        print(f"  * {a}")

    # 最终判定
    print()
    overall = summary["overall_score"]
    if overall >= 90:
        verdict = "[EXCELLENT] 标杆！优秀标准执行"
    elif overall >= 80:
        verdict = "[GOOD] 良好，少数细节需优化"
    elif overall >= 70:
        verdict = "[WARNING] 需改进，建议制定整改计划"
    else:
        verdict = "[FAIL] 不合格，须立即行动"
    print(f"  判定：{verdict}")
    print(BORDER)


# ---------------------------------------------------------------------------
# 模拟数据生成
# ---------------------------------------------------------------------------

def demo_result() -> AuditResult:
    """生成一组模拟自查数据（5个检查项）"""
    items = [
        CheckItem(name="摆盘标准",  score=80, weight=0.25, pass_line=75),
        CheckItem(name="制服规范",  score=90, weight=0.20, pass_line=80),
        CheckItem(name="迎宾流程",  score=65, weight=0.25, pass_line=80),
        CheckItem(name="清洁卫生",  score=95, weight=0.20, pass_line=85),
        CheckItem(name="噪音控制",  score=70, weight=0.10, pass_line=75),
    ]
    return AuditResult(
        hotel="Hilton Beijing Wangfujing",
        area="前厅 & 餐饮",
        items=items,
    )


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def run_demo():
    """运行完整演示"""
    result = demo_result()
    show_result(result)


if __name__ == "__main__":
    run_demo()
