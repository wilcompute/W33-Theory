.PHONY: generate-summary test

generate-summary:
	python scripts/collect_results.py
	python scripts/make_numeric_comparisons_from_summary.py || true

# Run tests after generating summary artifacts
test: generate-summary
	pytest -q

check-json:
	python -m pytest -q tests/test_json_serialization.py tests/test_json_safe.py -q

