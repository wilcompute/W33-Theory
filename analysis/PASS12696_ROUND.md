# Pass 12696: a b-only PQ charge gives completion A a flavour-safe, N_DW = 1, visible axion; FCC-hh measures B's y′ to ±0.002; the keV-window particle; the Cabibbo anomaly needs a 5 s Ft shift

Claude track. Follows Pass 12695. **Not a theory of everything.** Script: `toe_pass12696_round.py`; certificate: `data/toe_pass12696_round.json`.

## (1) PQ anomaly-coefficient scan: completion A's conflict resolved at the bookkeeping level

The scan covers integer PQ charges in [−2, 2] on the third-family up-type quark (x_u), down-type quark (x_d) and charged lepton (x_e), with the light families neutral (CKM-level flavour safety, Pass 12694). It optionally adds a KSVZ colour triplet (x_Q, Y_Q ∈ {0, −1/3, 2/3}).
- N = (x_u + x_d + x_Q)/2; E = 3(4/9 x_u + 1/9 x_d) + x_e + 3Y_Q² x_Q; N_DW = |2N|.
- **460 assignments have N_DW = 1**; 352 of them charge the third family and keep g_aγγ ≥ 0.5 g_KSVZ.

| assignment | E/N | N_DW | g_aγγ / g_KSVZ | haloscope time |
|---|---|---|---|---|
| **b only** (x_d = ±1) | 2/3 | 1 | 0.65 | × 5.6 |
| b and τ, opposite signs | −4/3 | 1 | 1.69 | × 0.12 (easier) |
| b and τ, same sign (H_d-type) | 8/3 | 1 | 0.39 | × 44 |
| t and τ, same sign | 14/3 | 1 | 1.43 | × 0.24 |
| (Pass 12695) t and b | 5/3 | 2 | 0.13 | × 3,300 |

> **Result (anomaly bookkeeping, not a full model).** Pass 12695's conflict came from charging both t and b. Charging **one** third-family quark (b alone, or with τ) gives a flavour-safe axion with **N_DW = 1** and a photon coupling 0.4–1.7× KSVZ. Each such assignment needs a PQ-charged Higgs doublet coupling to that quark: a two-Higgs-doublet (DFSZ-like) structure whose consistency (doublet masses, mixing with the singlet) is not checked here. The lattice window m_a = 45–65 μeV applies, since N_DW = 1.

## (2) FCC-hh measures B's Yukawa

At σ ≈ 2.4 pb per state at 1.65–1.7 TeV (Pass 12692) and 30 ab⁻¹, with a 5% per-state mass resolution:

| reconstruction efficiency | N_rec per state | δ(ΔM) | δy′ |
|---|---|---|---|
| 10⁻³ | 7×10⁴ | 0.45 GeV | 0.0026 |
| 10⁻² | 7×10⁵ | 0.14 GeV | 0.0008 |

This holds if the states decay directly (SM mixing ≳ 10⁻⁴, so both T and T′ peaks are visible). In the cascade regime, ΔM comes from the soft-lepton endpoint instead. B's prediction y′ = 0.51 ± 0.02 would be tested at the 10–25σ level.

## (3) The keV-window particle

A particle X decaying electromagnetically at T = 5–30 keV, to reduce the CMB N_eff to 2.86 (Pass 12695):

| decay temperature | lifetime | ρ_X/ρ_γ at decay | ζ_X = m_X n_X/n_γ |
|---|---|---|---|
| 5.3 keV | 4.7×10⁴ s | 0.064 | 9×10⁻⁷ GeV |
| 10 keV | 1.3×10⁴ s | 0.064 | 1.7×10⁻⁶ GeV |
| 30 keV | 1.5×10³ s | 0.064 | 5×10⁻⁶ GeV |

Requirements: a lifetime of 10³–5×10⁴ s, a large abundance, and almost no neutrino or hadronic branching (hadronic BBN bounds at these lifetimes are orders of magnitude below ζ ~ 10⁻⁶ GeV). Photons stay below the 2.22 MeV deuterium threshold for T > 5.3 keV. Such a particle is possible but finely arranged. It still explains only the CMB half of the hint.

## (4) The Cabibbo-angle anomaly as an Ft shift

V_ud² ∝ 1/Ft. To bring the superallowed V_ud (0.97373) up to the neutron value (0.97456), the corrected Ft = 3072.24(1.85) s must drop by **5.2 s, which is 2.8σ** of its quoted uncertainty. A shift of that size in the nuclear-structure correction δ_NS or the inner radiative correction Δ_R^V is larger than current estimates. So either the superallowed corrections are underestimated, or the neutron g_A (PERKEO III) and the bottle τ_n must move.

## Status ledger after Passes 12684–12696

| item | status |
|---|---|
| Higgs-quartic zero at √(v M_Pl) / axion f_a | fits at the measured m_t (ΔAIC ≈ 0); look-elsewhere 12% |
| Completion A (intermediate scale) | viable with: an extra scalar (ACT n_s), ξ ≳ 10 (leptogenesis), **b-only (or b+τ) PQ charges** (flavour-safe, N_DW = 1, visible), a ≥ 1.8 TeV light flavon |
| Completion B (dark dimension + top partner) | viable with: y′ = 0.51 ± 0.02, triplet ≥ 1.74 TeV, GeV reheating; HL-LHC can exclude it to 2.1 TeV; FCC-hh measures y′ to ±0.002 |
| Planck boundary (AS/MPP) | 2.4σ disfavoured |
| Low N_eff (ACT + helium ≈ 2.85) | −2σ hint; only a partial (CMB-only) keV mechanism; SO decides at 3.9σ |
| Anomalies: α (Cs/Rb), KM3NeT, neutron τ, deuterium, W mass, Cabibbo angle | each traced to a measurement-method or input choice, none requiring new physics |
