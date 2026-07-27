# Passes 1120–1124 — a staleness sweep, the 540 audit, and three exact answers

Five items, plus one result that came from reading the supplied polytope papers and
turned out to be prior art three files deep.

---

## Pass 1120 — a sweep for boundaries a later file already answered

The BT810 → BT811 failure (two passes withdrawn) was not a discipline problem; it
was structural. Nothing in this workflow edits a file's Boundary when a later pass
closes it, so `scripts/check_stale_boundaries.py` now searches for the pattern
mechanically: extract the result-tokens of each boundary section with the **same
grammar the rediscovery guard uses**, then look for them in strictly later files
(ordered by BT/pass number or ISO date, which is how this corpus actually sorts).

```text
scanned 1230 analysis/*.md
  20 boundaries have a later file sharing >= 2 result tokens   (1.6%)
```

A usable signal rate, and it flags my own `w33_pass1117_1119` too — the tool is not
special-cased for anyone.

**Self-test pinned.** BT810's *original* boundary (recovered from git) shares
exactly two tokens with BT811 — `polar-pair@4` and `polar-pair@40` — so the case
that motivated the tool fires at the threshold. If the threshold is ever raised
above 2, or the noun-number tokens narrowed, this goes silent again and the next
two passes get spent. The self-test makes that a test failure instead.

Top candidates worth a human read include
`2026-07-08_pass70_15vector_doily_attack → pass72` (`spread@15, spread@3, spread@5`)
and `BT809_register_f4_regular_spread → BT836_gc_hemicells_in_spreads`
(`spread@10, spread@2, spread@45`).

---

## Pass 1121 — which 540 did the corpus actually mean?

Pass 1117 showed there are **two** non-isomorphic 540s. Classifying every file
that mentions 540 by whether its surrounding window uses line-vocabulary
(cube, skew, frame, 3A₁, chart) or point-vocabulary (noncollinear, nonedge,
quadrangle):

```text
LINE-nonedge  : 130 files
POINT-nonedge :  22 files
AMBIGUOUS     : 133 files      <- both vocabularies in the same window
```

**Nearly half cannot be classified mechanically.** That is the real finding: the
ambiguity is not a corner case, it is the modal case, and 133 files would each need
a human to say which object they meant. The 22 point-nonedge files include the
`levi_next5` series and the `bt767–bt779` octet run, which is where the
1620-quadrangle arithmetic lives.

---

## Pass 1122 — the tree-quotient family is a FILTER, and the converse fails

Pass 1119 showed every maximal subgroup has `b₁(Δ/H) = 0`. Extending to **all 116
conjugacy classes of subgroups** of PSp(4,3):

```text
TREE quotients (b1 = 0) :  23 of 116
non-tree      (b1 > 0)  :  93 of 116
```

So tree-quotient is **not** equivalent to maximal — 23 classes, only 5 maximal. But
the family has exact structure. Since `St^K ⊆ St^H` whenever `H ≤ K`, the dimension
`b₁ = dim St^H` is **anti-monotone**, so the tree-quotient set is **upward closed**:
a filter in the subgroup lattice. Its smallest member has order **32**:

| index | \|H\| | structure |
|---|---|---|
| 1 | 25920 | O(5,3) |
| 27 | 960 | (C₂)⁴ : A₅ |
| 36 | 720 | S₆ ← my 15-block stabiliser |
| 40, 40 | 648 | the two parabolics |
| 45 | 576 | ← my 12-block stabiliser |
| 135 | 192 | ← my 4-block stabiliser |
| … | … | (23 classes in all) |
| 810 | 32 | (C₂)³ : (C₂)² ← minimal |

All three of my block stabilisers appear, as they must. The **frame stabiliser
(index 540, order 48, C₂×S₄) does not**, nor does the Borel — matching b₁ = 2 and
b₁ = 1 exactly. Because the family is upward closed, the frame stabiliser containing
no tree subgroup is forced, not coincidental.

---

## Pass 1123 — BT811's 16 + 24 is exactly my 12-block

BT811 records that the index-45 maximal has line orbits `40 = 16 + 24`, the 16 being
the cross-transversals meeting both L and L⊥. Comparing against the 12-block that
Pass 1097 maps to that polar pair:

```text
cross-transversals meeting both L and Lperp : 16        (BT811's number, confirmed)
distinct lines used by the block's 12 frames : 24
intersection of the two sets                 : 0
```

**Disjoint.** The 12-block's frames use the complementary 24-orbit *entirely* and
touch none of the 16. And since 12 frames × 2 = 24 = the number of distinct lines,
each line is used exactly once: the 12-block is a **perfect matching on BT811's
24-orbit**, the same shape Pass 1100 found for the 4-blocks (a perfect matching on
8 lines forming a maximal partial spread).

So BT811's orbit anatomy and the block system are two views of one object, and the
16/24 split is precisely "lines a block can use" versus "lines it cannot".

---

## Pass 1124 — W(E6) confirms the parallel track's multiplicities and refutes the transitivity

Building W(E6) canonically as the **pointwise stabiliser of one A₂ triple** in
W(E₈) (since E₈ ⊃ A₂ × E₆):

```text
|pointwise stabiliser of an A2 triple| = 51840          = |W(E6)|   ✓
degree-81 irreducibles                 = 2              (so this IS U4(2):2,
                                                         not the Sp(4,3) of Pass 1020)
degree-81 multiplicities in the 2240   = [3, 0]         ✓ matches Pass 1113
```

**The multiplicities are confirmed** — one 81 occurs three times, the other zero
times, exactly as Pass 1113 reports. The ± labelling is convention.

**But the 2240 is not a transitive W(E6)-set:**

```text
transitive : false
orbits     : [1, 1, 27, 27, 27, 27, 27, 27, 240, 270, 270, 432, 432, 432]
rank       : 1193
```

Fourteen orbits, including **two fixed points** — the chosen A₂ triple itself and
its negative, both fixed because W(E6) fixes that A₂ pointwise. So "the
2240-element W(E6)-set" is fourteen carriers, and a minimality claim
`2240 < 3360 < 15120` should say which orbit carries the 3·81 before comparing it
with a transitive 3360. This confirms and sharpens the caveat raised in Pass 1119;
it does not contradict the multiplicities.

(For contrast, Pass 1119 computed the same 2240 under **Sp(4,3)** — a different
order-51840 group with a *single* 81 — and got orbits `[80, 2160]`. Both are right;
they are different subgroups of W(E₈).)

---

## What the supplied polytope papers actually produced: prior art, three deep

Reading Monson–Pellicer–Williams and Monson–Schulte suggested a sharp test. The
tomotope's automorphism group has **order 96** and is `Z₂⁴ ⋊ S₃` (it is B̃₃ reduced
mod 2); the 540-object stabiliser in PGSp(4,3) also has **order 96**. Are they the
same group?

**BT781 already ran exactly that test**, and its answer is a decisive negative:

```text
cube chart stabilizer:      2^3 : S3   = 48   {1:1, 2:19, 3:8, 4:12, 6:8}
tomotope derived subgroup:  2^4 : C3   = 48   {1:1, 2:15, 3:32}
```

not isomorphic — "one tomotope binary bit = one cube reflection bit". And its
element-order fingerprint `{1:1, 2:19, 3:8, 4:12, 6:8}` is *the same fingerprint*
BT811 later used to confirm O_h, which Pass 1111 then rediscovered. **The same fact
is in the corpus three times: BT781 → BT811 → Pass 1111.** `2³:S₃ ≅ C₂ × S₄ = O_h`,
so all three are the same group under three names.

That is the strongest single argument for Pass 1120's sweep and for
`RESULTS_VOCABULARY.md`: the corpus does not fail to contain things, it fails to
find what it contains.

BT781 also ends with "Next experiment: BT782 should build the explicit bridge
functor `Aut(Q3)=2³:S₃ → Γ(T)'=2⁴:C₃`". That is a live open question and is
**not** claimed here.

## Prior art

- [BT781](analysis/BT781_cube_tomotope_48_split.md) — owns the cube/tomotope 48 split and the fingerprint.
- [BT811](analysis/BT811_platonic_fine_print.md) — owns O_h and the 16 + 24 line orbits.
- [BT810](analysis/BT810_completed_geography_schlafli.md) — the geography and the stale boundary.
- [Pass 1097](analysis/w33_pass1097_name_the_frame_quotients.g), [Pass 1100](analysis/w33_pass1100_name_the_135.g), [Pass 1119](analysis/w33_pass1117_1119_aliases_orbits_trees.md).
- Pass 1113 (parallel track) — the A₂-triple multiplicities confirmed above.
- Monson, Pellicer, Williams, *The Tomotope*, Ars Math. Contemp. 5 (2012); Monson & Schulte, *Semiregular polytopes and amalgamated C-groups*, Adv. Math. 229 (2012).
