# y-qa — 品牌标准管理系统

> 希尔顿品牌标准在线自查、评分与差距分析平台

## 定位

**y-qa** 是 y-lab 为希尔顿旗下酒店设计的一站式品牌标准管理平台，帮助各酒店从「被动迎检」升级为「主动合规」：

1. **在线自查** — 各部门按清单逐项自检，无需翻纸质手册
2. **智能评分** — 自动计算单项/类别/酒店三级得分与合格率
3. **差距分析** — 一眼看出哪里「差在哪」「差多少」「怎么补」
4. **标准变更通知** — 集团发布新标准后，自动推送关联部门

## 架构

```
y-qa/
├─ audit/         # 自查清单模块
│   ├─ checklist.json        # 标准检查项（按品牌/区域/级别）
│   ├─ inspection.py         # 自查引擎：分配 → 执行 → 记录
│   └─ report.py             # 检查报告生成
│
├─ score/         # 打分引擎
│   ├─ engine.py             # 权重 + 分级 + 合格线计算
│   ├─ formula.py            # 品牌特定评分公式（Hilton/HGI/HX 等）
│   └─ ranking.py            # 部门/酒店/区域排名
│
├─ gap/           # 差距分析
│   ├─ analyzer.py           # 对比基线 → 标红差距
│   ├─ priority.py           # 差距优先级排序（严重度 × 紧迫度）
│   └─ action.py             # 自动生成整改建议
│
├─ bulletin/      # 标准变更管理
│   ├─ ingester.py           # 解析集团 PDF / 邮件/内部文档
│   ├─ matcher.py            # 匹配变更影响的部门和检查项
│   └─ notifier.py           # 飞书/邮件/APP 推送
│
├─ demo/          # 演示 & 快速原型
│   └─ run.py                # 模拟5个检查项的完整闭环
│
└─ README.md
```

### 模块职责

| 模块 | 职责 | 典型接口 |
|------|------|---------|
| `audit` | 标准清单管理 + 自检流程 | `AuditSession.create(area, level)` → items |
| `score` | 评分计算 + 合格判定 | `ScoreEngine.run(items)` → scores, pass_rate |
| `gap` | 差距定位 + 根因分析 | `GapAnalyzer.analyze(scores, baseline)` → gaps |
| `bulletin` | 变更感知 + 影响扩散 | `BulletinService.ingest(doc).notify()` |

## 使用示例

### 快速体验

```bash
cd qa
python demo/run.py
```

示例输出：

```
====================================================
  y-qa 品牌标准自查报告
  酒店：Hilton Beijing Wangfujing  |  区域：前厅 & 餐饮
====================================================

检查项             得分    权重    合格线     加权       状态
------------------------------------------------
摆盘标准            80  0.25     75   20.0   [PASS]
制服规范            90  0.20     80   18.0   [PASS]
迎宾流程            65  0.25     80   16.2   [FAIL]
清洁卫生            95  0.20     85   19.0   [PASS]
噪音控制            70  0.10     75    7.0   [FAIL]
------------------------------------------------
综合得分          80.2 / 100
合格率           60.0%  (3/5)

  [GAPS] 差距分析
------------------------------------------------
  ########.. 摆盘标准        80/ 75  [PASS]
  #########. 制服规范        90/ 80  [PASS]
  ######.... 迎宾流程        65/ 80  [NEEDS]
  #########. 清洁卫生        95/ 85  [PASS]
  #######... 噪音控制        70/ 75  [NEEDS]

  [ACTIONS] 整改建议
------------------------------------------------
  * 迎宾流程 距合格线差 15 分，下次巡检前重点改进
  * 噪音控制 距合格线差 5 分，下次巡检前重点改进

  判定：[GOOD] 良好，少数细节需优化
====================================================
```

### 集成 API

```python
from yqa.score import ScoreEngine
from yqa.gap import GapAnalyzer

# 评分
scores = ScoreEngine.evaluate(checklist_results, brand="hilton")
print(scores.total, scores.pass_rate)

# 差距分析
gaps = GapAnalyzer.compare(scores, baseline="Q1_2026_PASS_THRESHOLD")
for g in gaps:
    print(f"[{g.severity}] {g.item} — {g.deficit} 分")
```

## 开发计划

| 阶段 | 内容 | 状态 |
|------|------|------|
| P0   | demo/run.py（模拟闭环） | ✅ 完成 |
| P1   | audit 模块：JSON 清单 + 自检流程 | ⬜️ |
| P2   | score 模块：权重 + 合格线 + 排名 | ⬜️ |
| P3   | gap 模块：差距分析 + 整改建议 | ⬜️ |
| P4   | bulletin 模块：变更摄取 + 推送 | ⬜️ |
| P5   | 飞书 bot 集成 + 看板视图 | ⬜️ |

## 品牌支持矩阵（规划）

| 品牌 | 标准数 | 检查维度 | 评分公式 |
|------|--------|---------|---------|
| Hilton Hotel & Resorts | 200+ | 10 | 加权平均 |
| Hilton Garden Inn | 150+ | 8 | 精简加权 |
| Hampton by Hilton | 120+ | 6 | 门纲法 |
| DoubleTree by Hilton | 160+ | 8 | 加权平均 |
| HX (Hilton X) | 180+ | 9 | 体验加权 |

## 贡献

欢迎提交 PR 补充新品牌标准清单或改进评分模型。

---

*Built for y-lab, crafted for Hilton.*
