# Pass 179 — Exact Sentinel/Context Poisson Pair

Passes 167 and 175 computed the opening shells of the sentinel parity
lattice and its half-form dual.  Pass 179 fixes the normalization and
separates the exact theorem from a finite numerical check.

Let the binary sentinel code be

\[
S=[40,15,8]_2,
\]

and define two full-rank sublattices of the standard Euclidean
\(\mathbf R^{40}\):

\[
A=\{x\in\mathbf Z^{40}:x\bmod2\in S\},\qquad
B=\{z\in\mathbf Z^{40}:z\bmod2\in S^\perp\}.
\]

## Exact Euclidean dual and covolume

The residue-code dimensions give

\[
[\mathbf Z^{40}:A]=2^{40-15}=2^{25},\qquad
[\mathbf Z^{40}:B]=2^{40-25}=2^{15}.
\]

Every \(2e_i\) lies in \(A\).  Consequently, if \(u\in A^\vee\), then
\(2u=z\in\mathbf Z^{40}\).  Pairing with all residue representatives of
\(S\) says exactly that \(z\bmod2\in S^\perp\).  The converse follows
from the same parity pairing, so

\[
\boxed{A^\vee=\tfrac12 B}.
\]

Its covolume is independently forced by the index:

\[
\operatorname{covol}(A)=2^{25},\qquad
\operatorname{covol}(\tfrac12B)
=2^{-40}2^{15}=2^{-25}.
\]

This also reconciles the two normalizations used in the earlier
passes.  For the half form \(\langle x,y\rangle=x\cdot y/2\), the Gram
determinants are \(2^{10}\) for \(A\) and \(2^{-10}\) for \(B\); for
Euclidean Poisson summation the relevant covolume is \(2^{25}\), not
\(2^{10}\).

## Poisson identity

The standard rank-40 Poisson formula now gives, for every \(t>0\),

\[
\boxed{
\sum_{x\in A}e^{-\pi t\lVert x\rVert^2}
=2^{-25}t^{-20}
\sum_{z\in B}e^{-\pi\lVert z\rVert^2/(4t)}.}
\]

Both the factor \(2^{-25}\) and the argument \(1/(4t)\) are forced:
the former by \(\operatorname{covol}(A)^{-1}\), the latter by
\(A^\vee=(1/2)B\).

## Exact finite algebra and its boundary

The witness recomputes all 41 coefficients of the MacWilliams transform
of the sentinel enumerator.  It checks every division by \(2^{15}\),
nonnegativity, total size \(2^{25}\), and the complete inverse transform
back to the sentinel enumerator (including its zero coefficients).  It
then expands both coordinate-theta products through scaled norm 40.

At \(t=0.45,0.50,0.55\), the two truncated sums agree to floating-point
precision.  Those evaluations corroborate the normalization only.  A
finite shell window cannot prove an infinite theta identity; the exact
proof is the dual-lattice and covolume argument above.

## Reproducibility

- Witness: `analysis/w33_pass179_poisson_modular_pair.py`
- Certificate: `data/w33_pass179_poisson_modular_pair.json`
- Focused test: `tests/test_pass179_poisson_modular_pair.py`

