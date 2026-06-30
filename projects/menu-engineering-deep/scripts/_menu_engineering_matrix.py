# Menu Engineering Analysis Script
# Run: python knowledge_center/_menu_engineering_matrix.py
# Outputs: ME matrix (Star/Cash Cow/Question/Dog) for bazaar menu items

import json
from pathlib import Path

KC = Path(__file__).parent
with open(KC / "fb_graph.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entities = data.get("entities", [])
items = []
for e in entities:
    if e.get("type") == "bazaar_menu_item":
        p = e.get("properties", {})
        if p.get("appearances", 0) >= 5:
            items.append({
                "name": e.get("name", "?"),
                "apps": p.get("appearances", 0),
                "avg_price": (p.get("avg_price", 0) or 0) * 100,
                "avg_rev": p.get("avg_revenue", 0) or 0,
                "sell_rate": round(((p.get("avg_sell_rate", 0) or 0) * 100), 1),
                "total_rev": p.get("total_revenue", 0) or 0,
                "lifecycle": f"{p.get('first_seen','?')[:7]} -> {p.get('last_seen','?')[:7]}"
            })

# Classify
stars = [i for i in items if i['sell_rate'] >= 85 and i['avg_rev'] >= 120]
cows = [i for i in items if i['sell_rate'] >= 70 and i['avg_rev'] < 120]
questions = [i for i in items if i['sell_rate'] < 70 and i['avg_rev'] >= 120]
dogs = [i for i in items if i['sell_rate'] < 70 and i['avg_rev'] < 120]

print(f"Menu Engineering Matrix: {len(items)} items")
print(f"Stars: {len(stars)} | Cash Cows: {len(cows)} | Questions: {len(questions)} | Dogs: {len(dogs)}")
