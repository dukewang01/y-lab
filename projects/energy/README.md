# energy (能源管理)

> **让每一度电、每一吨水都看得见。**

酒店是能耗大户。空调、照明、厨房设备、洗衣房——能源成本是GOP的隐形杀手。

## 待开发模块

```
energy/
├── meter/            # 水电表读数采集
│   ├── reader.py     # 自动读数
│   └── dashboard.py  # 能耗看板
├── carbon/           # 碳中和
│   ├── scope1.py     # 直接排放（燃气/燃油）
│   ├── scope2.py     # 间接排放（电力）
│   └── scope3.py     # 供应链排放
├── analytics/        # 能效分析
│   ├── benchmark.py  # 单位RevPAR能耗对标
│   └── savings.py    # 节能方案ROI测算
└── report/
    └── esg_report.py # ESG报告自动生成
```

## 关键指标

- kWh/间夜（单位入住能耗）
- 吨水/间夜
- 碳排/间夜（kgCO₂e）
- 能源成本/总营收比

## 关联项目

`mep`(工程设备) · `faq-expansion`(电气FAQ) · `bridge-cross-station`(跨站关联)

## 数据源

- 水电费账单（FIN站已有数据）
- 工程部设备运行日志
- 外部ESG评级
