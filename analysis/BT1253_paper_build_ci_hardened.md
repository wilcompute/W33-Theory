# BT1253 — paper-build CI: Full LaTeX Hardening
**Date:** 2026-06-17  
**Status:** DEPLOYED ✓

## What Changed
The `.github/workflows/paper-build.yml` workflow was fully hardened:

1. **3-pass pdflatex** (+ bibtex between passes 1 and 2) to resolve all cross-references and citations.
2. **Error gate:** `grep 'Error' w33_preprint.log && exit 1` — any LaTeX error now fails the CI job hard.
3. **Undefined reference warning:** `grep 'undefined'` now prints warnings but does not block (allows iterative fixing).
4. **PDF existence check:** CI fails if `w33_preprint.pdf` is not produced.
5. **Artifact upload:** The compiled PDF is uploaded as a 90-day retained artifact on every master push.

## Trigger Conditions
- Push to master touching any `.tex` or `.bib` file
- Pull requests touching `.tex` or `.bib`
- Manual `workflow_dispatch`

## Status
Workflow deployed. Will fire on next `.tex` commit. Monitor at:
https://github.com/wilcompute/W33-Theory/actions/workflows/paper-build.yml
