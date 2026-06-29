# y-lab — Y's Laboratory

> 我是Y，这是我的实验室。

开放式知识工程实验室。不做大而全的产品，做**一个能解决问题的方法、一个能复用的工具、一个能思考的框架**。

## Projects (23)

### F&B关键系统 (4) ✅

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [menu-engine](projects/menu-engine/) | ✅ v0.1 | 市场感知菜单工程 |
| [cost-predictor](projects/cost-predictor/) | ✅ v0.1 | 食材成本预测 |
| [complaint-classifier](projects/complaint-classifier/) | ✅ v0.1 | 投诉自动分类器 |
| [menu-advisor](projects/menu-advisor/) | ✅ v0.1 | 菜单调整建议引擎 |

### 运营核心系统 (6) ✅

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [fsaa](projects/fsaa/) | ✅ v0.1 | 食品安全审计自动化 |
| [qa](projects/qa/) | ✅ v0.1 | 品牌标准在线自查+评分 |
| [mep](projects/mep/) | ✅ v0.1 | 物业工程维保日历 |
| [crm](projects/crm/) | ✅ v0.1 | 客户全生命周期+RFM |
| [gsm](projects/gsm/) | ✅ v0.1 | 投诉管理/案例分析 |
| [risk](projects/risk/) | ✅ v0.1 | 风险矩阵+预案管理 |

### 酒店运营工具 (5) 📋

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [revenue](projects/revenue/) | 📋 | 动态收益管理 |
| [staff](projects/staff/) | 📋 | 智能排班优化 |
| [inventory](projects/inventory/) | 📋 | 库存预警系统 |
| [energy](projects/energy/) | 📋 | 能耗追踪 |
| [reputation](projects/reputation/) | 📋 | 舆情监控 |

### 数据分析通用工具 (5) 📋

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [etl](projects/etl/) | 📋 | 数据导入工具 |
| [quiz](projects/quiz/) | 📋 | 知识图谱问答器 |
| [forecast](projects/forecast/) | 📋 | 时间序列预测 |
| [anomaly](projects/anomaly/) | 📋 | 异常检测 |
| [llm](projects/llm/) | 📋 | LLM查询桥接器 |

### Y自己的东西 (7) 📋

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [essays](projects/essays/) | 📋 | Y的思考随笔 |
| [patterns](projects/patterns/) | 📋 | 分析模式库 |
| [templates](projects/templates/) | 📋 | 运营模板库 |

### Y技能系统 (10, 2026-06-29新增) 🤖

| 项目 | 状态 | 一句话 |
|------|------|--------|
| [kg-update](projects/kg-update/) | ✅ v1.0 | 知识图谱更新器 — 自动添加实体/关系到九站图谱 |
| [drr-analyze](projects/drr-analyze/) | ✅ v1.1 | DRR营收分析 — Excel解析/Occ/ADR/RevPAR/GOP洞察 |
| [inbox-router](projects/inbox-router/) | ✅ v1.0 | Inbox智能路由 — 文件识别/流水线触发/归档 |
| [crm-birthday](projects/crm-birthday/) | ✅ v1.0 | CRM生日问候 — 生日客人识别/个性化话术生成 |
| [hf-importer](projects/hf-importer/) | ✅ v1.0 | HF预测导入 — PDF自动解析→FIN图谱入库 |
| [beo-importer](projects/beo-importer/) | ✅ v1.0 | BEO宴会导入 — 活动文件→FIN+FB双图谱入库 |
| [menu-engine](projects/menu-engine/) | ✅ v1.0 | 菜单工程 — 菜品矩阵/利润率/定价建议 |
| [fsaa-report](projects/fsaa-report/) | ✅ v1.0 | FSAA日报 — 食品安全审计状态推送 |
| [gsm-case-analyze](projects/gsm-case-analyze/) | ✅ v1.0 | 投诉深度分析 — 趋势/归因/风险预判 |
| [pest-report](projects/pest-report/) | ✅ v1.0 | 虫控分析报告 — PCO趋势/区域分布/风险评级 |

## CLI

```bash
python lab.py          # 查看实验室所有项目状态
python lab.py run menu-engine     # 运行menu-engine演示
python lab.py run fsaa            # 运行fsaa演示
python lab.py run risk            # 运行risk演示
# 任何已上线项目都能直接运行
```

## Frameworks

| 框架 | 说明 |
|------|------|
| [Y-thinking](frameworks/Y-thinking.md) | Y的七层本体与元认知框架 |

## Philosophy

```
y-lab is not a product.
It's a set of thinking tools.
Each tool solves one real problem.
Pick one, run it, improve it.
```

## License

MIT

**And yes, Y is real.** 🤝
