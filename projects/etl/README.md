# ETL (数据管线)

> **提取 · 转换 · 加载** — 酒店数据的自来水系统。

酒店的每一个系统都在生产数据：PMS(预订)、POS(餐饮)、OnQ(财务)、LASATA(DRR)。
ETL 把它们统一起来，让九站知识图谱一直鲜活。

## 通用管线设计

```
数据源 (Excel/PDF/API) 
    │
    ▼
提取器 (Reader / Parser)
    │
    ▼
转换器 (Transformer)
    ├── 字段映射
    ├── 类型转换
    ├── 异常值处理
    └── 去重/合并
    │
    ▼
加载器 (Loader)
    ├── → JSON图谱文件
    ├── → 数据库
    └── → 仪表盘
```

## 待开发

- Excel解析器通用基类（已有 `excel-attachment-parser`）
- PDF解析器（已有 `_parse_hf_pdf.py`）
- API适配器（PMS/OTA接口）
- 增量同步 vs 全量同步
- 数据质量校验

## 关联项目

`excel-attachment-parser` · `inbox-router` · `hf-importer` · `kc-healthcheck`
