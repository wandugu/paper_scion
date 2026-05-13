# SCOPE and SCION

This repository is the accompanying implementation for the paper
**SCOPE and SCION: A Benchmark and an Auditable Reference Pipeline for Schema
Induction and Fusion from Text** (`paper/scion_v6.tex`).

It mainly includes two parts:

- **SCOPE**: benchmark construction utilities for schema induction and ontology
  fusion. SCOPE converts public relation extraction (RE) and event extraction
  (EE) datasets into a unified typed schema-edge representation, exports
  train/dev/test splits, and produces dataset statistics and case packages.
- **SCION**: an auditable schema induction and fusion pipeline. SCION mines
  candidate spaces from train text, applies contract-constrained schema
  generation and validation, optionally fuses induced schemas with ontology
  packages, and evaluates schema graphs with Literal, Fuzzy, Continuous, and
  Graph metrics.

## Repository Layout

```text
config/
  config.yaml                  # Runtime, dataset, metric, and experiment config
paper/
  scion_v6.tex                 # Paper source used as the implementation reference
src/
  ontology_generate.py         # SCION schema/event induction and optional KG extraction
  ontology_process.py          # Pipeline entry point: generate, evaluate, or both
  ontology_eval.py             # Literal/Fuzzy/Continuous/Graph schema metrics
  scion_rl.py                  # SCION-RL candidate-policy runner
  convert_public_datasets.py   # Public RE/EE dataset conversion
  scope_experiment.py          # SCOPE export, heuristic eval, downstream table helper
  utils/
    scion_candidates.py        # Candidate package mining, validation, and fallback schema
    build_scope_dataset.py     # SCOPE root/subset/task/case package builder
    scope_dataset_utils.py     # SCOPE schema and document utilities
    benchmark_stats.py         # Dataset statistics and coverage checks
    paper_report.py            # Paper-oriented reporting utilities
  rebuttal/                    # Diagnostic and ablation experiment drivers
data/
  input/                       # Converted inputs and gold schemas
  scope/                       # SCOPE benchmark package
  output/                      # Generated schemas, graph outputs, metrics, reports
rebuttal/
  outputs/                     # Diagnostic and ablation outputs
tests/
  rebuttal/                    # Regression tests for selected diagnostic logic
```

## Main Components

- Public RE/EE dataset conversion into the project schema and sample format.
- SCOPE package construction, including `docs.train.jsonl`, `docs.dev.jsonl`,
  `docs.test.jsonl`, full schemas, source/subset schemas, task cases, fusion
  cases, and summary statistics.
- Candidate-constrained SCION schema induction through `src.ontology_generate`.
  The pipeline builds evidence-linked candidate packages from train text,
  constrains entity/relation/event/role outputs to that package, validates the
  result, and records controllability statistics.
- SCION-lite and SCION-full modes through `scion.mode` in `config/config.yaml`.
- Event schema support for EE `(event_type, role, ARG)` edges and SCOPE
  `edge_kind="ee"` schema records.
- Optional ontology package fusion and optional graph extraction through the
  bundled `knowledge_graph_maker` implementation.
- Schema-graph evaluation with Literal, Fuzzy, Continuous, and Graph metrics.
- SCION-RL and diagnostic/ablation experiment entry points under `src.scion_rl`
  and `src/rebuttal/scripts/`.

## Setup

Use Python 3.10+.

```bash
pip install -r requirements.txt
```

Configure LLM and embedding backends in `config/config.yaml`. API keys should be
provided through environment variables:

```bash
set DEEPSEEK_API_KEY=...
set OPENAI_API_KEY=...
set GROQ_API_KEY=...
set OPENROUTER_API_KEY=...
```

Run Python entry points as modules from the repository root:

```bash
python -m src.ontology_process
```

On Unix-like shells, `run.sh` also maps script paths to module paths:

```bash
./run.sh python src/ontology_process.py
```

## Reproduction Workflow

### 1. Convert Public Datasets

```bash
python -m src.convert_public_datasets
```

The converter reads `dataset_conversion` entries from `config/config.yaml` and
writes converted schemas and samples under `data/input/`.

### 2. Build SCOPE

```bash
python src/utils/build_scope_dataset.py
```

The builder writes the SCOPE root package, source/subset schemas, task packages,
case packages, and statistics under `data/scope/`.

### 3. Run SCION Schema Induction and Evaluation

```bash
python -m src.ontology_process
```

Key configuration fields:

- `pipeline.mode`: `all`, `generate_only`, or `eval_only`
- `input.type`: `sample`, `dataset`, `scope`, `text`, or `file`
- `input.scope`: SCOPE root, part, source name, split, and max-doc settings
- `ontology.output_sections`: `entities`, `relationships`, `events`, or `all`
- `scion.mode`: `lite` or `full`
- `scion.candidate_constraints_enabled`: candidate package construction and
  validation toggle
- `event_extraction.enabled`: event schema generation toggle
- `evaluation.enabled`: schema metric toggle

Generated schemas, candidate packages, graph artifacts, controllability logs,
and metrics are written under `data/output/` unless overridden in config.

### 4. Run Schema Evaluation Only

```bash
python -m src.ontology_eval
```

Gold and predicted schema paths, embedding backend, threshold, smoothing
parameters, and output paths are read from the `evaluation` config block.

### 5. Run SCION-RL Candidate-Policy Experiments

After `src.ontology_generate` writes a candidate package:

```bash
python -m src.scion_rl train --candidate-package data/output/scion_candidate_package_SCOPE_zh.json --output-policy data/output/scion_rl_policy.json
python -m src.scion_rl infer --candidate-package data/output/scion_candidate_package_SCOPE_zh.json --policy data/output/scion_rl_policy.json --output-schema data/output/scion_rl_schema.json
```

### 6. Run Diagnostic and Ablation Experiments

Individual experiment wrappers are under `src/rebuttal/scripts/`, for example:

```bash
python -m src.rebuttal.scripts.E1_run_reachable_eval
python -m src.rebuttal.scripts.E3_run_eta_baseline
python -m src.rebuttal.scripts.E6_run_fusion_baselines
python -m src.rebuttal.scripts.E9_run_scion_rl_ablation
```

The aggregated driver is:

```bash
python -m src.rebuttal.scripts.E0_run_all
```

Outputs are written to `rebuttal/outputs/`.

## SCOPE Schema Representation

SCOPE normalizes RE schemas as typed relation edges:

```json
{
  "edge_kind": "re",
  "head_entity": "Person",
  "rel_type": "place_of_birth",
  "tail_entity": "Location"
}
```

SCOPE normalizes EE schemas as event-role edges:

```json
{
  "edge_kind": "ee",
  "event_type": "Acquisition",
  "role": "Buyer"
}
```

The EE form corresponds to `(event_type, role, ARG)` in the unified schema graph.

## Configuration Notes

Common config blocks:

- `language`: output language, currently `zh` or `en`
- `llm`: provider, model, decoding parameters, API key environment settings
- `input`: text source and SCOPE selection
- `ontology`, `prompts`, `event_extraction`: schema hints and prompt templates
- `scion`: candidate constraints, lite/full mode, and candidate package limits
- `runtime`: graph extraction and request pacing
- `evaluation`: embedding backend, threshold, graph smoothing, output path
- `scope_dataset`: SCOPE build ratios, case sizes, fusion case settings
- `scope_experiment`: export/eval/downstream helper settings
- `rebuttal`: diagnostic and ablation experiment settings

Use `OT_CONFIG_PATH` to run with an alternate config:

```bash
set OT_CONFIG_PATH=C:\path\to\config.yaml
python -m src.ontology_process
```

## Tests

```bash
python -m pytest tests
python -m compileall src tests
```

## License

See `LICENSE`.
