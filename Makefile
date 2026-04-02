.PHONY: bootstrap doctor audit generate-summary test check-json verify-root-edge build-pdf prepare-w33-bundle

bootstrap:
	./scripts/bootstrap_repo_env.sh

doctor:
	python3 tools/repo_doctor.py

audit:
	python3 tools/repo_cleanup_audit.py

generate-summary:
	python scripts/collect_results.py
ifdef ALLOW_PARTIAL
	python scripts/make_numeric_comparisons_from_summary.py || true
else
	python scripts/make_numeric_comparisons_from_summary.py
endif

# Run tests after generating summary artifacts
test: generate-summary
	pytest -q

check-json:
	python -m pytest -q tests/test_json_serialization.py tests/test_json_safe.py -q

verify-root-edge:
	./scripts/verify_root_edge_mapping.sh

build-pdf:
	./scripts/build_toe_pdf.sh

prepare-w33-bundle:
	python tools/prepare_w33_analysis_bundle.py --bundle-dir artifacts/bundles/W33_Heisenberg_action_bundle_20260209_v1 --out-dir analysis/w33_bundle_temp --v0 0
