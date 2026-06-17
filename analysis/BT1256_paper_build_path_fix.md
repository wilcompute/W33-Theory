# BT1256 — paper-build CI: Path Fix (paper/ subdirectory)
**Date:** 2026-06-17  
**Status:** DEPLOYED ✓

## Issue
The previous `paper-build.yml` assumed `w33_preprint.tex` was in the repo root. The actual location is `paper/w33_preprint.tex` (confirmed by GitHub API path resolution in BT1253).

## Fix
- `working-directory` changed to `${{ github.workspace }}/paper` for all pdflatex/bibtex steps
- `paths:` trigger updated to `paper/**` (covers .tex, .bib, .sty, figures)
- Error detection changed from `grep 'Error'` to `grep -E '^!'` which catches actual LaTeX fatal errors (lines starting with `!`) without false-positives from section headers containing the word "Error"
- Artifact path updated to `paper/w33_preprint.pdf`

## Status
Workflow will fire on next push to `paper/**`. Monitor at:
https://github.com/wilcompute/W33-Theory/actions/workflows/paper-build.yml
