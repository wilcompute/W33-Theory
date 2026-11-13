# Pass 12660: a validated F ≥ 0.044 for type B; at q = 8 no stabiliser state is optimal (best stabiliser value 3 against 2.4985); every 9-set found by search is the weak type

Claude track. Follows Pass 12659. **Not a theory of everything.**

## 1. Validated degree-6 bound for type B (`w33_typeB_degree6_margin.py`)

Fix δ₀ = 0.044 (below the SDP optimum 0.04516 of Pass 12658) and maximise the smallest eigenvalue t of both Gram blocks (51 and 136):
- t = 1.5605×10⁻³ (SCS, optimal);
- equality residual 4×10⁻¹³ before, and **4×10⁻¹⁶ after** a least-norm correction of Frobenius norm 7.7×10⁻¹³;
- smallest eigenvalues after correction: 1.56053×10⁻³ and 1.56053×10⁻³.

The correction is nine orders of magnitude below the margin, so the corrected Gram matrices are positive definite and the identity F·|v|² − δ₀·|v|⁶ = SOS holds to machine precision. Hence

> **F ≥ 0.044·|v|⁴ for the F₄ regulus (type B)**, i.e. c ≥ 0.704, by validated floating-point numerics.

This is not an exact rational certificate. It replaces the previous best 0.0244 (Lovász). The true value is 1/16 = 0.0625 numerically. The Gram matrices are saved in `data/w33_typeB_degree6_margin_solution.npz`.

By the quotient lemma (Pass 12659) the bound transfers to nothing new at three qubits, where 1/8 is already exact.

## 2. Stabiliser states are not optimal at q = 8 (`w33_regulus_stabiliser_minimum.py`, `w33_f8_minimiser_structure.py`)

On a stabiliser state of a Lagrangian M, d·F = |M ∩ {Q = 0}|. Simulated annealing over Lagrangians (symplectic transvection moves):

| q | best stabiliser value m* | steps | numerical c_q |
|---|---|---|---|
| 2 | 1 | 1 | 1 |
| 4 | 1 | 21 | 1 |
| 8 | **3** | 2,316,143 (no improvement) | **2.4985** |
| 16 | 1 | 1,908 | 1 |

- For q = 2, 4, 16 a Lagrangian meeting the quadric in a single point is found at once, and c_q = 1 is the stabiliser value.
- For q = 8 the search finds nothing below 3. This is annealing evidence, not an exhaustive count over the 4,922,775 Lagrangians.
- The numerical optimum 2.4985 < 3, so **at q = 8 the minimiser is a genuinely non-stabiliser state**.

**Structure of that minimiser** (Pauli side; d·F recomputed from Pauli expectations agrees to 10⁻¹⁵, a cross-check of the CZ model):
- its Pauli stabiliser has order 4, all non-identity elements uncovered;
- of the 567 covered Paulis only 63 have non-zero expectation, 7 in each of the nine bases, i.e. a subgroup of order 8 in each Lagrangian;
- of the 3,528 uncovered Paulis, 480 are non-zero.

No closed form for 2.498508646688 was found. The minimiser is saved in `data/w33_f8_minimiser.npy`.

## 3. Census of five-qubit 9-sets (`w33_five_qubit_nine_set_census.py`)

Fifteen maximal 9-sets: the Pass 12650 set, the two regulus quotients, ten from the annealed floor-24 states (Pass 12652), and the two returned by the exact-cover search in forward and reversed order.

| source | count | simple eigenvalues | c = 32·min F |
|---|---|---|---|
| search (12650, floor-24, DLX) | 13 | 271 | 1.000000 |
| regulus quotient, type 27 | 1 | 1 | 2.498509 |
| regulus quotient, type 17 | 1 | 1 | 2.498509 |

- **Every set found by search has the same invariants and c = 1.** The two regulus quotients are the only sets seen with c = 2.4985.
- So unstructured search lands on the weak type every time. The strong sets were only found through the F₈ construction.
- Whether the 13 search sets are one Sp(10,2)-orbit was not tested; they agree on the invariants computed.

## 4. c_q ≥ 1 for all even q: not proved

No linear argument can work: the pure-state relations linear in the squared expectations are exactly the quadric sum rules (Pass 12656), and the LP built from them is trivial. The statement stays numerical for q = 4, 8, 16 and proved only for q = 2.

## Open

- c₃₂ (still computing).
- An exhaustive proof that no Lagrangian meets the F₈ quadric in fewer than 3 points.
- Closed form of 2.498508646688; exact 1/16 for type B.
