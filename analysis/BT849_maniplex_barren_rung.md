# BT849 — The Barren Rung: Maniplexes, the Tomotope, and Why the Substrate Delocalizes

**Status: PROVEN (GAP + independent python, `analysis/bt849_maniplex_barren_rung.py`, GAP witnesses `.tmp/gap_bt849*.g`, data `data/bt849_maniplex_barren_rung.json`)**

The tomotope — this project's runtime middleware since Pillar 70 — is
classified as a **maniplex**: the canonical rank-4 maniplex that is *not* a
polytope (Monson–Pellicer–Williams), whose minimal regular cover fails the
intersection property. Its monodromy order **18432 = 96 × 192 is exactly what
Pillar 70 measured**. BT849 brings the maniplex literature to bear on the
BT848 amalgamation ladder, with one validated search and three sharp zeros.

## The search and its controls

A regular rank-4 maniplex = an **sggi**: four involutions r₀…r₃ with the
string condition, *without* requiring the intersection property (that extra
axiom is what makes a polytope). Exhaustive search over involution quadruples
(r₀ fixed per class, complete up to conjugacy):

| group | result |
| --- | --- |
| **L₂(11)** (control) | exactly type {3,5,3}, 11 facets / 11 vertices, IP true — **the 11-cell rediscovered** |
| **L₂(19)** (control) | {5,3,5}, 57/57, IP true — **the 57-cell** — *plus* degenerate {5,5,5} maniplexes with a single facet or single vertex, IP false — **Leemans–Toledo's family, visible in our own search** |
| **U₄(2)** | **zero** rank-4 sggi with any 5 in the type |
| **A₆ = L₂(9)** | **zero** rank-4 sggi of *any* type, and **zero** rank-3 sggi (no regular maps) — confirmed independently in pure python |

Leemans–Toledo (Discrete Math. 2023): regular rank-4 maniplexes with group
PSL(2,q) exist for infinitely many q; each is the 11-cell, the 57-cell, or
has a single facet/vertex; **none exist at rank > 4**.

## The three theorems

1. **The GC obstruction extends to maniplexes.** BT848 showed universality +
   Lagrange forbid rank-4 GC *polytopes* inside Sp(4,3). Now: U₄(2) admits no
   rank-4 *maniplex* with a 5 in its Schläfli type either. Even dropping the
   intersection property, the substrate group cannot crystallize its
   icosahedral local data into a rank-4 flag object.
2. **The amalgam closure is the barren rung.** The substrate's D₁₀-amalgam
   closes at A₆ = PSL(2,9) (BT848) — and q = 9 is the *empty* rung of the
   PSL(2) maniplex ladder: A₆ supports no sggi at rank 3 or 4 at all (the
   maniplex-level extension of A₆'s famous string-C-group exceptionality).
   The ladder reads: **q = 9 barren (substrate folds into schedules), q = 11
   the 11-cell, q = 19 the 57-cell**, infinitely many degenerate rungs, and
   J₁ × L₂(19) above.
3. **The tomotope is the workaround.** Where rank-4 polytopality and even
   5-type maniplexity fail, the substrate's actual middleware is the
   tomotope — a *non-polytopal maniplex with no 5 in its type*
   ({3,12,4}-flavored Coxeter data, 192 flags, cover monodromy 18432). The
   machine's flag-level runtime is exactly the structure that survives the
   obstruction.

## Why the GC content is delocalized (the physics reading)

The substrate cannot host a GC crystal: no single rank-4 flag object with
icosahedral type can form on Sp(4,3). So the GC geometry exists only in the
**delocalized** form mapped in BT836–848: Petersen splits, chiral pentads,
chart double covers, dodecahedra in the dark sector — spread over the 36
schedules instead of concentrated in one polytope. Universality says the
concentrated versions exist uniquely — *elsewhere* — as the 11-cell and
57-cell. The substrate keeps their local physics and trades their global
rigidity for the tomotope's maniplex runtime.

## Literature hooks queued

- **Voltage operations** (Hubard–Mochán–Montero, Combinatorica 2023): the
  formal home of Pillar 73's voltage functor and the BT838 Wythoff ladder.
- **Cayley extensions** (Cunningham–Mochán–Montero 2025): maniplexes with
  vertex-regular subgroups — candidate formalism for the free PSp-torsors of
  BT742/746.
- **Polytopality criteria** (Garza-Vargas–Hubard; Mochán 2024 on 2-orbit
  maniplexes): apply to the compass D₁₀-incidence geometry to find its exact
  polytopality failure locus.
