import json

from src.ontology_generate import build_event_schema, build_ontology
from src.utils.scion_candidates import build_candidate_package


class FakeLLM:
    def __init__(self, payload):
        self.payload = payload
        self.last_user_message = ""

    def generate(self, user_message, system_message):  # noqa: ARG002
        self.last_user_message = user_message
        return json.dumps(self.payload)


def _package():
    return build_candidate_package(
        chunks=["Person joins Organisation during Conflict."],
        entity_hints=["Person", "Organisation"],
        relationship_hints=[
            {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
        ],
        event_type_hints=["Conflict"],
        argument_role_hints=["Participant"],
        mode="lite",
        language_code="en",
    )


def test_build_ontology_enforces_candidate_contract():
    llm = FakeLLM(
        {
            "entities": ["Person", "Unlinked Type"],
            "relationships": [
                {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
                {"head_entity": "Person", "rel_type": "invented_by_test", "tail_entity": "Organisation"},
            ],
        }
    )

    ontology = build_ontology(llm, "Person joins Organisation.", candidate_package=_package())

    assert "[SCION Candidate Contract]" in llm.last_user_message
    assert ontology.entities == ["Person"]
    assert [rel.model_dump(exclude_none=True) for rel in ontology.relationships] == [
        {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"}
    ]


def test_build_event_schema_enforces_candidate_contract():
    llm = FakeLLM(
        {
            "events": [
                {
                    "event_type": "Conflict",
                    "arguments": [
                        {"role": "Participant", "description": "", "required": False},
                        {"role": "Unknown Role", "description": "", "required": False},
                    ],
                }
            ]
        }
    )

    events = build_event_schema(llm, "Person joins Organisation during Conflict.", candidate_package=_package())

    assert "[SCION Candidate Contract]" in llm.last_user_message
    assert events == [
        {
            "event_type": "Conflict",
            "description": "",
            "trigger_words": [],
            "arguments": [{"role": "Participant", "description": "", "required": False}],
        }
    ]
