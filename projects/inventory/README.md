# y-inventory — 库存预警系统

食材临期提醒+自动补货建议。

## 解决的痛点

> 冰箱里的食材过期了才发现，造成浪费和成本损失。

## 架构

```
inventory/
├── tracking/     — 库存实时状态（品名/数量/有效期）
├── alert/        — 临期预警+过期报警
├── reorder/      — 自动补货建议（基于历史消耗速率）
└── waste/        — 浪费分析报告
```

## 用法

```python
from inventory import InventoryManager

inv = InventoryManager()
inv.add("牛肉", qty=50, unit="kg", expiry="2026-07-10")
inv.add("基围虾", qty=20, unit="kg", expiry="2026-06-29")
alerts = inv.check_expiry()  # 返回即将过期的物品
reorder = inv.suggest_reorder()  # 建议补货
```
