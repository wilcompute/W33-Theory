# BT804 — The Trio Theorem: Pillow Quotients and the Double Fano

Two exact structure theorems for the tetrahedron / Csaszar / Szilassi trio.

## Theorem 1 (the tetrahedral pillow)

Every one of the 7 geometric realizations keeps exactly C2 (BT803), and in
every case the involution has EXACTLY 4 fixed points on the surface
(Riemann-Hurwitz for chi(T) = 0), with census:

```text
Csaszar (all 5):  1 fixed vertex + 3 swapped edges          = 4
Szilassi (both):  3 swapped edges + 1 freely-rotated hexagon = 4
quotients (equivariant subdivision):
  Csaszar  -> V,E,F = 7,12,7   chi = 2   SPHERE
  Szilassi -> V,E,F = 11,15,6  chi = 2   SPHERE
```

So every realization is a double cover of the sphere with 4 branch points
— the TETRAHEDRAL PILLOW S^2(2,2,2,2).  The trio is one tower:

```text
tetrahedron (h=0 ground)  =  pillow orbifold
Csaszar / Szilassi (h=1)  =  its smooth double covers
```

the genus-1 layer is literally the q=2 cover of the genus-0 ground state,
and the duo/half-turn theme (BT750: duo = central half-turn) reappears as
the deck transformation.

## Theorem 2 (the double Fano)

In cyclic Z7 form, ALL 14 Csaszar faces have circular gap class {1,2,4} =
the quadratic residues mod 7, and

```text
faces  =  Fano plane (7 lines, diff set {0,1,3})
          DISJOINT-UNION  mirror Fano (x -> -x image).
```

The Csaszar torus IS the union of the two Z7-invariant Steiner triple
systems; each is an exact 1-factorization companion: the 7 Fano triangles
partition the 21 edges of K7 perfectly (each edge in exactly one line).
The remaining 21 = 3x7 triples are the classes {1,1,5}, {1,3,3}, {2,2,3}.

QR bridge (BT774): the same residue set {1,2,4} that runs the even
positions of the 1/7 reptend generates the Fano difference set and hence
the Csaszar faces.  The decimal clock, the Fano plane, and the minimal
torus triangulation are three faces of the QR/QNR split of Z7.

## Census identities

```text
v + e + f = 7 + 21 + 14 = 42 = |F42| (cells = symmetries)
e + f     = 35 = #triples of the 7-set = #lines of PG(3,2)
v + e     = 28 = C(8,2)  (A8 = GL(4,2) shadow)
```

## Boundary

Open: the explicit A7 < GL(4,2) transfer of the double-Fano split to a
14-line family in PG(3,2); the pillow branch points vs the BT776
corner-centers; enumeration of all 30 STS(7) confirming exactly 2 are
Z7-invariant (= the two face systems).
