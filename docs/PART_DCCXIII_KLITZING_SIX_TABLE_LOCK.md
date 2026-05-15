# Part DCCXIII — Klitzing Six-Table Lock

This part turns the manual HTML hunt into an executable lock-check for the six tomotope sections:

1. partial-a marker in GC section,
2. partial-b marker in GC section,
3. rectified tomotope operation anchor,
4. truncated tomotope operation anchor,
5. maximal-expanded tomotope operation anchor,
6. omnitruncated tomotope operation anchor.

## What it checks

Given an `Abstract polytopes.html` source, it verifies:

- partial-a and partial-b occur and share one enclosing `<table> ... </table>` range,
- all four operation anchors occur and share one enclosing operation table range,
- operation anchor order is strict: `rect < trunc < exp < omni`.

## Why this matters

This removes ambiguity about where the six tomotope sections are in the raw HTML and gives deterministic table boundaries for downstream extraction.

## Artifact

- Script: `exploration/w33_tomotope_klitzing_six_table_lock.py`
- Test: `tests/test_w33_tomotope_klitzing_six_table_lock.py`
- Output: `data/w33_tomotope_klitzing_six_table_lock_summary.json`
