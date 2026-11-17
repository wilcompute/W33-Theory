# Pass 12686: follow-ups to the intermediate-scale picture

The vectorlike rescue passes electroweak precision. The boundary-condition pulls are recomputed. SMASH inflation is at ≈2σ against ACT DR6, dark-dimension neutrinos need y ~ 10⁻³, axion-string GWs are unobservable, and unification is unchanged.

Claude track. Follows Passes 12684–12685. **Not a theory of everything.** Script: `toe_pass12686_intermediate_scale_followups.py`; certificate: `data/toe_pass12686_intermediate_scale_followups.json`.

## (1) The vectorlike rescue passes the T parameter by a factor of ~500

The rescue: a doublet Q plus a singlet T, Yukawa y′ H Q T^c, no SM mixing (Pass 12685). The T parameter is computed with the Lavoura–Silva formula for vectorlike quarks. The neutral currents are the products of the charged-current mixing matrices. Calibrations:
- the SM top gives T = 1.2025, matching N_c m_t²/(16π s²c² M_Z²) exactly;
- a degenerate vectorlike doublet gives 0.

| M_VL | y′ (R = 1 / 30 μm) | ΔT |
|---|---|---|
| 1.5 TeV | 0.509 / 0.530 | 0.0005 / 0.0006 |
| 3 TeV | 0.498 / 0.522 | 0.0001 |
| 10 TeV | 0.484 / 0.514 | < 10⁻⁴ |

Split singlet masses of 1.0–2.5 TeV give ΔT = 0.0003–0.0007. The global fit allows |ΔT| ≲ 0.27 (2σ). **The dark-dimension rescue is electroweak-safe.** Its remaining requirements:
- small mixing with the SM, so the partners decay;
- consistency with direct LHC searches. For M_VL ≥ 1.5 TeV that is satisfied for most decay patterns.

## (2) Joint test of λ(μ*) = 0 boundary conditions

The pull is (measured − predicted)/σ. σ includes α_s ± 0.0009 and, for the direct mass, a 0.5 GeV pole/MC ambiguity.

| boundary | M_t predicted | pull (direct 172.57 ± 0.29) | pull (pole 172.4 ± 0.7) |
|---|---|---|---|
| √(v M_Pl) | 172.57 | +0.01 | −0.22 |
| axion f_a (2025 lattice) | 172.39–172.44 | +0.20 | +0.01 |
| √(v M̄_Pl) | 172.80 | −0.35 | −0.52 |
| M_GUT²/M_Pl | 171.42 | +1.74 | +1.27 |
| M_Pl (AS / multiple-point criticality) | 170.98 | +2.40 | +1.84 |
| dark-dimension M₅, no new states | 174.38 | −2.73 | −2.57 |

With the pole/MC ambiguity included, the exclusions of Pass 12684 soften:
- Planck boundary: 2.4σ instead of 3.7σ;
- dark dimension: 2.7σ instead of ≥ 4σ.

The ranking is unchanged. The intermediate-scale boundaries fit; the Planck and dark-dimension boundaries are disfavoured at 2–3σ.

## (3) SMASH-type nonminimal quartic inflation vs ACT DR6: about 2σ low in n_s

The single-field limit is U = λφ⁴/4/(1 + ξφ²)² in the Einstein frame, with the field-space metric included. λ is normalised to A_s = 2.1×10⁻⁹.

| N_* | ξ | n_s | r | λ |
|---|---|---|---|---|
| 55 | 0.1 / 1 / ≥ 10 | 0.9644 / 0.9649 / 0.9650 | 0.009 / 0.004 / 0.0035 | 1.2×10⁻¹¹ / 5.2×10⁻¹⁰ / … |
| 60 | 0.1 / 1 / ≥ 10 | 0.9673 / 0.9678 / 0.9678 | 0.008 / 0.0035 / 0.003 | 1.0×10⁻¹¹ / 4.4×10⁻¹⁰ / … |
| 55–60 | ≤ 0.01 | 0.952–0.965 | 0.05–0.2 | excluded by r |

The maximum is n_s ≈ 0.968 at N_* = 60. P-ACT-LB gives **0.9743 ± 0.0034**, so the pull is −1.9σ at N = 60 and −2.7σ at N = 55. This is the same pressure the literature reports for Higgs and Starobinsky inflation (2505.02407, 2510.18656). The required λ ~ 10⁻¹⁰ (ξ ~ 1) is well inside the PQ window λ_σ ≲ 0.1 of Pass 12685.

> SMASH inflation therefore survives only at the ≈2σ level, unless the ACT shift is a BAO/CMB-tension artefact (as several authors caution) or reheating pushes N_* above 60. Remedies discussed in the literature include a short reheating epoch and R² admixtures.

## (4) Dark-dimension neutrinos in the rescued scenario

Using m_ν ~ y²⟨H⟩²/M₅ (Montero–Vafa–Valenzuela, 2512.09052):

| R | M₅ | y for m_ν₃ = 0.05 eV | m_KK = 1/R |
|---|---|---|---|
| 1 μm | 5.7×10⁸ GeV | 9.7×10⁻⁴ | 0.197 eV |
| 30 μm | 1.8×10⁸ GeV | 5.5×10⁻⁴ | 7 meV |

This is consistent with their y ~ 10⁻³. The bulk sterile KK tower lies at 7–200 meV, the range constrained by cosmology (dark neutrino towers, 2411.07029). The normal-ordering minimum Σm_ν = 0.0588 eV sits just inside the DESI DR2 ΛCDM bound (0.064 eV).

## (5) Axion-string gravitational waves: unobservable

The GW amplitude from global strings scales as f_a⁴ log⁴ (Gorghetto–Hardy–Nicolaescu, 2101.11007). At f_a = 10¹¹ GeV it is ≈ 5×10⁻¹⁷ of its value at f_a = 10¹⁵ GeV, which is roughly the LISA/ET threshold. So the post-inflationary axion of this picture has **no** GW signature. Its tests are haloscopes (MADMAX/ALPHA at 45–65 μeV) and the axion-star / miniclusters phenomenology.

## (6) Unification and perturbativity with the vectorlike family

The family shifts every b_i by +2, so the b_i differences, and hence the SM non-unification pattern, are unchanged. The couplings at M_Pl are (g_Y, g₂, g₃) = (0.52, 0.58, 0.56), all perturbative. It neither helps nor hurts gauge unification.

## Status

**Survives (numerical):** the intermediate-scale picture. The quartic zero, axion dark matter, PQ-threshold stability, the seesaw, √(v M_Pl), and the electroweak-safe vectorlike rescue of the dark dimension are all consistent.

**Under 2σ pressure:**
- SMASH inflation, from the ACT DR6 n_s;
- the Planck boundary;
- the dark dimension without new states.

**Not observable:** the axion-string GWs.

**Sharpest near-term tests:** haloscopes at 45–65 μeV; FCC-ee M_t; LHC/FCC-hh vectorlike top partners with y′ ≈ 0.5; Simons Observatory / CMB-S4 n_s and r (SMASH predicts r ≈ 0.003–0.009).
