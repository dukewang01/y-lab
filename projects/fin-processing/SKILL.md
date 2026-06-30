# FIN Processing (财务数据处理)

酒店财务数据处理工具箱。包含GCM分析、成本监控、数据标签化、费用导入。

## 脚本清单 (10个)

| 脚本 | 功能 |
|:-----|:-----|
| `_analyze_gcm_ytd.py` | GCM（集团管理费）YTD分析 |
| `_import_gcm_ytd.py` | GCM YTD数据导入 |
| `_import_fin_cost_apr.py` | 导入4月成本数据 |
| `_import_fixed_asset.py` | 固定资产导入 |
| `_label_fin.py` | FIN数据自动打标签 |
| `_fin_daily_check.py` | 财务日数据校验 |
| `_fin_detail.py` | 财务明细查询 |
| `_extract_outlet_data.py` | 各店数据提取 |
| `_update_fin_0506.py` | 5/6日财务更新 |
| `_update_final_revenue.py` | 最终营收修正 |
| `_normalize_labels.py` | 标签规范化 |

## FIN架构

FIN站（财务营收站）含四大模块:
1. 营业点营收（各店收入/成本/利润）
2. 成本监控（食品成本/人工/能源）
3. 管理费GCM
4. 库存效率
5. 促销管理

## 数据来源

- DRR日报
- HF（History & Forecast）月报
- GCM对账单
- 业主会议报告
