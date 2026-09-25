# 24 September 2026 — relative time / Fano VM continuation

This packet continues the temporal-E8 controller line after commit 5b747479d.
It adds three exact bridges and repairs one older network witness.  The common
theme is that structures which previously shared only counts now share explicit
chain maps, addresses, and group actions.

## 1. Common winding survives as relative H2

Let K be the filled 27-history temporal complex and G its null 1-skeleton.
The certified dimensions are

    V=27, E=108, F=36,
    rank(d1)=26, rank(d2)=36.

Therefore

    dim H1(G)=82,
    dim H1(K)=46,
    H2(K)=0,
    dim H2(K,G)=36,

and the long exact sequence reduces dimensionally to

    0 -> 36 -> 82 -> 46 -> 0.
The distinguished relative class is the sum of all 36 oriented temporal
triangles.  Its connecting boundary is exactly the 108-edge PSp-invariant
orientation cycle, already proved to equal the orbit sum of one positive pulse
in each of the four null directions.

So the integer common winding is not destroyed by filling the temporal
triangles.  It moves from ordinary H1 to a distinguished line inside the
relative-boundary sector H2(K,G).  This gives an exact topological location for
the finite arrow while preserving the earlier no-go in filled H1.

Producer: analysis/w33_20260924_common_winding_relative_h2.py

## 2. The seven-qutrit VM has a Fano/K7/Csaszar routing completion

Index the seven Pass10941 qutrit registers by the seven nonzero vectors of
F2^3.  The repo's cyclic Fano lines become exactly the xor-zero triples.

All 168 elements of GL(3,2)=PSL(2,7) act as mode permutations.  Embedded
block-diagonally on the x/z coordinates they preserve the 14-dimensional
symplectic form over F3 and conjugate F_i, P_i and CZ_ij equivariantly.

The 21 unordered register pairs form one orbit; the 42 directed pairs form one
orbit.  The full pair graph is K7, which is the 1-skeleton of the Csaszar
seven-vertex torus triangulation.  The two cyclic Fano heptads provide its 14
faces and every K7 edge occurs in one face of each heptad.
Pass10941 is more economical than that physical completion: its exact lowering
uses only the six pair couplers

    01, 12, 23, 34, 45, 56,

a Hamiltonian path P7, yet already closes the full seven-qutrit Clifford target.
Thus the remaining fifteen K7 couplers are a symmetry/routing completion rather
than an algebraic universality requirement.

Producer: analysis/w33_20260924_fano_seven_qutrit_vm_fabric.py

## 3. The eight E8 leaves and seven VM modes are one affine F2^3 codec

The eight Eisenstein W33 leaves through the fixed temporal Hesse A2^4 are an
affine F2^3 torsor.  The seven VM registers are now assigned to the seven
nonzero translation directions of that same torsor.

From every base leaf x, mode address v points objectwise to the unique leaf
x+v.  The E8 overlap metric is then visible directly on the seven VM labels:

    overlap 13: 100,010,001,111  -> modes 0,1,2,5
    overlap  4: 110,011,101      -> modes 3,4,6.

The three second-row vectors sum to zero and form one Fano line.  Their four
complementary directions are the four-point affine cap.
This explains the Pass7409 symmetry reduction objectwise.  The full Fano
linear group has order 168.  Stabilizing the E8-selected Fano line reduces it
to an order-24 S4, acting faithfully on the four-point complement.  Adjoining
the eight affine leaf translations gives

    2^3:S4 = W(D4), order 192,

exactly the previously certified full orientation-fibre image.

Producer: analysis/w33_20260924_leaf_fibre_fano_vm_bridge.py

## 4. BT1349 correction

Replaying proofs/bt1349_multi_photon_toroidal_scaling.py exposed an old
inconsistency.  The script correctly stated that every pair of Fano points lies
on one line, but then incorrectly asserted that point adjacency by sharing a
line is 3-regular.  That adjacency is necessarily K7 and has degree 6.

The repaired witness now uses all 21 pair channels, spectrum 6^1+(-1)^6,
diameter one, and still obtains Schmidt rank three across every one-qutrit
versus six-qutrit cut.  The seven Fano lines partition the 21 pair channels
into seven triples.

The correction strengthens the new VM bridge: its 21-coupler completion is
exactly the corrected Fano/K7/Csaszar network, not the old fictitious
3-regular point graph.
## 5. BT1348 was also a legacy witness, not a full qutrit QEC proof

The same replay discipline exposed three independent BT1348 overclaims.

First, with its declared convention X|k>=|k+1> and Z|k>=omega^k|k>,
the correct Weyl relation is XZ=omega^-1 ZX, not XZ=omega ZX.

Second, span{|000>,|111>,|222>} with the two Z-difference checks is a
ternary repetition subspace that detects one-site X shifts, not a full
[[3,1,2]]_3 quantum code.  A one-site Z phase preserves both checks while
acting nontrivially on the encoded qutrit.

Third, the BT1340 routing permutation is unitary but does not preserve that
repetition subspace: the equal logical superposition has exact post-routing
subspace weight 2/3.

This does not invalidate the later BT3715 [[3,1,2]]_3 construction.  BT3715
uses a different three-term logical basis and explicitly passes all 27
Knill-Laflamme conditions for one known qutrit erasure.

Finally, 1+12+27=40 is a valid W33 shell identity, but 36 != 12+27.  Shell
sizes alone neither prove QEC correctability nor eliminate the non-Clifford
resource.  The current ADQC/Pass10941 resource boundary therefore supersedes
the old BT1348 no-factory inference.

Producer: analysis/w33_20260924_bt1348_bt1349_errata.py

## 6. External cross-check

The architecture remains compatible with independent quantum-computing results:

- Proctor et al., Phys. Rev. A 95, 052317 (2017), establish ancilla-driven
  qudit computation from one fixed ancilla-register interaction, ancilla
  preparation, local ancilla measurement and classical feed-forward.
- Glaudell, Ross, van de Wetering and Yeh, arXiv:2202.09235, establish the
  qutrit Clifford+T universality lane and the role of qutrit T as an injectable
  non-Clifford resource.
- Revis, Zakaryan and Raissi, arXiv:2506.05478, classify local-Clifford orbits
  of qutrit graph states through seven qutrits, independently confirming that
  seven-qutrit graph-state structure should be analyzed up to qudit local
  complementations rather than inferred from connectivity alone.

These papers support the computational ingredients, not the new W33/E8/Fano
identifications, which are repository-derived certificates.

## 7. M36 is objectwise the temporal 36

The explicit Witting-to-W33 isomorphism admits a symplectic quarter-turn
J(a,b,c,d)=(c,d,-a,-b) that sends the four Witting coordinate axes exactly
onto the temporal Bell line B.  The remaining 36 Witting/M36 rays therefore
map bijectively to the 36 W33 points off B.

For each off-B point P, the three history lines through P that are disjoint
from B are exactly one temporal triangle.  Hence there is now an explicit
dictionary

    M36 ray_id -> Witting ray -> W33 point off B -> temporal triangle.

The four nine-ray M36 families are exactly the four nearest-point fibres over
the four Bell-line points.  This is a finite-geometry identification only;
the M36 two-qubit/ququart resource is not retyped as qutrit magic.

Producer: analysis/w33_20260924_m36_temporal_triangle_dictionary.py

## 8. The tempting E6-affine-36 identification is false

The temporal 36 triangles and the E6 affine 36 triads have the same coarse
shadow: 27 vertices, degree 8, 108 edges, 36 triangles, and adjacency spectrum
8^1+2^12+(-1)^8+(-4)^6.  They are nevertheless nonisomorphic.

Their nonedge common-neighbour histograms separate them exactly:

    temporal Q-side: {2:162, 4:81}, diameter 2
    E6/W33 point-side: {0:27, 3:216}, diameter 3.

The 27 zero-common-neighbour E6 pairs are precisely the pairs in the nine
firewall fibre triads. Adding those nine triads closes SRG(27,10,1,5).
Thus temporal-36 and E6-affine-36 are a cospectral point/line-dual firewall
pair, not the same incidence geometry.

Producer: analysis/w33_20260924_temporal_e6_dual_residue_firewall.py

## 9. Even the two order-1296 residue automorphism groups differ

The graph firewall lifts to the symmetry groups.  Both 27-vertex graphs have
full automorphism group order 1296 and vertex stabilizer order 48, but the
groups are nonisomorphic.

The temporal Q-side group has regular translation kernel C3^3 and split
stabilizer PGL(2,3)xC2 ~= S4xC2.  The E6 point-side group has regular
nonabelian Heisenberg kernel H27 and stabilizer GL(2,3).  Element orders expose
the split directly: the temporal full group has no order-8 elements, while the
E6 group has 324; their order-48 stabilizers have 0 versus 12 order-8 elements.

Producer: analysis/w33_20260924_temporal_e6_aut_group_firewall.py

## 10. M36 is the complete 36-line null atlas of finite history space

The M36 dictionary sharpens once the 27 histories are viewed as
Sym2(F3) ~= F3^3 with determinant quadratic form q(a,b,c)=ac-b^2.
There are exactly four projective null directions.  For each M36 family, all
nine corresponding temporal triangles are the nine parallel affine lines in
one null direction, and they partition the 27 history points.

Thus

    36 M36 rays = 4 null directions x 9 affine null lines/direction.

The four family directions are exactly the four P1(F3) directions already
identified with the four Hesse striations and four temporal-Hesse A2
components.  Within each family the native (mu,nu) ray coordinates are related
to the quotient plane F3^3/<null direction> by an explicit invertible affine
2x2 map.

Producer: analysis/w33_20260924_m36_null_line_atlas.py

## Boundary

The packet proves finite chain, incidence, group-action and controller-address
statements.  It does not derive a continuum time coordinate, identify seven
qutrit modes with seven physical particle species, or show that the full K7
coupler fabric is required in hardware.  In fact the Pass10941 compiler proves
the opposite algebraically: six pair couplers already suffice for its Clifford
closure, while K7 restores the full Fano routing symmetry.
