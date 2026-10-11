# Pass 11917: proof of the dual-pair singularity — the down Yukawa is a level-3 theta two-qutrit state in a frame fixed by the flux

Producer: `analysis/w33_pass11917_dual_pair_singularity_proof.py`
Certificate: `data/w33_pass11917_dual_pair_singularity_proof.json`
Regression: `tests/test_w33_pass11917.py`
Track: Claude. Proves Pass 11916, and joins it to Pass 11872 (product state ⟺ factorised torus).

## 1. Exact formula

**Setup.**
* The 10 carries flux N₁.
* The 5̄ carries N₂ = 3N₁⁻¹.
* The Higgs carries N₁ + N₂ = m·1.
* Ω is compatible, so it commutes with N₁ and N₂.

**Change of variables.** Put x₁ = y + (N₂/m)u and x₂ = y − (N₁/m)u. Because N₁m⁻¹N₂ = (3/m)·1 is a **scalar**,

  x₁N₁Ωx₁ + x₂N₂Ωx₂ = m yΩy + (3/m) uΩu.

**The Yukawa.** It is the coefficient of ψ^m_c in ψ^{N₁}_a ψ^{N₂}_b:

  **Y^c_{ab} = Σ_{k ∈ ℤ², N₂k ≡ a+b−c (mod m)} exp(iπ(3/m) uᵀΩu),  u = k + (N₂a − N₁b)/3.**

**Check.** The formula matches the 4D overlap integrals: the ratio is constant to 10⁻⁹. The entries where the formula
vanishes are ≤ 10⁻⁸ numerically. This was tested on A₂ ⊗ A₂′ at an entangled Ω and on (1,1,4) at a non-scalar Ω.

**Wilson lines.** They add only a linear phase 2πi(3/m)u·(ζ_Q − ζ_R), plus the Higgs's own shift.

## 2. Reduction mod 3

**gcd(m, 3) = 1 for every det-3 form.** If a + c ≡ 0 mod 3, then a ≡ b ≡ 0 mod 3, so 9 | ac − b². Checked on 64
forms.

**Splitting the characteristic.** By CRT the characteristic of Y^c_{ab} splits into two parts:
* the mod-m part is −N₁c, which is independent of a and b;
* the mod-3 part is N₂a − N₁b.

**Two frames only.** Mod 3 both fluxes have rank 1: N₁ ≡ λvvᵀ and N₂ ≡ μwwᵀ, with v·w ≡ 0 because N₁N₂ = 3. Since
x² + y² is **anisotropic over F₃**, there are exactly two orthogonal pairs of lines:
* the **axes** {(1,0),(0,1)};
* the **diagonals** {(1,1),(1,−1)}.

**The Yukawa as a two-qutrit state.** Y^c is the 3×3 coefficient matrix of the level-3 theta vector

  f_c(q mod 3) = Σ_{q′ ≡ q} g_c(q′),  with g_c Gaussian in the metric (m/3)Ω,

taken in the tensor split F₃² = ⟨v⟩ ⊕ ⟨w⟩. **The flux chooses the tensor factorisation.** det Y^c is that
factorisation's determinant (Pass 11659: nodes = determinants).

## 3. Theorem

**Statement.** Suppose Ω is diagonal in the integral lift of the frame. The lift has index 1 for the axes and index 2
for the diagonals, both coprime to 3. Then g_c factorises on each coset, so

  **rank Y^c ≤ 1 (axes), ≤ 2 (diagonals)** for every Higgs mode and every Wilson line.

**Relation to 11872.**
* For the axes this is exactly 11872: rank 1 ⟺ factorised torus.
* For the diagonals the torus is 2-isogenous to E₊ × E₋. Pulled back, the fluxes become (6,2), (2,6) and (8,8). The two
  cosets of the isogeny supply **exactly one** extra Schmidt rank.

**Numerical check** (scalar Ω, random Wilson lines):

| pair | frame | max s₂/s₁ | max s₃/s₁ |
|---|---|---|---|
| x²+3y² = diag(1,3) | axes | 1·10⁻¹⁵ | 7·10⁻¹⁷ |
| (3,±3,4) | axes | 2·10⁻¹³ | 7·10⁻¹⁵ |
| A₂, (1,±1,4) | diagonals | 0.76 – 0.96 | ≤ 4·10⁻¹⁴ |

**Correction to Pass 11916.** The three axis-frame dual pairs have rank **1**, not 2.

## 4. Which pairs are forced, and the tree-level lift

**When the zero is forced.** A compatible Ω is a polynomial in N₁, so the zero is forced for all moduli exactly when
the eigenframe of N₁ is its own mod-3 frame.
* **A₂** has eigenvectors (1,±1), which are its diagonals.
* **x² + 3y²** is diagonal, so its eigenframe is the axes.
* For these two pairs m_d = m_e = 0 for every compatible modulus. Checked: max s₃/s₁ ≤ 2·10⁻¹⁵ at Ω = i(1.2 + 0.05N₁).
* Since 11916's entangling-compatibility argument forces A₂, this is why the zero survived every modulus there.

**When it lifts.** The four pairs (1,±1,4) and (3,±3,4) have **irrational** eigenframes. A non-scalar compatible
modulus Ω = i(t + yN₁) un-factorises the frame, and the zero lifts at tree level.
* At y = 0.05, max s₃/s₁ = 4.8·10⁻⁴ for (1,±1,4) and 4.5·10⁻⁹ for (3,±3,4). The latter is Gaussian-suppressed but
  grid-stable: identical at G = 12 and 16.
* **The lift is linear:** for (1,1,4) the median s₃/s₂ is 6.4·10⁻⁷, 2.1·10⁻⁶, 6.0·10⁻⁶ at y = 3·10⁻⁴, 10⁻³,
  3·10⁻³, a log-slope of 0.975.

## Physical reading

**The first-generation down/electron mass in these models is a frame misalignment.** It measures how far the modulus's
eigenframe is from the flux's mod-3 frame:
* it vanishes identically for the two "W(3,3)" theta systems A₂ and x² + 3y² of Pass 11915;
* it is first order in the misalignment for the irrational-frame pairs.

**What this does not do.** It does not fix the size: the coefficient is small (s₃/s₂ ≈ 2·10⁻³·y here). Nor does it
give the CKM.

## Prior art

* Cremades–Ibáñez–Marchesano; Antoniadis–Kumar–Maillard; Antoniadis–Kumar–Panda: product formulas for magnetized
  theta functions.
* Gauss: forms of determinant 3.
* Corpus:
  * 11872, product ⟺ factorised torus. Cited; this pass is its Yukawa-side generalisation with a flux-chosen frame.
  * 11659, nodes = determinants.
  * 11915, 11916.
