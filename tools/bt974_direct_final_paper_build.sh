#!/usr/bin/env bash
set -euo pipefail
export TEXINPUTS=".:./manuscripts/tex:${TEXINPUTS:-}:"

python tools/integrate_bt942_selector_appendix_w33.py
python tools/integrate_bt952_exact_selector_w33.py
python tools/integrate_bt957_final_selector_w33.py
python tools/integrate_bt967_selector_rails_w33.py
python tools/integrate_bt973_rail_generation_phase_w33.py
python tools/integrate_bt1134_w33_paper.py
python tools/integrate_bt1139_w33_paper_k3_a4.py
python tools/integrate_bt1142_w33_paper_a4_table.py
python tools/integrate_bt1145_w33_metric_bridge.py
python tools/integrate_bt1147_w33_matrix_derivation.py
python tools/integrate_bt1148_w33_weyl_split.py
python tools/integrate_bt1149_w33_orientation.py
python tools/integrate_bt1150_w33_hyperkahler.py
python tools/integrate_bt1151_w33_15sector.py
python tools/integrate_bt1154_w33_projective15_refinement.py
python tools/integrate_bt949_holonet_w33_crossref.py
python tools/integrate_bt958_holonet_final_selector_pointer.py
python tools/integrate_bt967_holonet_selector_rails.py
python tools/integrate_bt1136_holonet_product_heat_pointer.py

python -m pytest -q tests/test_bt1133_finite_heat_moments.py tests/test_bt1134_paper_integration.py tests/test_bt1138_k3_a4_normalization.py tests/test_bt1139_k3_a4_paper_integration.py tests/test_bt1140_seeley_dewitt_a4_convention_split.py tests/test_bt1141_spin_hodge_a4_coefficients.py tests/test_bt1142_a4_convention_table_paper_integration.py tests/test_bt1143_curvature_matrix_verifier.py tests/test_bt1144_w33_finite_carrier_alignment.py tests/test_bt1145_metric_bridge_integration.py tests/test_bt1146_random_weyl_result.py tests/test_bt1147_matrix_derivation_integration.py tests/test_bt1148_k3_weyl_signature_split.py tests/test_bt1148_weyl_split_integration.py tests/test_bt1149_k3_orientation_convention.py tests/test_bt1151_tau15_pg32_sector.py tests/test_bt1152_projector_refinement.py tests/test_bt1153_clifford_completion.py tests/test_bt1154_projective15_refinement.py

pdflatex -interaction=nonstopmode w33_paper.tex
pdflatex -interaction=nonstopmode w33_paper.tex
pdflatex -interaction=nonstopmode photonic_holonet.tex
pdflatex -interaction=nonstopmode photonic_holonet.tex

mkdir -p build_artifacts
cp -f w33_paper.pdf build_artifacts/ 2>/dev/null || true
cp -f photonic_holonet.pdf build_artifacts/ 2>/dev/null || true
cp -f *.log build_artifacts/ 2>/dev/null || true
sha256sum build_artifacts/* > build_artifacts/SHA256SUMS.txt 2>/dev/null || true
