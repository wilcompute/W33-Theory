# BT806 — The A7 Ladder and the Anti-Flag Theorem

Closes the BT805 boundary: the canonical home of the Csaszar census inside
PG(3,2).

## GAP witness

```text
A7 < GL(4,2) = A8 is TRANSITIVE on points (15), lines (35), planes (15)
  - both conjugacy classes; line stabilizer order 72 = triple stabilizer
  => the classical equivariant bijection {triples of 7} <-> {lines of
     PG(3,2)} exists; the 21+14 split does NOT live at the A7 level.
N_GL(4,2)(Sylow-7) = F21 = C7:C3   (multiplier C3 = QR set {1,2,4})
```

## Python verification (explicit Singer + Frobenius matrices)

```text
F21 orbits on PG(3,2):
  points:  [1, 7, 7]    vacuum point p0 + two heptads
  lines:   [7, 7, 21]   <- THE CSASZAR CENSUS
  planes:  [1, 7, 7]    fixed plane pi0 + two 7-orbits
p0 NOT on pi0           <- ANTI-FLAG
```

## The Anti-Flag Theorem

The two 7-line orbits are exactly

```text
(a) STAR(p0):   the 7 lines through the vacuum point
(b) LINES(pi0): the 7 lines of the fixed Fano plane (a PG(2,2))
```

and (p0, pi0) is a NON-INCIDENT point-plane pair.  Under the A7 bijection
these are the two Z7-invariant Steiner triple systems = the 14 Csaszar
faces (BT804/805).  Therefore:

```text
Csaszar faces (14)  =  star + plane of an anti-flag
Csaszar edges (21)  =  the generic line orbit
Csaszar vertices(7) =  a heptad point orbit
```

The torus's (v, e, f) = (7, 21, 14) census IS the F21-orbit structure of
PG(3,2) - and the two interleaved Fano systems that looked like twins on
the 7-set are revealed as a point-star and its polar plane: PROJECTIVE
DUALITY is what interchanges them.  The BT772/BT804 mirror themes
(chirality = P-axis vs L-axis; Fano vs mirror-Fano) all reduce to the
same mechanism: a point-object and a plane-object exchanged by duality.

## The vacuum ladder

```text
q=2:  PG(3,2) points: 15 = 1 + 7 + 7      (vacuum + 2 heptads, F21 clock)
q=3:  W(3,3)  points: 40 = 1 + 12 + 27    (vacuum + gauge + matter)
```

The 1/7 reptend multiplier {1,2,4} (BT774) is the C3 that runs the q=2
clock; the Z12 rectangle clock (BT746) runs the q=3 one.

## Boundary

Open: the exact A7-bijection image of a SINGLE Fano system (does Fano_A
map to the star and Fano_B to the plane canonically, or does the choice
of bijection swap them - i.e. is the chirality of BT804 the duality
class?); the heptad orbits as Conwell-style structures; and the q=3 lift
of the anti-flag theorem (skew pair = the W33 anti-flag analogue?).
