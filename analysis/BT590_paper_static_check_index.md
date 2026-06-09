# BT590 - End-to-End Paper Static Check Index

This index records the current paper-support/check pipeline and the intended run order.

## Primary target

```text
paper/w33_preprint.tex
```

## Script and artifact order

1. BT574 static verifier

```bash
python analysis/bt574_latex_sanity_verifier.py
```

Purpose: statically checks the W33 preprint section insertion, required formulas, local inputs, and basic LaTeX balance.

2. BT578 build harness, static mode

```bash
python tools/build_w33_preprint.py
```

Purpose: runs the static verifier when available and performs direct document-token checks.

3. BT578 build harness, optional compile mode

```bash
python tools/build_w33_preprint.py --compile
```

Purpose: after static checks, attempts `latexmk -pdf`; if unavailable, falls back to two `pdflatex` passes. If no TeX compiler is installed, it exits cleanly after explaining what is missing.

4. BT581 static hook

```bash
bash tools/check_w33_preprint_static.sh
```

Purpose: repository-root wrapper around the BT578 static build harness.

5. BT584 workflow template

```text
analysis/BT584_preprint_static_check_workflow_template.yml
```

Purpose: CI-ready workflow template that calls the BT581 hook.

6. BT587 workflow installer

```bash
python tools/install_preprint_workflow.py
```

Purpose: in a local checkout, copies the BT584 template to `.github/workflows/w33-preprint-static-check.yml`.

## New paper inserts

BT588 leakage-ratio insert:

```text
analysis/BT588_leakage_table_latex_insert.tex
```

BT589 homology-separation insert:

```text
analysis/BT589_homology_separation_latex_insert.tex
```

## Recommended manual sequence

```bash
python analysis/bt574_latex_sanity_verifier.py
python tools/build_w33_preprint.py
bash tools/check_w33_preprint_static.sh
python tools/build_w33_preprint.py --compile
```

The compile step is optional and depends on local TeX availability.

## Boundary

This index is an execution manifest. It does not prove that a local machine has a TeX distribution installed, and it does not replace the mathematical verifiers attached to each breakthrough theorem.
