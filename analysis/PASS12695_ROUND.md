# Pass 12695: A's light flavon needs v_F ≳ 1.8 TeV; HL-LHC can only exclude B (to ~2.1 TeV); a third-family axion is ~3,300× harder for haloscopes and has N_DW = 2; a keV entropy window explains only the CMB N_eff; neutron V_ud removes the Cabibbo-angle anomaly

Claude track. Follows Pass 12694. **Not a theory of everything.** Script: `toe_pass12695_round.py`; certificate: `data/toe_pass12695_round.json`.

## (1) Completion A: a PQ-neutral flavon for the light families

Flavon exchange generates (d̄s)² with coefficient ~ m_d m_s / v_F⁴ (couplings √(m_d m_s)/v_F, m_φ ~ v_F). The ε_K bound Λ > 1.6×10⁵ TeV, for an O(1)-phase coefficient, gives **v_F ≳ 1.8 TeV**. The flavon is PQ-neutral, so NA62 is untouched. Completion A's flavour structure is therefore:
- PQ charges on the third generation (Pass 12694);
- a separate TeV-or-heavier flavon for the first two generations.

## (2) Completion B at the HL-LHC

Single-T projections at 3 ab⁻¹ are ≈ 1.85 TeV exclusion (CMS 2016) and 1.44 TeV discovery (CMS 2022). The triplet's 3× cascade rate shifts both by +202 GeV:

| | lightest T | M_VL |
|---|---|---|
| HL-LHC exclusion reach | 2.05 TeV | **≈ 2.10 TeV** |
| HL-LHC discovery reach | 1.64 TeV | 1.69 TeV |
| current limit (Pass 12693) | 1.69 TeV | 1.74 TeV |

> The HL-LHC discovery reach lies **below** the present limit. HL-LHC can exclude completion B's triplet up to ≈ 2.1 TeV but cannot discover it. Discovery needs FCC-hh, where σ ≈ 2 pb at 1.7 TeV (Pass 12692). B's y′ = 0.51 ± 0.02 is nearly mass-independent, so B survives exclusion by moving the triplet up. Its decisive tests are therefore the micron fifth force and the dark matter, not the LHC.

The soft-lepton tag survives acceptance: 98% of W* leptons have E > 5 GeV in the parent frame (Michel spectrum, endpoint ΔM/2 = 22 GeV).

## (3) Completion A's third-family axion is hard for haloscopes

| PQ-charged fields | E/N | N_DW | g_aγγ / g_KSVZ | haloscope time vs KSVZ |
|---|---|---|---|---|
| one neutral heavy quark (KSVZ) | 0 | 1 | 1 | 1 |
| **t, b only** | 5/3 | **2** | **0.13** | **× 3,300** |
| t, b, τ | 8/3 | 2 | 0.39 | × 44 |

E/N = 5/3 nearly cancels the QCD contribution (1.92), so the photon coupling drops 7.7× and the scan time (∝ g⁻⁴) rises by ~3,300. N_DW = 2 also needs a domain-wall solution in the post-inflationary scenario, such as Lazarides–Shafi or a small explicit breaking. That could shift the lattice m_a window.

> This creates a conflict inside completion A. The flavour-safe charge assignment (Pass 12694) makes the axion nearly invisible to MADMAX/ALPHA-type searches unless leptons are also charged. It also reintroduces a domain-wall problem. The KSVZ version is detectable but leaves flavour to a separate sector.

## (4) A keV-era entropy window

Photon-entropy injection after BBN must avoid:
- D photodisintegration: E_max = m_e²/(22T) < 2.22 MeV, i.e. T ≳ 5.3 keV;
- CMB spectral distortions: z ≳ 2×10⁶, i.e. T ≳ 0.47 keV.

So it is allowed for **T ≈ 5–30 keV**. A 4.8% injection (F = 1.048) lowers the CMB N_eff to 2.86. D/H then shifts by F^(−1.6):

| rates | pull vs Cooke+2018 |
|---|---|
| PRIMAT | +5.8σ (excluded) |
| PArthENoPE | **+1.9σ** (allowed) |

With data-driven d+d rates, a late (5–30 keV) decaying particle could explain the CMB half of the low-N_eff hint. It cannot explain helium, which records N_eff at BBN.

## (5) Forecasts

If N_eff = 2.85, Simons Observatory (σ ≈ 0.05) would see a **3.9σ** deficit and CMB-S4 (σ ≈ 0.03) **6.5σ**. The hint will be settled within the decade.

## (6) Extra: V_ud from the neutron and the Cabibbo-angle anomaly

Inputs: |V_ud|² τ_n(1 + 3g_A²) = 4908.6(1.9) s (Czarnecki–Marciano–Sirlin 2018), g_A from PERKEO III.

| V_ud source | V_ud | first-row sum with V_us(K_l3) | with V_us(K_μ2) |
|---|---|---|---|
| neutron, bottle τ_n | 0.97456(44) | 0.99956 (−0.5σ) | 1.00050 (+0.6σ) |
| neutron, beam τ_n | 0.96889(116) | 0.98854 (−5.1σ) | 0.98949 (−4.6σ) |
| superallowed 0⁺→0⁺ | 0.97373(31) | **0.99794 (−3.1σ)** | — |

> **Result.** The bottle neutron lifetime with PERKEO III's g_A gives a V_ud that **satisfies** first-row CKM unitarity. The ≈ 3σ "Cabibbo-angle anomaly" appears only with the superallowed-nuclear V_ud, which differs from the neutron value by 1.6σ, pointing at the nuclear-structure corrections (δ_NS). The beam lifetime would make unitarity fail at ~5σ, another argument against it (cf. Passes 12691–12692). This continues the pattern: the anomaly sits in one measurement method, not in the SM.

## Net

- **Completion A** now has a coherent but costly flavour structure: third-generation PQ charges plus a ≥ 1.8 TeV PQ-neutral flavon. Its price is a nearly photophobic, N_DW = 2 axion.
- **Completion B** cannot be discovered at the HL-LHC; it is excludable there only to ~2.1 TeV.
- The low-N_eff hint has one surviving partial mechanism (a 5–30 keV entropy injection, CMB half only, PArthENoPE rates). It will be decided by Simons Observatory.
- The Cabibbo-angle anomaly joins the list of method-dependent anomalies.
