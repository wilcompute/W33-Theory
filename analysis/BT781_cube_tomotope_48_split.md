# BT781 — The Cube/Tomotope Order-48 Split

The prompt clue was excellent: BT780 found a 48-element stabilizer for a cube
chart, while the tomotope edge symmetry group has order 96.  The natural guess
is that the cube-chart stabilizer might be the tomotope's chiral half.

BT781 tests that directly.

## Result

The two 48s are **not isomorphic**.  The mismatch is not noise; it is the
structure.

```text
cube chart stabilizer:       2^3 : S3      = 8 * 6  = 48
tomotope derived subgroup:   2^4 : C3      = 16 * 3 = 48
```

The element order distributions distinguish them immediately:

```text
cube chart 48:        {1:1, 2:19, 3:8, 4:12, 6:8}
tomotope derived 48:  {1:1, 2:15, 3:32}
```

So the cube chart half keeps the full coordinate permutation/reflection quotient
`S3`, but only three binary translation bits.  The tomotope derived half keeps
four binary bits, but only oriented triality `C3`.

## Exact cube side

The base cube-chart stabilizer in PSp(4,3) induces the full automorphism group
of the local hypercube `Q3`:

```text
Aut(Q3) = C2^3 : S3
|C2^3| = 8
|S3|   = 6
8 * 6 = 48
```

The derived subgroup of this cube half has order 12 and is `A4`:

```text
cube-derived order distribution: {1:1, 2:3, 3:8}
```

## Exact tomotope side

Using the tomotope edge action from the tomotope paper:

```text
rho0 = (5 10)(6 9)(7 12)(8 11)
rho1 = (1 6)(2 5)(3 8)(4 7)
rho2 = (5 9)(6 10)(7 11)(8 12)
rho3 = (5 8)(6 7)(9 12)(10 11)
```

we recover:

```text
|Gamma(T)| = 96
Gamma(T)' = 48
normal 2-core inside Gamma(T)' = C2^4
Gamma(T)' / C2^4 = C3
```

This agrees with the older tomotope invariant file, which records group order
96, derived subgroup order 48, abelianization order 2, and normal 2-core order
16.

## Breakthrough interpretation

The same number `48` appears in two complementary forms:

```text
cube transport:       2^3 : S3
oriented tomotope:    2^4 : C3
```

That is a binary/reflection trade:

```text
2^3 * 6 = 2^4 * 3
```

or, said geometrically:

```text
one tomotope binary bit = one cube reflection bit
```

This fits the chirality story from BT745-BT778.  The cube-chart layer is not the
tomotope chiral half; it is the **reflection-completed local transport half**.
The tomotope half is instead the **binary-completed oriented triality half**.

## Normalization ladder

The order-48 unit now appears in three different places:

```text
tomotope flags:             192 = 4  * 48
tomotope edge symmetry:      96 = 2  * 48
W33 directed edges / SEH:    480 = 10 * 48
```

The GraphTheory note emphasizes the same `480` as five independent discrete
Einstein-Hilbert / directed-edge / triangle-orientation derivations, so the
48-unit is plausibly the smallest shared local symmetry quantum behind both the
cube-web transport layer and the tomotope flag layer.

## Next experiment

> **ALREADY RESOLVED -- read BT782 and BT783 before acting on this.**
> The experiment proposed below was carried out immediately: `BT782` states the
> bridge as an exact sequence `1 -> C2_chiral -> Gamma(T)' -> Aut+(Q3) -> 1`, and
> `BT783` executes the test and refutes it (`Gamma(T)'` has trivial centre, no
> normal C2, no index-2 subgroup, so it cannot be that extension). Pass 1127
> re-derived BT783's obstruction from scratch because this section still read as
> open; that pass is now narrowed to cite BT783. Pass 1376 confirms both files
> against the PUBLISHED generators of `Gamma(T)` for the first time.


BT782 should build the explicit bridge functor:

```text
Aut(Q3)=2^3:S3  -->  Gamma(T)'=2^4:C3
```

by quotienting the cube reflection bit and adding the missing tomotope binary
bit.  If this works, it identifies the chiral projection map from local hypercube
routing into tomotope orientation.
