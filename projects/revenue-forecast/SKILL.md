# Revenue Forecast (营收预测引擎)

酒店营收预测与分析系统。基于History & Forecast (HF) 数据和 DRR 日报，自动生成全月/季度/年度营收预测。

## 脚本清单 (11个)

| 脚本 | 功能 |
|:-----|:-----|
| `_may_forecast.py` | 5月全月预测生成 |
| `_import_hf_forecast.py` | HF预测数据导入FIN图谱 |
| `_revenue_analysis.py` | 营收深度分析 |
| `_import_hf_514.py` | 导入5/14 HF数据 |
| `_import_hf_may.py` | 导入5月HF数据 |
| `_import_hf_may_full.py` | 导入5月全量HF |
| `_import_hf_may_fix.py` | 5月HF数据修正 |
| `_parse_hf.py` | HF报告通用解析器 (OnQ格式) |
| `_parse_hf_pdf.py` | HF PDF版解析器 |
| `_import_hf_0610.py` | 导入6/10 HF数据 |
| `_import_hf_0618.py` | 导入6/18 HF数据 |

## HF数据结构

| 字段 | 来源 | 频次 |
|:-----|:----|:----:|
| 客房收入(实际) | DRR日报 | 日 |
| 客房收入(预测) | HF月报 | 月 |
| F&B收入(实际/预测) | HF月报 | 月 |
| GOP(实际/预测) | HF月报 | 月 |
| 出租率和ADR | HF月报 | 月 |

## 预测流程

1. 解析HF报告 → 提取全年预算 + 月度预测
2. 对比DRR日报实际 → 计算偏差
3. 基于MTD实际 + 月底预测 → 生成全月展望
4. 滚动更新YTD趋势 → 年度可完成度评估

## 输出

```
6月预测: 客房 ¥655万 (预算¥764万, 完成率86%)
        F&B ¥229万 (预算¥275万, 完成率83%)
YTD缺口: 客房 ¥271万 | F&B ¥81万
下半年需追: ¥352万/月才能达标
```
