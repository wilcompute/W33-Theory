# Pass 12659: regulus constants 1, 1, 2.4985, 1 for q = 2, 4, 8, 16; odd characteristic gives 0 by an explicit quadratic phase; a quotient lemma; certainty-relation form

Claude track. Follows Pass 12658. **Not a theory of everything.**

## 1. The constants c_q = d · min F (`w33_regulus_constants_q16_q32.py`)

Analytic-gradient minimisation in the CZ model of the F_q regulus set (q + 1 bases in dimension d = q²):

| q | qubits | bases | d | c_q = d·min F | starts reaching it |
|---|---|---|---|---|---|
| 2 | 2 | 3 | 4 | 1.000000 | 20 of 20 |
| 4 | 4 | 5 | 16 | 1.000000 | 60 of 60 |
| 8 | 6 | 9 | 64 | **2.498508646688** | 2 of 80 (6+ of 300 in Pass 12658) |
| 16 | 8 | 17 | 256 | 1.000000 | 4 of 60 |
| 32 | 10 | 33 | 1024 | running at commit; see addendum | |

- c₁₆ = 1 to 13 digits; the next level found is 1.387.
- So q = 8 is the outlier so far, not the start of a trend.
- For q = 16 and 32, maximality of the set is Kantor's theorem (arXiv:1601.04194, Thm 5.2) and was not re-verified here.
- These are numerical minima. For q ≥ 8 only a few starts reach the lowest value, so a lower minimum cannot be excluded by this run.

## 2. Why characteristic 2 (`w33_regulus_odd_characteristic.py`)

For an odd prime p the same construction gives p + 1 MUBs of C^p ⊗ C^p, but **min F = 0**:
- the quadratic-phase states A(x₁, x₂) = ω^{a·x₁² + b·x₂²}/p are exactly unbiased to all p + 1 bases whenever ab is a non-residue mod p;
- the number of such (a, b) is 2, 8, 18 for p = 3, 5, 7, i.e. (p − 1)²/2, each with F = 0 to 10⁻¹⁵.

**Mechanism** (line-Fourier form, Pass 12658). F = 0 needs a unimodular function whose restriction to every affine line has a flat Fourier transform. In odd characteristic an anisotropic quadratic phase does this. In characteristic 2 squaring is additive, so every quadratic form on F_q² is degenerate along some direction and the mechanism is unavailable. This is the state-level reason that Kantor's q^k + 1 sets are maximal only for even q.

(At p = 7 the gradient-free optimiser stalled at 0.016; the explicit zeros settle the value.)

## 3. A quotient lemma (proved)

Let p be an antisymmetric Pauli with Tr Q(p) = 1, V₊ its +1 eigenspace, and C̄ the covered set of the quotient set in p⊥/⟨p⟩. For φ ∈ V₊:

> **d·F(φ) = (d/2)·F̄(φ)**, where F̄ is the quotient set's F on V₊ ≅ C^{d/2}.

Proof. Paulis anticommuting with p have zero expectation on φ. Among those commuting with p, each coset {b, b+p} contains at most one covered Pauli, because Tr Q(b+p) = Tr Q(b) + 1 and every covered Pauli has Tr Q = 0; and b, b+p act identically up to sign on V₊. So Σ_C ⟨P⟩² = Σ_C̄ ⟨P̄⟩². ∎

Consequences:
- **d·min F ≤ (d/2)·min F̄**: in units of 1/d the quotient is at least as strong.
- Numerically equality holds for the F₈ regulus and both quotient types (2.498508646688), and for type B → three qubits (1 and 1).
- Any lower bound proved for a regulus set transfers to its quotients.

## 4. Lovász bounds for the quotient sets (`w33_five_qubit_quotient_theta.py`)

| five-qubit quotient | ϑ upper | min F ≥ (float certificate) | numerical min F |
|---|---|---|---|
| type 27 | 30.1119 | 0.0278 | 0.0781 |
| type 17 | 30.1863 | 0.0254 | 0.0781 |

Both beat the 0.0172 of the Pass 12650 set, and both are far from tight.

## 5. Certainty-relation form

F ≥ c/d says Σ_t IC_t ≥ (m + c)/d for the m bases. By convexity of −log, the collision entropies satisfy

Σ_t H₂(B_t) ≤ m·log₂ d − m·log₂(1 + c/m).

| set | m | d | c | entropy deficit (bits) | status of c |
|---|---|---|---|---|---|
| two-qubit triple | 3 | 4 | 1 | 1.245 | proved |
| three-qubit five-set | 5 | 8 | 1 | 1.315 | proved (Pass 12652) |
| type B / F₄ regulus | 5 | 16 | 0.7225 | 0.973 | degree-6 SOS, float |
| type B / F₄ regulus | 5 | 16 | 1 | 1.315 | numerical |
| F₈ regulus and its quotients | 9 | 64, 32 | 2.4985 | 3.181 | numerical |
| F₁₆ regulus | 17 | 256 | 1 | 1.402 | numerical |

**Literature.** Upper bounds on entropy sums are "certainty relations" (Puchała–Rudnicki–Życzkowski, arXiv:1506.07709). The review arXiv:2410.23997 notes they are trivial for extendible MUB sets, because an unbiased vector saturates them. So strongly unextendible sets are exactly the incomplete MUB sets with a non-trivial certainty relation. Mandayam et al. (arXiv:1302.3709) introduced the d/2 + 1 examples; Grassl–McNulty–Mišta–Paterek (arXiv:1611.08962) give non-Pauli triples.

## Open

- c₃₂, and whether c_q = 1 for all q ≠ 8.
- Why q = 8: no closed form for 2.498508646688. The minimiser has eight probability levels, each of multiplicity 8, in every basis.
- Proofs: only q = 2 is proved (c = (d/2)(1 + |⟨ψ|ψ*⟩|²) − 1 ≥ 1).
