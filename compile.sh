#!/usr/bin/env bash
# compile.sh -- Build W36_PAPER.pdf from source
# Requires: pdflatex, bibtex, inkscape >= 1.0

set -euo pipefail

echo "=== W(3,3) Theory Paper -- Build Script ==="
echo ""

# ── Step 1: Convert SVG figures to PDF ─────────────────────────────────────
echo "[1/4] Converting SVG figures to PDF via Inkscape..."
if command -v inkscape &>/dev/null; then
  for svg in figures/*.svg; do
    pdf="${svg%.svg}.pdf"
    echo "      $svg -> $pdf"
    inkscape "$svg" --export-filename="$pdf"
  done
  echo "      Done."
else
  echo "      WARNING: inkscape not found. Skipping SVG conversion."
  echo "      The \\includesvg macro requires Inkscape on PATH."
  echo "      Alternatively, convert SVGs manually and use \\includegraphics."
fi

echo ""

# ── Step 2: First pdflatex pass ────────────────────────────────────────────
echo "[2/4] First pdflatex pass..."
pdflatex -interaction=nonstopmode W36_PAPER.tex

echo ""

# ── Step 3: BibTeX ─────────────────────────────────────────────────────────
echo "[3/4] Running bibtex..."
bibtex W36_PAPER || true   # tolerate missing .bib entries

echo ""

# ── Step 4: Two more pdflatex passes (resolve refs) ────────────────────────
echo "[4/4] Final pdflatex passes (x2)..."
pdflatex -interaction=nonstopmode W36_PAPER.tex
pdflatex -interaction=nonstopmode W36_PAPER.tex

echo ""
echo "=== Build complete: W36_PAPER.pdf ==="
echo ""

# ── Word-count estimate ────────────────────────────────────────────────────
if command -v texcount &>/dev/null; then
  echo "Word count:"
  texcount W36_PAPER.tex 2>/dev/null | grep "Words in text"
fi
