# y-quiz — 知识图谱问答器

用自然语言问y-lab的数据："上个月投诉最多的是什么？"

## 解决的痛点

> 想查一个数据要打开三个系统：财务系统看成本、投诉系统看问题、CRM看客户。能不能一句话问完？

## 用法

```python
from quiz import QuizEngine

qe = QuizEngine()
qe.load_knowledge_base("my_data.json")

answer = qe.ask("上月投诉最多的是什么类型的？")
print(answer)
# "上月菜品品质类投诉最多，共12起，占42%"
```

## 架构

```
quiz/
├── parser/       — 自然语言解析（提取意图+实体）
├── lookup/       — 知识图谱查询
├── synthesize/   — 答案合成
└── feedback/     — 问答日志（持续改进）
```
