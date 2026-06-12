# BT850 — The Tomotope's Symmetry Type: Class 2_{0,1,2}, Exactly

**Status: PROVEN (machine-verified from the Pillar 70 flag model, `analysis/bt850_tomotope_two_orbit_class.py`, data `data/bt850_tomotope_two_orbit_class.json`)**

The user's pointer "the tomotope is actually classified as a maniplex" lands
on a datum nobody had computed: the tomotope's exact **symmetry type** in the
2-orbit taxonomy of Hubard et al. — the invariant that Mochán's
*Polytopality of 2-orbit maniplexes* (Discrete Math. 2024) consumes.

## Setting the record straight (heals BT849's framing)

The tomotope is an abstract **uniform 4-polytope** (hence a rank-4 maniplex),
built by Monson–Pellicer–Williams (Ars Math. Contemp. 2012). Its fame: it has
**infinitely many distinct minimal regular covers** — impossible in rank 3,
where the minimal regular cover is unique. The driver is its monodromy group
of order **18432 = 96 × 192** (exactly Pillar 70's measurement) failing the
intersection condition: the regular covers leave the polytope world and land
in maniplexes. (BT849's MD and the paper paragraph have been corrected — the
*covers* are non-polytopal, not the tomotope itself.)

## T1 — Independent automorphism computation

From the four monodromy generators on 192 flags (Pillar 70 bundle), the full
automorphism group = centralizer of the monodromy in Sym(192), built
flag-image by flag-image: **|Aut| = 96**, acting with **two orbits [96, 96]**
— the tomotope is a 2-orbit maniplex.

## T2 — The class: 2_{0,1,2}

For each color i, the i-move r_i sends orbits to orbits (monodromy commutes
with Aut). Computed:

```text
I = {0, 1, 2}   (vertex-, edge-, face-moves stay in orbit)
links = {3}     (only the CELL-move crosses orbits)
```

**The tomotope is in class 2_{0,1,2}** — the facet-alternating class. The
symmetry type graph is two vertices with semi-edges at colors 0,1,2 and a
single link at color 3.

## T3 — The orbit invariant is the cell type

The two orbits share all 4 vertices, all 12 edges, all 16 faces — but **split
the 8 cells 4 + 4, exactly by cell type**: orbit 0 = flags in hemioctahedra,
orbit 1 = flags in tetrahedra. The tomotope **alternates spherical cells
(tetrahedra) and projective cells (hemi-octahedra)**.

This is precisely the blind spot of the classical "locally X" taxonomy (a
polytope whose facets have *different* topologies — sphere and projective
plane — fits no "locally spherical/projective/toroidal" box). The tomotope is
the canonical inhabitant of that gap, and its class 2_{0,1,2} is the formal
home: Monson–Schulte's *semiregular polytopes and amalgamated C-groups*
(alternating facet types) and Mochán's 2-orbit polytopality criteria apply
verbatim.

## Machine reading

The middleware's two flag orbits = the machine's two packet phases
(tetrahedral = spherical = "classical-capable transport" vs hemioctahedral =
projective = "twisted transport") — the 2_{0,1,2} class says the runtime
crosses phases **only at cell hops** (color 3), i.e. phase changes are
localized to the cell-adjacency layer, which is exactly where the BT828–834
runtime engineering placed its commit boundaries.

## Open

- Run Mochán's polytopality criteria in reverse: which 2_{0,1,2} maniplexes
  over the same symmetry type graph cover the tomotope, and where do our
  measured covers (the 18432 monodromy quotients, BT831 architecture) sit in
  her classification?
- The voltage-operations formalism (Hubard–Mochán–Montero, Combinatorica
  2023): express the tomotope's tetra/hemiocta alternation as a voltage
  operation on a smaller maniplex — candidate base: the 4-vertex simplex
  with a Z₂ voltage (cf. Pillar 73's voltage functor).
- Cayley-extension reading (Cunningham–Mochán–Montero 2025): Aut = 96 acts
  with two orbits; check whether a subgroup acts regularly on the 4 vertices
  (Cayley maniplex test for the middleware).
