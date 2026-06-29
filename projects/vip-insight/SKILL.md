---
name: "vip-insight"
description: "Daily VIP alerts: churn risk, complaint history, recall recommendations"
---

# VIP Insight

Daily scan of CRM + GSM + FIN data to generate VIP guest alerts. Answers: "Who needs my attention today?"

## Data Sources

- **CRM**: `guests.json` (profile, spend, visits), `visits.json` (visit history)
- **GSM**: `gsm_graph.json` (complaint cases categories + linked entities)
- **FIN**: `fin_graph.json` (revenue data for stay detection)

## Alert Categories (Tri-tier)

### 🔴 Tier 1 — High Churn Risk
Active in last 12 months, then went silent for 90+ days.
- Criteria: total_spend >= 5,000 AND last_visit > 90 days ago AND <= 365 days ago
- Score = (spend / 1000) * (days / 30) * priority_multiplier
- Has guest complained? Check GSM for complaint_category matches
- **Action**: Immediate contact recommended

### 🟤 Tier 2 — Long-lost (Sleeping Giants)
Last visited more than a year ago, high historical value.
- Criteria: total_spend >= 10,000 AND last_visit > 365 days ago
- **Action**: Batch recall campaign (seasonal offers, holiday promotions)

### 🟢 Tier 3 — Currently in-house
Guest likely staying at the hotel based on DRR stay dates aligned with CRM last_visit.
- **Action**: Personalized greeting, upsell opportunities (via outlet preferences)

### 🎂 Tier 4 — Birthday (from crm-birthday)
Guests celebrating birthday this week.
- **Action**: Birthday offer + greeting

## Cross-Reference with GSM

For each churn-risk guest, check:
1. Does their complaint category exist in GSM? (search GSM complaint_category entities)
2. What's the top issue category for this guest? (noise/service/facility/pest/etc.)
3. Was compensation paid?
4. → Helps determine: "did they leave because of an unresolved issue?"

## Python Implementation

```python
import json, sys
from datetime import datetime, timedelta
sys.stdout.reconfigure(encoding='utf-8')

guests = json.load(open('knowledge_center/fb_crm/guests.json','r',encoding='utf-8'))
visits = json.load(open('knowledge_center/fb_crm/visits.json','r',encoding='utf-8'))
gsm = json.load(open('knowledge_center/gsm_graph.json','r',encoding='utf-8'))
fin = json.load(open('knowledge_center/fin_graph.json','r',encoding='utf-8'))

now = datetime.now()

# Build last_visit index
last_visit = {}
for v in visits:
    gid = v.get('guest_id')
    d = v.get('date','')
    if gid and d:
        if gid not in last_visit or d > last_visit[gid]:
            last_visit[gid] = d

# Tier 1: Churn Risk (90-365 days)
churn = []
# Tier 2: Long-lost (365+ days)
long_lost = []

for g in guests:
    gid = g['id']
    if gid not in last_visit or g.get('total_visits',0) == 0:
        continue
    try:
        last_dt = datetime.strptime(last_visit[gid], '%Y-%m-%d')
        days = (now - last_dt).days
        spend = g.get('total_spend', 0)
        name = g['name']
        
        if spend >= 5000 and 90 <= days <= 365:
            score = (spend / 1000) * (days / 30)
            # Check GSM for related complaints? (future enhancement)
            churn.append((score, name, spend, last_visit[gid], days))
        elif spend >= 10000 and days > 365:
            long_lost.append((spend, name, spend, last_visit[gid], days))
    except:
        pass

churn.sort(reverse=True)
long_lost.sort(reverse=True)

# Print report
print(f"[Tier 1] 流失预警: {len(churn)}人")
print(f"[Tier 2] 长期沉睡: {len(long_lost)}人")
```

**Note**: The GSM cross-reference is a future enhancement once individual guest-to-complaint mapping is built in the GSM graph.
