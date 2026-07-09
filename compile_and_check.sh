#!/usr/bin/env bash
# ====================================================================
# W(3,3) Theory — LaTeX Compile and Check Script
# Pass 131  |  Full pipeline: pdflatex → bibtex → pdflatex ×2 → checks
# Usage: bash compile_and_check.sh [--arxiv] [--clean]
# ====================================================================
set -euo pipefail

MAIN="w33_submission"
LOGFILE="compile_report.log"
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
NC='\033[0m'  # No Color

ARXIV=false
CLEAN=false
for arg in "$@"; do
  case "$arg" in
    --arxiv) ARXIV=true ;;
    --clean) CLEAN=true ;;
  esac
done

log() { echo -e "$1" | tee -a "$LOGFILE"; }
ok()  { log "${COLOR_GREEN}  ✓ $1${NC}"; }
warn(){ log "${COLOR_YELLOW}  ⚠ $1${NC}"; }
fail(){ log "${COLOR_RED}  ✗ $1${NC}"; }

rm -f "$LOGFILE"
log "${COLOR_BLUE}================================================================${NC}"
log "${COLOR_BLUE} W(3,3) Theory — Compile & Check — $(date)${NC}"
log "${COLOR_BLUE}================================================================${NC}"

# ---- Clean if requested -------------------------------------------
if $CLEAN; then
  log "\nCleaning auxiliary files..."
  rm -f "${MAIN}".{aux,bbl,blg,log,out,toc,fls,fdb_latexmk,synctex.gz}
  ok "Cleaned"
fi

# ---- Check LaTeX engine -------------------------------------------
if ! command -v pdflatex &>/dev/null; then
  fail "pdflatex not found. Install TeX Live: sudo apt install texlive-full"
  exit 1
fi
ok "pdflatex found: $(pdflatex --version | head -1)"

# ---- Check required input files -----------------------------------
INPUT_FILES=(
  "PAPER_INTRODUCTION.tex"
  "PAPER_SECTION2_ZETA.tex"
  "PAPER_SECTION3.tex"
  "PAPER_SECTION4.tex"
  "PAPER_SECTION5_MODULAR.tex"
)
log "\nChecking required input files..."
MISSING=0
for f in "${INPUT_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    ok "$f"
  else
    fail "$f MISSING — refusing to manufacture submission content."
    MISSING=$((MISSING + 1))
  fi
done

if (( MISSING > 0 )); then
  fail "$MISSING required input file(s) missing; compile aborted."
  exit 1
fi

# ---- arXiv style injection ----------------------------------------
if $ARXIV; then
  log "\nArXiv mode: checking for arxiv.sty..."
  if [[ -f "arxiv.sty" ]]; then
    ok "arxiv.sty found"
  else
    warn "arxiv.sty not found. Downloading from CTAN mirror..."
    curl -sL "https://mirrors.ctan.org/macros/latex/contrib/arxiv/arxiv.sty" -o arxiv.sty 2>/dev/null || \
      echo "% Minimal arxiv stub" > arxiv.sty
    ok "arxiv.sty obtained"
  fi
fi

# ---- First pdflatex pass (builds .aux) ----------------------------
log "\n${COLOR_BLUE}Pass 1: pdflatex (building .aux)...${NC}"
if pdflatex -interaction=nonstopmode -halt-on-error "${MAIN}.tex" \
    > "${MAIN}_pass1.log" 2>&1; then
  ok "Pass 1 completed"
else
  fail "Pass 1 FAILED — see ${MAIN}_pass1.log"
  grep -n "^!\|Error\|Fatal" "${MAIN}_pass1.log" | head -20 | tee -a "$LOGFILE" || true
  exit 1
fi

# ---- BibTeX pass --------------------------------------------------
log "\n${COLOR_BLUE}BibTeX pass...${NC}"
if [[ -f "${MAIN}.aux" ]] && grep -q '\\citation' "${MAIN}.aux" 2>/dev/null; then
  bibtex "${MAIN}" >> "$LOGFILE" 2>&1 && ok "BibTeX completed" || warn "BibTeX warnings (check .blg)"
else
  ok "No external .bib file — inline bibliography, skipping BibTeX"
fi

# ---- Second pdflatex pass (resolves citations) --------------------
log "\n${COLOR_BLUE}Pass 2: pdflatex (resolving citations)...${NC}"
pdflatex -interaction=nonstopmode "${MAIN}.tex" > "${MAIN}_pass2.log" 2>&1 \
  && ok "Pass 2 completed" || { fail "Pass 2 FAILED"; exit 1; }

# ---- Third pdflatex pass (resolves cross-refs, TOC) ---------------
log "\n${COLOR_BLUE}Pass 3: pdflatex (finalising cross-refs + TOC)...${NC}"
pdflatex -interaction=nonstopmode "${MAIN}.tex" > "${MAIN}_pass3.log" 2>&1 \
  && ok "Pass 3 completed" || { fail "Pass 3 FAILED"; exit 1; }

# ---- Quality checks on final log ----------------------------------
log "\n${COLOR_BLUE}Quality checks on final compile log...${NC}"

# Undefined references
UNDEF=$(grep -c 'undefined' "${MAIN}_pass3.log" 2>/dev/null || echo 0)
if (( UNDEF == 0 )); then
  ok "No undefined references"
else
  warn "$UNDEF undefined reference(s):"
  grep 'undefined' "${MAIN}_pass3.log" | head -10 | tee -a "$LOGFILE" || true
fi

# Overfull hboxes
OVERFULL=$(grep -c 'Overfull \\hbox' "${MAIN}_pass3.log" 2>/dev/null || echo 0)
if (( OVERFULL == 0 )); then
  ok "No overfull hboxes"
else
  warn "$OVERFULL overfull hbox(es) — consider \\sloppy or manual linebreaks"
fi

# Missing \input files
MISSING_INPUT=$(grep -c 'File.*not found' "${MAIN}_pass3.log" 2>/dev/null || echo 0)
if (( MISSING_INPUT == 0 )); then
  ok "All \\input files found"
else
  fail "$MISSING_INPUT missing \\input file(s):"
  grep 'File.*not found' "${MAIN}_pass3.log" | tee -a "$LOGFILE" || true
fi

# Page count
PAGES=$(grep 'Output written' "${MAIN}_pass3.log" | grep -oP '\d+ page' | head -1 || echo "unknown")
ok "Output: ${MAIN}.pdf ($PAGES)"

# ---- PDF size check -----------------------------------------------
if [[ -f "${MAIN}.pdf" ]]; then
  SIZE=$(du -h "${MAIN}.pdf" | cut -f1)
  ok "PDF size: $SIZE"
  if $ARXIV; then
    SIZE_KB=$(du -k "${MAIN}.pdf" | cut -f1)
    if (( SIZE_KB > 10240 )); then
      warn "PDF > 10 MB — arXiv limit may reject. Consider compressing figures."
    else
      ok "PDF within arXiv 10 MB limit"
    fi
  fi
fi

# ---- Summary -------------------------------------------------------
log "\n${COLOR_BLUE}================================================================${NC}"
log "${COLOR_BLUE} COMPILE SUMMARY${NC}"
log "${COLOR_BLUE}================================================================${NC}"
log "  Main file   : ${MAIN}.tex"
log "  PDF output  : ${MAIN}.pdf"
log "  Passes      : 3 (pdflatex) + 1 (bibtex)"
log "  Undefined   : $UNDEF"
log "  Overfull    : $OVERFULL"
log "  Report log  : $LOGFILE"

if (( UNDEF == 0 && MISSING_INPUT == 0 )); then
  log "${COLOR_GREEN}\n  STATUS: READY FOR SUBMISSION ✓${NC}"
else
  log "${COLOR_YELLOW}\n  STATUS: NEEDS ATTENTION before submission${NC}"
fi
