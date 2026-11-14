# Regulus stabilizer parity and an exact six-qubit saddle

[Pass 12662](PASS12662_Q32_CONSTANT_ELEVEN_ODD_K_PATTERN_TORUS_NEGATIVE.md) observed odd covered counts in binary regulus stabilizers and found different numerical behavior near the saved cost-three and cost-eleven states. Both observations can be investigated directly in Pauli coordinates. The count parity holds in every Lagrangian coset. The saved cost-three state has an exact descending curve, despite its positive-semidefinite Hessian.

## Parity in every coset

Write q = 2^k and Q(x,z) = x1 z1 + x2 z2 over F_q. The binary Pauli form is the trace of its polar form. Let M be any binary Lagrangian of dimension 2k and r any label. Restricted to r + M, the component Tr Q is affine linear because its polarization vanishes on M. Complete Tr to a basis of binary linear functionals on F_q. The zero indicator of Q is the product of one affine factor and k-1 factors of degree at most two in 2k binary variables. Its degree is at most 2k-1. Each monomial therefore misses a variable and sums to zero modulo two. This is the binary Chevalley-Warning counting argument.

Every coset contains an even number of Q-zeros, counting the origin when present. On M itself there are an odd number of nonzero covered labels. This proves the observed parity for every k and every Lagrangian. The proof gives a stabilizer lower bound of one. The sharper odd-k stabilizer conjecture involves information beyond this parity. [Chevalley-Warning at the boundary](https://plclark.github.io/PeteLClark/Research/Chevalley_Warning_on_the_Boundary.pdf) · [Kantor's regulus construction](https://pages.uoregon.edu/kantor/PAPERS/maxPartial.pdf)

## Full real tangent Hessian

Let the objective be the sum of squared Hermitian Pauli expectations over the nonzero covered labels C. For a stabilized unit vector psi with Lagrangian M, choose coset representatives r and basis vectors psi_r = P_r psi. Distinct cosets have distinct characters on M, so the psi_r form an orthonormal basis. Use the projective coordinates (psi + sum z_r psi_r) / sqrt(1 + sum |z_r|^2), with r ranging over nontrivial cosets. [Dehaene and De Moor's binary stabilizer representation](https://arxiv.org/abs/quant-ph/0304125)

For r let a count the labels in C intersect M that anticommute with r. Let n0 and n1 count the covered labels in r + M that commute or anticommute with r, respectively. The real and imaginary squared-coordinate coefficients are 4(n0-a) and 4(n1-a). To see this, a Pauli in M acts diagonally in the coset basis. After normalization, its squared expectation contributes -4|z_r|^2 when it anticommutes with r and zero otherwise. A Pauli outside M has a linear expectation only in its own coset coordinate. Its transition amplitude has modulus one and is real or imaginary according to its commutation with P_r, giving the corresponding +4 term. These contributions give the full Hessian with twice the stated quadratic coefficients and no mixed terms.

The saved F8 stabilizer has 32 zero and 94 positive directions. The saved F32 stabilizer has 17 zero and 2029 positive directions. Along an isolated zero direction the objective is constant for the entire normalized two-state curve. In fact, with real t along that direction the exact change is 4(n-a)t^2/(1+t^2)^2, where n is the corresponding coset count. The F32 computation establishes second-order stability and leaves mixed flat-direction variation open.

## Exact F8 descent

The executable builds the saved F8 stabilizer from commuting Pauli projections and constructs a curve with four first-order flat coordinates and three second-order coordinates of positive curvature. In the coset convention of the executable, its first-order directions are -i P257, -i P268, -P274 and +P287 applied to psi. Its second-order correction is (-2 P13 + 2 P19 - P30/2) applied to psi. The normalized six-qubit curve satisfies

    objective(t) - 3 = (-40 t^4 + 320 t^6 + 544 t^8) / (1 + 4 t^2 + (33/4) t^4)^2.

Thus the saved state is a saddle. At t = 1/4 the exact value is 392207/132613, about 2.95753. The [existing common-code witness](2026-11-14_regulus_quotient_witness.md) gives a lower value of about 2.49851. The contribution here is a local analytic mechanism in the unrestricted parent space that explains how descent begins and supplies a test for F32.

Replay with py -3 analysis/toe_20261114_regulus_stabilizer_variation.py.
