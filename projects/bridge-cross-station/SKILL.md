# Bridge Cross-Station (知识图谱跨站桥接)

连接酒店九站体系之间的知识图谱桥接脚本。将分散在不同站点的知识关联成统一网络。

## 脚本清单 (10个)

| 脚本 | 桥接内容 |
|:-----|:---------|
| `_bridge_chafing_fire.py` | 烧烤炉火灾 → RISK+GSM+QA联动 |
| `_bridge_chafing_qa.py` | 烧烤炉 → QA品牌标准 |
| `_bridge_counter.py` | 前台计数器事件 → 多站串联 |
| `_bridge_exposure.py` | 暴露事件 → RISK |
| `_bridge_fsaa_qa.py` | FSAA食品审计 ↔ QA品牌标准 |
| `_bridge_gsm_qa.py` | GSM投诉 ↔ QA合规标准 |
| `_bridge_gsm_risk.py` | GSM投诉 ↔ RISK风险预案 |
| `_bridge_label.py` | 标签统一化（跨站对齐） |
| `_bridge_phase1.py` | 第一阶段跨站桥接 |
| `_bridge_slipper.py` | 拖鞋事件 → 多站追溯 |

## 九站体系

| 站 | 色标 | 功能 |
|:--:|:----:|:-----|
| MEP | 🟡 | 物业工程机电 |
| FSAA | 🔴 | 食品安全审计 |
| RISK | 🔵 | 风险管理 |
| QA | 🟢 | 品牌标准 |
| FIN | 🟣 | 财务营收 |
| FB | 🟠 | 产品/促销 |
| LIB | 🟠 | 知识图书馆 |
| GSM | 🌐 | 投诉/案例 |
| CRM | 🧑‍🤝‍🧑 | 客户数据 |

## 桥接模式

1. **事件溯源**: 投诉→设备故障→工程整改→标准更新
2. **标准对齐**: FSAA检测点→QA标准→RISK预判
3. **标签归一**: 跨站同义词/层级标签统一
4. **链路追溯**: 损失→责任→整改→预防
