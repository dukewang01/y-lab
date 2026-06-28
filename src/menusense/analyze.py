from collections import Counter
from .sense import MenuItem


class MenuAnalyzer:
    def __init__(self, sense):
        self.sense = sense

    def pricing_summary(self, outlet: str = "") -> dict:
        items = self.sense.menu_items
        if outlet:
            items = [i for i in items if outlet.lower() in i.outlet.lower()]
        prices = [i.selling_price for i in items if i.selling_price > 0]
        if not prices:
            return {"error": "no pricing data"}
        return {
            "outlet": outlet or "all",
            "count": len(prices),
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices),
            "median": sorted(prices)[len(prices) // 2],
            "bands": self._price_bands(prices),
        }

    def _price_bands(self, prices):
        result = []
        thresholds = [("0-50", 50), ("51-100", 100), ("101-200", 200),
                       ("201-500", 500), ("500+", float("inf"))]
        remaining = prices[:]
        for label, t in thresholds:
            count = sum(1 for p in remaining if p <= t)
            if label == "500+":
                count = sum(1 for p in remaining if p > 500)
            result.append({
                "band": label, "count": count,
                "pct": round(count / len(prices) * 100, 1)
            })
            remaining = [p for p in remaining if p > t]
        return result

    def menu_health(self, outlet: str = "") -> dict:
        items = self.sense.menu_items
        if outlet:
            items = [i for i in items if outlet.lower() in i.outlet.lower()]
        matrix = {"stars": 0, "cash_cows": 0, "plow_horses": 0, "dogs": 0}
        for item in items:
            p = item.selling_price
            cr = self._estimate_cost_rate(p)
            if p >= 200 and cr <= 0.30:
                matrix["stars"] += 1
            elif p >= 200:
                matrix["cash_cows"] += 1
            elif p < 200 and cr <= 0.33:
                matrix["plow_horses"] += 1
            else:
                matrix["dogs"] += 1
        return {"outlet": outlet or "all", "total_items": len(items), "matrix": matrix}

    def _estimate_cost_rate(self, price: float) -> float:
        if price >= 300: return 0.28
        elif price >= 200: return 0.30
        elif price >= 100: return 0.33
        elif price >= 50: return 0.35
        return 0.38

    def cost_trend(self) -> dict:
        ingredients = self.sense.ingredients
        if not ingredients:
            return {"error": "no cost data"}
        trends = []
        for ing in ingredients:
            if ing.cost_history:
                months = sorted(ing.cost_history.keys())
                prices = [ing.cost_history[m] for m in months]
                if len(prices) >= 2:
                    change = (prices[-1] - prices[0]) / prices[0]
                    trends.append({
                        "name": ing.name, "current": prices[-1],
                        "first": prices[0],
                        "change_pct": round(change * 100, 1),
                    })
        trends.sort(key=lambda t: -abs(t["change_pct"]))
        return {"ingredients_tracked": len(ingredients), "trends": trends[:10]}

    def sentiment_summary(self, outlet: str = "") -> dict:
        complaints = self.sense.complaints
        if outlet:
            complaints = [c for c in complaints if outlet.lower() in c.outlet.lower()]
        if not complaints:
            return {"total": 0, "message": "no complaint data"}
        categories = Counter()
        keywords = Counter()
        for c in complaints:
            categories[c.category] += 1
            for kw in c.keywords:
                keywords[kw] += 1
        return {
            "total": len(complaints),
            "top_categories": dict(categories.most_common(5)),
            "top_keywords": dict(keywords.most_common(10)),
        }

    def preference_wind(self) -> dict:
        prefs = self.sense.preferences
        if not prefs:
            return {"error": "no preference data"}
        categories = Counter()
        keywords = Counter()
        for p in prefs:
            categories[p.category] += 1
            for kw in p.keywords:
                keywords[kw] += 1
        return {
            "total": len(prefs),
            "categories": dict(categories.most_common(8)),
            "top_flavors": dict(keywords.most_common(10)),
        }
