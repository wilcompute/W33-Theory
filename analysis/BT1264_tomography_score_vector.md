# BT1264 -- Tomography Score Vector

## Purpose

BT1264 compresses the full-order Clifford regimes into one recovery score vector.

## Score components

Each regime receives five binary gates:

```text
closure51840
diameter14
polar_path_P4P4
unique_all_channel_endpoint
labelled_nonzero_spread
```

## Result

```text
diam14_polar_path: 5/5
diam12:             2/5
diam10_A:           2/5
diam10_B:           1/5
diam10_C:           1/5
```

The winner is

```text
diam14_polar_path
```

## Interpretation

Only the diameter-14 polar path regime passes all five gates.  Diameter 12 has a strong labelled signal, but fails the diameter and polar-path gates.  Diameter-10 regimes close too fast and are rejected despite full order.

## Files

- Code: `analysis/bt1264_tomography_score_vector.py`
- Result: `data/bt1264_tomography_score_vector_summary.json`
