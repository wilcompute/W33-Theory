# Part MDCLXXXI: Clifford L/R Grid vs W33 Spread Scheme Boundary

## Claim Boundary

MDCLXXXI is a finite boundary theorem for the GitHub-added
MCCCCXVII-MCCCCXXXII Clifford fibration selector.

That packet proves:

```text
12 special Clifford fibrations = K6 disjoint union K6 = L family plus R family
36 L/R cross-pairs
36 W33 spreads
```

MDCLXXXI checks the next question: whether the raw `36` Clifford cross-pairs
carry the same natural association scheme as the `36` W33 spreads.

They do not.

## Clifford L/R Scheme

Each `L_i, R_j` cross-pair shares exactly two great decagons.  The union of
those two decagons has `20` vertices.

For the `36` cross-pairs:

```text
shared decagons per pair = 2
vertices per pair = 20
distinct cross-pairs share 0 decagons
vertex-overlap profile = 0:180, 4:450
```

The zero-overlap relation is exactly the same-row/same-column relation on a
`6 x 6` grid:

```text
srg(36,10,4,2)
```

The complementary four-overlap relation is:

```text
srg(36,25,16,20)
```

## W33 Spread Scheme

The W33 spreads have a different two-class scheme:

```text
spread-overlap profile = 4:270, 1:360
overlap-4 graph = srg(36,15,6,6)
overlap-1 graph = srg(36,20,10,12)
```

So the count identity is real:

```text
36 Clifford L/R cross-pairs = 36 W33 spreads
```

but the natural schemes are not the same.

## Reading

This is not a failure of the Clifford fibration theorem.  It is the precise
location of the missing selector.

The raw Clifford side gives:

```text
6 x 6 rook/Hamming scheme
```

The W33 spread side requires:

```text
spread/double-six association scheme
```

Therefore any canonical `600`-cell-to-W33 spread labeling cannot be only the
raw `L x R` address.  It must include an additional symplectic twist that
transforms the `6 x 6` Clifford grid into the W33 spread scheme.

## Artifacts

- Analysis: `analysis/w33_clifford_lr_spread_scheme_boundary.py`
- Tests: `tests/test_w33_clifford_lr_spread_scheme_boundary.py`
- Result: `PART_MDCLXXXI_CLIFFORD_LR_SPREAD_SCHEME_BOUNDARY_results.json`
