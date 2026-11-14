# Full partial transpose excludes zero on the common F8 regulus code

Let rho be a normalized positive operator on the fully symmetric three-copy space of the common four-logical-qubit code. Let H be the averaged weighted Pauli-pair objective from the preceding calculation. Impose X = rho transposed on the first copy positive semidefinite. Identical pure tensor powers are feasible. This requirement implies PPT on the pair marginal and therefore H has nonnegative expectation. [Pair-marginal relaxation](2026-11-14_regulus_three_copy.md) · [Symmetric extension methods](https://arxiv.org/abs/quant-ph/0308032)

Pauli twirling preserves feasibility and the objective. The simultaneous Z operators dephase the total xor of the three computational labels. Simultaneous X operators identify the sixteen remaining blocks by a common translation of the labels. On the symmetric space the xor-zero block is represented in the 51 unnormalized orbit sums used in the previous pass. Complex conjugation also preserves feasibility and the objective, which is real. Averaging with the conjugate permits a real symmetric block with 1,326 free entries.

For a Bell vector labelled by logical Pauli v, the expectation of the first-copy partial transpose of the two-copy marginal is the expectation of P_v tensor P_v divided by 16. If the objective were zero, each of its 99 summands would vanish, since their coefficients are positive and the pair marginal has positive partial transpose. In the full transposed state X this makes the trace on the tensor product of each such Bell line with the third-copy space zero. Positivity then forces X to annihilate that entire tensor product.

The verifier enforces only the kernel equations in total xor zero, using the Bell vector with components proportional to the signs of Z^z on the pairs (t,t xor x), and third-copy label x. It evaluates the output at (a,b,a xor b). Exchanging the last two slots leaves X invariant, so one output per such pair suffices. The script directly checks the indexing against an explicit three-copy partial transpose in dimension four. For the actual logical dimension sixteen the resulting integer matrix has 13,464 rows and 1,326 columns. Its rank modulo 101 is 1,326, which proves full column rank over the reals. Thus a zero-objective twirled block would vanish and could not have trace one.

The feasible set is compact, so the full-cut relaxation has a strictly positive minimum. This proves a strict gap on the common code. The certificate below gives a conservative numerical lower bound. Transfer to the unrestricted five- or six-qubit minima would require additional arguments.

Replay with `py -3 analysis/toe_20261114_regulus_full_ppt.py`.

## Quantitative lower bound

Let c be the vector of upper-triangular block entries and A the integer constraint matrix. Trace normalization gives 16 times the scalar product of the orbit sizes with the diagonal entries of c equal to one. Cauchy–Schwarz gives ||c||² ≥ 1/(16² sum of squared orbit sizes). For a covered Pauli v, the associated column test uses an unnormalized Bell vector of squared norm 16 at one fixed third-copy label. Since X is positive with trace one, X² ≤ X. The squared norm of its image under X is at most its quadratic expectation under X. Summing those quadratic expectations over all third-copy labels gives the pair Pauli expectation. The equations sample a subset of output coordinates, so ||Ac||² is bounded above by the sum of the pair Pauli expectations at the covered labels, and hence by the weighted objective.

The executable certifies AᵀA ≥ (1+margin) I with a rounded integer Cholesky factor and a strictly diagonally dominant integer residual. It verifies bounds for exact integer products and sums in binary64 before using the result. This gives an explicit rational lower bound by combining the preceding inequalities.

The certified dimension-scaled lower bound is 1542413711 / 383729558093824, about 4.01953e−6.
