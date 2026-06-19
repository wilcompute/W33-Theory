# BT1330 — W33 vs. Surface Code Threshold Simulation Plan

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1325 (Overhead Comparison)

---

## 1. Goal

BT1325 gave an analytic overhead comparison between W33 and the distance-9 surface code. This BT specifies the **simulation program** needed to convert that analytic argument into a numerical threshold study.

---

## 2. Simulation Questions

The study must answer:
1. What is the empirical logical error curve $p_L(p)$ for W33?
2. What is the same curve for rotated surface codes of distances 5, 7, 9?
3. Where do the two curves cross for equal physical qubit budget and equal logical target?
4. What decoder latency penalty appears in the comparison?

---

## 3. Noise Model

Use a uniform depolarising channel:
$$
\mathcal{E}_p(\rho) = (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z).
$$

Supplement with measurement error rate $q_m$ and idling error rate $q_i$:
$$
q_m = q_i = 10^{-3}
$$
for the baseline study, with sensitivity sweeps.

---

## 4. Code Instances

### W33 instance
- One logical qubit
- 33 physical qubits
- distance target 9
- decoder: lookup table / exact syndrome map

### Surface code instances
- rotated distance-5: 49 qubits
- rotated distance-7: 97 qubits
- rotated distance-9: 161 qubits
- decoder: MWPM

---

## 5. Simulation Grid

Run physical error rates:
$$
p \in \{10^{-4}, 3\times 10^{-4}, 10^{-3}, 3\times 10^{-3}, 10^{-2}, 3\times 10^{-2}, 10^{-1}\}
$$
with
$$
N = 10^6
$$
shots per data point for the W33 code and
$$
N = 10^5
$$
shots per data point for each surface code distance.

The lower W33 runtime cost justifies denser sampling.

---

## 6. Outputs

For each code and each $p$ record:
- empirical logical error rate $\hat p_L$
- decoder latency mean and variance
- syndrome weight histogram
- correction success rate conditional on weight

The central plot is:
- **log-log plot** of $p_L$ vs. $p$
- marker for equal-overhead comparison (33 vs. nearest surface-code budget)
- marker for equal-target comparison ($p_L=10^{-6}$)

---

## 7. Expected Regimes

Analytic expectations from BT1325:
- W33 exponent near 9 in low-noise regime
- surface code exponent near $\lfloor (d+1)/2 \rfloor$
- W33 dominant in low-overhead regime
- surface code may recover advantage only in very large-scale lattice limit

---

## 8. Compute Strategy

Recommended software stack:
- stabiliser simulator for W33 exact syndrome sampling
- PyMatching or equivalent for surface-code MWPM
- batch Monte Carlo with fixed random seeds for reproducibility

Recommended outputs in repository:
- CSV tables of all $p, \hat p_L$
- latency summary tables
- notebook/script reproducing plots
- markdown interpretation note

---

## 9. Deliverable Standard

The threshold study is complete only when it contains:
1. raw data tables
2. fitted exponents
3. equal-budget comparison
4. equal-target comparison
5. latency-normalised comparison

---

## 10. Status

This BT defines the simulation protocol. The next implementation step is to build the W33 syndrome simulator and surface-code benchmark harness.

**Next:** BT1331 — Q7 routing graph, conditional on W63 existence.
