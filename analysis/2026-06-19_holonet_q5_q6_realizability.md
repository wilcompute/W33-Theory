# Analysis: HoloNet Q5–Q6 Routing and Physical Realizability

**Date:** 2026-06-19  
**Covers:** BT1320–BT1322

---

## Summary

This analysis document accompanies the BT1320–BT1322 proof series, synthesising the key numerical results and open questions arising from the completion of the W33 Photonic HoloNet architecture.

---

## Key Numerical Results

### Routing (BT1320–BT1321)

| Quantity | Value |
|----------|-------|
| Q5 node count | 243 |
| Q5 graph degree | 10-regular |
| Q5 fibre size | 21 nodes |
| Q5 max route length | $\text{diam}(\mathcal{G}_4) + 1$ |
| Q6 node count | 729 |
| Q6 graph degree | 12-regular |
| Phase drift resolution | $\pi/3$ |
| Cross-sector corrections needed | 6 |
| Classical overhead (bits) | 18 |

### Physical Realizability (BT1322)

| Resource | Requirement | Budget | Margin |
|----------|-------------|--------|--------|
| Waveguide crossings | 567 | 10,000 | 94.3% |
| Phase shifters | 252 | 2,000 | 87.4% |
| Optical switches | 210 | 500 | 58.0% |
| Control bits | 18 | 64 | 71.9% |
| Latency (ps) | 432 | 1,000 | 56.8% |
| QEC cycle (μs) | 1.9 | 10 | 81.0% |

All resources comfortably within budget.

---

## Theoretical Observations

1. **Harmonic phase schedule** (BT1321): The choice $\theta_k = \pi k/3$ is not arbitrary — it is the unique schedule making the phase correction group isomorphic to $\mathbb{Z}/6\mathbb{Z}$, which matches the 6-sector structure of the Q6 HoloNet.

2. **Toroidal embedding efficiency** (BT1322): The toroidal heptad structure reduces crossing number from the naive $O(|E|^2/|V|) \approx 6561$ down to 567 — a **10.8× improvement** attributable purely to the W33 algebraic structure.

3. **Latency scaling**: The $\tau_q = \tau_1/q$ recurrence means each higher quadrant is *faster* per hop, not slower. This is a non-obvious but critical property: the HoloNet naturally accelerates at deeper levels.

4. **QEC cycle vs. decoherence**: The 1.9 μs cycle vs. >10 μs decoherence time gives a safety factor of ~5×. For fault-tolerant operation, a safety factor of 3× is generally considered sufficient.

---

## Open Questions

1. **Experimental discriminators vs. Microsoft 4D codes**: What measurable quantity — syndrome weight, logical error rate as a function of physical error rate, or latency — most cleanly distinguishes W33 from the Microsoft 4D construction of BT1297?

2. **Q7 and beyond**: Is there a natural Q7 extension, or does the heptad symmetry impose a hard ceiling at Q6 (since $7 = \#\text{Fano points}$ and the Fano plane is 2-dimensional over $\mathbb{F}_2$)?

3. **Thermal noise model**: The realizability proof assumes 10 K operating temperature. What is the degradation curve to 77 K (liquid nitrogen) and 300 K (room temperature)?

4. **W33 vs. surface code overhead**: At the same logical error rate $p_L = 10^{-6}$, how many physical qubits does W33 require compared to a distance-9 surface code?

---

## Status

The BT1301–BT1322 HoloNet architecture series is **complete**. All sub-problems (architecture, runtime, latency, entropy, optimality, stability, physical budget, toroidal bridge, routing, coherence, realizability) have been resolved.

The theory is ready for experimental validation.
