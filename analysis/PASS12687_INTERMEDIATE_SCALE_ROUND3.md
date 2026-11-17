# Pass 12687: 3-loop QCD closes the running offset; SMASH inflation at −2.65σ; the vectorlike rescue needs ≳1.65 TeV; the dark dimension's dark radiation is +2.6 to +3.1σ against ACT DR6; combined likelihood

Claude track. Follows Passes 12684–12686. **Not a theory of everything.** Script: `toe_pass12687_intermediate_scale_round3.py`; certificate: `data/toe_pass12687_intermediate_scale_round3.json`.

## (1) The two leading 3-loop QCD terms remove the 2-loop offset

Added terms:
- β_g₃ += (65/2) g₃⁷/(16π²)³ (pure QCD, n_f = 6);
- β_yt += −619.4 y_t g₃⁶/(16π²)³ (the 3-loop quark-mass anomalous dimension, γ₂(n_f = 6) = 4.839 in α_s/π units).

| point (M_t, M_h, α_s) | Buttazzo 3-loop λ(M_Pl) | 2-loop offset | + 3-loop QCD offset |
|---|---|---|---|
| 173.34, 125.15, 0.1184 | −0.01430 | −0.00103 | **−0.00005** |
| 172.34, 125.15, 0.1184 | −0.00770 | −0.00112 | −0.00016 |
| 173.34, 125.15, 0.1191 | −0.01250 | −0.00098 | **0.00000** |
| 173.34, 126.15, 0.1184 | −0.01140 | −0.00102 | −0.00003 |

The uniform offset used in Passes 12684–12686 (+0.155 GeV in the required M_t) was exactly the missing 3-loop QCD running. The residual is ≤ 1.6×10⁻⁴ in λ(M_Pl), i.e. ≤ 0.025 GeV in M_t. **All earlier required-M_t numbers stand.**

## (2) SMASH reheating: N_* ≈ 55.6, n_s = 0.9653, −2.65σ

Instant (radiation-like) reheating, k = 0.05 Mpc⁻¹, Liddle–Leach N_* from the inflationary energy scale:

| ξ | N_* | n_s | r | pull vs P-ACT-LB 0.9743 ± 0.0034 |
|---|---|---|---|---|
| 0.1 | 56.05 | 0.9651 | 0.0089 | −2.72 |
| 1 | 55.63 | 0.9653 | 0.0040 | −2.65 |
| ≥ 10 | 55.6 | 0.9653 | 0.0035 | −2.64 |

Instant reheating is the most favourable case: a matter-like reheating phase lowers N_* and hence n_s. **SMASH inflation is disfavoured at ≈2.6σ** if the P-ACT-LB n_s holds. Several authors attribute the ACT shift partly to BAO/CMB tension, so this is not yet decisive.

## (3) The vectorlike rescue needs M_VL ≳ 1.65 TeV

The Yukawa y′ splits the two charge-2/3 states by ≈ y′v/√2 ≈ 89 GeV:

| M_VL | T masses | B | lightest > 1.49 TeV (singlet pair limit)? | > 1.6 TeV (doublet)? |
|---|---|---|---|---|
| 1.5 TeV | 1456, 1545 | 1500 | **no** | no |
| 3 TeV | 2957, 3044 | 3000 | yes | yes |
| 10 TeV | 9958, 10042 | 10000 | yes | yes |

LHC limits are from the 2412.01761 review and the ATLAS (T,B) doublet result; they depend on the branching ratios. y′ changes by only 0.01–0.02 over 1.5–3 TeV (Pass 12685), so the rescue survives for **M_VL ≳ 1.65 TeV**. The y′ ≈ 0.5 Higgs Yukawa of a nearly degenerate T–T′–B triplet is the collider signature.

## (5) The dark dimension's dark radiation vs ACT DR6

ΔN_eff = (4/7)(3 + 7/8·6)(10.75/g_s)^{4/3}: the thermalised 5D graviton (g* = 3) plus bulk neutrinos (g* = 6), decoupled above the electroweak scale. This reproduces the 2411.07029 benchmark of 0.22.

| plasma at decoupling | g_s | ΔN_eff | N_eff | pull vs ACT DR6 P-ACT-LB (2.86 ± 0.13) |
|---|---|---|---|---|
| SM | 106.75 | 0.221 | 3.265 | **+3.1σ** |
| + vectorlike Q+T (needs T_dec ≳ TeV) | 138.25 | 0.156 | 3.200 | +2.6σ |
| + PQ, KSVZ, ν_R (only if T_dec > 10¹¹ GeV) | ~156 | 0.133 | 3.177 | +2.4σ |

The benchmark dark radiation is in about 3σ tension with ACT DR6. Two qualifications:
- **Model dependence.** A 2026 analysis (2606.20486) argues the KK-tower population can be kept negligible through the post-inflationary history. Allowing running of the spectral index relaxes the bound to ΔN_eff < 0.58 (2604.26541).
- **The rescue partly helps.** The vectorlike family needed for the Higgs boundary also dilutes the dark radiation by 30%.

## (4) Combined likelihood (pulls in M_t, n_s, N_eff)

| model | χ² | extra params | ΔAIC vs SM + ΛCDM |
|---|---|---|---|
| SM + ΛCDM (free M_t, n_s) | 2.00 | 0 | 0 |
| λ(√(v M_Pl)) = 0 | 2.00 | 0 | 0.00 |
| λ(f_a, lattice axion) = 0 | 2.04 | 0 | +0.04 |
| λ(M_Pl) = 0 (AS / multiple-point criticality) | 7.74 | 0 | +5.7 |
| dark dimension + vectorlike quark | 6.86 | 1 | +6.9 |
| full SMASH (f_a boundary + its inflation) | 9.01 | 0 | +7.0 |
| dark dimension, no new states | 17.17 | 0 | +15.2 |

The SM baseline's χ² = 2.0 comes from N_eff = 3.044 against 2.86 ± 0.13 (+1.4σ). The boundary models trade a free parameter (M_t) for a prediction at no χ² cost. AIC does not credit what a model explains beyond these three observables: dark matter and strong CP for SMASH, the dark-energy/neutrino coincidence for the dark dimension.

> **Ranking after three rounds (numerical).**
> - The intermediate-scale boundary (λ = 0 at √(v M_Pl) or at the lattice-axion f_a) fits **for free**.
> - The Planck boundary, full SMASH (because of its inflation) and the dark dimension even with its vectorlike rescue (because of dark radiation) sit at ΔAIC ≈ +6 to +7. That is disfavoured but not excluded, and depends on ACT's n_s and N_eff.
> - The bare dark dimension is strongly disfavoured (ΔAIC = +15).
