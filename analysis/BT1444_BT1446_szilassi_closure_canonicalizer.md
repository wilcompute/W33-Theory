# BT1444--BT1446: Szilassi fixed face, closure transport, and Frobenius canonicalizer

## BT1444 — fixed-face extractor

The actual Szilassi coordinate data were parsed from `data/Toroidal-Polyhedra-Realizations.txt`.

For both Szilassi realizations, the coordinate C2 symmetry is

\[
R(x,y,z)=(-x,-y,z).
\]

The unique fixed face is face index 4 with ordered boundary

\[
[11,9,12,10,8,13].
\]

The image of this boundary under \(R\) is

\[
[10,8,13,11,9,12],
\]

which is a cyclic shift by three vertices.  Thus the fixed face is not only fixed as a set; its boundary is transported by a half-turn to the opposite boundary points.

The centroids are on the rotation axis:

\[
(0,0,2)\quad\text{for Szilassi v1},
\qquad
(0,0,4)\quad\text{for Szilassi v2}.
\]

## BT1445 — closure orientation transport

The boundary shift by three vertices gives three opposite pairs:

\[
(11,10),\qquad(9,8),\qquad(12,13).
\]

The odd Otto tick can therefore be carried by the fixed Szilassi hexagon as:

\[
12\text{ closure ticks}
=3\text{ opposite pairs}\times2\text{ sides}\times2\text{ orientations}.
\]

This simultaneously lands in:

\[
168\text{ active bins},\qquad 21\text{ Fano flags},\qquad 8\text{ local states},\qquad24\text{ guard bins}.
\]

The result is an orientation-compatible finite transport law.  It is still not a physical embedding of Otto's helix; it is the exact finite closure skeleton.

## BT1446 — Frobenius involution canonicalizer

The Frobenius symmetry is modeled as affine maps over \(\mathbb Z_7\):

\[
F_{42}=\mathbb Z_7:\mathbb Z_6,
\qquad
x\mapsto ax+b.
\]

The seven involutions are

\[
x\mapsto -x+b.
\]

The Szilassi fixed face has index 4, so the canonical involution is the one fixing 4.  Since \(b=2\cdot4=1\pmod 7\), it is

\[
\tau_4(x)=-x+1\pmod7.
\]

Its cycle structure is

\[
(0\ 1)(2\ 6)(3\ 5)(4).
\]

This exactly matches the closure ledger:

\[
2+2+2+1.
\]

It also gives a canonical ordering seed:

- 12 Otto strands = 3 transposition pairs \(\times\) 2 sides \(\times\) 2 orientations;
- 21 Fano flags = 7 face indices \(\times\) 3 local directions;
- closure face first = fixed face 4.

## New conclusion

The odd 13th half-turn has a precise finite closure carrier:

\[
\boxed{
\text{odd half-turn}
\to
\text{Szilassi fixed hexagon }[11,9,12,10,8,13]
\to
\tau_4=(0\ 1)(2\ 6)(3\ 5)(4)
}
\]

This is the strongest form of the closure-tick conjecture so far.
