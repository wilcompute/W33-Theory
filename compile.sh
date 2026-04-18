#!/usr/bin/env bash
# =============================================================
#  W(3,3) Theory — arXiv Submission Build Script
#  Author: Wil Dahn  |  April 2026
#  Usage:  bash compile.sh [--arxiv]
# =============================================================
set -euo pipefail

PAPER="W36_PAPER"
FIGDIR="figures"

echo "================================================"
echo " W(3,3) Theory — Paper Build"
echo "================================================"

# ── Step 1: Convert SVG figures to PDF (requires Inkscape ≥ 1.0)
echo ""
echo "[1/4] Converting SVG figures to PDF..."
for svg in "${FIGDIR}"/*.svg; do
    base="${svg%.svg}"
    if command -v inkscape &>/dev/null; then
        inkscape "$svg" --export-filename="${base}.pdf" 2>/dev/null
        echo "      ✓  ${svg} → ${base}.pdf"
    else
        echo "      ⚠  Inkscape not found — skipping ${svg}"
        echo "         Install: https://inkscape.org/release/"
    fi
done

# ── Step 2: Patch \includesvg → \includegraphics for arXiv mode
if [[ "${1:-}" == "--arxiv" ]]; then
    echo ""
    echo "[2/4] Patching \\includesvg → \\includegraphics for arXiv..."
    cp "${PAPER}.tex" "${PAPER}_arxiv.tex"
    sed -i 's/\\includesvg\[/\\includegraphics[/g' "${PAPER}_arxiv.tex"
    TEXFILE="${PAPER}_arxiv"
    echo "      ✓  Created ${PAPER}_arxiv.tex"
else
    TEXFILE="${PAPER}"
fi

# ── Step 3: LaTeX triple-compile (resolves all cross-references)
echo ""
echo "[3/4] Compiling LaTeX (3 passes)..."
for pass in 1 2 3; do
    echo "      Pass ${pass}/3..."
    pdflatex -interaction=nonstopmode "${TEXFILE}.tex" > /dev/null
done
bibtex "${TEXFILE}" > /dev/null 2>&1 || true
pdflatex -interaction=nonstopmode "${TEXFILE}.tex" > /dev/null
pdflatex -interaction=nonstopmode "${TEXFILE}.tex" > /dev/null
echo "      ✓  ${TEXFILE}.pdf generated"

# ── Step 4: Build arXiv .tar.gz bundle
if [[ "${1:-}" == "--arxiv" ]]; then
    echo ""
    echo "[4/4] Building arXiv submission bundle..."
    BUNDLE="W33_Theory_Dahn_2026_arxiv"
    mkdir -p "${BUNDLE}"
    cp "${PAPER}_arxiv.tex" "${BUNDLE}/"
    cp "${PAPER}.bbl"       "${BUNDLE}/" 2>/dev/null || true
    mkdir -p "${BUNDLE}/figures"
    cp figures/*.pdf        "${BUNDLE}/figures/" 2>/dev/null || true
    cp figures/*.svg        "${BUNDLE}/figures/" 2>/dev/null || true
    tar -czf "${BUNDLE}.tar.gz" "${BUNDLE}/"
    rm -rf "${BUNDLE}/"
    echo "      ✓  ${BUNDLE}.tar.gz ready for arXiv upload"
    echo ""
    echo "================================================"
    echo " arXiv bundle: ${BUNDLE}.tar.gz"
    echo " Upload at:    https://arxiv.org/submit"
    echo "================================================"
else
    echo ""
    echo "================================================"
    echo " Output: ${TEXFILE}.pdf"
    echo " For arXiv bundle: bash compile.sh --arxiv"
    echo "================================================"
fi
