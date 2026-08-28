# Five-front closure: trade lattice, S5 carrier, q=5 defect, and tensor shadows

Date: 2026-08-28

This note records the five requested non-sequential continuations after the
optimal near-ovoid / native T(10) packet.  It reconciles the concurrent
Holotrade near-ovoid/minimum-blocker correspondence rather than duplicating it.
Every statement below is finite/exact unless its boundary explicitly says
otherwise.

## 1. The missing ten-set intertwiner: exact C2 boundary

The ten native code-stratum fibres are not an arbitrary ten-set.  The
stabilizer of the singular F2^6 translation vector 4 has order 1920, kernel 16
on the ten fibres, and image S5 of order 120.  HJ10's certified residual C2 has
profile `1^2 2^4`; inside the native S5 this is exactly the 15-element
double-transposition class.  For a selected target double transposition there
are

`2! * 4! * 2^4 = 768`

C2-equivariant bijections, and 11,520 if the target involution is not selected.
No present datum distinguishes one of them.  The natural P1(F9) split
centralizer contains an order-eight rotation, whereas S5 has no order-eight
element, so the residual C2 cannot extend to the natural D16/C8 projective
centralizer.

Source/certificate:
- `38a6fa722e33c3370953241d79609755c025d098`
- `c17608784aa3234e980fb6ffbc7ca81bf931da20`

Boundary: no HJ S5 action is claimed.  The maximal currently certified shared
action is the residual C2.

## 2. The rank-15 trade lattice is the integral E15/GQ(4,2) carrier

The primitive incidence-kernel lattice has minimum squared norm 8, exactly 90
signed minima, and 45 antipodal minimum-vector lines.  Those 45 lines are
literally the previously constructed 45 dual flat-tetrad pairs.  Their
orthogonality graph is `SRG(45,12,3,3)` and their nonorthogonality graph is
`SRG(45,32,22,24)`.

The minimum vectors already generate the full integral rank-15 lattice.  Its
determinant and discriminant group are

`det = 2^17 * 3^10 = 7739670528`,

`A_L = (Z/2)^5 x (Z/6)^9 x Z/24`.

PSp(4,3) is transitive on the 45 unsigned minima with stabilizer 576, and on
the 90 signed minima with stabilizer 288.  Every one of the 7,200 local
near-ovoid pair trades has a unique decomposition as a sum of two signed
minimum vectors of inner product -2.

The real span is the historical E15 carrier because
`24 P_{-4} = 8I + J - 4A`.

Source/certificate:
- `747a159dea67c6ffea96beaf2560991a4c9f252d`
- `f5837a8abfac436bf8ea061e89daf8fcee928a36`

Boundary: this is an integral finite-lattice/incidence identification, not a
physical Hilbert-space claim.

## 3. W(3,5): deficiency six is impossible

The earlier support theorem gave `def(W(3,5)) >= 6`.  At deficiency six, the
eigenfunction shell equation forces maximum defect magnitude one, so the
positive and negative supports are six-line sets with minimum internal degree
four.  Generalized-quadrangle incidence forces each sign support to be a full
six-line pencil, and their centres must be noncollinear.

Thus all deficiency-six candidates form one PSp(4,5) orbit of occupancy
targets: zero on one full pencil, two on a noncollinear full pencil, one on the
other 144 lines.  Symplectic transvections are transitive on all 19,500 ordered
noncollinear centre pairs.  Exact backtracking rejects the representative.
Therefore

`7 <= def(W(3,5)) <= 12`.

Source/certificate:
- `b85825483f6712834993ae36eeee242ef1ecc9d8`
- `a9cef9dbf3f0073ff509ae6b34c256f40af8ac5f`

Holotrade reconciliation:
- `571015b51fa38a3f60108ed39bcdb83398bae173`

Boundary: deficiency seven is not claimed attainable; 12 remains the existing
feasible upper bound.

## 4. The 360x8 cover produces an exact shadow-only tau2=110 formulation

The concurrent Holotrade commit
`689684b1d1e461642a428b1d8235e06c9545e9b1` proved the bidirectional map between
360 minimum blockers and 2,880 near-ovoids, with eight admissible deletions per
blocker.  The depth-2 continuation uses that theorem rather than re-owning it.

At equality `|X|=110`, assign one minimum blocker `B_L` to each first-coordinate
line and put `H_q={L:q in B_L}`.  A tight blocker exists iff every `H_q` is the
union of complete four-line pencils centred at an independent W33 set.  Given
those centres `C_q`, the leaves reconstruct as `X={(p,q):p in C_q}`.  The row
shadow of every line is then exactly `B_L`, and the size is automatically 110.

The exact pencil-union code contains 40,055 independent centre sets producing
37,850 distinct line masks.  A frozen negative control satisfies the old
`|H_q| divisible by 4`, `|C_q|<=7`, and total-size-110 conditions but fails the
new pencil-union condition on 21 of its 29 nonempty coordinates.  Hence the
new obstruction is strictly stronger than the old degree-only relaxation.

The 360x8 cover yields 320 labelled near-ovoid predecessor incidences per axis
at equality.  At size `110+s`, at least `40-4s` shadows per axis are minimum,
so at least `8(40-4s)` predecessor incidences survive.  The current 115 witness
has 33 minimum shadows on each axis and 264 such incidences per axis.

Holotrade source/certificate:
- `8d56c6b6e2c9ec5b0883f5ccac293481aed2cdbb`
- `b8c32b4e520d568a8477381c2ef7336de8e87dd9`

Boundary: this is an exact equivalent reformulation of the 110 case, not yet a
proof of feasibility or infeasibility.  The depth-2 interval remains
`110 <= tau_2 <= 115`.

## 5. The native T(10) is exactly the repository's S5 duad target

The intrinsic graph on the ten `{x,x+4}` fibres is
`T(5)=SRG(10,6,3,4)` with Petersen complement.  It has exactly five maximal
K4s; those five K4s form a canonical five-set, and each fibre lies in exactly
two K4s.  Hence each fibre is canonically a duad of that five-set.  The induced
action on the five K4s is all S5.

This identifies the native code-stratum T(10) carrier with the literal
`k5_edges=C(5,2), n10=10` target already used by
`analysis/w33_s6_to_s5_branching_gauge.py`.  The old S6-to-S5 branching map and
the new code-stratum T(10) therefore meet on the same ten-state carrier, up to
the now-explicit duad coordinates rather than by cardinality alone.

Source/certificate are the same exact action packet as Front 1:
- `38a6fa722e33c3370953241d79609755c025d098`
- `c17608784aa3234e980fb6ffbc7ca81bf931da20`

## Evidence status

All numerical/theorem claims above were independently recomputed while the
packet was constructed and are frozen in executable source plus JSON
certificates on `master`.  At the final status check, GitHub's combined-status
endpoint returned no status records for the newest W33 and Holotrade commits;
therefore this note does not claim a new remote CI/Actions run for this packet.
