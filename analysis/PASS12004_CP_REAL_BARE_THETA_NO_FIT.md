# Pass 12004: the bare CP-real theta quark sector cannot fit — the vectorlike row is necessary

Producer: `analysis/w33_pass12004_cp_real_bare_theta_no_fit.py`
Certificate: `data/w33_pass12004_cp_real_bare_theta_no_fit.json`
Regression: `tests/test_w33_pass12004.py`
Track: Claude. Reservation `e1698064a`. Complements Codex Pass 12005, which shows that one complex vectorlike down row
**suffices**. This pass shows the row is **necessary** within the theta quark model of Pass 11942.

## Setting

* **Up home.** [[τ, ε_u], [ε_u, τ]], Wilson-free.
* **Down home.** [[τ, ε_d], [ε_d, τ_d]]. It shares τ, the quark-doublet torus, and carries a Wilson line z_d on the 5̄
  factor only.
* **Generalized CP.** The theta-group generalized CP is (Ω, z) → (−Ω̄ + 2B, −z̄ + k/3), with B integer diagonal.

## Results

**1. The CP-fixed locus (certified).**
* **Fixed set.** Re τ, Re τ_d ∈ ℤ; Re ε = 0; Re z_d ∈ ℤ/6.
* **Identity on the locus.** Y = Ph ∘ Ȳ exactly (termwise), with Ph[a,c] = exp(2πi(b₁a² + b₂c² + kc)/3).
* **Common left factor.** It is the same, e^{2πi a²/3}, for up and down. Both Yukawas are therefore real in one common
  left basis, and J ≡ 0.
* **Checks.** 120 random locus points satisfy the identity to 5·10⁻¹¹; an off-locus control fails at 10⁻².

**2. The up sector fits exactly on the locus.** τ = 1 + 0.8745i and ε_u = 0.00552i reproduce m_c/m_t and m_u/m_c. This
is the Weber point of Pass 11938, sitting on the T²-CP line Re τ = 1.

**3. Positive control.** At that τ, an unrestricted *complex* down sector fits all five down observables exactly
(χ² ≈ 10⁻¹⁶): m_s/m_b, m_d/m_s, |V_us|, |V_cb| and |V_ub|.

**4. The bare CP-real down sector at that τ does not fit** (frozen search record).
* **Grid.** 746,496 points: 24 discrete classes × 36 × 24 × 36.
  * Im τ_d ∈ [10⁻⁴, 10];
  * ε_d as a fraction of the positivity bound;
  * Im z_d/Im τ_d ∈ [−60, 60].
* **Evaluator.** A centred-window theta that stays accurate in the cusp. It agrees with the N = 40 reference to
  2·10⁻¹³ wherever both are valid.
* **Polish.** Each class is polished from its 20 best grid points.
* **Result.** The global minimum is **χ² = 329** for 5 observables and 3 parameters. At the optimum
  m_s/m_b = 0.064 against 0.0185, and |V_ub| = 0.0025 against 0.0038.
* **Cross-check.** The Codex 12005 bare point (B = 0) lies in the same class and scores χ² ≈ 2.5·10⁵.

**5. Letting τ move.** Sacrificing the up sector, the best compromise found by seeded multistart is χ² = 213, with m_u/m_c
off by a factor of 13. The obstruction is the CP-reality of the down sector, not the shared torus.

## Two corrections made along the way (recorded)

* **A shared basin, not robustness.** An early multistart reported χ² = 213 "robustly" from two seeds. Both seeds drew
  starts from the same biased distribution, and the known exact up solution showed they were trapped. Fix: seed with
  the exact sub-solution, and grid instead of multistarting.
* **A truncation artefact.** An N = 40 grid found χ² = 257 deep in the cusp (Im τ_d ≈ 0.0085, Im z/Im τ_d ≈ 20). That
  value was a truncation artefact: the accurate evaluator gives 357. It is discarded. Every deep-cusp value here uses the
  centred evaluator.

## Reading

**Necessity and sufficiency.** Within this model, exact theta-group CP forbids a bare fit, and Pass 12005 shows one
complex vectorlike down row suffices. So the row is **necessary and sufficient**.
* **Where CP violation comes from.** It must be spontaneous and transmitted by vectorlike mixing: the theta flavour chain
  with exact CP is a Nelson–Barr theory.
* **θ̄.** Tree-level θ̄ ∈ {0, π}, because the bare determinants are real in the common CP frame. The branch is not fixed by
  the CP involution.

**Why the CP locus is natural.** Any CP-invariant moduli potential is stationary transverse to the CP locus (symmetric
criticality, Palais 1979).
* **Checked.** For a sample CP-invariant flavour potential, every real-part gradient vanishes to 5·10⁻⁹, against
  longitudinal gradients of O(65).
* **Consequence.** The CP locus is a natural place for the moduli, not a tuned one. Whether it is a minimum is not
  addressed.

**What is not new.**
* The fixed-set lemma for anti-symplectic involutions (Pass 11210; paper Prop. 3.2).
* "Siegel generalized CP = the antiunitary PGSp(4,3) coset" (paper Thm 9.8).
* The generic Nelson–Barr mechanism (Nelson 1984; Barr 1984; Bento–Branco–Parada 1991; arXiv:2505.20395).
* Generalized CP in Sp(4,ℤ) (Ding–Feruglio–Liu, arXiv:2010.07952).

What is new is the necessity statement for this chain.

## Scope

* **CP type.** T²-type generalized CP, i.e. the "integer real part" CP locus of Pass 11878. S-type CP on |τ| = 1 is not
  covered.
* **Model.** The down Wilson line is on the 5̄ factor only (the Pass 11942 model). M_Z-scale comparators.
* **Status.** A search-based no-fit (dense grid plus polishing), not a proof.
* **Not tested.** The Codex common-scale branch (12011–12015) uses running inputs. Its bare limit is not tested here.

Search drivers and run records: `analysis/search_drivers_12004/` (README maps each script; `deep.py validate` checks the centred evaluator).
