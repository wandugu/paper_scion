# SCOPE 与 SCION

本仓库为论文 **SCOPE and SCION: A Benchmark and an Auditable Reference Pipeline for Schema Induction and Fusion from Text**（`paper/scion_v6.tex`）的配套实现。

主要包括两个部分：

- **SCOPE**：面向 schema induction 与 ontology fusion 的基准构建工具。SCOPE 将公开关系抽取（RE）与事件抽取（EE）数据集转换为统一 typed schema-edge 表示，导出 train/dev/test split，并生成数据统计与 case package。
- **SCION**：可审计的 schema induction 与 fusion 流程。SCION 从 train text 构造 candidate space，在 candidate constraint 与 JSON contract 下完成 schema 生成、校验与 fallback，可选融合 ontology package，并使用 Literal、Fuzzy、Continuous、Graph 指标评测 schema graph。

## 目录结构

```text
config/
  config.yaml                  # 运行、数据集、指标与实验配置
paper/
  scion_v6.tex                 # 论文源码
src/
  ontology_generate.py         # SCION schema/event 归纳与可选 KG 抽取
  ontology_process.py          # 统一入口：生成、评测或两者都执行
  ontology_eval.py             # Literal/Fuzzy/Continuous/Graph 指标
  scion_rl.py                  # SCION-RL candidate-policy runner
  convert_public_datasets.py   # 公开 RE/EE 数据集转换
  scope_experiment.py          # SCOPE 导出、启发式评测、downstream 表格辅助
  utils/
    scion_candidates.py        # candidate package mining、validation 与 fallback schema
    build_scope_dataset.py     # SCOPE root/subset/task/case package 构建
    scope_dataset_utils.py     # SCOPE schema 与文档工具
    benchmark_stats.py         # 数据统计与覆盖率检查
    paper_report.py            # 论文统计报告工具
  rebuttal/                    # 诊断与消融实验驱动
data/
  input/                       # 转换后的输入与 gold schema
  scope/                       # SCOPE benchmark package
  output/                      # 生成 schema、图输出、指标与报告
rebuttal/
  outputs/                     # 诊断与消融输出
tests/
  rebuttal/                    # 部分诊断逻辑回归测试
```

## 主要组件

- 将公开 RE/EE 数据集转换为项目统一 schema/sample 格式。
- 构建 SCOPE package，包括 `docs.train.jsonl`、`docs.dev.jsonl`、`docs.test.jsonl`、full schema、source/subset schema、task case、fusion case 与统计汇总。
- 通过 `src.ontology_generate` 运行 candidate-constrained SCION schema induction。流程会从 train text 构造带 evidence pointer 的 candidate package，将 entity/relation/event/role 输出限制在候选空间内，并记录 controllability 统计。
- 通过 `config/config.yaml` 中的 `scion.mode` 运行 SCION-lite 或 SCION-full。
- 支持 EE `(event_type, role, ARG)` schema edge 与 SCOPE `edge_kind="ee"` 记录。
- 可选融合 ontology package，并可通过内置 `knowledge_graph_maker` 运行图谱抽取。
- 使用 Literal、Fuzzy、Continuous、Graph 指标进行 schema-graph evaluation。
- 通过 `src.scion_rl` 与 `src/rebuttal/scripts/` 运行 SCION-RL、诊断与消融实验入口。

## 安装

建议使用 Python 3.10+。

```bash
pip install -r requirements.txt
```

LLM 与 embedding 后端集中配置在 `config/config.yaml`。API key 建议通过环境变量提供：

```bash
set DEEPSEEK_API_KEY=...
set OPENAI_API_KEY=...
set GROQ_API_KEY=...
set OPENROUTER_API_KEY=...
```

多数 Python 入口建议从仓库根目录以模块方式运行：

```bash
python -m src.ontology_process
```

类 Unix shell 下也可以使用 `run.sh` 将脚本路径转换为模块路径：

```bash
./run.sh python src/ontology_process.py
```

## 复现实验流程

### 1. 转换公开数据集

```bash
python -m src.convert_public_datasets
```

脚本读取 `config/config.yaml` 的 `dataset_conversion` 配置，并将转换后的 schema 与 sample 写入 `data/input/`。

### 2. 构建 SCOPE

```bash
python src/utils/build_scope_dataset.py
```

构建脚本会在 `data/scope/` 下写出 SCOPE root package、source/subset schema、task package、case package 与统计文件。

### 3. 运行 SCION schema induction 与 evaluation

```bash
python -m src.ontology_process
```

主要配置项：

- `pipeline.mode`：`all`、`generate_only` 或 `eval_only`
- `input.type`：`sample`、`dataset`、`scope`、`text` 或 `file`
- `input.scope`：SCOPE root、part、source name、split 与 max-doc 设置
- `ontology.output_sections`：`entities`、`relationships`、`events` 或 `all`
- `scion.mode`：`lite` 或 `full`
- `scion.candidate_constraints_enabled`：是否构造并校验 SCION candidate package
- `event_extraction.enabled`：是否生成 event schema
- `evaluation.enabled`：是否运行 schema 指标评测

生成 schema、candidate package、graph artifact、controllability log 与指标默认写入 `data/output/`。

### 4. 仅运行 schema evaluation

```bash
python -m src.ontology_eval
```

gold/pred schema 路径、embedding backend、阈值、smoothing 参数与输出路径均从 `evaluation` 配置读取。

### 5. 运行 SCION-RL candidate-policy 实验

`src.ontology_generate` 写出 candidate package 后，可以运行：

```bash
python -m src.scion_rl train --candidate-package data/output/scion_candidate_package_SCOPE_zh.json --output-policy data/output/scion_rl_policy.json
python -m src.scion_rl infer --candidate-package data/output/scion_candidate_package_SCOPE_zh.json --policy data/output/scion_rl_policy.json --output-schema data/output/scion_rl_schema.json
```

### 6. 运行诊断与消融实验

单个实验脚本位于 `src/rebuttal/scripts/`，例如：

```bash
python -m src.rebuttal.scripts.E1_run_reachable_eval
python -m src.rebuttal.scripts.E3_run_eta_baseline
python -m src.rebuttal.scripts.E6_run_fusion_baselines
python -m src.rebuttal.scripts.E9_run_scion_rl_ablation
```

聚合驱动：

```bash
python -m src.rebuttal.scripts.E0_run_all
```

输出写入 `rebuttal/outputs/`。

## SCOPE Schema 表示

SCOPE 将 RE schema 统一为 typed relation edge：

```json
{
  "edge_kind": "re",
  "head_entity": "Person",
  "rel_type": "place_of_birth",
  "tail_entity": "Location"
}
```

SCOPE 将 EE schema 统一为 event-role edge：

```json
{
  "edge_kind": "ee",
  "event_type": "Acquisition",
  "role": "Buyer"
}
```

EE 形式对应统一 schema graph 中的 `(event_type, role, ARG)`。

## 配置说明

常用配置块：

- `language`：输出语言，当前为 `zh` 或 `en`
- `llm`：供应商、模型、解码参数、API key 环境变量
- `input`：输入文本来源与 SCOPE 选择
- `ontology`、`prompts`、`event_extraction`：schema hint 与提示词模板
- `scion`：candidate constraint、lite/full mode 与 candidate package 限制
- `runtime`：图抽取与请求节奏
- `evaluation`：embedding backend、阈值、graph smoothing、输出路径
- `scope_dataset`：SCOPE 构建比例、case size、fusion case 设置
- `scope_experiment`：export/eval/downstream 辅助设置
- `rebuttal`：诊断与消融实验设置

可通过 `OT_CONFIG_PATH` 指定备用配置：

```bash
set OT_CONFIG_PATH=C:\path\to\config.yaml
python -m src.ontology_process
```

## 测试

```bash
python -m pytest tests
python -m compileall src tests
```

## License

见 `LICENSE`。
