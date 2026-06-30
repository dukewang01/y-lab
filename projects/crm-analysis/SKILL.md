# CRM Analysis (客户数据管理)

酒店客户数据管理与分析系统。包含客户数据导入、历史订单解析、偏好标签、小程序深度分析。

## 脚本清单 (11个)

| 脚本 | 功能 |
|:-----|:-----|
| `_crm_import_2022h1.py` | 导入2022上半年客户数据 |
| `_crm_import_2022h2.py` | 导入2022下半年客户数据 |
| `_crm_import_2022nd.py` | 导入2022年末补充数据 |
| `_crm_import_2023h1.py` | 导入2023上半年数据 |
| `_crm_import_2023q4.py` | 导入2023Q4数据 |
| `_crm_import_h3.py` | 导入H/3数据（历史散客） |
| `_crm_import_history.py` | 全量历史客户导入 |
| `_crm_import_orders.py` | 解析/导入历史订单 |
| `_wx_miniprogram_analysis.py` | 微信小程序深度分析 |
| `_bridge_open_menu_crm.py` | OPEN自助菜单↔CRM偏好桥接 |
| `_bridge_settlement.py` | CRM结算桥接 |

## 数据规模

- 客户数: 3,831人
- 到店记录: 21,083条
- 偏好标签: 4,254条
- 覆盖: BACIO/OPEN/YUXI + 历史散客 + VIP高管 + 企业客户 + 政府官员

## 分析维度

1. 客户价值分层（高/中/低/流失）
2. 到店频率与消费曲线
3. 菜品偏好画像
4. 最优推荐链路（CRM标签→FB菜品）

## 数据存储

CRM知识图谱：`knowledge_center/fb_crm/`
