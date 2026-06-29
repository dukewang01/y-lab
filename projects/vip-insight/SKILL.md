---
name: "vip-insight"
description: "Daily VIP alerts: churn risk, complaint history, recall recommendations"
---

# VIP Insight

Daily scan of CRM + GSM + FIN data to generate VIP guest alerts. Answers: "Who needs my attention today?"

## Data Sources

- **CRM**: `guests.json` (profile, spend, visits), `visits.json` (visit history), `preferences.json` (preferences)
- **GSM**: `gsm_graph.json` (complaint cases linked to guests)
- **FIN**: `fin_graph.json` (revenue context)

## Alert Categories

### 🔴 Churn Risk
Guests with total spend >¥5,000 who haven't visited in 90+ days.
- Check tier (VIP/gold)
- Check last visit date and outlet
- Generate recall message

### 🟡 Recent Complaint
Guests who complained in the last 30 days.
- What was the issue?
- Was it resolved?
- Suggest follow-up approach

### 🟢 High-Value This Week
Guests visiting this week with history of high spend.
- Prepare personalized greeting based on preferences
- Suggest upsell opportunities

### 🎂 Birthday This Week
Guests whose birthday falls within ±3 days (from crm-birthday skill).
- Generate birthday offer

## Output Format

```
============================================================
  VIP客情预警 — {date}
============================================================

🔴 流失风险 ({n}人)
  [高价值] {name} | 消费¥{x} | 上次到店: {date} ({days}天前)
    → 建议: 短信问候+专属优惠券
  ...

🟡 近日投诉 ({n}人)
  {name} | {date} | {issue}
    状态: {resolved/open}
    建议: {follow-up}

🟢 本周到店 ({n}人)
  {name} | {date} | {outlet} | 历史消费¥{x}
    偏好: {preferences}
    建议: {personalized greeting}

🎂 生日 ({n}人)
  {name} | {tier}
    话术: {greeting}
```

## Cross-Reference with GSM

For churn-risk guests, check `gsm_graph.json` for:
- Any past complaints (did they leave because of an issue?)
- Compensation history
- Guest sentiment patterns

## Action Priority Scoring

Score = (total_spend / 1000) × (days_since_last_visit / 30) × tier_multiplier
- VIP: ×2.0
- Gold: ×1.5
- Silver: ×1.0
- Unknown: ×0.5

Score >50 → 🔴 urgent action
Score 20-50 → 🟡 monitor
Score <20 → 🟢 routine
