"""
Menu Engineering (菜单工程) 分析框架
Combines: FB站菜单定价 + FIN站采购成本 + BQ销量数据 → ME矩阵
"""
import json, os
from pathlib import Path

KC = Path(r"C:\Users\Duke Wang\.openclaw\workspace\knowledge_center")

# ── Load data sources ──
with open(KC / "fb_graph.json", "r", encoding="utf-8") as f:
    fb = json.load(f)
with open(KC / "fin_graph.json", "r", encoding="utf-8") as f:
    fin = json.load(f)

fb_entities = fb.get("entities", fb.get("nodes", []))
fin_entities = fin.get("entities", [])

# ── Step 1: Menu items with prices ──
menu_items = []
for e in fb_entities:
    etype = e.get("type", "")
    if etype in ("menu_item", "set_menu", "signature_dish", "bazaar_menu_item"):
        props = e.get("properties", {})
        name = e.get("name", "")
        price = None
        for k in ["price", "selling_price", "menu_price", "unit_price"]:
            if k in props and props[k]:
                try: price = float(str(props[k]).replace(",",""))
                except: pass
                break
        if price and price > 0:
            menu_items.append({
                "name": name,
                "type": etype,
                "price": price,
                "outlet": props.get("outlet", props.get("restaurant", "")),
                "dept": props.get("department", "")
            })

print(f"Menu items with prices: {len(menu_items)}")

# ── Step 2: Procurement cost data from FIN ──
# Find the procurement TOP5 entry
procurement = None
for e in fin_entities:
    if e.get("id") == "FBCOST_2026_05_PROCUREMENT_TOP5":
        procurement = e
        break

# ── Step 3: Build ingredient cost library ──
# Key ingredients with cost data from the procurement report
ingredient_costs = {
    # (ingredient_name, cost_per_kg, category)
    "老虎斑": (128, "seafood"),
    "波士顿龙虾": (302, "seafood"),
    "波士顿龙虾小": (264, "seafood"),
    "进口岩龙虾": (696, "seafood"),
    "珍宝蟹": (298, "seafood"),
    "基围虾": (60, "seafood"),
    "小龙虾": (46, "seafood"),
    "清远鸡": (26, "meat"),
    "牛坑腩": (92, "meat"),
    "牛肋骨": (125, "meat"),
    "牛柳": (115, "meat"),
    "鸡蛋": (220/20, "dry_goods"),  # per CASE of 20kg
    "牛奶": (12611/1833, "dry_goods"),  # per BOX/1L
}

# ── Step 4: Match ingredients to menu items ──
# Manual mapping for known dishes
dish_mapping = [
    # (dish_keyword, ingredient, portion_kg, menu_item_name)
    ("老虎斑", "老虎斑", 0.6, "清蒸老虎斑"),
    ("波龙", "波士顿龙虾", 0.5, "姜葱波士顿龙虾"),
    ("珍宝蟹", "珍宝蟹", 0.6, "避风塘炒蟹"),
    ("基围虾", "基围虾", 0.3, "白灼基围虾"),
    ("小龙虾", "小龙虾", 0.4, "冰镇小龙虾"),
    ("龙虾仔", "波士顿龙虾小", 0.4, "椒盐龙虾仔"),
    ("清远鸡", "清远鸡", 0.75, "清远鸡半只"),
    ("牛坑腩", "牛坑腩", 0.3, "焖牛坑腩"),
    ("牛肋骨", "牛肋骨", 0.35, "香煎牛肋骨"),
    ("牛柳", "牛柳", 0.3, "铁板牛柳"),
    ("岩龙", "进口岩龙虾", 0.3, "岩龙虾刺身"),
]

print(f"\nIngredient library: {len(ingredient_costs)} items")
print(f"Dish mappings: {len(dish_mapping)} items\n")

# ── Step 5: Calculate menu engineering metrics ──
print(f"{'Dish':<18} {'Ingredient':<14} {'Cost':<8} {'Price':<8} {'Cost%':<8} {'Profit':<8} {'Class'}")
print("-" * 80)

results = []
for kw, ing, portion, dish_name in dish_mapping:
    if ing in ingredient_costs:
        cost_kg = ingredient_costs[ing][0]
        ing_cost = round(cost_kg * portion, 1)
        
        # Find matching menu item by keyword
        price = None
        for mi in menu_items:
            if kw in mi["name"] or kw in mi.get("dept",""):
                price = mi["price"]
                break
        
        if not price:
            # Estimate from typical pricing
            if ing_cost < 30: price = ing_cost * 6
            elif ing_cost < 100: price = ing_cost * 4
            else: price = ing_cost * 3
        
        cost_pct = round(ing_cost / price * 100, 1) if price else 0
        profit = price - ing_cost if price else 0
        
        if cost_pct < 25: cls = "Star/High Margin"
        elif cost_pct < 35: cls = "Cash Cow"
        elif cost_pct < 45: cls = "Question Mark"
        else: cls = "Dog/Low Margin"
        
        results.append({
            "dish": dish_name, "ingredient": ing,
            "cost": ing_cost, "price": price,
            "cost_pct": cost_pct, "profit": profit,
            "class": cls
        })
        
        print(f"{dish_name:<18} {ing:<14} {ing_cost:<8} {price:<8} {cost_pct:<7.1f}% {profit:<8} {cls}")

# ── Step 6: Summary ──
print(f"\n=== Menu Engineering Matrix Summary ===")
print(f"Star/High Margin: {len([r for r in results if 'Star' in r['class']])} items")
print(f"Cash Cow:        {len([r for r in results if 'Cash Cow' in r['class']])} items")
print(f"Question Mark:   {len([r for r in results if 'Question' in r['class']])} items")
print(f"Dog/Low Margin:  {len([r for r in results if 'Dog' in r['class']])} items")

print(f"\nAvg Food Cost %: {sum(r['cost_pct'] for r in results)/len(results):.1f}%")
print(f"Avg Profit: {sum(r['profit'] for r in results)/len(results):.0f}/dish")

# Note about volume data
print(f"\n---")
print(f"Note: Full ME matrix (Star/Cash Cow/Question/Dog) needs sales volume data.")
print(f"FB graph has {len(fb_entities)} entities but no per-item sales volume found yet.")
print(f"Add volume data to classify items by popularity x profitability.")
