#!/usr/bin/env bash
set -euo pipefail

python scripts/collect_results.py
python scripts/make_numeric_comparisons_from_summary.py || true

echo "Generated SUMMARY_RESULTS.json and NUMERIC_COMPARISONS.json (if available)"
