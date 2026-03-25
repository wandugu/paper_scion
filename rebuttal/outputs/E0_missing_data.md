# E0 Missing Data

以下 source 缺少用于 reachable 构造的 train 证据：

- duIE_zh: docs.train.jsonl relations/events evidence

准备方式：为对应 source 补充 `data/scope/subsets/<subset>/docs.train.jsonl`，并确保每条样本含 `relations/events` 字段。