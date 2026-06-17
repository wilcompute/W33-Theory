# BT1243 -- BT1236 Section Status

## Purpose

BT1243 materializes the BT1236 paper section file under `paper/sections`.

## File

```text
paper/sections/sec_bt1236_minimal_clifford_word_metric.tex
```

## Recorded invariants

The section records:

```text
Sp(4,3) order = 51840
minimal projective-transvection count = 4
word-metric diameter = 14
B4 = 534, B8 = 14994, B12 = 51803, B14 = 51840
```

## Status

The sanity JSON now reports:

```text
section_materialized_preprint_input_pending
```

The section file exists. The remaining paper mutation is the input line insertion into `paper/w33_preprint.tex`.

## Boundary

This is section materialization, not full preprint mutation. The remaining command is:

```bash
python tools/integrate_bt1236_insert.py
```
