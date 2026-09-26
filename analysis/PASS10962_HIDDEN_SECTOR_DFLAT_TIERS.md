# Pass 10962 — the hidden sector does not rescue matter parity

Producer: `analysis/w33_pass10962_hidden_sector_dflat_tiers.py`
Tier C reproducer: `analysis/w33_pass10962_tierc_rays.py` (~15 min)
Frozen input: Pass 10960 ledger + `data/w33_pass10962_hidden_gauge_ledger.json.gz` (hidden gauge group of every slot, from the vector multiplets of the raw spectra)
Certificates: `data/w33_pass10962_hidden_sector_dflat_tiers.json`, `data/w33_pass10962_tierc_rays.json`
Regression: `tests/test_w33_pass10962_hidden_sector_dflat_tiers.py` (89 tests, ~15 s)

## The loophole

Pass 10960 closed, exactly, every FI-cancelling D-flat **singlet** vacuum of the 88
W(3,3) Z6 Standard Models with a B−L direction: none preserves matter parity. It named one
loophole — Standard-Model singlets charged under the **hidden** gauge group (SU(2), SU(3),
SU(4), SU(5), SO(8), SO(10) factors), whose parity can be compensated by a hidden gauge
element. This pass closes it in three tiers.

## Tier A — exact, every hidden direction (32 models)

A D-flat vacuum is D-flat for the hidden maximal torus; a parity-preserving vacuum is fixed
by P·h with h conjugable into that torus. So split hidden fields into weight components,
impose U(1) + hidden-torus D-flatness + FI cancellation, and let the parity of a component be
3(B−L)·q + 2η·w with **both** the B−L freedom t and the hidden torus element η free. For 32
models the ever-even components carry an exact Farkas vector: **no hidden-sector direction of
any kind rescues matter parity.** (Weight systems of every hidden representation are
generated and checked: SU(n) exterior/symmetric powers and adjoints, SO(2n) vectors,
spinors, adjoints.)

## Tier B — exact over invariant generators (55 models)

By Luty–Taylor and Kempf–Ness, a parity-preserving D-flat vacuum exists iff some
FI-cancelling product of hidden-group invariant generators exists with every generator
matter-even (the parity element fixes the invariants, hence the unique closed orbit in the
fibre, hence a Kempf–Ness point up to a compact gauge transformation). The generators used:
SM × hidden singlets; every quadratic invariant (conjugate pairs; real and bi-doublet
squares); SU(N) baryons and antibaryons; SU(5) 10·10·5 and 10·5̄·5̄. For 55 models the
ever-even generators carry an exact Farkas vector. **Scope:** completeness of this generator
set is *not* proved for these models (each contains bi-fundamental, SU(4) 6 or SU(5) 10
hidden fields), so the statement is "no rescue among the standard invariants".

## Tier C — the last model, exactly (Z6II_23…2913)

Its generators do admit FI-cancelling D-flat directions. Exact cdd (GMP) enumeration of the
cone over the 46 ever-even generator types: **62,309 extreme rays, 2,846 FI-cancelling, 0
realizable** — each obstructed by a Smith-normal-form parity certificate over the full B−L
freedom (HiGHS MILP agrees: infeasible).

## The anomaly-free models

The four anomaly-free Z6-II models (no FI term; the origin is D-flat) admit **no matter
parity at all**: no B−L direction and zero Z2 characters of the charge lattice odd on every
q, u^c, d^c, e^c.

## Verdict

Across the whole W(3,3) Z6 class, matter parity survives no supersymmetric vacuum: exactly
for singlet directions (Pass 10960), exactly for every hidden direction in 32 models, exactly
over the standard invariant generators in the remaining 56, and vacuously in the 4
anomaly-free models. The one remaining gap is completeness of the invariant generators for
the 55 Tier-B models.

## Also in this pass: Z12-I carries the W(3,3) twist and hosts Standard Models (pilot)

The same Kac-coordinate enumeration (Holotrade ed67ee5) applied to Z12-I on the E6 lattice
(v = (1/12, −5/12, 1/3)) gives 270 E8 classes of order dividing 12, 3026 modular-invariant
E8 × E8 pairs, and **1167 pairs whose Z3 part (θ⁴) carries the W(3,3) twist — all of them
exactly (A8, D7+U1), the SU(9) × SO(14) × U(1) vacuum**. A pilot random-Wilson-line scan
already found Standard Models; the first four spectra fail the same test (no FI-cancelling
singlet vacuum at all; their fixed-parity singlets again have 3(B−L) = 3). A full campaign
is running and will be reported as its own pass.

Prior art: Pass 10960; Holotrade ed67ee5 (Kac enumeration, orbifolder validation), 28620b4,
2ebfb50; Luty & Taylor, Phys. Rev. D 53 (1996) 3399; Kempf & Ness (1979).
