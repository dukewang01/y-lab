# Complaint Classifier (投诉分类器)

酒店投诉自动分类与分析系统。基于GSM投诉数据，自动识别投诉类型、分配责任部门、推荐处理方案。

## 源代码

- scripts/_logcase_v3.py — 投诉案例v3解析器（knowledge_center路径）
- src/complaint_classifier/__init__.py — 分类器核心逻辑
- demo/run.py — 运行示例

## 分类体系

- 噪音(19%) / 态度(16%) / 效率(13%) / 设施(9%) / 清洁(9%)
- 空调 / 水质 / 虫害 / 停车场 / 电梯 / 泳池
- 共25+子类覆盖全场景

## 审批阶梯

GSM自决￥100 → GSM￥500 → MOD￥1,000 → DO免房 ← GM公关级
