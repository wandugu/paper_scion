from src.scion_rl import infer_schema, score_contract_reward, train_policy, weighted_reward
from src.utils.scion_candidates import build_candidate_package


def test_scion_rl_policy_trains_and_infers_schema():
    package = build_candidate_package(
        chunks=["Person joins Organisation during Conflict near Place."],
        entity_hints=["Person", "Organisation", "Place"],
        relationship_hints=[
            {"head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
        ],
        event_type_hints=["Conflict"],
        argument_role_hints=["Participant"],
        mode="lite",
        language_code="en",
        max_text_candidates=5,
        max_evidence=2,
    )

    policy = train_policy([package], epochs=2)
    schema = infer_schema(package, policy)
    reward_terms = score_contract_reward(schema, package)

    assert policy["schema"] == "scion_rl_policy_v1"
    assert policy["training_trace"]
    assert schema["entities"]
    assert schema["relationships"]
    assert schema["events"]
    assert 0.0 <= weighted_reward(reward_terms, policy["reward_weights"]) <= 1.0
