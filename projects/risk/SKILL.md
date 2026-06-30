# RISK (风险管理)

酒店风险管理（Risk Management）系统。涵盖案例Excel解析、风险等级分类、法律框架绑定。

## 源代码

- src/risk/__init__.py — 风险引擎核心
- demo/run.py — 运行示例

## 知识图谱

- 实体: 1,248个
- 关系: 6,943条
- 覆盖: 事故/隐患/整改/保险/法律

## 法律框架

7部法律绑定具体投诉场景:
- 消费者权益保护法 / 民法典 / 食品安全法
- 消防法 / 住宿业管理办法 / 个保法 / 合同法

## 脚本参考 (knowledge_center)

- _parse_log_cases.py — 案例日志解析
- _parse_log_cases_v2.py — 解析v2
- _logcase_v3.py — 解析v3（推荐）
- _bridge_gsm_risk.py — GSM?RISK桥接
