# Passes 1826–1830 — the spreads are traps, they beat the octets mod 2, and only two classes read the whole sign

Five items. One explains why every resolution search this project has run gets
stuck; one overturns a claim I made three passes ago; one leaves an object
deliberately unnamed.

---

## Pass 1828 (the main result) — a spread is a **trap**, not a seed

A spread is 10 pairwise disjoint lines partitioning the 40 points, so all
`C(10,2) = 45` of its line-pairs are frames. Two of them cannot share a matching
edge — their endpoint sets are disjoint, or meet in one line whose partners are
disjoint. So:

> **Each spread's 45 frames are an independent set of `H`.**

The bookkeeping is better than that. The 240 edges are partitioned by the 40
lines, 6 each (verified), and a spread's 45 matchings cover **exactly** the 180
edges lying off its own lines — confirmed for all 36 spreads:

```text
all 36 spreads independent in H         : True
all 36 leave exactly their own 60 edges : True
```

So completing a spread to an exact cover is a 15-frame problem on 60 edges
instead of a 60-frame problem on 240, and the arithmetic is perfect: exactly
**15** frames lie entirely inside those 60 leftover edges, and `15 × 4 = 60`.

It fails, and not narrowly:

```text
over all 36 spreads: candidate frames [15], completions found [0]

the 15 candidates touch only 20 of the 60 leftover edges (each 3 times)
   -> 40 of the 60 lie in NO admissible frame at all
```

> **Every spread's 45-frame `K₁₀` is a MAXIMAL independent set of `H` that is not
> maximum**, and it is blocked absolutely: two thirds of the edges it leaves
> behind cannot be covered by *any* frame disjoint from it.

**This explains the search history.** `α(H) = 60`, but `H` has at least 36 known
maximal independent sets of size 45, each a highly symmetric configuration that
a greedy or DFS search will walk straight into and cannot back out of locally.
Five previous searches for a resolution stalled; the spreads are a named reason.
Any future search should forbid completing a `K₁₀`.

A structural check ties this to Pass 1829: the size-36 spread involution fixes
exactly **60** frames, and `45 + 15 = 60` — the `K₁₀` plus precisely the 15
blocked candidates, with zero overlap. The trap and its 15 false exits are one
orbit of one involution.

---

## Pass 1827 — the systematic sweep, and a correction

Pass 1817 concluded that the 45 octets were "the only family that adds mod-2
rank." That was measured on **two** families. Measured on every relation-family
`{f : rel(f,x) = v}` over every base object class and attained value:

```text
baseline rank_F2(M^T) = 195
  octet          gain +30   (values 0, 2)
  spread         gain +36   (values 0, 1, 2)     <- BEATS the octets
  line           gain +15
  edge/point/frame  +1      (the all-ones vector; trivial)
```

and combining them:

```text
+ octets                 225      <- the parallel track's Pass 1606/1607 figure
+ spread (both lines)    231
+ octets + spreads       260
+ lines as well          260      (lines are subsumed)
```

> **The spreads supply more independent `F₂` directions than the octets do, and
> together they take the frame system from 195 to 260** — 65 new XOR directions
> rather than 30.

So my Pass 1817 sentence was wrong, and wrong in the way this repo keeps
punishing: a claim whose scope exceeded its measurement. The correct statement is
that among the families tested there, only the octets gained; a systematic sweep
finds a better one. The practical consequence is immediate — the XOR-native
attack should be given all 260, not 225.

---

## Pass 1829 (physics) — one involution is sensitive to all four bits, and only two classes are

`Res_H(χ) = Res_H(χ·ε)` fails exactly when `H` meets a class where `δ_B ≠ 0`, so
the smallest possible detector of a bit is cyclic. For every one of the four
chiral blocks:

```text
degree 15 : visible on 8 classes, element orders {2,4,6,8,12}   smallest: order 2
degree 24 : visible on 6 classes, element orders {2,6,10}       smallest: order 2
degree 30 : visible on 7 classes, element orders {2,4,6,12}     smallest: order 2
degree 81 : visible on 6 classes, element orders {2,4,8,10}     smallest: order 2
```

Every bit is readable by a single involution — no bit is more "global" than
another, so there is no hierarchy of locality across the Hodge sectors. And the
classes sensitive to **all four at once**:

```text
classes reading all four bits : 2
   size  36, order 2, OUTER, fixes 0 pts / 10 lines / 60 frames   <- the SPREADS
   size 540, order 2, OUTER, fixes 8 pts /  6 lines / 16 frames   <- the FRAMES
```

> **Exactly two conjugacy classes are sensitive to the entire four-bit
> handedness, and both are the substrate's own geometric involutions: the 36
> spreads and the 540 frames.**

Stated carefully, because the tempting over-read is close by: a single class
yields a single number, so one involution does **not** *determine* four bits — it
is *sensitive* to all four. Determining them needs four independent measurements,
which is Pass 1826.

---

## Pass 1826 — a minimal complete set of observables

Four independent bits need four measurements. Writing `χ_V(c) − Σ_i avg_i(c) =
Σ_i s_i δ_i(c)`, recovering `s ∈ {±1}⁴` requires a class set on which the `δ`
matrix has rank 4:

```text
classes where any bit is visible : 10   (all OUTER, as required)
MINIMUM classes needed           : 4
number of working quadruples     : 152 of 210
```

One minimal set, geometrically:

| class | size | order | fixes |
|---|---|---|---|
| a | 540 | 4 | 0 pts / 4 lines / 6 frames |
| b | 4320 | 12 | 0 pts / 1 line / 0 frames |
| c | **36** | 2 | 0 pts / 10 lines / **60 frames** — the spreads |
| d | 5184 | 10 | 0 pts / 0 lines / 0 frames |

So the handedness is fully determined by four class measurements, and 152 of the
210 possible quadruples suffice — the observable is robust, not delicate.

---

## Pass 1830 — the 270-class, characterised but deliberately **not named**

The order-4 outer 540-class squares into a class of size 270 (Pass 1820). What it
is, measurably:

```text
size 270, order 2, INNER, centraliser 192 = 2 x 96
fixes 0 points, 4 lines, 24 frames
the 4 fixed lines are PAIRWISE DISJOINT, covering 16 of the 40 points
all four sign bits vanish on it (as they must, being inner)
it is a square
```

Two natural namings, both **refuted**:

```text
the 4-line set as the invariant : its G-orbit has size 2880, not 270  -> NO
the 4 lines as a transversal set: not one of the 540 transversal sets -> NO
```

So the class is not determined by its fixed lines, and the object of size 270 it
ought to index is **unknown**. Recorded as an open question rather than given a
gestural name, per CLAUDE.md failure mode 3.

One byproduct worth keeping: the 540 frames have 540 **distinct** transversal
sets, all of size 4, one per frame — a bijection. BT794 owns the "4 isotropic
transversals per skew pair"; the distinctness is what makes it a labelling.

---

## Bonus — two of BT795's June open questions, answered

Searching for the *result* (`spread@180`) rather than the topic turned up
[BT795](analysis/BT795_spread_envelope_routing_cell.md), whose "180 parallel
paths" is the same 180 as Pass 1828's, in routing language. Verified directly:

```text
BT794/795 transversals == my cross-matching edges (checked on 120 frames): True
```

Each of a skew pair's 4 isotropic transversals meets `L₁` and `L₂` once each, and
that point pair **is** an edge of the cross-matching. So BT794/795's routing
vocabulary and the Hodge vocabulary describe one object: *a frame's 4 routing
paths are its 4 harmonic-sector edges.* BT795 owns the count.

BT795 then asks (open question 2, June 11) whether four spreads partition the 40
lines — a 1-factorisation of the line set. The answer:

```text
quadruples of spreads covering all 40 lines : 0
DISJOINT pairs of spreads                   : 0 of 630
maximum lines shared by two spreads         : 4
```

> **No. The 36 spreads pairwise intersect** — not a single disjoint pair exists,
> so there is no spread-resolution of `W(3,3)`'s lines at any size, let alone 4.

That closes BT795's open question 2. It also rhymes with Pass 1828: spreads
refuse to pack, both as line sets and as frame sets.

## Prior art

- [BT795](analysis/BT795_spread_envelope_routing_cell.md) / BT790 — **own** the
  36 spreads and the `K₁₀` of 45 skew pairs. Pass 1828 shows that `K₁₀` is a
  maximal-not-maximum independent set of `H`; BT795 reads it as a routing
  envelope, which is untouched by this.
- [BT794](analysis/BT794_klein_regulus_transversal_lift.md) — **owns** the 4
  isotropic transversals per skew pair.
- Passes 1606/1607 (parallel track) — **own** the `195 → 225` octet gain that
  Pass 1827 extends to 260.
- Passes 1841–1845 (parallel track) — **own** the 28,800 certified signature
  resolutions; none nine-covers, so the resolution stays open and Pass 1828 is
  an obstruction result, not a solution.
- Pass 1817 — the claim Pass 1827 corrects.
- Passes 1819/1816 — the four bits and their locality, refined here.

## Still open

- `χ(H) = 9`. Pass 1828 removes a whole class of search strategies rather than
  supplying one.
- What has size 270.
- Whether any family beyond octets, spreads and lines adds `F₂` rank past 260.
