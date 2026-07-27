# Passes 1117–1119 — two 540s, a stale open-question list, and the tree characterisation

Three intended results. **Two were already in the corpus**, one survives and is
sharper than expected, and the way the two were lost is a failure mode this
repository has not previously named.

---

## The failure mode: a file's "Open:" list is not evidence

BT810 ends with

> Open: … and the binary octahedral question: is the order-48 chart group 2O or
> O_h as an abstract group (both order 48 — settle by element orders)?
> … the 2T x 2T action on the 9+9 points off the polar pair … compute the point
> orbits of the index-45 maximal

I read that, took it at face value, and answered both — Pass 1111 (O_h) last
batch and Pass 1118 (the orbits) this one.

**Both were already answered by BT811**, whose title is
*"Platonic Fine Print: O_h Confirmed, and the Polar-Pair Anatomy"* and whose first
line is *"Settles the two open identifications from BT810 by direct computation."*
It has the same element-order profile `{1:1, 2:19, 3:8, 4:12, 6:8}`, the same
exclusion of 2O, the same `40 points = 8 + 32` with the same "4+4 fused by the
polarity" mechanism — and it goes further, giving the line orbits `40 = 16 + 24`
and identifying the 16 as the cross-transversals meeting both L and L^⊥.

BT810 was never updated. Its Boundary section has been stale by exactly one file
since BT811 was written.

**So: an "Open:" list records what was open when that file was written, not what
is open now.** Nothing in this project's workflow edits a file's boundary when a
later pass closes it, and BT810→BT811 are adjacent numbers by the same author.
Before answering a stated open question, check whether the *next* file already
did. Both of my closures are withdrawn; BT811 owns them, and BT810 now points at
it.

The guard caught this, twice, through the noun-number tokens added in Pass 1107
(`polar-pair@32` → BT811). That token class has now produced four real catches in
two batches.

---

## Pass 1117 — there are TWO 540s and they are not the same object (SURVIVES)

The 540 appears in this corpus as `frames`, `skew pairs`, `cubes`, `nonedges`,
and the `540-class`. Four denote one thing. **One does not.**

W(3,3) is **not self-dual**, so "nonedge" of the *point* graph and of the *line*
graph are different objects, and both number 540:

| | count | stabiliser order | stabiliser type |
|---|---|---|---|
| line-nonedges (frames / skew pairs / cubes) | 540 | 48 | `C₂ × S₄` |
| point-nonedges (noncollinear point pairs) | 540 | 48 | `((C₄ × C₂):C₂):C₃` |

The two stabilisers are **not conjugate in PSp(4,3)**, so the two G-sets are
**not isomorphic**. Same cardinality, same stabiliser *order*, different objects.

This is not hypothetical. Both are already in the corpus, carrying the **same
arithmetic**:

- BT773: "540 cubes in W(3,3), one per 3A₁ involution", `51840 = 540 × 2 × 48`
- `analysis/2026-07-10_levi_next5_v3.md`: "540 unordered noncollinear point pairs",
  fiber 96, `51840 = 2 · 540 · 48`
- `analysis/w33_minimal_support_geometry.py`: "nonedges × C(μ,2)/2 = 540 × 6/2"
  — noncollinear **point** pairs

Nothing found says these are different sets. All the frame-action work (rank 32,
the three block systems, the 135/45/36 quotients) is about the **line**-nonedge
540; the 1620-quadrangle-support work is about the **point**-nonedge 540. The
rule is to write *point*-nonedge or *line*-nonedge and never bare "nonedge".
`RESULTS_VOCABULARY.md` now carries the table.

---

## Pass 1119 — every maximal subgroup has a tree quotient (SURVIVES, narrowed)

**First, prior art.** `β₁ = 160 − 80 + 1 = 81` for the point–line Levi graph is
**BT586's**, which calls it "the protected W33 homology sector, H₁ = 81". Pass
1110 recomputed it without citing that. BT586 does **not** identify it with the
Steinberg module and computes **no** quotients, so what follows is still new — but
the raw 81 is not.

Extending to every maximal subgroup of PSp(4,3), plus the Borel:

| H | \|H\| | index | b₁(Δ/H) | Steinberg multiplicity | agree |
|---|---|---|---|---|---|
| maximal | 960 | 27 | 0 | 0 | ✓ |
| maximal (S₆) | 720 | 36 | 0 | 0 | ✓ |
| maximal (parabolic) | 648 | 40 | 0 | 0 | ✓ |
| maximal (parabolic) | 648 | 40 | 0 | 0 | ✓ |
| maximal | 576 | 45 | 0 | 0 | ✓ |
| **Borel** | 162 | 160 | **1** | **1** | ✓ |
| **frame stabiliser** | 48 | 540 | **2** | **2** | ✓ |

Multiplicities from the character table as fixed-point counts, cycle ranks from
the quotient graphs — independent computations, agreeing in all seven rows.

**Every maximal subgroup of PSp(4,3) has a tree quotient**, hence kills the
Steinberg. It first appears at the **Borel** with exactly one independent cycle —
the classical statement that St occurs once in `Ind_B^G 1` and not at all in
`Ind_P^G 1` for a proper parabolic *P > B*, recovered here as a graph fact rather
than quoted — and doubles at the frame stabiliser. The block stabilisers of
Pass 1110 were instances of a rule that covers every maximal.

---

## Cross-track check: the parallel Pass 1113 carrier claim

Pass 1113 reports, for the 2240 unordered A₂ root triples {α,β,γ} with sum 0,
`⟨χ_A2, 81₊⟩ = 0` and `⟨χ_A2, 81₋⟩ = 3`. Recomputed independently from the E₈
roots and the Springer tower of Pass 1020:

```text
A₂ root triples with α+β+γ = 0 : 2240    ✓ agrees
|K|                             : 51840   ✓ agrees
degree-81 multiplicity          : 3       ✓ agrees
```

**The 3 is confirmed.** Two conditions belong with it.

**The group is Sp(4,3), not W(E6).** The tower `K = [C_{W(E8)}(w), C_{W(E8)}(w)]`
has 34 irreducibles of degrees `1, 4, 4, 5, 5, 6, …, 80, 81` — a **single** 81.
The degree-4 and degree-5 constituents are the Weil representations of Sp(4,3),
identifying `K = Sp(4,3) = 2.U4(2)`. W(E6) = U4(2):2 is a **different** group of
the same order 51840, with 25 irreducibles and **two** 81s. So `⟨χ_A2, 81₊⟩ = 0`
is not a statement one can make inside this tower — there is no 81₊ here. This is
the Sp(4,3) ≇ W(E6) distinction Pass 1020 had to correct in five files.

**The 2240 is not transitive.** Under Sp(4,3) it splits `[80, 2160]`, rank 146.
A carrier-minimality claim (2240 < 3360 < 15120) should say which orbit carries
the 3·81, since an intransitive 2240 is not straightforwardly comparable to a
transitive 3360.

Neither point contradicts the parallel result; both are conditions for reading it
correctly. If their group is genuinely U4(2):2 and genuinely transitive on the
2240, the two computations concern different subgroups of W(E₈) and both stand —
but "the 51840-element group acting on the 2240 triples" does not determine which.

---

## Ratchet

Re-run on the fresh corpus after this batch: **23.1%** against a baseline of
22.9%, delta **+0.20**, inside the 0.5 tolerance. Merge list 863 vs 859. The
baseline is deliberately **not** raised.

## Prior art

- [BT811](analysis/BT811_platonic_fine_print.md) — **owns** the O_h confirmation and the 8+32 / 16+24 orbit anatomy.
- [BT810](analysis/BT810_completed_geography_schlafli.md) — the geography, and the stale Boundary now corrected.
- [BT586](analysis/BT586_fiber_vs_levi_homology_separation_note.md) — **owns** β₁(Levi) = 81.
- [BT773](analysis/BT773_involution_cube_theorem.md) — the 540 cubes.
- [2026-07-10_levi_next5_v3.md](analysis/2026-07-10_levi_next5_v3.md) — the 540 noncollinear **point** pairs.
- [Pass 1020](analysis/w33_pass1020_e8_transitive_51840.g) — the Springer tower and Sp(4,3) ≇ W(E6).
- Pass 1113 (parallel track) — the A₂-triple carrier claim checked above.
