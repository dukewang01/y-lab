"""
adapters/base.py — 适配器基类
用户仿照这个模板，把自己的数据接进来。
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MenuItem:
    """一道菜的标准化表示"""
    name: str
    outlet: str           # 所属餐厅/售卖点
    selling_price: float  # 售价
    category: str = ""    # 前菜/主菜/甜品/饮品
    cost_price: Optional[float] = None  # 食材成本（如果有）
    appearances: int = 0   # 售卖次数（如果有）


@dataclass
class IngredientRecord:
    """一种食材的标准化表示"""
    name: str
    current_cost: float
    unit: str = "kg"
    monthly_costs: dict = field(default_factory=dict)  # {"2026-01": 120, "2026-02": 128}


@dataclass
class ComplaintRecord:
    """一条投诉"""
    summary: str
    outlet: str = ""
    category: str = "general"
    keywords: list = field(default_factory=list)


@dataclass
class PreferenceRecord:
    """一条客户偏好"""
    category: str = ""
    value: str = ""
    keywords: list = field(default_factory=list)


class BaseAdapter:
    """你只需要实现下面四个方法，就能跑y-menu-engine了"""

    def load_menu(self) -> list[MenuItem]:
        raise NotImplementedError

    def load_ingredients(self) -> list[IngredientRecord]:
        raise NotImplementedError

    def load_complaints(self) -> list[ComplaintRecord]:
        raise NotImplementedError

    def load_preferences(self) -> list[PreferenceRecord]:
        raise NotImplementedError

    def connect(self, engine):
        """把数据灌入引擎"""
        engine.load_menu(self.load_menu())
        engine.load_ingredients(self.load_ingredients())
        engine.load_complaints(self.load_complaints())
        engine.load_preferences(self.load_preferences())
        return engine
