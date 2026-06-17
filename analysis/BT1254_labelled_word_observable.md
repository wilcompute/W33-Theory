# BT1254 -- Labelled-Word Observable

## Purpose

BT1251 proved that ordered/oriented variants disappear when we quotient to the unlabelled symmetric Cayley sphere. BT1254 adds the minimal labelled observable that keeps generator channels fixed.

## Observable

Use the eight labelled channels

```text
g1p, g1m, g2p, g2m, g3p, g3m, g4p, g4m
```

and record the inverse-pair tensor.  The inverse pairs are

```text
(g1p,g1m), (g2p,g2m), (g3p,g3m), (g4p,g4m)
```

A fixed-label orientation flip is no longer invisible: it swaps one pair of rows and columns in the labelled tensor.  The unlabelled symmetric Cayley sphere still remains unchanged.

## Consequence

BT1233/BT1242 are correct unlabelled recovery invariants.  BT1254 is the first labelled layer for orientation-sensitive tomography.  Future pulse-level or transcript-level tests should refine this tensor with labelled geodesic counts.

## Files

- Code: `analysis/bt1254_labelled_word_observable.py`
- Result: `data/bt1254_labelled_word_observable_summary.json`
