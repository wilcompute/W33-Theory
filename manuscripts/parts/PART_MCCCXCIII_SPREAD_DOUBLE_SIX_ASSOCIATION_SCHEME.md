# Part MCCCXCIII: Spread / Double-Six Association Scheme

## Claim Boundary

MCCCXCIII is a finite association-scheme theorem.  It compares the 36 W33
spreads with the 36 `E6` double-sixes from MCCCXCII.

It does not choose a canonical spread-to-double-six bijection.  The canonical
labeling problem remains open.

## W33 Spread Side

A W33 spread is a partition of the 40 points into 10 disjoint isotropic lines.
The verifier finds:

```text
spreads = 36
spread size = 10 lines
each W33 line lies in 9 spreads
```

Pairwise spread overlaps are:

```text
overlap 4 lines: 270 pairs
overlap 1 line : 360 pairs
```

The overlap-4 graph is:

```text
srg(36,15,6,6).
```

The overlap-1 graph is the complementary class:

```text
srg(36,20,10,12).
```

## E6 Double-Six Side

For every W33-derived `E6` matter chart, MCCCXCII gives 36 double-sixes.
Pairwise double-six overlaps are:

```text
overlap 4 weights: 270 pairs
overlap 6 weights: 360 pairs
```

The overlap-4 graph is again:

```text
srg(36,15,6,6).
```

The overlap-6 graph is the complementary class:

```text
srg(36,20,10,12).
```

This holds for all eight matter charts.

## Reading

The equality

```text
36 W33 spreads = 36 E6 double-sixes
```

is now stronger than a count.  Both sides carry the same exact two-class
overlap scheme:

```text
class A: srg(36,15,6,6)
class B: srg(36,20,10,12)
```

This links the W33 spread/MUB side and the `E6` double-six side as finite
association schemes, while keeping the stronger canonical bijection as the
next target.

## Artifacts

- Analysis: `analysis/w33_spread_double_six_association_scheme.py`
- Tests: `tests/test_w33_spread_double_six_association_scheme.py`
- Result: `PART_MCCCXCIII_SPREAD_DOUBLE_SIX_ASSOCIATION_SCHEME_results.json`
