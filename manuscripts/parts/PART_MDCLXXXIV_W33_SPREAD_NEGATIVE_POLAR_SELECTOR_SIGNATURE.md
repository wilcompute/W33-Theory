# Part MDCLXXXIV: W33 Spread Negative-Polar Selector Signature

## Claim Boundary

MDCLXXXIV proves the exact graph type of the W33 spread selector.

It does not yet construct the final `60` antipodal-address to `40` W33-line
incidence transport.

## Input

MDCLXXXIII showed that the raw Clifford antipodal selector is:

```text
60 antipodal 600-cell addresses = A5 in degree-six action
36 L/R cells = action fibers g(i)=j
```

Those `36` cells form the ordinary `6 x 6` rook grid.

The obvious next guess is that the W33 spread graph is a Latin-square
completion of that rook grid: same row, same column, or same symbol.

## Result

That guess is false in a useful way.

The W33 spread overlap-`4` graph is:

```text
srg(36,15,6,6)
```

but it has:

```text
clique number = 4
independence number = 5
```

A `6 x 6` Latin-square graph would contain visible `K6` cliques:

```text
6 row cliques
6 column cliques
6 symbol cliques
```

The raw rook grid has clique number `6`; the W33 spread graph has clique number
`4`.  Therefore the missing selector is not a Latin/Euler third direction on
the raw Clifford grid.

## Negative-Polar Replacement

The verifier constructs the minus-type quadratic form over `F2`:

```text
Q(x0,...,x5) = x0*x1 + x2*x3 + x4 + x4*x5 + x5
```

There are exactly `36` nonsingular nonzero vectors with `Q=1`.

Join two such vectors when their polar bilinear form is zero.  The resulting
graph is again:

```text
srg(36,15,6,6)
```

The verifier then finds an explicit graph isomorphism:

```text
W33 spread overlap-4 graph  ~=  NO^-(6,2)
```

## Group-Order Lock

For `m=3`,

```text
|O^-(2m,2)| = 2 * 2^(m(m-1)) * (2^m + 1) * product_{i=1}^{m-1}(2^(2i)-1)
```

so:

```text
|O^-(6,2)| = 51840 = |W(E6)|
```

This is the selector-level return of the same `W(E6)` symmetry that has been
appearing throughout the W33/E6/E8 bridge.

## Reading

The bridge ladder is now:

```text
raw Clifford antipodal selector = A5 degree-six torsor
36 raw L/R cells                = 6 x 6 rook graph
36 W33 spreads                  = NO^-(6,2) negative-polar graph
negative-polar group order      = 51840 = |W(E6)|
```

So the missing twist is not "add one more Latin symbol."  It is:

```text
rook/A5 torsor  ->  negative-polar W(E6) selector
```

The next target is correspondingly sharper: lift this negative-polar selector
to an explicit `60`-address / `40`-line incidence transport.

## Artifacts

- Analysis: `analysis/w33_spread_negative_polar_selector_signature.py`
- Tests: `tests/test_w33_spread_negative_polar_selector_signature.py`
- Result: `PART_MDCLXXXIV_W33_SPREAD_NEGATIVE_POLAR_SELECTOR_SIGNATURE_results.json`
