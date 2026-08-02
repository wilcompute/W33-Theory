# Pass 2016 — the `1/q` law is just a perfect matching in `K_{q+1}`

Credit where it belongs: this came from the user's observation that `6 × 11 = 66`
is the edge count of `K₁₂`. It is not a numerical coincidence — it is the whole
theorem, and it collapses four passes of machinery into one line.

## The residual set is a disjoint union of complete graphs

Each totally isotropic line has `q+1` points, and every pair of them is
collinear — so **a line's internal edges form a `K_{q+1}`**. The residual set
after a spread seed is exactly the internal edges of the spread's own lines, so:

```text
  q   spread lines   C(q+1,2)   product   residual (measured)
  3            10          6         60          60   match
  5            26         15        390         390   match
  7            50         28       1400        1400   match
 11           122         66       8052        8052   match
```

> **The residual set is `q²+1` disjoint copies of `K_{q+1}`.**

At `q = 11` each line is a `K₁₂` with **66 edges**, and `122 × 66 = 8052`.

## The touched set is one perfect matching per copy

`σ_S` fixes every spread line setwise and is fixed-point-free, so on each line it
is a fixed-point-free involution of `q+1` points — a **perfect matching of that
`K_{q+1}`**, with `(q+1)/2` edges:

```text
  q   (q+1)/2 per line   x lines   touched (measured)
  3                 2         20          20   match
  5                 3         78          78   match
  7                 4        200         200   match
 11                 6        732         732   match
```

## Therefore

```text
touched / residual = [(q+1)/2] / [q(q+1)/2] = 1/q
```

> **The `1/q` law is the ratio of a perfect matching to all edges of `K_{q+1}`.**
> Nothing about symplectic geometry enters the ratio at all — the geometry only
> supplies the decomposition into `K_{q+1}`s and the involution that matches each
> one.

And the `q`-even branch becomes trivial: `K_{q+1}` with `q` even has an **odd**
number of vertices, so it has no perfect matching. That is the same statement as
"no non-square `μ` exists in characteristic 2", arrived at without any group
theory.

`q = 11`: matching 6 of `C(12,2) = 66`, and `6/66 = 1/11`.

## On the Ihara zeta and RH — the honest reading

The user also noted that `1/q` appears in Ihara zeta theory. It does, and the
repository has Ihara–Bass and Hashimoto material (parallel track, Passes
1943/1970). But:

- the `1/q` here is a **matching-to-edge ratio in `K_{q+1}`**, derived above with
  no analysis in it;
- the Ihara radius of convergence for a `k`-regular graph is `1/(k−1)`, and
  `K_{q+1}` is `q`-regular, giving `1/(q−1)` — **which is not `1/q`**.

So the numbers coincide and the objects do not, and the two do not even match
once the regularity is put in. I am flagging this rather than pursuing it because
three claims in this arc were false for exactly this reason (Passes 1875, 1984,
2007 — all "matching numbers taken as matching objects"), and the elementary
derivation above leaves no room for a zeta interpretation of *this* `1/q`.

That is not a claim that Ihara theory is irrelevant to the substrate — the
parallel track's `C₄`-twisted Artin–Ihara factorisation is real work on a real
object. It is a claim that **this particular `1/q` is not that `1/q`.**

## The third 66

The user notes 66 is also the edge count of the genus-6 structure from the two
toroidal polyhedra, and the repository has material on both. That is a third
occurrence of 66 and it deserves the same test the other two got: **compare the
objects, not the counts.** For `K₁₂` the identification is exact and structural
(a line *is* a `K₁₂`); for the genus-6 structure it is currently a number, and
`scripts/gset_audit.py` exists precisely to settle that kind of question.

## What this changes

- The `1/q` law needs no proof beyond the two structural facts above, both of
  which are already established: lines are `K_{q+1}`s (trivial), and `σ_S`
  matches each line (Pass 1894, the linewise stabiliser is `C₂`).
- The **candidate-orbit property** — that every residual candidate is
  `{M, σ(M)}` — is untouched by this and remains the one open step. It is a
  statement about which *frames* exist, not about the ratio.

## Prior art

- Passes 1877/1882/1982/2011 — the arc this collapses; Pass 1974 (parallel
  track) — the candidate-orbit scoping that survives it.
- Pass 1894 — **owns** the `C₂` linewise stabiliser.
- The `K₁₂` observation is the user's.
