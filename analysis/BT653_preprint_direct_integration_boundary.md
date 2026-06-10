# BT653 Preprint Direct Integration Boundary

Goal: place the BT646 and BT647 section inputs directly before the TOE Singularity section in paper/w33_preprint.tex.

Desired insertion:

```tex
% BT646--BT647 inserts
\input{sections/sec_bt646_internal_s4_hodge_clock}
\input{sections/sec_bt647_synthesis_bridge}
```

Target location:

```tex
\section{The TOE Singularity Theorem}
```

What is already pushed:

- paper/sections/sec_bt646_internal_s4_hodge_clock.tex
- paper/sections/sec_bt647_synthesis_bridge.tex
- tools/integrate_bt646_bt647_inserts.py
- analysis/BT650_static_verification_note.md

The integration helper is idempotent and inserts each input line only if it is absent.

Run path from a checkout:

```bash
python tools/integrate_bt646_bt647_inserts.py
python analysis/bt574_latex_sanity_verifier.py
python tools/build_w33_preprint.py --compile
```

Boundary:

A direct connector update of paper/w33_preprint.tex was attempted after fetching the active file and locating the insertion point, but the connector content filter blocked the full-file replacement.  The repository therefore has the section files and the exact idempotent integration tool, but this note records that the main preprint file still needs the helper to be run in a checkout or a smaller accepted patch route.
