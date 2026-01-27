#!/usr/bin/env pwsh

# Generate SUMMARY_RESULTS.json and (optionally) NUMERIC_COMPARISONS.json
python scripts/collect_results.py
try {
  python scripts/make_numeric_comparisons_from_summary.py
} catch {
  Write-Host "make_numeric_comparisons_from_summary.py failed or no numeric comparisons; continuing"
}
Write-Host "Generated SUMMARY_RESULTS.json and (optionally) NUMERIC_COMPARISONS.json"