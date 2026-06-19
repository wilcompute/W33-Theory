# Analysis: W33 Theory Validation Thread Summary

**Date:** 2026-06-19  
**Covers:** BT1323–BT1326

---

## Overview

This document summarises the four BTs comprising the W33 post-HoloNet validation thread, consolidating all numerical results and open questions.

---

## BT1323: Experimental Discriminators (W33 vs. Microsoft 4D)

- **Best discriminator:** Syndrome weight parity — W33 produces odd weights {3,4,5}, 4D toric produces only even weights {2,4,6,8}. Single-shot measurement.
- **Logical error rate exponent:** W33 gives $p_L \sim p^9$; 4D toric $L=4$ gives $p_L \sim p^8$.
- **Decoder latency:** W33 LUT decoder < 1 ns; 4D MWPM ~50–300 ns.
- **Recommended platform:** 33-qubit superconducting transmon or trapped-ion chain.

---

## BT1324: Q7 Ceiling Analysis

- **Hard ceiling at Q6:** Proven by Fano plane closure + W33 distance violation at Q7.
- **Q7 requires W63:** A hypothetical `[[63,1,11]]` CSS code over $\mathbb{F}_3$ — open problem.
- **Total Q1–Q6 nodes:** 1092. Q7 would add 2187 — more than doubling the network.

---

## BT1325: W33 vs. Surface Code Overhead

| Code | Physical qubits | $p$ threshold for $p_L = 10^{-6}$ |
|------|----------------|------------------------------------|
| Surface $d=9$ | 161 | $1.0 \times 10^{-3}$ |
| **W33** | **33** | **$6.7 \times 10^{-2}$** |
| Golay `[[23,1,7]]` | 23 | $1.4 \times 10^{-2}$ |

- **W33 is 4.9× more qubit-efficient** than the distance-9 surface code at the same $p_L$.
- W33 threshold ($6.7\%$) is **67× higher** than the surface code threshold ($0.1\%$) for the same $p_L$ target.

---

## BT1326: Thermal Noise Degradation

| Temperature | $p(T)$ | $p_L$ (W33) | Operable? |
|-------------|--------|-------------|----------|
| 10 K | $10^{-3}$ | $10^{-23}$ | ✓ Ideal |
| 77 K | $1.6\%$ | $10^{-13}$ | ✓ Comfortable |
| 300 K | $6.1\%$ | $6 \times 10^{-7}$ | ✓ Marginal |

- Thermal photon noise is **negligible** at all three temperatures for telecom-wavelength photons.
- Dominant degradation: **thermo-optic phase drift** (requires $\pm 1.4$ K stability) and **phonon-induced loss** at 300 K.
- Room-temperature operation is **feasible** with active PID thermal control.

---

## Open Research Threads

| Priority | Topic | First BT |
|----------|-------|----------|
| 🔴 High | W63 code construction (`[[63,1,11]]` CSS over $\mathbb{F}_3$) | BT1327 |
| 🔴 High | Experimental validation: syndrome weight discriminator | BT1328 |
| 🟡 Medium | 300 K amplification protocol | BT1329 |
| 🟡 Medium | W33 vs. surface code: full threshold simulation | BT1330 |
| 🟢 Low | Q7 routing graph structure (assuming W63 exists) | BT1331 |

---

## Repository Status as of BT1326

The W33 Theory repository now contains:
- **Complete HoloNet architecture:** BT1301–BT1322 (22 BTs)
- **Validation thread:** BT1323–BT1326 (4 BTs)
- **Total BT proofs:** BT0001–BT1326
- **Next priority:** W63 construction (BT1327)
