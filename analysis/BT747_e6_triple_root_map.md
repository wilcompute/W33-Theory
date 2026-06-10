# BT747 — The E6 Tri-Orthogonal Root Map

BT746 attached a canonical anti-symplectic involution to each of the 51840
presentation pairs.  BT747 identifies its W(E6) conjugacy class.

## Results (exact)

```text
class size under PSp(4,3)  = 540
class size under PGSp(4,3) = 540   (does not split / fuse)
Type-A and Type-B pairs give the SAME class
pairs fixed per involution = 96 = 48 Type-A + 48 Type-B
540 x 96 = 51840  (exact fibration)
geometry: each involution fixes 8 points + 6 lines of W(3,3)
```

## The naive root map is refuted; the triple root map replaces it

W(E6) has exactly TWO involution classes in its outer coset (odd
reflection length): the 36 reflections (type A1) and the 540 involutions
of type **3A1** — products of three mutually orthogonal reflections.
Since the canonical class has size 540, every presentation pair determines
not a single root but an unordered

```text
TRIPLE of pairwise orthogonal roots of E6  (an A1+A1+A1 subsystem),
```

equivariantly: t(g.pair) = g t(pair) g^{-1}.  The map is a 96-to-1
fibration onto the 540 tri-orthogonal triples, perfectly balanced between
the two chirality torsors (48 + 48 over every triple).

## Reading

- The selector presentation space fibers over the 3A1 subsystems of E6.
  Tri-orthogonality is the E6 face of the lift structure: three commuting
  sign flips per presentation, matching the three substrate directions
  (q = 3) rather than one.
- Chirality (BT746, absolute) is invisible to the involution: each fiber
  splits evenly.  Chirality and the root-triple are INDEPENDENT canonical
  coordinates on the presentation space.
- Combined coordinates: (root triple, chirality, 48-element fiber).  Note
  48 = 16 x 3 = |W(3A1)| x ... — the residual fiber structure is the next
  open object.

## Boundary

Open: the residual 48-element fiber structure (is it a torsor under the
centralizer C_W(t) of order 51840/540 = 96, mod the Z2 = <t> itself?);
which 8-point/6-line W33 configurations are the fixed geometries of the
540 class (8 + 6 = 14 Levi vertices, chi_St value computable); and whether
the BT718 selector sheet meets every fiber the same number of times
(2160/540 = 4 — a uniform 4 would make the canonical sheet a section of
the triple-root fibration too).
