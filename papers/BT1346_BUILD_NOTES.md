# BT1346 — arXiv Build Notes

This file accompanies `papers/BT1346_photonic_holonet_accessible.tex`.

## Purpose

This is the LaTeX / arXiv-style version of the accessible Photonic Holonet paper.
It is intended to turn BT1345 into a submission-ready manuscript skeleton.

## Build

```bash
cd papers
pdflatex BT1346_photonic_holonet_accessible.tex
pdflatex BT1346_photonic_holonet_accessible.tex
```

If `physics.sty` is unavailable in the local TeX distribution, remove:

```latex
\usepackage{physics}
```

and replace `\ket{...}` with ordinary math notation as needed.

## Companion files

- `papers/BT1345_photonic_holonet_accessible.md` — readable markdown version
- `papers/BT1346_photonic_holonet_accessible.tex` — LaTeX version
- `proofs/BT1344_lab_README.md` — lab-facing witness-to-experiment map
- `proofs/bt1343_unified_witness_runner.py` — unified executable witness chain

## Next natural step

A likely BT1347 is a shorter journal-style version: 6–10 pages, tighter theorem structure,
minimal glossary, and direct embedding of the numerical witness table.
