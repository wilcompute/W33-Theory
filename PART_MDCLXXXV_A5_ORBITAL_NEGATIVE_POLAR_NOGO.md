# Part MDCLXXXV: A5 Orbital Negative-Polar No-Go

## Claim Boundary

MDCLXXXV rules out one precise candidate for the missing selector:

```text
diagonal A5 orbital selection on the raw 6 x 6 Clifford L/R grid
```

It does not rule out a non-diagonal `A5` subgroup inside the
negative-polar `O^-(6,2)` action, nor a symplectic relabeling of the
`36` cells.

## Input

MDCLXXXIII showed:

```text
60 antipodal 600-cell addresses = A5 in degree-six action
36 L/R cells = action fibers g(i)=j
```

MDCLXXXIV showed:

```text
36 W33 spreads = NO^-(6,2) negative-polar graph
clique number = 4
```

The natural next guess is:

```text
maybe the W33 spread graph is an A5-invariant orbital graph
on the same 36 raw cells
```

## Orbital Enumeration

The diagonal `A5` action on the `36` cells has:

```text
16 unordered pair orbitals
```

These `16` orbitals partition all unordered cell pairs:

```text
C(36,2) = 630
```

The raw rook graph is exactly six of those orbitals:

```text
[0, 1, 5, 6, 10, 14]
```

with edge count:

```text
180
```

## Unique SRG Candidate

Among all unions of the `16` diagonal-`A5` orbitals, there is exactly one
union with parameters:

```text
srg(36,15,6,6)
```

Its orbit indices are:

```text
[0, 1, 2, 5, 6, 7, 10, 12, 14]
```

So it is:

```text
raw rook graph + three extra orbitals [2, 7, 12]
```

## No-Go

That unique diagonal-`A5` SRG has:

```text
clique number = 6
```

because it contains all row and column `K6` cliques from the raw rook graph.

But the W33 spread graph / `NO^-(6,2)` has:

```text
clique number = 4
```

Therefore:

```text
unique diagonal-A5 srg(36,15,6,6) != W33 negative-polar spread graph
```

The shared SRG parameters are not enough.  The clique-number invariant separates
the raw A5 orbital completion from the live W33 selector.

## Reading

The selector ladder is now sharper:

```text
raw Clifford antipodal addresses -> A5 torsor
raw 36 L/R cells                  -> 6 x 6 rook grid
diagonal-A5 orbital completion    -> Latin/rook SRG with K6 cliques
W33 spreads                       -> NO^-(6,2), clique number 4
```

So the missing bridge is not a local orbital pick on the raw grid.  It must be
a genuine negative-polar/symplectic twist of the cell labels.

## Artifacts

- Analysis: `analysis/w33_a5_orbital_negative_polar_nogo.py`
- Tests: `tests/test_w33_a5_orbital_negative_polar_nogo.py`
- Result: `PART_MDCLXXXV_A5_ORBITAL_NEGATIVE_POLAR_NOGO_results.json`
