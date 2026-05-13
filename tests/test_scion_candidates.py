from src.utils.scion_candidates import (
    build_candidate_package,
    candidate_package_to_schema,
    constrain_events_to_candidates,
    constrain_ontology_to_candidates,
)


def _package():
    return build_candidate_package(
        chunks=[
            "A Person joins an Organisation and deploys an Object in a Place during a Conflict.",
            "The Conflict affects an Impacted Party and requires a Critical Asset.",
        ],
        entity_hints=["Person", "Organisation", "Object", "Place"],
        relationship_hints=[
            {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
        ],
        event_type_hints=["Conflict"],
        argument_role_hints=["Initiator", "Impacted Party"],
        mode="full",
        language_code="en",
        max_text_candidates=8,
        max_evidence=2,
    )


def test_candidate_package_contains_evidence_and_full_clusters():
    package = _package()

    assert package["mode"] == "full"
    assert any(item.get("evidence") for item in package["entities"])
    assert any(item.get("cluster_id") for item in package["entities"])
    schema = candidate_package_to_schema(package)
    assert schema["relationships"]
    assert schema["events"][0]["arguments"]


def test_constrain_ontology_to_candidate_package_removes_unlinked_items():
    package = _package()
    entities, relationships, report = constrain_ontology_to_candidates(
        entities=["Person", "Unlinked Type"],
        relationships=[
            {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
            {"head_entity": "Person", "rel_type": "invented_by_test", "tail_entity": "Place"},
        ],
        package=package,
    )

    assert entities == ["Person"]
    assert relationships == [{"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"}]
    assert report["removed_entities"] == ["Unlinked Type"]
    assert report["removed_relationships"]


def test_constrain_events_to_candidate_package_preserves_linked_roles():
    package = _package()
    events, report = constrain_events_to_candidates(
        [
            {
                "event_type": "Conflict",
                "arguments": [
                    {"role": "Initiator", "description": "", "required": False},
                    {"role": "Unknown Role", "description": "", "required": False},
                ],
            },
            {"event_type": "Ignored Event", "arguments": []},
        ],
        package=package,
    )

    assert events == [
        {
            "event_type": "Conflict",
            "arguments": [{"role": "Initiator", "description": "", "required": False}],
        }
    ]
    assert report["removed_events"] == ["Ignored Event"]
    assert report["removed_roles"] == ["Conflict|Unknown Role"]
