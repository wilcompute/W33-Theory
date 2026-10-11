# Pass 11909: deriving r — the up sector's own loops put the Wilson line at the symmetric point

Producer: `analysis/w33_pass11909_up_sector_coleman_weinberg.py`
Certificate: `data/w33_pass11909_up_sector_coleman_weinberg.json`
Regression: `tests/test_w33_pass11909.py`
Track: Claude.

## Setting

**Texture.** The exact magnetized up texture (Passes 11906–11907) at the hierarchy torus Im τ = 4.209:
* Yukawas y_c(ζ) = 0.94·t_c(ζ);
* masses m_c = y_c v/√2, with v = 246 GeV.

**Potential.** At fixed v the tree potential does not depend on ζ. The Wilson-line potential is therefore the
ζ-dependent part of the up sector's one-loop potential (N_c = 3), in two completions:
* **SM with a hard cutoff Λ:** V = −(3/16π²) Σ_c [2Λ² m_c² + m_c⁴(ln(m_c²/Λ²) − ½)].
* **Supersymmetric:** up squarks of common soft mass m̃, no mixing, MS-bar at the matching (mediation) scale Q:
  V = (3/16π²) Σ_c [S_c²(ln(S_c/Q²) − 3/2) − m_c⁴(ln(m_c²/Q²) − 3/2)], with S_c = m_c² + m̃².

**Expansion in m_c².**
* The coefficient of Σm_c² is 2Λ² (SM) or 2m̃²(1 + ln(Q²/m̃²)) (supersymmetric). In the supersymmetric case the finite
  threshold survives even at Q = m̃.
* The coefficient of Σm_c⁴ is ln(m̃²/m_c²) + O(1).
* In the units of Pass 11907 this gives r ≈ y₀²v²[ln(m̃²/m_t²) + …] / (4m̃²(1 + ln(Q²/m̃²))).

## Results

| completion | vacuum |
|---|---|
| SM, Λ = 0.2, 0.5, 1, 5 TeV | ν = 0 (m_c = m_u) |
| SUSY, standard mediation Q ≥ m̃ (m̃ = 0.3, 1, 3 TeV; Q/m̃ = 1.01–10) | ν = 0 (m_c = m_u) |
| SUSY, e^{−1/2} < Q/m̃ < q_hi(m̃) | hierarchical |

Details of the hierarchical band:

| m̃ | q_hi | band width above e^{−1/2} | width × (m̃/v)² | Q/m̃ giving the observed up ratios |
|---|---|---|---|---|
| 300 GeV | 0.8598 | 0.253 | 0.38 | 0.7706 |
| 1 TeV | 0.6453 | 0.039 | 0.64 | 0.6307 |
| 3 TeV | 0.6127 | 0.0062 | 0.92 | 0.6103 |

At each "observed" Q the vacuum reproduces m_c/m_t = 3.6·10⁻³ and m_u/m_c = 1.7·10⁻³ to 10⁻⁶.

## Reading

**Minimal completions give no hierarchy.** In the minimal completions (SM with a cutoff, or MSSM-like with any mediation
scale at or above the stops), the up sector's own loops put the Wilson line at the symmetric point, so m_c = m_u.

**What the hierarchy needs.** The hierarchical vacuum of Pass 11907 requires the top sector's Wilson-line-dependent
Higgs-mass term to cancel to O(v²/m̃²). In the MSSM parametrisation that happens only for Q ≈ m̃/√e, below standard
mediation. The band shrinks as (v/m̃)², with a slowly growing log.

**So the up-quark hierarchy is tied to the naturalness of the top-sector Higgs mass.** It needs a cancellation the size
of the little hierarchy. A UV completion in which that contribution is finite and cancels (for example
Scherk–Schwarz-type finite Higgs potentials) is the natural place to look; it is not computed here.

## Not established

* Only the up sector's loops are included. Gauge, down-sector and lepton contributions to the ζ potential are not, and
  they could also shift the quadratic coefficient.
* Stop mixing (A-terms) and non-degenerate soft masses are not included.

## Prior art

* Coleman–Weinberg (1973).
* Little hierarchy / MSSM naturalness, e.g. Barbieri–Giudice.
* Corpus: 11904–11907.
