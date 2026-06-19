# BT1334 — Superconducting Pulse Schedule for the W33 Syndrome Discriminator Experiment

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1328 (Experimental Validation Protocol)

---

## 1. Platform

Target: a **33-transmon array** with a square-grid coupler topology, operating at $\sim 5$ GHz qubit frequencies and $\sim 15$ mK dilution refrigerator temperature. Representative hardware: IBM or Google superconducting devices scaled to 33 qubits.

---

## 2. Qubit Layout

The 33 data qubits are arranged in a pattern compatible with the W33 stabiliser geometry. The 32 ancilla qubits (one per stabiliser) are interleaved. Total qubit count: **65 physical qubits**.

Layout:
- Data qubits: Q1–Q33
- X-stabiliser ancillae: A1–A16
- Z-stabiliser ancillae: B1–B16

---

## 3. Pulse Sequence Overview

The full experimental sequence comprises four phases:

| Phase | Description | Duration |
|-------|-------------|----------|
| 1. Initialisation | Reset all 65 qubits to $|0\rangle$ | $\sim 2\,\mu\mathrm{s}$ |
| 2. Encoding | Prepare $|\bar{0}\rangle$ via encoding circuit | $\sim 15\,\mu\mathrm{s}$ |
| 3. Fault injection | Apply single Pauli on one data qubit | $\sim 50\,\mathrm{ns}$ |
| 4. Syndrome extraction | Ancilla-mediated stabiliser readout | $\sim 8\,\mu\mathrm{s}$ |

Total per-shot duration: $\sim 25\,\mu\mathrm{s}$.

---

## 4. Encoding Circuit

The W33 $|\bar{0}\rangle$ state is prepared using a **Clifford encoding circuit** of depth approximately 20 CNOT layers. Key steps:

1. Apply Hadamard to data qubits in the X-logical support of $\bar{X}$.
2. Propagate entanglement via CNOT gates along the stabiliser graph, layer by layer.
3. Verify: apply all $Z$-stabiliser ancilla measurements and confirm all outcomes $+1$.

If any Z-stabiliser outcome is $-1$ during verification, re-run encoding.

---

## 5. Fault Injection Pulses

For each trial, select:
- Random data qubit index $j \sim \mathrm{Uniform}(1,33)$
- Random Pauli type $\tau \sim \mathrm{Uniform}(\{X,Y,Z\})$

Apply the corresponding gate:
- $X$: standard $\pi$-pulse on qubit $j$
- $Z$: virtual Z-gate (no physical pulse needed for most architectures)
- $Y$: $\pi$-pulse followed by virtual Z

Pulse duration: $\sim 50\,\mathrm{ns}$ for $X/Y$, instantaneous for $Z$.

---

## 6. Syndrome Extraction Circuit

Stabiliser readout uses a **flag-ancilla circuit** for each stabiliser:

For an $X$-stabiliser $S_i = X^{\otimes \mathrm{supp}(i)}$ with ancilla $A_i$:

```
H(A_i)
CNOT(A_i, Q_{j1})
CNOT(A_i, Q_{j2})
...
CNOT(A_i, Q_{jk})
H(A_i)
Measure(A_i)
```

All 32 stabilisers are extracted in **8 parallel layers** (CNOT scheduling by graph colouring of the stabiliser support graph).

**Readout duration per layer:** $\sim 1\,\mu\mathrm{s}$ CNOT time $+$ reset.

---

## 7. Timing Budget

| Operation | Time |
|-----------|------|
| Single-qubit gate | 20 ns |
| Two-qubit (CNOT) gate | 50 ns |
| Ancilla readout | 500 ns |
| Ancilla reset | 300 ns |
| Encoding circuit (20 CNOT layers) | $\sim 15\,\mu\mathrm{s}$ |
| Syndrome extraction (8 layers) | $\sim 6.4\,\mu\mathrm{s}$ |
| Classical decision (LUT) | $< 1\,\mathrm{ns}$ |
| **Total shot time** | **$\sim 25\,\mu\mathrm{s}$** |

At $10^5$ shots: total experiment time $\approx 2.5\,\mathrm{s}$. Practical in a single session.

---

## 8. Error Budget

Expected noise sources:

| Source | Rate | Impact |
|--------|------|--------|
| CNOT gate error | $0.5\%$ | Primary |
| Single-qubit gate error | $0.05\%$ | Minor |
| Readout error | $0.3\%$ | Secondary |
| Idling $T_1$ decay during encoding | $0.1\%$ | Minor |

Total effective physical error rate: $\sim 0.9\%$, well within the W33 threshold of $6.7\%$.

---

## 9. Classical Data Pipeline

For each shot:
1. Read 32 ancilla outcomes $\to$ syndrome word $s \in \mathbb{F}_2^{32}$.
2. Record syndrome weight $w = \mathrm{wt}(s)$.
3. Append $(j, \tau, w)$ to trial log.
4. After $N$ shots: compute syndrome weight histogram.

No real-time correction is needed for the discriminator experiment — only syndrome weight recording.

---

## 10. Expected Results

| Outcome | Interpretation |
|---------|----------------|
| Histogram support includes $w=3$ or $w=5$ | W33 confirmed |
| Histogram support is subset of $\{2,4,6,8\}$ only | Platform implements a 4D-type code or hardware error |
| Histogram is flat across all weights | Encoding failure — re-run |

---

**Next:** BT1335 — W63 existence decision tree and falsification strategy.
