# Pass 11916: dual det-3 fluxes force a massless family — the entangling-compatible SU(5) assignment gives m_d = m_e = 0

Producer: `analysis/w33_pass11916_dual_flux_massless_first_generation.py`
Certificate: `data/w33_pass11916_dual_flux_massless_first_generation.json`
Regression: `tests/test_w33_pass11916.py`
Track: Claude.

## 1. Compatibility forces the Eisenstein dual pair

A magnetized flux N on T⁴ is (1,1) for the period matrix Ω exactly when NΩ is symmetric.

**When the entangling modulus is on.** Suppose Ω₁₂ ≠ 0 and Ω₁₁ = Ω₂₂ (the latter is required by the A₂/Eisenstein 10
flux). A det-3 form [[p,q],[q,r]] is compatible only if p = r, so p² − q² = 3. That leaves only
**A₂ = [[2,1],[1,2]] and A₂′ = [[2,−1],[−1,2]]**.

**The SU(5) assignment.** In SU(5) the up Yukawa is 10·10 and the down and lepton Yukawas are 10·5̄. To have I_up ≠ I_down,
the assignment is forced:
* the 10 and the 5̄ carry fluxes (A₂, A₂′);
* up = A₂ ⊗ A₂;
* down and leptons = A₂ ⊗ A₂′.

## 2. Dual fluxes have a scalar Higgs flux

A₂′ = 3A₂⁻¹ = adj(A₂). Every det-3 form satisfies N + 3N⁻¹ = (tr N)·1 (Cayley–Hamilton, checked to 10⁻¹⁵). So a dual
pair has a **scalar** Higgs flux. Among the det-3 forms with entries ≤ 4 there are six dual pairs, with Higgs fluxes 4·1,
5·1 or 7·1.

## 3. Theorem (numerical)

For every dual pair, every single-Higgs-mode Yukawa matrix is **singular**: its rank is exactly 2.

| test | max s₃/s₁ over Higgs modes |
|---|---|
| A₂ ⊗ A₂′, Ω = it[[1,β],[β,1]] with (t, β) = (1.5, 0), (2, 0.4), (3, −0.2), with and without random Wilson lines | ≤ 2·10⁻¹⁵ |
| all six dual pairs, scalar Ω, random Wilson lines | ≤ 10⁻¹⁴ |
| controls A₂ ⊗ A₂ (up) and A₂ ⊗ rect (Pass 11915) | full rank (min s₃/s₁ ≫ 10⁻⁶) |

Eight further, non-dual pairs are also singular. All of them have Higgs fluxes that are scalar-equivalent or doubled.

**Partial explanation.** A dual pair is related by the 90° lattice rotation R, since adj(N) = RᵀNR. But R is not a
symmetry once β ≠ 0 or Wilson lines are switched on, and the zero persists anyway. A full proof is open.

## Physical reading

**Massless first generation at tree level.** In the entangling-compatible SU(5) assignment, the 10·5̄ Yukawas have an
**exactly massless down quark and electron** for any localised Higgs, any modulus and any Wilson line. The up sector
(A₂ ⊗ A₂) is full rank.

**Where the masses must come from.** The first-generation down and electron masses must come from a superposition of
Higgs modes. Such a superposition is radiatively allowed here: det 16 is coprime to 3, so the ℤ₃ class selection of
Pass 11914 does not apply.

**What this suggests.** The data have m_d/m_s ≈ 0.05 and m_e/m_μ ≈ 0.005. The structure points to these being
perturbative effects on a texture whose leading order is singular. It does not yet predict their size.

## Recorded (frozen)

* The up slope varies continuously with the entangling parameter β, where Ω = it[[1,β],[β,1]]: s/π = −8/3, −2.34, −2,
  −4/3 at β = 0, 1/4, 1/2, −1/2.
* Lifting the zero with a Higgs admixture does **not** produce the Gatto–Sartori–Tonin relation. Over 362 hierarchical
  samples, corr(log V_us, log √(m_d/m_s)) = 0.06, and the median of V_us/√(m_d/m_s) is 14.

## Prior art

* Cremades–Ibáñez–Marchesano; Antoniadis–Kumar–Maillard: the (1,1) condition for magnetized T⁴.
* Gauss: reduced binary forms of determinant 3, and adjugate forms.
* Corpus: 11912, 11914, 11915.
