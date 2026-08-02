# Passes 2050–2053 and 2064 — exact methods and scope

This packet executes five continuations while preserving the distinction between
literal finite computations, frozen expensive censuses, executable reference
models, literature identifications, and physics or hardware proposals.

## Common finite model

The q=3 computations use the literal projective model already frozen in the
repository: 40 points, 40 totally isotropic lines, 240 collinear edges, 540
frames, 36 spreads, PSp(4,3) of order 25,920 and PGSp(4,3) of order 51,840.
Signed-edge maps use the orientation determined by the sorted point labels.

## Pass 2050 — full-group fusion of orbit-cover subgroups

Pass 2012 completely enumerated the 1,026 subgroups of one four-line spread-pair
stabilizer H≅S4×D8 and found 33 H-conjugacy classes that admit a 60-frame exact
cover formed from whole frame orbits.  Pass 2050 conjugated those 33 literal
subgroups by all 51,840 elements of PGSp(4,3).

The result is 14 full-group subgroup conjugacy types.  For every type the
recorded normalizer order N and class size c satisfy N c=51,840.  The member
lists partition the 33 local classes.  This is a full-group classification of
the positive subgroup types represented inside H.

A separate calculation took the first deterministic exact-cover witness returned
for each of the 33 local classes.  There are 32 distinct frame sets, occupying 12
full-group schedule orbits.  This is deliberately not called a classification of
all schedules: a subgroup can admit multiple exact covers, and only one frozen
search witness per local class was transported.

## Pass 2051 — explicit quadratic maps

The signed 240-edge representation is reconstructed from its literal action.
Two inverse order-three classes of size 40 give class sums C+ and C-.  Their sum,
together with the size-45 involution class sum, separates the blocks
15+24+81+30+90.  On the 90, D=C+−C- satisfies D²=−192I, so
J=D/sqrt(192) is the canonical PSp-equivariant complex structure.  The outer
similitude sends J to −J.

Seven bilinear maps are then built without character-only reasoning.

1. Vertexwise edge energy, projected to the point -4 eigenspace and differentiated,
   gives a symmetric surjection Sym²(90)→15.
2. The same construction through the point +2 eigenspace gives
   Sym²(90)→24.
3. Writing an edge flow as a skew 40×40 matrix X, the graph-restricted
   commutator XY−YX gives Λ²(90)→30.
4. Inserting the point adjacency A gives XAY−YAX, with surjective projections
   to 30 and 81.
5. J-twisting the commutator,
   C(Jx,y)+C(Jy,x), gives symmetric maps to 30 and 81.

Every nonzero map in this canonical family is surjective.  The untwisted maps
are chirality-even; the J-twisted maps are chirality-odd.  Under simultaneous
mu6 rotation of both inputs, the maps to 15 and the two J-twisted maps are
invariant, while the 24 and untwisted commutator channels span a period-three
bilinear orbit.  These are exact selection rules for the constructed maps, not
coupling constants and not a complete basis of each Hom space.

## Pass 2052 — executable architecture reference

The prototype rebuilds W(3,3), reads the independently hashed D8 schedule,
regenerates the order-eight subgroup, verifies that the selected frames are a
union of twelve orbits, expands them to sixty frames and checks the 240-bit edge
profile `{1:240}`.

The same program builds the 36-lane spread relation A and verifies A²=9I+6J.
Thus A/3 is an exact involution on mean-zero signals.  It also builds the
18-lane rook-double crossbar as two 3×3 banks with cross-bank row-or-column
connections.  The storage comparison of 120 seed bits against 600 expanded
frame-ID bits assumes fixed D8 generators and excludes metadata and error
protection; it is a reference-model estimate, not an FPGA synthesis result.

## Pass 2053 — identifying the spread graph

The literal adjacency matrix is hashed before identification.  A fixed spread
has a 15-vertex local graph isomorphic to the Kneser graph K(6,2), and the twenty
non-neighbours induce the Johnson graph J(6,3).  Together with the rank-three
PGSp(4,3) action, this identifies the graph as the standard `NO_6^-(2)` graph,
also denoted `NO_5^{-perp}(3)`.

This extra evidence is essential.  Tens of thousands of nonisomorphic strongly
regular graphs share the parameters (36,15,6,6); parameters and spectrum alone
would be another unsafe count match.  The database name and automorphism-group
identification are prior art.  The repository contribution is the literal
realisation on its 36 spreads and the certified subconstituent maps.

## Pass 2064 — the regular-spread rank-three family at q=3,5,7

For each prime q=3,5,7, the code constructs F_(q²)=F_q(alpha), alpha² a
nonsquare, embeds the one-dimensional F_(q²)-subspaces of F_(q²)² as a regular
symplectic spread, and generates its complete projective symplectic orbit using
all point transvections.  The complete orbit sizes are 36, 300 and 1,176.

Every pair census has only two values: 1 and q+1.  The q+1 relation is strongly
regular:

| q | v | k | lambda | mu | nontrivial eigenvalues |
|---:|---:|---:|---:|---:|---:|
| 3 | 36 | 15 | 6 | 6 | 3, -3 |
| 5 | 300 | 195 | 130 | 120 | 15, -5 |
| 7 | 1176 | 875 | 658 | 630 | 35, -7 |

All three cases match the formulas frozen in the certificate.  Standard
finite-geometry results explain why distinct regular spreads meet in at most
q+1 lines and why an intersection of at least three lines is a regulus.  The
exact all-odd-q strongly regular formulas were not located as a quoted theorem
in the literature search and are not proved in this pass.  They remain a
uniform conjectural family beyond the complete q=3,5,7 computations.
Non-Desarguesian symplectic spreads, equivalently the broader ovoid side of
Q(4,q), are explicitly outside this census.

## Reproduction tiers

- `w33_pass2051_explicit_quadratic_intertwiners.py`,
  `w33_pass2052_integrated_geometry_hardware_prototype.py`, and
  `w33_pass2053_identify_spread_graph.py` are literal rebuilders.
- `w33_pass2064_regular_spread_rank3_family.py --full` rebuilds the complete
  q=3,5,7 orbit censuses; its default mode verifies the frozen certificate.
- `w33_pass2050_full_group_orbit_cover_fusion.py` is a fail-closed replay of the
  expensive full-group fusion table.  It does not pretend to reconstruct all
  conjugations in CI.
- `w33_pass2050_2053_2064_verify_frozen.py` checks all 77 canonical assertions,
  every digest, and the independent D8 exact-cover witness.
