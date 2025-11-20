# coding=utf-8
# Copyright 2022 The current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The TACRED dataset for English Relation Classification"""

import json
import os

import datasets

_CITATION = """\
@inproceedings{zhang-etal-2017-position,
    title = "Position-aware Attention and Supervised Data Improve Slot Filling",
    author = "Zhang, Yuhao  and
      Zhong, Victor  and
      Chen, Danqi  and
      Angeli, Gabor  and
      Manning, Christopher D.",
    booktitle = "Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D17-1004",
    doi = "10.18653/v1/D17-1004",
    pages = "35--45",
}

@inproceedings{alt-etal-2020-tacred,
    title = "{TACRED} Revisited: A Thorough Evaluation of the {TACRED} Relation Extraction Task",
    author = "Alt, Christoph  and
      Gabryszak, Aleksandra  and
      Hennig, Leonhard",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.142",
    doi = "10.18653/v1/2020.acl-main.142",
    pages = "1558--1569",
}

@article{stoica2021re,
  author    = {George Stoica and
               Emmanouil Antonios Platanios and
               Barnab{\'{a}}s P{\'{o}}czos},
  title     = {Re-TACRED: Addressing Shortcomings of the {TACRED} Dataset},
  journal   = {CoRR},
  volume    = {abs/2104.08398},
  year      = {2021},
  url       = {https://arxiv.org/abs/2104.08398},
  eprinttype = {arXiv},
  eprint    = {2104.08398},
  timestamp = {Mon, 26 Apr 2021 17:25:10 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2104-08398.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
TACRED is a large-scale relation extraction dataset with 106,264 examples built over newswire
 and web text from the corpus used in the yearly TAC Knowledge Base Population (TAC KBP) challenges.
 Examples in TACRED cover 41 relation types as used in the TAC KBP challenges (e.g., per:schools_attended
 and org:members) or are labeled as no_relation if no defined relation is held. These examples are created
 by combining available human annotations from the TAC KBP challenges and crowdsourcing.

 Please see our EMNLP paper, or our EMNLP slides for full details.

Note: There is currently a label-corrected version of the TACRED dataset, which you should consider using instead of
the original version released in 2017. For more details on this new version, see the TACRED Revisited paper
published at ACL 2020.

Note 2: This Datasetreader changes the offsets of the following fields, to conform with standard Python usage (see
#_generate_examples()):
- subj_end to subj_end + 1 (make end offset exclusive)
- obj_end to obj_end + 1 (make end offset exclusive)
- stanford_head to stanford_head - 1 (make head offsets 0-based)
"""

_HOMEPAGE = "https://nlp.stanford.edu/projects/tacred/"

_LICENSE = "LDC"

_URL = "https://catalog.ldc.upenn.edu/LDC2018T24"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_PATCH_URLs = {
    "dev": "https://raw.githubusercontent.com/DFKI-NLP/tacrev/master/patch/dev_patch.json",
    "test": "https://raw.githubusercontent.com/DFKI-NLP/tacrev/master/patch/test_patch.json",
}
_RETACRED_PATCH_URLs = {
    "train": "https://raw.githubusercontent.com/gstoica27/Re-TACRED/master/Re-TACRED/train_id2label.json",
    "dev": "https://raw.githubusercontent.com/gstoica27/Re-TACRED/master/Re-TACRED/dev_id2label.json",
    "test": "https://raw.githubusercontent.com/gstoica27/Re-TACRED/master/Re-TACRED/test_id2label.json"
}

_VERSION = datasets.Version("1.0.0")

_CLASS_LABELS = [
    "no_relation",
    "org:alternate_names",
    "org:city_of_headquarters",
    "org:country_of_headquarters",
    "org:dissolved",
    "org:founded",
    "org:founded_by",
    "org:member_of",
    "org:members",
    "org:number_of_employees/members",
    "org:parents",
    "org:political/religious_affiliation",
    "org:shareholders",
    "org:stateorprovince_of_headquarters",
    "org:subsidiaries",
    "org:top_members/employees",
    "org:website",
    "per:age",
    "per:alternate_names",
    "per:cause_of_death",
    "per:charges",
    "per:children",
    "per:cities_of_residence",
    "per:city_of_birth",
    "per:city_of_death",
    "per:countries_of_residence",
    "per:country_of_birth",
    "per:country_of_death",
    "per:date_of_birth",
    "per:date_of_death",
    "per:employee_of",
    "per:origin",
    "per:other_family",
    "per:parents",
    "per:religion",
    "per:schools_attended",
    "per:siblings",
    "per:spouse",
    "per:stateorprovince_of_birth",
    "per:stateorprovince_of_death",
    "per:stateorprovinces_of_residence",
    "per:title",
]

_RETACRED_CLASS_LABELS = [
    "no_relation",
    "org:alternate_names",
    "org:city_of_branch",
    "org:country_of_branch",
    "org:dissolved",
    "org:founded",
    "org:founded_by",
    "org:member_of",
    "org:members",
    "org:number_of_employees/members",
    "org:political/religious_affiliation",
    "org:shareholders",
    "org:stateorprovince_of_branch",
    "org:top_members/employees",
    "org:website",
    "per:age",
    "per:cause_of_death",
    "per:charges",
    "per:children",
    "per:cities_of_residence",
    "per:city_of_birth",
    "per:city_of_death",
    "per:countries_of_residence",
    "per:country_of_birth",
    "per:country_of_death",
    "per:date_of_birth",
    "per:date_of_death",
    "per:employee_of",
    "per:identity",
    "per:origin",
    "per:other_family",
    "per:parents",
    "per:religion",
    "per:schools_attended",
    "per:siblings",
    "per:spouse",
    "per:stateorprovince_of_birth",
    "per:stateorprovince_of_death",
    "per:stateorprovinces_of_residence",
    "per:title"
]

_NER_CLASS_LABELS = [
    "LOCATION",
    "ORGANIZATION",
    "PERSON",
    "DATE",
    "MONEY",
    "PERCENT",
    "TIME",
    "CAUSE_OF_DEATH",
    "CITY",
    "COUNTRY",
    "CRIMINAL_CHARGE",
    "EMAIL",
    "HANDLE",
    "IDEOLOGY",
    "NATIONALITY",
    "RELIGION",
    "STATE_OR_PROVINCE",
    "TITLE",
    "URL",
    "NUMBER",
    "ORDINAL",
    "MISC",
    "DURATION",
    "O"
]


def convert_ptb_token(token: str) -> str:
    """Convert PTB tokens to normal tokens"""
    return {
        "-lrb-": "(",
        "-rrb-": ")",
        "-lsb-": "[",
        "-rsb-": "]",
        "-lcb-": "{",
        "-rcb-": "}",
    }.get(token.lower(), token)


class Tacred(datasets.GeneratorBasedBuilder):
    """TACRED is a large-scale relation extraction dataset with 106,264 examples built over newswire
    and web text from the corpus used in the yearly TAC Knowledge Base Population (TAC KBP) challenges."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="original", version=_VERSION, description="The original TACRED."
        ),
        datasets.BuilderConfig(
            name="revisited",
            version=_VERSION,
            description="TACRED Revisited (corrected labels for 5k most challenging examples in dev and test split).",
        ),
        datasets.BuilderConfig(
            name="re-tacred",
            version=datasets.Version("1.1.0"),
            description="Relabeled TACRED (corrected labels for all splits and pruned)"
        )
    ]

    DEFAULT_CONFIG_NAME = "original"  # type: ignore

    @property
    def manual_download_instructions(self):
        return (
            "To use TACRED you have to download it manually. "
            "It is available via the LDC at https://catalog.ldc.upenn.edu/LDC2018T24"
            "Please extract all files in one folder and load the dataset with: "
            "`datasets.load_dataset('DFKI-SLT/tacred', data_dir='path/to/folder/folder_name')`"
        )

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "docid": datasets.Value("string"),
                "token": datasets.Sequence(datasets.Value("string")),
                "subj_start": datasets.Value("int32"),
                "subj_end": datasets.Value("int32"),
                "subj_type": datasets.ClassLabel(names=_NER_CLASS_LABELS),
                "obj_start": datasets.Value("int32"),
                "obj_end": datasets.Value("int32"),
                "obj_type": datasets.ClassLabel(names=_NER_CLASS_LABELS),
                "stanford_pos": datasets.Sequence(datasets.Value("string")),
                "stanford_ner": datasets.Sequence(datasets.Value("string")),
                "stanford_deprel": datasets.Sequence(datasets.Value("string")),
                "stanford_head": datasets.Sequence(datasets.Value("int32")),
                "relation": datasets.ClassLabel(names=_RETACRED_CLASS_LABELS if self.config.name == 're-tacred' else _CLASS_LABELS),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('DFKI-SLT/tacred', data_dir=...)` that includes the unzipped files from the TACRED_LDC zip. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )

        patch_files = {}
        if self.config.name == "revisited":
            patch_files = dl_manager.download_and_extract(_PATCH_URLs)
        elif self.config.name == "re-tacred":
            patch_files = dl_manager.download_and_extract(_RETACRED_PATCH_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.json"),
                    "patch_filepath": patch_files.get("train"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.json"),
                    "patch_filepath": patch_files.get("test"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.json"),
                    "patch_filepath": patch_files.get("dev"),
                },
            ),
        ]

    def _generate_examples(self, filepath, patch_filepath):
        """Yields examples."""
        # This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        patch_examples = {}
        if patch_filepath is not None:
            with open(patch_filepath, encoding="utf-8") as f:
                if self.config.name == "revisited":
                    patch_examples = {example["id"]: example for example in json.load(f)}
                elif self.config.name == "re-tacred":
                    patch_examples = {_id: {"id": _id, "relation": label} for _id, label in json.load(f).items()}

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for example in data:
                id_ = example["id"]

                if id_ in patch_examples:
                    example.update(patch_examples[id_])
                elif self.config.name == "re-tacred":
                    # RE-TACRED was pruned, skip example if its id is not in patch_examples
                    continue

                yield id_, {
                    "id": example["id"],
                    "docid": example["docid"],
                    "token": [convert_ptb_token(token) for token in example["token"]],
                    "subj_start": example["subj_start"],
                    "subj_end": example["subj_end"] + 1,  # make end offset exclusive
                    "subj_type": example["subj_type"],
                    "obj_start": example["obj_start"],
                    "obj_end": example["obj_end"] + 1,  # make end offset exclusive
                    "obj_type": example["obj_type"],
                    "relation": example["relation"],
                    "stanford_pos": example["stanford_pos"],
                    "stanford_ner": example["stanford_ner"],
                    "stanford_deprel": example["stanford_deprel"],
                    "stanford_head": [
                        head - 1 for head in example["stanford_head"]
                    ],  # make offsets 0-based
                }
