# BT805 — PG(3,2) IS the Tetrahedron; the 35-Line Dictionary

Executes the user's hint: Fano = PG(2,2), the tetrahedron represents
PG(3,2), and the Csaszar/Szilassi count 21 + 14 = 35 = #lines of PG(3,2).
All verified exactly.

## T1: the cell model

The 15 points of PG(3,2) = nonzero vectors of F2^4 = nonempty subsets of
a 4-set = the 15 CELLS of the tetrahedron:

```text
4 vertices (wt 1) + 6 edges (wt 2) + 4 faces (wt 3) + 1 body (wt 4) = 15
```

The 35 lines {a, b, a+b} acquire tetrahedron names — the complete census:

```text
E+V+V : 6    an edge with its two endpoints
E+F+V : 12   vertex + face + the edge joining them (flag lines)
E+E+E : 4    the three edges of a face — and ONLY those
             (no skew edge-triple is ever a line)
E+F+F : 6    an edge with the two faces sharing it
B+E+E : 3    the three opposite-edge pairs, closed by the body
B+F+V : 4    vertex + opposite face + body (the four altitudes)
             total = 35
```

The incidence algebra of the tetrahedron IS the line set of PG(3,2).
The 15 planes are 15 Fano copies (PG(2,2) inside, as the user said).

## T3: completeness of the double Fano (BT804)

Brute-force enumeration: there are EXACTLY 30 Steiner triple systems on
7 labeled points, and EXACTLY 2 of them are invariant under the 7-cycle.
Their disjoint union is precisely the 14-face set of the Csaszar torus
(all gap class {1,2,4} = QR mod 7).  BT804's double-Fano statement is now
complete: the Csaszar faces are THE two cyclic Steiner systems — there
are no others to choose.

## T4: the dual-invariant 35 (user's formulation)

```text
Csaszar:   e + f = 21 + 14 = 35      Szilassi:  e + v = 21 + 14 = 35
```

Duality swaps v <-> f but preserves "edges + 14-cell partner" = 35 =
#lines of PG(3,2).  The complementary sum is also invariant:

```text
e + (7-cell partner) = 21 + 7 = 28 = C(8,2)   (the A8 = GL(4,2) shadow)
v + e + f = 42 = |F42|                         (cells = symmetries)
tetra cells = 15 = #points PG(3,2);  tetra flags = 24 = f = |Aut(K4)|
```

## The trio, fully unified

```text
tetrahedron     = PG(3,2) point set (15 cells), pillow orbifold (BT804)
Csaszar         = double cover of the pillow; faces = the 2 cyclic STS(7)
Szilassi        = dual double cover; same 21-edge budget
35 = e + 14     = lines of PG(3,2) = triples of Z7
{1,2,4}         = QR mod 7 = Fano gaps = 1/7 reptend skeleton (BT774)
```

PG(2,2) lives on the 7 vertices (twice, as the two cyclic Steiner
systems); PG(3,2) lives on the tetrahedron's 15 cells; the torus pair is
the bridge, with its 35 = e+14 census naming the lines.

## Boundary

Open: the A7 < A8 = GL(4,2) transfer making "triples of 7 <-> lines of
PG(3,2)" canonical (then the double-Fano = a distinguished 14-line family
in PG(3,2) — which family?); and the W33 lift: W(3,3)'s 40 = PG(3,3)
points vs the tetrahedral PG(3,2) ground — the q=2 vs q=3 ladder.
