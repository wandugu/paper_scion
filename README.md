# The Graph Maker

A Python library that can convert any text into a graph of knowedge given an ontology.

[![The Graph Maker](./src/assets/GraphMaker.png)](https://github.com/rahulnyk/knowledge_graph_maker)
_Image generated using Adobe Firefly and Photoshop_

## What is a knowledge graph?

A knowledge graph, also known as a semantic network, represents a network of real-world entities—i.e. objects, events, situations, or concepts—and illustrates the relationship between them. This information is usually stored in a graph database and visualized as a graph structure, prompting the term knowledge “graph.”

Source: https://www.ibm.com/topics/knowledge-graph

## Why Graph?

KG can be used for a multitude of purposes. We can run graph algorithms and calculate centralities of any node, to understand how important a concept (node) is to this body of work. We can calculate communities to bunch the concepts together to better analyse the text. We can understand the connectedness between seemingly disconnected concepts.

The best of all, we can achieve **Graph Retrieval Augmented Generation (GRAG)** and chat with our text in a much more profound way using Graph as a retriever. This is a new and improved version of **Retrieval Augmented Generation (RAG)** where we use a vectory db as a retriever to chat with our documents.

---

## This project

This project is an example notebook that demonstrates the use of the knowledge graph maker library。仓库现已自带
`knowledge_graph_maker` 源码，默认会优先加载本地实现，无需联网下载。

## 项目结构与运行方式

- 所有 Python 脚本均位于 `src/` 目录下，其中 `src/demo.py` 是主要的演示脚本。
- 运行脚本前请确保 `config/config.yaml` 中的参数已经根据自身环境调整完毕。
- 示例素材（如封面图、样例文本等）也集中在 `src/assets/` 下，方便统一维护。
- 如已拥有一份旧的本体定义，可将其放入 `input/ontology_schema_exist.json`（或在
  `config/config.yaml` 的 `input.existing_ontology_path` 中指定其它路径）。脚本会先
  构建新的本体，再与旧版本进行去重合并，最终输出合并后的 `ontology_schema.json`。
- 若只需生成本体文件，可在 `runtime.graph_extraction_enabled` 中设置为 `false`，
  此时脚本只会输出合并后的本体 JSON，跳过节点/边文件及 Neo4j 相关流程。

运行示例脚本：

```bash
python src/demo.py
```

如需自定义 PYTHONPATH 或以模块方式运行，也可以执行 `python -m src.demo`。

> Note: 仓库自带的 `src/knowledge_graph_maker` 目录已经同步了官方实现，若只需运行本示例，
> 无需通过网络安装 `knowledge-graph-maker`，断网环境下也可直接执行。

如果希望使用官方 pip 版本，可根据需要执行 `pip install knowledge-graph-maker`。

To set up this project you can use [Poetry](https://python-poetry.org/docs/configuration/).
If you use poetry, please dont install the graph maker library manually. The poetry environment will manage that for you.

```shall
$ poetry config --local virtualenvs.in-project true
$ poetry install
```

---

## [Here is the python notebook that demonstrates how to extract graph from text cospus. ](https://github.com/rahulnyk/graph_maker/blob/main/graph_maker_example.ipynb)

Summary of the notebook

### 1. Define the Ontology of your Graph

The library understands the following schema for the Ontology. Behind the scene, ontology is a pydantic model.

```python
ontology = Ontology(
    # labels of the entities to be extracted. Can be a string or an object, like the following.
    labels=[
        {"Person": "Person name without any adjectives, Remember a person may be references by their name or using a pronoun"},
        {"Object": "Do not add the definite article 'the' in the object name"},
        {"Event": "Event event involving multiple people. Do not include qualifiers or verbs like gives, leaves, works etc."},
        "Place",
        "Document",
        "Organisation",
        "Action",
        {"Miscellanous": "Any important concept can not be categorised with any other given label"},
    ],
    # Relationships that are important for your application.
    # These are more like instructions for the LLM to nudge it to focus on specific relationships.
    # There is no guarentee that only these relationships will be extracted, but some models do a good job overall at sticking to these relations.
    relationships=[
        "Relation between any pair of Entities",
        ],
)
```

#### Event extraction add-on in this repo

The demo script in this repository extends the ontology configuration with an optional `event_extraction` block (see
`config/config.yaml`). When enabled, the script will ask the LLM to propose high-level event types along with:

- `trigger_words`: verbs or short phrases that can be used to anchor the event in the text corpus.
- `arguments`: a list of roles, each containing `role`, `description`, and whether the role is `required`.

The generated list is merged into `output/ontology_schema.json` under the `events` field so that downstream consumers have a
ready-made schema for event/argument extraction without interfering with the base `Ontology` model.

### 2. Split the text into chunks.

We can use as large a corpus of text as we want to create large knowledge graphs. However, LLMs have a finite context window right now. So we need to chunk the text appropriately and create the graph one chunk at a time. The chunk size that we should use depends on the model context window. The prompts that are used in this project eat up around 500 tokens. The rest of the context can be divided into input text and output graph. In my experience, 800 to 1200 token chunks are well suited.

### 3. Convert these chunks into Documents.

Documents is a pydantic model with the following schema

```python
## Pydantic document model
class Document(BaseModel):
    text: str
    metadata: dict
```

The metadata we add to the document here is tagged to every relation that is extracted out of the document.
We can add the context of the relation, for example the page number, chapter, the name of the article, etc. into the metadata. More often than not, Each node pairs have multiple relation with each other across multiple documents. The metadata helps contextualise these relationships.

### 4. Select an LLM Client

```python
## Groq models
model = "mixtral-8x7b-32768"
# model ="llama3-8b-8192"
# model = "llama3-70b-8192"
# model="gemma-7b-it"

## Open AI models
oai_model="gpt-3.5-turbo"

## Use Groq
# llm = GroqClient(model=model, temperature=0.1, top_p=0.5)
## OR Use OpenAI
llm = OpenAIClient(model=oai_model, temperature=0.1, top_p=0.5)
```

You can also define your own LLM client and pass it on to the graph maker. check out the [Knowledge Graph Maker](https://github.com/rahulnyk/knowledge_graph_maker) for more info.

### 5. Run the Graph Maker.

The [Knowledge Graph Maker](https://github.com/rahulnyk/knowledge_graph_maker) directly takes a list of documents and iterates over each of them to create one subgraph per document. The final output is the complete graph of all the documents.

Here is the simple example code

```python
from knowledge_graph_maker import GraphMaker, Ontology, Document
from knowledge_graph_maker.llm_clients.groq_client import GroqClient


graph_maker = GraphMaker(ontology=ontology, llm_client=llm, verbose=False)

## create a graph out of a list of Documents.
graph = graph_maker.from_documents(
    list(docs),
    delay_s_between=10 ## delay_s_between because otherwise groq api maxes out pretty fast.
    )
## result -> a list of Edges.
print("Total number of Edges", len(graph))
## 1503
```

The output is the final graph as a list of edges, where every edge is a pydantic model like the following.

```python
class Node(BaseModel):
    label: str
    name: str

class Edge(BaseModel):
    node_1: Node
    node_2: Node
    relationship: str
    metadata: dict = {}
    order: Union[int, None] = None
```

The [Knowledge Graph Maker](https://github.com/rahulnyk/knowledge_graph_maker) runs each document through the model and parses the response into graph edges.

### 6. Save to Neo4j (optional step)

We can save the model to Neo4j either to create an RAG application, run Network algorithms, or maybe just visualise the graph using the Bloom

```python
from graph_maker import Neo4jGraphModel

create_indices = False
neo4j_graph = Neo4jGraphModel(edges=graph, create_indices=create_indices)

neo4j_graph.save()

```
