# BT744 — The Tits Building Dictionary

The Levi graph of W(3,3) is the rank-2 Tits building of Sp(4,3) (type C2,
the generalized quadrangle GQ(3,3)).  Under this dictionary the entire
selector program (BT696–BT742) is Tits-building geometry:

```text
selector object                        building object
------------------------------------   ---------------------------------
Levi graph (80 vertices, 160 flags)    the building Delta
flags (point, line)                    chambers (160)
Levi 8-cycles (1620)                   APARTMENTS
Hodge E4 = chart81 (dim 81, BT742)     Solomon-Tits H~1(Delta) = Steinberg
BT713 selector sheets                  apartment systems
BT718 hinge rule                       canonical apartment choice
BT696 lift multiplicity 32             |N(T)| = 2^5 (torus normalizer)
```

## Verified facts (all exact)

1. **Apartment count.**  1620 octagons enumerated combinatorially
   (4 points + 4 lines, consecutive collinear, diagonals non-collinear =
   ordinary quadrangle).  Arithmetic: |Sp(4,3)|/|N(T)| = 51840/32 = 1620.
2. **Transitivity.**  PSp(4,3) is transitive on the 1620 apartments;
   stabilizer order 16 = 25920/1620 (image of N(T)).
3. **81 apartments through every chamber** (uniform), 1620·8/160 = 81.
4. **Solomon-Tits basis.**  The 81 apartments through a fixed chamber have
   rank 81 over F2 AND over Q — they are a BASIS of the cycle space.  The
   protected memory sector has a canonical combinatorial basis: the
   apartments through any chosen chamber.
5. **Steinberg vanishing law.**  chi_St(g) = #fixflags − #fixvertices + 1
   vanishes EXACTLY on the 3-singular elements (order divisible by 3):
   16640 3-singular + 9280 3-regular elements, zero violations.
6. **Regular-module corollary.**  Since chi_St vanishes on all nontrivial
   elements of the Sylow-3 subgroup U (|U| = 81 = q^mu), St|_U is the
   REGULAR module F[U]: the protected 81-sector is free of rank 1 over the
   substrate's ternary symmetry group.  "81 = q^mu = H_1 protected memory"
   now has its precise algebraic form: one free generator over U.

## Why this is the right frame

Solomon-Tits is exactly the statement that the building has the homotopy
type of a wedge of spheres whose top homology is Steinberg; for rank 2 the
building is the incidence graph and the spheres are the apartment octagons.
The selector program's empirical discoveries — the 24->3->1 reduction, the
multiplicity 32, the rank-81 sheets, the unique bridge — are the shadow of
this classical structure, now made explicit.  In particular:

- BT696's "every rectangle has 24 valid lifts, every cycle has multiplicity
  32" is apartment combinatorics: 2160·24 = 51840 = |Sp(4,3)| and
  1620·32 = 51840.
- BT713's rank-81 sheets are apartment systems that span St.
- BT742 + Schur: the chart81 -> E4 bridge is the unique (up to scalar)
  G-map between two copies of St.

## Boundary

Open: the exact 51840 = 2160·24 coincidence suggests the (rectangle, lift)
presentation space is a free Sp(4,3)-space — chirality orbits to be
computed (BT745).  Also open: a W(E6)-equivariant statement for the
embedding Sp(4,3) = W(E6)' and transport of the apartment basis to the E6
root system side.
