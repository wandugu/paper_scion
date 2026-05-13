"""Native lightweight SCION-RL contract-policy runner.

This module keeps the SCION-RL interface inside the main codebase instead of
only reporting diagnostic tables. It implements a deterministic reward-shaped
candidate ranking policy over SCION candidate packages. It does not bundle the
paper's Qwen/offline-PPO model training artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .utils.scion_candidates import candidate_package_to_schema, normalize_candidate_label


REWARD_TERMS = [
    "json_validity",
    "candidate_constraint",
    "evidence_coverage",
    "compactness",
    "structural_consistency",
]
DEFAULT_REWARD_WEIGHTS = {
    "json_validity": 0.25,
    "candidate_constraint": 0.20,
    "evidence_coverage": 0.20,
    "compactness": 0.10,
    "structural_consistency": 0.25,
}
DEFAULT_POLICY_WEIGHTS = {
    "evidence_count": 0.34,
    "support": 0.24,
    "config_hint": 0.18,
    "clustered": 0.12,
    "label_length": -0.03,
}


def load_candidate_package(path: str | Path) -> Dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != "scion_candidate_package_v1":
        raise ValueError(f"Not a SCION candidate package: {path}")
    return payload


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _candidate_label(item: Dict[str, Any], label_key: str) -> str:
    return str(item.get(label_key) or "").strip()


def _feature_vector(item: Dict[str, Any], label_key: str) -> Dict[str, float]:
    label = _candidate_label(item, label_key)
    support = float(item.get("support") or 0.0)
    evidence = item.get("evidence") or []
    evidence_count = float(len(evidence)) if isinstance(evidence, list) else 0.0
    return {
        "evidence_count": min(evidence_count / 3.0, 1.0),
        "support": min(support / 8.0, 1.0),
        "config_hint": 1.0 if item.get("source") == "config_hint" else 0.0,
        "clustered": 1.0 if item.get("cluster_id") else 0.0,
        "label_length": min(len(normalize_candidate_label(label).split()) / 6.0, 1.0),
    }


def score_candidate(item: Dict[str, Any], label_key: str, policy_weights: Dict[str, float]) -> float:
    features = _feature_vector(item, label_key)
    return sum(policy_weights.get(name, 0.0) * value for name, value in features.items())


def _rank(items: Sequence[Dict[str, Any]], label_key: str, policy_weights: Dict[str, float]) -> List[Dict[str, Any]]:
    return sorted(
        (item for item in items if _candidate_label(item, label_key)),
        key=lambda item: (
            score_candidate(item, label_key, policy_weights),
            len(item.get("evidence") or []),
            _candidate_label(item, label_key),
        ),
        reverse=True,
    )


def infer_schema(
    package: Dict[str, Any],
    policy: Dict[str, Any],
    max_entities: int = 16,
    max_relationships: int = 24,
    max_events: int = 12,
) -> Dict[str, Any]:
    policy_weights = dict(DEFAULT_POLICY_WEIGHTS)
    policy_weights.update(policy.get("policy_weights") or {})
    selected_package = {
        "schema": package.get("schema"),
        "mode": package.get("mode"),
        "entities": _rank(package.get("entities", []), "label", policy_weights)[:max_entities],
        "relationships": _rank(package.get("relationships", []), "rel_type", policy_weights)[:max_relationships],
        "events": _rank(package.get("events", []), "event_type", policy_weights)[:max_events],
        "roles": _rank(package.get("roles", []), "role", policy_weights),
    }
    return candidate_package_to_schema(selected_package, max_entities, max_relationships, max_events)


def _schema_counts(schema: Dict[str, Any]) -> Tuple[int, int, int, int]:
    entities = schema.get("entities") if isinstance(schema.get("entities"), list) else []
    relationships = schema.get("relationships") if isinstance(schema.get("relationships"), list) else []
    events = schema.get("events") if isinstance(schema.get("events"), list) else []
    role_count = sum(
        len(event.get("arguments") or [])
        for event in events
        if isinstance(event, dict)
    )
    return len(entities), len(relationships), len(events), role_count


def score_contract_reward(schema: Dict[str, Any], package: Dict[str, Any]) -> Dict[str, float]:
    try:
        json.dumps(schema, ensure_ascii=False)
        json_validity = 1.0
    except TypeError:
        json_validity = 0.0

    entity_count, relationship_count, event_count, role_count = _schema_counts(schema)
    output_size = max(1, entity_count + relationship_count + event_count + role_count)

    package_size = max(
        1,
        len(package.get("entities", []))
        + len(package.get("relationships", []))
        + len(package.get("events", []))
        + len(package.get("roles", [])),
    )
    candidate_constraint = min(output_size / package_size, 1.0)
    evidence_items = 0
    for section in ("entities", "relationships", "events", "roles"):
        for item in package.get(section, []):
            if item.get("evidence"):
                evidence_items += 1
    evidence_coverage = min(evidence_items / package_size, 1.0)
    compactness = 1.0 / (1.0 + max(0, output_size - 48) / 48.0)
    structural_consistency = 1.0 if entity_count and relationship_count else 0.5 if entity_count else 0.0

    return {
        "json_validity": json_validity,
        "candidate_constraint": candidate_constraint,
        "evidence_coverage": evidence_coverage,
        "compactness": compactness,
        "structural_consistency": structural_consistency,
    }


def weighted_reward(reward_terms: Dict[str, float], reward_weights: Dict[str, float] | None = None) -> float:
    weights = dict(DEFAULT_REWARD_WEIGHTS)
    if reward_weights:
        weights.update(reward_weights)
    return sum(weights.get(term, 0.0) * reward_terms.get(term, 0.0) for term in REWARD_TERMS)


def train_policy(
    packages: Sequence[Dict[str, Any]],
    epochs: int = 3,
    reward_weights: Dict[str, float] | None = None,
) -> Dict[str, Any]:
    if not packages:
        raise ValueError("At least one candidate package is required.")
    policy_weights = dict(DEFAULT_POLICY_WEIGHTS)
    weights = dict(DEFAULT_REWARD_WEIGHTS)
    if reward_weights:
        weights.update(reward_weights)

    trace: List[Dict[str, Any]] = []
    epochs = max(1, int(epochs))
    for epoch in range(epochs):
        rewards: List[float] = []
        for package in packages:
            schema = infer_schema(package, {"policy_weights": policy_weights})
            terms = score_contract_reward(schema, package)
            rewards.append(weighted_reward(terms, weights))
        mean_reward = sum(rewards) / len(rewards)
        policy_weights["evidence_count"] += 0.01 * mean_reward
        policy_weights["support"] += 0.005 * mean_reward
        policy_weights["label_length"] -= 0.002 * (1.0 - mean_reward)
        trace.append({"epoch": epoch + 1, "mean_reward": round(mean_reward, 6)})

    return {
        "schema": "scion_rl_policy_v1",
        "algorithm": "deterministic_reward_shaped_candidate_policy",
        "paper_rl_target": "offline_ppo_qwen3_8b_not_bundled",
        "reward_terms": REWARD_TERMS,
        "reward_weights": weights,
        "policy_weights": policy_weights,
        "training_trace": trace,
    }


def _load_packages(paths: Iterable[str]) -> List[Dict[str, Any]]:
    return [load_candidate_package(path) for path in paths]


def _cmd_train(args: argparse.Namespace) -> None:
    packages = _load_packages(args.candidate_package)
    policy = train_policy(packages, epochs=args.epochs)
    _write_json(args.output_policy, policy)


def _cmd_infer(args: argparse.Namespace) -> None:
    package = load_candidate_package(args.candidate_package)
    policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
    schema = infer_schema(
        package,
        policy,
        max_entities=args.max_entities,
        max_relationships=args.max_relationships,
        max_events=args.max_events,
    )
    _write_json(args.output_schema, schema)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the native lightweight SCION-RL contract policy.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train", help="Train a deterministic policy from candidate packages.")
    train.add_argument("--candidate-package", action="append", required=True, help="Path to a SCION candidate package JSON.")
    train.add_argument("--output-policy", required=True, help="Where to write the policy JSON.")
    train.add_argument("--epochs", type=int, default=3)
    train.set_defaults(func=_cmd_train)

    infer = subparsers.add_parser("infer", help="Infer a schema from one candidate package and a policy JSON.")
    infer.add_argument("--candidate-package", required=True, help="Path to a SCION candidate package JSON.")
    infer.add_argument("--policy", required=True, help="Path to a SCION-RL policy JSON.")
    infer.add_argument("--output-schema", required=True, help="Where to write the induced schema JSON.")
    infer.add_argument("--max-entities", type=int, default=16)
    infer.add_argument("--max-relationships", type=int, default=24)
    infer.add_argument("--max-events", type=int, default=12)
    infer.set_defaults(func=_cmd_infer)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
