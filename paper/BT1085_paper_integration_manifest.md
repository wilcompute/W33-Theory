# BT1085 paper integration manifest

This manifest records which BT1083--BT1085 results belong in each paper.

## W33 preprint / w33_paper line

Add:

```text
paper/sections/sec_bt1083_1085_matter_bridge.tex
```

Recommended insertion point:

```text
before \section{The TOE Singularity Theorem}
```

Reason: the section is a matter-sector bridge result. It belongs after the symmetry/phase/leakage material and before the global uniqueness/falsifier sections.

## Photonic holonet paper

Add:

```text
paper/sections/sec_bt1083_1085_holonet_bridge.tex
```

Recommended insertion point:

```text
before \subsection{The ethos}
```

Reason: the section is an architecture/runtime bridge result. It belongs after the physics-to-architecture dictionary and before the closing ethos/verification apparatus.

## Integration helper

```text
tools/bt1085_integrate_latest_paper_sections.py
```

The helper inserts both sections idempotently.

## Boundary

The TeX sections are committed and paper-ready. The helper records the exact insertion points for the large source files.
