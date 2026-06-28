"""
adapters/csv_adapter.py — CSV文件适配器示例
把你的菜单/食材/投诉/偏好数据放在CSV里，直接接入引擎。
"""
import csv
from pathlib import Path
from .base import BaseAdapter, MenuItem, IngredientRecord, ComplaintRecord, PreferenceRecord


class CsvAdapter(BaseAdapter):
    """
    从CSV文件读取数据。

    文件格式预期：
      menu.csv:       name, outlet, selling_price, category
      ingredients.csv: name, current_cost, unit
      complaints.csv:  summary, outlet, category, keywords
      preferences.csv: category, value, keywords

    用法：
        adapter = CsvAdapter(data_dir="my_data/")
        engine = adapter.connect(SenseEngine())
    """

    def __init__(self, data_dir: str):
        self.dir = Path(data_dir)

    def _read_csv(self, filename: str) -> list[dict]:
        path = self.dir / filename
        if not path.exists():
            print(f"  [skip] {path} not found")
            return []
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def load_menu(self) -> list[MenuItem]:
        rows = self._read_csv("menu.csv")
        items = []
        for r in rows:
            try:
                items.append(MenuItem(
                    name=r.get("name", ""),
                    outlet=r.get("outlet", ""),
                    selling_price=float(r.get("selling_price", 0)),
                    category=r.get("category", ""),
                    appearances=int(r.get("appearances", 0)),
                ))
            except (ValueError, KeyError):
                continue
        print(f"  loaded {len(items)} menu items from CSV")
        return items

    def load_ingredients(self) -> list[IngredientRecord]:
        rows = self._read_csv("ingredients.csv")
        items = []
        for r in rows:
            try:
                items.append(IngredientRecord(
                    name=r.get("name", ""),
                    current_cost=float(r.get("current_cost", 0)),
                    unit=r.get("unit", "kg"),
                ))
            except (ValueError, KeyError):
                continue
        print(f"  loaded {len(items)} ingredients from CSV")
        return items

    def load_complaints(self) -> list[ComplaintRecord]:
        rows = self._read_csv("complaints.csv")
        items = []
        for r in rows:
            kw = [k.strip() for k in r.get("keywords", "").split(",") if k.strip()]
            items.append(ComplaintRecord(
                summary=r.get("summary", ""),
                outlet=r.get("outlet", ""),
                category=r.get("category", "general"),
                keywords=kw,
            ))
        print(f"  loaded {len(items)} complaints from CSV")
        return items

    def load_preferences(self) -> list[PreferenceRecord]:
        rows = self._read_csv("preferences.csv")
        items = []
        for r in rows:
            kw = [k.strip() for k in r.get("keywords", "").split(",") if k.strip()]
            items.append(PreferenceRecord(
                category=r.get("category", ""),
                value=r.get("value", ""),
                keywords=kw,
            ))
        print(f"  loaded {len(items)} preferences from CSV")
        return items
