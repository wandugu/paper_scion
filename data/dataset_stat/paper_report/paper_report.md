# Paper Report

- dataset: duIE_zh
- language: zh

## Counts we report

### Pred schema
- relation_types: 18
- event_types: 0
- roles: 0
- re_edges: 18
- ee_edges: 0
- graph_nodes: 58
- graph_edges: 85

### Samples
- sample_count: 286426
- doc_count: 191957
- dedup_by_text: True
- cross_dataset_dedup: False

## Graph F1 config

- embedding_backend: ollama
- embedding_model: models/bge-m3
- ollama_model: bge-m3
- embedding_dim: 1024
- similarity: cosine
- matching: hungarian
- threshold: 0.45
- graph_smoothing_rounds: 2
- graph_smoothing_alpha: 0.5

## Fusion track

- base_ontologies: 1
- leakage_check: ['drop entries that exactly match gold labels']
- mapping_fields: ['equivalent', 'broader', 'narrower']

