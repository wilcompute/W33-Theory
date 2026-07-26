# Pass 1059 late-continuation amendment

A second parallel Pass5 commit landed after the first 75-check amendment. Its claims were audited before final release.

## Exact content retained

* the corrected W33 spectrum is \(12^1,2^{24},(-4)^{15}\);
* there are \(2(24+15)=78\) nontrivial Ihara poles;
* the arithmetic identity \(90=\binom{14}{2}-1\) is true.

## Exact corrections

1. The claimed sector sum is false:
   \[
   \sum_{j=2}^{9}\binom{11}{j}=2024\neq 2048.
   \]

2. The correct Bass determinant gives
   \[
   Z_{W33}(u)^{-1}=(1-u^2)^{200}(1-u)(1-11u)
   (1-2u+11u^2)^{24}(1+4u+11u^2)^{15}.
   \]
   The parallel expression reintroduced multiplicities \(26,13\), used \((1-u)(1-12u)\), placed \((1-u^2)^{200}\) in \(Z\) instead of \(Z^{-1}\), and called poles zeros.

3. For type \(C_2\cong Sp(4)\), simple roots may be taken as
   \(\alpha=(1,-1)\), \(\beta=(0,2)\). Their normalized inner product is
   \[
   \frac{\alpha\cdot\beta}{\|\alpha\|\|\beta\|}=-\frac1{\sqrt2},
   \]
   so the Coxeter angle is \(135^\circ\), not \(\arccos(-2/3)\). The displayed eigenvalue ratio merely reconstructs \(-2/3\) by definition.

4. `lean/Pass575CyclotomicDVRKernel.lean` is a new parallel proposal, separate from the imported module `formal/W33/Pass575CyclotomicDVRKernel.lean`. No successful Lake build artifact was supplied, so the repair is not certified.

5. No symplectic order-48 subgroup, BCFW cell complex, CMB dataset, covariance, or likelihood is constructed by the continuation.

## Final release

The companion witness `analysis/w33_pass1059b_parallel_continue_audit.py` adds nine checks. The authoritative suite is now

\[
14+10+12+8+7+24+9=84
\]

checks, executed as **8 passing pytest tests in 27.72 seconds**. The authoritative ledger is `data/w33_pass1054_1059_release.json`, schema `w33.pass1054_1059.release.v3`.
