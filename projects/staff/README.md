# staff (员工管理)

> **酒店的人，是最大的变量也是最大的资产。**

## 待开发模块

```
staff/
├── scheduling/      # 排班管理
│   └── roster.py    # 智能排班（基于预测Occ）
├── attendance/      # 考勤分析
│   └── tracker.py   # 出勤率/迟到/加班
├── performance/     # 绩效管理
│   ├── kpi.py       # KPI设定与追踪
│   └── review.py    # 评估报告
├── training/        # 培训管理
│   ├── record.py    # 培训记录
│   └── quiz.py      # 培训测验（对接quiz项目）
└── analytics/       # 人力资源分析
    ├── turnover.py  # 离职率分析
    └── cost.py      # 人力成本分析
```

## 数据来源

- 排班系统
- HR系统
- 考勤机数据
- 绩效评估

## 关联项目

`quiz`(培训测验) · `front-office`(前厅人力) · `fb-analysis`(餐饮人力)
