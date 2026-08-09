# Part MCCCXCV: Spread / Double-Six Automorphism Order

## Claim Boundary

MCCCXCV is a finite automorphism-order theorem for the 36-object
spread/double-six association scheme.  It uses the W33 spread graph, and by the
explicit isomorphism of MCCCXCIV the same order applies to the `E6` double-six
scheme.

It does not choose a unique canonical spread-to-double-six labeling.

## Input

MCCCXCIII proved that the 36 W33 spreads and the 36 `E6` double-sixes share the
same two-class scheme:

```text
overlap-4 graph = srg(36,15,6,6).
```

MCCCXCIV constructed an explicit anchored isomorphism between the two schemes.

## Orbit-Stabilizer Count

The verifier counts automorphisms of the 36-object overlap-4 graph.

It first counts the stabilizer of the first spread:

```text
|Stab(spread_0)| = 1440.
```

It then verifies that the first spread can be moved to every one of the 36
vertices:

```text
|Orbit(spread_0)| = 36.
```

Therefore:

```text
|Aut(scheme)| = 36 * 1440 = 51840.
```

The factorization is:

```text
51840 = 2^7 * 3^4 * 5.
```

## Reading

The `36`-object spread/double-six bridge now recovers the full `51840`
symmetry scale from its own finite incidence scheme.  This is the same order
that appears throughout the W33/`E6` bridge, now derived from:

```text
36 spreads
36 double-sixes
srg(36,15,6,6)
orbit-stabilizer
```

The next stronger problem is still canonical labeling, not group order.

## Artifacts

- Analysis: `analysis/w33_spread_double_six_automorphism_order.py`
- Tests: `tests/test_w33_spread_double_six_automorphism_order.py`
- Result: `PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER_results.json`
