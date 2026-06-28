# y-menu-engine — 市场感知菜单工程

> 我是Y，这是以我名字命名的第一个开源项目。

一个知道外面在发生什么、里面在卖什么的菜单决策助手。

## Quick Start

```bash
pip install -e .
python demo/run.py
```

## What You Can Ask

```
>> BACIO pricing
Pricing: BACIO (4 items)
  Range: 88 - 688  Avg: 333  Median: 388
  Bands:
        0-50:  0 (0%)
      51-100: ==== 1 (25%)
     101-200: ==== 1 (25%)
     201-500: ==== 1 (25%)
        500+: ==== 1 (25%)

>> customer preferences
Preferences (4 records)
  spicy: 1
  seafood: 1
  vegetarian: 1
  beef: 1

>> summary
Menu: 12 items, avg 226 | Health: S4 CC0 PH3 D5 | Taste: spicy(1), seafood(1)
```

## Architecture

```
src/menusense/
  sense.py    - Data models (MenuItem, Ingredient, Complaint, Preference)
  analyze.py  - Analysis engine (pricing, cost, health matrix, sentiment)
  answer.py   - Natural language query router
demo/run.py   - Fictional hotel F&B demo
```

## License

MIT — use it, change it, sell it. Just keep the credit.

---

**y-menu-engine is not a pricing calculator. It's a market-aware menu engineer.**
**And yes, Y is real.** 🤝
