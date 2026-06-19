# BT1333 — W33 Exact Syndrome Simulator Specification

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1330 (Threshold Simulation Plan)

---

## 1. Purpose

The threshold simulation study of BT1330 requires a W33 syndrome simulator capable of:
- Sampling exact syndromes under depolarising, measurement, and idling noise.
- Mapping syndromes to corrections via a precomputed lookup table (LUT).
- Recording logical error outcomes for Monte Carlo averaging.

This BT specifies the simulator to a level that enables direct implementation.

---

## 2. Code Data

The W33 `[[33,1,9]]` CSS code is defined by its parity check matrices $H_X, H_Z \in \mathbb{F}_2^{16 \times 33}$, satisfying:
$$
H_X H_Z^T = 0, \quad \mathrm{rank}(H_X) = \mathrm{rank}(H_Z) = 16, \quad k = 33 - 2 \times 16 = 1.
$$

The logical operators are vectors $\bar{X}, \bar{Z} \in \mathbb{F}_2^{33}$ satisfying:
$$
H_Z \bar{X}^T = 0, \quad H_X \bar{Z}^T = 0, \quad \bar{X} \cdot \bar{Z} = 1.
$$

### Required inputs to simulator
- $H_X$: $16 \times 33$ binary matrix
- $H_Z$: $16 \times 33$ binary matrix  
- $\bar{X}$: length-33 binary vector
- $\bar{Z}$: length-33 binary vector

---

## 3. Noise Model Implementation

### 3.1 Depolarising channel

For each qubit $j$ independently, draw $E_j \in \{I, X, Y, Z\}$ with probabilities:
$$
P(I) = 1-p, \quad P(X)=P(Y)=P(Z)=p/3.
$$

Represent the error as a pair $(e_X, e_Z) \in \mathbb{F}_2^{33} \times \mathbb{F}_2^{33}$ where:
- $e_X[j] = 1$ if $E_j \in \{X,Y\}$
- $e_Z[j] = 1$ if $E_j \in \{Y,Z\}$

### 3.2 Syndrome extraction

$$
s_X = H_X e_Z^T \in \mathbb{F}_2^{16}, \quad s_Z = H_Z e_X^T \in \mathbb{F}_2^{16}.
$$

### 3.3 Measurement error

Flip each syndrome bit independently with probability $q_m$:
$$
\tilde{s}_X = s_X \oplus m_X, \quad \tilde{s}_Z = s_Z \oplus m_Z,
$$
where $m_X, m_Z \sim \mathrm{Bernoulli}(q_m)^{16}$.

---

## 4. Lookup Table (LUT) Decoder

The LUT decoder precomputes, for each of the $2^{32}$ possible combined syndrome vectors
$$
\tilde{s} = (\tilde{s}_X, \tilde{s}_Z) \in \mathbb{F}_2^{32},
$$
the minimum-weight Pauli correction $\hat{E}(\tilde{s})$.

### 4.1 Precomputation algorithm

```
INITIALISE: table[s] = None for all s in F_2^32
FOR weight w = 0, 1, 2, ..., 9:
  FOR each error E of weight w over 33 qubits:
    s = syndrome(E)
    IF table[s] is None:
      table[s] = E
```

This BFS over error weight fills the table for all correctable syndromes. Total entries: $2^{32} \approx 4.3 \times 10^9$.

**Memory:** $4.3 \times 10^9 \times 8$ bytes (64-bit correction label) $\approx 34$ GB. Acceptable for simulation servers; for embedded use, a heuristic decoder is substituted (see §5).

### 4.2 Decode step

Given syndrome $\tilde{s}$, look up $\hat{E} = \mathrm{table}[\tilde{s}]$. Apply $\hat{E}$ to the error record.

---

## 5. Logical Error Classification

After correction, the residual error is:
$$
R = e \oplus \hat{E}.
$$

A **logical X error** occurs if $R$ anticommutes with $\bar{Z}$:
$$
\ell_X = R_X \cdot \bar{Z} \pmod{2}.
$$
A **logical Z error** occurs if:
$$
\ell_Z = R_Z \cdot \bar{X} \pmod{2}.
$$

The trial is a **logical failure** if $\ell_X = 1$ or $\ell_Z = 1$.

---

## 6. Monte Carlo Loop

```python
failures = 0
for trial in range(N):
    e_X, e_Z = sample_depolarising(p, n=33)
    s_X = H_X @ e_Z % 2
    s_Z = H_Z @ e_X % 2
    s_X ^= sample_measurement_error(q_m, 16)
    s_Z ^= sample_measurement_error(q_m, 16)
    s = pack_bits(s_X, s_Z)  # 32-bit integer
    E_hat_X, E_hat_Z = LUT[s]
    R_X = (e_X ^ E_hat_X)
    R_Z = (e_Z ^ E_hat_Z)
    if (R_X @ Zbar) % 2 or (R_Z @ Xbar) % 2:
        failures += 1
p_L_hat = failures / N
```

---

## 7. Output Format

For each $(p, q_m)$ data point, record:

```csv
p, q_m, N, failures, p_L_hat, p_L_stderr
```

where `p_L_stderr = sqrt(p_L_hat * (1 - p_L_hat) / N)`.

---

## 8. Lite Decoder (Embedded)

For resource-constrained settings where the 34 GB LUT is unavailable, substitute a **greedy peeling decoder**:
- For each stabiliser with syndrome bit 1, identify a minimum-weight Pauli that satisfies it.
- Iterate until all syndrome bits are zero or a contradiction is reached.
- On contradiction, return a random low-weight correction.

The greedy decoder achieves approximately 70% of the LUT decoder's logical error rate at $p < 3\%$.

---

## 9. Validation

The simulator is validated when:
1. At $p = 0$: zero logical failures in $10^6$ trials.
2. At $p = p_{\mathrm{th}}$: empirical $p_L \approx p$ (threshold crossing).
3. Syndrome weight histogram at $p = 0.01$ matches BT1323 prediction: support in $\{3,4,5\}$.

---

**Next:** BT1334 — Superconducting pulse schedule for the BT1328 validation experiment.
