# Pass 12045: the Barr row as geometry

* **Producer:** `analysis/w33_pass12045_geometric_barr_row.py` (12/12 checks, about 12 s)
* **Certificate:** `data/w33_pass12045_geometric_barr_row.json`
* **Regression:** `tests/test_w33_pass12045.py`
* **Drivers and records:** `analysis/search_drivers_12045/`
* **Track:** Claude. Reservation `e0177b4bb`.

## The question

Pass 12004 and Pass 12044 showed that, with exact CP, the theta quark sector needs one complex vectorlike row (Codex
12005): it is a Nelson–Barr theory. In 12005 that row is three free complex numbers. Is the row itself geometry?

The row index is the d^c (5̄) index c, which is the index of the τ_d torus in the down theta. The natural guess is the
level-3 theta vector of the same torus, with one complex Wilson line w:

  b_c = λ · ϑ_c(τ_d, w),  ϑ_c(τ, w) = Σ_n exp(3πiτ(n+c/3)² + 6πi(n+c/3)w).

The row term B_c D d^c S is hypercharge-neutral. So w is the Wilson line of the CP-breaking scalar's U(1), not of
hypercharge.

Parameter count:
* **Down sector:** 3 theta + 3 row = 6 parameters for the 6 down targets, J included. This is a square system.
* **12005, for comparison:** 8 parameters for the same 6 targets.

## Results

**1. The quark sector is solved exactly, at isolated points.**
* **Branch A.** Im τ_d = 0.158, ε_d = 0.0589i, z_d = 0.0284i, λ = 161, w = −0.0775 − 0.367i.
* **Fit.** All six down targets fit to 10⁻¹², and the Jacobian has full rank.
* **Other branches.** Branches B and C are exact as well. A broad-start catalogue found **at least seven** branches that
  are distinct up to symmetry.
* **Symmetry images.** Within a branch, the other solutions are sign flips and quasi-period shifts of w, with identical
  observables.

**2. CP violation is one number.** All bare moduli sit on the CP locus, and J is an odd function of Re w alone.
* **CP-fixed set.** J = 0 exactly at Re w ∈ ½ℤ, the heavy row's own CP-fixed set.
* **Not at ±⅙.** Re w ∈ ±⅙ + ℤ is *not* CP-conserving: a ℤ/3 shift of w is a right phase on the row that the light
  down matrix does not share.
* **The observed J** needs Re w = −0.0775.

**3. Determinant identity (exact, for any row).** With one heavy row and the shared matching of Codex 12007,
M_d = m·A and M_e = Aᵀ·e. So det A cancels:

  |det M_e / det M_d| = |det e_bare / det d_bare|.

This is checked to 10⁻¹¹ for |b| from 0.16 to 135. The row can move masses around within a sector, but not this ratio.

**4. The charged leptons, branch by branch, with no new parameters (12007's rule).**
Each branch predicts (m_μ/m_τ, m_e/m_μ); the data are (0.0588, 0.00474). The errors are the quark-comparator errors,
propagated linearly.

| branch | m_μ/m_τ | m_e/m_μ | verdict |
|---|---|---|---|
| A | 0.0193 | 0.0364 | sharp (σ_ln 0.08, 0.13): excluded at **13.6σ, 15.8σ** |
| B | 0.528 | 8.3·10⁻⁵ | excluded at 6.3σ, 4.7σ |
| C | 0.0574 | 0.00329 | see below |
| others | (0.129, 0.0017), (0.86, 3·10⁻⁶), (0.77, 10⁻⁵), (0.25, 4.9·10⁻⁴) | | far off |

**Branch C in detail.** Each ratio on its own is uninformative: σ_ln is 2.2 and 4.4. Both are dominated by two inputs:
* the up-sector Weber invariant m_u m_t/m_c² (Pass 11938);
* |V_us|, whose sensitivity is 54.

The two sensitivity rows are nearly anti-parallel along the up inputs (±10.46 against ∓21.07). So the Weber direction
cancels in **m_e m_μ/m_τ²**, which is sharp. C predicts it at **0.66 × data**.

The exact nonlinear posterior follows branch C by homotopy, with a 5% theory error per lepton ratio:
* **With the comparator errors:** χ² = 2.8 for 2 constraints, and the Weber invariant is pulled −4 ± 5%.
* **With lattice-precision quark ratios** (m_s/m_b 1%, m_d/m_s 4%, m_u/m_c 5%, m_c/m_t 2%): **χ² = 10.8, which is
  2.8σ**.
* **With a 10% theory error:** C is consistent.

## Corrections made along the way

1. **"Within 2.4%" was not significant.** The first look at branch C ("m_μ/m_τ within 2.4%, parameter-free") meant
   nothing. Propagated through the quark errors by a homotopy-tracked Monte Carlo, C's prediction spans more than a
   decade. Only the combination m_e m_μ/m_τ² is sharp.
2. **"Unique up to symmetry" was false.** Narrow starts suggested a unique solution; broad starts found at least seven
   branches.

## Reading

**What holds.** The geometric row is sufficient for the quark sector. Two CP-locus homes plus one theta-vector row give
all eight quark data, with CP violation in one Wilson-line phase. But this is a fit (8 parameters for 8 data), not a
prediction.

**Where it becomes predictive, and fails.** With the 12007 shared SU(5) matching it predicts the charged leptons:
* every branch found is excluded, except C;
* C is in 1.7–2.8σ tension through m_e m_μ/m_τ².

The determinant identity explains why no choice of row escapes the tension.

**What would decide it.** The open item is now concrete: the common-scale running of m_e m_μ/m_τ² relative to the down
ratios (compare Codex 12011). A ≈10% net running correction would make branch C consistent. A small one would exclude
it, and with it the geometric row under the shared matching.

## What is not new

* Nelson–Barr (Nelson 1984; Barr 1984).
* Single-vectorlike Nelson–Barr flavour (Cherchiglia–De Conto–Nishi, arXiv:2103.04798).
* Modular Nelson–Barr (arXiv:2505.20395).
* Theta-function Yukawas on magnetized tori (Cremades–Ibáñez–Marchesano 2004).
* The row (12005), the shared matching (12007), the homes and z_e = 6z_d (11942), the Weber invariant (11938).

What is new:
* the theta-vector row and its square system;
* the one-phase CP statement;
* the row-independent determinant identity, used as a test;
* the branch-by-branch lepton verdict.

## Scope

* **Model.** The 11942 homes, one heavy row, and the 12005/12007 matching.
* **Comparators.** The supplied M_Z values, with no running.
* **Search.** The catalogue is search-based (at least seven branches).
* **Statistics.** Sensitivities are linear, except the exact posterior on C.
