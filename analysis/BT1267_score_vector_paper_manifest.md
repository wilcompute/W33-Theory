# BT1267 -- Score Vector Paper Section

## Purpose

BT1267 adds a compact paper section for the tomography score vector.

## New section files

```text
analysis/BT1267_score_vector_paper_section.tex
paper/sections/sec_bt1267_tomography_score_vector.tex
```

## Content

The section defines

```text
S = (C,D,P,E,L)
```

where the entries represent closure, diameter-14 word metric, polar path edge geometry, unique all-channel endpoint, and labelled nonzero channel spread.

## Regime scores

```text
diam14_polar_path: 5/5
diam12:             2/5
diam10_A:           2/5
diam10_B:           1/5
diam10_C:           1/5
```

## Boundary

The analysis-side source contains the fuller pass/review/fail wording. The materialized paper section is more compact because the richer direct create call was blocked by the connector safety layer.
