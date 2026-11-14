# Bell projector for the common four-qubit regulus code

The exact witness for both F8 regulus quotients has a common eigenspace for two independent commuting Pauli operators. Regard that 16-dimensional space as four logical qubits. Covered physical Paulis outside the stabilizer centralizer have zero expectation. Inside it, two physical Paulis in the same stabilizer coset have the same squared expectation. The exact count is 135 surviving physical terms, giving 63 logical terms of weight one and 36 of weight two. [Common quotient witness](2026-11-14_regulus_quotient_witness.md)

For a normalized logical vector Ïˆ, let A be the operator on two copies obtained by summing w(v) P_v tensor P_v over the logical labels. Then the dimension-scaled objective is the expectation of A on Ïˆ tensor Ïˆ. All these two-copy Pauli products commute. In a logical Pauli chart with transpose parity q, the Bell eigenvalue at label u is the integer sum of w(v) times (âˆ’1) to the power q(v)+Ï‰(u,v). The certificate constructs a split quadratic refinement q of the quotient symplectic form and verifies all 256 eigenvalues. They are âˆ’9 with multiplicity 184 and 23 with multiplicity 72. All 72 high Bell vectors are symmetric under exchange of the two copies. In particular, for the rank-72 projector Î  onto those vectors,

    scaled objective = 32 ||Î  (Ïˆ tensor Ïˆ)||Â² âˆ’ 9.

This reduces the lower-bound problem on the common code to a product-vector overlap with one explicit projector. A lower bound for the four-qubit code alone would still need a separate argument to apply to states outside that code.

## Exact test of the two-copy relaxation

Relax Ïˆ tensor Ïˆ to a normalized positive operator supported on the symmetric subspace, with positive partial transpose. Twirling by simultaneous Pauli conjugation preserves these constraints and the objective and makes the operator Bell diagonal. Conversely, a Bell probability vector on symmetric labels with nonnegative partial transpose is a feasible state for this relaxation. The partial-transpose eigenvalues are the sign transform with entries (âˆ’1) raised to q(u+v), divided by 16. This follows by partially transposing a Bell projector, which gives a Pauli conjugate of the swap operator divided by 16. [Peres, Separability criterion](https://doi.org/10.1103/PhysRevLett.77.1413)

The exact integer witness has denominator 3264, total mass one, nonnegative partial-transpose eigenvalues, and objective zero. The verifier checks these properties using integers after recovering the candidate from the floating-point linear program. The original nonnegative Pauli multiplicities form an exact dual certificate. On symmetric Bell labels, their product with the partial-transpose sign matrix equals the objective row. Thus the relaxation optimum is exactly zero and a strictly positive bound requires extra constraints.

Replay with `py -3 analysis/toe_20261114_regulus_bell.py`.
