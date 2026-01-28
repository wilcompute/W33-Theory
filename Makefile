.PHONY: generate-summary test check-json verify-root-edge build-pdf

generate-summary:
	python scripts/collect_results.py
	python scripts/make_numeric_comparisons_from_summary.py || true

# Run tests after generating summary artifacts
test: generate-summary
	pytest -q

check-json:
	python -m pytest -q tests/test_json_serialization.py tests/test_json_safe.py -q

verify-root-edge:
	./scripts/verify_root_edge_mapping.sh

build-pdf:
	./scripts/build_toe_pdf.sh
