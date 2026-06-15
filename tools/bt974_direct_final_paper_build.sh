#!/usr/bin/env bash
set -euo pipefail

# w33_paper.tex pulls in \input{partN_*} files that live in manuscripts/tex/.
# Expose that directory to kpathsea so the master manuscript resolves its
# includes (trailing ':' keeps the default search paths). Without this,
# pdflatex halts at "part5_unified_breakthrough.tex not found".
export TEXINPUTS=".:./manuscripts/tex:${TEXINPUTS:-}:"

python tools/integrate_bt942_selector_appendix_w33.py
python tools/integrate_bt952_exact_selector_w33.py
python tools/integrate_bt957_final_selector_w33.py
python tools/integrate_bt967_selector_rails_w33.py
python tools/integrate_bt973_rail_generation_phase_w33.py
python tools/integrate_bt1134_w33_paper.py
python tools/integrate_bt949_holonet_w33_crossref.py
python tools/integrate_bt958_holonet_final_selector_pointer.py
python tools/integrate_bt967_holonet_selector_rails.py
python tools/integrate_bt1136_holonet_product_heat_pointer.py

python -m pytest -q \
  tests/test_bt1133_finite_heat_moments.py \
  tests/test_bt1134_paper_integration.py

pdflatex -interaction=nonstopmode w33_paper.tex
pdflatex -interaction=nonstopmode w33_paper.tex
pdflatex -interaction=nonstopmode photonic_holonet.tex
pdflatex -interaction=nonstopmode photonic_holonet.tex

mkdir -p build_artifacts
cp -f w33_paper.pdf build_artifacts/ 2>/dev/null || true
cp -f photonic_holonet.pdf build_artifacts/ 2>/dev/null || true
cp -f *.log build_artifacts/ 2>/dev/null || true
sha256sum build_artifacts/* > build_artifacts/SHA256SUMS.txt 2>/dev/null || true
