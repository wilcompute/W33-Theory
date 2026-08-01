# Passes 1882–1887 — the obstruction is the spread's own involution, the 90 is the only complex sector, and the free cuts provably cannot help a solver

Six items. One unifies two separate arcs; one is the strongest physics statement
of the batch; one is a negative that I predicted myself three batches ago and can
now confirm at solver level. The resolution is still open, and one of my own
models turned out to be buggy.

---

## Pass 1882 — the matching **is** a collineation, and it is the chirality reader

Pass 1877 showed the completing frames' edges form a perfect matching of each
spread line. The obvious question is whether that matching is a group element.
Building it as a permutation `σ` of the points and testing directly:

```text
q=3: fixed-point-free involution TRUE | a COLLINEATION TRUE | fixes each spread line TRUE
q=5: fixed-point-free involution TRUE | a COLLINEATION TRUE | fixes each spread line TRUE
q=7: fixed-point-free involution TRUE | a COLLINEATION TRUE | fixes each spread line TRUE
```

> **Each spread `S` carries a canonical collineation `σ_S` — a fixed-point-free
> involution fixing every line of `S` — and the candidate frames' matching edges
> are exactly `σ_S`'s 2-cycles.**

That completes the mechanism. `σ_S` acts fixed-point-freely on each `(q+1)`-point
line, which is possible only when `q+1` is even, so `q` odd gives the matching and
`q` even gives none — the `1/q` law and the `q = 2` exception in one object.

And at `q = 3`, `σ_S` fixes 0 points and 10 lines. That is precisely the size-36
conjugacy class of Pass 1485/1829 — **the class in bijection with the 36 spreads,
and one of only two classes sensitive to all four handedness bits**.

> **The same group element that reads the substrate's complete handedness also
> generates the obstruction to the resolution.**

Two arcs that ran separately for dozens of passes — chirality and the resolution
— turn out to be driven by one involution.

---

## Pass 1885 (physics) — the degree-90 is a **complex** representation, and it is the only one

Pass 1880 found the degree-90 admits an invariant complex structure at index 2,
which was odd — why should the constraint block be so cheap? Because it is not
really a real representation at all:

```text
Res_PSp(4,3) (90) = 45 + 45,  each with FS indicator 0  [COMPLEX type]
are the two constituents complex conjugates of each other? TRUE
dim End_PSp(90) over R = 2
```

> **The constraint sector's degree-90 is a 45-dimensional COMPLEX representation
> of `PSp(4,3)`, seen as a real 90.** It is the unique sector of the substrate
> carrying a genuine `U(1)`.

This explains the index-2 price exactly. The complex structure already lives
inside `PSp(4,3)`; the outer involution is precisely what conjugates the two
degree-45s and destroys it. So the outer element of `W(E₆)` is the thing that
makes the substrate real.

Combined with Pass 1880: the physical 81 is parity-obstructed and can never be
complex at any subgroup; the 90 is *already* complex and needs only the outer
involution removed. Phase and chirality are controlled by the same `ℤ/2`.

---

## Pass 1884 — what `#14` is: ubiquitous, but not universal

Three unrelated `G`-sets carry the same degree-24, so I checked all six natural
ones:

```text
points_40   : 1 + 15(#6) + 24(#14)
lines_40    : 1 + 15(#9) + 24(#14)
octets_45   : 1 + 20(#11) + 24(#14)
frames_540  : 1 + 15(#7) + 15(#9)x2 + 20(#11)x2 + 24(#14)x2
                + 60(#18) + 60(#19)x2 + 64(#21) + 81(#23) + 81(#24)
cubic_27    : 1 + 6(#4) + 20(#11)
spreads_36  : 1 + 15(#9) + 20(#11)
```

`#14` appears in 4 of 6 — points, lines, octets, frames — and is **absent** from
the 27 and the 36. Its complement `#11` (degree 20) appears in exactly the other
four: frames, 27, 36, octets. So the natural `G`-sets split into a `#14` family
and a `#11` family overlapping only on frames and octets.

A detail worth recording: `frames_540` contains **both** degree-81 extensions,
once each. The frames see both chiralities symmetrically as a module; it is the
*eigenspace* (Pass 1492) that picks one.

---

## Passes 1883/1886 — the `k`-ladder, and a bug in my own model

Asking how many pairwise disjoint exact covers exist, by CP-SAT:

```text
k=1 : OPTIMAL   0.6 s
k=2 : OPTIMAL   127.9 s
k=3 : UNKNOWN   420 s, 815,976 conflicts
k=4 : UNKNOWN   420 s, 222,801 conflicts
k=5 : UNKNOWN   420 s,   4,401 conflicts
```

**The `k ≥ 3` rows are not evidence, because the model is wrong there.** My
symmetry break fixes the frames of clique 0 to colours `0..k−1`. At `k = 9` that
is genuinely without loss of generality, since all nine frames of the clique are
coloured, one per colour. At `k < 9` only `k` of the nine are used, so the
constraint additionally dictates *which* `k` — an extra restriction, not a
symmetry break. Pass 1878 already exhibited three disjoint covers by exhaustive
search, so `k = 3` is satisfiable and the `UNKNOWN` there reflects my bug plus the
time limit, nothing about the mathematics.

Recorded rather than quietly deleted: this is the same class of error as the
heredoc and the `PositionProperty` traps — a construct that is valid in one
regime silently reused in another.

---

## Pass 1887 — three solver attacks, and a negative I had already predicted

**The reformulation** (verified, and worth keeping regardless of the outcome).
Every edge lies in exactly 9 frames, all mutually adjacent, so each edge is a
9-clique of `H`; `H` is 32-regular and `32 = 4 × 8`, forcing any two adjacent
frames to share exactly one edge. Checked:

```text
pairs covered by the 240 cliques : 8640 = edges of H,  cliques edge-disjoint: TRUE
=> chi(H) = 9  <==>  540 variables in 1..9 with 240 AllDifferent(9) constraints
```

That replaces the 4,860-variable / 99,909-clause CNF of five earlier attempts
with a small CP model.

**Attempt 1, plain CP-SAT**: `UNKNOWN` at 900 s — 2,127,575 branches but only
3,622 conflicts. That ratio is the signature of unbroken symmetry.

**Attempt 2, prescribed automorphism**: build collineations directly as
symplectic transvections, find elements of order 3 and 9, and demand an
`S`-invariant colouring so the unknowns become orbits. Every candidate was
**rejected before solving**: some 9-clique always contains two frames of the same
orbit, which no rainbow colouring can tolerate. 14 of 14 rejected.

**Attempt 3, add the free cuts.** Passes 1613/1817/1827/1828 proved exact
identities every class must satisfy — 60 frames per class, exactly 8 per octet
family, exactly 12 per point family, at most 5 per spread `K₁₀`. Adding all of
them:

```text
UNKNOWN at 1500 s — 255,166 branches and 163 conflicts
```

Branches fell 8× and conflicts fell **22×**, to almost nothing. That is not the
solver doing better; it is the solver finding almost no contradictions to learn
from.

> **The free cuts cannot help a search, and Pass 1818 said so.** A cut is "free"
> exactly when its indicator has zero `(−4)`-eigenvalue mass — which is precisely
> the statement that it is already implied by the spectral relaxation. Pass 1818
> measured their branching value as `0.0000` and I added them to a solver anyway.
> 163 conflicts is that measurement, confirmed operationally.

The corollary is directional rather than dispiriting: the constraints worth
adding are the ones with **nonzero** `(−4)`-mass, and Pass 1818 already ranked
them — the spread-pair family at `0.9535`. Only a weak inequality for it was used
here.

---

## Cross-track convergence

The parallel track's Passes 1882–1886 branch the five sectors to the exceptional
`S₆` and find the natural constituent `V₉ = [4,2]` occurring with multiplicities
`(0,1,0,0,1)` across `(15, 24, 30, 81, 90)` — singling out **the 24 and the 90**,
with the two copies isometric and orthogonal. Those are exactly the two blocks
this batch singles out independently: the 24 is the duality-stable, `G`-set
ubiquitous one (Pass 1884) and the 90 is the uniquely complex one (Pass 1885).
Two very different computations picking the same pair. They also adopt the parity
obstruction from Pass 1880 for the 81, which is consistent with the ownership
here.

---

## Prior art

- Pass 1485/1829 — **own** the size-36 spread involution class that Pass 1882
  identifies as the obstruction's generator.
- [BT795](analysis/BT795_spread_envelope_routing_cell.md)/BT790 — **own** the 36
  spreads and the `K₁₀`.
- Pass 1818 — **owns** the branching-value measurement that Pass 1887 confirms.
- Pass 1878 — **owns** the exhaustive three-cover result that invalidates the
  `k ≥ 3` rows here.
- Passes 1841–1845 and 1882–1886 (parallel track) — the certified resolutions and
  the `S₆` branching.

## Still open

- `χ(H) = 9`. Three solver attacks, all `UNKNOWN`; no attempt has yet used the
  high-branching-value spread family as decision variables.
- A written proof that `σ_S` exists for every spread and every odd `q`.
- Whether the 90's invariant `J` is unique up to conjugacy, which would make its
  `U(1)` canonical rather than merely available.
