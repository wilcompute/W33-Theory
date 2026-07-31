# Passes 1470–1474 — the blocks are chiral in *opposite* ways, and the 11-/57-cell link is real at the cell level and impossible at the polytope level

Five items, plus the side question. One of them corrects my own Pass 1467
headline.

---

## Pass 1470 — fusion versus splitting: Pass 1467 was too coarse

Pass 1467 said "the constraint sector is chiral; the gauge and physical sectors
are not." That is not right. Both are outer-automorphism phenomena, but of
**opposite type**:

| block | degree | in `PSp` | in `PGSp` | behaviour |
|---|---|---|---|---|
| gauge | 15 | 2 | 4 | **splits** — two extensions each |
| gauge | 24 | 1 | 2 | **splits** |
| physical | 81 | 1 | 2 | **splits** |
| constraint | 45 | 2 | **0** | **fuses** → one degree-90 |

- The two degree-45s are **exchanged** by the outer element and become a single
  irreducible of degree 90 in `PGSp(4,3)`; no 45 survives.
- The Steinberg 81 is **preserved** but acquires a sign: it has two extensions,
  differing by the sign character of `PGSp/PSp`.

> **The constraint block's halves are swapped; the physical block is split.
> Both are chirality, and they are not the same kind of chirality.**

So the physical sector is not chirality-free after all — it is chirality-*split*.
The corrected statement is in `BT1408` as
Proposition (blocks behave oppositely under the outer automorphism).

---

## Pass 1471 — the degree-90 is not identified

`PGSp(4,3)` has exactly one degree-90 irreducible, and `|PGSp|/90 = 576`. The
tempting reading is the 90 hyperbolic lines whose polarity-pairs give the 45
polar pairs.

**Not established.** My script computed the 540 noncollinear *point* pairs, not
the 90 hyperbolic lines — a different object (Pass 1117's two-540 distinction
again). The identification of the degree-90 with any 90-element geometric set
remains **open**, and is recorded as open rather than asserted from a matching
integer.

---

## Pass 1472 — the 11-cell and 57-cell: real at the cell level, impossible at the polytope level

The 57-cell's automorphism group is `PSL(2,19)` and the 11-cell's is `PSL(2,11)`.
The decisive test is divisibility:

```text
|PSp(4,3)|  = 25920 = 2^6 · 3^4 · 5
|PGSp(4,3)| = 51840 = 2^7 · 3^4 · 5
|PSL(2,11)| =   660 = 2^2 · 3 · 5 · 11
|PSL(2,19)| =  3420 = 2^2 · 3^2 · 5 · 19

11 | 51840 ?  FALSE          19 | 51840 ?  FALSE
A5 (order 60) inside PSp(4,3) ?  TRUE
```

**Neither 11 nor 19 divides either group order**, so no `PSL(2,11)` or
`PSL(2,19)` can act on `W(3,3)` or on any carrier built from it. But `A₅` — the
rotation group of *both* the hemi-icosahedron and the hemi-dodecahedron — **is**
inside `PSp(4,3)`.

> **The cells are hostable; the polytopes are not.** And this is exactly
> [BT836](analysis/BT836_gc_hemicells_in_spreads.md)'s result — *"their cells are
> already inside `W(3,3)` — one in every measurement schedule"* — now with the
> obstruction that makes it sharp: the containment stops at the cell because the
> prime does.

**On the proposed `57 = 76 − 19` reading of the parallel track's bridge census:**
it cannot be `PSL(2,19)`. `76 = 57 + 19` there is a partition of gauge
counts — 57 bridges retaining all fourteen Mackey sources, 19 losing one — and
since 19 divides none of the acting group orders, no `PSL(2,19)` orbit structure
can be responsible. The instinct to look was right; the arithmetic closes it.
This is the fifth failure mode's exact shape, caught before a pass was spent.

---

## Pass 1473 — the resolution, and the guards, refreshed

`χ(H) = 9` remains open (Pass 1465: `ω(H) = 9` exactly, no clique obstruction). A
solver-based attack is the outstanding item and was not reached.

Guards re-measured after five grammar changes, since every previously quoted
number predated at least one of them:

```text
corpus index          : 21,380 files, 2,696 distinct tokens
boundary sweep        : 1,502 files scanned, 17 candidates
insert portability    : 221 inserts, 0 would break
```

---

## Pass 1474 — a third insert-portability failure, from my own edit

Adding the Proposition above to `BT1408` broke `photonic_holonet.tex`
immediately: the new text uses `\PGSp`, and the guarded preamble provided `\PSp`
and `\Aut` but not `\PGSp`.

That is the **third** time an insert edit has broken the Holonet, and the second
time it was mine. `\PGSp` is now in the preamble, in
`fix_insert_portability.py`'s block, and in the portability checker's
`HOST_ONLY` list — so the next occurrence is caught by the tool rather than by a
build.

```text
w33_paper.tex        0 errors
photonic_holonet.tex 0 errors
```

The lesson generalises past LaTeX: a guard whose vocabulary is a hand-written
list will be incomplete exactly where the next thing is written, and the fix is
to extend the list *when the build catches it*, not to trust the list.

## Prior art

- [BT836](analysis/BT836_gc_hemicells_in_spreads.md) — **owns** the hemicell result; the obstruction above sharpens it, it does not replace it.
- [BT841](analysis/bt841_eleven_cell_a5_boundary_carrier.py) — **owns** the `660 = 11 × A₅` boundary carrier.
- [Pass 1467](analysis/w33_pass1465_1469_the_constraint_block_is_chiral.md) — the headline corrected here.
- Passes 1500–1504 (parallel track) — the bridge census whose `57 + 19` is addressed above.
