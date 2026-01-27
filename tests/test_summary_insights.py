from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))


from src.summary_insights import (  # noqa: E402
    collect_key_result_stats,
    compute_numeric_comparison_stats,
    load_numeric_comparisons,
    load_summary_results,
)


def test_key_result_stats():
    summary_results = load_summary_results(ROOT / "SUMMARY_RESULTS.json")
    summaries = summary_results.get("summaries", {})
    stats = collect_key_result_stats(summaries)
    assert stats["total_parts"] >= 1
    assert stats["total_predictions"] >= 0
    assert stats["parts_with_key_results"] >= 0
    assert stats["key_result_entries"] >= 0
    assert isinstance(stats["parameter_usage"], dict)


def test_numeric_comparison_stats():
    numeric_entries = load_numeric_comparisons(ROOT / "NUMERIC_COMPARISONS.json")
    stats = compute_numeric_comparison_stats(numeric_entries)
    assert stats.count == len(numeric_entries)
    assert stats.mean_abs_diff >= 0
    assert stats.max_abs_diff >= 0
