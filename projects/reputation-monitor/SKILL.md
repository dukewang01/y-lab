# Reputation Monitor (口碑监控)

酒店在线声誉监控系统。覆盖OTA评论(携程/美团)、社交媒体(小红书/抖音)、新闻舆情。

## 脚本清单 (11个)

| 脚本 | 功能 |
|:-----|:-----|
| `_get_storage_quotes.py` | 获取数据仓库引用/数据 |
| `_get_quotes.py` | 通用数据获取 |
| `_extract_tencent_ai_report.py` | 腾讯AI行业报告提取 |
| `_find_storage_pdf.py` | 查找数据仓库PDF |
| `_list_pdfs.py` | PDF文件列表扫描 |
| `_ima_search.py` | IMA知识库搜索 |
| `_ima_search2.py` | IMA搜索v2 |
| `_ima_search_kb.py` | IMA知识库搜索(深度) |
| `_ima_addable.py` | IMA可添加内容检查 |
| `_ima_explore.py` | IMA内容浏览探索 |
| `_ima_raw.py` | IMA原始数据访问 |

## IMA知识库接口

IMA是Y的内部知识库/记忆系统，支持：
- **搜索**: 语义搜索已有知识
- **添加**: 将新发现加入知识库
- **探索**: 浏览关联知识

## 待开发模块

### OTA评论分析
- 携程/美团评分趋势
- 关键词提取 + 情绪分析
- 差评自动分类(清洁/态度/设施)
- 好评亮点汇总

### 社交媒体
- 小红书/抖音提及监控
- 热门推文/打卡点分析
- KOL/KOC效果追踪

### 舆情预警
- 负面事件自动检测
- 危机公关建议

## 数据来源

- IMA知识库 (现有爬取数据)
- 小红书API/爬虫 (待接入)
- 携程/美团API (待接入)
