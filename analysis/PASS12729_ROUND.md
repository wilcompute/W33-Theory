# Pass 12729: the orbifold verdicts of Passes 12724–12727 are withdrawn; the literature formula gives a +0.3 to +0.6 correction, the size of the hybrid's mismatch. A drops below B′ in evidence on the tuned route, but a near-Planck PQ field during inflation offers an untuned escape. B′'s 6–7 MeV reheating partly lowers N_eff. Automatic precision allocation rediscovers the first-layer rule.

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12729_round.py`;
  - `explore_pass12729_alloc.py` (≈20 min);
  - `data/explore_pass12729_orbifold_fix.json`.
- Tests: `tests/test_toe_pass12729.py`, 7 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 7.

## (4) Orbifold thresholds: retraction and the correct formula
**Retracted:**
- the SU(5) and SO(10) tower-sum numbers of Passes 12724–12727 (the "window 10–15", the "overshoot −1.46", the radiative-brane "−1.9");
- my Higgs-universal recomputation earlier in this pass.

**Why:** I mishandled the Higgs zero modes, and the results disagreed in sign with the published analyses.

**The correct formula** (Contino–Pilo–Rattazzi–Trincherini, hep-ph/0108102, eq. 20; consistent with Hall–Nomura, hep-ph/0111068):
- δα_i⁻¹ = +β_i^H ln(ΛR)/2π.
- Here β^H = C(A) − ΣC(r) over the even zero modes, which is (3, 1, −3/5) for SU(3), SU(2), U(1) with the gauge and Higgs-doublet zero modes.
- In the standard combination this is **(6/7) ln(ΛR)/2π**, which lowers α_s. Hall–Nomura find δα_s ≈ −0.010.

**Corrections:** +0.31 (ΛR = 10), +0.46 (30), +0.57 (64), +0.63 (100). The SO(10) orbifold has the same even zero modes, so it takes the same values.

**Status:** this is the same size as the hybrid's +0.26 unification mismatch. **The hybrid's orbifold doublet–triplet route is open again.** Whether it cancels or adds to the mismatch depends on a sign mapping to be done carefully next.

**Method check:** the threshold convention still passes the Hisano–Murayama–Yanagida triplet test (Pass 12728). The error was in the KK bookkeeping, not the convention.

## (1) A without low-scale inflation
- **Mechanism:** with the PQ field at f_I during inflation, the isocurvature bound on H_I rises by f_I/f_a.

| H_I | f_I needed |
|---|---|
| 10¹⁰ GeV | 1.8×10¹⁵ GeV |
| 10¹¹ GeV | 1.8×10¹⁶ GeV |
| 10¹² GeV | 1.8×10¹⁷ GeV (0.07 M_Pl) |
| 10¹³ GeV | 1.8×10¹⁸ GeV (0.73 M_Pl) |

- **An untuned escape:** A can use ordinary higher-scale inflation (no tuned hilltop) if the PQ field sits at 0.01–0.7 M_Pl during inflation.
- **Condition:** the field must then relax to f_a without non-thermal symmetry restoration (parametric resonance), or the post-inflation regime returns.

## (2) A's evidence with ACT (tuned-inflation route)

| SM m_t prior width | A (m_t × Ω × inflation factors) | after 8 trials | B′ (Pass 12709) |
|---|---|---|---|
| 15 GeV | 0.026 (5.51 × 0.082 × 0.058) | 0.003 | 0.044 |
| 5 GeV | 0.009 | 0.001 | 0.015 |
| 2 GeV | 0.003 | 0.0004 | 0.006 |

- **On the tuned route, A now ranks below B′.** The pre-inflation Ω density costs ×0.08, and the hilltop tuning costs ×0.06.
- **On the large-f_I route** the inflation factor is ~1, and A is about 17× higher.
- **Prior art:** Redi–Strumia, "Axion–Higgs unification" (JHEP 11 (2012) 103), already motivates f_a ≈ 10¹¹ GeV from the quartic zero.

## (3) B′'s reheating and the low-N_eff hint
- **Literature:** N_eff < 3 for T_RH ≲ 7 MeV (de Salas et al. 2015); ≈ 3.046 above ~10 MeV (Hasegawa et al. 2019).
- **B′'s window, 5.96–17 MeV, overlaps the edge.** At T_RH ≈ 6–7 MeV, N_eff ≈ 2.9–3.0.
- **Verdict:** B′ can account for part of the ACT + helium hint (≈ 2.85 ± 0.1), but only at the edge of a window whose lower bound comes from the same physics.
- **Novelty:** no paper combining B-mesogenesis with the dark dimension was found, so **B′ appears new**.

## (5) Automatic precision allocation (code, 2 layers, d = 64)
- **Per-matrix ternary cost, measured post hoc** (bits/char):
  - layer 0: MLP-in 0.669, MLP-out 0.548, o 0.490, v 0.438, k 0.181, q 0.107;
  - layer 1: MLP-in 0.397, MLP-out 0.198, v 0.105, o 0.080, k 0.067, q 0.045.
- **The four most sensitive matrices are all in layer 0.** Layer 0's summed cost is 2.43 against 0.89 for layer 1.
- **The greedy allocator agrees:** when the 4 bits/weight budget first allows a full-precision matrix, it picks a layer-0 one (o0).
- **The first-layer rule emerges from the data.**
- **Caveat:** post-hoc costs are not additive when everything is quantised at once (joint 4.1–4.5 bits/char), so quantisation-aware training is still needed.

## Status
- **A:** strained on the tuned route (evidence below B′). There is an untuned escape via a near-Planck PQ field during inflation.
- **B′:** coherent and novel. It may account for part of the low-N_eff hint at T_RH ≈ 6–7 MeV.
- **Hybrid:** the orbifold doublet–triplet route is reopened (literature correction +0.3 to +0.6, the size of its mismatch).
- **Ternary:** automatic allocation recovers the first-layer rule.
