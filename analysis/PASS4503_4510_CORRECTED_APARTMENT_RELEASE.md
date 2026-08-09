# Passes 4503–4510 — corrected apartment obstruction, cohomology, GQ scaling, and local gauge release

## Release correction

This report supersedes the **restricted-subgroup section claims** in `PASS4469_4494_APARTMENT_EXTENSION_RELEASE.md`. The earlier full-group result remains valid:

```text
0 -> K/J (29) -> E=M/J (39) -> H10=M/K (10) -> 0
PSp(4,3): rank(A)=389, rank([A|b])=390 -> nonsplit.
```

Pass 4503 found that the historical Pass-4493 point/line `370/370` result does not reproduce from the exact current geometry. The corrected section census is executable and frozen.

## 4503 — every maximal subgroup type retains the obstruction

The five maximal subgroup types of `PSp(4,3) ≅ U4(2)` have orders

```text
960, 720, 648, 648, 576
```

and exact section ranks

```text
2^4:A5, order 960, index 27               388 / 389  nonsplit
spread stabilizer S6, 720, index 36        386 / 387  nonsplit
line stabilizer, 648, index 40             386 / 387  nonsplit
point stabilizer, 648, index 40            387 / 388  nonsplit
class-45 involution centralizer, 576, 45    386 / 387  nonsplit
```

The canonical incident point-line flag stabilizer has order `162` and instead gives

```text
384 / 384, affine dimension 6.
```

Therefore the old statement “fix one point or line and choose a protected complement” is withdrawn. A verified natural splitting gauge is an **incident flag**.

## 4504 — exact flag gauge compiler

The flag section family has `2^6=64` elements. Exhaustive enumeration in the canonical quotient coordinates gives optimum

```text
(total minimal ambient Hamming weight, max column weight, union support)
= (42, 9, 13)
```

with column weights

```text
1,1,1,1,5,5,5,5,9,9.
```

This is software gauge synthesis in `E=M/J`, not a physical measurement or decoder optimum.

## 4505 — the full 29D radical has two cohomological obstruction bits

For `R29=K/J`, exact Cayley-graph cocycle propagation over all `25920` elements gives

```text
dim Z^1 = 31
dim B^1 = 29
dim H^1 = 2.
```

There are three nonzero classes. All three generate exactly the same 23-dimensional support

```text
W/J = (K ∩ rowspace(N))/J
```

already resolved by Pass 4492 as the route-hull/sentinel extension

```text
8 | (1 | 14).
```

The separate six-dimensional radical factor is absent from every nonzero H1-class closure.

## 4506 — the bridge scales from 10 to 70 on Q(5,3)=GQ(3,9)

The repo's independent `Q(5,3)` builder gives

```text
112 points
280 lines
102060 apartments
rank H = 279
rank N = 91
rank(N^T N)=70
```

and verifies entrywise

```text
H H^T = N^T N  over F2.
```

Therefore

```text
radical dimension = 279-70 = 209
protected quotient = im(N)/ker(N^T), dimension 91-21 = 70.
```

On the dual `GQ(9,3)` orientation, the apartment Gram is the all-ones matrix of rank `1`, while the incidence Gram has rank `22`: the bridge fails sharply. This is a concrete orientation-sensitive characteristic-two theorem.

## 4507 — fail-closed release hardening

The continuation found two stale-result failures:

1. Pass 4493's old restricted section table;
2. Pass 4482's frozen ten-line basis indices.

Pass 4482 was re-solved in the current exact geometry. Its replacement line basis is

```text
0,1,4,10,17,18,22,24,26,31
```

and again has Gram rank `10` and intersection graph `P4 ⊔ 3K2` with six edges.

The two independent W33 builders used by this frontier were also checked to have exactly the same point and line ordering, so the stale Pass-4482 list was not excused as a harmless reindexing.

The new release policy regenerates executable witnesses and requires frozen JSON to remain byte-for-byte unchanged. Public registry loss under concurrent writes is also guarded.

## 4508 — outside box: two F2^2 cohomologies have different outer actions

Pass 4496 gives `H^1(PSp,V8)=F2^2` for the protected eight-core; the `PGSp` outer involution swaps a basis, leaving one nonzero class fixed.

Pass 4505 gives `H^1(PSp,R29)=F2^2` for the full radical, but Pass 4508 computes the outer action as the **identity**, so all three nonzero radical classes are fixed.

Equal dimension is therefore not an identification of the two cohomology spaces as `PGSp` outer modules.

## 4509 — outside box: a two-charge restriction barcode explains the flag threshold

Restriction of the three nonzero radical classes gives:

```text
M20 order 960              kills 0
spread S6 order 720        kills 0
line stabilizer 648        kills one 1D class
point stabilizer 648       kills a different 1D class
class-45 centralizer 576   kills 0
incident flag 162          kills all three nonzero classes
```

Equivalently, point and line stabilizers annihilate distinct one-dimensional obstruction subspaces; their incident intersection kills the full two-dimensional `H^1`.

This explains the corrected geometry: **point or line removes one obstruction charge; an incident flag removes both.**

## 4510 — outside box: the minimum flag gauge is one radius-one W33 line cell

The 13-line union support of the optimal Pass-4504 section is exactly the closed neighborhood of the fixed line in the line-intersection graph.

Its induced graph is

```text
K1 join 4 K3.
```

The four triangles are the four pencils of three other lines through the four points of the fixed line. Thus a valid symmetry-broken protected representative register can be chosen entirely inside one radius-one W33 line cell.

This is finite-graph locality, not automatically spatial, optical, energetic, or causal locality in hardware.

## Evidence boundary

The exact claims are certified by the executable Pass-4503–4510 scripts, frozen JSON certificates, focused pytest packet, and GitHub Actions regeneration workflow. The subgroup classification uses the standard `PSp(4,3) ≅ U4(2)` maximal-subgroup structure; the generalized-quadrangle scaling uses the repo's independently built `Q(5,3)` incidence geometry.

No absence-of-search-result claim is used as proof of novelty. No code/module dimension is assigned a particle or physical state-count interpretation without a separate physical derivation.
