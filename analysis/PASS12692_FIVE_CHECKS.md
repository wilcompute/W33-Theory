# Pass 12692: five checks — EW fits can't decide α; KM3NeT at the joint flux is a 2.2σ fluctuation; an axiflavon in completion A needs |C_sd| < 0.09; the B triplet gives ~13,000 HL-LHC pairs; helium and ACT both prefer N_eff ≈ 2.85

Claude track. Follows Passes 12690–12691. **Not a theory of everything.** Script: `toe_pass12692_five_checks.py`; certificate: `data/toe_pass12692_five_checks.json`. Uses the CT18NNLO PDF set through the `parton` reader, from the public LHAPDF server.

## (1) Electroweak fits cannot tell Cs-α from Rb-α

- The relative difference between the two α determinations is 1.2×10⁻⁹.
- The hadronic Δα(M_Z) uncertainty is ~10⁻⁴, about 9×10⁴ times larger.
- The induced M_W shift is 2×10⁻⁸ GeV.

The Cs/Rb split can be settled only by atom-interferometry systematics, or by electron g−2 itself, which sides with Rb (Pass 12691).

## (2) KM3-230213A at the joint-fit flux

- The joint KM3NeT + IceCube + Auger fit gives E²Φ = 7.5×10⁻¹⁰ GeV cm⁻² s⁻¹ sr⁻¹. At that flux KM3NeT expects 0.013 events, so P(≥1) = 1.3%: **2.2σ**. This is consistent with IceCube's own 2.9σ joint-livetime statement once trials and spectrum choices are allowed for.
- The joint-fit flux sits between cosmogenic expectations for mixed-composition UHECRs (~10⁻¹¹–10⁻¹⁰) and proton-rich ones (~10⁻⁹–10⁻⁸); these are literature ranges.
- Reading: either an upward fluctuation of a mostly-mixed UHECR sky, or a transient. No new physics is required by the numbers.

## (3) Completion A with flavour from the PQ field (axiflavon / flaxion type): |C_sd| < 0.09

BR(K⁺ → π⁺a) = m_K³|C_sd|²(1 − m_π²/m_K²)³/(16π f_a² Γ_K). The NA62-based bound is f_a/|C_sd| > 1.1×10¹² GeV ([Toni 2025, 2503.05865](https://arxiv.org/abs/2503.05865)).

| \|C_sd\| | BR at f_a = 10¹¹ GeV | f_a bound | m_a bound |
|---|---|---|---|
| 1 | 3.5×10⁻⁹ | > 1.1×10¹² | < 5 μeV |
| 0.22 (Cabibbo-size) | 1.7×10⁻¹⁰ | > 2.4×10¹¹ | < 24 μeV |
| 0.05 | 8.8×10⁻¹² | > 5.5×10¹⁰ | < 104 μeV |

> **Result.** Completion A's lattice axion window (f_a ≈ 10¹¹ GeV, m_a = 45–65 μeV) is compatible with a flavour-from-PQ sector only if the axion's s–d coupling is **|C_sd| < 0.09**. A generic Cabibbo-size coupling (0.22) is excluded: it would push m_a below 24 μeV, out of the lattice window. Either the first two down-type generations carry equal PQ charge, or flavour comes from a separate sector. NA62's 2025–26 data will tighten this.

## (4) Completion B's triplet: rates and decay regimes

Method: LO QCD pair production (Combridge partonic cross sections) folded with CT18NNLO, μ = M. The validation σ_LO(tt̄, 13 TeV) = 491 pb gives K = 832/491 = 1.70; K is capped at 1.6 for heavy states.

| √s | M = 1.60 | 1.65 | 1.70 | 2.00 TeV |
|---|---|---|---|---|
| 13.6 TeV | 1.6 fb | 1.2 fb | 0.92 fb | 0.19 fb |
| 14 TeV | 1.9 fb | 1.45 fb | 1.1 fb | 0.24 fb |
| 100 TeV | 2.8 pb | 2.4 pb | 2.1 pb | 0.94 pb |

These are per state. **HL-LHC (3 ab⁻¹) gives ≈ 13,000 triplet pairs at 1.65 TeV.** FCC-hh gives millions, enough to measure the 89 GeV T–T′ splitting and hence y′.

**Decay regimes.** The internal transitions (B → T W*, T′ → B W*, ΔM ≈ 44 GeV) have Γ ≈ 1.8×10⁻⁵ GeV. Mixing-induced decays to SM quarks have Γ ≈ M³θ²/(16πv²). The cascades dominate for SM mixing **θ < 1.1×10⁻⁴**, giving soft-lepton or soft-jet "compressed" signatures that standard VLQ searches (which assume prompt decays to Wb, Zt, ht) do not cover. For larger θ the standard limits (1.49–1.6 TeV) apply.

## (5) Neutron lifetime vs helium — and a low-N_eff coincidence

Y_p(τ_n) uses d ln Y_p/d ln τ_n = 0.73, around Y_p = 0.2470 at τ_n = 879.4 s.

| τ_n | Y_p | Aver+21 | Hsyu+20 | Kurichin+21 | EMPRESS 22 |
|---|---|---|---|---|---|
| bottle 877.8 | 0.2467 | −0.4σ | −0.8σ | −0.2σ | −2.8σ |
| beam 888.1 | 0.2488 | −1.0σ | −1.3σ | −1.2σ | −3.5σ |

Helium mildly prefers the bottle value (consistent with g_A, Pass 12691) but cannot split them on its own.

**The coincidence.** Fixing τ_n at the bottle value and reading the helium deficit as dark radiation (∂Y_p/∂N_eff ≈ 0.013):

| helium set | Y_p | implied N_eff |
|---|---|---|
| all four | 0.2439 ± 0.0015 | **2.83 ± 0.12** |
| without EMPRESS | 0.2455 ± 0.0017 | 2.96 ± 0.13 |

ACT DR6's CMB-only value is N_eff = 2.86 ± 0.13. With all four helium sets, the two probes agree almost exactly, and their combination 2.84 ± 0.09 sits ≈ 2.3σ below the SM's 3.044. The helium side rests on EMPRESS: without it the hint drops to ≈ 0.6σ.

> **Status: a hint, not a result.** Helium (if EMPRESS holds) and the CMB damping tail independently prefer N_eff ≈ 2.85. A deficit of ~0.2 would point to non-standard neutrino decoupling: a low reheating temperature of a few MeV, neutrino–dark-sector interactions, or late entropy injection. The low-reheating option is incompatible with completion A (T_RH ≳ 10¹¹ GeV) and with completion B as formulated (T_i ~ GeV, which is too high to reduce N_eff). It would therefore be a third direction, not a confirmation of either. The decisive inputs are the next helium surveys and Simons Observatory / CMB-S4 N_eff (σ ≈ 0.03–0.05).
