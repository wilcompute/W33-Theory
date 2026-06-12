# BT848 — The Amalgamation Ladder: Universality Explains the 11-Cell/57-Cell Connection

**Status: PROVEN (GAP + python, `analysis/bt848_universal_amalgam_ladder.py`, GAP witnesses `.tmp/gap_bt848*.g`, data `data/bt848_universal_amalgam_ladder.json`)**

The 11-cell and 57-cell are **universal polytopes**: by the amalgamation
theory of abstract polytopes, the 11-cell is *the unique* polytope with
hemi-icosahedral facets and hemi-dodecahedral vertex figures (group L₂(11),
**no proper quotients**), and the 57-cell is *the unique* one the other way
around (L₂(19)). Hartley's classification: exactly **17 universal rank-4
locally projective polytopes** with **441 quotients** in all; every rank-4
locally projective section-regular polytope has hemi-dodecahedral facets or
hemi-icosahedral vertex figures. One step up, the universal polytope with
dodecahedral facets and hemi-icosahedral vertex figures is finite with group
**J₁ × L₂(19)** of order 600415200 — facets 600415200/60 = **10006920**,
vertices /120 = 5003460 (the classical numbers) — where **J₁ is the first
sporadic Janko group, whose involution centralizer is 2 × A₅: icosahedral.**

## Why this hits the substrate: the A₅ classes are the amalgam data

All three groups — L₂(11), L₂(19), U₄(2) = PSp(4,3) — have **exactly two
conjugacy classes of A₅**. In the GC polytopes, *incidence is intersection*:
vertices and facets are the two A₅ classes, and a vertex lies on a facet iff
the two A₅s intersect in a prescribed subgroup. GAP profiles (new):

| group | within-class | cross-class | reading |
| --- | --- | --- | --- |
| L₂(11) | {S₃: 10} | **{D₁₀: 6}**, {A₄: 5} | 11-cell vertex-on-facet = **D₁₀**, 6 per facet |
| L₂(19) | {2: 30}, {3: 20}, **{D₁₀: 6}** | {2: 30}, {5: 12}, {S₃: 10}, {A₄: 5} | **Perkel graph** (57-cell facet adjacency) = within-class D₁₀, 6-regular; vertex-on-facet = S₃, 10 per facet |
| U₄(2) | cl.1 {1:60, 2:90, 3:40, 6:20, A₄:5}; cl.2 {1:30, 2:60, 3:90, 6:20, A₄:15} | {1: 60}, {2: 150}, **{D₁₀: 6}** | compass incidence = **D₁₀**, 6-regular both ways |

The substrate's two 216-compass classes (BT843) carry **the same D₁₀
incidence signature as the 11-cell**: each spread compass is D₁₀-incident to
exactly 6 pentad compasses and vice versa — a bipartite 6-regular incidence
geometry on 216 + 216 with 216 × 6 = **1296 = 6⁴** incident pairs = 36
schedules × 36 core pairs (and 1296 = the E₆-bridge local stabilizer order).

## The Triple Closure Theorem (GAP-verified)

Take one icosahedral amalgam **A₅ ∗_{D₁₀} A₅** (two icosahedral groups glued
over a pentagonal dihedral) and ask what group the pair generates:

```text
in L₂(11):  ⟨A, B⟩ = PSL(2,11), order 660   — the 11-cell
in L₂(19):  ⟨A, B⟩ = PSL(2,19), order 3420  — the 57-cell (Perkel edge)
in U₄(2):   ⟨A, B⟩ = A₆ ≅ PSL(2,9), order 360 — inside EXACTLY ONE
            spread stabilizer: incidence = cohabiting a unique schedule,
            and the closure is that schedule's own core
```

**One local amalgam, three completions: L₂(9), L₂(11), L₂(19).** The
substrate is the **q = 3 member of the same PSL(2)-ladder** whose other two
members *are* the 11-cell and the 57-cell. The primes line up with the
substrate's spectral ghosts: 9 = q², 11 = k − 1 (the Ihara prime of the zeta
critical circle 1/√11), 19 (Heawood genus H(19) = 20 = BC rings).

## The obstruction and the universality verdict

Inside Sp(4,3) the amalgam closes *small* (A₆ — it folds back into a
schedule) and can never close *large*: by universality, any rank-4 regular
polytope with hemi-icosa facets + hemi-dodeca vertex figures has group
exactly L₂(11), and 11 ∤ 25920; same for L₂(19) and J₁ × L₂(19). **The
substrate carries the complete local data of both GC polytopes (BT836–847)
but the rank-4 amalgamation is arithmetically forbidden** — the GC polytopes
are what the substrate's compass geometry *becomes* when the gluing prime is
changed from 9 to 11 or 19. They are not subobjects; they are sibling
completions — and the universal cover of the family adjoins the first
sporadic group J₁, whose local structure (2 × A₅ involution centralizer) is
exactly the compass.

## Face completion (python witness, full hemicell not just skeleton)

The compass Petersen 15-orbit has exactly **12 pentagons**, splitting under
the compass A₅ into **two orbits of 6**, each covering every edge exactly
twice — i.e. each orbit is a valid hemi-dodecahedral **face set**. Every
compass needle carries **two chiral fully-faced hemi-dodecahedra {5,3}₅**,
matching the chiral pairs found at every other level (pentads BT845, dark
dodecahedra BT847).

## Open

- Build the substrate's bipartite D₁₀-incidence geometry on 216+216
  explicitly and compute its rank-4-amalgam failure locus (where the
  intersection property breaks — it must break, by universality).
- The J₁ trail: 1296 = 6⁴ incident pairs; |J₁| = 2³·3·5·7·11·19 contains the
  clock prime 7 and both GC primes; J₁ ⊃ L₂(11) maximal (index 266). Is
  there a substrate shadow of the Livingstone graph (266 = 2·7·19)?
- The {3,5,3} mixed amalgam (icosahedral facets, hemi-dodeca vertex
  figures): which of Hartley's 17 universals is it, and does its group
  arithmetic touch the substrate?
