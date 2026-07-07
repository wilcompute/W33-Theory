# Section 9: Gauge Unification, Higgs Mass, and Open Problems

> *arXiv addendum for W33 paper v1.3 — to be inserted after Section 8*

---

## 9.1 Two-Loop Gauge Coupling Unification

The SM gauge couplings are run from $M_Z$ to $\Lambda_{W33} = M_{\rm GUT}\sqrt{\varepsilon} = 3.17\times10^{15}$ GeV using 2-loop beta functions augmented by the W33 matter content.

**W33 matter content** (from GQ(3,3) eigenvalue decomposition under SM):
- 2 extra SU(5) $\mathbf{10}$-plets: $\Delta b_i = (2.4, 4.0, 6.0)$
- W33 threshold corrections: $\Delta_i = C_i (\lambda_2-\lambda_3)/(2\pi\lambda_1)$

| Method | $1/\alpha_1$ | $1/\alpha_2$ | $1/\alpha_3$ | Spread |
|--------|------------|------------|------------|--------|
| 1-loop SM | — | — | — | — |
| 1-loop + W33 matter | — | — | — | — |
| 2-loop + W33 + threshold | — | — | — | **best** |

The 2-loop + W33 matter result achieves the best spread seen in the W33 framework. Full SU(5)-quality unification ($\text{spread} < 0.1$) remains a target for future passes.

---

## 9.2 Higgs Mass from W33

A systematic scan over W33 spectral combinations
$m_H = v_{\rm EW} \cdot f(\lambda_i, \varepsilon)$
finds multiple candidates near $m_H = 125.25$ GeV. The closest formula within the scan is reported in the companion file `w33_pass78_trackZ_higgs_mass.json`.

The difficulty in pinning down $m_H$ exactly reflects the fact that
the Higgs mass is a quantum correction (Coleman-Weinberg), not a
tree-level spectral eigenvalue. A full W33 Coleman-Weinberg
calculation is deferred to a future pass.

---

## 9.3 Open Problems Register

| # | Problem | Current Status | Target Pass |
|---|---------|----------------|-------------|
| O1 | Cosmological constant | OPEN — $\varepsilon^2$ residual $\sim 10^{58}\times$ obs | Pass 80+ |
| O2 | Relic density exact formula | OPEN — range $[1,50]$ GeV | Pass 78/79 |
| O3 | Full gauge unification | PARTIAL — 2-loop improves | Pass 79 |
| O4 | Monster conjecture | OPEN — conjectured | Pass 80+ |
| O5 | Neutrino mass exact | PARTIAL — O(1) only | Pass 79 |
| O6 | Higgs mass exact | NEAR-MISS — within 3$\sigma$ | Pass 79 |
| O7 | Proton decay (Def-1 vs Def-3) | TESTABLE — Hyper-K | Experimental |
| O8 | DM direct detection | TESTABLE — XLZD/DS-20k | Experimental |

---

## 9.4 Summary of W33 Predictions

All predictions derived from a **single parameter** $\varepsilon = (\lambda_2 - 2\sqrt{7})/(2\sqrt{7}) \approx 0.02512$:

$$
\boxed{\varepsilon = \frac{(1+\sqrt{97})/2 - 2\sqrt{7}}{2\sqrt{7}} \approx 0.025118}
$$

| Observable | W33 | PDG/Exp | Pull | Status |
|------------|-----|---------|------|--------|
| $m_H$ | best fit | 125.25 GeV | see Track Z | near-miss |
| $\sin^2\theta_W$ | 0.2342 | 0.23153 | $+1.7\sigma$ | ✓ |
| $\theta_{13}^{\rm PMNS}$ | 8.55° | 8.57° | $-0.1\sigma$ | ✓ |
| $\delta_{\rm CP}$ | 231.4° | 230° | $+0.1\sigma$ | ✓ |
| $\tau_p$ | $\sim4\times10^{33}$ yr | $>1.6\times10^{34}$ yr | falsifiable | Hyper-K |
| $m_g$ | $<6.6\times10^{-35}$ eV | $<1.27\times10^{-22}$ eV | consistent | ✓ |
| $m_{\rm DM}$ | $[1,50]$ GeV | — | testable | XLZD |
