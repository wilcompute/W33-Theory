# Passes 11802–11807 — the W(3,3) heterotic Standard Models in two-qutrit levels, II: twisted families, charge quantisation as level integrality, an all-order exotic obstruction, the cubic up texture m_t = m_c, the Z6-II scope, and an exact bracket certificate

Producer: `analysis/w33_pass11802_11807_levels_charges_textures.py`
Input: `data/w33_pass11802_a8_class_states.json.gz` (orbifolder 1.2 states of every model whose θ² shift has an SU(9) half; 47 Z6-I + 13 Z6-II)
Certificate: `data/w33_pass11802_11807_levels_charges_textures.json`
Regression: `tests/test_w33_pass11802_11807.py`

**Conventions.** Levels are the nine weights εᵢ of the SU(9) of the θ² shift (Pass 11714). The occupation profile of a state with momentum p is occᵢ = ⟨p, εᵢ⟩ − mean.

The **core set** is the 33 Z6-I W(3,3) Standard Models whose SM SU(3) × SU(2) lies in that SU(9) and whose three net quark doublets are all untwisted. The SM pair is chosen by Holotrade's criterion: exactly three net doublets, preferring a pair inside SU(9). This corrects 11715's first-version count of 28; see that note.

## 11802 — the twisted half of a family is a single fermion

**Shape.** Every twisted SM-charged state with integral occupation is **single-level**: occupation profile ±εᵢ, one fermion (or hole) in one level. This holds for 757 weights over the 33 models; no other integral shape occurs.

**In the flagship.**
* The twisted d^c are one fermion in a colour level (Y = 1/3).
* The twisted L are one fermion in a weak level (Y = −½).

> **A family is a three-fermion 10** (two GUT levels plus one flavour level, untwisted) **plus a one-fermion 5̄** (one GUT level, at a fixed point).

## 11803 — THEOREM + census: charge quantisation is level integrality

**Theorem.** Y and T₃ are diagonal on the levels, so

  Q_em = Σᵢ qᵢ occᵢ, with q = 1/3 (colour levels), 0 or −1 (the two weak levels), 0 (flavour levels).

Hence **integral occupation ⇒ standard charges**: colour singlets have integer charge and triplets have charge in ℤ ± 1/3.

**Census over the 33 models.** Counts are weights:

| | standard charge | fractional charge |
|---|---|---|
| integral occupation, untwisted | 1253 | 0 |
| integral occupation, twisted | 757 | 0 |
| fractional occupation (all twisted) | 500 | **3543** |

**Every fractionally charged exotic has fractional level occupation**, and all of them are twisted. The converse fails: 500 fractional-occupation weights have standard charges.

**Reading.** Electric charge is the level occupation weighted by (1/3, 1/3, 1/3, 0, −1, 0, 0, 0, 0). Fractional charges are exactly what states that break the SU(9) occupation lattice can carry.

## 11804 — an all-order obstruction to decoupling exotics with ordinary condensates

**Selection rule.** Gauge invariance conserves the total SU(9)-half momentum. So the **fractional class** f = occ mod ℤ (modulo uniform shifts) adds to zero in every coupling, at every order.

**Consequence for masses.** Suppose every condensate has integral occupation. Then a mass term for an SM-charged state in representation R and class f needs a partner in R̄ and class −f.

**Census.** In **all 33** models the SM-charged fractional states are class-unbalanced. The flagship has 5 unbalanced weights among 14.

> **Corollary.** In every one of these Standard Models, some fractionally charged exotics stay massless at every order unless the vacuum condenses **fractional-occupation (twisted, SU(9)-breaking) fields**.

Further constraints, from the hidden gauge factors and the other E₈ half, can only add to this obstruction.

**Relation to prior work.** This is the level-language counterpart, for the Z6-I W(3,3) class, of the all-order lattice obstructions the Codex track proved on its Z6-II benchmark (Pass 11799).

## 11805 — the cubic up texture, the Higgs, and sin²θ_W

**The only cubic up coupling.** Momentum conservation allows exactly two kinds of untwisted Q · u^c · X coupling:
* Q(planes 1, 2) · u^c(planes 1, 2) · H(plane 3);
* Q(3) · u^c(3) · H(3), which the untwisted one-field-per-plane rule forbids.

This holds in 31 of the 33 models; the 2 exceptions (SM_20260917_8 and SM_20260917_151) have no cubic up coupling at all. Therefore the tree-level up Yukawa is

  **Y_up = g · ε_αβ on the two degenerate planes, with singular values (g, g, 0).**

> **m_t = m_c at string tree level**, and the order-three-plane family has no cubic up mass. A realistic hierarchy needs the plane symmetry broken (twisted or higher-order couplings, Wilson-line effects). This is a structural texture of the whole class, not a fit.

**The Higgs.** H = weak ∧ c ∧ d. Its components have Q_em ∈ {−1, 0, 1}, and the neutral component exists. Because electromagnetism is level-diagonal, a vev of the neutral component preserves U(1)_em.

**Coexistence with families.** These vacua use exactly the escape listed in Codex Pass 11731, a *different Higgs representation*. The Higgs is untwisted matter, not an adjoint principal background, and it coexists with the three plane families.

**Weinberg angle.** The level traces give sin²θ_W = Tr T₃² / Tr Q² = (1/2)/(4/3) = **3/8**, the standard unification value.

## 11806 — Z6-II, and the scope of the Codex benchmark

**The Z6-II models.** Of the 128 Z6-II models, 13 have an SU(9) half in 2V, and 9 have the SM inside it. In those 9 the untwisted sector carries only **one (7 models) or two (2 models)** net quark doublets. So the 2+1 level dictionary is a Z6-I phenomenon.

**The benchmark.** The Codex benchmark `Z6II_34__SM_20260917_1558` has θ² classes **(D7+U1, D7+U1) at every fixed point**: 2V + nW₃ and 4V + nW₃ for n = 0, 1, 2 all have 84 integral roots per half. The A8 class would have 72.

**What that means.**
* The benchmark belongs to the W(3,3) *anomaly class*. Every Z6-II shift has anomaly class 1 (Holotrade fbd2c5f).
* It does not belong to the strict A8/SU(9) class, so the two-qutrit level dictionary does not apply to it literally.

This is a scope note on how "W(3,3) heterotic class" is used in the corpus (for example Pass 10960's 215 models). It is not a correction of the Codex results.

## 11807 — exact certificate: the trivector cubic is the nine-level determinant

**Method.** Pass 11681's bracket was applied to all 84 × 84 pairs of trivector basis elements.

**Result.**
* [e_A, e_B] has no operator or trivector part.
* It is nonzero exactly when A and B are disjoint, and then equals **sign(A, B, C) · e\*_C**, with C the complement.

**Count.** That gives **1680 = 9!/(3!)³** nonzero couplings. All of them are partitions, and the constant is exactly 1. The untwisted cubic coupling, and with it y_t = g of Pass 11716, is the determinant of the nine levels.

## Scope

These are readings and selection rules on actual orbifolder spectra, plus one exact algebraic certificate.

**Not computed:**
* CFT coupling magnitudes beyond the untwisted cubic;
* F- and D-flat vacua;
* actual exotic masses;
* corrections that split m_t from m_c.

**Prior art.**
* Holotrade 3caf15e, a6f1cae, 93b34e1 and fbd2c5f.
* Codex 11731 and 11799.
* The standard untwisted-coupling rule, Yukawa = g × ε over planes × E₈ structure constant.
* The classical GUT value sin²θ_W = 3/8.
