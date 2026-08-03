# Glue-track withdrawn claims — one ledger

**Written Pass 2578, covering Passes 2106–2577 (2026-08-02).**

Every claim this track published and later withdrew or corrected, in one place, with the
mechanism that caught it. Listed because a scattered set of corrections inside individual
pass files is unreadable, and because the *pattern* is more useful than any single entry.

---

## Withdrawn or corrected claims

| # | claim | pass | what was wrong | caught by |
|---|---|---|---|---|
| 1 | "the three shortest words give the three smallest metallic constants" | 2107 | `φ` is 11th of 22 by size; the real pattern is the reducibility dichotomy | own recount, Pass 2440 |
| 2 | frame stabiliser has order 96 | 2455 | that is the `PGSp` figure; `PSp` acts with stabiliser 48 | GAP frame action, Pass 2510 |
| 3 | "the chiral carrier has no invariant bilinear form at all" | 2467 | true of each degree-4 *constituent*; the 8-dim carrier has one symmetric and one alternating form | `Sym²`/`Λ²` invariants, Pass 2477 |
| 4 | the certificate defect has a single cause (integer dict keys) | 2482 | `1887` has zero integer-like keys and still fails; at least two causes | direct inspection, Pass 2493/2499 |
| 5 | "frontier completeness is the load-bearing question" | 2505 | Pass 1821 had already proved the census complete | parallel track pointing at 1821, Pass 2516 |
| 6 | rank-9 eigenspaces are "unions of isotypic components"; `135 = 15 + 4×30` | 2528 | false where multiplicity is 2 — splitting is the mechanism; and the grouping came from the wrong group | `PGSp` decomposition, Pass 2536 |
| 7 | `135 = 15 + 120` | 2536 | numerically right, structurally `15 + 60 + 60` | merge arithmetic, Pass 2569 |
| 8 | `ℚ(√2)` links the order-8 lift to the silver word | 2520 | finite-order vs infinite-order; no map can relate them | Pass 2571 |
| 9 | greedy merge finds the finest commutative fusion | 2574 | pairwise commuting ≠ closed algebra; "rank 3" span was 14-dimensional | its own eigenvalue count |

## Results produced and then discarded before publication

These never entered the corpus; recorded so the numbers are never mistaken for results.

| run | output | why discarded |
|---|---|---|
| Pass 2503 #1 | group order 192, 62,784 covers, link size 53 | hand-written generators were not symplectic |
| Pass 2503 #2 | crash on line images | GAP's `SP(4,3)` uses a different form convention |
| Pass 2511 | link sizes 4848 / 5019 / 4561, cliques 2 / 2 / 3 | frame labelling mismatch, exposed by trivial stabilisers |
| Pass 2517 | orbit sizes 25920 for all reps | second labelling mismatch; reps are not covers under that ordering |
| Pass 2525 | fractional multiplicities, `MATCH ? false` | class-fusion mismatch; would have published a false **negative** about the parallel track |
| Pass 2542 | max partial ovoid 6 | search prune made `best` an underestimate; corpus value 7 was right |

---

## The pattern, which is the point

**Six of the nine withdrawals and all six discarded runs were caught by comparison against
a number somebody had already frozen** — `3,547,800`, `13,648`, `394,200`, `7`, `540`.
Not by review, not by care.

Three rules earned the hard way, in order of how much they saved:

1. **Build the check before building the result.** Every one of the six discarded runs
   looked correct until compared. A run with no known number to hit is not evidence.
2. **A disagreement with the corpus is a bug in the new code until proved otherwise.**
   Six occurrences. Zero exceptions so far.
3. **A broken computation can produce a confident false NEGATIVE about someone else's
   work** (Pass 2525). That is worse than a false positive about your own, because
   nobody else is motivated to re-check it.

And one structural cause, not a discipline failure: **certificates are prose-free, so no
topic search reaches them.** Seven questions in this arc were treated as open while their
answers sat in committed data. That is what `scripts/build_certificate_index.py`
(Pass 2570) exists to fix.

---

## What survived

For balance, the claims that were checked and held: the `C₆`/`S₃` fibre split and its
`C₃`/`S₃` chirality consequence; the central-character mechanism unifying three
independent results; `Sp(4,3)` and `PGSp(4,3)` as the two order-51840 doublings; the Weil
straddle for all odd `q`; the pentagon augmentation-ideal restriction; the `K₈` criterion
(executed by the parallel track to give `χ(H) ≥ 10`); the `73 = ` weighted-orbit-count
resolution; the independent reproduction of `394,200` and `3,547,800`; rank 22 confirmed
three ways; and the commutative ceiling `Σ m = 14`.

The ratio matters less than the fact that both lists exist.
