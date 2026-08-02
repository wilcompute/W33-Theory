# Passes 2011–2015 — exact methods and scope record

This file records how the five certificates were obtained and, equally
importantly, what each computation does **not** establish.

## Common literal model

All five passes use the same literal `W(3,3)` model:

- 40 projective points of `F_3^4`;
- 40 totally isotropic lines of four points;
- 240 collinear point pairs;
- 540 frames, each an unordered pair of disjoint isotropic lines with its
  canonical four-edge cross-matching;
- 36 spreads, each an exact cover of the 40 points by ten isotropic lines;
- the projective similitude group `PGSp(4,3)` of order 51,840, generated from
  the 40 symplectic transvections and one nonsquare similitude.

The projective action was closed explicitly as permutations of the 40 points,
then transported to lines, frames, spreads, edges, and octets.  No class was
identified from cardinality alone.

---

## Pass 2011 — decorated four-line spread pairs

The 270 unordered spread pairs sharing four lines form a transitive `G`-set with
point stabilizer

`H = Stab({S,T}) ≅ S4 × D8`, `|H|=192`.

Three conjugacy-class carriers have the same smallest centralizer orbit profile:

| class size | element order | centralizer | decoration over one spread pair |
|---:|---:|---:|---|
| 270 | 2 | 192 | canonical linewise half-turn |
| 540 | 4 | 96 | one of two inverse coherent quarter-turns |
| 1620 | 4 | 32 | one of six cyclic orders of the four common lines |

For the size-540 representative, the induced permutation fixes all four common
lines and is a 4-cycle on the four points of each common line.  Conjugating the
literal decorated object under `G` produces exactly 540 objects and exactly two
objects over each of the 270 spread pairs.

For the size-1620 representative, the induced permutation is a 4-cycle on the
set of four common lines.  Conjugating the decorated object gives exactly 1,620
objects and exactly six objects over each spread pair—the six cyclic orders of a
four-element set.

This is a stabilizer-and-action identification, not a count match.

---

## Pass 2012 — complete subgroup enumeration inside `H`

The subgroup lattice of the fixed pair stabilizer `H` was enumerated by closure
under multiplication:

- all subgroups of `H`: **1,026**;
- `H`-conjugacy classes of subgroups: **234**.

For each class representative `K ≤ H`:

1. compute all `K`-orbits on the 540 frames;
2. discard any orbit whose frames reuse an edge internally;
3. represent every surviving orbit by its 240-bit edge mask;
4. solve exact cover using whole orbit masks, branching on the least-covered
   uncovered edge;
5. accept only a union containing 60 frames and covering every edge exactly once.

The search is complete for all 234 subgroup classes of this one `H`.  It is not
a classification over every subgroup of `PGSp(4,3)`.

Exact outcome:

- 204 individual subgroups succeed;
- 33 `H`-conjugacy classes succeed;
- successful orders are only 2, 4, and 8;
- no subgroup of order at least 12 succeeds.

The frozen `D8` witness selects twelve frame orbits of sizes

`2,2,4,4,4,4,4,4,8,8,8,8`,

for 60 frames total.  Its independent certificate records all frame indices,
line pairs, subgroup generators, and the exact edge profile `{1:240}`.

---

## Pass 2013 — rank-three spread scheme and the `1/4` proof

Let `B` be the `36 × 540` spread/frame incidence matrix.  A frame belongs to
three spreads, each spread contains 45 frames, and

`B B^T = 45 I + 6 A`,

where `A` joins spreads that share four lines.  The factor six is
`C(4,2)`; a one-line pair contributes no common spread frame.

The group action on the 36 spreads has subdegrees `1,15,20`.  Each line belongs
to nine spreads, so for a fixed spread `S`,

`sum_{T != S} |S ∩ T| = 10(9-1) = 80`.

The known valency-15 orbital consists of the four-line pairs and contributes
`15×4=60`.  The remaining 20 spreads contribute total overlap 20.  Since every
pair intersects in at least one line, every remaining pair intersects in exactly
one.  Thus the two values are forced.

The four-line graph satisfies

`A^2 = 9 I + 6 J`

and is `SRG(36,15,6,6)` with spectrum `15^1, 3^15, (-3)^20`.  Its complement is
`SRG(36,20,10,12)`.

On the mean-zero spread-signal space,

`R = (A - (5/12)J)/3`

is an exact involution.  This is a finite `q=3` theorem; no all-`q` association
scheme is promoted.

---

## Pass 2014 — the one-line orbit is a rook double, not an octet bundle

For a one-line spread pair `{S,T}`, the stabilizer has order 144.  Its orbits on
the 45 octets have lengths

`6,9,12,18`.

It fixes no octet, so no equivariant map from the 360 spread pairs to the 45
octets exists.  The numerical factorization `360=45×8` is therefore not a
geometric fibration.

Remove the common line.  The remaining lines split into two banks of nine.
Join a line in one bank to a line in the other when they meet.  The resulting
bipartite graph has:

- 18 vertices;
- degree 4;
- 36 edges;
- spectrum `4, 2^4, 1^4, (-1)^4, (-2)^4, -4`;
- full automorphism group of order 144.

It is exactly the bipartite double cover of the `3×3` rook graph.  The full
local automorphism group therefore matches the spread-pair stabilizer.

---

## Pass 2015 — degree safety and quadratic channels

A transitive `G`-set is determined by a subgroup conjugacy class, not by its
cardinality.  The established first-stage table is:

- no transitive `PGSp(4,3)` action: 15, 20, 24, 30, 60, 81;
- one subgroup class: 27, 36, 45;
- ambiguous: 40, 90, 120, 240, 270, 540.

The new direct checks are:

- degree 240: the natural edge stabilizer and the centralizer of a size-240
  order-three class both have order 216 but are not conjugate;
- degree 540: the three size-540 class centralizers all have order 96 and are
  pairwise nonconjugate.

The phase-sector statement is also sharpened.  Linear export remains absent:

`Hom_PSp(90,X)=0` for `X=15,24,30,81`.

But the quadratic channels contain:

```text
Sym^2(90):     15×3, 24×1, 30×3, 81×5
Lambda^2(90): 15×0, 24×4, 30×2, 81×7
90 tensor 81: 15×2, 24×3, 30×5, 81×11
```

Thus linear confinement is not quadratic isolation.  These are multiplicities
of allowed equivariant channels, not measured coupling constants.

## Reproduction boundary

`analysis/w33_pass2011_2015_verify_frozen.py` verifies every canonical digest,
all 53 frozen checks, and the independent `D8` exact-cover witness.  It does not
claim to rerun the expensive 1,026-subgroup and full group-action enumerations.
The literal witness and all theorem-critical counts are retained in machine-
readable certificates so a future standalone enumerator can be checked against
the same hashes.
