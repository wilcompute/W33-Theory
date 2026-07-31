# Passes 1375–1378 — the stabiliser is S₅, the tomotope checked against its own paper, A₄ as the derived core, and why the guard could not see any of it

Four results. One refutes a value that was frozen into `data/ALIAS_REGISTRY.json`
as canonical; one checks ~50 files' worth of tomotope claims against the primary
source for the first time; one finds the object BT781–BT783 were circling; and one
diagnoses, by measurement, why this corpus keeps rediscovering group theory
specifically.

---

## Pass 1375 — the 432-orbit stabiliser is S₅, and the "order 60" correction is wrong three times over

Pass 1126 found that W(E₆)'s three orbits of size 432 on the 2240 A₂ root triples
each carry exactly one degree-81 irreducible, reported the point stabiliser as
order 120, and deliberately declined to name it.

Commit `2da603e52` issued a correction, and froze it into the alias registry:

> **Key correction resolved:** `|Sp(4,3)| = 25920`. For orbit size 432, the
> stabilizer order is `25920/432 = 60`, consistent with `A₅ ≅ PSL(2,5)`, not
> order-120 `S₅`.

Every step of that is wrong, and the script it shipped could not have detected it.

```text
|Sp(4,3)|   = 51840          <- not 25920
|PSp(4,3)|  = 25920          <- this is what 25920 is
|Sp| = 2|PSp|                 true    (Sp(4,3) = 2.U4(2), the DOUBLE COVER)

group acting on the 2240 A2 triples = W(E6) = U4(2):2, order 51840
  #Irr = 25   (25 = U4(2):2;  34 = Sp(4,3))   -> NOT Sp(4,3) either
```

So the divisor is `51840/432 = 120`, and the correction divides by the order of a
group that is not acting — the exact `Sp(4,3) ≇ W(E₆)` conflation Pass 1020 had to
repair in five files.

It also mislocates the object. The shipped GAP script searches for 432-orbits
among the 2-element subsets of the 40 points of W(3,3). Run:

```text
orbits of PSp(4,3) on the 780 point-pairs : [240, 540]
any orbit of size 432 there?              : false
```

There are only `C(40,2) = 780` such pairs and they split `240 + 540`. The script
prints nothing, and would have done so silently. The 432s live on the 2240 A₂ root
triples in E₈.

**The answer.** With `W(E₆)` built correctly as the pointwise stabiliser of an A₂
triple in `W(E₈)`:

```text
orbits on the 2240 : [1, 1, 27×6, 240, 270, 270, 432, 432, 432]      sum 2240
each 432-orbit  |stab| = 120 = 51840/432
   IdGroup             = [120, 34]
   StructureDescription= S5
   element orders      = 1,2,2,3,4,5,6
   isomorphic to SL(2,5)?  false
   isomorphic to C2 x A5?  false
   stab1 ~ stab2 ~ stab3 conjugate in W(E6)?   ALL TRUE
```

**The stabiliser is S₅, and the three orbits are conjugate — one orbit type, not
three.** The 60 in the retracted correction is not meaningless, but it names a
different object:

```text
|S5 ∩ W(E6)'| = |S5 ∩ PSp(4,3)| = 60,   IdGroup [60,5] = A5
```

It is the intersection with the simple group, arrived at by wrong arithmetic on
the wrong group.

### The S₅ coincidence, resolved rather than asserted

Pass 1125 refused to comment on the fact that its eight minimal tree-filter
generators include an `S₅ = SmallGroup[120,34]`, and that the 432-stabiliser also
has order 120 — "two order-120 objects in one session is exactly the coincidence
this corpus gets burned by." Both are now named, and they are **provably different
subgroups**:

| | Pass 1125's S₅ | Pass 1375's S₅ |
|---|---|---|
| lives in | `PSp(4,3)`, index 216 | `W(E₆) = U4(2):2` |
| inside the simple group? | **yes** | **no** — meets it in A₅ |
| kills the Steinberg? | **yes** (minimal tree generator) | its A₅ part does **not** |

Since `PSp(4,3) ⊴ W(E₆)`, conjugation preserves containment in it, so the two S₅'s
are **not conjugate in W(E₆)**. Abstractly isomorphic, structurally distinct: one
sits inside the simple group and kills the Steinberg module; the other is split
across the outer coset and stabilises the Steinberg's carrier. The coincidence was
real and it is not a bridge.

---

## Pass 1376 — the tomotope, checked against its own paper for the first time

This repository has roughly fifty tomotope files. **Every one of them works from
restated numbers.** A grep for the actual published permutations —

```text
rho0 = (5,10)(6,9)(7,12)(8,11)     rho2 = (5,9)(6,10)(7,11)(8,12)
rho1 = (1,6)(2,5)(3,8)(4,7)        rho3 = (5,8)(6,7)(9,12)(10,11)
```

(Monson–Pellicer–Williams, *The Tomotope*, Ars Math. Contemp. **5** (2012), p. 9)
— returns nothing. The group has been described here dozens of times and never
once constructed. Constructing it:

```text
|Gamma(T)|           = 96                       <- literature value, CONFIRMED
IdGroup              = [96, 227] = (C2^4 : C3) : C2 = 2^4 : S3
transitive on 12     = true
Gamma(T)'            = [48, 50] = 2^4 : C3      <- BT781/BT783, CONFIRMED
  centre order       = 1                        <- BT783, CONFIRMED
  abelianisation     = C3                       <- BT783, CONFIRMED
  index-2 subgroup   = none                     <- BT783, CONFIRMED
```

**BT781 and BT783 are correct.** Their structural claims, which the corpus has been
propagating on trust for dozens of files, hold against the primary source.

### One thing the corpus has been saying loosely

The most-cited fact about the tomotope here is that it "fails the intersection
condition, and is therefore not an abstract polytope". Tested directly on the
published generators:

```text
intersection condition  <rho_I> ∩ <rho_J> = <rho_{I∩J}>
tested 256 pairs (I,J);  FAILURES = 0       -> the condition HOLDS for Aut(T)
```

The failure in the literature is a property of the **monodromy (connection) group**,
not of `Aut(T)`. `Aut(T)` satisfies the intersection condition. What actually fails
here, and fails first, is the *string* condition:

```text
(rho0 rho2)^2 = 1 ?  true
(rho0 rho3)^2 = 1 ?  true
(rho1 rho3)^2 = 1 ?  FALSE
```

so `⟨ρ₀…ρ₃⟩` is not a string group at all in this labelling, and the intersection
condition is not even the operative obstruction at the automorphism level. Files
that attribute the IC failure to `Γ(T)` should say `Mon(T)`.

---

## Pass 1377 — A₄ is the derived core, and the 540 frames are not polytope facets

### The order-96 comparison nobody had run

`Γ(T)` has order 96. So does the 540-frame stabiliser in `PGSp(4,3)`. BT781
compared their order-**48** halves and got a negative. The 96s had never been
compared:

```text
Gamma(T)                            = [96, 227] = 2^4 : S3
frame stabiliser in PGSp(4,3)       = [96, 226] = C2 x C2 x S4
isomorphic?                           FALSE
```

Adjacent SmallGroup IDs, different groups. The negative now holds at both levels.

### What both sides actually share

```text
frame stabiliser in PSp(4,3)   = [48,48] = C2 x S4 = O_h,  derived subgroup = A4
frame stabiliser in PGSp(4,3)  = [96,226],                 derived subgroup = A4
Gamma(T)' = 2^4:C3 = [48,50]                            contains 2^2:C3 = A4
largest common subgroup of O_h and Gamma(T)'  (Pass 1127)          = A4
```

**A₄ is not an artefact of the comparison — it is the derived subgroup of the frame
stabiliser itself, at both levels of the group.** BT781/BT782 looked for the
"exchange rate" between the two order-48 spendings of 48 and framed it as a
quotient. It is not a quotient (Pass 1127: no nontrivial common quotient exists at
all); it is a **shared derived core**, approached from below by both sides.

`A₄ = 2²:C₃` is the rotation group of the tetrahedron, and the tomotope's cells are
four tetrahedra and four hemioctahedra. Whether that is the reason is **not**
claimed here — it is the next experiment, stated as a question.

### The 540 frames are not the facets of a rank-4 polytope

`O_h = Aut(cube)` is a string C-group of type `{4,3}`, so it is a legitimate
facet-group candidate: if it extends to a rank-4 string C-group on all of
`PSp(4,3)`, the 540 frames are the facets of an abstract regular 4-polytope with
25920 flags. Searched exhaustively over the extensions:

```text
string C-group {4,3} generating triples in O_h            : 48
candidate rho3 (involutions centralising rho0, rho1)      : 3
rank-4 string C-group extending the frame cube            : NONE
```

A clean obstruction. (That *some* rank-4 regular polytope exists for `U4(2)` is
published — Leemans & Vauthier, *An atlas of abstract regular polytopes for small
groups*, 2006 — and is not claimed here. The question answered is whether the
**frame** stabiliser is one of the facet groups. It is not.)

---

## Pass 1378 — the guard was blind to group notation, and that is measurable

Pass 1127 rediscovered BT783. The interesting part is not the mistake but its
cause, which is mechanical and was measured, not guessed.

`scripts/check_stale_boundaries.py` **did** find BT781's boundary section. It then
extracted from it:

```text
BT781 boundary tokens: []          <- zero
```

The entire grammar — code parameters `[[n,k,d]]`, slash-sequences, `noun@number` —
is blind to

```text
Aut(Q3)=2^3:S3  -->  Gamma(T)'=2^4:C3
```

which is the single most common way a result is stated in this corpus. The
threshold was never the problem; there was nothing to threshold.

`group_tokens()` in `scripts/check_rediscovery.py` fixes it. The normalisation
matters as much as the matching, because this repo writes one group five ways —
`2^3:S3`, `C2^3 : S3`, `(C2 x C2 x C2):S3`, `SmallGroup[48,48]`, `C2 x S4` — so
cyclic factor lists are collapsed to powers and the `C`/`Z` prefix dropped:

```text
BT781 boundary  -> {grp:2^3:S3, grp:2^4:3, grp:Q3, grp:S3}
  vs BT782      :  4 shared tokens
  vs BT783      :  2 shared tokens
```

Both now clear the ≥2 threshold. The gated self-test strengthens rather than
weakens: BT810 vs BT811 goes from 2 shared tokens to **5**.

---

## Confirmed from the parallel tracks

- **The shifted-adjacency erratum is right.** Rebuilt independently from the 40
  projective points: `spec(A) = 12¹ ⊕ 2²⁴ ⊕ (−4)¹⁵`, so `spec(D) = 11¹ ⊕ 1²⁴ ⊕
  (−5)¹⁵`, `Tr D = −40`, `Tr D² = 520`, `Tr D³ = −520`, and the historical cubic
  evaluates to `1296, −64, 80` on the three true eigenvalues with
  `rank p_old(D) = 40` — it annihilates nothing. Independently reproduced.
- **The 2240 decomposition is right.** Its trivial-multiplicity 14 equals the orbit
  count, and its multiplicity-square sum is `1193`, matching the rank computed in
  Pass 1124 by a different route.
- **`120 = 40 lines × 3 perfect matchings` is arithmetically sound**: the line
  stabiliser in `PGSp(4,3)` has order `51840/40 = 1296`, inducing `S₄` on the four
  points, and a matching stabiliser `D₈` of index 3 gives `1296/3 = 432 = 51840/120`.

## Prior art

- [BT781](analysis/BT781_cube_tomotope_48_split.md) — the 48-split; its boundary now points forward.
- [BT782](analysis/BT782_cube_tomotope_bridge_program.md), [BT783](analysis/BT783_cube_tomotope_obstruction.md) — **own** the bridge refutation.
- [Pass 1020](analysis/w33_pass1020_e8_transitive_51840.g) — `Sp(4,3) ≇ W(E6)`, the distinction the retracted correction lost.
- [Pass 1124](analysis/w33_pass1120_1124_boundaries_aliases_trees.md), [Pass 1126](analysis/w33_pass1125_1128_filter_carrier_bridge.md) — the 14 orbits and the 3×81.
- Monson, Pellicer & Williams, *The Tomotope*, Ars Math. Contemp. **5** (2012) — the generators.
- Leemans & Vauthier, *An atlas of abstract regular polytopes for small groups* (2006) — rank-4 polytopes for `U4(2)`.
