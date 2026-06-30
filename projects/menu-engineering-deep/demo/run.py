import sys
sys.path.insert(0, "src")

from menusense import SenseEngine, MenuSense, MenuItem, Ingredient, Complaint, Preference

# -- Restaurant data (fictional) --
sense = SenseEngine()
sense.load_menu([
    MenuItem("Australian M5 Wagyu", "BACIO", 688, "main"),
    MenuItem("Lobster Linguine", "BACIO", 388, "main"),
    MenuItem("Parma Ham & Melon", "BACIO", 168, "starter"),
    MenuItem("Tiramisu", "BACIO", 88, "dessert"),
    MenuItem("Steamed Grouper", "YUXI", 498, "main"),
    MenuItem("Dongpo Pork", "YUXI", 138, "main"),
    MenuItem("Kung Pao Chicken", "YUXI", 88, "main"),
    MenuItem("Fried Rice", "YUXI", 38, "staple"),
    MenuItem("Weekday Lunch Buffet", "OPEN", 198, "buffet"),
    MenuItem("Weekend Dinner Buffet", "OPEN", 298, "buffet"),
    MenuItem("Craft Beer (Glass)", "BEER SOCIETY", 58, "beverage"),
    MenuItem("Chicken Wings", "BEER SOCIETY", 68, "snack"),
])
sense.load_ingredients([
    Ingredient("Wagyu Beef", 320, "kg", {"Jan":300, "Feb":310, "Mar":315, "Apr":320, "May":330, "Jun":340}),
    Ingredient("Lobster", 280, "kg", {"Jan":260, "Feb":270, "Mar":280, "Apr":290, "May":285, "Jun":280}),
    Ingredient("Grouper", 128, "kg", {"Jan":120, "Feb":125, "Mar":128, "Apr":130, "May":135, "Jun":140}),
    Ingredient("Beef Brisket", 92, "kg", {"Jan":85, "Feb":88, "Mar":90, "Apr":92, "May":95, "Jun":100}),
])
sense.load_complaints([
    Complaint("Too salty", "YUXI", "taste", ["salty"]),
    Complaint("Slow service", "YUXI", "service", ["slow"]),
    Complaint("Steak overcooked", "BACIO", "quality", ["overcooked"]),
    Complaint("Limited buffet variety", "OPEN", "variety", ["limited"]),
])
sense.load_preferences([
    Preference("G-1", "food", "likes spicy", ["spicy"]),
    Preference("G-2", "food", "seafood lover", ["seafood"]),
    Preference("G-3", "dietary", "vegetarian", ["vegetarian"]),
    Preference("G-4", "food", "likes beef", ["beef"]),
])

ms = MenuSense(sense)

print("=== y-menu-engine Demo ===")
print(f"Data: {sense.stats()}\n")

questions = [
    "pricing",
    "BACIO pricing",
    "cost trends",
    "customer preferences",
    "complaints",
    "menu health",
    "summary",
]
for q in questions:
    print(f">> {q}")
    print(ms.ask(q))
    print()
