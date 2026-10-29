# Passes 12418–12425: one identity, two codes

Claude track. Producer: `analysis/w33_pass12418_to_12425_one_identity_two_codes.py`. Drivers: `analysis/search_drivers_12419/`.

**Cross-track input:** 923c4eb20 (wilcompute), which contributes two things:

- the binary adjacency code [[40,8,6]] with its 240 minimum hexads;
- the correction to the Pass 12410 trace criterion.

## 12418: the correction, accepted

In the split case, a closure solution is a Hodge star iff its ±i eigenspaces are balanced, 3 + 3. The condition tr κ = 0 is an equivalent
shortcut only for characteristic p ≠ 3. Over F₉, κ = i·I has trace 6i = 0 but is not metric. The cross-track has already applied this to
the 12410 document.

The relaxed hypercharge search is complete: 59/59 candidates, no solution.

## 12419: the identity and its two reductions

The collinearity graph of W(3,q) is strongly regular, so its adjacency matrix satisfies

  A² + 2A − (q² − 1)I = (q + 1)J.

A prime is "interesting" for a strongly regular graph when it divides r − s, which here is 2q. These are the primes where p-ranks carry
information beyond the graph's parameters (Brouwer–van Eijl 1992; Brouwer–Van Maldeghem, *p-Ranks*). So the interesting primes are 2 and p.

| prime | reduction | consequence | q = 3 | q = 5 | q = 7 |
|---|---|---|---|---|---|
| 2 | A² ≡ 0 | self-orthogonal → binary CSS code [[q³+q²+q+1, q² − 1, d]]; rank₂ A = q(q²+1)/2 + 1 (in-corpus rank law, Pass 322) | [[40, 8, 6]] | [[156, 24, ≤10]] | [[400, 48, ≤14]] |
| p | (A + I)² ≡ J | every qupit graph-state cut has rank ≤ rank_p(A + I) | 11 | 36 | 85 |

**Why the second ceiling has the value it does.** Mod p, (A + I)_xy = 1 iff y ∈ x^⊥. So A + I is the point–hyperplane incidence matrix of
PG(3,p), with its columns relabelled by the symplectic polarity. Its p-rank is Smith's 1 + C(p + 2, 3) (Smith 1969; in-corpus note
2026-10-22). This matches all three computed values.

## 12420: the ceiling is reached, and it is not holographic

Hill-climbing reaches the ceiling at every q: 11, 36 and 85. Random graphs of the same degree reach n/2 (20, 78, 200).

The ceiling as a fraction of the volume is 0.275, 0.231 and 0.213. It tends to 1/6, since (1 + C(p + 2, 3))/(p³ + p² + p + 1) → 1/6.
So it is a reduced volume law, not an area law.

## 12421: the code distance

The symmetric difference of two intersecting lines has weight 2q, and it is a nontrivial logical operator:

- at q = 3, all 240 such words are logicals, and they are exactly the cross-track minimum hexads;
- at q = 5 and 7, 40 of 40 sampled are logicals.

So d ≤ 2q. Equality is proved at q = 3 by the cross-track's exhaustive search and is a **conjecture** for q ≥ 5.

## 12425: synthesis

The cross-track binary code and this track's ternary entanglement ceiling are the two interesting-prime reductions of a single identity.

The q-dependence comes from classical results:

- rank₂(A), from the rank law;
- rank_p(A + I), from Smith's formula;
- the code dimension, which follows from the rank law.

What is new here:

- the reading of rank_p(A + I) as a graph-state entanglement ceiling;
- the code family for all odd q, together with the d ≤ 2q bound;
- the scaling of the ceiling toward 1/6 of the volume.
