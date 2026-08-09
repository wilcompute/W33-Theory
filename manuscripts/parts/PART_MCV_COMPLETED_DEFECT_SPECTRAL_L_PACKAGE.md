# Part MCV: Completed Defect Spectral L-Package

The completed Dirichlet product is already a stable analytic object. But it is even better viewed as a one-parameter spectral family rather than a single frozen point.

## The spectral coordinate

For each split prime $p\equiv1\pmod3$, define
\[
z_p=p^{-s},
\qquad
x_p(s)=\frac{z_p-1}{p-1}.
\]
The quantity $x_p(s)$ is the natural centered spectral coordinate of the split-prime packet.

## The completed spectral family

For deformation parameter $\lambda$, define the local factor
\[
\Lambda_p^{\mathrm{def}}(s;\lambda)
=
\left(\frac{1+\lambda x_p(s)}{1-\lambda x_p(s)}\right)
\exp\!\left(2\lambda\,(p^{-s}-1)\log\!\left(1-\frac1p\right)\right).
\]

Then the finite-cutoff global object is
\[
\Lambda_X^{\mathrm{def}}(s;\lambda)
=
\prod_{\substack{p\le X\\ p\equiv1\ (3)}}
\Lambda_p^{\mathrm{def}}(s;\lambda).
\]

At $\lambda=1$ this recovers the completed defect Dirichlet package:
\[
\Lambda_X^{\mathrm{def}}(s;1)=\widehat D_X(s).
\]
At $\lambda=0$ it is the identity.

## Exact oddness / reciprocity

The deformation variable is exactly odd:
\[
\Lambda_p^{\mathrm{def}}(s;\lambda)
\Lambda_p^{\mathrm{def}}(s;-\lambda)=1,
\]
and therefore
\[
\Lambda_X^{\mathrm{def}}(s;\lambda)
\Lambda_X^{\mathrm{def}}(s;-\lambda)=1.
\]

So the completed package is not just a single analytic value at $\lambda=1$; it is the $\lambda=1$ slice of a global odd spectral family.

## Closed-form logarithm

Its logarithm is again explicit:
\[
\log\Lambda_p^{\mathrm{def}}(s;\lambda)
=
2\operatorname{artanh}\!\bigl(\lambda x_p(s)\bigr)
+2\lambda\,(p^{-s}-1)\log\!\left(1-\frac1p\right).
\]

Thus the entire package is a completed spectral $L$-family built from the same odd split-prime signal that appeared in Parts MCI--MCIII, but now promoted to a two-variable analytic object.

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_defect_spectral_l_package.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_defect_spectral_l_package.json`
- Result: `PART_MCV_completed_defect_spectral_l_package_results.json`
