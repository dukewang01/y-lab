# Menu Engineering Deep (菜单工程·深度版)

> 不是简单的菜单，是**酒店餐饮的智慧大脑**。  
> 三层架构：感知 → 分析 → 回答，让每一道菜都会说话。

---

## 🧭 核心引擎

三层递进架构，从数据采集到智能决策：

```
┌─────────────────────────────────────────────┐
│              回答层 · Answer                  │
│  自然语言查询 → 菜单建议 → 行动方案            │
├─────────────────────────────────────────────┤
│              分析层 · Analyze                  │
│  BCG矩阵 / 成本率 / 利润贡献 / 趋势 / 情绪     │
├─────────────────────────────────────────────┤
│              感知层 · Sense                    │
│  采购数据 / 菜品定价 / 投诉反馈 / 客户偏好      │
└─────────────────────────────────────────────┘
```

---

## 📦 脚本清单

### 核心引擎 (5个)

| 脚本 | 大小 | 功能 |
|:-----|:----:|:-----|
| `_menu_sense_core.py` | **16.8KB** 🏆 | 市场感知菜单引擎核心 — **最大的单一脚本** |
| `_menu_engineering.py` | 5.6KB | 菜单工程分析框架 — FB+FIN双图合并分析 |
| `_menu_engineering_matrix.py` | 1.5KB | BCG矩阵生成器 |
| `_menu_sense_scout.py` | 4.7KB | 菜单侦察器 — 搜索/推荐/市场感知 |
| `_menu_sense_scout2.py` | 1.3KB | 侦察器增强版 |

### 已有菜单引擎 (来自 menu-engine 项目)

| 模块 | 大小 | 功能 |
|:-----|:----:|:-----|
| `engine/sense.py` | 1.8KB | 感知引擎基座 |
| `engine/analyze.py` | 4.6KB | 分析逻辑 (销售/成本/分类) |
| `engine/answer.py` | 5.5KB | 自然语言回答生成 |
| `sensors/price_index.py` | 3.8KB | 价格指数传感器 |
| `sensors/trend_sensor.py` | 2.7KB | 趋势传感器 |
| `adapters/csv_adapter.py` | 3.4KB | CSV数据适配器 |
| `demo/run.py` | 2.3KB | 引擎运行演示 |

---

## 🧠 能力体系

### 1. 菜单分析 (What's on the menu?)

```
• 菜品定价分布        — 各店/各品类价格带分布
• 成本率分析           — 食材成本 / 毛利率
• BCG矩阵             — 明星/金牛/问题/瘦狗
• 利润贡献排行         — 哪个菜赚最多
```

### 2. 感知 (Market Sense)

```
• 价格感知             — 竞品价格对标 / 价格弹性
• 趋势感知             — 季节变化 / 流行趋势
• 情绪感知             — 投诉关键词 / 好评亮点
• 偏好感知             — CRM客户偏好画像
```

### 3. 推荐 (What to do?)

```
• 菜单优化             — 增删改菜品建议
• 定价策略             — 上调/下调/捆绑推荐
• 促销建议             — 折扣力度/时段选择
• 供应链影响           — 成本波动下的替换方案
```

---

## 📊 数据源

| 数据源 | 来源 | 用途 |
|:------|:-----|:-----|
| FB知识图谱 | `fb_graph.json` | 菜品/定价/Outlet/促销 |
| FIN知识图谱 | `fin_graph.json` | 采购成本/供应商业绩 |
| GSM图谱 | `gsm_graph.json` | 投诉/差评分析 |
| CRM偏好 | `fb_crm/preferences.json` | 客户口味画像 |
| CRM客群 | `fb_crm/guests.json` | 客群RFM分层 |
| 促销图谱 | `fb_crm/518_promo_graph.json` | 历史促销数据 |

---

## 💡 典型查询

```
"OPEN自助餐哪个菜成本率最高？"
→ 返回TOP5高成本菜品 + 替换建议

"YUXI的明星菜品有哪些？"
→ BCG矩阵中的明星象限菜品

"推荐一个适合夏季的新菜单"
→ 基于季节+成本+偏好的综合建议

"BACIO的利润贡献排行"
→ 各菜品利润贡献TOP10

"这个月牛肉成本涨了，哪些菜受影响？"
→ 成本变动影响分析 + 替换方案
```

---

## 🔄 与现有项目的关系

| 相关项目 | 关系 |
|:---------|:-----|
| `menu-engine` (11py) | 基础引擎模块 — 提供sense/analyze/answer基础设施 |
| `menu-engineering-deep` (5py) | **深度分析层** — 核心算法/矩阵/Scout |
| `menu-advisor` (2py) | 菜单顾问 — 基于此引擎的轻量级应用 |
| `fb-analysis` (14py) | F&B营收分析 — 提供营收和促销历史数据 |
| `crm-analysis` (11py) | CRM客户分析 — 提供偏好画像输入 |

---

## 🚀 快速开始

```python
from menu_sense_core import MenuSenseEngine

engine = MenuSenseEngine()

# 问一个问题
print(engine.ask("推荐一个高利润的晚餐套餐"))

# 看BCG矩阵
matrix = engine.build_bcg_matrix("OPEN")
print(matrix)

# 成本分析
cost_analysis = engine.analyze_costs("YUXI")
print(cost_analysis.top5_high_cost())
```
