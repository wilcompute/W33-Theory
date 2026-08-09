# Part MCCCXCII: E6 36 Double-Six Bridge

## Claim Boundary

MCCCXCII is a finite cubic-surface incidence theorem on the W33-derived `E6`
minuscule matter weights.  It identifies the double-six combinatorics inside
the finite weight geometry.  It does not by itself assert a continuum algebraic
surface.

## Input

MCCCXC gave the 27 projected `E6` weights in each matter chart.  MCCCXCI found
the 45 zero-sum tritangent triples.  The same 27-weight chart carries the
Schlaefli graph:

```text
srg(27,16,10,8)
```

where an edge is the inner product `1/3` relation.

## Double-Six Definition

In this graph convention, a double-six is two disjoint six-cliques:

```text
row A = 6 mutually skew weights
row B = 6 mutually skew weights
```

with cross edges forming a perfect matching:

```text
each A_i is skew to exactly one B_j,
each B_j is skew to exactly one A_i.
```

## Result

For every one of the eight W33-derived matter charts, the verifier finds:

```text
six-cliques = 72
double-sixes = 36
```

and checks:

```text
each six-clique appears in exactly one double-six;
each weight appears in exactly 16 double-sixes;
each double-six has exactly 6 cross matching edges.
```

## Reading

The chain now recovers the classical cubic-surface incidence stack from the
finite W33/E6 matter weights:

```text
27 weights
45 zero-sum tritangent triples
36 double-sixes
```

The double-six layer is no longer an imported analogy.  It is reconstructed
from the exact inner products of the W33-derived `E6` minuscule matter charts.

## Artifacts

- Analysis: `analysis/w33_e6_36_double_six_bridge.py`
- Tests: `tests/test_w33_e6_36_double_six_bridge.py`
- Result: `PART_MCCCXCII_E6_36_DOUBLE_SIX_BRIDGE_results.json`
