#!/usr/bin/env bash
# BT1866 — run the BT1863 Holonet TeX splice and perform local sanity checks.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 tools/apply_bt1857_holonet_patch.py
OUT="papers/BT1347_photonic_holonet_journal_with_BT1857.tex"

if [[ ! -f "$OUT" ]]; then
  echo "BT1866 FAIL: expected output missing: $OUT" >&2
  exit 1
fi

grep -q "sec:k12-f12-compiler" "$OUT"
grep -q "Raw code distance" "$OUT"
if grep -q "begin{enumerate}\[nosep\]" "$OUT"; then
  echo "BT1866 FAIL: enumitem-only [nosep] option found" >&2
  exit 1
fi

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$OUT"
  echo "BT1866 latexmk compile passed"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error "$OUT"
  echo "BT1866 pdflatex compile passed"
else
  echo "BT1866 TeX syntax checks passed; no TeX engine found for PDF compile"
fi
