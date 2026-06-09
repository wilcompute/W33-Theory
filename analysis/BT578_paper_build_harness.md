# BT578 - Paper Build Harness

Added `tools/build_w33_preprint.py`.

Default mode runs static checks only:

```bash
python tools/build_w33_preprint.py
```

Compile mode first runs the static checks, then attempts to build the PDF if a local TeX toolchain is available:

```bash
python tools/build_w33_preprint.py --compile
```

Compiler order:

1. `latexmk -pdf`
2. `pdflatex` twice

If neither compiler is installed, the harness exits cleanly after explaining what is missing.

The harness delegates to `analysis/bt574_latex_sanity_verifier.py` when present, then performs a few direct token checks against `paper/w33_preprint.tex`.
