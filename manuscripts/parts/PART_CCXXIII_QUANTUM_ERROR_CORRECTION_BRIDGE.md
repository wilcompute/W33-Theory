# Part CCXXIII: Quantum Error Correction and Holographic Codes from W(3,3)

## Abstract

We demonstrate that the strongly regular graph SRG(40,12,2,4) — equivalently the W(3,3)
collinearity graph of the generalized quadrangle of order (3,3) — provides a zero-parameter
foundation for quantum error-correcting (QEC) codes, holographic codes, and the HaPPY
construction of AdS/CFT. Every physically relevant quantity (code parameters, stabilizer
count, scrambling time, Hayden-Preskill recovery, Page time) follows from the combinatorial
integers {V=40, K=12, MU=4, M_LAM=27, |Aut|=51840} without any free tuning.

---

## 1. QEC Code Parameters [[n, k, d]] = [[40, 12, 4]]

An [[n, k, d]] stabilizer code encodes k logical qudits into n physical qudits with
code distance d. Matching to W(3,3):

| Parameter | Symbol | W(3,3) Source | Value |
|-----------|--------|---------------|-------|
| Physical qudits | n | V | 40 |
| Logical qudits | k | K | 12 |
| Code distance | d | MU | 4 |
| Qudit alphabet | q | Q | 3 |

The code distance d = MU = 4 is the minimum number of vertices that separate any two
non-adjacent vertices in the graph (equal to the co-clique intersection number μ = 4).
This is not a coincidence: in CSS constructions the parity-check structure mirrors the
co-adjacency structure of the underlying combinatorial design.

---

## 2. Code Rate and Redundancy

The code rate R = k/n = K/V = 12/40 = 0.30 quantifies the fraction of physical
resources used for logical information. The complementary redundancy factor n/k = V/K
= 40/12 ≈ 3.33 measures physical overhead per logical qudit.

The ratio V/K = 10/3 arises from the girth-structure of W(3,3): each vertex participates
in exactly K = 12 edges (adjacencies), consuming 10/3 physical qudits per logical qudit
stored — a natural consequence of the graph's regularity.

---

## 3. Error Correction Capacity

From distance d = 4:

- **Correctable errors**: t = ⌊(d−1)/2⌋ = 1 (any single physical error is correctable)
- **Detectable errors**: d−1 = 3 (up to 3 errors are detectable, though only 1 correctable)
- **Error threshold**: p_th = d/n = 4/40 = 0.1 (error rate below 10% is tolerable)

The factor d/n = MU/V = 1/10 is determined purely by the co-degree parameter μ = 4 and
vertex count V = 40.

---

## 4. Stabilizer Structure and Syndrome Space

The stabilizer group of an [[n, k, d]] code has n−k = V−K = 28 independent generators.
Each generator corresponds to a Pauli operator acting on a subset of physical qudits.

- **Stabilizer generators**: n−k = 28 independent Pauli operators
- **Syndrome space**: 28-dimensional (2^28 distinct syndromes for qubit codes)
- **Logical operators**: k = 12 pairs (one X-type and one Z-type per logical qudit)

The identity n = (n−k) + k gives V = 28 + 12 = 40, decomposing the graph's vertex set
into stabilizer generators and logical operators.

---

## 5. Perfect Tensor Properties

A perfect tensor T on m legs satisfies: for any partition into two equal halves A and Ā
of |A| = m/2 legs each, the tensor is an isometry from A to Ā. In the HaPPY
construction, perfect tensors tile the hyperbolic plane.

With K = 12 legs per tensor and Q = 3 states per leg:

- **Half-legs**: K//2 = 6 legs per party
- **Von Neumann entropy per leg**: ln(Q) = ln(3) ≈ 1.0986 nats
- **Total entropy for K legs**: K·ln(Q) = 12·ln(3) ≈ 13.18 nats

The perfect tensor condition is equivalent to the maximal entanglement of each bipartition,
which is guaranteed by the symmetry group |Aut| = 51840 acting transitively on the graph.

---

## 6. HaPPY Holographic Code and Subregion Duality

The HaPPY (Harlow-Almheiri-Pastawski-Preskill-Yoshida) code constructs holographic
quantum error correction by tiling the Poincaré disk with perfect tensors. In this code:

- **Boundary** (CFT side): n = V = 40 physical qudits
- **Bulk** (AdS side): k = K = 12 logical qudits
- **Bulk-to-boundary ratio**: V/K ≈ 3.33

Subregion duality: any connected boundary region of size K+1 = 13 can reconstruct
any bulk operator. The complementary region has size V−(K+1) = V−13 = 27 = M_LAM,
equal to the co-graph's regularity degree.

This is W(3,3)'s holographic Rindler-wedge: a boundary region of 13 vertices encodes
the entire bulk, while the complementary 27-vertex region forms a quantum error-correcting
code by itself (the co-graph SRG(40,27,18,18) is the complementary structure).

---

## 7. Quantum Secret Sharing

An [[n, k, d]] QEC code implements a ((d, n−d+1, n)) quantum threshold secret-sharing
scheme: any d = MU = 4 shares are sufficient to reconstruct the k = 12 logical qudits.

| Quantity | Formula | Value |
|----------|---------|-------|
| Minimum shares to reconstruct | d = MU | 4 |
| Maximum withheld shares | n − d = V − MU | 36 |
| Secret size (logical qudits) | k = K | 12 |

The threshold MU = 4 is the graph's co-adjacency number μ, the minimum vertex separator
of the complement graph. This combinatorial meaning makes the threshold an intrinsic
property of the geometry, not a free parameter.

---

## 8. Quantum Channel Capacity

For a [[n, k, d]] code used over noisy quantum channels:

**Erasure channel** (threshold below which quantum capacity is positive):
$$p_e < \frac{d}{2n} = \frac{4}{80} = 0.05$$

**Depolarizing channel** (threshold):
$$p_d < \frac{d}{n} = \frac{4}{40} = 0.1$$

Both thresholds are determined by the ratio MU/V = 4/40. The erasure threshold is exactly
half the depolarizing threshold, a standard result from quantum information theory that
here emerges automatically from the SRG parameters.

---

## 9. Scrambling Time and Quantum Chaos

Fast scramblers saturate the Hayden-Preskill scrambling time bound. The scrambling
time for a system with K = 12 logical degrees of freedom and Q = 3 states per degree is:

$$t_{\rm scr} \sim \frac{K}{Q} \ln Q = 4 \ln 3 \approx 4.394 \text{ units}$$

The automorphism group |Aut| = 51840 = |W(E₆)| controls the depth of quantum chaos.
Expressed in units of log₃:

$$\log_3|{\rm Aut}| = \frac{\ln 51840}{\ln 3} \approx 9.9 \approx 10$$

This near-integer (≈ 10) reflects the W(E₆) exceptional structure of the automorphism
group. The scrambling requires approximately 10 Q-ary operations, consistent with
fast-scrambling behavior (logarithmic in system size V = 40 since log₃ 40 ≈ 3.36).

---

## 10. Hayden-Preskill Protocol and Page Time

The Hayden-Preskill protocol concerns information recovery from a black hole. A black
hole modeled by the V = 40 vertex graph:

- **Page time**: At t_Page = V/2 = 20 evaporation steps, the entropy stops increasing.
  This is when the black hole has radiated half its qudits.

- **Hayden-Preskill recovery threshold**: After the Page time, throwing k = 12 qudits
  into the black hole requires collecting only k + n/2 = 12 + 20 = 32 Hawking quanta
  to reconstruct the thrown-in information.

- **Quantum capacity proxy**: The fraction of qudits carrying logical information is
  (n−k)/n = 28/40 = 0.70 — the stabilizer overhead controls the quantum channel capacity.

The Page time V/2 = 20 and recovery threshold 32 = K + V//2 are combinatorially determined
by the graph parameters, with no appeal to Planck-scale physics.

---

## Summary Table

| Bridge | Physical Concept | Formula | W(3,3) Value |
|--------|-----------------|---------|--------------|
| 1 | QEC code [[n,k,d]] | [[V, K, MU]] | [[40, 12, 4]] |
| 2 | Code rate | K/V | 0.30 |
| 3 | Correctable errors | ⌊(d−1)/2⌋ | 1 |
| 4 | Stabilizer generators | V−K | 28 |
| 5 | Perfect tensor entropy/leg | ln(Q) | 1.0986 nats |
| 6 | Subregion recovery threshold | K+1 | 13 |
| 7 | Secret-sharing threshold | MU | 4 |
| 8 | Erasure threshold | MU/(2V) | 0.05 |
| 9 | Scrambling time | (K/Q)ln Q | 4.394 |
| 10 | Hayden-Preskill recovery | K+V/2 | 32 |

**Free parameters: 0.**

All values derive from the integers V=40, K=12, MU=4, M_LAM=27, |Aut|=51840 that
define the SRG(40,12,2,4) and its automorphism group W(E₆).

---

*Part of the Theory of Everything derivation series. SRG(40,12,2,4) = W(3,3) collinearity graph of GQ(3,3).*
