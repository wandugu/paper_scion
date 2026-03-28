from src.rebuttal import rebuttal_experiments as rexp


def test_e1_reachable_precision_uses_full_predictions():
    canonical_gold = [("re", "person", "works_for", "org")]
    reachable_target = [("re", "entity", "works_for", "entity")]
    selected = rexp._e1_prediction_generation_target(canonical_gold, reachable_target, "reachable", anchor_from_target=True)
    assert selected == canonical_gold


def test_e2_target_variants_are_distinct():
    raw_edges = [("re", "Person ", "Works-For", "Org")]
    typed = rexp._variant_transform(raw_edges, "typed_unnormalized")
    normalized = rexp._variant_transform(raw_edges, "full_normalized_gold")
    assert typed != normalized


def test_e2_full_normalized_matches_e1_full_gold():
    raw_edges = [("re", " Person", "Works-For", "Org ")]
    canonical = [rexp._canonicalize_edge(raw_edges[0], typed=True, ignore_direction=False)]
    normalized = rexp._variant_transform(canonical, "full_normalized_gold")
    assert normalized == canonical


def test_e3_cache_key_includes_target_variant():
    key = rexp._build_e3_cache_key("S1", "eta", "full_normalized_gold", "submission_aligned_scope_v1", "abc123")
    assert "full_normalized_gold" in key
    assert "submission_aligned_scope_v1" in key


def test_e3_full_gold_matches_submission_aligned_eval():
    assert rexp._e3_target_variant() == "full_normalized_gold"


def test_e8_cache_key_includes_noise_and_encoder():
    key = rexp._build_e8_cache_key("S1", "scion_full", 0.2, "bge-m3", "submission_aligned_scope_v1", "abc123")
    assert "noise=0.2000" in key
    assert "encoder=bge-m3" in key


def test_e8_zero_noise_matches_base_eval():
    assert rexp._e8_noise_run_tag(0.0) == "full"
    assert rexp._e8_noise_run_tag(0.2).startswith("E8_noise_")
