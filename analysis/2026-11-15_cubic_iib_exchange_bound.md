# A curvature bound on massive spin-two exchange of cubic-link currents

The [previous Betti calculation](2026-11-15_cubic_iib_betti_sources.md) proved that the six RR gauge fields on the primitive cubic link have nonzero massive neutral spin-two overlaps. The overlap norm alone allowed that weight to sit at arbitrarily high mass. Here a Weitzenböck estimate bounds where that weight can sit and therefore gives a lower bound on the massive spin-two exchange kernel.

## A bound on the first spectral moment

Use the unit AdS and link normalization of the [charged spectrum calculation](2026-11-14_cubic_iib_spectrum_anomalies.md). The Kähler–Einstein base has scalar curvature 24. Rescale the six underlying harmonic anti-self-dual two-forms \(\gamma_i\) to make their averaged Gram matrix the identity. Constant fiber factors can be included in this rescaling. Work with probability volume measure and write \(G_{ij}=\langle\gamma_i,\gamma_j\rangle\). For the orthonormal neutral scalar eigenfunctions \(Y_j\) with squared spin-two masses \(\lambda_j\) in AdS units, use \(C_j=\int G Y_j\) and \(w_j=\|C_j\|_{\rm F}^2\). Set \(T=\sum_{j>0}w_j\) and \(D=\sum_{j>0}\lambda_j w_j\). The previous pointwise rank argument gives \(T\ge6\), with \(D=\int\sum_{i,k}|\nabla G_{ik}|^2\) by Parseval.

For the positive Laplacian convention the Weitzenböck identity gives \(\nabla^*\nabla\gamma=(2W^- -8I)\gamma\). Define the finite positive number \(B=\max_S\lambda_{\max}(2W^- -8I)\) in the curvature-operator convention on two-forms. If it were nonpositive, integrating the identity would force all six forms to be parallel, which conflicts with their local rank bound and integral independence. For a pointwise linear map \(A\) whose columns are the forms, write \(G=A^TA\), and let \(Q_{ij}=\langle\nabla\gamma_i,\nabla\gamma_j\rangle\). The product rule is \(\Delta G=2A^T(2W^- -8I)A-2Q\). The matrices \(G,Q\) are positive semidefinite, and \(A^T(2W^- -8I)A\le BG\). Multiplication by \(G\), trace, and integration give

\[
D\le 2B\int\mathrm{tr}(G^2)=2B(T+6)\le4BT.
\]

Thus the overlap-weighted mean squared mass is at most \(4B\). At least one sourced level has \(m^2L^2\le4B\), and at least half of the total overlap weight lies at \(m^2L^2\le8B\) by the Markov bound. These are statements about the normalized overlaps; obtaining a numerical mass bound needs a curvature bound for the chosen cubic metric. [Four-dimensional harmonic two-form Weitzenböck formula](https://www.kkms.org/kkms/vol03_1/03112.pdf)

## Massive exchange at nonnegative Euclidean spectral parameter

Within the transverse-traceless exchange channel, factor out the common gravitational normalization and the tensor projectors. For an external spectral parameter \(x\ge0\) of the Euclidean AdS tensor kinetic operator, the scalar trace in the symmetric gauge-pair space is \(\mathcal E(x)=\sum_{j>0}w_j/(x+\lambda_j)\). Equivalently the scalar kernel before taking its trace is the sum of rank-one matrices \(C_j\otimes C_j/(x+\lambda_j)\). The massless graviton is omitted from both expressions. Cauchy–Schwarz on the weighted spectral sum and the first-moment estimate imply

\[
\mathcal E(x)\ge\frac{T^2}{D+xT}\ge\frac{6}{x+4B}.
\]

In particular the formal zero-shift inverse-mass moment is at least \(3/(2B)\). Averaging the scalar diagonal source \(u^TC_j u\) over unit gauge directions in six dimensions yields the exchange lower bound \(1/[4(x+4B)]\) for the average, since its squared fourth moment includes \(2\|C_j\|_{\rm F}^2/[6(6+2)]\). The kernel has positive spectral weight and cannot be reproduced exactly by a finite polynomial contact term in this channel. This is a resolvent estimate for massive spin-two exchange. A full four-current correlator would also specify external wavefunctions, boundary conditions, tensor structures, contact terms, and other bulk fields. [Geometric KK spin-two eigenvalues](https://arxiv.org/abs/2104.12773)

Replay the matrix inequalities and exact rational spectral controls with `py -3 analysis/toe_20261115_cubic_iib_exchange_bound.py`.
