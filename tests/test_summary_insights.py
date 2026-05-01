import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_JSON = ROOT / "archive" / "json"


from src.summary_insights import collect_key_result_stats  # noqa: E402
from src.summary_insights import (
    compute_numeric_comparison_stats,
    load_numeric_comparisons,
    load_summary_results,
)


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    joined = ", ".join(str(path) for path in paths)
    raise FileNotFoundError(f"None of the expected fixtures exist: {joined}")


def _summary_results_path() -> Path:
    return _first_existing(
        ROOT / "SUMMARY_RESULTS.json",
        ARCHIVE_JSON / "SUMMARY_RESULTS.json",
    )


def _numeric_comparisons_path() -> Path:
    return _first_existing(
        ROOT / "NUMERIC_COMPARISONS.json",
        ARCHIVE_JSON / "NUMERIC_COMPARISONS.json",
    )


def test_key_result_stats():
    summary_results = load_summary_results(_summary_results_path())
    summaries = summary_results.get("summaries", {})
    stats = collect_key_result_stats(summaries)
    assert stats["total_parts"] >= 1
    assert stats["total_predictions"] >= 0
    assert stats["parts_with_key_results"] >= 0
    assert stats["key_result_entries"] >= 0
    assert isinstance(stats["parameter_usage"], dict)


def test_numeric_comparison_stats():
    numeric_entries = load_numeric_comparisons(_numeric_comparisons_path())
    stats = compute_numeric_comparison_stats(numeric_entries)
    assert stats.count == len(numeric_entries)
    assert stats.mean_abs_diff >= 0
    assert stats.max_abs_diff >= 0


def main():
    sys.path.append(str(ROOT))


if __name__ == "__main__":
    main()
