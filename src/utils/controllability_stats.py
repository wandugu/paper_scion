"""Controllability 统计相关结构与输出。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .common import resolve_project_path, save_json
from .logger import get_ot_logger


LOGGER = get_ot_logger()


@dataclass
class ControllabilityStats:
    candidate_entities: int = 0
    candidate_relationships: int = 0
    candidate_events: int = 0
    merged_entities: int = 0
    merged_relationships: int = 0
    merged_events: int = 0
    retained_entities: int = 0
    retained_relationships: int = 0
    retained_events: int = 0
    json_attempts: Dict[str, int] = field(default_factory=lambda: {"ontology": 0, "events": 0})
    json_success: Dict[str, int] = field(default_factory=lambda: {"ontology": 0, "events": 0})
    fallback_counts: Dict[str, int] = field(default_factory=lambda: {"ontology": 0, "events": 0})
    fallback_reasons: Dict[str, List[str]] = field(default_factory=lambda: {"ontology": [], "events": []})

    def record_json_attempt(self, section: str) -> None:
        if section in self.json_attempts:
            self.json_attempts[section] += 1
            LOGGER.debug("JSON 解析尝试计数: section=%s attempts=%s", section, self.json_attempts[section])

    def record_json_success(self, section: str) -> None:
        if section in self.json_success:
            self.json_success[section] += 1
            LOGGER.debug("JSON 解析成功计数: section=%s success=%s", section, self.json_success[section])

    def record_fallback(self, section: str, reason: str) -> None:
        if section in self.fallback_counts:
            self.fallback_counts[section] += 1
            if reason:
                self.fallback_reasons[section].append(reason)
            LOGGER.debug("Fallback 触发: section=%s reason=%s count=%s", section, reason, self.fallback_counts[section])

    def set_candidate_counts(self, entities: int, relationships: int, events: int) -> None:
        self.candidate_entities = entities
        self.candidate_relationships = relationships
        self.candidate_events = events

    def set_merge_counts(
        self,
        merged_entities: int,
        merged_relationships: int,
        merged_events: int,
        retained_entities: int,
        retained_relationships: int,
        retained_events: int,
    ) -> None:
        self.merged_entities = merged_entities
        self.merged_relationships = merged_relationships
        self.merged_events = merged_events
        self.retained_entities = retained_entities
        self.retained_relationships = retained_relationships
        self.retained_events = retained_events

    @staticmethod
    def _ratio(numerator: int, denominator: int) -> float:
        return round(numerator / denominator, 4) if denominator else 0.0

    def to_payload(self, dataset_name: str, fallback_note: Dict[str, str]) -> Dict[str, Any]:
        json_attempts_total = sum(self.json_attempts.values())
        json_success_total = sum(self.json_success.values())
        fallback_total = sum(self.fallback_counts.values())
        return {
            "dataset": dataset_name,
            "timestamp": datetime.utcnow().isoformat(),
            "candidate_counts": {
                "entities": self.candidate_entities,
                "relationships": self.candidate_relationships,
                "events": self.candidate_events,
            },
            "merged_counts": {
                "entities": self.merged_entities,
                "relationships": self.merged_relationships,
                "events": self.merged_events,
            },
            "retained_counts": {
                "entities": self.retained_entities,
                "relationships": self.retained_relationships,
                "events": self.retained_events,
            },
            "retained_ratio": {
                "entities": self._ratio(self.retained_entities, self.candidate_entities),
                "relationships": self._ratio(self.retained_relationships, self.candidate_relationships),
                "events": self._ratio(self.retained_events, self.candidate_events),
            },
            "merged_ratio": {
                "entities": self._ratio(self.candidate_entities - self.retained_entities, self.candidate_entities),
                "relationships": self._ratio(
                    self.candidate_relationships - self.retained_relationships, self.candidate_relationships
                ),
                "events": self._ratio(self.candidate_events - self.retained_events, self.candidate_events),
            },
            "json_parse": {
                "ontology": {
                    "attempts": self.json_attempts["ontology"],
                    "success": self.json_success["ontology"],
                    "success_rate": self._ratio(self.json_success["ontology"], self.json_attempts["ontology"]),
                },
                "events": {
                    "attempts": self.json_attempts["events"],
                    "success": self.json_success["events"],
                    "success_rate": self._ratio(self.json_success["events"], self.json_attempts["events"]),
                },
                "overall": {
                    "attempts": json_attempts_total,
                    "success": json_success_total,
                    "success_rate": self._ratio(json_success_total, json_attempts_total),
                },
            },
            "fallback": {
                "ontology": {
                    "count": self.fallback_counts["ontology"],
                    "rate": self._ratio(self.fallback_counts["ontology"], self.json_attempts["ontology"]),
                    "reasons": self.fallback_reasons["ontology"],
                },
                "events": {
                    "count": self.fallback_counts["events"],
                    "rate": self._ratio(self.fallback_counts["events"], self.json_attempts["events"]),
                    "reasons": self.fallback_reasons["events"],
                },
                "overall": {
                    "count": fallback_total,
                    "rate": self._ratio(fallback_total, json_attempts_total),
                },
            },
            "fallback_note": fallback_note,
        }


def _stats_cfg(config: Dict[str, Any]) -> Dict[str, Any]:
    stats = config.get("stats")
    return stats if isinstance(stats, dict) else {}


def controllability_enabled(config: Dict[str, Any]) -> bool:
    stats_cfg = _stats_cfg(config)
    if stats_cfg.get("enabled", True) is False:
        return False
    cfg = stats_cfg.get("controllability")
    if isinstance(cfg, dict):
        return bool(cfg.get("enabled", True))
    return True


def resolve_controllability_output_path(config: Dict[str, Any]) -> Path:
    stats_cfg = _stats_cfg(config)
    ctrl_cfg = stats_cfg.get("controllability") or {}
    output_dir = resolve_project_path(stats_cfg.get("output_dir", "data/dataset_stat"))
    filename = ctrl_cfg.get("filename", "controllability_stats.json") if isinstance(ctrl_cfg, dict) else "controllability_stats.json"
    return output_dir / filename


def controllability_fallback_note(config: Dict[str, Any]) -> Dict[str, str]:
    stats_cfg = _stats_cfg(config)
    ctrl_cfg = stats_cfg.get("controllability") or {}
    if not isinstance(ctrl_cfg, dict):
        return {}
    note_cfg = ctrl_cfg.get("fallback_note") or {}
    if not isinstance(note_cfg, dict):
        return {}
    return {str(key): str(value) for key, value in note_cfg.items()}


def write_controllability_stats(stats: ControllabilityStats, config: Dict[str, Any], dataset_name: str) -> None:
    if not controllability_enabled(config):
        return
    path = resolve_controllability_output_path(config)
    payload = stats.to_payload(dataset_name, controllability_fallback_note(config))
    save_json(path, payload)
    LOGGER.info("Controllability 统计已写入: %s", path)


__all__ = [
    "ControllabilityStats",
    "controllability_enabled",
    "resolve_controllability_output_path",
    "controllability_fallback_note",
    "write_controllability_stats",
]
