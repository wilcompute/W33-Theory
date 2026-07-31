# Passes 1475–1479 — the physical sector's sign is pinned, the degree-90 guess is refuted, and the hemicell obstruction is located

Five items. One answers the sharpest open physics question; two are refutations
of my own proposals; one measures a guard I had been extending by hand and finds
it covered under a quarter of the risk.

---

## Pass 1475 — the resolution, now a SAT instance, still open

The 9-colouring reformulation encodes directly:

```text
variables : x[f][c],  540 frames x 9 classes
(a) each frame exactly one class
(b) for each EDGE and each class, exactly one of the 9 frames through it
    has that class   <- this IS "every class is an exact cover", and it
                        forces the class sizes to 60 automatically
symmetry break: fix the classes of the 9 frames through edge 1
```

CaDiCaL did not decide it in ten minutes. That is itself informative — the
instance is small (a few thousand variables) and genuinely hard, which is
consistent with four hand-rolled searches also failing. **Open**, and now
open in a form another solver or a longer run can simply be pointed at.

---

## Pass 1476 — the degree-90 is NOT the hyperbolic lines (my guess, refuted)

The natural carrier for `PGSp`'s unique degree-90 irreducible would be the 90
hyperbolic lines — the nondegenerate 2-spaces, on which the polarity acts freely
to give the 45 polar pairs. Built and decomposed:

```text
hyperbolic lines (nondegenerate 2-spaces) : 90   ✓
transitive under PSp(4,3)                 : yes
permutation character over PSp            : 1 + 15 + 20 + 24 + 30 = 90
```

**No degree-45 and no degree-90 constituent.** The 90-point module shares `15`,
`24` with the gauge block and `30` with the constraint block, but contains
neither 45. So the degree-90 irreducible is *not* carried by the 90 hyperbolic
lines, and `90 = 90` was a matching integer.

**The degree-90 remains unidentified.** Recorded as a refuted guess rather than
quietly dropped.

---

## Pass 1477 (physics) — the physical sector carries ONE specific extension

The Steinberg 81 has two extensions to `PGSp(4,3)`, differing by the sign
character (Pass 1470). Which one the harmonic sector carries is computable,
because the harmonic space is a concrete subspace of the signed edge module:

```text
harmonic invariant under the FULL group PGSp(4,3) : TRUE
full-group harmonic character computable          : TRUE
decomposition over PGSp                           : [[81, 1]]
a SINGLE degree-81 extension                      : TRUE   (irreducible #24)
```

> **The physical sector is `PGSp`-invariant and carries exactly one of the two
> degree-81 extensions — not both, and not a mixture.**

That closes the question Pass 1470 opened. The chain is now complete and every
link is a computation:

```text
240 signed edge 1-chains
  = 39 gauge (15 (+) 24, each SPLITTING over PGSp)
  + 81 physical (Steinberg, SPLITS, and the harmonic space carries ONE extension)
  + 120 constraint (30 (+) 45 (+) 45, the two 45s FUSED into one degree-90)
```

---

## Pass 1478 — where the hemicell obstruction actually bites

BT836 places the 11-cell's and 57-cell's *cells* inside `W(3,3)`; Pass 1472
showed the *polytopes* cannot follow because 11 and 19 divide neither group
order. But the group-theoretic obstruction is not the first one reached:

```text
W(3,3): 40 points, collinearity-graph clique number = 4 (the lines)

11-cell 1-skeleton = K11        needs an 11-clique;  omega = 4      FAILS
57-cell 1-skeleton = Perkel     needs 57 vertices;   40 available   FAILS
```

**Both fail at the skeleton, for two different reasons, before divisibility is
even reached.** The 11-cell fails on clique number (`11 > 4`); the 57-cell fails
on cardinality (`57 > 40`).

So the honest picture of the long-standing "related to the theory of everything
somehow" question is a three-level answer:

| level | status |
|---|---|
| the **cell** (hemi-icosahedron / hemi-dodecahedron, rotation group `A₅`) | **inside** `W(3,3)` — BT836 |
| the **1-skeleton** (`K₁₁` / Perkel) | fails on clique number / cardinality |
| the **polytope** (`PSL(2,11)` / `PSL(2,19)`) | fails on divisibility — Pass 1472 |

The containment stops immediately above the cell, and it stops for elementary
reasons. That is a more useful statement than either "they are related" or "they
are not".

---

## Pass 1479 — the host-only macro list, computed instead of extended

Three Holonet build breaks came from a hand-written nine-entry guard list being
incomplete exactly where the next insert was written. The set is finite, so it
should have been computed:

```text
w33_paper_body defines   : 45
photonic_holonet defines : 11
shared                   :  8
DEFINED IN w33_paper ONLY: 37     <- the real risk surface
DEFINED IN holonet ONLY  :  3
```

The 37: `Aut, CC, Cl, FF, GL, GQ, HH, Neff, OO, PG, PGSp, PSL, PSU, Phisix,
Phithree, Phitwelve, Pin, QQ, RR, SO, SU, Tr, ZZ, …, diag, example, lemma,
proposition, remark, spec, vEW`.

**My hand list covered 9 of 37 — under a quarter.** Both tools now load the
computed list from `data/w33_pass1479_host_only_macros.json`, regenerable with
`scripts/compute_host_only_macros.py`, so it cannot drift from the manuscripts
again. Portability re-checked: 221 inserts, 0 would break.

The general lesson, which is not about LaTeX: **a guard whose vocabulary is
hand-written is incomplete exactly where the next thing is written.** When the
underlying set is computable, compute it.

## Prior art

- [BT836](analysis/BT836_gc_hemicells_in_spreads.md) — **owns** the hemicell containment that Pass 1478 bounds from above.
- [Pass 1470](analysis/w33_pass1470_1474_fusion_versus_splitting_and_the_gc_obstruction.md) — the split/fuse distinction whose open half Pass 1477 closes.
- [Pass 1465](analysis/w33_pass1465_1469_the_constraint_block_is_chiral.md) — the 9-colouring reformulation now encoded as SAT.
