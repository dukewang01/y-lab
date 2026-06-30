import json
from pathlib import Path
from collections import Counter, defaultdict

kc = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center")

with open(kc / "fb_graph.json", "r", encoding="utf-8") as f:
    fb = json.load(f)

# 找有price字段的菜品
price_items = []
for e in fb.get("entities", []):
    p = e.get("properties", {})
    if "price" in p:
        price_items.append((e.get("name","?"), e.get("type","?"), str(p.get("price",""))))

print(f'有price字段的条目: {len(price_items)}')
types = Counter(t for _,t,_ in price_items)
for t,c in types.most_common():
    print(f"  {t}: {c}")

# 按outlet分组
outlet_items = defaultdict(list)
for e in fb.get("entities", []):
    p = e.get("properties", {})
    out = p.get("outlet","") or p.get("restaurant","") or ""
    if out and "price" in p:
        outlet_items[out].append(e.get("name","?"))

print()
for o, items in sorted(outlet_items.items()):
    print(f"  {o}: {len(items)}道菜")
print(f"总计有定价+outlet: {sum(len(v) for v in outlet_items.values())}道")

# 看看CRM偏好数据在哪
crm_dir = kc / "fb_crm"
if crm_dir.exists():
    print("\nCRM偏好文件:")
    for f in sorted(crm_dir.glob("*")):
        print(f"  {f.name} ({f.stat().st_size} bytes)")
