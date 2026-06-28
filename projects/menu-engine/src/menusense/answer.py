from .sense import SenseEngine
from .analyze import MenuAnalyzer


class MenuSense:
    OUTLETS = {
        "bacio": "BACIO", "open": "OPEN", "yuxi": "YUXI",
        "yuxi": "YUXI", "yuan": "YUAN", "beer": "BEER SOCIETY",
        "italian": "BACIO", "self-service": "OPEN", "chinese": "YUXI",
    }

    def __init__(self, sense: SenseEngine):
        self.sense = sense
        self.analyzer = MenuAnalyzer(sense)

    def ask(self, query: str) -> str:
        q = query.lower().strip()
        outlet = self._detect_outlet(q)

        if self._match(q, ["pricing", "price", "cost", "band", "多少钱", "定价", "价格"]):
            d = self.analyzer.pricing_summary(outlet)
            return self._format_pricing(d)

        if self._match(q, ["health", "matrix", "bcg", "quality", "健康", "矩阵"]):
            d = self.analyzer.menu_health(outlet)
            return self._format_health(d)

        if self._match(q, ["trend", "ingredient", "fluctuation", "波动", "涨", "跌", "食材"]):
            d = self.analyzer.cost_trend()
            return self._format_cost(d)

        if self._match(q, ["preference", "flavor", "taste", "喜好", "偏好", "口味", "风向"]):
            d = self.analyzer.preference_wind()
            return self._format_preference(d)

        if self._match(q, ["complaint", "sentiment", "feedback", "投诉", "情绪", "反馈"]):
            d = self.analyzer.sentiment_summary(outlet)
            return self._format_sentiment(d)

        if self._match(q, ["summary", "report", "all", "综合", "总结", "报告", "总览"]):
            return self._full_report(outlet)

        return (
            "y-menu-engine: ask me about menu pricing, cost trends,\n"
            "preference insights, complaint analysis, or menu health.\n"
            "Examples:\n"
            '  "BACIO pricing"\n'
            '  "cost trends"\n'
            '  "customer preferences"\n'
            '  "menu health"\n'
            '  "summary report"'
        )

    def _detect_outlet(self, q: str) -> str:
        for kw, name in self.OUTLETS.items():
            if kw in q:
                return name
        return ""

    def _match(self, q: str, keywords: list) -> bool:
        return any(kw in q for kw in keywords)

    def _format_pricing(self, d: dict) -> str:
        if "error" in d:
            return "No data: " + d["error"]
        lines = [
            f"Pricing: {d['outlet'] or 'All'} ({d['count']} items)",
            f"  Range: {d['min']:.0f} - {d['max']:.0f}  Avg: {d['avg']:.0f}  Median: {d['median']:.0f}",
            "  Bands:",
        ]
        for b in d.get("bands", []):
            bar = "=" * max(1, round(b["pct"] / 5)) if b["count"] else ""
            lines.append(f"    {b['band']:>8}: {bar} {b['count']} ({b['pct']:.0f}%)")
        return "\n".join(lines)

    def _format_health(self, d: dict) -> str:
        if d.get("total_items", 0) == 0:
            return "No menu health data"
        mx = d["matrix"]
        return (
            f"Menu Health ({d['total_items']} items)\n"
            f"  Stars: {mx.get('stars', 0)}   Cash Cows: {mx.get('cash_cows', 0)}\n"
            f"  Plow Horses: {mx.get('plow_horses', 0)}   Dogs: {mx.get('dogs', 0)}"
        )

    def _format_cost(self, d: dict) -> str:
        if "error" in d:
            return "No data: " + d["error"]
        lines = [f"Cost Trends ({d['ingredients_tracked']} tracked)"]
        for t in d.get("trends", [])[:5]:
            arrow = "+" if t["change_pct"] > 0 else ""
            lines.append(f"  {t['name']}: {t['first']} -> {t['current']} ({arrow}{t['change_pct']}%)")
        return "\n".join(lines)

    def _format_preference(self, d: dict) -> str:
        if "error" in d:
            return "No data: " + d["error"]
        lines = [f"Preferences ({d['total']} records)"]
        flavors = d.get("top_flavors", {})
        items = list(flavors.items())[:6] if isinstance(flavors, dict) else flavors[:6]
        for k, v in items:
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    def _format_sentiment(self, d: dict) -> str:
        if d.get("total", 0) == 0 or d.get("message") == "no complaint data":
            return "No complaint data"
        lines = [f"Complaints ({d['total']})"]
        for k, v in d.get("top_categories", {}).items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    def _full_report(self, outlet: str) -> str:
        parts = []
        p = self.analyzer.pricing_summary(outlet)
        if "error" not in p:
            parts.append(f"Menu: {p['count']} items, avg {p['avg']:.0f}")
        h = self.analyzer.menu_health(outlet)
        mx = h["matrix"]
        parts.append(f"Health: S{mx.get('stars',0)} CC{mx.get('cash_cows',0)} PH{mx.get('plow_horses',0)} D{mx.get('dogs',0)}")
        c = self.analyzer.cost_trend()
        if "error" not in c and c.get("trends"):
            tops = [t for t in c["trends"][:2] if abs(t["change_pct"]) > 5]
            if tops:
                parts.append("Cost: " + ", ".join(f"{t['name']} {t['change_pct']:+.0f}%" for t in tops))
        pr = self.analyzer.preference_wind()
        if "error" not in pr and pr.get("top_flavors"):
            fv = list(pr["top_flavors"].items())[:2]
            parts.append("Taste: " + ", ".join(f"{k}({v})" for k, v in fv))
        return " | ".join(parts)
