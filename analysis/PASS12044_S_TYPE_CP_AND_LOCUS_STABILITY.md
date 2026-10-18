# Pass 12044: S-type CP also forbids a bare fit, and the CP locus is a saddle of the toy one-loop potential

* **Producer:** `analysis/w33_pass12044_s_type_cp_and_locus_stability.py` (13/13 checks)
* **Certificate:** `data/w33_pass12044_s_type_cp_and_locus_stability.json`
* **Regression:** `tests/test_w33_pass12044.py`
* **Search drivers and run records:** `analysis/search_drivers_12044/`
* **Track:** Claude. Reservation `a7b08f8c1`.

This pass completes Pass 12004 in two directions. Its Scope line said "S-type CP on |τ| = 1 is not covered" and
"whether [the CP locus] is a minimum is not addressed". Both are now covered.

## Part A: S-type generalised CP

**The CP elements.** CP∘g with g = S × h. S acts on the shared doublet torus, and h ∈ {S, T^{2b}} acts on the second
factor of each home. CP sends (Ω, z) to

  (−conj((AΩ+B)(CΩ+D)⁻¹), −conj((CΩ+D)⁻ᵀ z) + (0, k/3)).

**A1. J vanishes identically.** S acts on the level-3 theta as the discrete Fourier transform, up to a scalar:
* F ⊗ F for S × S;
* F ⊗ 1 for S × 1.

This is checked to 10⁻¹⁵. The left factor F is common to the up and down sectors, so J ≡ 0 on every S-type fixed set.
* **With Wilson lines.** Checked on S × T⁰ fixed points. Shifting Re z_d off the fixed set restores J ≠ 0.
* **Why the Wilson lines matter.** With z = 0 every theta Yukawa is parity-blocked (TOE39), so J = 0 trivially. The
  first control here was vacuous for exactly that reason, and was replaced.

**A2. The up sector fits exactly on the S arc.**
* **Fixed set.** On the CP∘(S × S) fixed set the up home is unitary-symmetric: Ω conj(Ω) = 1. Equivalently
  |τ|² + |ε_u|² = 1, with ε_u ⊥ τ.
* **Fit.** The up sector fits exactly at τ = ±0.67622 + 0.73669i, |ε_u| = 0.00459. This is the S-arc image of the
  Weber point.
* **Positive control.** At that τ a complex down home fits all five down observables exactly.

**A3. Every branch closes. Four of the five do so exactly.**

| up home | down home | why it fails |
|---|---|---|
| S × S | S × T^{2b} | The down home forces \|τ\| = 1. The up home has \|τ\|² = 1 − \|ε_u\|². So ε_u = 0, which is rank one (Pass 11872). |
| S × S | S × S | S × S moves the 5̄ Wilson line into the doublet factor. A real CP needs that component to vanish, so ε_d z_d = 0. This leaves either a rank-one down Yukawa or no Wilson line. With no Wilson line both Yukawas are parity-symmetric, so the CKM has a decoupled generation: one entry of modulus 1 and four zeros (TOE39; checked with the full theta to 2·10⁻¹⁶). |
| S × T^{2b}, b ≠ 0 | any | The smaller eigenvalue of Im Ω_u is cos(θ/2)(2 sin(θ/2) − ρ), and (2 sin(θ/2))² − ρ² = 2(1+b). For b ≥ 1 the home is empty, for b = −1 degenerate, for b ≤ −2 indefinite. |
| S × T⁰ | any | One parameter for two up observables. min χ²_up = **94.6**, with m_u/m_c = 0.0131 against 0.0020. This is the one search-based entry: a 6,001-point scan; the evaluator is accurate to 5·10⁻⁷ on this curve. |

**Why the doublet component must vanish exactly.** A Z/3 shift of the doublet-factor Wilson line is a left phase on
Q. The up sector does not share that phase. Admitting the shift gives J = −3.4·10⁻⁴, which shows it is not a symmetry.

**Reading.** Under exact theta-group CP, the bare quark sector cannot fit on either family of CP-fixed loci:
* the T² lines (Pass 12004);
* the S arc (here).

The Barr row of Pass 12005 is therefore necessary on both.

### Corrections made along the way (recorded)

1. **Penalty fit.** A penalty fit never reached the fixed set, and returned "no result" on every branch. The sets are
   reachable (projection residual 10⁻¹⁶); the penalty method was at fault.
2. **Joint multistart.** A joint constrained multistart over 27 branches reported χ² ≥ 9339. It failed its own
   complex-down control (χ² = 1230 where 0 is attainable), so it is **not used**.
3. **Truncation artefacts.** A scan of the Wilson-free S × S down home found "minima" deep in its cusp: first 1.04·10⁴,
   then 3432 at finer resolution.
   * **Cause.** The centred-window theta follows v₂ only, while the soft direction of Im Ω_d is rotated there. The
     parity residual of the computed Yukawa was 0.41 where it is exactly 0.
   * **Resolution.** The values are discarded, and the exact parity argument replaces the scan.
   * **Lesson.** For a z = 0 theta, the parity residual is a free accuracy test.

## Part B: is the CP locus a minimum?

**The potential.** This uses the toy Coleman–Weinberg potential of Codex Pass 12034, with its counterterm family
c Σ N_c Tr Y†Y. The transverse (CP-odd) directions are the real parts of the ten theta moduli.

**B1. The locus is stationary.** Transverse gradients are ≤ 10⁻¹⁰, against longitudinal gradients of 6·10⁻⁴ to 2. This
is symmetric criticality (Palais 1979), as 12004 stated.

**B2. At the 12005 Nelson–Barr vacuum the locus is a saddle.**
* **Negative mode.** The transverse Hessian has a negative eigenvalue for every s ∈ {0.1, 1, 10} and Q ∈ {0.5, 1, 2}.
* **No counterterm cures it.** The best minimum eigenvalue over c ranges from −0.011 to −0.12.
* **Mechanism.** The counterterm Hessian is itself indefinite there, with eigenvalues (−2951, −18, +1.9, +3.3, +8.4).
  So no coefficient c can remove the negative mode.

**B3. Control.** At a generic locus point the same counterterm does make the transverse Hessian positive (minimum
eigenvalue 1.2·10⁴ at c = 10⁴). The saddle is therefore a property of the vacuum, not of the method.

**Together with 12034.** Codex 12034 shows the longitudinal failure: the fitted point is not stationary along its six
shape directions (residual force 4.5·10⁻⁵ after the counterterm). This pass adds the transverse failure:
* **Transverse:** a saddle.
* **Longitudinal:** a force.

So the toy potential holds the Nelson–Barr vacuum in neither direction. In this model, spontaneous CP violation would
also run away radiatively. Stabilising the moduli, transverse directions included, is a UV problem.

## What is not new

* Generalised CP in Sp(4, ℤ) (Ding–Feruglio–Liu, arXiv:2010.07952).
* The |τ| = 1 CP-fixed arc of modular CP (Novichkov–Penedo–Petcov–Titov, arXiv:1905.11970).
* Symmetric criticality (Palais 1979).
* The parity-block theorem (TOE39).
* The 12034 potential and its counterterm (Codex).

What is new:
* the closure of the S-type branches for this quark model;
* the transverse saddle at the 12005 vacuum, with its counterterm-indefiniteness mechanism.

## Scope

* **CP elements.** Only the product elements S × {S, T^{2b}}, with S on the shared torus. Non-product elements of
  Sp(4, ℤ) mixing the two factors are not covered.
* **Model.** The 11942 down model.
* **Part A.** Exact except the S × T⁰ up scan.
* **Part B.** A toy one-loop potential with one counterterm family, evaluated at the 12005 theta moduli. The Barr row is
  not included in V, and this is not the MSSM field-dependent spectrum.
