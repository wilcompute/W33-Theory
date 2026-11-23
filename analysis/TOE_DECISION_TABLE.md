# Decision table: which measurement decides which completion (Claude track, as of Pass 12719)

**Update (Pass 12719):**
- **Top mass:** with M_t = 172.80 ± 0.26 (toponium-corrected, arXiv:2603.28865), μ₀ = 2.5×10¹⁰ GeV and P(absolutely stable) ≈ 10⁻³. y′ drops by about 0.01 for both B′ (≈0.496) and the hybrid (≈0.460).
- **B′:** its dark-dimension radius cannot drive DESI's evolving dark energy; lunar laser ranging excludes that by 38×.
- **Hybrid:** Dimopoulos–Wilczek doublet–triplet splitting conflicts with discrete Goldstone protection; a pseudo-Goldstone-Higgs route (Tavartkiladze 2018) is the candidate fix.

**Not a theory of everything.** This is a map of three candidate completions of the Standard Model built around the zero of the Higgs quartic coupling near 10¹⁰–10¹¹ GeV, and of the experiments that decide between them. It summarises Passes 12684–12718.

## The three completions

| | A | B′ | Hybrid |
|---|---|---|---|
| Idea | intermediate-scale axion (PQ at ~f_a) plus seesaw leptogenesis | micron-to-nanometre dark dimension plus a TeV top partner plus B-mesogenesis | E₆ SUSY at M_SS ~ 10¹⁰ plus TeV vectorlike Q + U as pseudo-Goldstones |
| Dark matter | axion | dark baryon ψ (mesogenesis) | generic (LSP/other) |
| Baryon asymmetry | leptogenesis (MFV tree splittings, 7–9% of space) | B-mesogenesis at T_RH = 6–17 MeV | standard (not specified) |
| Key parameter | f_a, g_aγγ = 0.4–1.7 g_KSVZ | y′ = 0.49–0.51 (flat), R = 0.009–0.2 μm | y′ = 0.45–0.48, falling with M_VL |
| Naturalness issue | none severe | narrow surviving range (λ ∈ [10⁻⁴, 2.3×10⁻³]) | accidental SO(10) protected to dimension 11 (Z₁₀ or brane separation) |
| Evidence vs SM today | 0.03–0.23 | 0.006–0.044 | 0.1–0.75 (if the mechanism holds) |

## The experiments

| measurement | expected timing | A | B′ | Hybrid |
|---|---|---|---|---|
| FCC-ee short-distance m_t (σ ≈ 0.04 GeV) | 2040s | needs λ to cross zero: decided at 18σ | same | same |
| HL-LHC vectorlike-quark search to ≈2 TeV | 2030s | — | discovery possible (≥ 1.74 TeV) | discovery possible |
| Belle II inclusive B → baryon + missing energy (≈10⁻⁷) | 2030s | — | **covers 56–100%** | — |
| Belle II exclusive ψΛ, ψp at 10⁻⁸–10⁻⁹ | 2030s | — | 83–100% | — |
| FCC-hh y′ and M_VL | 2060s | — | y′ = 0.49–0.51, flat in M_VL | y′ ≈ 0.47 − 0.015 per TeV |
| Hyper-K / DUNE proton decay | 2030s | — | — | **no signal** (τ ≈ 4×10³⁶ yr) |
| Haloscopes near 100 μeV (MADMAX, ALPHA) | 2030s | axion at g = 0.4–1.7 g_KSVZ | — | — |
| Short-range gravity, 10–200 nm | — | — | invisible (≥ 10⁸ below reach) | — |
| Simons Observatory N_eff | late 2020s | low-N_eff hint (−2σ) unexplained by all | | |

## Which result kills which model
- **FCC-ee finds the vacuum absolutely stable** (M_t ≤ 170.98 GeV): all three are gone, since the quartic zero they rely on doesn't exist. About 1% likely today.
- **No vectorlike quark below ~6 TeV at FCC-hh:** B′ and the hybrid lose their TeV partner. A survives.
- **A vectorlike quark with y′ ≈ 0.49–0.51 and no M_VL dependence:** B′ is favoured, at a Bayes factor of about 45 against the hybrid. Belle II must then see B → ψ + baryon.
- **A vectorlike quark with y′ falling as 0.47 − 0.015·(M_VL/TeV − 1.74):** the hybrid is favoured (about 45:1).
- **Belle II sees nothing at 10⁻⁸ (inclusive):** B′ is dead.
- **Hyper-K sees proton decay:** the hybrid (τ ≈ 4×10³⁶ yr) is disfavoured.
- **A haloscope finds an axion at 40–180 μeV with g ≈ g_KSVZ:** A is strongly favoured.

## Side track: ternary computing (Passes 12708–12717)

| domain | verdict |
|---|---|
| radix economy (cost ∝ r) | 3 is optimal only for SNR ≳ 9; binary below that |
| on-chip logic energy | binary wins by 2.5× |
| chip-to-chip links | PAM3 optimal in a narrow band (GDDR7, USB4 v2, Thunderbolt 5 ship it) |
| addition / multiplication | carries 3.5× shorter; carry-free signed-digit; multiplier tree 6 vs 8 levels |
| NN weights, memory-bound | on the energy–accuracy front (48 pJ/weight vs 240 for int8) |
| NN weights, weight-stationary digital | ternary wins below 0.073 pJ/bit |
| analog crossbars | not cheaper per operation than binary |
| attention | ternary matches full precision with 50% zeros; binary fails |
| flash / ECC | +61% bits per cell, at the cost of ~6 dB SNR and extra reads |
