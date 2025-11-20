"""命令行工具：对比预测与金标准本体，输出多种评测指标。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

from utils.ontology_eval import compute_ontology_metrics, load_schema_file, schema_dict_to_graph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="评估两个本体文件之间的一致性指标。")
    parser.add_argument("--gold_onto", required=True, help="金标准本体 JSON 文件路径")
    parser.add_argument("--pred_onto", required=True, help="预测/待评测的本体 JSON 文件路径")
    parser.add_argument(
        "--emb_model",
        default="BAAI/bge-large-zh-v1.5",
        help="sentence-transformers 模型名称 (默认: BAAI/bge-large-zh-v1.5)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.45,
        help="Fuzzy F1 阈值，判断两节点是否语义匹配 (默认: 0.45)",
    )
    parser.add_argument(
        "--graph_smoothing_rounds",
        type=int,
        default=2,
        help="Graph F1 中图平滑的迭代次数 (默认: 2)",
    )
    parser.add_argument(
        "--graph_smoothing_alpha",
        type=float,
        default=0.5,
        help="Graph F1 中残差权重 alpha (默认: 0.5)",
    )
    parser.add_argument(
        "--output_json",
        type=str,
        default=None,
        help="若指定，则把指标写入该 JSON 文件",
    )
    return parser.parse_args()


def write_metrics(path: Path, metrics: Dict[str, Dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    gold_schema = load_schema_file(args.gold_onto)
    pred_schema = load_schema_file(args.pred_onto)

    gold_graph = schema_dict_to_graph(gold_schema)
    pred_graph = schema_dict_to_graph(pred_schema)

    metrics = compute_ontology_metrics(
        gold_graph=gold_graph,
        pred_graph=pred_graph,
        emb_model=args.emb_model,
        threshold=args.threshold,
        graph_smoothing_rounds=args.graph_smoothing_rounds,
        graph_smoothing_alpha=args.graph_smoothing_alpha,
    )

    for name, result in metrics.items():
        print(
            f"[{name}] Precision={result['precision']:.4f} "
            f"Recall={result['recall']:.4f} F1={result['f1']:.4f}"
        )

    if args.output_json:
        write_metrics(Path(args.output_json), metrics)


if __name__ == "__main__":
    main()
