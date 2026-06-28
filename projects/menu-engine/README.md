# menu-engine — 市场感知菜单工程

**Built: 2026-06-28** | **Status: v0.1 dev**

市场感知菜单工程智能体。理解外部市场价格波动和内部菜品偏好，辅助菜单决策。

## 架构

```
src/menusense/
  sense.py    - 数据模型 (MenuItem, Ingredient, Complaint, Preference)
  analyze.py  - 分析引擎 (定价/成本/BCG矩阵/偏好/投诉)
  answer.py   - 自然语言查询路由
adapters/
  base.py     - 适配器基类
  csv_adapter.py - CSV文件适配器示例
sensors/
  price_index.py  - 市场价格传感器（季节性+波动）
  trend_sensor.py - 消费趋势传感器
demo/run.py   - 虚构酒店数据演示
```

## 用法

```bash
cd projects/menu-engine
pip install -e .
python demo/run.py
```
