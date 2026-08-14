# Passes 5074–5081 — coarea derivative, q4 shell rigidity, quadratic order, compiler Pareto, Tanner closure, and three outside-box probes

**Status:** EXECUTED 2026-08-14.  The promoted statements are finite combinatorics, exact linear algebra/group arithmetic, or explicitly bounded search statements.  The all-q minimum-distance theorem and the heavy-chart part of the q=4 minimum shell remain open.

## 5074 — the all-q distance wall is a block-support/coarea derivative problem
For a binary Levi cohomology class and an opposite same-type vertex pair O, compare the parities along its q+1 length-four geodesics.  Modulo a common flip these q+1 values define a cut of K_{q+1}.  If the smaller cut side has size s_O, the number of selected apartments in that chart is

`w_O=s_O(q+1-s_O)`.

Every apartment belongs to exactly four opposite-pair charts, hence the exact coarea identity

`4 wt(x)=sum_O w_O`.

If `A(x)` denotes the number of active charts, every active chart contributes at least q, so `wt(x)>=q A(x)/4`.  Therefore the outstanding family theorem `d=q^4` is equivalent to proving the concentrated block-support inequality `A(x)>=4q^3` for every nonzero class.  A chamber class has `wt=q^4`, exactly `4q^3` active charts, and every active chart is a minimum `1|q` cut, so equality is attainable.

At q=2 the entire 2^16-word code was enumerated: among 65,535 nonzero classes, minimum apartment weight is 16, minimum active-chart support is 32, there are exactly 45 minimizers, and in fact `A(x)=2 wt(x)` for every word because every nonzero K3 cut has weight two.  The all-q block-support inequality remains open.

## 5075 — q=4 local-minimum shell rigidity
Pass5056 gives `[13600,256,256]_2`.  Assume a weight-256 word has only inactive charts and minimum `1|4` cuts.  Fix one selected apartment by transitivity.  It lies in four charts, and in each chart its local K5 edge has two possible singleton endpoints, giving 16 seeds.  Exact chart-state propagation gives exactly eight satisfiable seeds and eight inconsistent seeds.  The eight satisfiable supports are precisely the eight chamber stars through the fixed apartment.

Thus any non-chamber weight-256 word must contain a heavier `2|3` chart.  If `A2=2t` is the number of heavy charts, the coarea identity forces

`A1=256-3t`, `A_active=256-t`.

The supported local Tanner-triangle count is correspondingly `1024-8t`, versus 1024 for a chamber star.  This reduces the unresolved q=4 shell to a sharply defined heavy-chart sector instead of a 13,600-bit blind search.

## 5076 — sqrt(17) is an integral quadratic-order bridge
On the quadratic twisted-Hecke channel let

`A=[[1,4],[1,0]]`,  `chi_A=x^2-x-4`.

For the corrected historical q=2 transfer matrix `B2=[[4,2],[2,5]]`, define `C=B2-4I`.  The integral matrix

`P=[[2,-1],[-1,1]]`, `det P=1`

satisfies `A P=P C`.  Hence the two Z-lattices are integrally conjugate, not merely rationally similar.

Writing `lambda=(1+sqrt(17))/2`, the maximal order is `O_K=Z[lambda]` with discriminant 17.  The q=3 recurrence polynomial is obtained from `mu=10+4lambda`:

`mu^2-24mu+76=0`.

Therefore `Z[mu]=Z+4 O_K` is the conductor/index-four order and has discriminant `4^2*17=272`.  This gives an exact arithmetic explanation for the corrected historical discriminants 17 and 272.  It does not resurrect the retracted p=5 discriminant claim, and no PSp-equivariant geometric intertwiner is asserted: the older transfer recurrence was not supplied with such a group action.

## 5077 — denominator-780 raw compiler is a strict one-swap local optimum
The Smith-floor raw 24-apartment V24 basis from Pass5070 has inverse denominator 780 and condition number about 72382.4833.  Its complete nonsingular one-apartment-swap neighborhood contains 3,289 distinct bases; only eight retain exact denominator 780.  The best *other* denominator-780 one-swap basis has condition number about 74483.1939.  Hence the frozen floor basis is a strict one-swap local optimum for numerical conditioning subject to the exact arithmetic floor.

A seeded two-swap search screened 24,547 candidates.  Exact denominator tests on the 1,200 numerically best candidates found no denominator-780 basis; the best numerical condition encountered without the denominator constraint was about 102.57.  This is search evidence, not a proof of the global denominator-780 conditioning optimum.  The denominator-3120 raw basis from Pass5070 remains a useful balanced control at condition about 105.4622.

## 5078 — all-q Tanner six-cycle law
Let the apartment point graph join two apartments when they share a length-four root (equivalently, when they occur together in a theta check).  If `A=P∪Q` and `B=P∪R` share root P, a third apartment adjacent to both is either `Q∪R`, producing the one theta-check triangle, or `P∪S` for one of the remaining q-2 complementary roots S.  Girth eight and uniqueness of paths shorter than four exclude crossed alternatives.  Thus every apartment-point edge lies in one theta triangle and q-2 Tanner-six-cycle triangles.

Equivalently every apartment-point triangle is either a single theta triple or three apartments sharing one root.  Since the number of roots is `q^3(q+1)^2(q^2+1)`, the Tanner-six-cycle count is

`q^3(q+1)^2(q^2+1) C(q,3) = T(q)(q-2)`,

where `T(q)=q^3(q+1)(q^2+1) C(q+1,3)` is the theta-check count.  The exact anchors are 0, 4320, 108800 and 1170000 at q=2,3,4,5.

## 5079 — outside box: the derivative observation is structurally real
For a fixed chamber, exactly `q^4` apartments contain it.  Each such apartment contributes one chart of each of four incidence roles: point endpoint, point interior, line endpoint, line interior.  In a fixed role an active chart contains q chamber-star apartments because its local cut is a `1|q` star.  Double-counting therefore gives exactly `q^3` active charts in each role:

`q^3+q^3+q^3+q^3=4q^3`.

So the formal equality `d(q^4)/dq=4q^3` has a literal finite-geometric shadow: `q^4` is the chamber-star volume and its four codimension-one/root-direction sheets each have size `q^3`.  This is a discrete coarea derivative, not infinitesimal calculus in the prime-power parameter q.

Exact role counts are `8+8+8+8` at q=2, `27+27+27+27` at q=3 and `64+64+64+64` at q=4.  At q=3 the chamber stabilizer has a normal unipotent subgroup U of order 81 acting regularly on the 81 chamber-star apartments; U has element orders `1^1 3^44 9^36`, center order 3 and derived subgroup order 9, and the local switches split into four order-three root directions.

## 5080 — outside box: a noncommutative discrete Hessian
The four root directions are not Cartesian coordinates.  At q=3 the six subgroups generated by pairs of root directions have orders

`9,9,9,9,27,81`.

Thus four direction pairs close at the naive `q^2` size, one grows through a commutator layer to `q^3`, and one generates the full `q^4` unipotent carrier.  At q=2 the corresponding fingerprint is `4,4,4,4,4,8`.  This is a concrete finite-difference/root-commutator analogue of an anisotropic Hessian: second-direction composition detects the curvature of the C2 building rather than a flat four-dimensional grid.  The calculus language is interpretive only; the subgroup orders are exact.

## 5081 — outside box: the derivative carrier is not a four-dimensional Hamming cube
Form the chamber-star switch graph by joining two star apartments when they differ within one active root chart.  Its vertex count is q^4 and degree is `4(q-1)`, exactly what H(4,q) would have, but its spectrum is different.

- q=2: `chi=(x^2-16)(x^2-4)^2 x^2 (x^2-2)^4`; this 16-vertex degree-four graph is not Q4.
- q=3: `chi=(x-8)(x-5)^4(x-2)^10(x+1)^18(x+4)^12(x^2-4x+1)^6(x^2+2x-2)^6(x^2-x-8)^6`; it is not H(4,3).
- q=4: `chi=(x-12)(x-8)^6(x-6)^24(x-4)^9(x-2)^24 x^84(x+4)^72(x^2-8)^18`; it is not H(4,4).

The derivative really does have four root directions, but the local q^4 carrier is curved/non-Cartesian.  This is also a firewall against identifying the q=2 support graph with the hypercube solely from the shared `16 vertices / degree 4` count.

## Evidence boundary
The derivative statement is an exact combinatorial coarea/root-sheet identity, not a claim that q is a continuous physical coordinate.  The all-q apartment minimum distance still requires the global active-chart inequality.  At q=4 the local-minimum sector is classified, but heavy `2|3` cuts remain the only possible source of exotic minimum words.  The sqrt(17) bridge is arithmetic/integral, not yet a geometric group intertwiner.  The denominator-780 two-swap result is sampled evidence, whereas the one-swap local optimum is exhaustive.
