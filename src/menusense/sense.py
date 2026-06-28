from dataclasses import dataclass, field


@dataclass
class MenuItem:
    name: str
    outlet: str
    selling_price: float
    category: str = ""
    platform: str = "dine-in"
    ingredient_list: list = field(default_factory=list)
    appearances: int = 0


@dataclass
class Ingredient:
    name: str
    current_cost: float
    unit: str = "kg"
    cost_history: dict = field(default_factory=dict)


@dataclass
class Complaint:
    summary: str
    outlet: str
    category: str = "general"
    keywords: list = field(default_factory=list)


@dataclass
class Preference:
    guest_id: str = ""
    category: str = ""
    value: str = ""
    keywords: list = field(default_factory=list)


class SenseEngine:
    def __init__(self):
        self.menu_items: list[MenuItem] = []
        self.ingredients: list[Ingredient] = []
        self.complaints: list[Complaint] = []
        self.preferences: list[Preference] = []

    def load_menu(self, items: list[MenuItem]):
        self.menu_items = items
        return self

    def load_ingredients(self, ingredients: list[Ingredient]):
        self.ingredients = ingredients
        return self

    def load_complaints(self, complaints: list[Complaint]):
        self.complaints = complaints
        return self

    def load_preferences(self, preferences: list[Preference]):
        self.preferences = preferences
        return self

    def stats(self) -> dict:
        return {
            "menu_items": len(self.menu_items),
            "ingredients": len(self.ingredients),
            "complaints": len(self.complaints),
            "preferences": len(self.preferences),
            "outlets": list({m.outlet for m in self.menu_items}),
        }
