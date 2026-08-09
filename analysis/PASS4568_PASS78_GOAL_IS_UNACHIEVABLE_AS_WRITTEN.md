# Pass 4568 — Pass 78's outstanding goal cannot be done as written, and here is the object that can

Pass 4566 cited `w33_pass78_equivariant_closure.py:109` as naming the natural completion of
the L-function work:

> *"It is not yet the full edge-zeta Artin factorization across all 34 irreducibles."*

I treated that as a well-posed target and queued it. A scoping pass says it is not one.

## 1. The 34 irreducibles are Sp(4,3)'s — but Sp(4,3) is not what acts

`w33_pass77_group_out.txt` holds the degree list verbatim:

```
Sp43_degrees=[1,4,4,5,5,6,10,10,15,15,20,20,20,20,20,20,24,30,30,30,
              36,36,40,40,45,45,60,60,60,60,64,64,80,81]
```

34 entries, Σd² = 51840, top degree 81. So the "34 irreducibles" are **Sp(4,3)**, order
51840.

But the same file records `perm_group_order=25920`, `rank_action=3`. **The group acting on
the 40 points is PSp(4,3)**, the quotient by the centre — and PSp(4,3) ≅ U₄(2) has **20**
conjugacy classes, not 34. Pass 78's sentence silently mixes the acting quotient with its
double cover.

## 2. The blocking fact: no Sp(4,3)-cover exists, and none can

An Artin–Ihara factorization requires a **graph cover with a deck group**. The zeta of a
`G`-cover factors as `∏_ρ L(u,ρ)^{dim ρ}` over the irreps of the **deck** group — and a deck
group must act **freely**.

Sp(4,3) acts on W(3,3)'s 40 points with stabilizers of order 51840/40 = **1296**. The action
is very far from free, so W(3,3) is not a `G`-cover of anything for this `G`. A genuine
cover with Deck ≅ Sp(4,3) would need **40 × 51840 = 2,073,600 vertices** — an object nobody
is proposing to build.

The only graph covers that exist in this corpus are the **Z₂ double covers** from ±1
signings (`w33_pass4436_4438_lfunction_cover_landscape.py:89`, 80 vertices), which is exactly
the one-dimensional case Pass 4436 already did. The cyclic lifts elsewhere
(`PART_CCCCV_w33_cyclic_cover_distance_search_results.json`, n = 480 and 720) are CSS-code
constructions, not zeta covers.

**So the sentence at line 109 describes a factorization of an object that does not exist.**

## 3. What the correct completion actually is

Not an Artin factorization of a cover — an **equivariant decomposition of the edge module**.

W(3,3) has 480 directed arcs. The arc stabilizer has order 51840/480 = **108**, so as a
G-module

```
C^480  =  Ind_H^G 1,      |H| = 108
```

Only irreps possessing an `H`-fixed vector appear, with multiplicities summing as
`Σ_ρ m_ρ · dim ρ = 480`. The Hashimoto operator commutes with the action, so it block-
diagonalises over that decomposition — and the largest possible block is bounded by the
largest irrep degree, **81**. That is trivially tractable in numpy.

What Pass 78 *achieved* is the rank-3 piece: it factorizes the Ihara–Bass denominator on the
**40-dimensional point permutation module only**, into

```
(1 − 12u + 11u²)¹ · (1 − 2u + 11u²)²⁴ · (1 + 4u + 11u²)¹⁵ · (1 − u²)²⁰⁰
```

with the degree check `2(1 + 24 + 15) + 400 = 480`. The gap it named is the step from the
**point module** to the **arc module** — genuinely undone, genuinely worth doing, and not
what the sentence says.

## 4. Cost

One GAP script for the 34×34 character table (`w33_pass1075_gsp43_character_table.g` already
loads it) plus the permutation character of the order-108 arc stabilizer; then ~150 lines of
numpy to project and block-diagonalise. The corpus currently holds **degrees only**, no full
table.

## 5. The pattern this belongs to

This is the seventh time this session that a stated target turned out to rest on an
unchecked premise — and the first where the target was not mine. The premise here was
*"there is a cover whose deck group has 34 irreps"*, and it is false because the group with
34 irreps does not act freely, or even faithfully, on the object in question.

Recorded rather than attempted. `CLAUDE.md`'s rule is to state what would make a computation
invalid before running it; here the answer is that the computation has no domain.

## Evidence boundary

The degree list and `perm_group_order` are quoted from `w33_pass77_group_out.txt`; the
count of 34 entries and Σd² = 51840 were verified. The claim that PSp(4,3) has 20 classes is
standard and is cited, not recomputed here. The freeness argument uses only |G|/|orbit| and
is exact. No character table was computed, and the proposed arc-module decomposition is
**scoped, not performed** — its multiplicities are unknown until the permutation character
of the order-108 stabilizer is taken.
