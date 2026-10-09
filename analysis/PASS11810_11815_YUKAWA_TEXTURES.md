# Passes 11810–11815 — all-order Yukawa textures of the W(3,3) Z6-I Standard Models: top = charm at tree level, bottom and tau only through the hidden sector at high order, fractional charges labelled by a bit and a qutrit, and a Lean module

Producer: `analysis/w33_pass11810_11813_yukawa_textures.py`
Probe: `analysis/w33_pass11813_level_probe.cpp` (derived from Pass 11797's probe; build with `analysis/w33_pass11797_build_probe.py`, pointing its source name at this file)
Inputs: `data/w33_pass11810_probe_fields.json.gz` (orbifolder field data of the 33 core models), `data/w33_pass11802_a8_class_states.json.gz`
Certificate: `data/w33_pass11810_11813_yukawa_textures.json`
Lean: `formal/W33/Pass11815LevelCharges.lean`
Regression: `tests/test_w33_pass11810_11815.py`

## Method

**What is tested.** For a mass-matrix entry A_i B_j H ∏S, the question is whether some non-negative integer vector of insertions S satisfies the necessary selection rules, and at what minimal degree.

**The rules.**
* **(G)** All U(1) charges sum to zero. This is exact.
* **(N)** Hidden SU(5), SU(4) and SU(2) N-ality sums to zero. This is necessary.
* **(K)** The point-group sector sum is k ≡ 0 (mod 6).
* **(R)** The H-momentum rule: Σ(q_sh + osc)ᵢ ≡ −1 (mod (6, 6, 3)).

**How it is solved.** A mixed-integer linear program (scipy `milp`) gives the minimal degree. Infeasibility is an **all-order** exclusion under the rules used.

**Status of the R rule.**
* R is exact for untwisted fields.
* For twisted states in the non-prime G2 planes, the γ correction of arXiv:1301.2322 is not established for Z6-I. Results that rely on R are therefore tested under four γ placements: none, plane 1, plane 2, both.
* Rigorous lower bounds are also computed **without R**, which strictly relaxes the rules.

**Insertions.** Two kinds are used:
* *pure singlets*, which are hidden-neutral;
* *composites*: every Y = 0 SM singlet, subject to hidden N-ality.

Nine models whose hidden representations are SO-type (dimensions 8, 16) are excluded from the composite analysis, leaving 24.

**Higgs mixing.** The analysis is optimistic about it: each entry takes the minimum over all doublets of the right hypercharge.

## 11810 — up quarks: top = charm at tree level

**Tree level.** In all 33 core models the only cubic up couplings are Q_α u^c_β H with α ≠ β on the two degenerate planes. So

  **Y_up = g ε_αβ, and m_t = m_c at string tree level.**

**Calibration.** On the flagship, orbifolder's own `AddCoupling` also admits q₁·bu₁·bl₁ and q₂·bu₂·bl₁. Both violate the exact untwisted H-momentum rule; `AddCoupling` does not apply R. This is recorded in the certificate.

**Pure-singlet condensates.** In **10 models**, the flagship among them, the up matrix is **exactly g·ε to all orders**, under every γ placement. Four more are locked under no γ, plane-1 and plane-2 placements; only with γ on both planes do they acquire a very-high-order third-family entry. In all of these models no gauge-neutral pure-singlet monomial carries nonzero R. That is the structural reason: no singlet insertion can repair the R mismatch of the diagonal entries.

**Hidden composites.** In all 24 analysable models the entries that split top from charm (the diagonal of the ε block) first appear at singlet degree **≥ 6**, typically 9–21. The third family's diagonal entry appears at degree 3.

## 11811 — down quarks and charged leptons: only through the hidden sector, at very high order

**Hidden-neutral condensates.** In **22 of 33** models, including the flagship, the down and lepton matrices vanish **to all orders by U(1) gauge invariance alone** (0/120 and 0/84 entries in the flagship).

**Hidden composites.**
* With R, they first appear at degree **15–24** in all 24 analysable models.
* Without R, the rigorous lower bound is **≥ 8** in 22 of 24; two models allow degree 1.

> **Reading.** In this class the bottom and tau masses must come from hidden-sector composites (confining hidden SU(5)/SU(4)/SU(2)) through operators of very high degree. With string-scale-suppressed condensates, m_b/m_t and m_τ/m_t are suppressed far below their observed values (≈ 1/40 and 1/100). Together with m_t = m_c, this is a sharp phenomenological verdict on the whole class in perturbative superpotential terms.

## 11812 — the fractional-class group is ℤ₂ × ℤ₃: a bit and a qutrit

This holds in **all 47** Z6-I A8-class models.

* **One class per fixed point.** Every twisted fixed point carries a single fractional level class.
* **The group.** The classes generate exactly ⟨[V]⟩ × ⟨[W]⟩ = **ℤ₂ × ℤ₃**:
  * the shift class [V] has order 2;
  * the class [W] of the Wilson line on the order-three plane has order 3.

> **Every fractional electric charge is labelled by one bit (θ³ parity) and one qutrit (the fixed point of the order-three plane).**

Combined with Pass 11804: decoupling the exotics needs condensates at specific qutrit-plane fixed points with odd θ³ parity.

## 11813 — tool

The level probe dumps orbifolder's internal field data:
* SM-analyser labels;
* sector index;
* representation dimensions;
* all U(1) charges;
* q_sh, oscillator and γ data.

It also checks named couplings with orbifolder's own gauge and space-group filter. That filter is a **necessary screen only**: it applies no R rule and computes no amplitudes.

## 11815 — Lean

`formal/W33/Pass11815LevelCharges.lean` proves the following, with no `sorry`. It type-checks against the repository's Mathlib.

| result | statement |
|---|---|
| 11803 | an integral level occupation has integer electric charge iff its colour number is divisible by 3; otherwise the charge lies in ℤ ± 1/3 |
| 11805 | sin²θ_W = Tr T₃² / Tr Q² = 3/8 from the level traces |
| 11807 | 9!/(3!)³ = 1680 ordered partitions of the nine levels |
| 11714 | the SU(9) anomaly A(Λ³C⁹) = 9, and 3 · 9 = 27 = 3³ |


## Relation to Holotrade 82f8d66 / 2fa6596 / b81ef8c, and a correction

**Down and lepton zeros (prior art).** Holotrade 82f8d66 found the down-quark and charged-lepton Yukawas absent in exactly the 55 doublet–triplet solvers. Holotrade 2fa6596 corrected the reason: those models have a single doublet charge class, i.e. no Higgs-type doublet. That is prior art. Pass 11811 adds:
* an all-order statement (MILP over every insertion degree);
* the hidden-composite channel, which first appears at degree 15–24.

**Correction of the up texture.** Holotrade 82f8d66 reported the flagship's order-three q u^c H_u couplings at plane entries (3,3), (1,1), (1,2), (2,1), (2,2): a "2+1 block", read as qualitatively CKM-like.
* The entries (1,1), (2,2) and (3,3) pair Q and u^c from the **same** untwisted plane.
* The untwisted cubic superpotential is g ε_ijk f_abc Uⁱ Uʲ Uᵏ, with one field per plane, so the exact untwisted H-momentum rule forbids them.
* Orbifolder's `AddCoupling` admits them because it does not apply the R rule (calibration, Pass 11813).

The cubic up texture is therefore **only** the ε pair (1,2), (2,1): two degenerate tree-level masses, top = charm. The block-diagonal CKM reading of 82f8d66 does not survive, and its "heavy top from a cubic" becomes "a degenerate heavy top–charm pair from a cubic".

## Scope

**Necessary rules only.**
* No CFT amplitudes.
* No F- or D-flat vacuum.
* The γ-corrected R rule for Z6-I G2 planes is not established, which is why variants and no-R bounds are reported.

**What is claimed.** The conclusions are about degeneracy and suppression, which hold **for every allowed coefficient**. They are not mass predictions.

**Prior art.**
* Holotrade 93b34e1 (cubic tops) and 3caf15e (plane table).
* Codex Passes 11797–11801 (probe, all-order lattice obstructions on Z6-II).
* The Froggatt–Nielsen-style reading of singlet insertions is standard.

**Passes 11814, 11816 and 11817 are released unused.**
