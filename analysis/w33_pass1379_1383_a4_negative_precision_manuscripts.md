# Passes 1379–1383 — the A₄ is a coincidence, the sweep's first measured precision, and both manuscripts are clean

Five results. Three are negatives, and two of those refute predictions I made in
the previous batch. That is the point: every claim below was checked rather than
carried forward.

---

## Pass 1379 — the A₄ is NOT structural, and the discriminator is the action

Pass 1377 found A₄ appearing three times: as the derived subgroup of the frame
stabiliser in `PSp(4,3)`, again as the derived subgroup at the `PGSp(4,3)` level,
and inside `Γ(T)′ = 2⁴:C₃` as `2²:C₃`. I flagged the tetrahedral reading — the
tomotope's cells are four tetrahedra — as *the next experiment, stated as a
question*, explicitly not claimed.

**It fails.** A₄ is the rotation group of a tetrahedron, so the discriminating
test is not "is it A₄" but "does it *act* like A₄" — a faithful degree-4
alternating action on an invariant 4-set.

```text
FRAME SIDE
  frame stabiliser        = C2 x S4 = [48,48],  derived subgroup = A4 = [12,3]
  the frame's two lines carry 4 points each: {1,2,3,40} and {4,6,22,34}
  action on line 1's 4 points : order 12 = A4    FAITHFUL
  action on line 2's 4 points : order 12 = A4    FAITHFUL
  orbits on the frame's 8 points = [4, 4]

TOMOTOPE SIDE
  subgroups of order 12 in Gamma(T)' (up to conjugacy): 5, all A4 = [12,3]
    A4  orbits on the 12 points = [6, 6]
    A4  orbits on the 12 points = [12]
    A4  orbits on the 12 points = [12]
    A4  orbits on the 12 points = [6, 6]
    A4  orbits on the 12 points = [6, 6]
  invariant 4-sets: NONE, in any of the five classes
```

The frame's A₄ is the rotation group of a genuine tetrahedron — the four points
of a totally isotropic line — acting faithfully, twice, once on each half of the
frame. The tomotope's A₄ has **no invariant 4-set at all**; every orbit is 6 or
12. Same abstract group, incompatible actions.

**So the A₄ is an order coincidence and is now written down as one.** This is the
same shape as Pass 1375's two S₅'s: abstractly isomorphic, structurally
unrelated. Two for two — in this corpus, an abstract isomorphism between small
groups is worth nothing until the actions are compared.

One further datum against the tetrahedral reading: `⟨ρ₀,ρ₂,ρ₃⟩` does fix
`{1,2,3,4}` pointwise, but the setwise stabiliser of that 4-set in `Γ(T)` induces
only a group of **order 4** on it — not `A₄`, not `S₄`.

---

## Pass 1380 — the selector/Steinberg obstruction is structural, not a bad intertwiner

The parallel track's Pass 1374 reports `Hom_G(ℚ¹²⁰, E₄ℚ¹⁶⁰) = 0`: the natural
selector–flag bimodule annihilates the protected Steinberg sector, with maximum
combined rank 40. That is a statement about one family of maps. Pass 1375 places
the Steinberg carrier's stabiliser as an `S₅` that does **not** lie in `PSp(4,3)`.
Those are two views of one obstruction, and the subgroup lattice adjudicates:

```text
maximal subgroups of W(E6) whose order is divisible by 432 : [25920, 1296, 1296]
  25920 = PSp(4,3)  (index 2)  contains a conjugate of the S5?  FALSE
   1296            (index 40)  contains a conjugate of the S5?  FALSE
   1296            (index 40)  contains a conjugate of the S5?  FALSE
```

**No maximal subgroup of `W(E₆)` that is large enough to contain a 432-selector
stabiliser contains the Steinberg carrier's `S₅`.** In particular the index-2
maximal `PSp(4,3)` contains selector stabilisers of order 432 and no conjugate of
the `S₅` — which is exactly Pass 1375's `S₅ ∩ PSp(4,3) = A₅`, re-derived from the
lattice.

**Scope, stated precisely.** This does not prove "no bridge exists". It shows the
two objects cannot be simultaneously stabilised inside any of the three maximal
subgroups that could host the selector, so a bridge cannot be built by descending
to a common overgroup of that kind. That is a sharpening of Pass 1374's `Hom = 0`
from "this family of maps fails" toward "the failure is lattice-level", and no
further.

---

## Pass 1381 — the boundary sweep's first measured precision: 2 of 5

I built the sweep, wired it into CI, and never validated one candidate — the same
unfalsifiability the tool exists to prevent. Adjudicating the top five by reading
both files:

| boundary → later file | verdict |
|---|---|
| `BT808_600cell_icosahedral_orbits` → `BT809_register_f4_regular_spread` | **HIT** |
| `2026-07-08_pass76_QEC_codes_alpha_code` → the `[[137,1,3]]` thread | **HIT** |
| `BT1204_holonet_milestone_dashboard` → `BT1214_encoded_clifford_tomography` | miss |
| `w33_pass1117_1119_aliases_orbits_trees` → `THE_SELECTION_LAYER` | miss (tool defect) |
| `2026-07-08_pass70_15vector_doily_attack` → `pass72_cumulative_bijection` | miss |

**Precision 40% on the top 5.** For an advisory tool that is usable — the base
rate for a random later file is effectively zero — and it is now a number rather
than a hope.

**Hit 1 is exact.** BT809's opening line is *"Closes the three BT808 boundary
questions, all GAP-confirmed."* BT808's Boundary still read `Open:`. This is the
BT810/BT811 pattern precisely, caught before a pass was spent on it. BT808 now
points at BT809.

**Hit 2 is worse than stale.** `pass76` asks "Exact distance of `[[137,1,3]]`: is
d=3 exactly, or higher?" It was answered — `analysis/CANON_137_1_21.md` records
*"the Alpha code is `[[137,1,21]]`, **not** `[[137,1,3]]`"*, refuted and upgraded
— and yet `2026-07-15_pass82_grand_synthesis.md` still asserts `[[137,1,3]]`. The
sweep named `pass82` rather than `CANON_137_1_21`, i.e. it found a *propagator* of
the dead value rather than the answer. Still a true positive, and arguably the
more useful pointer.

**One miss was a real tool defect, now fixed.** `RE_INLINE_OPEN` was
`^\s*(?:>\s*)?Open:` — it accepted **blockquoted** `Open:` lines. So
`w33_pass1117_1119`, which quotes BT810's open list verbatim *in order to say it
was already answered*, registered as owning that boundary itself. A file
discussing someone else's open question was treated as having it. The blockquote
alternative is removed; the sweep drops from 34 candidates to 32.

---

## Pass 1382 — the group grammar's retrospective rate is 8.4%, *lower* than I predicted

I predicted the uncited-duplication rate for group results would be "plausibly
higher" than the 21% Pass 328 measured for code parameters, on the reasoning that
group results are the modal claim type here. Measured over all 1254 analysis
files:

```text
distinct group tokens                       : 108
usable (appear in 2-8 files, so a result
        rather than a topic)                : 48
files asserting a usable group token that
  an UNCITED file also asserts              : 105
rate                                        : 8.4%
```

**8.4%, against 21% for code parameters.** My prediction was wrong, and the
direction is informative: group notation is *less* prone to silent duplication
than code parameters, most likely because a `SmallGroup` ID or an `n^k:Cm` is
distinctive enough that authors notice the collision themselves, whereas
`[[n,k,d]]` triples look interchangeable. The token class still earns its place —
it is what catches BT781 → BT782 — but it is a scalpel, not the main vein.

---

## Pass 1383 — both manuscripts are clean, and the erratum's target was real

The false-cubic quarantine had never been pointed at the two manuscripts, where
84 `theorem` environments live. Scanning `w33_paper.tex` (16,298 lines) and
`photonic_holonet.tex` (9,531 lines) for eight signatures — the eigenvalue set
`{−7,−1,5}`, multiplicities `{16,10,6}`, both forms of the old cubic, the 32-dim
packet, `Z(−1)=0`, and the Taylor coefficients `8,−248`:

```text
w33_paper.tex        : 0 hits    corrected spectrum present (line 1020)
photonic_holonet.tex : 0 hits
```

**Both are clean.** And the history settles what the erratum was actually
correcting. Before commit `3efbd4a68`, `w33_paper.tex` contained

```latex
\begin{theorem}[Master Cubic]\label{thm:mastercubic}
\boxed{(t+1)\bigl[(t+1)^2 - (2q)^2\bigr] \;=\; 0,}
with roots $t = -1$, $t = -1 + 2q = 5$, and $t = -1 - 2q = -7$.
```

so the erratum's target was **real**, not a strawman. The sequence is: erratum
committed 14:21, manuscript repaired by `3efbd4a68` (Passes 1137–1140) at 17:19
the same day, on a parallel branch. `eq:mastercubic` now reads
`(t−11)(t−1)(t+5)=0` and the theorem explicitly states there is no 32-dimensional
`D`-invariant restriction of the point carrier.

**Consequence for the open queue:** the parallel track's standing next step
"quarantine every descendant of the false cubic" is, for the two manuscripts,
already done and now verified. Any remaining quarantine work is in `analysis/`
and `data/`, not in the papers.

## Prior art

- [Pass 1377](analysis/w33_pass1375_1378_s5_tomotope_a4_guard.md) — posed the A₄ question refuted above.
- [BT808](analysis/BT808_600cell_icosahedral_orbits.md) / [BT809](analysis/BT809_register_f4_regular_spread.md) — the stale boundary and its closure.
- [CANON_137_1_21](analysis/CANON_137_1_21.md) — **owns** the `[[137,1,21]]` correction.
- Pass 1374 (parallel track) — the `Hom = 0` selector obstruction sharpened above.
- `3efbd4a68` Passes 1137–1140 — **own** the manuscript repair of the Master Cubic.
