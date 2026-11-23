# Decision table: which measurement decides which completion (Claude track, as of Pass 12731)

## Snapshot 2026-11-23 (through Pass 12731)

| item | status |
|---|---|
| Inputs | M_t = 172.80 ± 0.26 (toponium-corrected); μ₀ = 2.5×10¹⁰ GeV; SM vacuum 2.7–4.5σ from absolute stability (P = 3×10⁻⁶ to 3×10⁻³) |
| A | strained (12725): with M_t = 172.80, f_a = μ₀ = 2.5×10¹⁰ GeV gives m_a ≈ 230 μeV and an axion that is only 19% of the DM; full DM needs M_t ≈ 172.38 (0.8–1.6σ low); **rescued** by pre-inflation misalignment at θᵢ ≈ 0.992π (1% tuning; Pass 12726), which needs inflation below H_I ≈ 1.4×10⁵ GeV (isocurvature, Pass 12727); generic low-scale inflation then gives n_s 4.7–6.5σ below ACT, so A needs a second tuning (quadratic hilltop) (Pass 12728) |
| B′ | y′ ≈ 0.496 (flat R = 0.009–0.2 μm); dimension must be static today (a DESI-rate radion violates lunar ranging by 38×); Casimir quintessence needs 2×10⁻⁸ tuning at R ≤ 0.2 μm; decisive test is a Belle II inclusive B → baryon + missing-energy search |
| Hybrid | Q + U pseudo-Goldstones (gauged SO(10), 45 + 54 vacuum, anomaly-free Z₁₀); the uncoupled accidental symmetry also leaves a light vectorlike 5 + 5̄ (Higgs doublets + d^c triplets), which **unifies (δ = +0.25)**; open problem: TeV triplets need \|y_qq·y_ql\| ≲ 2×10⁻²⁵ (a symmetry forbidding one coupling); y′ ≈ 0.46 (gauge mediation), falling with M_VL; no proton decay at Hyper-K from dimension 6 |
| Hybrid update (12722) | the light-5 + 5̄ variant is disfavoured: seesaw-induced triplet couplings + proton stability force Σm_ν ≥ 0.08 eV > DESI's 0.064 (minimal flavour), and its y′ (≈0.50) coincides with B′'s; the Q + U-only variant (y′ ≈ 0.46) remains, with doublet–triplet splitting open |
| B′ dark energy (12722) | static radius + uncoupled thawing quintessence: Δχ² = 2.2 better than ΛCDM (DESI full CPL: 6.3) |
| Universal falsifier (12723) | for any quartic-zero completion with one TeV vectorlike family the needed y′ never drops below 0.41 (μ_match 10⁷–10¹³): a measured y′ < 0.41 kills the whole class; with M_t, scheme, α_s and threshold uncertainties the floor is 0.40 (95%: 0.35–0.47), so **y′ < 0.35** is the robust falsifier (Pass 12724) |
| B′ dark sector (12723) | static radius + DM-coupled quintessence (β ≈ 0.1): χ² 2.0 vs ΛCDM 6.3 with phantom crossing; energy flows DM → DE, so the dark baryon cannot be all of the DM; S8: **raised** by 1.3% (linear growth, Pass 12724 corrects 12723's proxy); ψ carries ≤ 80% of the DM; Belle II covers 62–89% by ~2042 |
| Hybrid DT splitting (12723) | orbifold S¹/(Z₂×Z₂′) in the window 10 ≲ M_*R ≲ 100 (KK thresholds narrow it to M_sR ≈ 10–15, Pass 12724) also gives the brane separation that protects the accidental SO(10) |
| B′ dark sector (12725) | coupling only the ≥ 20% second component (β ≈ 0.3) fits DESI (χ² 3.0) with σ8 unchanged (0.995) |
| Hybrid orbifold (12725) | SO(10) parity-class KK thresholds shift α₃⁻¹ by −1.5 already at M_sR = 10: tension with geometric protection; O(1.2–1.5) brane kinetic terms on SU(4) or SU(2)_L would repair it (Pass 12726), but radiative brane terms add a further −1.9, so the repair needs ~4.5× natural size (Pass 12727) |
| Timeline (12728) | parameter space probed — 2032: B′ 44%; 2035: A 60%; 2042: B′ 78%, hybrid 11%; 2045: A 96%; FCC-hh (2070s): B′ and hybrid 100% |
| Orbifold correction (12729) | **orbifold numbers of 12724–12727 withdrawn**; literature formula (Contino–Pilo–Rattazzi–Trincherini) gives +(6/7) ln(ΛR)/2π = +0.31 to +0.63 for ΛR 10–100, the size of the hybrid's mismatch: route reopened |
| A evidence (12729) | tuned-inflation route 0.003–0.026 (below B′); untuned escape with a PQ field of 0.01–0.7 M_Pl during inflation |
| Hybrid orbifold window (12730) | literature threshold cancels the +0.26 mismatch at ΛR ≈ 6.7 (|δ| < 0.1 for 3–14), overlapping protection at ΛR ≥ 9.8: consistent at ΛR ≈ 10–14 (one loop); at two loops |δ| ≤ 0.1 for ΛR ≳ 10 with M₁₂ ≈ 10¹⁷ (Pass 12731); DM: gaugino by freeze-in or axion (a higgsino needs μ ≳ 8e10, Pass 12731) |
| B′ and N_eff (12730) | at most ΔN_eff ≈ −0.06 (T_RH > 5.96 MeV ↔ N_eff > 2.98): does not explain the hint |
| Hybrid vs B′ | FCC-hh with a 3 TeV partner: Bayes factor ≈ 45 either way |
| Ternary | wins: PAM3 links, memory-bound and weight-stationary NN inference, attention (full precision with 45% zeros, with curriculum training), carry-free arithmetic, flash at ~3×10⁴ cycles; loses: on-chip logic energy, analog crossbars, ECC per SNR, qutrit hardware (needs gate error within 1.26× of qubits; transmons 4.5–9×, ions 20–70×) |

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
