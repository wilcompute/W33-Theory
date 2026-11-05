# Passes 12609–12611: haloscopes, GUT thresholds, and the axion-mass ceiling for the PQ-assisted model

Claude track. Continues `PASS12603_12608_PQ_ASSISTED_UNIFICATION.md`. Producer: `analysis/w33_pass12609_to_12611_pq_tests.py`. Test: `tests/test_w33_pass12609_to_12611.py`.

**Not a theory of everything.** These are the three caveats left open last round, each now quantified.

## 12609: current haloscopes do not reach it

`pq_haloscope_check.py`, using the combined haloscope envelope of O'Hare's AxionLimits compilation (github.com/cajohare/AxionLimits). **Controls [N]:** ADMX excludes KSVZ over all of 2.7 to 4 μeV and DFSZ over 53 percent of it; CAPP excludes KSVZ over 87 percent of 4.5 to 5.5 μeV.

| Model A, E/N = 2/3, g = 0.653 g_KSVZ | 25–60 μeV | 60–220 μeV |
|---|---:|---:|
| fraction excluded | 0 | 0 |
| fraction with any limit | 21% | 6% |
| best limit / prediction | 35 | 75 |

The model is untouched today. Its coupling lies above DFSZ, so a search reaching DFSZ across 25 to 60 μeV would decide it.

## 12610: SU(5) thresholds and the proton

`pq_gut_thresholds.py`. Non-SUSY SU(5) with 24_H and 5_H. Model A's light quarks are fragments of vectorlike 5 + 10 + 10, so their partners, the (8,1,0) and (1,3,0) of the 24 and the coloured triplet, sit near M_V. Each heavy mass is drawn log-uniformly within a factor of 3 or 10 of M_V, with linear response around the two-loop solution. **Control:** zero thresholds return the two-loop result.

| | above Super-K, ×3 / ×10 | τ 5–95%, ×10 | above 10³⁵ yr, ×10 |
|---|---:|---:|---:|
| **A** | 76% / 63% | 5×10³³ to 2×10³⁵ yr | 18% |
| B | 1% / 15% | 1.5×10³³ to 4×10³⁴ | 0.5% |
| single (3,2,1/6) | 0% / 0% | up to 1×10³³ | 0% |

So "1 of 85" from Pass 12605 is softer: B survives in 15 percent of wide-threshold draws. The ranking holds. **If Hyper-K sees no p→e⁺π⁰ to about 10³⁵ yr, Model A is excluded in about 80 percent of threshold configurations.** The τ formula is an estimate, accurate to a factor of about 3, and triplet-scalar decay is not included.

## 12611: the axion-mass ceiling depends on the Higgs instability scale

From the stability table of Pass 12607, with y_Q ≤ 1 and the requirement that m_ρ lie below the instability scale μ_I where λ_H turns negative:

| μ_I (GeV) | 10¹⁰ | 3×10¹⁰ | 10¹¹ |
|---|---:|---:|---:|
| m_a ceiling (μeV) | about 28 | about 114 | about 211 |

μ_I depends steeply on the top mass. My one-loop running is not accurate enough to fix it: it crosses near 10⁸, too low compared with published two- and three-loop results near 10¹⁰ to 10¹¹ at M_t ≈ 173 GeV, as I recall them. So the tension with heavy post-inflation simulations noted in Pass 12607 is **undecided**, not established. A precise μ_I(M_t) is needed. The table comes from a coarse grid in f.

## Cross-boundary

Parallel `6fdfcfefb` computed the two-loop single-(3,2,1/6) threshold independently: 2.1189×10⁷ GeV, against 2.1220×10⁷ from `pq_twoloop.py`. The two codes agree to 0.15 percent, a check on both. That commit also prunes by proton decay with an unspecified normalisation K; 12610 gives one specific band.

## Sources

AxionLimits (O'Hare), github.com/cajohare/AxionLimits; arXiv:1705.05370.
