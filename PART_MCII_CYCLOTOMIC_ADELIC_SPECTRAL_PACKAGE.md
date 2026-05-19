# Part MCII - Cyclotomic Adelic Spectral Package

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED ADELIC RECIPROCITY THEOREM

---

## Why this part exists

Part MCI proved that the completed split-prime packet is centered-self-reciprocal
in the variable \(t\). The completed defect Dirichlet package replaces that
single variable by the local spectral coordinates
\[
z_p=p^{-s}.
\]
The natural question is whether the same symmetry survives there.

---

## The theorem

For each split prime \(p\equiv1\pmod3\), define the completed local defect factor
in the spectral coordinate \(z\) by
\[
\widehat D_p(z)=\left(\frac{p-2+z}{p-z}\right)\left(1-\frac1p\right)^{-2(1-z)}.
\]
Then the exact involution is not a reflection in \(s\), but the centered local map
\[
\boxed{z\longmapsto 2-z.}
\]
Under this involution,
\[
\boxed{\widehat D_p(z)\,\widehat D_p(2-z)=1.}
\]
So the right centered variable is
\[
\boxed{u_p=z_p-1=p^{-s}-1,}
\]
and the completed package is odd in \(u_p\), not in \(s\) itself.

For a finite split-prime set \(S\), define the adelic package
\[
\widehat{\mathscr D}_S(\mathbf z)=\prod_{p\in S}\widehat D_p(z_p),
\qquad
\mathbf z=(z_p)_{p\in S}.
\]
Then the global reciprocity is coordinatewise:
\[
\boxed{\widehat{\mathscr D}_S(\mathbf z)\,\widehat{\mathscr D}_S(2-\mathbf z)=1,}
\]
where \(2-\mathbf z\) means \(z_p\mapsto2-z_p\) for every split prime.

---

## Consequence for the diagonal \(s\)-line

On the one-variable diagonal \(z_p=p^{-s}\), the exact involution becomes the
local spectral map
\[
\boxed{\sigma_p(s)=-\log_p(2-p^{-s}).}
\]
So each local factor satisfies
\[
\widehat D_p(s)\,\widehat D_p(\sigma_p(s))=1,
\]
but there is no single prime-independent reflection \(s\mapsto s^\ast\) that
implements the symmetry globally for all \(p\) at once.

That is the structural upgrade:
\[
\boxed{\text{the completed Dirichlet reciprocity is adelic, not diagonal.}}
\]

---

## Numerical profile

For the first split primes and for \(s=1/2\), the local involution gives
machine-precision reciprocity:
\[
\widehat D_7(s)\widehat D_7(\sigma_7(s))=1+O(10^{-15}),
\]
with the same behaviour on the larger verified cutoffs.

---

## What is now exact

1. the completed defect package has the same symmetry as the \(t\)-packet, but in the centered local coordinates \(u_p=p^{-s}-1\);
2. the exact reciprocity is coordinatewise over split primes;
3. the diagonal one-variable Dirichlet package is a restriction of a more natural adelic spectral object.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_adelic_spectral_package.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_adelic_spectral_package.json`
- Result: `PART_MCII_cyclotomic_adelic_spectral_package_results.json`
