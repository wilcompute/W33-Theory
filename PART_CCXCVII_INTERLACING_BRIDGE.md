# Part CCXCVII: Eigenvalue Interlacing in W(3,3)

## Overview

The **Cauchy interlacing theorem** states that for a graph G with adjacency
eigenvalues λ_1 ≥ λ_2 ≥ … ≥ λ_n, any induced subgraph H on m vertices has
eigenvalues μ_1 ≥ … ≥ μ_m satisfying:

$$\lambda_{n-m+i} \leq \mu_i \leq \lambda_i \qquad (i = 1, \ldots, m)$$

For W(3,3) with spectrum {12^1, 2^{24}, (−4)^{15}}, every extremal subgraph
(single vertex, maximum independent set I_{10}, maximum clique K_4) produces
tight arithmetic on SRG and SM constants.

---

## 1. Eigenvalue Layout

The 40 adjacency eigenvalues of W(3,3) in descending order:

| Position | Eigenvalue | Multiplicity |
| --- | --- | --- |
| 1 | 12 (= K) | 1 |
| 2 – 25 | 2 (= R_EIG) | 24 = MULT_R |
| 26 – 40 | −4 (= S_EIG) | 15 = MULT_S |

The split position is **1 + MULT_R = 25 = V − MULT_S**.

---

## 2. Single-Vertex Interlacing

A single vertex has degree 0 inside itself, so μ_1 = 0. Interlacing requires:

$$\lambda_{40} = S\_EIG = -4 \leq 0 \leq K = 12 = \lambda_1 \quad \checkmark$$

---

## 3. Maximum Independent Set I_{10}

Every eigenvalue of an independent set on m = α = 10 vertices equals 0.
Interlacing at position i = 1:

$$\lambda_{31} = S\_EIG = -4 \leq 0 \leq K = 12 = \lambda_1 \quad \checkmark$$

Position 31 falls in the S_EIG block (positions 26–40).

---

## 4. Maximum Clique K_4

A 4-clique K_4 has adjacency eigenvalues {3, −1, −1, −1} (i.e., {ω−1, −1, −1, −1}).
Interlacing at position i = 1 and i = 4:

$$\lambda_{37} = -4 \leq -1 \leq \lambda_4 = 2 \quad \checkmark$$
$$S\_EIG = -4 \leq 3 \leq K = 12 \quad \checkmark$$

| Quantity | Value | Notes |
| --- | --- | --- |
| Clique m | 4 = OMEGA | maximum clique size |
| Largest eigenvalue | 3 = ω − 1 | tight against clique degree |
| λ_37 | −4 = S_EIG | lower bound for μ_4 |
| λ_4 | 2 = R_EIG | upper bound for μ_4 |

---

## 5. Spectral Spread and Product

| Quantity | Formula | Value |
| --- | --- | --- |
| Eigenvalue spread | K − S_EIG | 16 = EW_GAUGE_4² |
| Spectral product | K × \|S_EIG\| | 48 = EDGES / 5 |

The spread 16 equals the Hoffman denominator (Part CCXCVI).

---

## 6. Ramanujan Property

W(3,3) satisfies the **Ramanujan inequality** λ_2 ≤ 2√(k − 1):

$$\lambda_2 = R\_EIG = 2 \leq 2\sqrt{11} \approx 6.63 \quad \checkmark$$

Square check (exact integers): R_EIG² = 4 ≤ 4(K − 1) = 44.

---

## 7. Summary Table

| Property | Value | Notes |
| --- | --- | --- |
| Interlacing upper bound | 12 = K | all μ_1 ≤ K |
| Interlacing lower bound | −4 = S_EIG | all μ_m ≥ S_EIG |
| Split position | 25 = V − MULT_S | R/S eigenvalue boundary |
| Spectral spread | 16 = EW_GAUGE_4² | Hoffman denominator |
| Spectral product K\|S\| | 48 = EDGES/5 | edge-eigenvalue link |
| Ramanujan | True | λ_2² = 4 ≤ 44 = 4(K−1) |
| Checks pass | 27/27 | ✓ |

---

## 8. Connections to Earlier Parts

- **Part CCXCVI** — Hoffman bound: spread K − S_EIG = 16 = Hoffman denominator.
- **Part CCXCV** — Seidel matrix: S_EIG = −4 feeds all lower interlacing bounds.
- **Part CCXCVI** — α = 10, ω = 4: interlacing at positions 31 and 37 exactly.
- **Part CCLXX** — W(3,3) core: SRG parameters (V, K, R_EIG, S_EIG) used throughout.
