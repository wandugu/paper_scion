# E0 Repo Map

- dataset loading code: `src/utils/dataset_paths.py`, `src/utils/scope_dataset_utils.py`
- split logic: `src/utils/build_scope_dataset.py` (`global_split_ratios`, `split_seed`)
- ontology/schema induction: `src/ontology_generate.py`, `src/ontology_process.py`
- metric evaluation: `src/ontology_eval.py`
- fusion pipeline related: `src/utils/build_scope_dataset.py`
- downstream extraction: `src/knowledge_graph_maker/graph_maker.py`
- RL training/inference: repository not found (only controllability hooks)
- configs/logging: `config/config.yaml`, `src/utils/logger.py`
