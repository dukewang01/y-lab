# y-etl — 酒店数据导入工具

把Excel/SQL/飞书多维表的数据一键导入y-lab知识图谱。

## 解决的痛点

> 飞书上有几十张表格，数据格式不统一，每次手工搬运费时又容易出错。

## 支持的输入源

| 源 | 状态 |
|----|------|
| CSV | ✅ 已支持 |
| Excel (.xlsx) | ✅ 已支持 |
| 飞书多维表 | 📋 规划中 |
| SQL (MySQL/PostgreSQL) | 📋 规划中 |

## 用法

```python
from etl import CsvImporter, ExcelImporter

# 从CSV导入菜单
importer = CsvImporter()
items = importer.import_menu("menu.csv")
```
