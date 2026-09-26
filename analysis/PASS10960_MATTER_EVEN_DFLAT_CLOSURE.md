# Pass 10960 — the FI term forces a B−L = ±1 condensate: exhaustive matter-even D-flat closure

Producer: `analysis/w33_pass10960_matter_even_dflat_closure.py`
Ledger (frozen input): `data/w33_pass10960_heterotic_left_chiral_ledger.json.gz`
Certificate: `data/w33_pass10960_matter_even_dflat_closure.json`
Z2-character certificates: `data/w33_pass10960_z2_character_certificates.json.gz`
Regression: `tests/test_w33_pass10960_matter_even_dflat_closure.py` (91 tests, ~60 s)

## The question

The heterotic route to the Standard Model on the W(3,3) twist produced 215
three-family Standard Models in the Z6-I and Z6-II orbifolds (Holotrade 5b3f3ad and
successors; recorded row by row in the `w33_paper_body.tex` ledger). Their live
question — open problem 1 of the *Forty Points* paper — was:

> Is there a vacuum that cancels the anomalous Fayet–Iliopoulos term with D-flat
> singlet VEVs while condensing **only matter-even singlets**?

Yes would rescue the class with proton stability; no excludes it as a realistic
MSSM in singlet vacua. The previous answer (Holotrade 28620b4, TOE ledger
`a3dbdf2d7`) was a *sampled* zero (60 B−L choices per model) and was explicitly
not a proof. The Holotrade gate (2ebfb50/6fbd638) recorded why it could not be
finished: the raw spectra `sp1/*.sp`, `sp2/*.sp` were in no repository.

## 1. Provenance closed

The raw orbifolder spectra were recovered from the WSL scan tree
(`~/orb/scan/cp/spec1`: 87 Z6-I; `~/orb/scan/cp2/sp`: 128 Z6-II — the gate's
sp1/sp2) and frozen as a normalised left-chiral ledger with exact rational U(1)
charges (every charge denominator divides 18; float residual < 1e-9 asserted).
Its SHA-256 is recorded in the certificate and checked by the test.

## 2. The gate contract, executed without sampling

For each model: hypercharge solved exactly; SM-singlets = fields trivial under
every nonabelian factor with Y = 0, grouped by charge vector; the anomalous U(1)
identified by the trace (all other traces vanish exactly; sign of the FI term
taken from the trace). B−L = x0 + N t is the full rational solution set of
B−L(q, u^c, d^c, e^c) = (1/3, −1/3, −1/3, 1).

| outcome (88 models with a B−L direction) | models | exact certificate |
| --- | --- | --- |
| no D-flat direction at all | 64 | Farkas vector λ: s·c_s + λ·m_s ≥ 0 on every singlet type |
| D-flat, but the singlets that can be even for **some** t are never D-flat | 23 | one Farkas vector on that union |
| every anomaly-cancelling extreme ray parity-obstructed | 1 (Z6II_23…2913) | 3334 exact rays (cdd, GMP), 304 cancel the FI term, each non-realizable by a Smith-normal-form obstruction |
| **matter-even D-flat direction** | **0** | — |

Why the three certificates are complete: D-flat feasibility is monotone in the
allowed support, every realizable even set lies inside the union of ever-even
types, and any FI-cancelling D-flat vector decomposes into extreme rays of the
pointed cone, at least one of which cancels the FI term; a realizable even set
containing it would make that ray's support realizable.

## 3. The physics of the obstruction: a B−L = ±1 condensate is forced

In all 23 Z6-I models of the middle row, exactly two singlet types are never even,
and **both have 3(B−L) = 3 fixed by the Standard Model itself** — B−L = +1, the
quantum numbers of a right-handed (s)neutrino — for every admissible B−L. Every
D-flat direction of these models switches one of them on (asserted in the test
against the exact D-flat witness). In Z6II_23…2913 the never-even types carry
3(B−L) = ±3 likewise.

So the anomalous U(1) forces B−L to be broken by a field with |B−L| = 1. This is
precisely the case in which Martin's criterion (Phys. Rev. D 46 (1992) R2769) says
R-parity does not survive: the unbroken remnant of U(1)_{B−L} contains matter
parity only if B−L is broken by fields with even 3(B−L). Realistic SO(10) models
use B−L = ±2 (126-type) breaking for this reason; here the FI term leaves no such
option.

## 4. A strictly more general parity family: every Z2 character

Independently of B−L, every Z2 character of the full U(1) charge lattice (Hermite
basis; ≤ 2^10 characters per model) that is odd on all q, u^c, d^c, e^c fields was
enumerated in all 211 anomalous models: 1024 such characters exist, in 64 models;
**none** makes its even singlets D-flat (1024 exact Farkas certificates, gzip
store). In the 23 D-flat Z6-I models no such character exists at all: their matter
parity can only be a higher-order element (some field has fractional 3(B−L)).

## 5. Controls

* The exact machinery reproduces the prior D-flat census **23 Z6-I + 105 Z6-II =
  128** with exact witness rays, and **88** models with a B−L direction.
* Realizable parity classes are found (with explicit rational t) whenever they exist:
  single ever-even types are realizable in every model; synthetic solvable and
  unsolvable congruence systems are classified correctly.
* Four Z6-II models are anomaly-free (no FI term): recorded, excluded from the
  question (the origin is D-flat).

## Verdict

**In singlet vacua, no model of the W(3,3) heterotic class preserves a matter
parity.** 83 of the 211 anomalous models have no supersymmetric singlet vacuum at
all; every other model with a B−L direction must condense a B−L = ±1 singlet,
spontaneously breaking R-parity, so the dimension-four baryon- and lepton-number
violating couplings are regenerated at order ⟨n⟩/M_s ≈ 0.2–0.4 (TOE ledger
`cfdc1f2`) unless suppressed by further selection rules. This supersedes the
sampled zero of 28620b4 and resolves open problem 1 of the Forty Points paper in
the singlet scope — negatively.

## Scope and remaining loopholes

* Only SM × hidden **singlet** directions (the gate's contract). Hidden nonabelian
  directions (e.g. SO(10)′ spinor or SU(2)′ doublet composites), whose parity can
  be compensated by hidden centre elements, are not covered and are the one
  remaining loophole for a matter-parity-preserving supersymmetric vacuum.
* R-parity violation is regenerated in general; whether the induced couplings are
  suppressed below the proton bound by higher-order selection rules in a specific
  model is not addressed.
* Non-supersymmetric vacua are outside the question.

Prior art cited: Holotrade 0fee779, 28620b4, bd6c60e (Gordan), babfd48, 2ebfb50
gate; TOE ledger commits 78ec0a0fc, a3dbdf2d7; Lebedev et al. arXiv:0708.2691
(matter parity from the Z2 of B−L); S. P. Martin, PRD 46 (1992) R2769.
