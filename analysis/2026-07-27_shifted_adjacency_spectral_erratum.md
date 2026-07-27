# Shifted-Adjacency Spectral Audit and Erratum

**Date:** 2026-07-27  
**Scope:** exact finite spectral algebra for the collinearity graph of `W(3,3)`.

## Result

Reconstruct `W(3,3)` directly from the forty projective points of
`PG(3,3)`, joining two distinct points exactly when their symplectic product
vanishes. The resulting adjacency matrix `A` verifies

\[
\operatorname{SRG}(40,12,2,4),
\qquad
\operatorname{spec}(A)=12^1\oplus2^{24}\oplus(-4)^{15}.
\]

Therefore the shifted operator used in the historical “master cubic” section,

\[
D=A-I,
\]

has the exact spectrum

\[
\boxed{\operatorname{spec}(D)=11^1\oplus1^{24}\oplus(-5)^{15}}.
\]

Its minimal and characteristic polynomials are

\[
\boxed{m_D(t)=(t-11)(t-1)(t+5)=t^3-7t^2-49t+55},
\]

\[
\boxed{\chi_D(t)=(t-11)(t-1)^{24}(t+5)^{15}}.
\]

Equivalently,

\[
\boxed{D^3=7D^2+49D-55I}.
\]

## Exact spectral projectors

The three rational projectors are

\[
P_{11}=\frac{(D-I)(D+5I)}{160},
\]

\[
P_1=-\frac{(D-11I)(D+5I)}{60},
\]

\[
P_{-5}=\frac{(D-11I)(D-I)}{96}.
\]

The verifier proves exact idempotence, mutual orthogonality, completeness,
and ranks

\[
\operatorname{rank}(P_{11},P_1,P_{-5})=(1,24,15).
\]

This is the correct three-mode decomposition of the full forty-dimensional
point carrier.

## Determinant and trace tower

The exact determinant-generating polynomial is

\[
\boxed{\det(I-xD)=(1-11x)(1-x)^{24}(1+5x)^{15}}.
\]

The moments are

\[
\boxed{m_n=\operatorname{Tr}(D^n)=11^n+24+15(-5)^n},
\]

and obey

\[
\boxed{m_{n+3}=7m_{n+2}+49m_{n+1}-55m_n}.
\]

In particular,

\[
\operatorname{Tr}D=-40,
\qquad
\operatorname{Tr}D^2=520,
\qquad
\operatorname{Tr}D^3=-520,
\qquad
\det D=-11\cdot5^{15}.
\]

## Historical claim falsified

The earlier proposed annihilator

\[
p_{\rm old}(t)=(t+1)((t+1)^2-36)
=t^3+3t^2-33t-35
\]

does **not** annihilate `D`. On the three true eigenspaces it takes the values

\[
p_{\rm old}(11)=1296,
\qquad
p_{\rm old}(1)=-64,
\qquad
p_{\rm old}(-5)=80.
\]

Thus `p_old(D)` has full rank forty. The accompanying historical roots
`{-1,5,-7}` and multiplicities `{16,10,6}` also sum to only `32`, so they
cannot be the spectrum of a `40 x 40` matrix. Consequently, the determinant,
Taylor-coefficient, octonion, `E8`, and anomaly-cancellation interpretations
constructed from that false polynomial are not spectral properties of
`D=A-I`.

## Positive replacement theorem

The useful replacement is not another numerological coefficient reading. It
is the exact **Shifted-Adjacency Three-Mode Theorem**:

> The point carrier of `W(3,3)` decomposes canonically into the constant,
> `24`-dimensional, and `15`-dimensional adjacency eigenspaces. For
> `D=A-I`, these carry eigenvalues `11`, `1`, and `-5`, with exact rational
> projectors above. Every polynomial propagation on the point carrier reduces
> uniquely to a quadratic in `D`, and every trace moment satisfies the stated
> third-order recurrence.

This theorem is strong enough for exact propagator reduction and regression
checking, while making no unsupported physical inference.

## Reproducibility

Run:

```bash
python analysis/w33_shifted_adjacency_spectral_audit.py
pytest -q tests/test_w33_shifted_adjacency_spectral_audit.py
```

The script rebuilds the geometry rather than trusting a stored adjacency
matrix and writes the machine-readable certificate to
`data/PART_2026_07_27_W33_SHIFTED_ADJACENCY_SPECTRAL_AUDIT.json`.
