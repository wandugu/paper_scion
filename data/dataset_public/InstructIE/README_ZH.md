# InstructIE: A Bilingual Instruction-based Information Extraction Dataset

[InstructIE: A Bilingual Instruction-based Information Extraction Dataset](https://doi.org/10.48550/arXiv.2305.11527)

[Github使用教程](https://github.com/zjunlp/EasyInstruct/blob/main/examples/kg2instruction/README.md)

## 新闻
* [2024/02] 我们发布了一个大规模(`0.32B` tokens)高质量**双语**(中文和英文)信息抽取(IE)指令微调数据集，名为 [IEPile](https://huggingface.co/datasets/zjunlp/iepie), 以及基于 `IEPile` 训练的两个模型[baichuan2-13b-iepile-lora](https://huggingface.co/zjunlp/baichuan2-13b-iepile-lora)、[llama2-13b-iepile-lora](https://huggingface.co/zjunlp/llama2-13b-iepile-lora)。
* [2023/10] 我们发布了一个新的**双语**(中文和英文)基于主题的信息抽取(IE)指令数据集，名为[InstructIE](https://huggingface.co/datasets/zjunlp/InstructIE)。
* [2023/08] 我们推出了专用于信息抽取(IE)的13B模型，名为[knowlm-13b-ie](https://huggingface.co/zjunlp/knowlm-13b-ie/tree/main)。
* [2023/05] 我们启动了基于指令的信息抽取项目。


InstructIE是一个基于主题schema的双语信息抽取数据集, 我们将文本划分成12个主题 (分别是人物, 地理地区, 建筑结构, 作品, 生物, 人造物件, 自然科学, 组织, 运输, 事件, 天文对象, 医学), 并为每个主题设计了相应的schema, 我们期望模型能在InstructIE上学习到一种通用抽取能力, 并泛化到其他领域上。


```
InstrueIE
├── train_zh.json          # 中文训练集。
├── train_en.json          # 英文训练集。
├── valid_zh.json            # 中文验证集。
├── valid_en.json            # 英文验证集。
├── test_zh.json           # 中文测试集。
├── test_en.json           # 英文测试集。
├── schema_zh.json         # 中文12个领域下的schema信息。
├── schema_en.json         # 英文12个领域下的schema信息。
```

<b>一条数据的示例</b>


```json
{
  "id": "bac7c32c47fddd20966e4ece5111690c9ce3f4f798c7c9dfff7721f67d0c54a5", 
  "cate": "地理地区", 
  "text": "阿尔夫达尔（挪威语：Alvdal）是挪威的一个市镇，位于内陆郡，行政中心为阿尔夫达尔村。市镇面积为943平方公里，人口数量为2,424人（2018年），人口密度为每平方公里2.6人。", 
  "relation": [
    {"head": "阿尔夫达尔", "head_type": "地理地区", "relation": "面积", "tail": "943平方公里", "tail_type": "度量"}, 
    {"head": "阿尔夫达尔", "head_type": "地理地区", "relation": "别名", "tail": "Alvdal", "tail_type": "地理地区"}, 
    {"head": "内陆郡", "head_type": "地理地区", "relation": "位于", "tail": "挪威", "tail_type": "地理地区"}, 
    {"head": "阿尔夫达尔", "head_type": "地理地区", "relation": "位于", "tail": "内陆郡", "tail_type": "地理地区"}, 
    {"head": "阿尔夫达尔", "head_type": "地理地区", "relation": "人口", "tail": "2,424人", "tail_type": "度量"}
  ]
}
```

各字段的说明:

|    字段     |                             说明                             |
| :---------: | :----------------------------------------------------------: |
|     id      |                       每个数据点的唯一标识符。                       |
|    cate     |           文本的主题类别，总计12种不同的主题分类。               |
|    text    | 模型的输入文本，目标是从中抽取涉及的所有关系三元组。                  |
|  relation   |   描述文本中包含的关系三元组，即(head, head_type, relation, tail, tail_type)。   |


利用上述字段，用户可以灵活地设计和实施针对不同信息**抽取需求**的指令和**输出格式**。


在训练集中我们还提供了 `entity` 字段可以执行实体命名识别任务，但我们没有在测试集中提供相应的实体标注数据。


## Citation

如果您使用了本项目代码或数据，烦请引用下列论文:
```bibtex
@article{DBLP:journals/corr/abs-2305-11527,
  author       = {Honghao Gui and
                  Shuofei Qiao and
                  Jintian Zhang and
                  Hongbin Ye and
                  Mengshu Sun and
                  Lei Liang and
                  Huajun Chen and
                  Ningyu Zhang},
  title        = {InstructIE: {A} Bilingual Instruction-based Information Extraction
                  Dataset},
  journal      = {CoRR},
  volume       = {abs/2305.11527},
  year         = {2023},
  url          = {https://doi.org/10.48550/arXiv.2305.11527},
  doi          = {10.48550/ARXIV.2305.11527},
  eprinttype    = {arXiv},
  eprint       = {2305.11527},
  timestamp    = {Thu, 22 Feb 2024 09:46:17 +0100},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2305-11527.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```