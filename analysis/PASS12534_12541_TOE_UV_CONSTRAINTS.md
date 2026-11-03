# Passes 12534–12541: an attempt on the theory of everything from outside W(3,3)

Claude track. Producer: `analysis/w33_pass12534_to_12541_toe_uv.py`. Test: `tests/test_w33_pass12534_to_12541.py`. Drivers in `analysis/toe_uv`: `sm_rge.py`, `swampland_casimir.py`, `as_fixedpoint.py`, `criticality.py`, `mpp_k.py`.

Labels: **[E]** exact, **[N]** numerical with a stated control, **[I]** interpretation, **[C]** conjecture of the mechanism being tested.

## Verdict first

**This is not a theory of everything, and none is close.** Nothing below explains the gauge group, the three generations, or the value of the cosmological constant. I tested the two most predictive quantum-gravity programmes I could compute against measured numbers:

| question | result |
|---|---|
| Does the fixed-point relation y_t² − y_b² = g_Y²/3 predict the top mass? | **No: it gives 182 GeV, against 172.57.** This is the published prediction, reproduced and ruled out by 9 GeV |
| Does asymptotic safety predict the Higgs mass? | **Near miss**: 127.2–128.8 GeV at the measured M_t, against 125.20 |
| Does multiple-point criticality fix both? | **Near miss**: matching M_H needs M_t ≈ 170.8 GeV |
| Does no-AdS₃ constrain neutrinos? | **Yes, conditional on a conjecture**: Dirac, normal ordering, Σm_ν ∈ [58.8, 69.9] meV, consistent with DESI |

The useful output is a short list of **experiments that can kill these ideas**, below.

## Controls

**[N]** `sm_rge.py`: two-loop SM RGEs with the NNLO matching of Buttazzo et al. At their reference point, mine against their eq. 61 at 1.22 × 10¹⁹ GeV: g₁ 0.6153 / 0.6154, g₂ 0.5054 / 0.5055, g₃ 0.4873 / 0.4873, y_t 0.3832 / 0.3825, λ −0.0151 / −0.0143. Slopes dλ/dM_t −0.0065 / −0.0066 and dλ/dM_H 0.0029 / 0.0029. The λ gap of 8 × 10⁻⁴ is the missing three-loop piece and is worth about 0.3 GeV in M_H.

`swampland_casimir.py` reproduces the published 7.7 meV and 2.5 meV.

Inputs: M_t = 172.57, M_H = 125.20, α₃ = 0.1180, M_W = 80.369.

## 12534: the swampland neutrino window

**The mechanism [C].** The non-SUSY AdS conjecture says no stable non-supersymmetric AdS vacuum exists. The SM on a circle has a 3D potential ∝ (Λ₄ + Σρ_Casimir)/L². If this goes negative anywhere there is an AdS₃ vacuum. (Ooguri–Vafa; Ibáñez, Martín-Lozano, Valenzuela; Gonzalo, Ibáñez, Valenzuela.) I did not originate this.

**[N] Result**, with Λ₄ = (2.24 meV)⁴ and current oscillation data:

| | Dirac | Majorana |
|---|---|---|
| normal | m₁ ≤ 7.65 meV, **Σ ∈ [58.8, 69.9] meV** | AdS₃ at every mass tested (up to 0.2 eV) |
| inverted | m₃ ≤ 2.54 meV, Σ ∈ [98.9, 101.6] meV | AdS₃ at every mass tested |

Against DESI DR2's Σ < 64.2 meV (95%, ΛCDM), inverted is excluded, and normal Dirac is allowed with m₁ ≤ 4.25 meV. **A window a few meV wide tied to Λ¼ contains the cosmological limit.** That is not independent evidence for the conjecture: the window was already known, and DESI's limit only shows the two do not conflict.

**Caveats.** Cao (arXiv:2306.15383) disputes the treatment of the radius and gets a very different number. The conjecture is unproven, and DESI's limit is model-dependent (w₀wₐ relaxes it to about 0.16 eV).

## 12535: asymptotic safety

**The mechanism [C].** Eichhorn–Held: above M_Pl gravity adds β_g ⊃ −f_g g, β_y ⊃ −f_y y, β_λ ⊃ f_λ λ, with universal f's. Sharp transition at k_tr.

**Branch A, both t and b nonzero (arXiv:1803.04027) [N].** Fitting f_g to g_Y and f_y to y_b leaves M_t predicted:

| k_tr (GeV) | 10¹⁶ | 10¹⁹ | 10²⁰ | 10²¹ |
|---|---|---|---|---|
| M_t (GeV) | 177.2 | **182.0** | 183.5 | 185.1 |

The paper's two-loop value is 182, so the code is right. **Measured: 172.57 ± 0.29.** Lowering k_tr to 10¹⁶ GeV does not rescue it, and other k_tr did not yield a solution on my grid. So this branch is ruled out at this truncation (one loop above k_tr, sharp transition). The paper already quotes 178–182; the mismatch is a limitation they know about.

**Branch B, top-dominated (the current frontier, arXiv:2507.18304) [N].** Fitting f_y to the measured M_t gives f_y = −4.5 × 10⁻⁴, far-UV y_t* = 0.236. Their f_y = −3.3 × 10⁻⁴ and y_t* ≈ 0.25, at their M_t ≈ 171, so we agree on where this is. **Three fits (f_g, f_y, f_λ) to three observables (g_Y, y_t, λ): none of these three is a prediction.** Their predictions are of flavour relations, not checked here.

**[E] The relevance table** (derived by hand here, 1-loop, diagonal, far UV, in units of 1/16π²). θ = β_y/y as y → 0, with G = g_Y*², t = y_t*², θ < 0 relevant, θ > 0 IR-attractive to zero:

| Yukawa | branch A (t − b = G/3) | branch B |
|---|---|---|
| y_b | fixed point | −3t + G = **+0.060** |
| light up | −G/2 | −3t/2 = −0.083 |
| light down | +G/2 | −3t/2 + G = **+0.143** |
| charged lepton | −17G/6 | −3t/2 − 7G/3 = −0.61 |
| Dirac ν | +G/6 | −3t/2 + 2G/3 = **+0.068** |

A nonzero τ on branch A would need y_τ² = (17/9)g_Y², far too large, so τ must sit at zero there.

**What I first thought, and why it was wrong.** I read θ_ν > 0 as "y_ν = 0 exactly", contradicting the Dirac requirement of 12534. Kowalska, Pramanick and Sessolo use exactly this IR-attractive zero to generate tiny Yukawas from a different UV fixed point, and they report Dirac, normal-ordered solutions. **So there is no conflict, and both programmes independently prefer Dirac + normal ordering.** The table's value is that it shows which Yukawas are decaying and how fast: θ_b/16π² ≈ 3.8 × 10⁻⁴ per e-fold is why y_b needs a cascade of thousands of e-folds, matching the scale of about 10³⁴⁰⁰ GeV in arXiv:2507.18304.

**Parameter count.** Only a handful of the roughly 26 SM parameters (g_Y, y_t, y_b, λ) are touched here, mostly by fits. g₂ and g₃ are relevant (free). So asymptotic safety in this form **reduces rather than eliminates** parameters.

## 12536: criticality and the top mass

**[N]** Imposing λ = β_λ = 0 at one scale k gives both masses (`criticality.py`):

| k (GeV) | M_t | M_H |
|---|---|---|
| 10¹⁷ | 169.14 | 121.85 |
| 4.9 × 10¹⁷ | **170.83** | **125.20** |
| 10¹⁸ | 171.56 | 126.70 |
| 2.4 × 10¹⁸ | 172.45 | 128.54 |
| 10¹⁹ | 173.87 | 131.54 |

**No k hits both.** At the measured masses λ(10¹⁹) = −0.0110, and β_λ vanishes near 3.5 × 10¹⁷ GeV with λ = −0.0113 there. Separately, λ(10¹⁹) = 0 at M_H = 125.20 needs **M_t = 170.86**, and the asymptotically safe fixed point at measured M_t gives M_H = 127.2–128.8.

**So both routes want M_t ≈ 170.9 GeV, 1.7 GeV below the 172.57 ± 0.29 value.** The pole-mass extraction carries an ambiguity usually quoted near 0.5 GeV, and α₃ shifts this by about 0.35 GeV per 0.0009. That makes it about 2.4σ on my rough combination, not a discovery.

**A coincidence I am not claiming.** k = 4.9 × 10¹⁷ GeV is close to the classic heterotic scale (Kaplunovsky, about 5 × 10¹⁷). k was solved for, so there is one free scale and one test (M_t), which it misses, and many candidate scales to compare with. It is not evidence.

## How to kill all of this

| measurement | decides | killed if |
|---|---|---|
| Top pole mass at a lepton collider threshold scan (tens of MeV) | near-criticality | M_t stays near 172.5, with α₃ improved: λ = 0 at M_Pl fails |
| Neutrinoless double beta decay (LEGEND, nEXO) | Dirac | **any signal**: no-AdS₃ fails and the Dirac AS solutions fail |
| Σm_ν from DESI, Euclid, CMB-S4 | the window | Σ > 69.9 meV, or a robust Σ below the oscillation floor of 58.8 meV |
| Mass ordering (JUNO) | NO | inverted |
| ΔN_eff (CMB-S4), only if right-handed ν were ever thermal | Dirac | no signal is not decisive: ≈ 0.14 would need high-temperature gravitational production |

## Scorecard

| target | status |
|---|---|
| Gauge group SU(3)×SU(2)×U(1) | **Unexplained** by anything here. It is input |
| Three generations | **Unexplained** |
| g_Y | Fit (f_g) |
| g₂, g₃ | Free |
| y_t | Fit, or wrong by 9 GeV on branch A |
| y_b | Bound from above in the literature; I did not check it |
| Light quarks, leptons | Free or unchecked |
| M_H | Correlated with M_t; near miss |
| CKM | Partial claims in arXiv:2507.18304, not checked here |
| ν | Dirac + NO preferred, conditional on two unproven programmes |
| Λ | **Input.** The window relates it to m_ν and does not derive it |
| Dark matter, baryogenesis, inflation, strong CP | **Not addressed** |

**What would count as a real step:** deriving f_g, f_y from a gravity calculation that gives 172.6 GeV without a fit, or deriving the matter content. I did neither.

## Sources

- D. Buttazzo et al., *Investigating the near-criticality of the Higgs boson*, arXiv:1307.3536.
- A. Eichhorn, A. Held, *Top mass from asymptotic safety*, arXiv:1707.01107; *Mass difference for charged quarks from asymptotically safe quantum gravity*, arXiv:1803.04027.
- R. Alkofer et al., arXiv:2003.08401. A. Eichhorn, Gyftopoulos, A. Held, arXiv:2507.18304.
- K. Kowalska, S. Pramanick, E. M. Sessolo, arXiv:2204.00866.
- L. E. Ibáñez, V. Martín-Lozano, I. Valenzuela, arXiv:1706.05392. E. Gonzalo, L. E. Ibáñez, I. Valenzuela, arXiv:2109.10961. Cao, arXiv:2306.15383.
- DESI: arXiv:2503.14738, arXiv:2503.14744.
- C. D. Froggatt, H. B. Nielsen, *Standard Model criticality prediction*, Phys. Lett. B 368 (1996).
