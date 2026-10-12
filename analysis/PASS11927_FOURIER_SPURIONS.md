# Pass 11927: background Fourier modes of the torus are two-qutrit Paulis — the local-adjoint flavour spurions

Producer: `analysis/w33_pass11927_fourier_spurions.py`
Certificate: `data/w33_pass11927_fourier_spurions.json`
Regression: `tests/test_w33_pass11927.py`
Track: Claude.

**What it answers.** The parallel packet 34e149d79 (target 4) found that CKM and PMNS move independently only under local
adjoint spurions (8,1) ⊕ (1,8). It left their geometric origin open as "a representation target for the compactification
/ spurion sector".

## Setting

* Magnetized SU(5) on T⁴ with a det-3 dual pair (N₁₀, N₅ = 3N₁₀⁻¹).
* The flux factorises A[3] = K(L₁₀) ⊥ K(L₅) (Pass 11921): the 10 is flavour qutrit 1 and the 5̄ is flavour qutrit 2.
* A background perturbation of the compactification (metric, B-field, flux non-uniformity) is a sum of plane waves
  e^{2πi(p·x + q·y)}, with k = (p, q) ∈ ℤ⁴.
* Its effect on the matter is its projection onto each bundle's zero modes.

## Results (A₂ and (1,1,4), all wavevectors with |kᵢ| ≤ 2, grid G = 20)

**1. One Pauli per wave.** Every plane wave acts on each flavour qutrit as a **single Weyl (Pauli) operator times a form
factor**.

**2. The selection rule.**

| wavevector class | on the 10 (qutrit 1) | on the 5̄ (qutrit 2) | representation | modes, A₂ / (1,1,4) |
|---|---|---|---|---|
| p, q ∈ N₅ℤ² | non-identity Pauli | scalar | **(8,1)** | 62 / 42 |
| p, q ∈ N₁₀ℤ² | scalar | non-identity Pauli | **(1,8)** | 70 / 48 |
| all others | Pauli | Pauli | (8,8) | 408 / 324 |

All 8 non-identity Paulis occur in each pure class.

**3. The Fourier lattice mod 3 is W(3,3).** The Pauli pair depends only on k mod 3, and it is additive in k (checked on
1574 pairs). So k ↦ (Pauli on the 10, Pauli on the 5̄) is a homomorphism ℤ⁴ → F₃² × F₃² with kernel 3ℤ⁴. All **80**
non-zero residue classes occur: the 80 non-identity two-qutrit Paulis, whose projective classes are the 40 points of
W(3,3). The pure classes are the two factor planes of the flux factorisation.

**4. Gaussian form factor.** log|c| is exactly quadratic in k (R² = 1.000). Modes whose form factor falls below 10⁻⁸ of
the zero mode are suppressed and not classified: 84 for A₂ and 210 for (1,1,4). Their sizes go down to 10⁻¹⁰, with fit
residuals at the 10⁻¹⁷ machine floor.

## Reading

**What the spurions are.** The (8,1) ⊕ (1,8) spurions are the **background Fourier modes whose wavevector lies in one
factor plane** of the flux factorisation:
* N₅ℤ² rotates only the 10, hence only the CKM;
* N₁₀ℤ² rotates only the 5̄, hence only the PMNS.

**Why earlier attempts moved both.** Generic background modes, and the scalar modulus anisotropy of Pass 11922, are
(8,8) and move CKM and PMNS together. This explains the +0.47 correlation found there.

**What enters at first order.** A background deformation changes the zero modes' Kähler metric, K_ab = δ_ab + ε
⟨ψ_a|δ|ψ_b⟩. Its flavour structure is exactly these Pauli projections, weighted by the Gaussian form factor.

**What is not done.** The pass names the geometric object; it does not derive its source. That source would be a non-flat
T⁴, a blow-up, or a flux non-uniformity carrying factor-plane Fourier modes. Nor does the pass derive the amplitudes.

## Prior art

* Magnetic translations and Weyl operators in the lowest Landau level; flavour from magnetized tori (Abe–Choi–Kobayashi–
  Ohki 2010).
* Non-universal Kähler metrics in magnetized models.
* New here: the factor-plane selection rule and its identification with the parallel track's (8,1) ⊕ (1,8) target.
* Corpus: Passes 11921 and 11922; parallel packet 34e149d79.
