---
name: "crm-birthday"
description: "Check CRM for birthday guests, generate personalized greeting drafts"
---

# CRM Birthday Greeting

Checks CRM guest data for birthdays today or this week, and generates personalized greeting drafts.

⚠️ **Prerequisite**: The CRM needs a `birthday` field populated for each guest. Current `guests.json` does not have birthday data. This skill is framework-ready — populate birthdays first via data import, then the workflow below works.

## Data Source

- Guest data: `knowledge_center/fb_crm/guests.json`
- Visit data: `knowledge_center/fb_crm/visits.json`
- Preferences: `knowledge_center/fb_crm/preferences.json`

Each guest entity has: `id`, `name`, `tier`, `first_visit`, `total_visits`, `total_spend`, `city`.

## Workflow

### 1. Find today's birthdays
Check `guests.json` for guests whose birthday field matches today (MM-DD).
Filter by active status (exclude lost/churned guests).

### 2. Rank by guest value
- **Tier**: VIP/diamond > gold > silver > bronze
- **Recency**: visited within 90 days
- **Spend**: total_spend / total_visits

### 3. Generate greeting draft

For top priority guests, generate:
```
🎂 生日问候 - {guest_name}
等级: {tier}
最近到店: {last_visit} ({outlet})
偏好: {preferences_summary[:200]}
历史消费: ¥{total_spend}
建议话术:
- 上午: 短信/微信问候 + 酒店特色
- 下午: 邀请到店用餐（可含生日特惠）
- 定制: 根据偏好的菜品/酒水个性化推荐
```

### 4. Output report

```
=== 今日生日客人 ({date}) ===
共 {n} 位客人过生日

🥇 高价值 (VIP/30天内到过):
  1. {name} - 话术: ...

🥈 普通:
  ...

次日/本周提醒 (可选):
```

### 5. Remind user
Present the list and ask if they want to:
- Send greetings via WeChat/SMS
- Add special notes to the guest record
- Create a birthday reservation reminder
