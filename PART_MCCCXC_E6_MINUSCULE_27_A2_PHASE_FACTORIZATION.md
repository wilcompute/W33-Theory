# Part MCCCXC: E6 Minuscule 27 x A2 Phase Factorization

## Claim Boundary

MCCCXC is a finite representation-geometry theorem.  It resolves the two
`81`-root matter sectors in the exact W33-derived

```text
E8 -> E6 x A2
```

decomposition.  It does not by itself assert a continuum particle spectrum.

## Input

MCCCLXXXIX proved that each W33 tetracode coordinate splits the exact `E8`
roots as:

```text
240 = 72_E6 + 6_A2 + 81 + 81.
```

The remaining question was whether each `81` is just a count or an actual
representation product.

## Factorization

For any coordinate and either `81`-sector, delete the selected `A2` coordinate.
The 81 roots project to:

```text
27 distinct E6 weights,
each appearing with 3 A2 phases.
```

So the exact factorization is:

```text
81 = 27_E6 * 3_A2.
```

This holds for all four coordinates and both conjugate `81` sectors, giving
eight verified matter-sector charts.

## E6 Weight Geometry

Each projected 27-weight set has:

```text
rank = 6
norm profile = {4/3:27}
barycenter = 0
Gram identity = G^2 = 6G
E6 reflection closure failures = 0
```

The pairing with the 72 `E6` roots has profile:

```text
{-1:432, 0:1080, 1:432}.
```

That is the finite minuscule weight behavior: root reflections permute the 27
weights instead of producing new weights.

## Schlaefli Graph

On the 27 projected weights, draw an edge when the inner product is `1/3`.
The verifier gets:

```text
vertices = 27
degree = 16
edges = 216
lambda = 10
mu = 8
```

So the graph is:

```text
srg(27,16,10,8),
```

the Schlaefli graph.  The complementary inner-product graph, using `-2/3`, is:

```text
srg(27,10,1,5).
```

## Reading

The matter sector is no longer only numerological:

```text
81 matter roots
  = 27 E6 minuscule weights
  x 3 A2 phases.
```

Together with MCCCLXXXIX, this upgrades

```text
240 = 72 + 6 + 81 + 81
```

into:

```text
E8 roots = E6 roots + A2 roots + (27 x 3) + (27* x 3*).
```

## Artifacts

- Analysis: `analysis/w33_e6_minuscule_27_a2_phase_factorization.py`
- Tests: `tests/test_w33_e6_minuscule_27_a2_phase_factorization.py`
- Result: `PART_MCCCXC_E6_MINUSCULE_27_A2_PHASE_FACTORIZATION_results.json`
