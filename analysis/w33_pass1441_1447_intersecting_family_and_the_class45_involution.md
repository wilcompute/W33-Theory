# Passes 1441–1447 — the covers are an intersecting family, and the C₂ is a class-45 involution

Seven items. Two are new mathematics, and the first of them answers a question
with a perfect numerical setup by saying **no**.

---

## Pass 1441 — the exact covers form an INTERSECTING FAMILY *(breakthrough)*

The setup was too good to ignore. Every edge lies in exactly **9** frame
matchings, and `540 = 9 × 60`. So a partition of all 540 frames into **nine**
disjoint exact covers — a *resolution*, nine parallel classes — has exactly the
arithmetic it needs. Nobody had asked.

Direct search failed, then failed again with proper backtracking, then a
set-packing attack over a pool of covers returned something strange: a greedy
maximum of **1** disjoint cover out of 9, across 4,000 random orderings. Not 2.
Never 2. That is not a search failure, it is a structural signal, so I tested it
head-on over a pool of 1,262 distinct covers:

```text
pairs compared                      795,691
DISJOINT pairs (sharing no frame)         0
minimum intersection observed             4

|A ∩ B| =  4 :    292   (0.037%)
|A ∩ B| =  5 :  2,198   (0.276%)
|A ∩ B| =  6 :  6,796   (0.854%)
|A ∩ B| =  7 : 16,276   (2.046%)
```

**No two exact covers are disjoint, and every observed pair shares at least four
frames.** The intersection distribution has a hard floor at 4 and falls off
sharply below 8.

**Consequence: there is almost certainly no resolution.** A resolution needs nine
pairwise-disjoint covers; not even *two* exist in a sample of 1,262. The perfect
arithmetic `540 = 9 × 60` with edge-multiplicity 9 is a coincidence of counting,
not a decomposition.

**The caveat, and it is the one this session has been learning.** My pool is
DFS-generated, and Pass 1439 established that this sampler is *not* uniform — it
under-draws the `C₂`-dominated region that holds 83% of covers. So "zero disjoint
pairs in my pool" is strong evidence, **not a proof**, and if disjoint pairs exist
they would most plausibly live exactly where my sampler is weakest. Stated as an
observation with its sampling bias named, not as a theorem.

---

## Pass 1442 — the involution stabilising a `C₂` cover is a **class-45** element *(breakthrough)*

83% of covers have a `C₂` stabiliser. What *is* that involution?

```text
involution classes in PSp(4,3)       : sizes 270 and 45   (315 involutions total)
the C2 cover's stabilising involution: class of size 45
it fixes                             : 84 of the 540 frames
of the cover's own 60                : exactly 12       (orbits 1^12 2^24)
```

**The twelve is reproduced independently** — BT1420 reports "a `C₂`-stabilised
cover fixes twelve selected frames", and this is that number from a separate
construction. And the involution is not generic: it comes from the **smaller
class, of size 45**, the same 45 that indexes the polar pairs.

**A scope correction for BT773.** BT773 states there are "540 cubes in `W(3,3)`,
one per 3A₁ involution". `PSp(4,3)` has only **315** involutions, in classes of
size 270 and 45 — so the 540 involutions cannot live in `PSp(4,3)` and must be
counted in `PGSp(4,3)`, including outer ones. BT773's arithmetic
`51840 = 540 × 2 × 48` is consistent with that reading. This narrows where the
statement holds; it does not refute it, and I computed only in `PSp(4,3)`.

---

## Pass 1443 — the `M20` chart, corroborated

Their Pass 1509 builds an `H(5,3)` chart of 243 covers with setwise stabiliser
`2⁴:A₅ = M20`. Independently:

```text
subgroups of order 960 in PSp(4,3), up to conjugacy : exactly ONE class
structure                                            : (C2 x C2 x C2 x C2) : A5
IdGroup                                              : [960, 11358]
index                                                : 27
243 = 3^5                                            : true
```

**`2⁴:A₅` exists, is unique up to conjugacy, and sits at index 27** — so their
identification is the only one available at that order. (My script printed
`is 2^4:A5? false` from a *guessed* SmallGroup ID `[960,11357]`; the actual ID is
`[960,11358]` and the structure description confirms it. The false line is my
error, not theirs.) The 243-cover chart itself is their computation and is not
reproduced here.

---

## Pass 1444 — 29 inserts made portable, proving the fix on one first

`scripts/fix_insert_portability.py` adds the guarded preamble (`\@ifundefined`,
`\providecommand`) that `BT1408` needed. It **enforces the Pass 1440 rule**: it
defaults to `--dry-run`, requires `--only NAME` or `--apply`, and the inserted
block is idempotent.

```text
dry run                                  : 29 inserts need a guard
proved on BT1134 alone, bare host        : 26.4 KiB PDF, exit 0
applied to the rest                      : 28 more files
portability check after                  : 0 would break   (was 29)
spot-checks in a bare host               : 2 of 3 clean
```

The one remaining failure, `BT1509`, needs something beyond theorem environments
and is left alone — it is the parallel track's newest insert.

---

## Pass 1445 — the sampler guard, narrowed from noise to nine

Pass 1438 measured its precision at **0 of 4**. Rather than keep a guard nobody
should trust, it now requires the specific shape the one real instance had: a
**distribution over stabiliser/orbit types drawn from sampled solutions**.

```text
deterministic-order samplers   : 134
claiming something universal   : 73  ->  9
```

Nine files is a list someone will actually read.

---

## Pass 1446 — the sweep's new `.tex` scope, measured

Scanning `.tex` raised the file set from 1,258 to 1,482 and was the fix that
would have caught `BT1420`. Running it now: **no `.tex` boundary/target pair
clears the two-token threshold.** The scope fix matters for the future — the
parallel track publishes theorems as inserts — but it surfaces nothing today, and
that is worth stating rather than leaving the impression it found things.

---

## Pass 1447 — a bug of mine, caught by the number being wrong

The first run of Pass 1442 reported the `C₂` involution fixing "7 to 9" of 540
frames and "0 to 1" of the cover's 60. That contradicted my *own* earlier
correct computation (12), which is what made me look.

The cause: `OnSets(frames[f], g)` applies `g` to the *set of line indices* stored
in `frames[f]`, but `g` permutes **frame indices**. The right test is `f^g = f`.
Corrected, the numbers become 84 and 12, and 12 matches BT1420 exactly.

Worth recording because the detection route was arithmetic, not review: a
disagreement with a number I already trusted. The published figures are from the
corrected run.

## Prior art

- Pass 1420 / Pass 1505 / Pass 1509 (parallel track) — **own** the `226800 → 3,547,800` census, the twelve fixed frames, and the `M20` chart corroborated above.
- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the 540-cube/involution bijection whose scope is narrowed above.
- [Pass 1439](analysis/w33_pass1436_1440_both_papers_build_and_a_weak_filter.md) — the sampler-bias finding that supplies Pass 1441's caveat.
