# Passes 1861–1866 — the trap survives every q, the bits align on frames, and the substrate has no phase

Six items. Five continue the resolution/chirality arc; Pass 1866 is separate and
closes a Remark I wrote into `BT1408` myself.

---

## Pass 1865 — the spread trap is **not** a `q = 3` accident

`GQ(q,q)` has `(q+1)(q²+1)` points, spreads of `q²+1` lines, and frames whose
cross-matching has `q+1` edges. The seed arithmetic is exact for every `q` by
construction, so the question is whether the *completion* fails only at `q = 3`.
Built from scratch for `q = 2` and `q = 5`:

| q | points | lines | edges | spread | K-frames | covers | leaves | candidates | needed | completions |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 15 | 15 | 45 | 5 | 10 | 30 | 15 | **0** | 5 | 0 |
| 3 | 40 | 40 | 240 | 10 | 45 | 180 | 60 | **15** | 15 | 0 |
| 5 | 156 | 156 | 2340 | 26 | 325 | 1950 | 390 | **65** | 65 | 0 |

In every case the leftover is exactly the spread's own lines' edges, and in every
case the completion fails.

Two things sharpen it. For **odd** `q` the number of admissible completing frames
**exactly equals the number needed** — `15 = 15`, `65 = 65` — so the arithmetic
is a perfect decoy. And the fraction of the leftover those candidates can touch
follows a law:

```text
q = 3 : 20/60  = 1/3        q = 5 : 78/390 = 1/5        -> exactly 1/q
q = 2 :  0/15  = 0          (no candidates at all; the even case is different)
```

> **In `W(q,q)` for `q ∈ {2,3,5}`, a spread's `K_{q²+1}` is a maximal independent
> set of the frame graph that is not maximum.** For odd `q` exactly the right
> number of completing frames exists and they reach only `1/q` of the edges they
> would have to cover.

That is a statement about symplectic quadrangles, not a fact about 40 points, and
the `1/q` law is a prediction to test at `q = 7`.

---

## Pass 1861 — the bottleneck was the **search order**, not the constraints

I proposed re-running the search with `K₁₀`-avoidance and all 260 XOR directions.
Measuring first turned out to matter more:

```text
naive DFS (lowest uncovered edge)    : 7,031,990 nodes, 0 covers, timed out at 120 s
MRV + dead-edge pruning              :   210,123 nodes, cover found in 10.1 s
```

Same constraints, same instance. Branching on the uncovered edge with the fewest
admissible frames, and pruning the moment any edge has none, is the difference
between failure and a 10-second success — a **33× node reduction**. The cover
found is genuine and Hoffman-tight (`‖A x + 4x‖ = 1.5 × 10⁻¹⁴`).

So the honest lesson is one I nearly missed by proposing more constraints: the
five stalled searches were not short of information, they were branching badly.
Reported as a search-engineering result, and it does **not** decide `χ(H) = 9`.

---

## Pass 1862 — greedy never reaches the maximum, in 4,000 tries

How bad is the landscape? Random greedy maximal independent sets:

```text
size 38-41 :  1,082      size 45 : 292  (7.3%)  <- the spread traps live here
size 42    :    923      size 46 :  87
size 43    :    924      size 47 :  28
size 44    :    653      size 48-49 : 2
size 60    :      0  of 4,000   -- 0.00%
```

> **Greedy never once reached `α(H) = 60`**, topping out at 49. The distribution
> peaks at 42–43, and the spread traps at 45 sit just above the mode.

Exact covers are not merely hard to find — they are invisible to local search.
Together with Pass 1861 this says the search must be constraint-propagating, not
constructive.

---

## Pass 1864 (physics) — the four bits are **aligned on the frames, split on the spreads**

Building the genuine signed 240-edge character (a fixed edge counts `+1` when its
orientation survives, `−1` when it is reversed) and decomposing:

```text
V = 15(#6) + 24(#14) + 30(#15) + 81(#24) + 90(#25),  multiplicity-free
chi_V on the 540 FRAME involutions : 12
chi_V on the  36 SPREAD involutions : -20
```

Per chiral block:

| block | frame class | spread class |
|---|---|---|
| 15 (gauge) | **+3** | −5 |
| 24 (gauge) | **+4** | **+4** |
| 30 (constraint) | **+2** | −10 |
| 81 (physical) | **+3** | −9 |

```text
all four the same sign on the frame class  : TRUE
all four the same sign on the spread class : FALSE
```

> **Read by the frames, all four sectors have the same handedness. Read by the
> spreads, three of them flip and only the degree-24 gauge block keeps its sign.**

So the bits are not four free parameters after all — the substrate occupies the
fully aligned corner *with respect to the frames*, which is 1 of the 16 available.
And the degree-24 is singled out: it is the only sector whose handedness agrees
on both geometric readers. Pass 1819's independence is about the `δ` functions;
this is about the values the substrate actually takes, and they are correlated.

---

## Pass 1863 — the 270 fibres over the 27

Pass 1830 failed to name the size-270 class by what its *element* fixes. Naming it
by what its **centraliser** stabilises works:

```text
centraliser : order 192, structure D8 x S4, index 270, NOT maximal
  orbits on 40 points : 16 + 24
  orbits on 40 lines  : 4 + 12 + 24
contained in the index-27 maximal (order 1920) : TRUE, with |M:C| = 10
contained in the index-45 polar-pair stabiliser : FALSE
```

My guess that `270 = 45 × 6` over the polar pairs was **wrong**. The truth is

> **`270 = 27 × 10`: the class fibres 10-to-1 over the index-27 maximal — the 27
> lines on the cubic surface.**

`|W(E₆)| / 27 = 1920`, so the index-27 object is the classical 27, and the 270 sits
above it with fibre 10. The object is named; what the fibre-10 is geometrically is
still open, but the class is no longer floating.

---

## Pass 1866 (separate — physics / photonics) — the substrate has **no phase**

`BT1408` carries a Remark of mine saying the 240-edge module has no Hodge star,
and asking where one must come from. A star on the middle degree needs a
`G`-invariant `J` with `J² = −1`, and the Frobenius–Schur indicator decides
whether one exists. Computed for every constituent, and then for the whole group:

```text
block  degree  FS   invariant J?
  #6      15    1   no  (real R, amplitude only)
  #14     24    1   no
  #15     30    1   no
  #24     81    1   no
  #25     90    1   no

indicators over ALL 25 irreducibles of PGSp(4,3) : [[1, 25]]
```

**Every single irreducible is of real type.** There is no `i` anywhere in the
representation theory of this group.

> **No `G`-invariant complex structure exists on any sector, so no Hodge star can
> be built from the module structure at all. It must be imposed from outside the
> symmetry.** `BT1408`'s Remark is closed, with a reason rather than an absence.

The scope, stated so it is not over-read: this is *expected* for a Weyl group —
`PGSp(4,3) ≅ W(E₆)` has rational character table, and rationality forces
`FS = +1` throughout. What is new is not the indicator computation but the
consequence: the missing star is not an oversight in the construction, it is
forbidden by `W(E₆)` being a reflection group.

**The photonic reading**, which is why this was worth doing separately. In an
optical realisation, an invariant `J` is exactly what lets a sector carry a
symmetry-respecting *phase* — a `U(1)` acting inside one irreducible block.
There is none. Every sector of the substrate is **amplitude-only**: interference
between two states of the same sector cannot be described by a phase the symmetry
preserves. A photonic implementation must therefore supply its own external phase
reference; the substrate will not generate one. That is a derived engineering
constraint, not a modelling choice, and it is the sharpest thing the "wedge /
Hodge star / dot product in optics" question has produced so far — the dot
product (invariant, real, symmetric) survives, the star does not.

---

## Prior art

- [BT1408](analysis/BT1408_frame_cross_matching_theorem_insert.tex) — **owns** the
  no-Hodge-star Remark that Pass 1866 closes.
- [BT795](analysis/BT795_spread_envelope_routing_cell.md) / BT790 — **own** the 36
  spreads and the `K₁₀`.
- Passes 1841–1845 (parallel track) — **own** the 28,800 signature resolutions;
  `χ(H) = 9` stays open and nothing here decides it.
- Pass 1828 — the `q = 3` trap this generalises; Pass 1830 — the failed naming
  Pass 1863 completes; Pass 1819 — the bit independence Pass 1864 refines.
- The Ramanujan/expander framing was checked against the corpus **before**
  computing and is already held there (17 prior mentions), so this batch does not
  touch it.

## Still open

- `χ(H) = 9`.
- The `1/q` law at `q = 7`, and a proof rather than three data points.
- What the fibre-10 over the 27 lines is.
