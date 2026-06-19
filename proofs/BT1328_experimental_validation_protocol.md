# BT1328 — Experimental Validation Protocol for the W33 Syndrome Discriminator

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1323 (Experimental Discriminators)

---

## 1. Goal

BT1323 identified the sharpest practical discriminator between W33 and Microsoft's 4D toric code family:

> **W33 admits odd syndrome weights {3,5}; 4D toric codes admit only even syndrome weights.**

This BT specifies a hardware-ready experimental protocol to test that claim.

---

## 2. Platform Requirements

A viable platform must support:
- 33 physical qubits
- repeated stabiliser measurement
- programmable single-qubit Pauli noise injection
- readout of the full syndrome vector in one round

### Best-fit near-term platforms

1. **Superconducting transmon array** with tunable couplers  
   Fastest route, best timing control.
2. **Trapped-ion chain of length 33**  
   Highest gate fidelity, slower cycle time.
3. **Photonic cluster emulator**  
   Conceptually aligned with HoloNet, but stabiliser extraction is harder.

**Recommendation:** begin with superconducting transmons.

---

## 3. Preparation Phase

### 3.1 Code state preparation

Prepare the W33 encoded logical state
$$
|\bar{0}\rangle
$$
using the known W33 encoding circuit or stabiliser pumping sequence.

### 3.2 Baseline syndrome calibration

Run $N_0 = 10^4$ shots without injected faults to estimate the background readout-induced syndrome histogram:
$$
P_0(w) = \Pr(\text{syndrome weight} = w \mid \text{no intentional fault}).
$$

This isolates measurement errors from the injected-noise signature.

---

## 4. Fault Injection Phase

For each trial:
1. Sample a random qubit index $j \in \{1,\ldots,33\}$.
2. Sample a Pauli fault $E_j \in \{X_j, Y_j, Z_j\}$ uniformly.
3. Apply the fault.
4. Measure the full stabiliser set.
5. Record the syndrome weight
$$
w = \mathrm{wt}(s).
$$

Repeat for
$$
N = 10^5
$$
shots.

---

## 5. Statistical Decision Rule

Define the observed histogram
$$
\hat{P}(w) = \frac{1}{N}\#\{\text{shots with syndrome weight } w\}.
$$

### W33 hypothesis
Expected support:
$$
\mathrm{supp}(\hat{P}) \subseteq \{3,4,5\}
$$
with nonzero mass on at least one odd weight:
$$
\hat{P}(3) + \hat{P}(5) > 0.
$$

### 4D toric hypothesis
Expected support:
$$
\mathrm{supp}(\hat{P}) \subseteq \{2,4,6,8\}
$$
so
$$
\hat{P}(3) = \hat{P}(5) = 0.
$$

### Binary test
Reject the 4D hypothesis if:
$$
N\big(\hat{P}(3)+\hat{P}(5)\big) \ge 20.
$$

The threshold 20 gives strong separation from readout outliers when $N=10^5$.

---

## 6. Robustness to Measurement Error

Let the per-stabiliser measurement error probability be $q_m$. For 32 stabilisers, the expected spurious syndrome weight is:
$$
\mathbb{E}[w_{\text{spur}}] = 32 q_m.
$$

At realistic superconducting readout levels $q_m \sim 10^{-3}$:
$$
\mathbb{E}[w_{\text{spur}}] = 0.032,
$$
far below the odd-weight signal from intentional faults. Thus odd weights 3 and 5 remain highly visible above calibration background.

---

## 7. Secondary Measurements

To strengthen the case, run two supplementary analyses:

### 7.1 Latency benchmark
Measure decoder time from syndrome acquisition to correction proposal.
- W33 target: < 1 ns LUT decision.
- 4D toric benchmark: 50–300 ns MWPM.

### 7.2 Multi-fault exponent fit
Inject depolarising noise at rates
$$
p \in \{10^{-2}, 10^{-3}, 10^{-4}\}
$$
and fit the logical error exponent:
- W33: exponent near 9.
- 4D toric (small instance): exponent near 8.

---

## 8. Success Criteria

The experiment is considered successful if:
1. Odd syndrome weights are observed significantly above calibration background.
2. The histogram support matches 
   $$
   \{3,4,5\}
   $$
   rather than the even-only 4D pattern.
3. Decoder latency is at least an order of magnitude below MWPM benchmark latency.

---

## 9. Deliverables

A complete validation package should contain:
- syndrome weight histograms
- calibration subtraction analysis
- latency histogram
- logical error exponent fit
- reproducible control sequence / pulse schedule

---

## 10. Status

This protocol is hardware-ready in outline. The next step is to instantiate it on a specific superconducting or trapped-ion platform.

**Next:** BT1329 — 300 K amplification protocol.
