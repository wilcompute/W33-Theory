# Part MCCCXCIV: Spread / Double-Six Scheme Isomorphism

## Claim Boundary

MCCCXCIV is an explicit finite isomorphism witness.  It constructs a labeling
between the 36 W33 spreads and the 36 `E6` double-sixes that preserves the
two-class overlap scheme from MCCCXCIII.

It is not a uniqueness theorem.  It does not prove that this labeling is
intrinsic or canonical.

## Input

MCCCXCIII proved that both sides have the same two-class scheme:

```text
class A: srg(36,15,6,6)
class B: srg(36,20,10,12)
```

with the dictionary:

```text
W33 spread overlap 4  <-> E6 double-six overlap 4
W33 spread overlap 1  <-> E6 double-six overlap 6
```

## Construction

Sort the 36 W33 spreads and the 36 double-sixes.  Anchor the first sorted W33
spread to the first sorted double-six.  A deterministic backtracking search
then extends that anchor to a full graph isomorphism of the overlap-4 graphs.

The same mapping works for all eight W33-derived `E6` matter charts.

## Result

The verifier checks:

```text
mapping is a permutation of 36 labels;
spread 0 maps to double-six 0;
spread overlap 4 maps to double-six overlap 4;
spread overlap 1 maps to double-six overlap 6;
relation failure count = 0;
same mapping works for all eight charts.
```

The explicit mapping is:

```text
[0, 5, 28, 30, 15, 4, 26, 25, 33, 35, 6, 13,
 22, 29, 21, 9, 20, 1, 2, 12, 17, 8, 31, 10,
 23, 24, 27, 32, 18, 19, 16, 3, 14, 7, 11, 34]
```

## Reading

The previous theorem showed a scheme-level resonance.  This theorem upgrades
that to an existence-level bridge:

```text
36 W33 spreads <-> 36 E6 double-sixes
```

with overlap classes preserved exactly.  The remaining stronger problem is to
derive the labeling intrinsically from the W33/E6 construction rather than by
anchored finite search.

## Artifacts

- Analysis: `analysis/w33_spread_double_six_scheme_isomorphism.py`
- Tests: `tests/test_w33_spread_double_six_scheme_isomorphism.py`
- Result: `PART_MCCCXCIV_SPREAD_DOUBLE_SIX_SCHEME_ISOMORPHISM_results.json`
