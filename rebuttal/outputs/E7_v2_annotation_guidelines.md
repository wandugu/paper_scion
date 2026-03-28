# E7 v2 Annotation Guidelines

任务目标：判断 **predicted schema item** 与 **gold schema item** 是否构成语义上可接受的匹配。

## 标注原则
1. 只看 schema-level 语义匹配，不判断某个具体句子是否支持。
2. 忽略证据句与文档数量（packet 中不提供 evidence 字段）。
3. 关注类型、角色、关系语义是否等价/可接受近义。
4. positive/negative controls 用于一致性校验，请按语义直觉标注。

## 标签
- 1: 语义可接受匹配
- 0: 语义不可接受匹配
- 空: 暂未标注
