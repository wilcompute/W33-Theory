# BT1029 — Timing recommendation parser

BT1029 adds parser logic that converts surfaced shard timing samples into safe
window-size recommendations.

## Input

```text
data/bt1026_incidence_shard_timing.json
```

## Current recommendations

No surfaced Actions timing samples are available yet, so the parser keeps the
safe defaults:

```text
degree_2 count = 8
degree_3 count = 8
```

## Policy

When timing samples exist, the parser scales the count using both a time budget
and a memory budget. Until then, it keeps the conservative 8-row default.

## Witnesses

```text
analysis/bt1029_timing_recommendation_parser.py
data/bt1029_timing_recommendation_parser.json
```
