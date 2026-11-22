# Pass 12689: completion B predicts a radius-independent Yukawa y′ = 0.51 ± 0.02 (a ≈ 90 GeV T–T′ splitting); completion A's extra scalar; the A-vs-B prediction matrix

Claude track. Follows Passes 12684–12688. **Not a theory of everything.** Script: `toe_pass12689_completion_matrix.py`; certificate: `data/toe_pass12689_completion_matrix.json`.

## (1) Completion B: y′ barely depends on the radius

Completion B is the dark dimension plus a vectorlike top partner, with λ(M₅) = 0. The running is the 3-loop-QCD-validated running of Passes 12685/12687, with M_t = 172.57 and M_VL = 1.65 TeV (the lightest LHC-allowed mass, Pass 12687).

| R | M₅ (GeV) | y′ needed | graviton-DM T_i | m_KK |
|---|---|---|---|---|
| 0.1 μm | 1.2×10⁹ | 0.494 | ~2.2 GeV | 2.0 eV |
| 0.3 μm | 8.5×10⁸ | 0.500 | ~1.5 GeV | 0.66 eV |
| 1 μm | 5.7×10⁸ | 0.507 | ~1.0 GeV | 0.20 eV |
| 3 μm | 4.0×10⁸ | 0.514 | ~0.7 GeV | 66 meV |
| 10 μm | 2.7×10⁸ | 0.521 | ~0.5 GeV | 20 meV |
| 30 μm | 1.8×10⁸ | 0.529 | ~0.3 GeV | 7 meV |

The radius varies by 300×, but y′ varies only by ±3.5%. M₅ ∝ R^{−1/3}, and the quartic's running near 10⁸–10⁹ GeV is slow, so y′ is set almost entirely by the measured M_t.

> **Prediction (conditional on completion B).** The vectorlike top partner has a Higgs Yukawa **y′ = 0.51 ± 0.02**, nearly independent of the unknown radius. For equal doublet and singlet Dirac masses, the two charge-2/3 states are split by **ΔM ≈ y′v/√2 ≈ 87–92 GeV**. That is a mass splitting a future hadron collider could resolve. Unequal Dirac masses change the splitting but not y′.

The T_i column uses the graviton-dark-matter scaling Ω ∝ T_i³ R / M_Pl, normalised to T_i ≈ 1 GeV at R = 1 μm ([2209.09249](https://arxiv.org/abs/2209.09249)). So in B the reheating stays at the GeV scale over the whole range.

## (2) Completion A: the extra scalar

Pass 12688 showed that ACT's n_s needs positive running of the PQ quartic, b ≈ 0.02–0.04, from a scalar s with κ ~ 3×10⁻⁵ to σ.
- Untuned, s acquires m_s ~ √κ f_a ≈ 5×10⁸ GeV after PQ breaking. That is heavy and harmless; it can decay to Higgs pairs through a small portal.
- KSVZ with a single heavy quark has N_DW = 1, so there is no domain-wall problem.
- The PQ symmetry is broken after inflation, so there is no axion isocurvature. The axion abundance is then set by strings, which is the origin of the lattice window m_a = 45–65 μeV.

## (3) Prediction matrix

| observable | A: SMASH-like intermediate scale | B: dark dimension + VL top partner | test |
|---|---|---|---|
| dark matter | QCD axion, m_a = 45–65 μeV | KK gravitons, keV-ish and drifting | haloscopes (MADMAX, ALPHA, ADMX) vs X-ray / galactic decays |
| new coloured states | KSVZ quark at ~10¹¹ GeV (invisible) | **T, T′, B ≥ 1.65 TeV, y′ = 0.51 ± 0.02, ΔM ≈ 90 GeV** | HL-LHC, FCC-hh |
| short-range gravity | Newtonian | deviation at 1–30 μm | torsion balances |
| reheating | ≳ 10¹¹ GeV | ~0.3–2 GeV | via the DM identity and baryogenesis route |
| baryogenesis | thermal leptogenesis (M_N 10¹⁰–10¹²) | low-scale / non-thermal | 0νββ, leptonic CP |
| r | 0.005–0.007 | model-dependent | Simons Observatory, CMB-S4 |
| N_eff | 3.044 | ≈ 3.044 (non-thermal gravitons) | does not discriminate |
| top mass | 172.4–172.6 predicted | free (absorbed by y′) | FCC-ee threshold scan |

**Discriminators.** A haloscope signal at 45–65 μeV confirms A and kills B, since B has no post-inflationary axion. A torsion-balance deviation at 1–30 μm, or a ≈ 90 GeV-split VLQ triplet, confirms B and kills A. A top mass well outside 172.4–172.6 GeV after FCC-ee kills A's prediction but not B.

## Parallel work since Pass 12688

The other track's 273 commits (2026-11-17 to 22) concern Witting-polytope photonics, H27 representations, W(3,3) gauge-plaquette dynamics and E₆ audits. None touches the intermediate-scale thread.

Its `toe_20261122_e6_h27_chirality_gate.py` (fc0971f0e) is consistent with Pass 12683:
- it gives the 27 → 10 + 5 + 2·5̄ + 2·1 branching;
- it adds a no-go: neither the group nor anomalies select three generations, and an unbroken H27 triplet forces degenerate masses.

That matches Pass 12683's finding that the frame geometry does not select the doublet–triplet split either.
