# BT941 — Optimized support-search engine

BT941 turns the BT938 branch-and-bound plan into a bitset search-engine scaffold.

## Encoding

- nonzero H classes: integers `1..255`;
- subspaces: row-reduced 8-bit mask tuples;
- support weights: imported from the H support distribution;
- pairings: precomputed table for `B(e,f)`.

## Exact table sizes

```text
pair_table_size = 255 * 255 = 65025
ordered_active_pair_count = 255 * 128 = 32640
```

## Current best

```text
profile = [6, 6, 6, 10, 10, 10, 14, 14]
support_sum = 76
raw_lower_bound = 48
```

## Boundary

This is an optimized engine scaffold, not a completed exhaustive proof. It records the exact table sizes, memo keys, pruning tests, and current support certificate.

## Witness

```text
analysis/bt941_compiled_exhaustive_search_engine.py
data/bt941_compiled_exhaustive_search_engine.json
```
