import json

from src.utils.ontology_graph import load_schema_file, schema_dict_to_graph


def test_scope_ee_edge_kind_role_is_preserved_from_list_schema(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        json.dumps(
            [
                {"edge_kind": "re", "head_entity": "Person", "rel_type": "member_of", "tail_entity": "Organisation"},
                {"edge_kind": "ee", "event_type": "Attack", "role": "Attacker"},
                {"edge_kind": "ee", "event_type": "Attack", "role": "Target"},
            ]
        ),
        encoding="utf-8",
    )

    schema = load_schema_file(schema_path)

    assert schema["events"] == [
        {
            "event_type": "Attack",
            "description": "",
            "trigger_words": [],
            "arguments": [
                {"role": "Attacker", "description": "", "required": False},
                {"role": "Target", "description": "", "required": False},
            ],
        }
    ]
    graph = schema_dict_to_graph(schema)
    labels = set(graph.nodes.values())
    assert "argument::attack::attacker" in labels
    assert "argument::attack::target" in labels


def test_scope_ee_edge_kind_role_is_preserved_from_dict_edges():
    schema = {
        "edges": [
            {"edge_kind": "ee", "event_type": "Transfer", "role": "Sender"},
            {"edge_kind": "ee", "event_type": "Transfer", "role": "Recipient"},
        ]
    }

    graph = schema_dict_to_graph(schema)

    labels = set(graph.nodes.values())
    assert "event::transfer" in labels
    assert "argument::transfer::sender" in labels
    assert "argument::transfer::recipient" in labels
