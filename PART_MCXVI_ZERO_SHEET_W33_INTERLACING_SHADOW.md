# Part MCXVI: Zero-Sheet W(3,3) Interlacing Shadow

**Date:** 2026-05-20
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED PRINCIPAL-SUBMATRIX / INTERLACING SHADOW

---

## Why this part exists

Part MCXV proved that the Hamming/Fano zero sheet has its own Twin-Pell spectral
fingerprint:

\[
\det(xI-A_Z)=x^8-9x^6+17x^4-8x^2.
\]

The remaining question was whether this graph is only abstractly compatible
with W(3,3), or whether it occurs inside the actual W(3,3) point graph.

It occurs inside W(3,3) as an induced 8-vertex principal subgraph.

---

## The theorem

Using the standard symplectic model of W(3,3) on projective points of
\(\mathbb F_3^4\), the zero-sheet graph embeds as an induced subgraph on the
W(3,3) vertex indices

\[
[4,0,8,21,14,22,16,1].
\]

The induced adjacency matrix is exactly the Hamming/Fano zero-sheet adjacency
matrix.

Therefore the zero-sheet eigenvalues are not merely compatible with W(3,3):
they are eigenvalues of an actual \(8\times 8\) principal submatrix of the
W(3,3) adjacency matrix.  Cauchy interlacing applies directly against the full
W(3,3) spectrum

\[
[12,\ 2^{24},\ (-4)^{15}].
\]

The squared nonzero zero-sheet eigenvalues are roots of

\[
f(y)=y^3-9y^2+17y-8.
\]

The exact sign certificate

\[
f(0)=-8,\quad f(1)=1,\quad f(2)=-2,\quad f(6)=-14,\quad f(7)=13
\]

places the squared roots in

\[
(0,1),\quad (1,2),\quad (6,7).
\]

Thus the adjacency eigenvalues lie in

\[
(-\sqrt 7,-\sqrt 6),\quad (-\sqrt2,-1),\quad (-1,0),\quad 0,\quad 0,\quad
(0,1),\quad (1,\sqrt2),\quad (\sqrt6,\sqrt7),
\]

which sits cleanly inside the W(3,3) interlacing window.

---

## Edge Decomposition

The induced shadow also partitions the 240 W(3,3) edges:

\[
240 = 9 + 78 + 153.
\]

Here

\[
9
\]

is the internal zero-sheet edge count,

\[
78 = 6\Phi_3 = \dim(E_6)
\]

is the cut from the zero sheet to its W(3,3) exterior, and

\[
153 = 9\cdot 17 = q^2(q^2+2^q)
\]

is the internal edge count of the complement.

So the same Twin-Pell coefficient \(17=q^2+2^q\) reappears in the complement
edge chamber.

---

## Boundary

This proves the zero sheet is an induced principal-submatrix shadow of W(3,3),
with exact interlacing and edge-decomposition arithmetic.  It does not yet
prove uniqueness of the zero-sheet orbit under \(\operatorname{Aut}(W(3,3))\),
nor does it derive the Hamming/Fano gauge choice from the full automorphism
group.

---

## Executable Artifact

- Analysis: `analysis/w33_zero_sheet_w33_interlacing_shadow.py`
- Tests: `tests/test_w33_zero_sheet_w33_interlacing_shadow.py`
- Data: `data/w33_zero_sheet_w33_interlacing_shadow.json`
- Result: `PART_MCXVI_zero_sheet_w33_interlacing_shadow_results.json`
