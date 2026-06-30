# HOE Management (酒店经营物资管理)

酒店经营物资（HOE - Hotel Operating Equipment）合同/供应商管理系统。包含品类管理、供应商评估、库存盘点、成本监控。

## 脚本清单 (18个)

| 脚本 | 功能 |
|:-----|:-----|
| `_create_hoe_module.py` | 初始化HOE模块（品类+合同类型+供应商状态） |
| `_hoe_cats.py` | HOE品类管理/分类 |
| `_hoe_final_run.py` | HOE最终执行/批量导入 |
| `_hoe_full_report.py` | 全量HOE报告生成 |
| `_import_drive_hoe.py` | 从飞书云盘导入HOE合同 |
| `_import_hoe21.py` | 导入第21批物资 |
| `_import_hoe33.py` | 导入第33批物资 |
| `_import_hoe33_fix.py` | 第33批数据修复 |
| `_import_hoe35.py` | 导入第35批物资 |
| `_import_hoe35_v2.py` | 第35批导入v2 |
| `_import_hoe43.py` | 导入第43批物资 |
| `_import_hoe51.py` | 导入第51批物资 |
| `_import_hoe51_fix.py` | 第51批数据修复 |
| `_import_hoe_glass.py` | 导入玻璃器皿合同 |
| `_parse_hoe_glass.py` | 解析玻璃器皿合同 |
| `_peek_hoe33_full.py` | 查看第33批完整数据 |
| `_peek_hoe43.py` | 查看第43批数据 |
| `_scan_drive_hoe.py` | 扫描飞书云盘HOE文件 |

## 品类结构

| 品类ID | 品类名 | 说明 |
|:------:|:-------|:-----|
| HOE01 | 家具/固定装置 | 桌椅/柜子/装饰 |
| HOE02 | 地毯/地板 | 走廊/客房/餐厅 |
| HOE03 | 窗帘/软装 | 窗饰/布艺 |
| HOE04 | 瓷器/玻璃/银器 | 餐具/玻璃杯/银具 |
| HOE05 | 厨房设备 | 灶台/冷柜/烤箱 |
| HOE06 | 布草/制服 | 床单/毛巾/员工服 |
| HOE07 | 客房备品 | 洗漱/mini吧/日耗 |
| HOE08 | 工程物资 | 管道/电气/暖通 |

## 供应商管理

- 供应商状态: Active / Inactive / Preferred / Blacklisted
- 合同类型: Annual / Quarterly / One-time / Framework
- 合同到期自动提醒

## 数据存储

HOE数据存储在FB站知识图谱内，作为子模块（HOE Module）。
