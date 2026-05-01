# Part LXXXIV — Chiral Exact-Sequence Factorization

**Status:** theorem-grade structural extension  
**Date:** April 27, 2026

Part LXXXIII produced the nilpotent supercharge

\[
Q=\frac{\mathcal D+J}{2},
\qquad
Q^*=\frac{\mathcal D-J}{2}.
\]

This part identifies the exact support of \(Q\).

## 1. Chiral projectors

Let

\[
P_+=\frac{P_0+\Gamma}{2},
\qquad
P_-=\frac{P_0-\Gamma}{2}.
\]

Then

\[
\boxed{QQ^*=P_+,}
\]

and

\[
\boxed{Q^*Q=P_-.}
\]

So \(Q\) is a unitary partial isometry from the 59-dimensional negative-chirality sector to the 59-dimensional positive-chirality sector.

## 2. Chiral decomposition

The positive chirality is

\[
\boxed{P_+=L_{15}+L_{24}+S_{20}.}
\]

The negative chirality is

\[
\boxed{P_-=S_{15}+Q_{24}+Q_{20}.}
\]

Both have dimension

\[
\boxed{15+24+20=59.}
\]

The harmonic sector is

\[
\boxed{1_L+1_S+1_Q=3.}
\]

Thus

\[
\boxed{121=59_+ + 59_- + 3_{\mathrm{harm}}.}
\]

## 3. Exact two-term complexes

The supercharge has only three nonzero forward blocks:

\[
\boxed{S_{15}\to L_{15},}
\]

\[
\boxed{Q_{24}\to L_{24},}
\]

\[
\boxed{Q_{20}\to S_{20}.}
\]

Equivalently,

\[
\boxed{
Q
=

Q_{S15\to L15}
\oplus
Q_{Q24\to L24}
\oplus
Q_{Q20\to S20}.
}
\]

Each block is an exact isometry on its sector.

So the completed W(3,3) Hodge complex is the direct sum of three two-term exact complexes plus the three harmonic mean modes.

## 4. Meaning

The nilpotent differential is not a black-box \(121\times121\) operator. It has a clean acyclic orientation:

\[
\boxed{
S_{15}\to L_{15},
\qquad
Q_{24}\to L_{24},
\qquad
Q_{20}\to S_{20}.
}
\]

The only cohomology is the three module means.

This is the finite exact-sequence form of the W(3,3) carrier.

## 5. Structural slogan

\[
\boxed{
\text{The W(3,3) Hodge carrier is three exact two-term complexes plus three harmonic means.}
}
\]

The exact part has dimension

\[
\boxed{2(15+24+20)=118,}
\]

and the harmonic/cohomology part has dimension

\[
\boxed{3.}
\]

## Audit Implementation

Executable surface:

- scripts/w33_chiral_exact_sequence_audit.py
- tests/test_w33_chiral_exact_sequence_audit.py
