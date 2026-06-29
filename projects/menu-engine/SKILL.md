---
name: "menu-engine"
description: "Menu engineering: item matrix, profitability, pricing recommendations"
---

# Menu Engineering

Analyzes menu item performance (popularity × profitability), generates menu engineering matrix, and provides actionable recommendations.

## Data Sources

- Menu items: `fb_graph.json` (FB_ME_* entities)
- Cost data: from procurement reports or manual input
- Sales data: from DRR F&B data or outlet reports

## Workflow

### 1. Identify target menu/outlet
User specifies: OPEN buffet, YUXI à la carte, BACIO Italian, etc.

### 2. Load menu items
From `fb_graph.json`, find entities matching the outlet (e.g. `FB_ME_OPEN`, `FB_MENU_YUXI`).

### 3. Build engineering matrix

Calculate for each menu item:
- **Popularity**: % of total covers that ordered this item
- **Profitability**: (selling price - cost) / selling price
- **Category**:
  - ⭐ **Stars**: High popularity × High profitability
  - 🐎 **Plowhorses**: High popularity × Low profitability
  - 🧩 **Puzzles**: Low popularity × High profitability
  - 🐕 **Dogs**: Low popularity × Low profitability

### 4. Generate report

```
=== Menu Engineering: {outlet} ===
总菜品: {n} | 日均销量: {x}

⭐ Stars (高人气×高利润):
  {item} | ¥{price} | 利润率{x}% | 销量{n}

🐎 Plowhorses (高人气×低利润):
  ...

🧩 Puzzles (低人气×高利润):
  ...

🐕 Dogs (低人气×低利润):
  ...

📊 建议:
  1. Stars → 突出展示/主推
  2. Plowhorses → 提价或降本
  3. Puzzles → 增加曝光/试吃
  4. Dogs → 考虑替换或删减
```

### 5. Optional: FIN cost integration
Cross-reference with `fin_graph.json` cost data for accurate margin calculation.
