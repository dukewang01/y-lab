"""
市场感知菜单工程 — 数据侦察
快速评估：FIN采购数据 / FB菜品定价 / GSM投诉情绪 / CRM偏好
看四站数据分别能提供什么、缺什么
"""
import json
from pathlib import Path
from collections import Counter, defaultdict

KC = Path(__file__).parent

def load_graph(name):
    path = KC / name
    if not path.exists(): return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("entities", [])

print("=" * 65)
print("  市场感知菜单工程 - 数据侦察")
print("=" * 65)

# ── 1. FIN站：采购数据 ──
print("\n【1】FIN站 - 采购与成本数据")
fin = load_graph("fin_graph.json")
fin_menus = [e for e in (fin or []) if "menu" in (e.get("name","").lower() or "")]
fin_proc = [e for e in (fin or []) if any(k in str(e.get("properties",{})) for k in ["procurement","purchase","采购","成本"])]
print(f"  总实体: {len(fin) if fin else 0}")
print(f"  菜单相关实体: {len(fin_menus)}")
print(f"  采购/成本相关: {len(fin_proc)}")

# 找食材价格数据
all_fin_props = []
for e in (fin or []):
    p = e.get("properties", {})
    for k,v in p.items():
        if any(w in str(k).lower() for w in ["price","cost","单价","价格","金额"]):
            all_fin_props.append((e.get("name","?"), k, v))
print(f"  含价格字段的实体: {len(set(n for n,_,_ in all_fin_props))}")
if len(all_fin_props) >= 3:
    print("  示例:")
    for n,k,v in all_fin_props[:3]:
        print(f"    {n}: {k}={v}")

# ── 2. FB站：菜品定价数据 ──
print("\n【2】FB站 - 菜品与促销数据")
fb = load_graph("fb_graph.json")
if fb:
    fb_menu_items = [e for e in fb if e.get("type") in ("menu_item","set_menu","signature_dish","bazaar_menu_item","dish","product")]
    fb_with_price = []
    for e in fb_menu_items:
        props = e.get("properties",{})
        price = None
        for k in ["price","selling_price","menu_price","unit_price"]:
            if k in props and props.get(k):
                try: price = float(str(props[k]).replace(",",""))
                except: pass
                break
        if price: fb_with_price.append((e.get("name","?"), price))
    
    print(f"  总实体: {len(fb)}")
    print(f"  菜品类实体: {len(fb_menu_items)}")
    print(f"  有定价的菜品: {len(fb_with_price)}")
    if fb_with_price:
        print(f"  价格范围: ¥{min(p for _,p in fb_with_price):.0f} ~ ¥{max(p for _,p in fb_with_price):.0f}")
        print(f"  均价: ¥{sum(p for _,p in fb_with_price)/len(fb_with_price):.0f}")

# ── 3. GSM站：投诉情绪 ──
print("\n【3】GSM站 - 投诉与情绪数据")
gsm = load_graph("gsm_graph.json")
if gsm:
    complaint_types = Counter()
    complaint_ratings = []
    for e in gsm:
        t = e.get("type","")
        if "complaint" in t.lower() or e.get("name","").lower().startswith("cmp"):
            ct = e.get("properties",{}).get("complaint_type","")
            complaint_types[ct] += 1
            rating = e.get("properties",{}).get("sentiment",{}).get("rating") if isinstance(e.get("properties",{}).get("sentiment"), dict) else None
            if rating: complaint_ratings.append(rating)
    print(f"  总实体: {len(gsm)}")
    print(f"  投诉案例: {sum(complaint_types.values())}")
    print(f"  投诉类型分布: {dict(complaint_types.most_common(8))}")

# ── 4. CRM站：客户偏好 ──
print("\n【4】CRM站 - 客户偏好数据")
crm = load_graph("crm_graph.json")
if crm:
    crm_prefs = [e for e in crm if e.get("type","") == "preference"]
    crm_guests = [e for e in crm if e.get("type","") == "guest"]
    print(f"  总实体: {len(crm)}")
    print(f"  客户: {len(crm_guests)}")
    print(f"  偏好: {len(crm_prefs)}")
    
    # 偏好标签分布
    pref_tags = []
    for e in crm_prefs:
        tags = e.get("properties",{}).get("tags","")
        if isinstance(tags, str): pref_tags.extend(t.strip() for t in tags.split(","))
        elif isinstance(tags, list): pref_tags.extend(tags)
    if pref_tags:
        pt = Counter(pref_tags)
        print(f"  偏好标签TOP 10: {dict(pt.most_common(10))}")

# ── 总结 ──
print("\n" + "=" * 65)
print("  📋 数据就绪度评估")
print("=" * 65)
checks = [
    ("FIN采购价格数据", bool(fin and len(fin_proc) > 3), "有"),
    ("FB菜品定价数据", bool(fb and len(fb_with_price) > 5), "有"),
    ("GSM投诉情绪数据", bool(gsm and sum(complaint_types.values()) > 5), "有"),
    ("CRM客户偏好数据", bool(crm and len(crm_prefs) > 5), "有"),
]
for name, ready, label in checks:
    print(f"  {'✅' if ready else '❌'} {name:25s} {'→'+label:>20s}")

print("\n  ✅ 四站数据齐活，可以开干！")
