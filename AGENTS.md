# AGENTS 使用说明

本文件面向在本仓库协作的代理（Codex/GPT 系列），总结项目结构、运行方式与开发约定，便于快速定位代码并保持风格一致。除非上层指令另有要求，所有变更请遵循本说明。

## 仓库概览
- 主要脚本位于 `src/`：
  - `ontology_generate.py`：根据背景语料生成本体与（可选）事件定义，是最常用的入口。
  - `ontology_process.py`：基于 `pipeline.mode` 串联本体生成、去重合并与评测。
  - `ontology_eval.py`：对比生成本体与金标准 schema，计算 Literal/Fuzzy/Continuous/Graph F1。
  - `convert_public_datasets.py`：将公开数据集 schema/样例转换为统一格式。
  - `knowledge_graph_maker/`：内置的知识图谱抽取实现，无需额外安装。
- 配置集中在 `config/config.yaml`，覆盖 LLM 供应商与模型参数、输入/输出路径、图谱抽取与评测开关、数据集转换路径等。
- 数据目录：
  - `data/input`：背景语料、已有本体、转换后的公开数据集。
  - `data/output`：生成的 schema、节点/边 JSON 及评测指标。
- 日志默认写入 `logs/`，请复用 `utils.logger.get_ot_logger`。

## 运行与测试
- 安装依赖：`pip install -r requirements.txt`。
- 常用命令：
  - 生成本体：`python src/ontology_generate.py`
  - 完整流程（生成→去重→评测或按模式跳过阶段）：`python src/ontology_process.py`
  - 仅评测：`python src/ontology_eval.py`
  - 转换公开数据集：`python src/convert_public_datasets.py`
- 运行前请根据场景调整 `config/config.yaml`，并通过环境变量提供对应 LLM API Key（如 `DEEPSEEK_API_KEY`、`OPENAI_API_KEY`、`GROQ_API_KEY`）。

## 开发约定
- **风格**：遵循 PEP 8，函数与变量命名保持清晰、语义化；避免在导入语句周围添加 try/except。
- **日志**：使用 `utils.logger.get_ot_logger()` 获取 logger，保持统一格式；不要在主流程中硬编码 `print`。
- **路径与配置**：优先通过 `utils.common.load_yaml_config` 读取配置，并使用 `resolve_project_path` 来定位相对路径；生成/读取文件时注意自动的语言后缀（`_zh`/`_en`）。
- **数据管线**：
  - 当新增处理步骤时，确保与 `pipeline`/`runtime` 配置对齐，可通过新增字段开关控制。
  - 复用 `utils.dataset_paths` 中的路径解析与背景文本加载工具，避免重复实现。
  - 图谱节点/边输出应保持与 `knowledge_graph_maker` 现有结构兼容。
- **提示词与模板**：若修改或新增提示词，请保持中英文模板一致性，并考虑 `ontology.output_sections`/`event_extraction` 配置的条件分支。
- **评测**：添加新指标时应与 `evaluation` 配置对齐，并在 `data/output` 输出结果 JSON；避免破坏现有的 F1 计算路径。
- **异常处理**：在核心流程中使用明确的错误信息；保持对缺失配置/文件的友好提示。

## 提交要求
- 提交前请尽量运行相关脚本或单元测试（如有），确保基本可运行。
- 保持 commit 信息简洁明了；若修改配置、提示词或示例数据，请在描述中说明范围。
- 如新增模块/脚本，请在本文件或 README 中补充用途与运行方法（若与用户指令无冲突）。

