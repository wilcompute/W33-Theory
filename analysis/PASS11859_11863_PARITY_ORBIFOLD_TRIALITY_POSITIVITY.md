# Passes 11859–11863 — no automorphism of E₈ makes chirality; the central translation is colour triality; three central-charge sectors in a 1 + 2 pattern; exact positivity bounds g₃² ≤ 1/48, g′² ≤ 1/8 + 6g₃², g₄ ≤ 1/12; B−L survives Lorentz-invariant breaking; Lean: A₆ ↛ SL(2,ℂ)

**Files**
* Producers:
  * `analysis/w33_pass11859_11862_parity_orbifold_sectors_breaking.py`
  * `analysis/w33_pass11861_bootstrap_positivity_bounds.py`
* Frozen:
  * `data/w33_pass11859_11862_parity_orbifold_sectors_breaking.json`
  * `data/w33_pass11861_bootstrap_positivity_bounds.json`
* Lean: `formal/W33/Pass11863A6NotInSL2.lean`
* Regression: `tests/test_w33_pass11859_11863.py`

## 11859 — the parity orbifold, and a sharper firewall (corrects the 11855 contrast)

**Construction.**
* The stabiliser of a Kramers reversal is SL(2,9)·2. Its anticentraliser coset (gJ₀g⁻¹ = −J₀: the F₉-antilinear parity)
  normalises the Lorentz group without centralising it.
* Each element h of that coset is lifted to E₈ through its Weil action on Di, as diag(D_h, det⁻¹) ∈ SU(5)_L.
* All sampled lifts normalise the so(11) commutant.

**Results.**
* **Parity alone.** On the spinorial block (32, Di), all 24 sampled parity projections keep **vector-like** spectra:
  n(10) = n(1̄0̄) and n(5̄) = n(5), with kept dimensions 0, 32 or 64. Lorentz elements, the controls, behave the same.
* **GUT phase × parity.** Combine the GUT-side Spin(10)-centre phase exp(2πiX/4) (X = the u(1) of so(10) ⊃ su(5), with
  charges ±1, ±3, ±5 on the spinor block) with parity elements. 16 elements had conjugate-paired eigenvalues on Di and
  16 did not (including 7 parity elements). **Every case is still vector-like.**

**Why: no single automorphism of E₈ produces chirality.**
* The adjoint of E₈ is a *real* representation. For any element g of the compact E₈, the fixed space is closed under the
  real structure, so it is a self-conjugate representation of the centraliser C(g).
* In SU(5)_L × SU(5)_GUT language the spinorial block is (10, Di) + (5̄, Di) + (1̄0̄, Di*) + (5, Di*). The conjugate
  multiplets pair with **Di\***. A phase λ on Di is therefore λ̄ on Di*, and the condition "eigenvalue 1" selects
  conjugate-paired kept spaces.

**Correction to 11855.** The 11855 "contrast", a Lorentz-breaking phase i on Di keeping exactly one 16, is correct in the
abstract product 32 ⊗ Di. But that action is **not an automorphism of E₈**: inside E₈ the 1̄6̄ is paired with Di*, on
which the phase is −i. The 11855 theorem itself (Lorentz-commuting projections are vector-like) stands, and is now a
special case of the general statement.

**Consequence: where chirality has to come from.** In E₈-based models chirality comes from pairing a *complex*
E₈-eigenspace with a *complex geometric* factor, as in orbifolds, where gauge eigenvalue ω pairs with internal
coordinates of eigenvalue ω̄. In the finite geometry the candidate complex factors are the charged central-charge
sectors of 11860.

## 11860 — generations: multiplicity-free E₈, and three central-charge sectors

* **E₈ is multiplicity-free** under so(11) × SL(2,9). The Lorentz parts of (55,1) + (11,5′) + (32,Di) + (1,Sym²Di) are
  irreducible and pairwise distinct: character norms 1, overlaps 0. Since the so(11) parts are also distinct, **no
  internal × Lorentz multiplet occurs more than once**, so repetitions (generations) cannot arise inside a single E₈
  under these symmetries. The bosonic A₆ embedding is likewise multiplicity-free (11846).
* **Three sectors, forced by geometry.** The translations ℤ₃ · M have a centre ℤ₃. Their characters split into three
  central-charge sectors k = 0, 1, 2 of 81 characters each.
  * **k = 0** is Minkowski momentum space, with A₆ orbits **1 + 20 + 30 + 30**.
  * **k = 1 and k = 2** are conjugate, with orbits **6 + 15 + 60**: no fixed point (as non-splitness requires), and
    isomorphic to each other but not to k = 0.

  So the geometry forces exactly three sectors, in a **1 + 2 pattern** (one neutral, two conjugate charged), not three
  identical copies.
* Combined with 11862, the charged sectors pair with colour triality: see the reading there.

## 11861 — exact reflection-positivity bounds on the bulk couplings

**Conventions.**
* Bulk action S = ½φG⁺φ + ½χΠ₂₀χ + (g₃/3!)Σφ³ + (g₄/4!)Σφ⁴ + (g′/2)Σφ²χ, with crosscap propagator G = 12Π₁₅ for φ and
  unit propagator Π₂₀ for the hidden χ.
* Boundary operators are unit-normalised, so the two-point function is Π₁₅.
* Tree four-point function = D − g₄C + g₃²E₁₅ + g′²E₂₀.

**The s-channel eigenvalues are integers:**

| channel | D | C | E₁₅ | E₂₀ |
|---|---:|---:|---:|---:|
| 60 | 2 | 0 | −96 | 0 |
| 24 | 2 | 0 | 96 | −16 |
| 20 | 2 | 24 | 288 | 40 |
| 15 | 2 | 24 | 384 | 32 |
| 1 | 17 | 60 | 576 | 64 |
| Λ² (105) | 0 | 0 | 0 | 0 |

**Positivity, channel by channel, gives exactly:**
* **g₃² ≤ 1/48**, from the 60-channel (fed only by φ-exchange);
* **g′² ≤ 1/8 + 6g₃²**, from the 24-channel. At g₃ = 0: **g′² ≤ 1/8**;
* **g₄ ≤ 1/12** at g₃ = g′ = 0, from the 15 and 20 channels. The repulsive quartic is bounded; the attractive side is
  unbounded at tree level;
* the 1, 15 and 20 channels give the full linear region: 17 − 60g₄ + 576g₃² + 64g′² ≥ 0, etc.

These are the finite analogues of unitarity bounds. Beyond them, the truncated tree-level bulk theory cannot be dual to
a reflection-positive boundary.

## 11862 — Lorentz-invariant breaking, B−L, and the central translation as colour triality

* **The commutant of SL(2,9) × ℤ₃** (11857), su(3) ⊕ so(5) ⊕ u(1) of rank 5, **contains the Standard-Model algebra**.
* **Its centre is B−L.**
  * On the spinorial block its charges are **(±1/4)⁴⁸ (quark-like, 3 × 16) and (±3/4)¹⁶ (lepton-like)**: lepton/quark
    ratio 3, the B−L pattern of so(6) ⊃ su(3) ⊕ u(1).
  * On all of E₈ the charges are 0⁵⁴, (±1/4)⁴⁸, (±1/2)³⁰, (±3/4)¹⁶, (±1)³.
* **Rank argument.** Lorentz-invariant directions of E₈ are exactly the commutant. Compact (semisimple) vevs there
  preserve rank 5. **So no Lorentz-invariant adjoint Higgs can reduce su(3) ⊕ so(5) ⊕ u(1) to the rank-4 SM: in the
  spinorial structure U(1)_{B−L} survives**, unless the Lorentz group or the adjoint-Higgs assumption is given up.
  * The bulk 15 and 20 modes are internal singlets, so vevs on them cannot break internal symmetry at all.
  * The bosonic A₆ × ℤ₃ structure gives the rank-4 SM directly (11850).
* **The central translation is colour triality.**
  * On E₈, **t_c = exp(8πi Y)** exactly (error 9·10⁻⁸, as automorphisms). Its ℤ₃ charge on every state is
    **q ≡ 12Y (mod 3)**:
    * Q and the (3,2)_{−5/6} → ω²;
    * uᶜ, dᶜ and the (3̄,2)_{5/6} → ω;
    * leptons and all colour singlets → 1.
  * This is **colour triality**: t_c is the centre element of SU(3)_colour.
  * **This explains 11850.** A₆ × ℤ₃ commutes with exactly the SM algebra because the central translation removes
    precisely the triality-±1 X/Y bosons of su(5).
* **Reading (conditional).** If the central ℤ₃ of the geometry and the central ℤ₃ of colour are identified in an
  orbifold-type invariance condition (gauge phase × character phase = 1), then colour singlets (leptons, triality 0)
  live in the neutral sector k = 0, i.e. ordinary Minkowski momentum space. Quarks and antiquarks (triality ±1) live in
  the conjugate charged sectors k = 2, 1 (orbits 6 + 15 + 60). This is a structural observation, not a derived
  confinement mechanism.

## 11863 — Lean: A₆ has no faithful image in SL(2, ℂ)

`W33.Pass11863A6NotInSL2` proves:
* **The involution lemma**, entrywise via `linear_combination`: in SL(2,ℂ), g² = 1 forces g = ±1. The key step is
  (a + d)² = 4, which forces b = c = 0 and a = d = ±1.
* **`no_injective_hom`**: the two distinct involutions (0 1)(2 3) and (0 1)(2 4) of A₆ would both map to −1. This is
  the finite step of the family no-go of 11854. That A₆ is perfect, so its U(2)-image lies in SU(2), is stated in the
  docstring, not formalised.

## Prior art and scope

* **Classical.**
  * E₈ adjoint is real.
  * Orbifold chirality needs geometric complex phases (Dixon–Harvey–Vafa–Witten).
  * The SM centre: the hypercharge ℤ₆ coincides with the centre of SU(3) × SU(2).
  * Finite subgroups of SL(2,ℂ).
* **Corpus.**
  * Passes 11832, 11844–11858.
  * Parallel Round 33 (non-split translations) and Round 35 (vector-like spectrum), cited.
* **New here.**
  * Parity and phase × parity projections are vector-like, explained by the real-representation argument, with the
    correction of 11855's contrast.
  * The 1 + 2 central-charge sectors (orbits 6 + 15 + 60).
  * The multiplicity-freeness of E₈ under so(11) × SL(2,9).
  * The exact integer positivity bounds.
  * The B−L centre and the rank obstruction.
  * **t_c = exp(8πiY) = colour triality.**
  * The Lean involution lemma and no-injective-hom theorem.
* **Scope.** Exact finite-group, Lie-algebra and linear-algebra computations. Physical names ("B−L", "colour",
  "triality", "unitarity bound") are fixed by the computed spectra and centre actions. No vacuum, confinement or chiral
  mechanism is derived.
