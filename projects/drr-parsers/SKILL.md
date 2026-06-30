# DRR Parsers (日报解析器集合)

每日营收报告(DRR)的各类解析器集合。支持Excel/PDF格式、单日/多日/批量解析。

## 脚本清单 (16个)

| 脚本 | 功能 |
|:-----|:-----|
| `_daily_revenue_parser.py` | 通用日报解析器 |
| `_drr_monthly_parser.py` | 月度汇总解析器 |
| `_drr_today_analysis.py` | 当日分析简报 |
| `_analyze_drr_0524.py` | 5/24日分析 |
| `_import_drr_0519.py` | 导入5/19日报 |
| `_import_drr_0523.py` | 导入5/23日报 |
| `_import_drr_0524_excel.py` | 导入5/24 Excel版 |
| `_import_drr_0525.py` | 导入5/25日报 |
| `_import_drr_0603.py` | 导入6/3日报 |
| `_import_drr_0610.py` | 导入6/10日报 |
| `_import_drr_0617.py` | 导入6/17日报 |
| `_import_drr_pdf_0524.py` | 解析5/24 PDF版 |
| `_import_drr_weekend_batch.py` | 周末批量导入 |
| `_extract_daily.py` | 逐日数据提取 |
| `_extract_daily2.py` | 逐日提取v2 |
| `_extract_daily3.py` | 逐日提取v3（全量） |

## 解析逻辑

统一使用 **Actual sheet** 列映射（详见 `drr-analyze` / `drr-auto-pipeline`）:
- E(5) = 当日实际, F(6) = Budget, G(7) = LY
- H(8) = MTD, I(9) = MTD Budget, J(10) = MTD LY
- O(15) = YTD

## 输出

解析结果 → `knowledge_center/fin/DRR_{YYYY_MM_DD}.json`
