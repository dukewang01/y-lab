# F&B Revenue Analysis

酒店餐饮营收分析工具箱。包含各店营收、促销效果、外卖分析、盈亏分析等功能。

## 脚本清单 (14个)

| 脚本 | 功能 |
|:-----|:-----|
| `_calc_fb_breakeven.py` | F&B盈亏平衡计算 |
| `_calc_open_takeout.py` | OPEN自助外卖分析 |
| `_check_bazaar.py` | 市集数据检查 |
| `_check_fb.py` | F&B数据完整性检查 |
| `_fb_align_7_2.py` | FB站7+2营业点对齐 |
| `_fb_align_7_2_v2.py` | 7+2对齐v2（修正版） |
| `_fb_align_final.py` | 7+2对齐最终版 |
| `_fb_connect_products.py` | 产品关联到营业点 |
| `_fb_connect_products_exec.py` | 执行产品关联 |
| `_fb_finish_7_2.py` | 完成7+2营业点搭建 |
| `_fb_import_takeout_bazaar.py` | 导入外卖/市集数据 |
| `_fb_link_faq.py` | FB站链接FAQ知识库 |
| `_fb_link_tags.py` | FB站标签关联 |
| `_scan_outlets.py` | 扫描各店营业数据 |

## 营业点结构

酒店F&B共**9个营业点**（7就餐+2零售）：

**堂食7店**：OPEN(自助) / YUXI(中餐) / BACIO(意餐) / BEER(啤酒荟) / YUAN(下午茶) / 宴会 / 送餐

**零售2类**：美食屋(Food Store) / 市集(Bazaar)

## 数据分析维度

1. 各店营收排名与Budget完成率
2. 促销活动效果评估（2017-2021五年促销日历）
3. 外卖 vs 堂食占比
4. 人均消费（Average Check）各店对比
5. 盈亏平衡分析
6. 菜品推荐链路（FB图谱→CRM标签）

## 数据来源

- DRR日报（Actual sheet → F&B outlets rows 58-68, 70-80, 93-95）
- FB知识图谱（product/outlet/promotion entities）
- CRM偏好标签（客户→菜品推荐）
