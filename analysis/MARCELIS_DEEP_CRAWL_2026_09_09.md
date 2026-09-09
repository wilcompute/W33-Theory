# Frans Marcelis deep crawl: the multichart finite-geometry atlas

**Date:** 2026-09-09  
**Scope:** external-site synthesis plus exact local falsifiers.  This note does not claim that Marcelis' constructions are identical to the W33/Holonet objects.  The recurring lesson of his site is the opposite: the useful relations are projections, quotients, trace maps, incidence correspondences, changes of coordinates, and alternative realizations.

## Crawl scope

The mathematical navigation was followed broadly rather than stopping at the pages whose titles already mention Witting or E8.  The pages/threads inspected include:

- PG(3,2): points, planes, pencils, coordinates, generalized quadrangles, spreads/ovoids/grids and the Veldkamp-space material;
- the E8 sequence: 600-cell slices, hypercube decompositions, PG(3,2) labels, Witting/PG(3,4) material, four-qubit labels, hyperbolic quadrics and generalized-hexagon material;
- the Witting-polytope and centre-structure pages;
- Penrose dodecahedron / Witting configuration;
- 27 lines, double-six, cubic-surface, Reye and rhombicosidodecahedron pages;
- Icosian / quaternionic constructions;
- Mermin pentagrams, Cayley--Salmon and Desargues configurations;
- the Miracle Octad Generator and both PG(3,2)- and PG(2,4)-based Steiner-system constructions;
- Heawood harmonic cubes, harmonic diagonal cubes, the Coxeter graph and Klein quartic;
- GQ(4,2) in elliptic/600-cell geometry;
- the Hessian configuration;
- hypercube / PG(3,2) pages.

WordPress utility links, login/subscription links and image-attachment URLs were not treated as separate mathematical pages.  One large linked PDF could not be fetched through the browser because of its size; the repository already contains the extracted Marcelis PDF and an earlier full-document execution packet (`analysis/BT1713_BT1715_fgmarcelis_execution.md`).

## The pages that look unrelated but are directly useful

| Marcelis thread | What the page actually carries | W33/Holonet use | Correct relation type |
|---|---|---|---|
| Hypercube / PG(3,2) | the 15 binary projective points and 35 lines rendered through a 4D cube language | local binary chart/Fano address language | coordinate realization / projection |
| Heawood graph of harmonic cubes | 14 harmonic cubes on Fano point/line vertices; 21 common harmonic-square incidences; MOG data encoded by the same graph | Fano scheduler / MOG / chart-incidence vocabulary | incidence quotient; **not** a literal subgraph of the 540-chart web |
| Klein quartic | the same Heawood/Fano triples reorganized by the genus-3 surface and spread hyperpackings | PSL(2,7)=GL(3,2) control symmetry, 7-fold scheduling | group/incidence realization |
| PG(3,2)-based S(5,8,24) | octads assembled from planes, complementary cubes, ovoids and affine-plane partitions | MOG/Golay/code threads | design construction |
| PG(2,4)-based S(5,8,24) | 21 PG(2,4) points + three Romans; AG(2,4) and an AG(4,2)->PG(3,2) projection for the 35 binary lines | GF(4)/binary atlas and MOG bridge | field restriction + affine/projective projection |
| Hessian configuration | exact `(9_4,12_3)` incidence, nine diameters and twelve `3{4}2` lines | qutrit Hesse/AG(2,3) phase-space layer | incidence isomorphism |
| Penrose dodecahedron / Witting | 40 Penrose/Witting states, PG(2,4) labeling, four-qubit symbols and 40 orthogonal tetrads | Witting state-side realization of W33 contexts; contextual communication | projective-state realization |
| Mermin / Cayley--Salmon / Desargues | Mermin pentagrams inside complements of GQ(2,2), Klein-quadric lines and Desargues/Petersen complements | Pauli contextuality and finite-geometry control cases | operator/incidence correspondence |
| GQ(4,2) elliptic / 27 lines | GQ(2,2) + double-six gives the 27-line GQ(4,2); 600-cell geometry realizes the same incidence | 27--40--45 generalized-quadrangle/E6 flank | incidence realization |
| Rhombicosidodecahedron / cubic surface | double-six, Reye configuration, cubic surface, 24-cell and 600-cell chained geometrically | toroidal/exceptional/cubic-surface bridge | projection/realization chain |
| Icosians | quaternionic 600-cell route feeding Witting/E8 structures | independent quaternionic E8 realization | alternative realization, not coordinate identity |
| Witting centre structures | translated/shrunk PG(3,2)-plane patterns and hypercubes inside Witting midpoint data | E8/Witting centre and binary control atlas | central projection / translation |
| E8 four-qubit pages | 120 Witting antipodal pairs, four-qubit labels, GF(4) and trace-map patterns, 2160 Witting edges | operator-label and E8/Witting edge layers | structured label map with a gauge/representative convention |

## Exact result 1: the Marcelis Heawood object does not literally sit in the 540-chart web

`analysis/w33_marcelis_multichart_atlas.py` reconstructs the W33 chart web from first principles:

```text
40 W33 lines
-> 540 skew line pairs = Q3 charts
-> 4 common transversals per chart
-> C(4,2)=6 neighboring charts
-> 540 vertices, degree 6, 1620 web edges
```

The chart web is triangle-free.  Build its distance-two/common-neighbor graph: two web vertices are adjacent there when they are not web-adjacent but share a web neighbor.  This 540-vertex graph is exactly 30-regular.

An exact Bron--Kerbosch maximum-clique search gives

```text
omega(distance2(chart_web)) = 6.
```

Now suppose a Heawood graph were a literal subgraph of the chart web.  The Heawood graph is bipartite with seven vertices on each side.  Any two vertices on one side share a neighbor on the other side.  Because the host chart web is triangle-free, their images would be nonadjacent in the chart web while sharing a neighbor, hence all seven images would form a `K7` in the distance-two graph.

They cannot: the exact maximum is six.

Therefore

```text
Heawood is NOT a literal 14-vertex subgraph of the 540-chart W33 web.
```

This is useful, not disappointing.  It tells us precisely how to read Marcelis and BT1714: the Heawood/Fano layer must be an incidence quotient, scheduler label, projection, fibre/control object or other functorial shadow.  A direct-inclusion claim is now ruled out.

## Exact result 2: the GF(4)->GF(2) trace is not a canonical projective map

Marcelis repeatedly uses the field trace in structured GF(4)/four-qubit constructions.  With

```text
GF(4) = {0, 1, omega, omega^2},  omega^2+omega+1=0,
Tr(x)=x+x^2,
Tr: 0,1,omega,omega^2 -> 0,0,1,1,
```

coordinatewise trace is additive on vectors.  But a projective point is a scalar class.  The verifier searches representatives and finds an explicit pair `v` and `omega*v` representing the **same** point of `PG(3,4)` whose nonzero binary trace vectors are different.  Over GF(2) those different nonzero vectors are different projective points.

Hence

```text
coordinatewise Tr_GF(4)/GF(2) is not, by itself,
a well-defined global map PG(3,4) -> PG(3,2).
```

Whenever the Marcelis pages obtain a valid PG(3,2) pattern from trace data, the construction is carrying extra structure: a chosen representative/phase convention, a restricted structured family, a quotient, or an accompanying geometric selection.  The repo should preserve that extra datum instead of treating `trace` as a canonical projective functor.

## The multichart dictionary

The safe architecture is now:

```text
complex Witting / CP(3) states
        |  orthogonality / chosen state realization
        v
40-context W33 incidence kernel  <->  projective F3^4 Pauli/symplectic labels
        |
        | choose local skew-line chart
        v
Q3 = F2^3 local XOR chart
        |
        +--> Fano / Heawood incidence-control language

separately:
PG(2,4), PG(3,4), GF(4) and four-qubit Marcelis labels
        |
        | structured trace / projection / chosen representative
        v
PG(3,2), MOG, Fano pencils/spreads
```

No bare count is allowed to identify these coordinate systems.

## External pages retained in the atlas

Primary Marcelis pages used in this pass:

- https://fgmarcelis.wordpress.com/
- https://fgmarcelis.wordpress.com/e8/
- https://fgmarcelis.wordpress.com/e8/e8-%C2%A74-8-hypercubes-and-16-333s/
- https://fgmarcelis.wordpress.com/e8-%C2%A76-more-on-the-relation-pg32-and-e8/
- https://fgmarcelis.wordpress.com/e8/e8-%C2%A76-alternative-set-of-14-hypercubes/
- https://fgmarcelis.wordpress.com/e8-%C2%A714-four-qubits/
- https://fgmarcelis.wordpress.com/witting-polytope/
- https://fgmarcelis.wordpress.com/structures-of-centres/
- https://fgmarcelis.wordpress.com/2018/02/21/penrose-dodecahedron-witting-polytope/
- https://fgmarcelis.wordpress.com/27-lines-on-a-cubic-surface/
- https://fgmarcelis.wordpress.com/2017/03/19/mermin-pentagrams-cayley-salmon-desargues/
- https://fgmarcelis.wordpress.com/2021/06/20/steiner-system-5824-from-finite-projective-space-pg32/
- https://fgmarcelis.wordpress.com/2021/06/29/steiner-system-s5824-from-projective-plane-pg24/
- https://fgmarcelis.wordpress.com/2021/06/30/heawood-graph-of-harmonic-cubes/
- https://fgmarcelis.wordpress.com/klein-quartic/
- https://fgmarcelis.wordpress.com/hessian-configuration/

The neighboring GQ(4,2), hypercube/PG(3,2), MOG, Icosian and centre pages were also cross-read through the site's internal navigation and the previously ingested Marcelis corpus in this repository.

## Boundary

This pass establishes finite incidence objects, two negative/falsifying results, and a source cross-index.  It does **not** prove that Marcelis' geometric visualizations are physical spacetime models, that the 540-chart Holonet is experimentally realized, or that every visual correspondence on the site defines a canonical algebraic map.  The point of this pass is to make those distinctions executable.
