from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.summary_insights import collect_key_result_stats  # noqa: E402
from src.summary_insights import (compute_numeric_comparison_stats,
                                  load_numeric_comparisons,
                                  load_summary_results)


def build_report(root: Path) -> str:
    summary_path = root / "SUMMARY_RESULTS.json"
    numeric_path = root / "NUMERIC_COMPARISONS.json"

    summary_results = load_summary_results(summary_path)
    summaries = summary_results.get("summaries", {})
    key_stats = collect_key_result_stats(summaries)

    numeric_entries = load_numeric_comparisons(numeric_path)
    numeric_stats = compute_numeric_comparison_stats(numeric_entries)

    lines = [
        "# W33 Summary Consistency Audit",
        "",
        "## Coverage",
        f"- Parts scanned: {key_stats['total_parts']}",
        f"- Parts with key results: {key_stats['parts_with_key_results']}",
        f"- Key result entries: {key_stats['key_result_entries']}",
        f"- Total predictions listed: {key_stats['total_predictions']}",
        "",
        "## Numeric Comparison Stats",
        f"- Entries: {numeric_stats.count}",
        f"- Mean |diff|: {numeric_stats.mean_abs_diff:.6f}",
        f"- Max |diff|: {numeric_stats.max_abs_diff:.6f}",
        "",
        "## W33 Parameter Coverage",
    ]

    for name, count in key_stats["parameter_usage"].items():
        lines.append(f"- {name}: {count} parts")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit W33 summary consistency.")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root containing SUMMARY_RESULTS.json",
    )
    args = parser.parse_args()
    report = build_report(args.root)
    print(report)


if __name__ == "__main__":
    main()
