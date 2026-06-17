# BT1248 -- Four-Transvection Stabilizer Regimes

## Purpose

BT1248 computes orbit/stabilizer diagnostics for the full-order four-transvection regimes from BT1242--BT1245.

## Stabilizer table

The acting group order is

\[
|Sp(4,3)|=51840.
\]

For each full-order orbit row, the setwise stabilizer is

\[
|\mathrm{Stab}(S)|=51840/|\mathcal O(S)|.
\]

The full-order rows are:

```text
diam10_A: count 12960, stabilizer 4
diam10_B: count 3240,  stabilizer 16
diam10_C: count 6480,  stabilizer 8
diam12:   count 25920, stabilizer 2
diam14:   count 12960, stabilizer 4
```

## Main conclusion

The BT1228 / BT1233 diameter-14 regime is not the largest-stabilizer orbit.  A diameter-10 orbit has stabilizer order 16.  Therefore the special role of the BT1228 regime is not maximal symmetry; it is balanced local closure:

\[
9^3 24^3
\]

on pairs and

\[
72^2 648^2
\]

on triples.

## Files

- Code: `analysis/bt1248_four_transvection_stabilizer_regimes.py`
- Result: `data/bt1248_four_transvection_stabilizer_regimes_summary.json`
