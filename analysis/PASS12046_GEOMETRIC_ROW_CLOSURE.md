# Pass 12046: closing the geometric Barr row

* **Producer:** `analysis/w33_pass12046_geometric_row_closure.py` (4/4 checks, about 20 s)
* **Certificate:** `data/w33_pass12046_geometric_row_closure.json`
* **Regression:** `tests/test_w33_pass12046.py`
* **Drivers and records:** `analysis/search_drivers_12046/`
* **Track:** Claude. Reservation `3034198e7`.

Pass 12045 left two continuous handles and one open item:
* **Handle 1:** the CP phase, Re w.
* **Handle 2:** the up modulus τ.
* **Open item:** branch C's 2–3σ lepton tension, to be decided by running.

This pass tries to fix both handles with natural discrete choices, and settles the open item. All three come out
negative, and each negative is informative.

## 1. Pinning the CP phase predicts only sin δ

With |V_us|, |V_cb| and |V_ub| fixed, J = c₁₂s₁₂c₂₃s₂₃c₁₃²s₁₃·sin δ.
* **Bound.** |J| ≤ J_max = 3.44·10⁻⁵, and the data need sin δ = 0.896.
* **What pinning predicts.** Any discrete CP source predicts sin δ and nothing more. That includes a Wilson line pinned
  at an order-3 or order-6 torsion point:
  * these are the quantised Wilson lines of ℤ₃/ℤ₆ orbifolds;
  * their phases are the "calculable phases" of geometrical CP violation.
* **Weak test.** A random δ lands within 4% of the data about 10% of the time.
* **Continuation record.** Pseudo-arclength continuation of branch A along the five CP-even targets traces J over
  [9·10⁻⁶, J_max], while Re w stays within [−0.078, −0.049]. No torsion value is reached on the traced arc.
* **Note on method.** Plain continuation in Re w fails at once: the curve folds in Re w, so arclength is needed.

## 2. The CM points do not miss the Weber invariant (a correction)

Pass 11938 tested only the **elliptic** CM points, which all give W = m_u m_t/m_c² ≥ 1. The paper then wrote that the
measured value is "missed by the CM points". That is an over-read.

On the CP line Re τ = 1, τ = 1 + iy is CM exactly when y² is rational, so CM points are dense there. Fitting ε_u to
m_c/m_t at each one, with W = 0.534 ± 3.3% at M_Z (lattice m_u/m_c):

| D | y² | W | pull at M_Z |
|---|---|---|---|
| −24 | 2/3 | 0.381 | −10.1 |
| **−48** (τ = 1 + i√3/2, Eisenstein field) | 3/4 | **0.513** | **−1.2** |
| −140 | 5/7 | 0.455 | −4.8 |
| −252 | 7/9 | 0.561 | +1.5 |
| −80 | 4/5 | 0.600 | +3.5 |

**Running.** W runs by +13% from M_Z to 2·10¹⁶ GeV (SM one loop, using Codex 12011's running), and other CM points
match at higher scales. Identifying the up modulus with a CM point would need the matching scale, so it is **not a
prediction**. The paper sentence is corrected accordingly.

## 3. Running does not rescue the leptons

Each catalogued branch (A, B, C, D, G) was followed in the matching scale:
* **Running:** Codex 12011's three-generation SM one-loop running of the full Yukawa matrices;
* **Re-solve:** at each of 8 scales from M_Z to 2·10¹⁶ GeV, the up home and the six row parameters are re-solved
  against the running quark targets.

Two lepton rules were tried, both with no new parameters:
* **(a)** the 12007 shared SU(5) matching;
* **(b)** a colour-triplet-only heavy state (bare theta leptons; the E6 exotic-D option).

**Outcome.** No branch comes close at any scale under either rule; at every point some ratio is off by more than 43%,
usually by factors.
* **Best case.** Branch C at M_Z under (a).
* **Branch C under running.** Its sharp combination m_e m_μ/m_τ² stays at 0.52–0.72 × data, while m_μ/m_τ rises to
  0.27 against 0.059.
* **Rule (b).** It is worse everywhere: for example, C's bare m_e/m_μ is 0.199.
* **Lepton ratios.** These do not run at one loop in the SM, so the comparison scale does not matter for them.

**A correction to my own estimate.** I first estimated that the y_t-driven running of m_s/m_b (+13%) would supply most
of the missing factor 1.5. The full running does not do that, because the CKM elements and the Weber invariant run at
the same time.

## Reading

**The quark sector.** The theta-vector Barr row completes it: CP violation sits in one Wilson-line phase, and the 8
quark data are fitted by 8 geometric parameters.

**The charged leptons.** The row cannot also produce them, at any matching scale, with or without the shared SU(5)
matching. The lepton sector needs structure the row does not carry, for example:
* a separate heavy lepton row;
* a different flux for the lepton partner;
* non-minimal Clebsches.

**What this closes.** The hope that one geometric object fixes both quarks and leptons in the 11942/12005 architecture.

## Scope

* **Branches.** Only the catalogued branches; the catalogue is search-based.
* **Running.** One-loop SM running without thresholds.
* **Model.** The 11942 homes.

## What is not new

* Geometrical CP violation (Branco–Gérard–Grimus 1984; de Medeiros Varzielas et al.).
* Quantised orbifold Wilson lines (Ibáñez–Nilles–Quevedo 1987).
* The running (Codex 12011).
* The Weber law (11938).
