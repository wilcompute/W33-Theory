# Pass 11921: the flux factorises W(3,3) into two flavour qutrits, and the radiatively preferred up Higgs is a flavour qutrit

Producer: `analysis/w33_pass11921_flavour_qutrits.py`
Certificates:
* `data/w33_pass11921_flavour_qutrits.json`
* `data/w33_pass11921_mixing_suppression_frozen.json`
* `data/w33_pass11921_qutrit_scan_frozen.json`

Regression: `tests/test_w33_pass11921.py`
Track: Claude. This pass joins Passes 11917–11920 to the corpus's W(3,3) = A[3] dictionary (Pass 11869) and its tensor
factorisations (Pass 11659).

## 1. The flux chooses a tensor factorisation of W(3,3)

**Setup.** Take a det-3 dual pair (N₁₀, N₅ = 3N₁₀⁻¹). Write ℓ_N for the mod-3 image line of N.

**The two translation groups.** Inside A[3] = F₃⁴, the W(3,3) space, the matter bundles have translation groups

  **K(L₁₀) = ℓ₅ × ℓ₅,  K(L₅) = ℓ₁₀ × ℓ₁₀.**

**Theorem.** For the principal Weil pairing, these are orthogonal, nondegenerate hyperbolic planes, and they span A[3].
That is a two-qutrit tensor factorisation (one of the 45), chosen by the flux. Checked for all four dual-pair types.

| field | flux | 3-torsion translation group | flavour charge |
|---|---|---|---|
| 10 (Q, u^c, e^c) | N₁₀ | K₁₀ | qutrit 1 |
| 5̄ (d^c, L) | N₅ | K₅ | qutrit 2 |
| H_u | 2N₁₀ | exactly K₁₀ | qutrit 1 |
| H_d | m·1, gcd(m, 3) = 1 | trivial | neutral |

**What this explains.**
* The up Yukawa lives on qutrit 1 alone, so it is monomial (Pass 11918).
* The down Yukawa is a two-qutrit theta state across the factorisation (Pass 11917). Its determinant is that
  factorisation's G-concurrence (Pass 11659).
* The CKM is the overlap of the up basis with the theta state's qutrit-1 Schmidt basis.

## 2. The radiatively preferred up Higgs is a flavour qutrit

**Exact degeneracy.** The K₁₀ translations act on Q, u^c and H_u, and they permute the three ℤ₃ classes of up Higgs
modes. Therefore the top eigenspace of the up Higgs Gram matrix C_{cc′} = Tr Y_c Y_{c′}† is **exactly 3-dimensional**,
for every modulus and Wilson line.
* The top eigenvalues agree to 4·10⁻¹⁵.
* The cross-class entries vanish to 10⁻¹⁵.
* Checked for A₂ and (1,1,4) with a hypercharge Wilson line.

**The Yukawa in that space.**

  **Y_u(h)_{ab} = h_{a+b} g_{a−b}**  (a, b ∈ ℤ₃), checked to 10⁻¹³ after removing class phases.

* h is a qutrit state, the Higgs's flavour state.
* g = (g₀, g₊, g₋) are three theta values. g₀ is dominant, with |g±/g₀| ≈ 0.015–0.08 at the sampled moduli.
* Without GUT breaking, g₊ = g₋.

**Consequence: the up masses come from h.** When the amplitudes of h are well separated compared with ε = |g±/g₀|,

  m_t : m_c : m_u ≈ the sorted |h_k|.

So the up hierarchy *is* the hierarchy of the Higgs's flavour state, and the up rotation is ≲ ε. The down Gram top
eigenvector is nondegenerate (gap ratio 0.76–0.91), so the radiative H_d is unique.

## 3. Correction to Pass 11918

**What was wrong.** "V_cb = 0 exactly in 87% of aligned rows" over-read a 10⁻⁵ threshold. The small values are Gaussian
suppression, not a selection rule.

| | (1,1,4) | A₂ |
|---|---|---|
| aligned rows | 12 712 | 5631 |
| V_cb < 10⁻¹² (double-precision floor) | 4550 | 787 |
| 10⁻¹² ≤ V_cb < 10⁻⁵ | 6483 | 3912 |
| V_cb ≥ 10⁻⁵ | 1679 | 932 |
| log-slope of V_cb against m_s/m_b | 1.04 | 1.43 |
| median V_cb/(m_s/m_b) | 4.0·10⁻⁷ | 2.8·10⁻⁷ |

**Confirmation.** A re-run sample has V_cb = 6.10·10⁻⁶, the same at theta truncation |n_i| ≤ 4 and ≤ 7.

**What stands.** The conclusion stands and sharpens. When aligned, mixing is Gaussian-suppressed far below the mass
ratios: the data have V_cb/(m_s/m_b) ≈ 2.2. This is the opposite of Gatto–Sartori–Tonin, which would need log-slope ½.

## 4. Does the flavour-qutrit Higgs rescue quark flavour? No

**Setup.** H_u is the qutrit state h, H_d is the radiative one, and the model is the hypercharge Wilson-line model of
Pass 11918. Sampler: `analysis/w33_pass11921_qutrit_scan.py`. The data are frozen, and one sample of each scan is
re-derived bit for bit.

**(a) Haar scan.** 237 moduli, each with the 12 stabiliser states and 200 Haar-random h: 50 244 rows.
* **No row** has realistic up masses (m_u/m_c and m_c/m_t within ×3).
* The CKM alone is reached in 257 rows, but never together with the up masses.

**(b) Targeted fit.** At each of 87 moduli, h is fitted to m_u/m_c, m_c/m_t, V_us, V_cb and V_ub. That is 4 real
degrees of freedom, with 3 class orderings × 12 starts.

| pair | moduli | best log-rms | median | corr(log fitted m_c/m_t, log ε) |
|---|---|---|---|---|
| (1,1,4) | 42 | 1.54 | 2.09 | 0.87 |
| A₂ | 45 | 1.45 | 1.86 | 0.97 |

**What blocks it.**
* **The charm mass is floored by the off-diagonal theta value.** With h hierarchical, the light 2×2 up block has
  off-diagonal entries ε·h_max, so m_c/m_t ≳ ε.
* **Making ε small doesn't help.** It needs large Im Ω, which kills the mixing (§3).
* **The best A₂ fit shows the dead end.** It reaches m_c/m_t = 4.6·10⁻³ only with V_cb = 1, a permutation.

## Reading

**What is new and structural.**
* The two SU(5) flavour sectors are the two qutrits of a W(3,3) factorisation chosen by the flux.
* The up Higgs is itself a flavour qutrit.
* The up Yukawa has the closed form h_{a+b} g_{a−b}.

**What fails.** Single-pair magnetized SU(5) cannot produce quark flavour, whether the Higgs is a single mode
(11918, 11920), a radiative superposition, or a free flavour qutrit (this pass). In every case the mass hierarchy and
the mixing come from the same Gaussian, with the wrong relative power.

**What the next model must have.** A second source of hierarchy that is not Gaussian. Natural candidates:
* a second flux pair, with different localisation per generation;
* non-renormalisable couplings;
* an up Higgs that is not in the top-Yukawa space.

## Prior art

* Heisenberg/magnetic-translation flavour symmetries of magnetized tori: Abe–Choi–Kobayashi–Ohki 2010 (arXiv:1001.1788).
  The factorisation into two orthogonal hyperbolic planes of the W(3,3) space, and the Higgs-as-qutrit degeneracy, are
  the new statements here.
* Corpus: 11659 (G-concurrence / nodes), 11869 (W(3,3) = A[3]), 11872, 11915–11920.
