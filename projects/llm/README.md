# y-llm — 轻量LLM查询桥接器

把y-lab的工具和知识图谱通过LLM连接，实现自然语言→工具调用→回答。

## 解决的问题

> 不用记API、不用写代码，用普通话说"帮我看看下个月菜单怎么调"，y-llm自动调menu-advisor+menu-engine+cost-predictor出方案。

## 架构

```
llm/
├── router/       — 意图识别（用户说→应该调哪个工具）
├── context/      — 上下文构建（把y-lab数据灌给LLM）
├── execute/      — 工具调用链
└── format/       — 回答格式化
```

## 用法

```python
from llm import LLMBridge

bridge = LLMBridge()
bridge.register_project("menu-engine")
bridge.register_project("cost-predictor")

answer = bridge.query("这个月菜单应该怎么调？")
```
