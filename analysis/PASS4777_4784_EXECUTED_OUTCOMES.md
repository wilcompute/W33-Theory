# Passes 4777–4784 — executed outcomes

## 4777 — the M2(Q) block now has literal matrix units

The unique noncommutative factor of the 270-residue orbital algebra is no longer only identified abstractly.  Let `E40` be the rank-40 central idempotent from Pass4753 and let `A_hot`, `A_cold` be the degree-3 and degree-12 orbital adjacency elements.  Define

`e11 = (1/5) E40 (A_hot + 2 E40)`,  `e22 = E40-e11`,

`e12 = e11 A_cold e22`,  `e21 = (25/324)e22 A_cold e11`.

Exact orbital-algebra multiplication gives

`e_ij e_kl = delta_jk e_il`.

Thus these four rational elements are literal matrix units for the `M2(Q)` factor.  The PGSp/PSp outer involution fixes all four pointwise.  On the 12 orbital basis relations it fixes 0–7,10,11 and swaps only 8 and 9.  Therefore the multiplicity-two 20-dimensional block responsible for `1±sqrt(13)` is **not** where the outer twist lives.

## 4778 — minimum kernel words are BLT-sets; q=5 has two classes

Equality in the Pass4754 bound `d=q+1` is exactly the BLT condition: `q+1` pairwise-skew lines of `W(3,q)` such that every external W-line meets zero or two selected lines.

At q=3, direct enumeration gives 270 minima in one PSp orbit; every support has Plücker span rank 3 and is planar.

At q=5, a weight-6 kernel MILP followed by PSp orbit closure gives two orbits.  Their sizes are

- 6,500, stabilizer 720, Plücker span rank 3;
- 13,000, stabilizer 360, Plücker span rank 5.

A second exact MILP excluding all 19,500 supports is infeasible, so the two orbits are complete.  These align with the classical **Linear** and **Fisher/Fi** BLT classes.  Betten's small-order BLT classification lists exactly two q=5 classes with full semilinear/orthogonal automorphism orders 1440 and 720, respectively; our PSp stabilizers are the index-two intersections 720 and 360.  The BLT names/classification are prior art.  The repository contribution here is the explicit identification of minimum line-kernel words with BLT-sets and the independent MILP/PSp certificate.

## 4779 — the entire rational 24D orthogonal module is not Leech

The 45-vector quotient of Pass4759 gives an integral Gram

`G45 = 15 I - 5 A45 + J`, where `A45 = SRG(45,12,3,3)`.

It has rank 24 and determinant

`2^10 * 3^10 * 5^23`.

Hence its determinant square class in `Q*/(Q*)^2` is 5.  A rational change of basis multiplies determinant by a square; scaling a 24-dimensional form by rational `c` multiplies determinant by `c^24`, again a square.  Therefore the square class 5 is an invariant of the whole rational quadratic space.  The Leech lattice is unimodular, square class 1.  Consequently **no commensurable lattice in this rational orthogonal module, under any rational scaling, is rationally isometric to Leech**.

This strengthens Pass4755 from a canonical-lattice no-go to a rational-form no-go.  ATLAS nevertheless lists a 24-dimensional integral representation of `U4(2)`, so this does not deny other abstract 24D representations; it blocks this particular repository orthogonal constituent as the Leech representation.

## 4780 — the dependency-cube stabilizer is W(D4), with literal triality

The PSp stabilizer of one of the 135 dependency cubes has order 192.  Its action on the cube's six residue vertices has image order 24 with S4 element-order census, in the six-edge action of a tetrahedron.  The kernel has order 8 and consists of the identity plus seven involutions, hence `C2^3`.  An actual order-24 complement is found, so

`H_cube = 2^3:S4 = W(D4)`.

This W(D4) fixes exactly three cube vertices in the 135-cube action.  Their setwise stabilizers are

- order 576 in PSp, quotient `C3` over W(D4);
- order 1152 in PGSp, quotient `S3` over W(D4).

Thus the repository's old D4/triality motif is now a literal subgroup tower rather than a numerical analogy.

## 4781 — exact covering-radius bracket and syndrome ceiling

The H10 adjacency code remains `[40,10,12]`.  The explicit coset representative

`253626779097`

has minimum distance 14 from H10, with coset weight distribution

`14:64, 16:128, 18:192, 20:256, 22:192, 24:128, 26:64`.

So `rho(H10)>=14`.

Because `d(H10^perp)=4`, every H10 coset is an orthogonal array of strength 3.  The first three Krawtchouk moment equations, together with complement symmetry from the all-one word, have no nonnegative solution for a hypothetical coset whose minimum is at least 17.  Hence

`14 <= rho(H10) <= 16`.

The exact value 14/15/16 remains open in this pass.

For the `[270,30,27]` syndrome code, all 540 dependency triangles impose even syndrome parity.  Every syndrome coordinate lies in six dependency triangles, so incidence counting gives syndrome weight at most 180.  Equality would force the 90 zero coordinates to meet every dependency triangle exactly once.  A 270-variable exact binary MILP proves this exact transversal infeasible.  Therefore

`wt(syndrome) <= 179`,

and the commuting parity Hamiltonian `H=-270+2s` has certified energy ceiling `88`.

## 4782 — bonkers: the 270 residues are exactly the triangles of the 45-point quotient

The three-cube W(D4) packets form 45 vertices.  The selected135 intersection-4 graph projects with exactly three edges above every quotient edge, producing `SRG(45,12,3,3)` with 270 edges.

Each residue lies in exactly three dependency cubes.  Those cubes lie in three distinct W(D4) packets, and the three quotient vertices form a triangle.  The 270 resulting quotient triangles are distinct.  `SRG(45,12,3,3)` itself has exactly 270 triangles, so

`{270 involution residues} = {270 triangles of SRG(45,12,3,3)}`

under an explicit PSp-equivariant construction.

## 4783 — bonkers: the 27 Petersen fibers are the 27 maximal K5s

The 45-point quotient has exactly 27 maximal cliques, all K5.  Every one of its 270 triangles lies in exactly one K5.  Each K5 contains ten triangles.  Put two of those ten triangles adjacent when they intersect in exactly one quotient vertex: the resulting ten-vertex graph is Petersen.

Taking all 27 K5s gives exactly the 405 hot edges of the selected270 router.  Thus the prior 27 Petersen fibers are simply the triangle/Kneser geometry internal to the 27 maximal K5s of the 45-point quotient.

## 4784 — bonkers: the outer involution is a triangle-chirality reversal

For every vertex of `SRG(45,12,3,3)`, its 12-neighbor graph is exactly `3 K4`.  In the 270-triangle model:

- triangle pairs sharing a quotient edge form residue orbital 5, subdegree 6;
- pairs sharing exactly one quotient vertex split into orbitals 1,8,9,11;
- orbital 1 is the cold relation, subdegree 12;
- orbital 11 is the hot/K5-Petersen relation, subdegree 3;
- orbitals 8 and 9 are a paired directed relation, each subdegree 12.

The PGSp/PSp outer involution fixes the shared-edge, cold, and hot relations and swaps **exactly** `8 <-> 9`.  Therefore its simplest nontrivial action in the residue router is a reversal of this paired triangle chirality, not an action on the M2 multiplicity space.

## Evidence and claim boundaries

All finite statements are backed by executable scripts in `analysis/w33_pass4777_*.py` through `analysis/w33_pass4782_4784_*.py` and frozen JSON certificates.  The q=5 Linear/Fisher names and small-order BLT classification are classical prior art.  The 24D conclusion is a rational orthogonal-form obstruction, not a ban on every abstract U4(2) representation in dimension 24.  Pass4781 intentionally leaves the covering-radius equality unresolved.
