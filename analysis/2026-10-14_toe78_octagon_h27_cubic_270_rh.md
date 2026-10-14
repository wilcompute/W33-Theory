# TOE78 — W33 octagon wedges, Heisenberg addresses, cubic tritangents and graph RH

14 October 2026. This packet adds finite mathematical results, not a fundamental physical Theory of Everything or the classical Riemann hypothesis.

## Results already validated by native GitHub CI

The actual 216-element native stabilizer of the two theta chord edges is the split group H27 ⋊ D8, containing a normal nonabelian extraspecial H27 that acts freely and transitively on their 27 common W33 Levi octagons. There are four center-preserving and four center-inverting elements in the D8 quotient. The ordinary projective one-qutrit Clifford group of order 216 is **not the same group**, despite equal order: the native group has a central order-three Heisenberg translation subgroup and an anti-symplectic coset inverting its center.

The native 216 permutation action on the 27 octagons has unordered-pair orbit valencies 2,4,4,8,8. Exactly one degree-ten union of those orbitals yields SRG(27,10,1,5), which has 45 triangle cliques satisfying the generalized-quadrangle incidence axioms. Crucially, those lines are literally the right cosets of five cyclic order-three subgroups of the **actual regular H27**; one is the Heisenberg center. The D8 direction orbits and resulting 216-tritangent orbits are verified by direct group multiplication, with tritangent orbit sizes 9,18,18. An exhaustive test over 432 H27 generator-basis gauges attempts to align those five directions with the repository's previously frozen regular/Payne H27 address geometry. It reports the actual match count rather than selecting a convenient identity by naming convention.

The recovered 27-vertex cubic graph is itself a 10-regular Ramanujan graph: its adjacency eigenvalues are 10 (once), 1 (20 times), and -5 (six times), satisfying the nontrivial bound 2sqrt(9)=6. Its exact Bass/Ihara determinant is

Z_27(u)^(-1)=(1-u^2)^108 (1-u)(1-9u)(1-u+9u^2)^20(1+5u+9u^2)^6.

This supplies a third distinct regular Ramanujan / graph-RH layer: W33 collinearity degree12 gives radius 11^(-1/2), W33 Levi incidence degree4 gives radius 3^(-1/2), and the induced cubic 27-point graph degree10 gives radius 1/3. The 11-site theta graph is irregular and has a different twisted Ihara calculation. None of those graph results establishes classical RH.

Each of the 45 cubic tritangents is one undirected prime 3-cycle; it has six **based, oriented** cyclic presentations, for a total of 270, equal to the trace of the length-three nonbacktracking matrix. The mapping (v0,v1,v2) to the support {(v0,0),(v1,1),(v2,2)} sends those 270 marked prime walks to the 270 externally phase-labelled tritangent cubic supports in the existing E8 instruction program. It is natural and equivariant for actions that permute tritangent points and fix external phase labels. It does not identify E8 root operators, complex phase amplitudes, masses or couplings.

## Stronger mechanism: 27 opposite vertices, not a mysterious numerology

In the native 80-vertex Levi graph, each incidence vertex has four edges. Choose any unordered two-edge wedge. This makes 80*C(4,2)=480 wedges, 240 centered at W33 projective points and 240 at totally isotropic lines.

For every wedge there are exactly 27 opposite vertices of the center, of the same bipartite type at Levi graph distance four. The generalized quadrangle axiom gives a unique length-four geodesic from the center to each opposite vertex through EACH of the wedge's two distinct first edges. Their union is a simple eight-cycle through that wedge. The midpoint of that cycle is the corresponding opposite vertex. Hence the 27 shared octagons of any wedge are **canonically and stabilizer-equivariantly** bijective with 27 opposite vertices.

Double-counting gives 480*27=1620*8=12960 wedge–octagon incidences. An independent finite-field F3^4 symplectic reconstruction (40 points, 40 isotropic lines) verified all 480 wedges and 27 disjoint shortest-path pairs. The native-repository census producer independently checks the full list of 1620 octagons and freezes the map for the actual 11-site theta chords. These calculations explain the origin of an H27 address carrier on local octagons and provide the missing canonical path to the known regular/Payne action. The cubic/E6 coordinate gauge must still be tested separately, and the trinification operator H27 (whose center is scalar) remains a different representation.

## Prior art and scientific boundaries

The 27/45 geometry of GQ(2,4) and associated Heisenberg and cubic-surface subgroups are established mathematics. See Dolgachev (2010), https://dept.math.lsa.umich.edu/~idolga/asia10.pdf, and Saniga et al., https://arxiv.org/abs/0903.0715. The potentially distinctive result is the explicit native W33 octagon-wedge realization and its correspondence to previously constructed source files, not a claim to have discovered GQ(2,4) itself.

Code:
- analysis/w33_20261014_toe77_H27_shared_octagon_group.py
- analysis/w33_20261014_toe78_cubic_270_ihara.py
- analysis/w33_20261014_toe78_wedge_opposites.py

Tests and GitHub Actions workflows are included for each. The cubic-Ihara run passed; additional group-orbit and full native-wedge runs may still be queued, so do not confuse a pushed script with a completed test.

## Five independent next research fronts

1. Complete the **canonical octagon -> opposite-point -> regular Payne H27 -> cubic 27 -> E8 phase-labelled triple** transport, including stabilizer orbits and all explicit gauge freedoms.
2. Test the 270-marked-prime spectral trace experimentally in a three-arm optical circuit against standalone theta and W33-embedded controls, with calibrated time-bin/OAM phase imperfections.
3. Couple the cubic H27 address sector to the full 27-orbit exact-cover quantum transition model, and compute actual central-character/projector selection rules rather than equating several occurrences of 27.
4. Construct a truly local 4D spin/overlap Dirac operator and investigate which gauge-allowed perturbations can lift the W33 bipartite rank-protected zero modes without violating anomaly constraints.
5. Certify a low-energy spectral gap for the interacting compact-U1 gauge sector and test whether embedding-sensitive 120° versus pi flux competition survives dynamical gauge fields.

The Theory of Everything remains unresolved.

## Follow-up: independently completed GitHub Actions verification

All three primary research tracks completed successfully:

- Native octagon H27/GQ/cubic address: https://github.com/wilcompute/W33-Theory/actions/runs/38647657091 — **7/7 tests**, with exhaustive 432 H27 normal-form basis searches. The printed certificate reports **48 actual equivariant gauges** from the newly constructed octagon cubic geometry to the previously frozen regular/Payne five-direction address geometry. This is a genuine 27-point torsor-and-45-line identification, but gauge *nonuniqueness* remains explicit.
- Cubic 27 Ramanujan / 270 marked nonbacktracking primes: https://github.com/wilcompute/W33-Theory/actions/runs/38647521435 — **1/1 test**, regenerating the exact strongly regular/Ihara certificate and the 270-to-270 based-oriented-cycle/externally-labelled-triangle correspondence.
- All native Levi 2-arcs and canonical 27 opposite-vertex bijection: https://github.com/wilcompute/W33-Theory/actions/runs/38647970837 — **1/1 test**, explicitly locating the native theta pair at **W33 point vertex 1**, not at an arbitrary or unspecified center. All **480 wedges**, including 240 centered at points and 240 centered at lines, possess 27 distinct antipodal cycles and the expected 12960 incidences.

The group producer also reports the new 216-action orbit decomposition on the **270 oriented/marked cubic phase supports as 54+108+108**, versus **27+27+216** under the previously frozen (different) 648-Clifford action. The tritangent orbit decomposition is **9+18+18**, while the native D8 orbit partition on five H27 directions is **1+2+2**. Four dihedral elements invert the Heisenberg center, preventing an identification of the whole order-216 group with ordinary complex-linear qutrit Clifford operations on a fixed central character.

**Additional nine-geometry theorem:** the automorphism group of the exponent-three extraspecial H27 has order 432, represented by the 432 ordered noncommuting generator pairs. Exactly 48 of those basis gauges preserve the selected five cyclic cubic directions, giving **432/48=9 equivalent H27 direction-system realizations** under the automorphism action. A separate exact source assertion enumerating all nine realizations has been committed; its latest dedicated CI should be checked before describing *that additional implementation* as successfully executed.

### A geometrical 240-chart atlas worth studying

At each of the 40 point-side W33 Levi vertices, the four incident flags admit exactly six unordered wedges. Therefore there are **240 point-centered wedge address charts**, each in natural bijection with its center's 27 opposite points. Dually there are 240 line-centered charts. At one fixed point, all six charts address the same 27 opposite points, but each uses a different selected pair of first paths; their transition maps are a concrete native gauge-comparison problem. The point stabilizer has order 1296 and each wedge stabilizer order 216 (index six), mirroring the six wedge choices.

This is an exact finite incidence atlas, **not** an automatic W(E6)-equivariant identification with 240 E8 roots. The repository has independently documented that transitive W33 240-element carriers and E8's Weyl-E6 root-orbit decomposition can obstruct such a bijection.

The next research frontier is to compute every one of the six wedge-to-wedge address transformations at a center explicitly, determine their action on the 45 cubic lines and 270 phase supports, and compare with the abstract normalizer structure of H27.