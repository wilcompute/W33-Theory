# Passes 1872–1876 — the `1/q` law has a mechanism, the 270 is named, and a phase costs more than any maximal subgroup

Five items. Two close questions I left open last batch; one is a clean negative I
am reporting as a negative.

---

## Pass 1872 — `1/q` holds at `q = 7`, and the reason is a **perfect matching**

`GQ(7,7)` built from scratch: 400 points, 400 lines, 11,200 edges, a spread of 50
lines.

```text
q   leftover  candidates  needed  equal?   touched     fraction   1/q
3      60         15        15     yes     20/60      0.333333   0.333333
5     390         65        65     yes     78/390     0.200000   0.200000
7    1400        175       175     yes    200/1400    0.142857   0.142857
```

The law holds exactly at `q = 7`. But the numbers say more than the ratio does:

```text
touched = 20, 78, 200   and   points = 40, 156, 400
```

`touched = |points| / 2` in every case. Tested directly:

```text
q=3: 20 edges on 40 distinct points -- pairwise disjoint: TRUE
q=5: 78 edges on 156 distinct points -- pairwise disjoint: TRUE
q=7: 200 edges on 400 distinct points -- pairwise disjoint: TRUE
```

> **The admissible completing frames pile their matchings `q`-fold onto a single
> PERFECT MATCHING of the point set.** Since the leftover has
> `(q²+1)q(q+1)/2` edges and a perfect matching has `(q+1)(q²+1)/2`, the touched
> fraction is exactly `1/q`, and `(1 − 1/q)` of the leftover is untouchable.

That is a mechanism, not a fitted law. It also explains the multiplicity Pass
1828 measured at `q = 3` ("each 3 times") — the multiplicity is `q`, forced by
counting: `(q²+1)q/2` candidates × `(q+1)` edges each, landing on
`(q+1)(q²+1)/2` distinct edges, is exactly `q`-fold. And it explains the even
case: at `q = 2` there are no candidates at all, so there is no matching to
land on.

Four data points and a counting argument. What remains is to show the candidate
matchings *must* lie in a perfect matching, which now looks like a short proof
rather than a search.

---

## Pass 1873 — the resolution, attacked properly, and still out of reach

Pass 1861 made covers findable. A resolution is a partition of the 540 frames
into 9 exact covers, so: generate covers with randomised MRV, then build a
resolution class by class, each class forbidding the frames already used.

```text
distinct exact covers generated : 25 in 153 s   (~6 s each)
resolution build, 31 trials     : best 2 of 9 classes (120 of 540 frames)
RESOLUTION FOUND                : False
```

Reported as a negative. Two things it does establish. Covers are *findable* but
still expensive — 6 seconds each, so they are rare rather than abundant. And the
class-by-class build dies at **2**: once 120 frames are removed, a third exact
cover on the remainder could not be found within the cap. That is a much sharper
failure point than "the search stalls," and it is where the next attempt should
aim — the obstruction, if there is one, bites between the second and third class.

---

## Pass 1874 (physics) — the degree-24 is the duality-invariant one

Pass 1864 found the 24 is the only chiral block whose sign agrees on both
geometric readers. Why:

```text
40-POINT permutation module : 1 + 15(#6) + 24(#14)
40-LINE  permutation module : 1 + 15(#9) + 24(#14)
```

> **The gauge sector `15 ⊕ 24` is exactly the nontrivial part of the 40-point
> permutation module** — that is, the exact 1-forms `d(functions on points)`,
> which is what a gauge sector should be, and `40 − 1 = 39 = 15 + 24` confirms it.

And the point/line duality of `W(3,3)` acts on that module by **fixing the
degree-24 and moving the degree-15 to a different irreducible** (`#6 → #9`). The
substrate's gauge block carries `#6`, the *point* version.

So the 24's agreement on both readers is not a coincidence: it is the constituent
the duality cannot move. The 15's disagreement is the duality acting. Stated at
the scope measured: `#6 ≠ #9` as irreducibles, and the 24 is literally the same
`#14` in both modules — whether `#9 = #6 · ε` exactly is one check further and is
not claimed here.

---

## Pass 1875 — the 270 is the ordered incident pairs of the 27 lines

Pass 1863 found `270 = 27 × 10` group-theoretically. The geometry:

```text
index-27 maximal        : order 1920 = 2^4 : S5
action on the 27        : transitive, RANK 3
suborbit lengths        : 1, 10, 16
```

Rank 3 with suborbits `1, 10, 16` is exactly the cubic-surface incidence
structure — each of the 27 lines meets **10** others and is skew to **16**. And:

```text
stabiliser of an ORDERED incident pair : order 192
|G| / 270                              : 192
centraliser D8 x S4                    : 192
```

> **The size-270 conjugacy class is in bijection with the 270 ordered pairs of
> intersecting lines on the cubic surface.** `27 × 10 = 270`.

The object CLAUDE.md's failure mode 3 told me not to name gesturally now has a
name, and it is a classical one. Pass 1830's two guesses failed because both
looked at what the *element* fixes; the class is named by its centraliser.

---

## Pass 1876 (physics / photonics) — a phase costs more than any maximal subgroup

Pass 1866 showed no `G`-invariant complex structure exists, so an imposed Hodge
star must break the symmetry. How much? Over `ℝ` an invariant `J` exists on a
module iff every real-type constituent occurs with **even** multiplicity. Tested
on the physical 81 for `G`, for `PSp(4,3)`, and for every maximal subgroup:

```text
PGSp(4,3)          51840   index  1   admits J: false
PSp(4,3)           25920   index  2   admits J: false
2^4 : S5            1920   index 27   admits J: false
C2 x S6             1440   index 36   admits J: false
(S3 x S3 x S3):C3:C2 1296  index 40   admits J: false
((C3xC3):C3:Q8):C3:C2 1296 index 40   admits J: false
2^3:2^2:(C3xC3):C2:C2 1152 index 45   admits J: false
```

> **No maximal subgroup of `W(E₆)` admits an invariant complex structure on the
> physical sector.** Breaking the symmetry by one step — even all the way to the
> index-45 polar-pair stabiliser — still buys no phase.

The photonic reading, and the reason this was worth doing: giving the substrate a
symmetry-respecting optical phase on the physical sector is not a small
concession. It costs strictly more than any single maximal reduction of `W(E₆)`,
so a realisation that wants interference in the 81 must descend at least two
steps in the subgroup lattice. Pass 1866 said the star must be imposed; this
prices it.

---

## Prior art

- [BT1408](analysis/BT1408_frame_cross_matching_theorem_insert.tex) — **owns** the
  no-Hodge-star Remark; Pass 1866 closed it, Pass 1876 prices it.
- [BT795](analysis/BT795_spread_envelope_routing_cell.md) / BT790 — **own** the 36
  spreads and the `K₁₀`.
- Passes 1841–1845 (parallel track) — **own** the certified signature
  resolutions; `χ(H) = 9` remains open and Pass 1873 does not decide it.
- Passes 1861/1865 — the MRV search and the `1/q` law this batch extends and
  explains; Pass 1830/1863 — the failed and partial namings Pass 1875 completes.

## Still open

- `χ(H) = 9`. Pass 1873 localises the failure to the second-to-third class.
- A proof that the candidate matchings must lie in a perfect matching.
- Whether `#9 = #6 · ε`, which would make the gauge bit *exactly* the point/line
  duality.
- The largest subgroup admitting `J` — it is below maximal, and finding it is now
  a lattice search rather than a question.
