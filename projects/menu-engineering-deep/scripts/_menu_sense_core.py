"""
_menu_sense_core.py — 市场感知菜单工程 核心引擎 v0.1
三层结构：
  感知层 → 采购/菜品/投诉/偏好
  分析层 → 成本率/BCG矩阵/趋势/情绪
  回答层 → 自然语言查询
"""
import json, re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict

KC = Path(__file__).parent

class MenuSenseEngine:
    def __init__(self):
        self.fb_graph = self._load("fb_graph.json")
        self.fin_graph = self._load("fin_graph.json")
        self.gsm_graph = self._load("gsm_graph.json")
        self.prefs = self._load("fb_crm/preferences.json")
        self.guests = self._load("fb_crm/guests.json")
        # FB站内的bazaar图谱（促销数据）
        self.bazaar = self._load("fb_crm/518_promo_graph.json")
        # CRM分段数据
        self.rfm = self._load("fb_crm/crm_rfm_segments.json")
        
        # 索引
        self._build_index()
    
    def _load(self, rel_path):
        full = KC / rel_path
        if not full.exists():
            return {}
        try:
            with open(full, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    
    def _build_index(self):
        """构建快速查询索引"""
        # FB菜品索引
        self.fb_items = {}
        for e in (self.fb_graph.get("entities", []) if isinstance(self.fb_graph, dict) else []):
            p = e.get("properties", {})
            price = p.get("price", "")
            if price:
                try:
                    price_val = float(str(price).replace(",","").replace("/位","").replace("¥",""))
                except:
                    price_val = 0
                outlet = p.get("outlet","") or p.get("restaurant","") or "未知"
                self.fb_items[e.get("name","?").strip()] = {
                    "type": e.get("type",""),
                    "price": price_val,
                    "outlet": outlet,
                    "properties": p
                }
        # 用拼音/简写映射
        if "BACIO意大利餐厅" in self.fb_items and "BACIO" not in self.fb_items:
            self.fb_items["BACIO"] = self.fb_items["BACIO意大利餐厅"]
        if "御玺中餐厅" in self.fb_items and "YUXI" not in self.fb_items:
            self.fb_items["YUXI"] = self.fb_items["御玺中餐厅"]
        if "OPEN全日餐厅" in self.fb_items and "OPEN" not in self.fb_items:
            self.fb_items["OPEN"] = self.fb_items["OPEN全日餐厅"]
        
        # 采购成本索引
        self.fin_budgets = {}
        for e in (self.fin_graph.get("entities", []) if isinstance(self.fin_graph, dict) else []):
            if e.get("type") == "budget":
                name = e.get("name","")
                p = e.get("properties", {})
                month = name.replace("月预算","").replace("预算","").strip()
                self.fin_budgets[month] = {
                    "food_cost_pct": p.get("budget_food_cost_pct", 0),
                    "beverage_cost_pct": p.get("budget_beverage_cost_pct", 0),
                    "total_fb_cost": p.get("budget_fb_cost", 0)
                }
        
        # GSM投诉索引 — 实际结构是risk_case/gsm_case
        self.complaints = []
        for e in (self.gsm_graph.get("entities", []) if isinstance(self.gsm_graph, dict) else []):
            etype = e.get("type","")
            name = e.get("name","")
            p = e.get("properties", {})
            # 兼容risk_case和gsm_case格式
            category = p.get("category", p.get("complaint_type", p.get("case_type","")))
            summary = str(p.get("summary", p.get("description", p.get("details",""))))
            outlet = p.get("outlet", p.get("location", p.get("department","")))
            # 只保留有具体内容的
            if etype in ("risk_case", "gsm_case", "complaint_case", "complaint") or "cmp" in name.lower():
                if category or summary:
                    self.complaints.append({
                        "name": name,
                        "type": category,
                        "outlet": str(outlet) if outlet else "",
                        "summary": summary[:200],
                        "date": p.get("date", p.get("occurred",""))
                    })
        
        # CRM偏好索引 — 实际是list格式，每个有category/value
        self.pref_tags = Counter()
        self.pref_guests = set()
        if isinstance(self.prefs, list):
            for pref in self.prefs:
                val = str(pref.get("value",""))
                cat = pref.get("category","")
                gid = pref.get("guest_id","")
                if gid:
                    self.pref_guests.add(gid)
                # 统计category
                self.pref_tags[cat] += 1
                # 从value里提取关键词
                for kw in ["辣","酸","甜","咸","海鲜","牛肉","猪肉","鸡肉","素食","清淡","沙拉","烧烤","火锅","刺身","日料","中餐","西餐","意面","麻辣","清淡"]:
                    if kw in val:
                        self.pref_tags[kw] += 1
        if isinstance(self.prefs, dict):
            for pid, pref in self.prefs.items():
                tags = pref.get("tags", pref.get("properties",{}).get("tags",""))
                if isinstance(tags, str):
                    for t in tags.split(","):
                        self.pref_tags[t.strip()] += 1
        if isinstance(self.guests, dict):
            for gid, g in self.guests.items():
                self.pref_guests.add(gid)
    
    def _find_prices_by_outlet(self, outlet):
        """按餐厅找定价"""
        results = {}
        for name, item in self.fb_items.items():
            if outlet.lower() in item["outlet"].lower() or item["outlet"].lower() in outlet.lower():
                if item["price"] > 0:
                    results[name] = item
        return results
    
    def _estimate_cost_pct(self, price):
        """根据价格估算成本率（没有精确食材成本时的启发式）"""
        if not price or price <= 0:
            return None
        # 经验法则：高价菜成本率低，低价菜成本率高
        if price >= 300: return 0.28
        elif price >= 200: return 0.30
        elif price >= 100: return 0.33
        elif price >= 50: return 0.35
        else: return 0.38
    
    def report_outlet_pricing(self, outlet):
        """餐厅定价报告"""
        items = self._find_prices_by_outlet(outlet)
        if not items:
            dm = {"bacio": "BACIO", "open": "OPEN", "yuxi": "YUXI", "yuan": "YUAN", "beer": "BEER SOCIETY", "御玺": "YUXI"}
            key = outlet.lower().strip()
            if key in dm:
                items = self._find_prices_by_outlet(dm[key])
        if not items:
            return f"未找到{outlet}的定价数据"
        
        prices = [v["price"] for v in items.values()]
        avg = sum(prices)/len(prices)
        lines = [f"📊 {outlet} 菜品定价概览（{len(items)}道菜）",
                 f"  └ 价格区间: ¥{min(prices):.0f} ~ ¥{max(prices):.0f}",
                 f"  └ 均价: ¥{avg:.0f}",
                 f"  └ 中位数: ¥{sorted(prices)[len(prices)//2]:.0f}"]
        
        # 按价格带分组
        bands = {"¥0-50": 0, "¥51-100": 0, "¥101-200": 0, "¥201-500": 0, "¥500+": 0}
        for p in prices:
            if p <= 50: bands["¥0-50"] += 1
            elif p <= 100: bands["¥51-100"] += 1
            elif p <= 200: bands["¥101-200"] += 1
            elif p <= 500: bands["¥201-500"] += 1
            else: bands["¥500+"] += 1
        lines.append(f"\n  💰 价格带分布:")
        for band, count in bands.items():
            if count > 0:
                pct = count/len(prices)*100
                bar = "█" * round(pct/5) + "░" * (20 - round(pct/5))
                lines.append(f"    {band:>12}: {bar} {count}道 ({pct:.0f}%)")
        
        return "\n".join(lines)
    
    def report_menu_health(self, outlet):
        """菜单健康度——成本率视角"""
        items = self._find_prices_by_outlet(outlet)
        if not items:
            dm = {"bacio":"BACIO","open":"OPEN","yuxi":"YUXI","yuan":"YUAN","御玺":"YUXI"}
            if outlet.lower().strip() in dm:
                items = self._find_prices_by_outlet(dm[outlet.lower().strip()])
        if not items:
            return f"未找到{outlet}的菜单健康数据"
        
        # 按价格跟预估成本率做矩阵
        matrix = {"Star(高利润率高销量)":[], "Cash Cow(稳定利基)":[],
                  "Plow Horse(跑量)":[], "Dog(需关注)":[]}
        # 简化：用价格作为销量代理（假设中档菜是跑量菜）
        for name, item in items.items():
            p = item["price"]
            cost_rate = self._estimate_cost_pct(p)
            profit_rate = 1 - cost_rate
            # 用价格中位数分高低
            if p >= 200:
                if profit_rate >= 0.7:
                    matrix["Star(高利润率高销量)"].append((name, p, cost_rate))
                else:
                    matrix["Cash Cow(稳定利基)"].append((name, p, cost_rate))
            else:
                if profit_rate >= 0.65:
                    matrix["Plow Horse(跑量)"].append((name, p, cost_rate))
                else:
                    matrix["Dog(需关注)"].append((name, p, cost_rate))
        
        lines = [f"🏥 {outlet} 菜单健康度矩阵",
                 f"  📊 基于{len(items)}道菜品的估算"]
        for cat, items_in_cat in matrix.items():
            if items_in_cat:
                lines.append(f"\n  ✅ {cat}")
                for name, p, cr in items_in_cat[:5]:
                    lines.append(f"    · {name[:20]:20s} ¥{p:<6} 预估成本率{cr*100:.0f}%")
                if len(items_in_cat) > 5:
                    lines.append(f"    · ...还有{len(items_in_cat)-5}道")
        
        return "\n".join(lines)
    
    def report_complaint_trend(self, outlet=None, recent="3m"):
        """投诉情绪——菜品相关投诉分析"""
        # GSM中risk_case可能没有结构化的菜品标签，改用全文搜索
        food_complaints = [c for c in self.complaints if any(kw in str(c.get("summary","")).lower() or str(c.get("type","")).lower() 
            for kw in ["菜","餐","食","菜单","food","dish","menu","口味","品质","food","餐厅","就餐","dining","restaurant"])]
        if not food_complaints:
            # 回退：全部投诉都算
            food_complaints = self.complaints
        
        lines = [f"📋 菜品相关投诉分析"]
        if outlet:
            filtered = [c for c in food_complaints if outlet.lower() in c.get("outlet","").lower()]
            lines.append(f"  🔍 过滤: {outlet}")
            lines.append(f"  📝 {len(filtered)}条相关投诉")
            if filtered:
                # 按关键词聚类
                keywords = Counter()
                for c in filtered:
                    s = str(c.get("summary",""))
                    for kw in ["慢","贵","不新鲜","卫生","咸","淡","凉","少","错"]:
                        if kw in s:
                            keywords[kw] += 1
                if keywords:
                    lines.append(f"  🔥 高频问题关键词:")
                    for kw, cnt in keywords.most_common(5):
                        bar = "█" * cnt
                        lines.append(f"    · {kw}: {bar} ({cnt}次)")
        else:
            lines.append(f"  📝 共{len(food_complaints)}条")
        return "\n".join(lines)
    
    def report_preference_tide(self):
        """偏好风向——CRM偏好标签潮汐"""
        if not self.pref_tags:
            return "暂无CRM偏好数据"
        
        lines = [f"🔥 客户偏好风向标（基于{len(self.pref_tags)}个偏好标签）"]
        
        # 按内容分类
        taste_tags = {k:v for k,v in self.pref_tags.items() 
                      if any(w in k for w in ["辣","酸","甜","咸","清淡","麻辣","海鲜","肉类","素食","烧烤"])}
        if taste_tags:
            lines.append(f"\n  👅 口味偏好TOP:")
            for tag, cnt in sorted(taste_tags.items(), key=lambda x:-x[1])[:8]:
                pct = cnt/len(self.pref_guests)*100 if self.pref_guests else 0
                lines.append(f"    · {tag}: {cnt}人 ({pct:.0f}%)")
        
        # 找出偏好最多的品类
        # 尝试从guests里解析
        cuisine_tags = {k:v for k,v in self.pref_tags.items()
                        if any(w in k for w in ["中餐","西餐","日料","意大利","烧烤"])}
        if cuisine_tags:
            lines.append(f"\n  🍽️ 菜系偏好:")
            for tag, cnt in sorted(cuisine_tags.items(), key=lambda x:-x[1])[:5]:
                lines.append(f"    · {tag}: {cnt}人")
        
        return "\n".join(lines)
    
    def report_cost_trend(self):
        """食材成本趋势"""
        if not self.fin_budgets:
            return "暂无月度成本数据"
        
        lines = [f"📈 月度食材成本率趋势"]
        for month in ["1","2","3","4","5","6"]:
            if month in self.fin_budgets:
                b = self.fin_budgets[month]
                food_pct = b.get("food_cost_pct",0)
                bev_pct = b.get("beverage_cost_pct",0)
                total = b.get("total_fb_cost",0)
                bar_len = round(food_pct * 50) if food_pct else 0
                bar = "█" * bar_len + "░" * (50 - bar_len)
                lines.append(f"  {month}月: {bar} 食物成本率{food_pct*100:5.1f}% | 饮品{bev_pct*100:5.1f}% | F&B总成本¥{total:,.0f}")
        
        # 波动分析
        food_pcts = [v.get("food_cost_pct",0) for v in self.fin_budgets.values() if v.get("food_cost_pct",0) > 0]
        if len(food_pcts) >= 2:
            min_pct, max_pct = min(food_pcts), max(food_pcts)
            if max_pct - min_pct > 0.05:
                lines.append(f"\n  ⚠️ 波动预警：食物成本率波动{max_pct*100-min_pct*100:.1f}个百分点")
        
        return "\n".join(lines)
    
    def answer(self, query):
        """自然语言查询入口"""
        q = query.lower().strip()
        
        # 匹配意图
        intents = []
        
        # 餐厅定价
        outlets_keywords = {"bacio":"BACIO","open":"OPEN","yuxi":"YUXI","yuan":"YUAN","御玺":"YUXI","beer":"BEER SOCIETY","italia":"BACIO"}
        matched_outlet = None
        for kw, name in outlets_keywords.items():
            if kw in q:
                matched_outlet = name
                break
        
        if any(w in q for w in ["定价","价格","多少钱","how much","价格带","价"]):
            if matched_outlet:
                return self.report_outlet_pricing(matched_outlet)
            else:
                return self.report_outlet_pricing("BACIO")
        
        # 菜单健康度
        if any(w in q for w in ["健康","矩阵","菜单质量","bcg","成本率","利润"]):
            if matched_outlet:
                return self.report_menu_health(matched_outlet)
            return self.report_menu_health("OPEN")
        
        # 投诉/情绪
        if any(w in q for w in ["投诉","情绪","抱怨","品质","feedback"]):
            return self.report_complaint_trend(matched_outlet)
        
        # 成本趋势（优先于偏好中的"趋势"关键词）
        if any(w in q for w in ["成本","采购","波动","涨","跌","trend","cost","食材"]):
            return self.report_cost_trend()
        
        # 偏好风向
        if any(w in q for w in ["偏好","口味","风向","喜欢","趋势"]):
            return self.report_preference_tide()
        
        # 综合报告
        if any(w in q for w in ["总结","综合","报告","全部","总览"]):
            parts = []
            if matched_outlet:
                parts.append(self.report_outlet_pricing(matched_outlet))
            else:
                parts.append(self.report_cost_trend())
                parts.append(self.report_outlet_pricing("OPEN"))
            parts.append(self.report_preference_tide())
            parts.append(self.report_complaint_trend(matched_outlet))
            return "\n\n".join(parts)
        
        # 免费回复
        if any(w in q for w in ["hi","你好","hello","嗨","早"]):
            return "你好！我是菜单工程助手。可以问我：\n· BACIO的定价情况\n· 食材成本趋势\n· 客户偏好风向\n· 投诉分析\n· 菜单健康度矩阵"
        
        return f"暂时无法回答「{query}」。可以试试：定价、成本趋势、偏好风向、投诉分析、菜单健康度"


if __name__ == "__main__":
    me = MenuSenseEngine()
    print(me.answer("hi"))
