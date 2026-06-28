# y-crm — 客户全生命周期管理系统

> 酒店行业客户数据管理 + RFM 分段 + 流失预警 + 偏好推荐

---

## 定位

y-crm 是 y-lab 面向酒店行业的客户关系管理组件，专注于 **客户全生命周期** 的数据驱动运营：

- **Guest（客户档案）** — 统一客户身份，聚合消费、偏好、行为轨迹
- **RFM（价值分段）** — 基于 Recency / Frequency / Monetary 三轴对客户分层
- **Churn（流失预警）** — 根据活跃衰退特征识别高流失风险客户
- **Preference（偏好推荐）** — 从历史标签提炼推荐特征，辅助精准营销

---

## 架构

```
crm/
├── README.md
├── guest/          # 客户档案模块
│   ├── model.py    # 客户数据结构
│   └── service.py  # 客户查询/合并/去重
├── rfm/            # RFM 价值分段模块
│   ├── model.py    # RFM 分数 & 分段定义
│   └── service.py  # 分段计算引擎
├── churn/          # 流失预警模块
│   ├── model.py    # 流失风险等级
│   └── service.py  # 流失检测逻辑
├── preference/     # 偏好推荐模块
│   ├── model.py    # 标签体系
│   └── service.py  # 偏好归纳 & 推荐生成
└── demo/
    └── run.py      # 端到端 demo（无外部依赖）
```

---

## 用法示例

```python
from guest.service import GuestService
from rfm.service import RfmService
from churn.service import ChurnService
from preference.service import PreferenceService

# 1. 加载客户
guests = GuestService.load_all()

# 2. RFM 分段
rfm = RfmService()
segments = rfm.segment_all(guests)

# 3. 流失预警
churn = ChurnService()
warnings = churn.evaluate_all(guests)

# 4. 偏好推荐
pref = PreferenceService()
recommendations = pref.recommend_all(guests)
```

```sh
# 运行 demo
python demo/run.py
```

---

## 快速开始

```bash
cd projects/crm
python demo/run.py
```

输出示例：

```
=== y-crm Demo ===

客户 张伟（uuid-001）
· 本月消费: 4 次 / ¥2,460.00
· RFM 分段: 高价值
· 流失风险: 低
· 推荐偏好: 商务出行、精品餐厅

客户 李娜（uuid-002）
· 本月消费: 1 次 / ¥380.00
· RFM 分段: 低价值
· 流失风险: 高 ⚠️
· 推荐偏好: 亲子活动、网红打卡
```

---

## 与 CRM 站的关系

y-crm 是 y-lab CRM 知识体系的一个 **可运行的数据层实现**。对应的知识体系（方法论、RFM 理论、流失模型分析）可参考：

> [y-lab CRM 知识站](https://github.com/y-lab/crm-wiki)（建设中）

Here the "落地" — 理论变成代码。

---

## License

MIT — y-lab
