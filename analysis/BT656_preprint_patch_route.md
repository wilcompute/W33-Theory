# BT656 Preprint Patch Route

This closes the smaller accepted route for BT646/BT647 integration.

Existing helper checked against repo:

```text
tools/integrate_bt646_bt647_inserts.py
```

It reads:

```text
paper/w33_preprint.tex
```

and inserts the two section inputs before:

```tex
\section{The TOE Singularity Theorem}
```

The exact inputs are:

```tex
\input{sections/sec_bt646_internal_s4_hodge_clock}
\input{sections/sec_bt647_synthesis_bridge}
```

The helper is idempotent because it tests whether each input line is already
present before inserting it.

## Repo check

The section files already exist:

```text
paper/sections/sec_bt646_internal_s4_hodge_clock.tex
paper/sections/sec_bt647_synthesis_bridge.tex
```

The active preprint still has the TOE Singularity section immediately after the
Symmetry, Phase, and Cubic Leakage block, so the helper remains the correct patch
route.

## Run path

From a checkout:

```bash
python tools/integrate_bt646_bt647_inserts.py
python analysis/bt574_latex_sanity_verifier.py
python tools/build_w33_preprint.py --compile
```

## Boundary

The connector blocks full-file replacement of paper/w33_preprint.tex.  Therefore
BT656 records the smaller accepted patch route and verifies that the helper is
already correct, instead of falsely claiming the main preprint was directly
rewritten through the connector.
