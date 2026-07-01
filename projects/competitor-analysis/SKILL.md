# Competitor Analysis (竞品分析)

酒店竞品分析系统。基于GCM（集团管理费）数据和公开信息，对比区域市场区域竞品表现。

## 脚本清单 (6个)

| 脚本 | 功能 |
|:-----|:-----|
| `_analyze_gcm_peers.py` | 竞品对比分析 (区域市场五店) |
| `_analyze_gcm_scenarios.py` | 场景模拟分析 |
| `_analyze_gcm_ytd.py` | GCM YTD趋势分析 |
| `_analyze_gcm_deep3.py` | GCM深度分析v3 (12KB，最全面) |
| `_import_gcm_ytd.py` | GCM YTD数据导入FIN图谱 |
| `_inspect_gcm.py` | GCM数据审视 |

## 竞品范围

区域市场区域六家酒店（自店 + 5家竞品），竞品以代号表示：

| 代号 | 说明 |
|:----:|:-----|
| Hotel-A | 自店（[HOTEL]） |
| Hotel-B | 竞品① |
| Hotel-C | 竞品② |
| Hotel-D | 竞品③ |
| Hotel-E | 竞品④ |
| Hotel-F | 竞品⑤ |

## 分析维度

- Occ/ADR/RevPAR对标
- 客房收入 vs F&B收入结构
- 季节性对比
- 重大活动/节假日影响

## 数据来源

竞品经营数据来自行业公开报告及业主会议资料。
