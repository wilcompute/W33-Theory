# BT1252 -- Polar Path Tetrahedron Identifier

## Purpose

BT1252 gives the diameter-14 balanced regime a geometric name and a finite incidence description.

## Computation

For the BT1228 / BT1233 four vectors

\[
(0,0,0,2),\quad (0,2,0,0),\quad (0,0,2,2),\quad (1,0,0,0),
\]

the symplectic-zero edges are

```text
(0,2), (0,3), (1,3)
```

and the nonzero edges are

```text
(0,1), (1,2), (2,3)
```

Both edge graphs are paths \(P_4\).  Thus the edge split is self-complementary:

\[
K_4=P_4\sqcup P_4.
\]

## Proposed name

```text
polar path tetrahedron
```

The name is literal: the polar/commuting edges of the tetrahedron form a path, and the nonpolar/noncommuting edges form the complementary path.

## Link to BT1245

This explains the balanced local closure law:

\[
9^3 24^3
\]

on pairs and

\[
72^2 648^2
\]

on triples.  The BT1228/BT1233 diameter-14 fingerprint is the word metric of this polar path tetrahedron regime.

## Files

- Code: `analysis/bt1252_polar_path_tetrahedron_identifier.py`
- Result: `data/bt1252_polar_path_tetrahedron_identifier_summary.json`
