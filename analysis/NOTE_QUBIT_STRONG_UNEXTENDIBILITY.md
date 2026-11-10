# All five-element sets of unextendible three-qubit Pauli MUBs are strongly unextendible, with an explicit constant

*A note for quantum-information readers. Repository passes 12636–12644; scripts and certificates are in `analysis/` and `data/`.*

## Setting

A set of n-qubit Pauli classes, i.e. maximal commuting sets of 2ⁿ − 1 Pauli operators that are pairwise disjoint, gives mutually unbiased stabiliser bases.
- It is **weakly unextendible** if no further Pauli class is disjoint from all of them. In geometric terms this is a maximal partial spread of the symplectic polar space W(2n − 1, 2).
- It is **strongly unextendible** if no vector at all is unbiased to every basis.

Mandayam, Bandyopadhyay, Grassl and Wootters (arXiv:1302.3709) constructed weakly unextendible sets of d/2 + 1 bases in d = 4 and d = 8. They proved that specific examples are strongly unextendible, using a Gröbner basis computation, and noted that a general proof remained open.

Write F(v) = Σ_e (|⟨e|v⟩|² − |v|²/d)², summed over all basis vectors of the set. Strong unextendibility means min F > 0 on the unit sphere.

## Results

**1. One orbit.** In d = 8 the maximal partial spreads have sizes 5 (24,192 sets) and 9 (960 sets, the complete MUB sets). The 24,192 five-sets form a **single orbit** of Sp(6,2), equivalently of the Clifford group, so strong unextendibility of one implies it for all.

**2. An explicit constant.** For a pure state, Σ over all Paulis of ⟨P⟩² = d − 1. With the twirl identity Σ_{e∈B} |e⟩⟨e|^{⊗2} = (1/d) Σ_{P∈class} P^{⊗2} this gives

F(v) = (1/d)(d − 1 − Σ_{P∈U} ⟨P⟩²) |v|⁴,

where U is the set of Paulis in none of the classes. The uncertainty relation of de Gois, Hansenne and Gühne (PRA 107, 062211 (2023)) bounds the sum by the Lovász number of the anticommutation graph of U. For the five-sets, |U| = 28. The graph is 12-regular with characteristic polynomial

(λ − 12)(λ − 4)(λ + 2)⁵(λ² + 2λ − 4)³(λ³ − 12λ + 8)⁵,

and an exact dual certificate over Q(√5), built in the rank-21 coherent closure of the graph, gives ϑ ≤ 4 + √5. Hence

> **For every five-element weakly unextendible set of three-qubit Pauli MUBs and every v ∈ C⁸,**
> F(v) ≥ (3 − √5)/8 · |v|⁴ = |v|⁴/(4φ²) ≈ 0.0955 |v|⁴.

**3. The true minimum** is 1/8. It is attained by stabiliser states of a Pauli class meeting the covered set in one point. It is certified numerically by a degree-6 sum-of-squares decomposition, with a 120-dimensional symmetric block and a 288-dimensional block of monomials vᵢvⱼv̄ₖ, and residual 10⁻¹¹. An exact certificate for 1/8 is open. Pairwise information cannot reach it, since ϑ > α = 6. A Shor-type relaxation of the pure-state constraints is also vacuous (bound 7): for a convex objective that is being maximised, the lifted variables can exceed the squares they stand for.

**4. Four qubits.** A nine-element (d/2 + 1) set in d = 16 satisfies F ≥ |v|⁴/16 **exactly and tightly** (Pass 12645): ϑ = α = 14, certified by a facially reduced dual over (1/4)Z, where complementary slackness with the three stabiliser optima is imposed and the result checked by exact LDLᵀ. So strongly unextendible Pauli MUB sets of size d/2 + 1 exist in d = 16, with min F = 1/d.

**5. Two qubits.** For the three-element sets, ϑ = α = 2, so min F = 1/4 exactly from the same inequality.

**6. Mirror pairs.** The 24,192 five-sets pair up: each covered set of 35 Paulis belongs to exactly two five-sets, which share no class.
- The two partners have identical second moments: Σ_e p_e² agrees for every state.
- They are separated by third moments: max_v (Σ_L p_e³ − Σ_R p_e³) = 9/16, attained by stabiliser states.
- In d = 8 the partners are Clifford-equivalent.
- In the two-qutrit analogue (d = 9, the 432 five-sets), partners lie in opposite orbits and are exchanged only by antiunitaries. There the witness is 16/27.

## What is not claimed

- No exact proof of the tight value 1/8.
- For d = 16, only one nine-element set is certified (min F = 1/16 exactly). Whether all nine-element sets are equivalent was not computed, and that set has no mirror partner.
- The Lovász equality ϑ = 4 + √5 is numerical; only the upper bound is certified.

## References

- P. Mandayam, S. Bandyopadhyay, M. Grassl, W. K. Wootters, *Unextendible mutually unbiased bases from Pauli classes*, Quantum Inf. Comput. 14 (2014); arXiv:1302.3709.
- C. de Gois, K. Hansenne, O. Gühne, *Uncertainty relations from graph theory*, Phys. Rev. A 107, 062211 (2023); arXiv:2207.02197.
- L. Lovász, *On the Shannon capacity of a graph*, IEEE Trans. Inf. Theory 25 (1979).
