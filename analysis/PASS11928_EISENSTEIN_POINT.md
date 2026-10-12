# Pass 11928: the Eisenstein point of the flavour torus — ℤ₃ generation charges, a W(3,3) line of fixed points, and polynomial hierarchies

Producer: `analysis/w33_pass11928_eisenstein_point.py`
Certificate: `data/w33_pass11928_eisenstein_point.json`
Regression: `tests/test_w33_pass11928.py`
Track: Claude.

**Motive.** Pass 11921 showed that quark flavour needs a second, **non-Gaussian** hierarchy source. A residual symmetry at a
modular fixed point is the standard source of polynomial hierarchies (Novichkov–Penedo–Petcov). This pass computes it for
the corpus's own Eisenstein point, on the magnetized SU(5) torus with the A₂ dual pair.

## 1. Residual ℤ₃ and generation charges

**The symmetry.** At Ω = ω·1 the rotation ρ: z ↦ ωz is a lattice automorphism. Every symmetric flux in the dx∧dy block is
ρ-invariant, so ρ acts on every zero-mode space, unitarily to 10⁻¹⁵.

**The charges** (eigenphase / (2π/3)):

| field | charges | multiplicities of 0 / 1 / 2 |
|---|---|---|
| 10 (A₂) | (0, 0, 2) | 2 / 0 / 1 |
| 5̄ (A₂′) | (0, 0, 2) | 2 / 0 / 1 |
| H_u (2A₂, 12 modes) | — | 3 / 5 / 4 |
| H_d (4·1, 16 modes) | — | 5 / 5 / 6 |

**The charge-2 generation** is an unbiased vector in the mode basis (all components of modulus 1/√3), i.e. a
stabiliser-type state relative to the up basis.

## 2. The orbifold fixed points form a W(3,3) line

**The line.** The 9 ρ-fixed points are A[1−ω] = {(x, −x)} ⊂ A[3] = F₃⁴. That is a totally isotropic plane: a **line of
W(3,3)**. For the A₂ pair it splits as (L ∩ K₁₀) ⊕ (L ∩ K₅), three points each.

**Charges localise.** At every fixed point the zero-mode value vector is an eigenvector of ρ. Value vectors transform by Rᵀ;
the eigen-residual is 2·10⁻¹⁵.
* **3 fixed points** carry local charge 0; their vectors lie in the charge-0 plane.
* **6 fixed points** carry charge 2; their vectors lie along the charge-2 generation.

**What blow-ups can do.** Point-localised (blow-up) Kähler corrections at the fixed points therefore **commute with the
residual ℤ₃** (commutator 2·10⁻¹⁵). They act block-diagonally, and their traceless image has rank 3 on each flavour
qutrit. They can split the degenerate charge-0 pair without mixing charges.

**Which planes give scalar sums.** Among all 130 planes of A[3], only K(L₁₀) and K(L₅) give scalar point-source sums
(on the 10, resp. the 5̄).

**A withdrawn reading.** A first reading took the common blow-up eigenvector to be a mode vanishing at all fixed points.
The fixed-point value matrix has full rank (singular values 2.07, 1.46, 1.46), so that reading was wrong. The correct
statement is the charge localisation above.

## 3. Polynomial hierarchies near the point

**Setup.** Perturb the modulus as Ω = ω·1 + ε(a + bJ), with the Higgs in a fixed ℤ₃-charge sector. Fits are log–log over
ε = 10⁻², 3·10⁻³, 10⁻³.

| Higgs charge | m_c/m_t | m_u/m_c |
|---|---|---|
| 0 | O(1) constant (slope 0.00) | ∝ ε² (slope 1.99) |
| 1 | ∝ ε (slope 1.00) | O(1) constant (slope 0.00) |
| 2 | 1 − O(ε) (slope −0.01) | ∝ ε² (slope 2.01) |

The O(1) constants depend on the Higgs combination inside its charge sector.

## Reading

**What proximity buys.** Proximity to the Eisenstein point supplies exactly the **polynomial, non-Gaussian** hierarchy that
Pass 11921 said was missing. That is a genuine new handle in this geometry.

**Its limit.** Each Higgs charge produces **one** hierarchical up ratio. The two charge-0 generations are degenerate under
the residual ℤ₃, so no single charge sector makes m_c/m_t and m_u/m_c both small.

**What could fix it.** The blow-up modes of the orbifold fixed points act precisely inside that degenerate charge-0 block,
without breaking the ℤ₃. Natural next test: charge-1 Higgs (m_c/m_t ∝ ε) plus charge-0 blow-up splitting. Their
combination is the candidate two-parameter, non-Gaussian texture.

## Prior art

* Residual symmetries and hierarchies near modular fixed points: Novichkov–Penedo–Petcov; Feruglio et al.
* Magnetized orbifold zero modes and Z_N fixed points (Abe–Kobayashi et al.).
* Orbifold charge localisation at fixed points (standard).
* New here:
  * the Eisenstein-point charges of the W(3,3) flavour qutrits;
  * the W(3,3)-line fixed set and its split across the flux factorisation;
  * charge localisation and the ℤ₃-commuting blow-up spurions;
  * the one-ratio-per-charge polynomial law.
* Corpus: Passes 11869, 11874 (fixed points of the level-3 modulus), 11876 (one modulus for all sectors excluded),
  11897 (T⁴/ℤ₃ Kähler moduli), and 11917–11927.
