#!/usr/bin/env bash
# BT1886 — run the dual Holonet TeX splice and perform local sanity checks.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 tools/apply_bt1857_holonet_patch.py
OUT="papers/BT1347_photonic_holonet_journal_with_BT1857_BT1880.tex"

if [[ ! -f "$OUT" ]]; then
  echo "BT1886 FAIL: expected output missing: $OUT" >&2
  exit 1
fi

grep -q "sec:k12-f12-compiler" "$OUT"
grep -q "sec:k12-f12-css-code" "$OUT"

if grep -q "begin{enumerate}\[nosep\]" "$OUT"; then
  echo "BT1886 FAIL: enumitem-only option found" >&2
  exit 1
fi

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$OUT"
  echo "BT1886 latexmk compile passed"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error "$OUT"
  echo "BT1886 pdflatex compile passed"
else
  echo "BT1886 TeX syntax checks passed; no TeX engine found for PDF compile"
fi
