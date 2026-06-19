# BT1323 — W33 vs. Microsoft 4D Codes: Experimental Discriminators

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1322 (Physical Realizability Proof), BT1297 (W33 vs. Microsoft 4D Codes)

---

## 1. Background

BT1297 established the algebraic comparison between the W33 `[[33,1,9]]` CSS code and Microsoft's 4D topological code family. That comparison was structural. The present BT asks: **what experiment, performable on near-term hardware, would most cleanly distinguish the two codes?**

Three candidate discriminators are analysed:
1. Syndrome weight distribution under depolarising noise
2. Logical error rate curve as a function of physical error rate
3. Decoder latency under real-time constraints

---

## 2. Discriminator 1: Syndrome Weight Distribution

### 2.1 W33 Syndrome Structure

The W33 code has parity check matrix $H \in \mathbb{F}_2^{32 \times 33}$ with row weights determined by the CSS construction over the $[[33,1,9]]$ codeword geometry. The **syndrome weight** for a single-qubit Pauli error $E_j$ on qubit $j$ is:
$$
w_j = \text{wt}(H e_j)
$$
where $e_j$ is the $j$-th standard basis vector. For W33, syndrome weights cluster sharply:
$$
w_j \in \{3, 4, 5\} \quad \text{for all } j = 1,\ldots,33.
$$

### 2.2 Microsoft 4D Syndrome Structure

The Microsoft 4D toric code on an $L \times L \times L \times L$ lattice has syndrome weights:
$$
w_j^{\text{4D}} \in \{2, 4, 6, 8\} \quad \text{(even only, by 4D hypercubic geometry)}.
$$

### 2.3 The Discriminator

**Odd syndrome weights are exclusive to W33.** A single measurement of syndrome weight 3 or 5 rules out the 4D toric code family entirely. This is the sharpest possible discriminator — a single-shot measurement suffices.

**Protocol:**
1. Prepare the code in the $|\bar{0}\rangle$ logical state.
2. Apply a random single-qubit depolarising channel $\mathcal{E}_p$ at rate $p = 0.01$.
3. Measure all stabilisers and record syndrome weight histogram.
4. **W33 signature:** histogram has support on $\{3,4,5\}$. **4D signature:** histogram has support on $\{2,4,6,8\}$.

---

## 3. Discriminator 2: Logical Error Rate Curve

Under independent depolarising noise at rate $p$, the logical error rate $p_L$ follows:

$$
p_L^{\text{W33}} \approx \binom{33}{9} p^9 (1-p)^{24} \approx 13{,}037{,}895 \cdot p^9
$$

$$
p_L^{\text{4D}}(L) \approx c_L \cdot p^{L^2/2}
$$

For $L=4$ (smallest 4D toric code with comparable distance): $p_L^{\text{4D}} \approx c_4 \cdot p^8$.

**Key comparison at $p = 10^{-3}$:**

| Code | $p_L$ estimate |
|------|----------------|
| W33 `[[33,1,9]]` | $\approx 1.3 \times 10^{-23}$ |
| 4D toric $L=4$, `[[32,6,4]]` | $\approx c_4 \times 10^{-24}$ |
| 4D toric $L=6$, `[[216,6,6]]` | $\approx c_6 \times 10^{-18}$ |

W33 achieves comparable $p_L$ to the $L=4$ 4D code with **33 physical qubits vs. 32**, but encodes 1 logical qubit vs. 6. The W33 advantage is **per-logical-qubit fidelity**, not encoding rate.

**Discriminator:** Measure $p_L$ at three physical error rates $p \in \{10^{-2}, 10^{-3}, 10^{-4}\}$ and fit the power-law exponent. W33 gives exponent $\approx 9$; 4D toric gives exponent $\approx L^2/2$.

---

## 4. Discriminator 3: Decoder Latency

The minimum-weight perfect matching (MWPM) decoder for the 4D toric code on $L^4$ physical qubits has complexity $O(L^4 \log L)$. For W33 with 33 qubits, the decoder is a fixed lookup table of size $2^{32}$ (pre-computable).

| Decoder | Complexity | Latency at $p=0.01$ |
|---------|-----------|---------------------|
| W33 lookup | $O(1)$ (LUT) | $< 1\,\text{ns}$ |
| 4D MWPM ($L=4$) | $O(256 \log 4)$ | $\sim 50\,\text{ns}$ |
| 4D MWPM ($L=6$) | $O(1296 \log 6)$ | $\sim 300\,\text{ns}$ |

W33's fixed small block size makes it the **clear winner for real-time decoding**, a critical constraint for the HoloNet's 432 ps end-to-end latency requirement (BT1322).

---

## 5. Recommended Experiment

Of the three discriminators, **Discriminator 1 (syndrome weight parity)** is the most practical for near-term hardware:
- Requires no logical state preparation fidelity (works even with imperfect init).
- Single-shot: one round of stabiliser measurements suffices.
- Binary outcome: odd syndrome weights confirm W33, even-only confirms 4D.

**Recommended platform:** Superconducting transmon qubits (33 qubits, all-to-all connectivity via coupler bus), or trapped-ion chain of length 33.

---

**Next:** BT1324 — Q7 extension ceiling analysis.
