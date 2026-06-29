---
name: "daily-summary"
description: "Generate daily hotel ops briefing: FIN/FB/GSM/CRM/FSAA all in one"
---

# Daily Summary

Generates a comprehensive daily hotel operations briefing by pulling data from all knowledge stations. One scan, one report, full picture.

## Data Sources (All Stations)

| Station | What to scan | Key entities |
|---------|-------------|--------------|
| **FIN** | Latest DRR/Revenue | `DAILY_*`, `MONTHLY_*` entities, GOP, RevPAR |
| **FB** | Promotions, menus, BEO events | `BEO_*`, `FB_PROMO_*`, menu changes |
| **GSM** | Recent complaints | Cases in last 7 days, comp totals, category trends |
| **CRM** | Guest metrics | VIP arrivals today, recent churn alerts |
| **FSAA** | Food safety | Open NCs, PCO findings, recent audits |
| **FAQ** | Usage | Recently accessed FAQs |
| **LIB** | New knowledge | Recent book/chapter additions |

## Report Sections

### 1. 🏨 财务快照 (FIN)
```
客房: Occ {x}% | ADR ¥{x} | RevPAR ¥{x} | 收入¥{x}
F&B: 当日¥{x} | 月累计¥{x}
预算达标: {metric} {±x.x%}
```

### 2. 🍽️ F&B动态 (FB)
```
今日宴会: {n}场 | 营收¥{x}
特推: {promo}
早餐SALT: {score}
```

### 3. 📋 客诉焦点 (GSM)
```
近7天:{n}件 | 赔偿¥{x}
重点: {top_category} ({n}件)
```

### 4. 👥 客情 (CRM)
```
VIP到店: {n}人 | {names}
流失预警: {n}人
```

### 5. 🛡️ 食品安全 (FSAA)
```
NC未关闭: {n}项 | PCO: {n}发现
```

### 6. 💡 今日提醒
```
- {action item 1}
- {action item 2}
```

## Workflow

1. Load each station's graph
2. Extract the latest/relevant data (last 7 days for GSM, latest DRR for FIN)
3. Format into concise briefing
4. Output to user

## Frequency

- Daily (morning): Full briefing
- On-demand: Quick check when user asks "今天什么情况?"
