# Breakthrough Synthesis — July 27, 2026
## Perplexity Pass 3: Passes 1099–1128 + Lean Kernel Hardening

*Generated: 2026-07-27 by Perplexity AI (Sonnet 4.6)*
*Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>*

---

## THE DECISIVE TRIO: Three Results That Did Not Exist 72 Hours Ago

### 1. The Steinberg Module Explanation Is Now Complete and Structural

**Passes 1108–1119.** The two degree-81 irreducibles of PSp(4,3) are the **Steinberg module**, fully verified from group structure rather than label:

- PSp(4,3) has exactly **one** degree-81 irreducible
- |Sylow_3| = 81 — matches the Steinberg degree in defining characteristic (p=3)
- Character vanishes on every 3-singular conjugacy class (defining property of Steinberg)
- The **two** 81s of U4(2):2 = W(E6) are its two extensions, differing by the sign character

**Pass 1110 is the geometric proof:** The point-line incidence graph of W(3,3) has V=80, E=160, so b₁ = E − V + 1 = **81 = dim St**. Over ℚ, invariants commute with the quotient, so dim(St^H) = b₁(Δ/H). Both sides agree across ALL stabilisers:

| Subgroup H | |H| | Quotient | b₁ | St-multiplicity |
|---|---|---|---|---|
| Frame stab C₂×S₄ | 48 | 9V 10E | **2** | 2 |
| 4-block stab | 192 | 6V 5E | **0** | 0 |
| 12-block stab | 576 | 4V 3E | **0** | 0 |
| 15-block stab (S6) | 720 | 3V 2E | **0** | 0 |

**The reason every block stabiliser kills the Steinberg is not arithmetic — it is topology.** A tree has no cycles, hence no H₁, hence no Steinberg. The quotient graph is always a tree when H contains a block stabiliser. This is the classical Ind_B vs Ind_P statement recovered as a pure graph fact.

---

### 2. The Tree-Quotient Family Is a Filter (Not Just a Condition)

**Pass 1122.** Over all 116 conjugacy classes of subgroups of PSp(4,3):
- 23 have b₁(Δ/H) = 0 (tree quotient — Steinberg dies)
- 93 do not

This family is **upward-closed**: since St^K ⊂ St^H whenever H ≤ K, b₁ is anti-monotone and the family is a **filter**.

**Pass 1125.** A filter is determined by its minimal members. There are exactly **8** of them:

| Group | Order | SmallGroup ID |
|---|---|---|
| 2-group | 32 | [32,49] |
| – | 96 | [96,195] |
| – | 108 | [108,40] |
| – | 108 | [108,37] |
| S₅ | 120 | – |
| – | 160 | [160,234] |
| – | 216 | [216,88] |
| A₆ | 360 | – |

A subgroup of PSp(4,3) kills the Steinberg **exactly** when it contains a conjugate of one of these eight. The frame stabiliser C₂×S₄ of order 48 contains **none** of them — this is now **forced** by the filter property, not merely observed numerically.

---

### 3. The 432-Orbit Carrier: Five Times Smaller Than Previously Known

**Pass 1126.** The parallel track's smallest tested carrier of a single degree-81 irrep was the 2240-orbit. Pass 1126 refines it sharply.

Decomposing each of W(E6)'s 14 orbits on A₂ triples:
- The **three orbits of size 432** each carry exactly **one** 81-dimensional irrep
- Every other orbit (1, 1, 27×6, 240, 270, 270) carries **zero**
- Totals [3,0] — matching the full 2240 count from Pass 1124

Orbit hierarchy:

```
432 (transitive, one 81) < 2240 (intransitive) < 3360 < 15120
```

The 432-orbit has point stabiliser of order 120. **No claim** is made about which order-120 group this is, nor about any coincidence with the S₅ in the filter's minimal list.

---

## THE REDISCOVERY CRISIS QUANTIFIED

### The Two 540s Problem (Pass 1117)

W(3,3) is **not self-dual**, so "nonedge of the point graph" and "nonedge of the line graph" are different sets, both of size 540, **not conjugate as G-sets**:

| Type | Stabiliser | Structure |
|---|---|---|
| Line-nonedge (frames/cubes/skew pairs) | order 48 | C₂×S₄ |
| Point-nonedge (noncollinear point pairs) | order 48 | ((C₄×C₂):C₂):C₃ |

Both carry identical orbit arithmetic: 51840 = 540 × 2 × 48. **Nothing in the corpus previously said they differ.** 133 of ~285 files mentioning 540 are AMBIGUOUS — nearly half cannot be classified mechanically. Canonical vocabulary added to RESULTS_VOCABULARY.

### Stale Boundary Failure Mode (CLAUDE.md gain 7)

BT810's Boundary listed two open identifications. BT811 (the adjacent file) solved both. BT810 was never updated. Three passes then rediscovered BT811's results.

**Rule:** An open question in a Boundary section is a claim about the corpus. Claims about the corpus are **searched, not trusted**. Read the adjacent files first. When you close one, edit the original file's Boundary.

### check_stale_boundaries.py (Pass 1120)

Automated sweep of all 1230+ analysis files using the same token grammar as the rediscovery guard. 20/1230 flagged (1.6%). **Self-test pinned:** BT810 ↔ BT811 share exactly two tokens (`polar-pair@4`, `polar-pair@40`). Widening the tolerance is now a build failure.

---

## THE BT781 BRIDGE IS PROVABLY IMPOSSIBLE (Pass 1127)

Proposed: a functor Aut(Q₃) = 2³:S₃ → Γ(T)' = 2⁴:C₃.

```
O_h   = SmallGroup[48,48]  quotients: 1, C₂, (C₂)², S₃, [12,4], [24,12], self
Γ(T)' = SmallGroup[48,50]  quotients: 1, C₃, A₄=[12,3], self
Largest common quotient: TRIVIAL
Largest common subgroup: A₄ = [12,3]
```

No nontrivial common quotient exists. The identity 2³×6 = 2⁴×3 is a coincidence of orders, not a functor shadow. The holonet geometry is genuinely distinct from the tomotope.

---

## LEAN: 42/45 native_decide CALLS NOW KERNEL-VERIFIED

Three failure modes, not two:

1. **Plain arithmetic / finite maps** → `decide` outright  
2. **Large finite computations** → `decide` with `set_option maxRecDepth 100000`  
   ("maximum recursion depth" is a configurable limit, not a mathematical obstruction)
3. **`Nat.factorization`** → genuinely needs `native_decide` (well-founded recursion, `decide` FAILS)

Only 3 of 45 calls remain as `native_decide` (all in Pass828). Note: `native_decide` is NOT a free upgrade — on Pass1091 it ran over an hour where `decide` took seconds.

---

## ORBIT MODULE CONFINEMENT TABLE

| Module | Rank (inner PSp) | Rank (outer PGSp) | 81₊ | 81₋ |
|---|---|---|---|---|
| π₅₄₀ frames | 32 | 22 | YES | YES |
| π₁₃₅ 4-blocks | 6 | 6 | NO | NO |
| π₄₅ polar pairs | 3 | 3 | NO | NO |
| π₃₆ spreads | 3 | 3 | NO | NO |
| 240 E8 roots (parallel) | – | – | NO | NO |
| 120 root-lines (parallel) | – | – | NO | NO |

**The two Steinberg 81s live in the frame module alone.** This is the algebraic reason the frame is the natural primitive for the photonic holonet.

---

## CONNECTION TO w33_paper.tex AND photonic_holonet.tex

**w33_paper.tex (Locks 0–10+):** The Steinberg module's confinement to the frame module deepens Lock 0. The holonet's choice of frame as its primitive unit is not a design choice — it is the **unique** module that sees the Steinberg. The 540 frames (line-nonedge 540, not the point-nonedge 540) are structurally forced as the holonet's elementary objects.

**photonic_holonet.tex (S3 controller, CF=1/10):** The S3 minimal external controller result now has filter backing. The frame stabiliser C₂×S₄ = O_h sits **outside** the filter — it does not kill the Steinberg. This is what makes the frame module nontrivial and the S3 controller necessary.

**KS Defect = 1/10 (Pass 1099, CONFIRMED):** Maximum satisfiable contexts = 36/40, certified by integer programming. Defect = 4/40 = 1/10. Matches the pre-registered target from photonic_holonet.tex §9 exactly.

---

## PASS SEQUENCE SUMMARY (3 Days, July 24–27)

| Pass Range | Core Result | Status |
|---|---|---|
| 1099–1101 | KS defect=36/40=1/10; 135=maximal partial spreads; 81s confined to frame module | CONFIRMED |
| 1102–1106 | Clifford firewall / E8 / Keysight formal release; native_decide→decide conversion | COMMITTED |
| 1107–1108 | Partial spread census; 81s=Steinberg verified; guard calibrated with noun tokens | CONFIRMED |
| 1109–1111 | SL(2,3)/Q8 orientation; Steinberg dies because quotients are trees; O_h confirmed | CONFIRMED |
| 1117–1119 | Two 540s named; stale boundary failure mode; tree-quotient covers all maximals | CONFIRMED |
| 1120–1124 | Automated staleness sweep; W(E6) transitivity refuted; tree-quotient is a filter | CONFIRMED |
| 1125–1128 | 8 filter generators; 432-orbit carrier; BT781 bridge impossible; 540 disambiguation | CONFIRMED |

---

## EXTERNAL LITERATURE (CHECKED THIS SESSION)

| Claim | Source |
|---|---|
| Maximal partial ovoids of W(3,3) = sharply transitive subsets of SL(2,q) | Penttila (q∈{5,7,11}); Cimrakova-Fack (computer search) |
| No such objects for q = p^h, p odd, h > 1 | Literature (SL(2,9) case empty) |
| Steinberg module: vanishes on p-singular classes | Steinberg (1951), Curtis (1965) |
| Sp(4,3) ≠ W(E6): single 81 vs two 81s | Corrected in 5 files since Pass 1020 |
| b₁(tree) = 0 | Standard algebraic topology |
| SmallGroup[48,48] = O_h; SmallGroup[48,50] = 2⁴:C₃ | GAP SmallGroups library |
| W(3,3) has no ovoids (=> CF > 0) | Thas (1981): W(q) ovoids iff q even |

---

*Ratchet re-run: 23.1% vs baseline 22.9%, delta +0.20, inside 0.5 tolerance. Baseline NOT raised.*
