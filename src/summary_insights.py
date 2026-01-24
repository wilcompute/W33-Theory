from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


@dataclass(frozen=True)
class NumericComparisonStats:
    count: int
    mean_abs_diff: float
    max_abs_diff: float


def _ensure_path(path: Path | str) -> Path:
    return path if isinstance(path, Path) else Path(path)


def load_summary_results(path: Path | str) -> dict[str, Any]:
    path = _ensure_path(path)
    return json.loads(path.read_text())


def load_numeric_comparisons(path: Path | str) -> list[dict[str, Any]]:
    path = _ensure_path(path)
    return json.loads(path.read_text())


def _count_key_results_entries(key_results: Any) -> int:
    if key_results is None:
        return 0
    if isinstance(key_results, dict):
        return len(key_results)
    if isinstance(key_results, list):
        return len(key_results)
    return 1


def collect_key_result_stats(summaries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    total_parts = len(summaries)
    total_predictions = 0
    parts_with_key_results = 0
    key_result_entries = 0
    parameter_usage: dict[str, int] = {}

    for meta in summaries.values():
        total_predictions += int(meta.get("predictions_total") or 0)
        key_results = meta.get("key_results")
        if key_results:
            parts_with_key_results += 1
        key_result_entries += _count_key_results_entries(key_results)

        parameters = meta.get("w33_parameters") or {}
        if isinstance(parameters, dict):
            for name in parameters:
                parameter_usage[name] = parameter_usage.get(name, 0) + 1

    return {
        "total_parts": total_parts,
        "total_predictions": total_predictions,
        "parts_with_key_results": parts_with_key_results,
        "key_result_entries": key_result_entries,
        "parameter_usage": dict(sorted(parameter_usage.items())),
    }


def compute_numeric_comparison_stats(entries: Iterable[dict[str, Any]]) -> NumericComparisonStats:
    diffs = [abs(float(entry["diff"])) for entry in entries if "diff" in entry]
    if not diffs:
        return NumericComparisonStats(count=0, mean_abs_diff=0.0, max_abs_diff=0.0)
    return NumericComparisonStats(
        count=len(diffs),
        mean_abs_diff=mean(diffs),
        max_abs_diff=max(diffs),
    )
