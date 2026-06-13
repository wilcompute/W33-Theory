# BT925 — Canonical mod-2 form on the homology

**Status: PARTIAL — canonical mod-2 bilinear form pinned; positive-definite integral lift still open.**

BT924 pinned the \(E_8\) rank and 2-adic location over \(\mathbb Z\). BT925 adds the canonical mod-2 bilinear form on

\[
H=\ker(A_2)/\operatorname{im}(A_2).
\]

## Corrected canonical statement

For cycles \(x,y\in\ker(A_2)\), the integer \(x^TAy\) is even, so

\[
B(x,y)=rac{x^TAy}{2}\pmod2
\]

is well-defined. The verifier checks:

- \(B\) descends through boundaries: \(B(\partial,z)=0\).
- \(B\) has rank \(8\) on \(H\).
- \(B\) is alternating: \(B(x,x)=0\) for all \(256\) classes of \(H\).

Thus

\[
oxed{(H,B)\cong E_8/2E_8	ext{ as a rank-8 symplectic } \mathbb F_2	ext{ bilinear space}.}
\]

## Important correction

The edge-parity functional

\[
q(x)=rac{x^TAx}{2}\pmod2
\]

is **not** the quadratic refinement of \(B\). It is linear on cycles and vanishes on \(H\). Equivalently, the Wu class vanishes, which is consistent with an even lattice lift, but it does not distinguish \(E_8\) from the indefinite even unimodular rank-8 form \(II_{4,4}\).

## Sharp residual

No mod-2 or mod-4 invariant can close the integral \(E_8\) lift. The remaining question is archimedean/integral:

\[
oxed{	ext{find the positive-definite even unimodular lift of the canonical rank-8 shadow}.}
\]

## Witness

```text
analysis/bt925_canonical_mod2_e8_form.py
data/bt925_canonical_mod2_e8_form.json
```
