# Rev Manager (收益管理智能体)

酒店收益管理智能分析系统。核心能力：基于历史数据+实时市场，自动给出最优定价建议。

## 脚本清单 (9个)

| 脚本 | 功能 |
|:-----|:-----|
| `_revpar_deep.py` | RevPAR深度分析 (8.8KB — 核心引擎) |
| `_revenue_analysis.py` | 营收综合分析 |
| `_analyze_occ_structure.py` | 入住率结构拆解 (散客/团队/Condo) |
| `_analyze_pace.py` | 预订节奏/提前天数分析 |
| `_price_targets.py` | 价格目标/底线分析 |
| `_scenario_test.py` | 场景模拟测试 |
| `_estimate_chengchang.py` | 成长率估算 |
| `_estimate_storage_earnings.py` | 库存收益估算 |
| `_generate_price_target_word.py` | 价格目标报告生成 |

## 核心能力

| 能力 | 说明 |
|:-----|:------|
| **价格弹性分析** | ADR上调/下调对Occ的影响 |
| **预订节奏** | 提前天数分布、取消率 |
| **场景模拟** | 如果ADR从¥630→¥650，RevPAR变化？ |
| **竞争对标** | 竞品价格变动时的应对策略 |
| **库存管理** | 未来N天可售房优化 |

## 数据输入

- DRR日报（历史Occ/ADR/RevPAR）
- 预订系统Pace数据
- 竞品价格（GCM/公开数据）
- 节假日/大型活动日历

## 典型输出

```
📊 RevManager建议 — 明天{日期}

当前预测Occ: 72.3% | ADR: ¥658 | RevPAR: ¥475
竞品均价: ¥690 | 建议ADR: ¥680 (+3.3%)

理由:
- 明天有{X}活动，预计增量需求
- 当前预订节奏超前LY 8%
- 竞品已上调¥30

风险: 上调¥22可能降低Occ 2pp → 净RevPAR+1.1%
```
