#!/usr/bin/env python3
"""FSAA 每日推送报告生成器 - 2026-05-02"""
import json, sys
from datetime import datetime
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fsaa_graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

entities = data.get('entities', [])
rels = data.get('relationships', [])
reltype_field = 'type' if rels and 'type' in rels[0] else ('label' if rels and 'label' in rels[0] else 'unknown')

print("=" * 60)
print("  FSAA 食品安全审计工作站 · 每日推送")
print(f"  日期: 2026-05-02 (星期六)")
print("=" * 60)
print()

# 1. 规模概览
print(f"📊 当前规模: 实体 {len(entities)} | 关系 {len(rels)}")

# 2. 核心领域分布
categories = {
    "检查项与标准": ["fsaa_check_item", "fsaa_standard", "fsaa_requirement", "fsaa_rule"],
    "NC不符合项": [t for t in set(e.get("type") for e in entities) if "nc" in t.lower() or "nc_" in t],
    "HACCP/过敏原/温控": ["fsaa_haccp", "fsaa_allergen", "fsaa_temp_standard", "fsaa_control_point", "fsaa_humidity_standard"],
    "存储/保质期": ["fsaa_storage_standard", "fsaa_shelf_life", "fsaa_storage_zone"],
    "设备/工具": ["fsaa_equipment", "fsaa_cleaning_cloth"],
    "化学品/虫害": ["fsaa_chemical", "fsaa_pco_finding"],
    "流程/操作": ["fsaa_process", "fsaa_operation", "fsaa_monitoring_freq", "fsaa_record"],
    "厨房/区域": ["fsaa_kitchen", "fsaa_area", "fsaa_outlet", "fsaa_floor"],
    "审计体系": ["audit_path", "audit_process", "audit_scope", "audit_role", "audit_region", "audit_rating"],
    "培训/角色": ["fsaa_training", "fsaa_role", "fsaa_ppe"],
    "FAQs": ["faq_entry"],
    "供应商": ["fsaa_supplier"],
    "餐饮菜单": ["fb_menu_item", "fb_signature_dish"],
}

for cat, types in categories.items():
    count = sum(1 for e in entities if e.get("type") in types)
    print(f"  {cat}: {count}")

# 3. 最近更新摘要
print()
print("🔄 最近重大更新:")
print("  • 2026-05-01: FSAA v7.5 — 1165实体/7521关系")
print("    - 检查项SOP全挂接")
print("    - QA标准映射")
print("    - NC-RISK桥接")
print("    - 30条FAQ补充")
print("  • 2026-04-30: FSAA v6.59 → 873实体/1661关系 + 10新实体")
print("  • 2026-04-30: 厨房布局更新(2F啤酒荟/3F面馆/6F+烧腊间+点心房+烤鸭间)")
print("  • 2026-04-29: PCO虫害报告 → 四站联动(FSAA/MEP/QA/RISK/FAQ)")
print("  • 2026-04-29: 21条NC不符合项(2026-04-22审计)入库")

# 4. 关键高风险项提醒
print()
print("⚠️ 重点提醒:")
print("  • 今日是星期六 — 早餐/自助餐高峰，建议重点关注:")

nc_entities = [e for e in entities if e.get("type","").startswith("fsaa_nc")]
nc_categories = Counter(e.get("type") for e in nc_entities)
if nc_categories:
    print("  • 未关闭不符合项分布:")
    for t, c in nc_categories.most_common(10):
        print(f"    - {t.replace('fsaa_nc_','')}: {c}条")

# 5. 厨房布局快速参考
kitchens = [e for e in entities if e.get("type") == "fsaa_kitchen"]
print()
print("🍳 厨房布局:")
for k in kitchens:
    print(f"  • {k.get('name','?')}")

# 6. 今日巡检清单建议
print()
print("✅ 今日FSAA巡检建议 (周六):")
print("  1.【晨检】人员健康检查(发烧/伤口/指甲)")
print("  2.【温度】冷藏<5°C / 冷冻<-18°C / 热存>63°C")
print("  3.【早餐】自助餐热食温度保持 >63°C")
print("  4.【化学】消毒液浓度: 含氯250PPM / 酒精75%")
print("  5.【过敏原】早餐区过敏原标识是否完整")
print("  6.【记录】FS365每日温度记录是否完整")
print("  7.【肥皂】洗手液/消毒凝胶/擦手纸是否充足")

# 7. 跨站联动提醒
print()
print("🔗 跨站提醒:")
print("  • RISK↔QA桥接: 128条 — 投诉案例↔审计缺陷映射")
print("  • NC可关联RISK案例 → 追溯到具体客诉/事件")
print("  • 厨房布局已更新 → 可精准定位各厨房检查路线")

# 8. 查询提示
print()
print("💡 查询命令:")
print("  python knowledge_center/fsaa_report.py          # FSAA完整报告")
print("  python knowledge_center/_fsaa_query.py          # FSAA查询工具")
print("  python knowledge_center/_check_fsaa_full.py     # FSAA完整自检")
print()
print("=" * 60)
print("  知识中心入口: knowledge_center/README.md")
print("  可视化面板:   knowledge_center/dashboard.html")
print("=" * 60)
