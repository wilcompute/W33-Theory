# Pass5704–5711 — Wilson transport, magnetic group bridge, Ramanujan 2560, L∞ correction, and generation symmetry

Status: **structurally closed; dedicated replay/publication CI pending**.

This packet executes the five carry-forward targets after Pass5691–5698 and three deliberately high-risk physics probes. It also repairs two inherited reproducibility/algebra issues rather than preserving attractive but incorrect readings.

## Pass5704 — finite adjoint SU(3) Wilson transport; face selection remains two-principle

The affine nine-site carrier has `K9` link space with 36 links and 28-dimensional real cycle space. The two repo-native 2-cell families are different:

- the E6 allowed36 cubics descend to **12 affine lines**, three lifts per line;
- affine translation geometry gives **54 parallelogram plaquettes**.

Their boundary ranks over `R` are respectively 12 and 24, while the combined 66-face system has rank 28. Therefore

- line triangles alone leave 16 harmonic 1-modes;
- translation plaquettes alone leave 4;
- the combined system leaves 0 over `R`.

The exact compact affine bracket was exponentiated in the adjoint representation. For `theta=1/8`, two noncommuting affine generators give a finite Wilson group commutator with distance from identity about `0.72121354`, while an explicitly constructed pure-gauge triangle closes to identity numerically. This is a real finite `Ad(SU3)=PSU3` transport carrier.

**Selection boundary:** E6 selects the 12 line faces; translation locality selects the 54 plaquettes. No theorem currently fixes the combined face action, relative weights, or physical coupling `g`.

## Pass5705 — the magnetic 192 is a direct-product doubling over the cube/frame quotient

For the signed Segre stabilizer `G96`:

- order `96`;
- center order `2`;
- derived subgroup order `24`;
- element orders `1^1 2^15 3^8 4^24 6^24 8^24`.

Quotienting the central sheet sign gives a projective group of order 48. The code constructs an explicit central `C2` and complementary `S4` subgroup, proving

`G96/<-I> ≅ C2 × S4 = O_h`,

the repo's cube/frame controller.

The derived 24 contains a closed `Q8` formed by its elements of orders 1,2,4, and quotient by that `Q8` has order 3 with nontrivial action. Thus

`G96' ≅ Q8:C3 ≅ SL(2,3)`.

Pass5692's diagonal involution `D` centralizes all of `G96`, has order two, and is not in `G96`. Hence, without any classification lookup,

`<G96,D> = G96 × C2`

of order 192. Its center has order 4 and its derived subgroup remains order 24.

This **is not** the tomotope order-96 group and **is not** `W(D4)` merely because 96/192 recur. The bridge is the exact quotient to `C2×S4` and the exact direct-product doubling.

## Pass5706 — reproducible Ramanujan tower through 2560; matching colors are gauge

A hidden reproducibility issue was found in Pass5693. For a bipartite signed graph, complementary signings `sigma` and `-sigma` are switching-equivalent, so the six two-of-four matching choices occur in pairs

`01~23`, `02~13`, `03~12`.

Their spectra are equal, but raw floating roundoff could select either labeled representative. Since the next deterministic perfect-matching factorization depends on vertex labels, this harmless gauge choice altered later numerics.

Pass5693 is now patched to fix the complement gauge canonically with representatives `01,02,03`. Under that convention the selected signed radii are approximately

| parent | selected signed radius |
|---:|---:|
| 160 | 3.4232028039 |
| 320 | 3.3960725809 |
| 640 | 3.4539332142 |
| 1280 | 3.4467824163 |

all below `2 sqrt(3) ≈ 3.4641016151`.

The explicit connected W33-rooted hierarchy therefore reaches

`80 -> 160 -> 320 -> 640 -> 1280 -> 2560`

with nontrivial graph radii approximately

`2.44949, 3.28377, 3.42320, 3.42320, 3.45393, 3.45393`.

**Recursion no-go:** `S4` relabels the four factor matchings transitively on the three `2+2` partitions. The deterministic color sequence is a gauge convention, not an automorphism-invariant finite-state law. Any genuine recursive theorem must be phrased in intrinsic switching-class data.

## Pass5707 — correction: `l1=0` forbids the advertised `l3` Jacobi repair

The existing `tools/build_linfty_firewall_extension.py` explicitly states `l_1=0`, uses a firewall-filtered `l_2` with nonzero Jacobiator, and presents `l_3` as repairing that anomaly.

For an ordinary uncurved L-infinity algebra, the arity-three relation schematically contains

`l1(l3) + sum_cyclic l2(l2) + sum_cyclic l3(l1,...) = 0`.

Therefore when `l1=0`, all `l3` terms vanish from this identity and `l2` must obey Jacobi strictly.

So the stated minimal model has an **empty `l3` repair set** on any triple with nonzero firewall Jacobiator. This supersedes the old confinement/L-infinity reading, while leaving intact the finite bracket-deletion Jacobiator and collision-support calculations.

Valid future routes are:

1. extend the graded space and define nonzero `l1` with `im(J) subset im(l1)`, then solve `l1(l3)=-J`;
2. modify `l2` by a genuine CE coboundary/deformation;
3. specify a different curved/higher structure and verify its identities explicitly.

The repo's later CE2 local solvers may still be useful as **deformation** machinery. Their CE differential is not the unary L-infinity bracket `l1`.

## Pass5708 — the E8 `(27,3)` has a real multiplicity-three, but only relative to E6

For the standard repo branching

`248=(78,1)+(1,8)+(27,3)+(27bar,3bar)`

under `E6 × SU3_family`, the 81-dimensional matter carrier is `27 tensor C3`.

Schur's lemma gives the exact commutant ladder:

- `E6` only: `M3(C)`, dimension 9;
- `E6 × Z3_center`: still `M3(C)`, dimension 9, because the center acts as scalar `omega I3`;
- a generic family torus: `C^3`, dimension 3;
- full irreducible `SU3_family`: `C`, dimension 1.

Thus the three-dimensional factor is a genuine multiplicity space for E6 alone. But an unbroken full family SU3 rotates those three directions irreducibly, so it does not intrinsically label three independent generations.

The affine SU3 of Pass5686/5696 has the correct abstract A2 type and adjoint dimension 8, but **no explicit intertwiner currently identifies it with the E8 `(1,8)` family factor**.

## Pass5709 — bonkers: old Z3 curvature can be SU3-center flux, but the adjoint cannot see it

For the four AG(2,3) directions, the repo connection has oriented plaquette curvature

`h=-det(d1,d2) mod 3`,

with 27 plaquettes of `h=1` and 27 of `h=2`.

Abstractly one may embed

`h -> omega^h I3 in Z(SU3)`.

Then a fundamental Wilson loop has trace `3 omega^h`, but conjugation by any center element acts trivially on `su3`; the adjoint holonomy is identity and its trace is always 8.

So Pass5691's “vertical Z3 is adjoint-trivial” is exactly compatible with a **center-flux interpretation**, but that interpretation is not derived by the adjoint carrier. A triality-nonzero matter representation and an explicit intertwiner are required to observe `h=1` versus `h=2`.

## Pass5710 — bonkers: DK dual rays have the same Pfaffian parity

The two unit-bond magnetic rays are `H=iS` with real skew `S`, finite gap `sqrt(3)`, and levels

`±sqrt(3), ±2sqrt(3)` each with multiplicity four.

Pass5692 gives

`S2=-D S1 D`,

where `D` has eight negative diagonal entries and therefore `det(D)=+1`. For 16-dimensional skew matrices,

`Pf(-A)=(-1)^8 Pf(A)=Pf(A)`

and

`Pf(D A D)=det(D) Pf(A)`.

Hence `Pf(S2)=Pf(S1)`. In the canonical basis both evaluate numerically to `-1296`.

Moreover `D` neither commutes nor anticommutes with one ray. `DK` exchanges `H1` and `H2`; it is not a chiral or antiunitary symmetry of a single Hamiltonian. Thus the two rays are one duality orbit with **no D-protected Pfaffian/Z2 separation**.

This remains a finite Majorana-skew diagnostic unless a physical BdG realization is independently established.

## Pass5711 — bonkers: exact family SU3 forces mass degeneracy

Once E6 irreducibility reduces generation-sensitive operators to Hermitian `3×3` matrices on the multiplicity factor, the real dimensions of the allowed Hermitian operator space are

- no family action: 9;
- center `Z3` only: 9;
- generic family torus: 3;
- full irreducible family SU3: 1.

Therefore exact unbroken `SU3_family` allows only

`M = m I3`,

so all three generation eigenvalues are degenerate. A torus permits three distinct diagonal masses but removes mixing; the center alone leaves arbitrary Hermitian `M3`.

This is a clean symmetry-breaking requirement: **a nondegenerate generation hierarchy cannot coexist with an exact unbroken family SU3 acting in the fundamental**.

## Corrections carried forward

- Pass5693 now fixes complementary-signing switching gauge before recursive lift selection.
- Pass5707 supersedes the `l1=0` L-infinity repair interpretation.
- Neither correction removes the underlying finite graph spectra, E6 36/9 support split, collision mask, or explicitly measured firewall Jacobiator.

## Physics firewall

Nothing in this packet derives QCD, confinement, the Yang–Mills mass gap, a physical value of `g`, observed fermion masses, CKM/PMNS mixing, a physical topological superconductor, or a spacetime continuum. The promoted objects are finite and exactly typed: Lie brackets, Wilson transporters, finite groups, signed graph covers, higher-algebra consistency conditions, commutants, center characters and Pfaffians.
