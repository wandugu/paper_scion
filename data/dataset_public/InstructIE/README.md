# InstructIE: A Bilingual Instruction-based Information Extraction Dataset

[InstructIE: A Bilingual Instruction-based Information Extraction Dataset](https://doi.org/10.48550/arXiv.2305.11527)

[Github Tutorial](https://github.com/zjunlp/EasyInstruct/blob/main/examples/kg2instruction/README.md)


## News
* [2024/02] We released a large-scale (0.32B tokens) high-quality bilingual (Chinese and English) Information Extraction (IE) instruction tuning dataset named [IEPile](https://huggingface.co/datasets/zjunlp/iepie), along with two models trained on `IEPile`, [baichuan2-13b-iepile-lora](https://huggingface.co/zjunlp/baichuan2-13b-iepile-lora) and [llama2-13b-iepile-lora](https://huggingface.co/zjunlp/llama2-13b-iepile-lora).
* [2023/10] We released a new bilingual (Chinese and English) theme-based Information Extraction (IE) instruction dataset named [InstructIE](https://huggingface.co/datasets/zjunlp/InstructIE).
* [2023/08] We introduced a dedicated 13B model for Information Extraction (IE), named [knowlm-13b-ie](https://huggingface.co/zjunlp/knowlm-13b-ie/tree/main).
* [2023/05] We initiated an instruction-based Information Extraction project.


InstructIE is an bilingual information extraction dataset based on topic schemas. We divide the text into 12 topics, namely, Person, Geographic_Location, Building, Works, Creature, Artificial_Object, Natural_Science, Organization, Transport, Event, Astronomy, Medicine. For each topic, we have designed corresponding schemas. We expect the model to learn a general extraction capability on InstructIE and generalize it to other domains.

```
InstrueIE
├── train_zh.json          # Chinese training set.
├── train_en.json          # English training set.
├── valid_zh.json            # Chinese validation set.
├── valid_en.json            # English validation set.
├── test_zh.json           # Chinese test set.
├── test_en.json           # English test set.
├── schema_zh.json         # Schema information for 12 domains in Chinese.
├── schema_en.json         # Schema information for 12 domains in English.
```


<b>Example of data</b>

```
{
  "id": "841ef2af4cfe766dd9295fb7daf321c299df0fd0cef14820dfcb421161eed4a1", 
  "text": "NGC1313 is a galaxy in the constellation of Reticulum. It was discovered by the Australian astronomer James Dunlop on September 27, 1826. It has a prominent uneven shape, and its axis does not completely revolve around its center. Near NGC1313, there is another galaxy, NGC1309.", 
  "relation": [
    {"head": "NGC1313", "head_type": "astronomical object type", "relation": "time of discovery", "tail": "September 27, 1826", "tail_type": "time"}, 
    {"head": "NGC1313", "head_type": "astronomical object type", "relation": "discoverer or inventor", "tail": "James Dunlop", "tail_type": "organization/human"}, 
    {"head": "NGC1313", "head_type": "astronomical object type", "relation": "of", "tail": "Reticulum", "tail_type": "astronomical object type"}
  ]
}
```


| Field       | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| id          | The unique identifier for each data point.                       |
| cate        | The category of the text's subject, with a total of 12 different thematic categories. |
| text       | The input text for the model, with the goal of extracting all the involved relationship triples. |
| relation    | Describes the relationship triples contained in the text, i.e., (head, head_type, relation, tail, tail_type). |

With the fields mentioned above, users can flexibly design and implement instructions and output formats for different information extraction needs.

We also provided the `entity` field in the training set to perform entity naming recognition tasks, but we did not provide corresponding entity annotation data in the test set.


## Citation

Please cite these papers if you use InstructIE in your work.

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

