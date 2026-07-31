# Passes 1480–1484 — the Steinberg's sign is visible exactly on the 540 involutions

Five items. The one that matters connects the physical sector's chirality to the
involution class that indexes the frames.

---

## Pass 1480 — the degree-90 has no transitive carrier at all

Pass 1476 refuted the 90-hyperbolic-line guess. The next question is whether the
degree-90 has *any* permutation carrier. `|PGSp|/90 = 576`, so a transitive
90-set needs an index-90 subgroup:

```text
maximal subgroup orders in PGSp(4,3) : 1152, 1296, 1296, 1440, 1920, 25920
MAXIMAL subgroups of order 576       : 0
```

There is **no maximal subgroup of order 576**, so no *primitive* degree-90 action
exists; any index-90 subgroup sits inside a maximal — most naturally at index 2
in the order-1152 polar-pair stabiliser, making a 90-set a double cover of the
45 polar pairs.

But that route is closed too, by a one-line argument: a **transitive** 90-point
permutation module contains the trivial character once, leaving 89 dimensions —
so it cannot contain a degree-90 irreducible. **The degree-90 is not a
constituent of any transitive 90-point permutation module.** It has to arise
some other way, and where remains open.

---

## Pass 1481 (physics) — the sign lives on the 540 involutions

The two degree-81 extensions agree on `PSp(4,3)` and differ somewhere on the
outer coset. Exactly where:

```text
classes where the two degree-81 characters differ : 6
  class  5: order  4, size  540, chi =  3 vs  -3    OUTER
  class 12: order  2, size   36, chi =  9 vs  -9    OUTER
  class 18: order  2, size  540, chi = -3 vs   3    OUTER
  class 21: order 10, size 5184, chi = -1 vs   1    OUTER
  class 22: order  8, size 6480, chi =  1 vs  -1    OUTER
  class 25: order  4, size 1620, chi = -1 vs   1    OUTER
```

**Every separating class is outer** — exactly as required, and a clean check that
the two really are extensions of one `PSp`-irreducible.

The striking entry is **class 18: an involution class of size 540**. That is
BT773's class — the one in bijection with the 540 frames (Pass 1450 established
it lives in `PGSp`, not `PSp`, and has size exactly 540). So:

> **The sign distinguishing the two Steinberg extensions is detected, with values
> `∓3`, precisely on the involution class that indexes the 540 frames.**

The physical sector's chirality and the frame geometry are read by the same
elements. Given that the frames are also what carry the cross-matching whose
cokernel is this same Steinberg (Pass 1397/1455), this is the third independent
appearance of the 540 in the physical sector's description — and the first where
it appears as a *character* fact rather than a counting one.

---

## Pass 1482 — every block picks a specific extension

Pass 1477 showed the harmonic block is `PGSp`-invariant and carries one specific
degree-81. The same computation on the exact block:

```text
exact block invariant under the FULL group : TRUE
GAUGE block over PGSp                      : [15 (#6), 24 (#14)], one each
```

So all three Hodge blocks are full-group invariant, and each picks specific
extensions rather than a sum over both. The decomposition is not merely
`PSp`-natural; it is `PGSp`-natural, with a definite choice in every block.

---

## Pass 1483 — the guard vocabularies, measured against the corpus's own authority

`check_rediscovery.py` carries three hand-written lists. `RESULTS_VOCABULARY.md`
is the authority on which object names this project has decided are load-bearing,
so the gap is measurable:

```text
guard lists (NAMED + ATOMS + GEOM_NOUNS) : 52 entries
names in RESULTS_VOCABULARY.md           : 105
canonical but UNGUARDED                  : 93
```

Distinctive ones the guard cannot see include `nonsplit 58-23 extension`,
`four-branch gluing`, `copy selector 360`, `cycle selector 120`, `m36 vacuum`,
`m45 vacuum`, `omega_432 x c3`, `five-primary sandpile bridge`.

**Reported, not applied — deliberately.** Most of the 93 are generic English
(`action`, `algebra`, `chain`, `orbit`), and the hand lists are *calibrated*:
Pass 328 measured flag rates per token class, and Pass 1107 narrowed
`GEOM_NOUNS` from 39.9% noise to 30.9% by **removing** generic nouns. Widening a
calibrated list without re-measuring would undo that work. The right move is to
add entries one at a time with a flag-rate measurement beside each, and
`scripts/compute_geom_vocabulary.py` now supplies the candidate list.

This is the opposite conclusion to Pass 1479, and for a stated reason: the LaTeX
macro set is an *exact* requirement (a missing macro is a build failure), while
the token vocabulary is a *tuned* signal (an extra token is noise). Compute the
first; measure before widening the second.

---

## Pass 1484 — the resolution SAT, running

Launched detached with no internal timeout:

```text
encoding : 4,860 variables, 99,909 clauses, built in 0.1 s
status   : still running at the time of writing
```

Undecided. Reported as running rather than as a result.

## Prior art

- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the 540 involution class that Pass 1481 finds carrying the sign.
- [Pass 1450](analysis/w33_pass1448_1454_hodge_maxwell_and_the_missing_star.md) — established that class lives in `PGSp`, not `PSp`.
- [Pass 1477](analysis/w33_pass1475_1479_which_81_and_where_the_obstruction_bites.md) — the harmonic block's extension, extended here to the gauge block.
- Pass 328 / Pass 1107 — **own** the calibration Pass 1483 declines to disturb.
