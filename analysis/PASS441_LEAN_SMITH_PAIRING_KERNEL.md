# Pass 441 — Lean formal Smith-pairing kernel

The repository's existing `formal/W33` Mathlib package now compiles the
integral algebraic core of Passes 435 and 440.

The formal source proves, with no `sorry` and no custom axioms:

1. explicit integral left and right witnesses are invertible;
2. the paired block
   \[
   \begin{pmatrix}q(q+1)&1\\0&q(q-1)\end{pmatrix}
   \]
   is carried to `diag(1,q²(q²-1))`;
3. the divisor factorization `q(q+1)q(q-1)=q²(q²-1)`;
4. the residual spectral multiplicity identity;
5. conductor-stratum sum and difference identities;
6. the valuation bookkeeping identity converting low and paired layers into
   the spectral valuation.

The proof is constructive: both matrix inverses are written down and checked.

## Formal boundary

This pass formalizes the integral block and polynomial/multiplicity bookkeeping.
The representation-theoretic central Fourier decomposition producing those
blocks remains the written theorem input from Passes 435 and 440. It is not
hidden behind a Lean axiom.

The source is integrated into the existing `W33` Lean root and uses the
repository's pinned Lean/Mathlib toolchain. CI performs the actual package
build and a no-`sorry` audit.
