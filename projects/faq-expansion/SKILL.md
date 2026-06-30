# FAQ Expansion (知识库扩展)

知识库FAQ的自动扩展与维护工具箱。包含模式化扩展、跨域桥接、关键词补充。

## 脚本清单 (10个)

| 脚本 | 功能 |
|:-----|:-----|
| `_add_faq_ring_lost.py` | 戒指丢失SOP + FAQ |
| `_faq_belt.py` | 传输带安全FAQ |
| `_faq_bodyfluids.py` | 体液泄漏处理FAQ |
| `_faq_electrical.py` | 电气安全FAQ |
| `_faq_expand.py` | 模式化FAQ扩展示范 |
| `_faq_expand2.py` | FAQ扩展v2 |
| `_faq_expand3.py` | FAQ扩展v3 |
| `_faq_fcu.py` | FCU风机盘管FAQ |
| `_faq_loto.py` | LOTO上锁挂牌FAQ |
| `_update_faq_lib.py` | 全量FAQ索引更新 |

## FAQ数据结构

```json
{
  "id": "FAQ_xxx",
  "question": "搜索关键词",
  "answer": "回答内容",
  "tags": ["标签1", "标签2"],
  "station": "所属工作站",
  "links": ["关联FAQ_ID1", "关联FAQ_ID2"]
}
```

## 当前规模

- 实体: 908个
- 关系: 1,074条
- 覆盖: 七站（MEP/FSAA/RISK/QA/FIN/FB/GSM）
