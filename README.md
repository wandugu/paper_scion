# Graph Maker 项目说明

本仓库提供一套中文优先的知识图谱本体构建与评测流程，核心脚本包括 `ontology_process.py`、`ontology_generate.py`、`ontology_eval.py` 以及公共数据集转换工具 `convert_public_datasets.py`。所有功能均基于 `config/config.yaml` 的配置自动加载，无需联网即可运行内置的 `knowledge_graph_maker` 实现。

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 按需修改 `config/config.yaml`（模型、提示词、输入/输出路径等）。
3. 一键运行完整流程：
   ```bash
   python src/ontology_process.py
   ```
4. 单独执行阶段：
   ```bash
   # 仅生成本体
   python src/ontology_generate.py

   # 仅评测本体
   python src/ontology_eval.py
   ```
5. 需要转换公开数据集时：
   ```bash
   python src/convert_public_datasets.py
   ```

## 项目结构与运行方式

- 所有 Python 脚本均位于 `src/` 目录下，其中 `src/ontology_generate.py` 是主要的本体生成脚本。
- 运行脚本前请确保 `config/config.yaml` 已根据环境调整完毕，核心字段包括：
  - `language` / `llm`：控制语言及模型参数，支持 DeepSeek、OpenAI、Groq 等。
  - `input`：指定背景文本、已有本体（默认为 `data/input` 下的文件）以及文本切片大小。
  - `output`：生成文件统一写入 `data/output`，文件名会自动添加语言后缀。
  - `pipeline` / `runtime`：流程控制与运行节奏配置（是否抽取节点/边、延迟等）。
  - `evaluation`：评测所需的设备、阈值、嵌入模型与指标输出路径（默认 `data/output/ontology_eval_metrics_2.json`）。
  - `dataset_conversion`：公开数据集转换的输入/输出目录（默认读写 `data/input`），以及样本条数限制。
- 示例素材与配置集中在 `src/assets/`、`config/`，便于统一维护。
- 如已拥有旧的本体定义，可放入 `data/input/ontology_schema_exist_<lang>.json`（或在 `config/config.yaml` 的 `input.existing_ontology_path` 中指定其它路径）。脚本会先构建新本体，再与旧版本去重合并，最终输出合并后的 `ontology_schema_<lang>.json`。
- 若只需生成本体文件，可在 `runtime.graph_extraction_enabled` 中设置为 `false`，此时脚本只会输出合并后的本体 JSON，跳过节点/边文件及 Neo4j 相关流程。
- `pipeline.mode` 可选 `all` / `generate_only` / `eval_only`，用于控制是否走完整流程，以及是否跳过生成或评测环节（评测仍需 `evaluation.enabled=true`）。
- `ontology.output_sections` 可以是 `entities`、`relationships`、`events` 的任意组合，仅保留列表中指定的板块；如需输出所有信息，配置 `all`（默认值）即可。
- `language.code`（目前支持 `cn`、`en`）用于控制 LLM 的输出语言。所有输入/输出文件都会根据语言自动追加 `_cn` 或 `_en` 后缀，例如背景语料 `data/input/background_cn.txt`、输出 `graph_nodes_cn.json`、`ontology_schema_cn.json` 等。
- `evaluation.enabled` 控制是否在生成新 schema 后，与金标准 schema 做本体评测。开启后会记录 Literal / Fuzzy / Continuous / Graph F1，并把指标写入 `evaluation.output_json`（默认 `data/output/ontology_eval_metrics_2.json`）。

## config/config.yaml 配置详解

`config/config.yaml` 汇总了所有运行参数，可根据需要按块调整：

- **language**：指定输出语言（`zh`/`en`）。
- **llm**：选择供应商与模型（DeepSeek/OpenAI/Groq），可设温度、top_p、默认 API Key、代理等。
- **dataset / input**：控制背景文本来源（直接文本或 `data/input` 下的文件）、已有本体路径、文本切片大小与数据集名称。
- **ontology / prompts / event_extraction**：定义实体、关系、事件的提示词模板、数量范围和回退样例。
- **output**：统一输出目录（默认 `data/output`）及各文件名，自动追加语言后缀。
- **pipeline / runtime**：决定是否仅生成或评测、是否抽取图谱节点/边，以及请求间隔、日志 Verbose 等运行参数。
- **evaluation**：指定评测的嵌入模型、阈值、平滑参数、输出文件和设备（支持 `auto`）。
- **dataset_conversion**：配置公开数据集的 schema 与样例路径、样本抽取上限，默认将转换结果写入 `data/input`。

运行示例脚本：

```bash
python src/ontology_generate.py
```

若希望根据配置一键完成“生成 -> 评测”或选择性跳过某些阶段，可运行流程控制脚本：

```bash
python src/ontology_process.py
```

## 核心脚本与流程说明

### ontology_generate.py —— 本体构建
- 输入：`data/input/background_<lang>.txt` 等背景语料，提示词由 `config/config.yaml` 的 `prompt`、`ontology` 块提供。
- 输出：本体文件 `data/output/ontology_schema_<lang>.json`，可选节点/边文件 `graph_nodes_<lang>.json`、`graph_edges_<lang>.json`。
- 关键特性：
  - 支持事件抽取扩展（`ontology.event_extraction.enabled`），自动生成事件类型、触发词与参数角色。
  - 支持分块处理长文本、温度与 top_p 等采样策略配置。
  - 先生成候选实体/关系/事件，再按提示词进行语义去重与结构化，确保输出字段完整一致。

### ontology_process.py —— 本体融合与流程编排
- 根据 `pipeline.mode` 选择只生成、只评测或先生成后评测。
- 在生成后会自动与已有本体（若存在）做语义匹配与去重融合，保留唯一实体、关系、事件定义，并按语言命名规则写回 `data/output/`。
- 可通过 `runtime.graph_extraction_enabled` 决定是否额外抽取节点/边并导出 Neo4j CSV；流程日志输出至 `logs/` 便于排查。

### convert_public_datasets.py —— 数据集转换与挖掘
- 依据 `config/config.yaml` 中的 `dataset_conversion` 设置，批量将公开数据集的 schema、样例转换为统一格式，方便直接复用到生成或评测流程。
- 支持对输入字段、标签的清洗与重命名，默认将转换结果写入 `data/input/`，便于后续挖掘与对齐。

## 公开数据集与下载

- **InstructIE**（多语言指令式信息抽取数据集）：提供丰富的实体、关系示例，适合训练或验证关系抽取与本体设计能力。下载地址：https://huggingface.co/datasets/zjunlp/InstructIE
- **DuIE 2.0**（百度中文关系抽取数据集）：涵盖大量中文三元组样本，适合本体关系的中文场景评测。下载地址：https://aistudio.baidu.com/datasetdetail/53720/0

### Graph 抽取与导出
- 若开启图谱抽取，生成脚本会在合并本体后调用内置的 `knowledge_graph_maker`，按照本体 schema 将语料转为节点/边 JSON，并可选导出 Neo4j CSV。
- 抽取流程包含：文本分块 → 文档封装 → 图谱生成 → 节点/边合并与去重；可配置分块大小、延迟、最大并发等运行参数。
- 输出文件带语言后缀，便于区分，同时保留源文本片段或元数据，方便溯源与挖掘。

### ontology_eval.py —— 评测指标
- 提供命令行工具对比金标准与生成本体，支持 Literal / Fuzzy / Continuous / Graph F1 四类指标：
  - **Literal F1**：严格字符串匹配，检验字段一致性。
  - **Fuzzy F1**：基于相似度的宽松匹配，适合同义或近义的实体/关系名。
  - **Continuous F1**：在连续得分空间上衡量匹配质量，兼顾召回与精度。
  - **Graph F1**：对齐节点与边后整体计算，反映结构性差异。
- 可指定嵌入模型（如 `BAAI/bge-large-zh-v1.5`）及匹配阈值，结果写入 `evaluation.output_json`。
- 如需调用 Ollama 服务（例如通过 `0.0.0.0:11434` 暴露的 `bge-m3`），可在 `config/config.yaml` 的 `evaluation.embedding_backend` 填写
  `ollama`，并在 `evaluation.ollama` 中配置 `base_url` 与 `model`；保留 `local` 则直接从本地路径加载模型。
- 评测前请安装 `sentence-transformers`、`numpy`、`scipy`。

## 本体评测命令行工具

若需要在离线环境或不同 schema 之间做对比，可直接运行 `ontology_eval.py`（所需路径、模型、阈值均从 `config/config.yaml` 读取）：

```bash
python src/ontology_eval.py
```

脚本会加载两个 schema，构建图表示，并输出 Literal / Fuzzy / Continuous / Graph F1。运行前请先 `pip install sentence-transformers numpy scipy` 以满足依赖。

如需自定义 PYTHONPATH 或以模块方式运行，也可以执行 `python -m src.ontology_generate`。

> Note: 仓库自带的 `src/knowledge_graph_maker` 目录已经同步了官方实现，若只需运行本示例，无需通过网络安装 `knowledge-graph-maker`，断网环境下也可直接执行。

如果希望使用官方 pip 版本，可根据需要执行 `pip install knowledge-graph-maker`。

## 文件布局

```
config/                 # 核心配置（模型、提示词、流程控制）
data/
  ├── input/            # 背景语料、已有本体或样例数据、转换后的公开数据集
  ├── output/           # 生成的本体、节点/边与评测指标
  └── dataset_public/   # 公开数据集原始文件
src/                    # 主程序与工具脚本
  ├── ontology_process.py
  ├── ontology_generate.py
  ├── ontology_eval.py
  ├── convert_public_datasets.py
  └── knowledge_graph_maker/  # 内置库实现
```

如需进一步定制，请直接修改配置或对应脚本逻辑。
