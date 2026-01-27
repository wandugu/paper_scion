# PHEE

## Metadata

- language: en
- task: ee
- #docs_dedup: 4825
- #schema_edges: 32
- typed_flag: True

## Limitations
- 未标注实体类型的关系统一使用 Entity 占位。
- EE 任务 role 不包含实体 typing。
- Fusion Track 定义：Track-1 单源归纳；Track-2 partial schema completion；Track-3 多源 fusion。

## Evaluation
- 评测脚本: `src/ontology_eval.py`
