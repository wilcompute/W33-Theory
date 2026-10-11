# Pass 11915: SU(5)-structured det-3 matrix fluxes on T⁴ — what the two W(3,3) theta systems do for flavour

Producer: `analysis/w33_pass11915_su5_matrix_fluxes_on_t4.py`
Certificate: `data/w33_pass11915_su5_matrix_fluxes_on_t4.json`
Frozen inputs:
* `data/w33_pass11915_slope_scan_frozen.json` (all twelve det-3 forms with entries ≤ 4);
* `data/w33_pass11915_ckm_wilson_sample_frozen.json` (40 random Wilson-line samples).

Regression: `tests/test_w33_pass11915.py`
Track: Claude.

## Idea selection

The candidates were brainstormed, ranked by how deep the W(3,3) connection is, whether they give a parameter-light
prediction, and how directly they address the open failures of Passes 11910–11914:

1. **(pursued here)** SU(5)-structured fluxes in the two det-3 classes. The up Yukawa is 10·10; the down and lepton
   Yukawas are both 10·5̄.
2. **(found in pursuing 1)** The two classes of positive binary forms with determinant 3 are A₂ = [[2,1],[1,2]] and
   x² + 3y² = diag(1,3). They are the corpus's two theta systems: Eisenstein/Hermitian (11897) and level-3 √3ℤ (11869).
3. **(partly covered by 1)** The Yukawa matrix as a two-qutrit state. Masses are its Schmidt coefficients, and the
   entangling modulus Ω₁₂ controls the hierarchy.
4. **(not tested)** A geometric Schmidt hierarchy (1, ε, ε²), which would predict m_u/m_c ~ m_c/m_t.
5. **(quick test: side result 4 below)** Within-class Higgs admixture as the up/down lever.
6. **(deferred: 2nd tier)** Families as eigenspaces of an order-3 Clifford roto-translation, giving Fourier-mixed families
   and CKM.
7. **(deferred: 2nd tier)** A T⁴/ℤ₃ (K3) flux ansatz with fewer moduli, within a K3×K3 tadpole budget of 24.
8. **(not pursued: low tier)** The odd Weil-4 sector as a stable W(3,3)-parity sector, i.e. a dark-matter candidate.
9. **(not pursued: low tier)** Spontaneous CP from Re Ω₁₂, and θ̄.
10. **(not pursued: low tier)** The spread Higgs phase as the origin of lepton mixing.
11. **(rejected)** Koide's relation from level-3 Fourier structure: the texture has no extra relation.
12. **(not pursued: low tier)** Magnetic-translation ℤ₃ as baryon or family number.
13. **(not pursued: low tier)** The top Yukawa from theta normalisation.
14. **(not pursued: low tier)** Hierarchies from Siegel cusps.

## Construction (verified)

**Zero modes.** ψ^{j,N}(z) ∝ e^{iπ(Nz)·(Im Ω)⁻¹·Im z}·ϑ[j,0](Nz, NΩ), with j ∈ N⁻¹ℤ²/ℤ², on T⁴ with Ω = it·1. Both classes
are (1,1) for a scalar Ω.

**Checks.**
* |ψ|² is periodic to 10⁻¹⁴.
* There are det N orthonormal modes.
* The Higgs fluxes 2N₁₀ = [[4,2],[2,4]] and N₁₀ + N₅ = [[3,1],[1,5]] carry 12 and 14 modes.

**Yukawas.** Computed as direct 4D overlap integrals.

## Results

1. **The down/lepton relation is automatic.** In SU(5), down and lepton Yukawas are both 10·5̄, so I_down = I_lepton.
   The data agree to 17 % (Pass 11910).
2. **Gaussian slopes are quantised.** ln I = s·t + c with:

   | Yukawa type | s/π |
   |---|---|
   | rect ⊗ rect | −4/3 |
   | A₂ ⊗ A₂ | −8/3 (dominant Higgs modes) or −2/3 |
   | A₂ ⊗ (rect class) | −2, −1 or −4, depending on relative orientation |

   * The attainable up/down log-ratios are {1/6, 1/4, 1/3, 1/2, 2/3, 1, 4/3, 2, 8/3, 4}. The observed 1.605 ± 0.03 is
     **not attainable**; the nearest value is 4/3.
   * Fitting the down invariant then puts the up invariant off by a factor of about 180 (with slope −2) or about 10⁴
     (with slope −1).
   * **With a scalar Ω, SU(5) det-3 fluxes cannot produce the up/down ratio.** A non-scalar Ω, i.e. the entangling
     modulus, is required.
3. **The class selection is broken geometrically.**
   * The up Higgs lattice (det 12) keeps the ℤ₃ one-entry-per-row selection.
   * The down Higgs lattice (det 14, coprime to 3) does not: all 14 down Yukawa matrices are full.
   * So the CKM is **nonzero without any cross-class Higgs admixture**. This removes Pass 11914's obstruction in
     principle.
4. **Generic Wilson lines do not give a realistic CKM.** 40 random samples at t = 1.8 (A₂/rect):
   * the CKM is mostly tiny (median V_us 0.011, V_cb 1.1·10⁻⁴) or misordered by a permutation;
   * none has a CKM-like hierarchical pattern;
   * the down masses are realistic-ish (median m_s/m_b 0.010, m_d/m_s 0.12);
   * the up light pair is under-split (median m_u/m_c 0.55).
5. **Side result (idea 5).** A within-class Higgs admixture, which radiative corrections allow, moves the Gaussian
   invariant strongly: ε = 0.01 multiplies it by about 8. The up/down ratio could therefore come from the Higgs profile,
   but at the price of a free parameter.

## Reading

The top idea gives two structural successes:
* down = lepton is automatic;
* the class selection is broken by the geometry itself, so mixing appears.

It also gives two quantitative failures:
* the slopes are quantised and do not include 1.605;
* generic Wilson lines give too little mixing.

The open problem is therefore narrowed to the non-scalar Siegel modulus (Ω₁₂) and the Wilson-line vacuum. These are the
same two moduli that carry the hierarchy (Passes 11907, 11912) and that fluxes failed to fix (Pass 11913).

## Prior art

* Cremades–Ibáñez–Marchesano: magnetized T^{2n} and non-factorizable fluxes.
* Antoniadis–Kumar–Maillard: magnetized T⁴ conditions.
* Kikuchi–Kobayashi–Nasu–Takada–Uchida: Siegel-modular magnetized T⁴.
* Gauss: reduced binary forms of determinant 3.
* Corpus: 11869, 11897, 11904–11914; TOE46–TOE49.
