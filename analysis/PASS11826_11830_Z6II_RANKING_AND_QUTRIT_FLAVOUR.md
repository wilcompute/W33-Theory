# Passes 11826–11830 — the Z6-II W(3,3) SU(9) Standard Models ranked by their whole Yukawa sector; qutrit flavour in four-dimensional SU(9)

Producer: `analysis/w33_pass11826_11830_z6ii_candidate_and_qutrit_flavour.py`
Frozen: `data/w33_pass11826_11830_z6ii_candidate_and_qutrit_flavour.json`
Regression: `tests/test_w33_pass11826_11830.py`
Input: `data/w33_pass11819_z6ii_probe_fields.json.gz` (Pass 11819: orbifolder field data for the nine Z6-II A8 models
with the SM inside SU(9), plus the Codex benchmark `Z6II_34_SM_1558`).

**Why.** Pass 11818–11822 excluded the Z6-I W(3,3) class (m_t = m_c exactly, no bottom/tau, hidden SU(5) confines far too
low). They left Z6-II, where every plane has a different twist, as the live branch. This packet asks whether any Z6-II
model survives the *whole* Yukawa sector and the most dangerous operators, not just the top.

**Method (necessary rules only).**
* U(1) charges (exact), hidden N-ality, sector, and the Z6-II R rule of arXiv:1301.2322
  (R1 + 6γ ≡ −1 mod 6, R2 ≡ −1 mod 3, R3 ≡ −1 mod 2).
* Insertions are hidden-neutral singlets.
* Minimal singlet degree d_ij of q bu H_u, q bd H_d and l be H_d by exact MILP, for every Higgs pair of the right
  hypercharge.
* Froggatt–Nielsen estimate Y_ij = c_ij ε^{d_ij} with random O(1) complex c_ij, median over samples. It is compared with
  GUT-scale m_c/m_t, m_u/m_t, m_s/m_b, m_d/m_b, m_b/m_t, m_μ/m_τ, m_e/m_τ, |V_us|, |V_cb| and |V_ub|. The score is the sum
  of squared log10 deviations over these ten numbers.

## Results

| model | score | cubic up entries | m_c/m_t | m_s/m_b | m_b/m_t | m_μ/m_τ | V_us | V_cb | μ degree | QLd | udd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Z6II_18_1116 | 9.75 | **0** | 0.0022 | 0.11 | 0.23 | 0.40 | 0.010 | 0.74 | 3 | 3 | 4 |
| Z6II_19_477 | 13.98 | 1 | 0.0018 | 0.016 | 0.019 | 0.084 | 0.004 | 0.70 | 4 | **0** | **0** |
| Z6II_03_435 | 14.08 | 1 | 0.0020 | 0.015 | 1.01 | 0.39 | 1.00 | 0.067 | 3 | **0** | **0** |
| Z6II_18_656 | 14.30 | 1 | 0.0020 | 0.017 | 0.021 | 0.080 | 0.004 | 0.61 | 4 | **0** | 1 |
| Z6II_34_1558 (Codex) | 14.41 | 1 | 0.0002 | 0.36 | 0.19 | 0.35 | 0.16 | 0.11 | 1 | **0** | **0** |
| Z6II_03_1353 | 17.63 | 4 | 0.36 | 0.012 | 0.13 | 0.41 | 0.72 | 0.69 | 4 | 0 | 0 |
| Z6II_43_1867 | 32.08 | 0 | 0.79 | 0.39 | 1.18 | 0.52 | 0.41 | 0.81 | 3 | 0 | 0 |
| Z6II_03_923 | — | 2 | no full-rank down sector | | | | | | 1 | 0 | 2 |
| Z6II_28_2298, Z6II_39_478 | — | — | no Higgs pair with down entries | | | | | | | | |

Observed targets: m_c/m_t ≈ 1/300, m_s/m_b ≈ 0.02, m_b/m_t ≈ 0.012, m_μ/m_τ ≈ 0.06, V_us ≈ 0.227, V_cb ≈ 0.04.

* **11826 (ranking).** No model fits. The best score, 9.75, is still about one decade of error per observable. It belongs
  to a model with **no cubic top**: there the top Yukawa is itself ε-suppressed.
* **11827 (what the textures do well).** Two single-cubic-top models, 19_477 and 18_656, reproduce the charged-fermion
  mass hierarchies to within factors of 2: m_c/m_t ≈ 0.002, m_s/m_b ≈ 0.016, m_b/m_t ≈ 0.02 and m_μ/m_τ ≈ 0.08. The
  third, 03_435, has the same up and down ratios but m_b ≈ m_t. They fail on mixing: V_cb ≈ 0.6–0.7 and V_us ≈ 0.004 are inverted relative to
  nature. The benchmark 1558 has the opposite failure, with good mixing magnitudes and too small a charm mass.
* **11828 (D-flatness).** An FI-cancelling D-flat singlet monomial is found in 6 of the 8 analysable models (Buccella
  criterion; F-flatness not addressed). For 03_435 and 18_656 the MILP returned the empty monomial, so none was found. We
  do not claim a proof of absence.
* **11829 (proton decay — the decisive failure).** In **every** single-cubic-top model, Q L d^c is allowed at degree 0
  (renormalisable), and u^c d^c d^c at degree 0 or 1. The only model with suppressed R-parity violation, 18_1116 (QLd at
  degree 3, udd at degree 4), has no cubic top. Even there ε⁷ ≈ 10⁻⁷ is about 17 orders short of the proton bound
  λ′λ″ ≲ 10⁻²⁴. **A Z6-II A8 model needs an additional matter parity**, which these models' selection rules do not supply.
  This parallels the Z6-I proton story (memory: matter parity needs only the Z2 of B−L, Holotrade 0fee779).
* **11830 (qutrit flavour in a four-dimensional SU(9)).** Under the two-qutrit Pauli group, the 9 and the adjoint 80 have
  **no** invariants, and the 84 has exactly **4**. These four are the Pauli-singlet trivectors, the E8 Cartan of
  Pass 11681, and they are not SU(5)-invariant. So an exact W(3,3) flavour symmetry is incompatible with SU(5) breaking.
  A level-diagonal GUT breaking preserves exactly the Z-type subgroup ⟨Z₁, Z₂⟩ ≅ Z₃×Z₃, which is a W(3,3) line. With the
  family charges equal to the qutrit coordinates of the family levels, that Z₃×Z₃ allows **at most one up-type entry per
  family row**. Over all vacuum and Higgs choices the patterns are:
  * 6 rank-1 (one heavy family);
  * 9 antidiagonal pairs (two degenerate families);
  * 3 permutations (three degenerate families);
  * 6 zero.

  A hierarchy therefore *requires* breaking the line symmetry, by vevs on the flavour levels.

## Scope and boundary

* The ε grid was {0.1, 0.15, 0.2, 0.3}, and every model chose ε = 0.1, the grid edge. The scores are order-of-magnitude
  texture tests, not predictions. They omit CFT coefficients, vector-like mixing and running.
* All operator degrees use necessary selection rules only. A degree-0 entry is *allowed*, not shown to be nonzero; the
  vector-like and identification caveats are those of Holotrade 2fa6596.
* **Verdict: the heterotic Z6-II A8 branch hosts the right quark-mass hierarchy but not the mixing, and it has unsuppressed
  R-parity violation.** It is not a viable Standard Model without a further symmetry. Together with 11818's Z6-I exclusion,
  this closes the W(3,3) T⁶/Z6 SU(9) route at the level of necessary rules. The next lever should not be another orbifold
  scan (see Passes 11831–11833 for the change of direction).

**Prior art.**
* Frampton–Kephart / Chen SU(9) flavour unification (cited in 11818).
* Codex benchmark 1558 (Pass 11797+).
* Holotrade 82f8d66 / 2fa6596 / 0fee779 for the Z6-I class and the matter-parity caveat.
* The Buccella et al. D-flatness criterion.
* Cabo Bizet et al., arXiv:1301.2322, for the R rule.
