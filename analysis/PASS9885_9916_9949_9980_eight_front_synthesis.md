# Pass9885–9916 + Pass9949–9980 — eight-front synthesis

Status: **PASS**, with explicit collision reconciliation and evidence boundaries.

This continuation executed the five queued fronts from Pass9725–9788 plus three additional outside-box attacks.  The original atomic reservation was Pass9885–9948 (commit `478a8661...`).  A parallel lane later reserved and landed Pass9921–9944.  Although our reservation was earlier, this lane voluntarily yielded Pass9917–9948 and rehomed its remaining four fronts to Pass9949–9980 so canonical pass names remain unique.  The parallel Pass9921–9944 theorem—type-8 Leech frames bridge to A1^24 2-neighbors whose glue is binary Golay—is used below rather than overwritten.

## 1. Pass9885–9892 — a fully symmetric single plus-polarization is impossible

For fixed glue complex structure R, the plus-type transverse Lagrangians form

\[
U(6,3)/O^+(6,3),\qquad |U(6,3)/O^+(6,3)|=7,530,558,336.
\]

If a faithful finite controller H fixes a plus Lagrangian then H embeds into a conjugate of O+(6,3). More generally every orbit has size at least

\[
|H|/\gcd(|H|,|O^+(6,3)|).
\]

The exact lower bounds are 560 for G2(4):2, 35 for J2:2, and 7 for the G2(4) edge stabilizer. Therefore no full faithful controller can canonically pick one plus Lagrangian. The Witt-sign repair requires symmetry breaking, a nontrivial selected set/orbit, or extra datum.

## 2. Pass9893–9900 — the global 13-state quotient is killed by rank 3

The previous gcd observation

\[
\gcd(4095,416,20800)=13
\]

was only a necessary cardinality condition.  The 416-point G2(4):2 action is rank 3 with point-stabilizer subdegrees

\[
1,100,315.
\]

A block containing a base vertex must be a union of point-stabilizer suborbits, hence has size 1, 101, 316, or 416. A 13-block quotient would require 32 points per block. Thus a full-G2-equivariant 13-state block quotient does **not** exist.

## 3. Pass9901–9908 — explicit F9/local-field intertwiner

The actual Golay/E6 glue matrices from Pass9237–9244 admit a simultaneous Darboux/F9 basis.  Let G be the Golay glue basis and put

\[
P=\begin{bmatrix}G\\GR\end{bmatrix}.
\]

Using the exact Pass9253 identity C_-=G K (G R)^T=I_6, one obtains

\[
P K P^T=J_0,\qquad P R=J_0 P,
\]

where

\[
J_0=\begin{bmatrix}0&I_6\\-I_6&0\end{bmatrix}.
\]

In coordinates z=a+bi in F9^6 with i^2=-1, R is multiplication by i and K is

\[
K(z,w)=\operatorname{Tr}_{\mathbf F_9/\mathbf F_3}\!\left(-i\sum_j z_j\overline{w_j}\right).
\]

For L=Q_3(i,zeta_9), pi=1-zeta_9 satisfies an Eisenstein polynomial reducing modulo 3 to pi^6, so

\[
\mathcal O_L/3\mathcal O_L\cong \mathbf F_9[\pi]/(\pi^6)
\]

and its six coefficient/graded layers are additively F9^6.  This is now an explicit finite-module intertwiner rather than a dimension coincidence.  An integral O_L/Niemeier lattice identification remains open.

## 4. Pass9909–9916 — the two 7,371-candidate schemes are genuinely different

The Q-(5,3) glue selector and Q+(5,3) Suzuki selector both have exactly 7,371 nondegenerate 2-spaces, but exhaustive stabilizer-orbital computation separates their natural coherent configurations.

Using the Gram matrix of [U V] together with its linear-relation kernel, modulo O(C|U) on the base and GL(2,3) on V, gives a complete stabilizer-orbit fingerprint by Witt extension. The orbital ranks are

- Q- hyperbolic base: **39**;
- Q- anisotropic base: **28**;
- Q+ hyperbolic base: **40**;
- Q+ anisotropic base: **27**.

Thus the shared cardinality 7,371 does not lift to an isomorphism of the natural orthogonal two-space schemes. Any weld must use a coarser fusion, broken symmetry, or genuinely external structure.

## 5. Pass9949–9956 — Bargmann orientation replaces absolute phase

The fragile absolute orientation phase is replaced by the qutrit Bargmann/Pancharatnam loop

\[
\mathcal B=\langle\psi_0|\psi_1\rangle
\langle\psi_1|\psi_2\rangle
\langle\psi_2|\psi_0\rangle.
\]

Its phase is exactly invariant under independent U(1) gauge phases on all three ports and under any common U(3) mode rotation. Complex conjugation sends B to its complex conjugate, so sign Im(B) gives a chirality bit whenever Im(B) is nonzero.

For the deterministic seeded stress model the Bargmann classifier scores:

- gauge-only: 2000/2000;
- mild: 2000/2000;
- moderate: 1993/2000 = **99.65%**;
- strong: 1654/2000 = 82.7%;
- extreme: 1107/2000 = 55.35%.

The naive absolute-overlap phase remains near chance under arbitrary local phases. These are simulation results, not hardware measurements or statistical guarantees.

## 6. Pass9957–9964 — 13 survives as a semiregular clock

Although a global 13-block quotient is impossible, every order-13 subgroup of G2(4):2 acts fixed-point-freely on both the 416 vertices and 20,800 edges because neither the vertex stabilizer J2:2 nor the edge stabilizer has a factor 13. Hence a chosen C13 gives

\[
416=32\cdot13,\qquad 20800=1600\cdot13,\qquad 41600=3200\cdot13.
\]

So the carrier decomposes into 32 vertex clocks, 1,600 edge clocks, and 3,200 flag clocks of length 13. Since 13=q^2+q+1 for q=3, a chosen orbit can carry a PG(2,3)/Singer-cycle labeling. This requires a choice of C13/orbit; it is not a G2-invariant block quotient.

## 7. Pass9965–9972 — finite-field norm parity is an exact gauge-invariant C2

In F9^x, the norm

\[
N(z)=z^4:\mathbf F_9^\times\to\mathbf F_3^\times\cong C_2
\]

is surjective. Its kernel is exactly

\[
\{1,-1,i,-i\}\cong C_4,
\]

the finite unitary phase group generated by the glue complex structure. Therefore

\[
N(uz)=N(z)\quad\text{for every }N(u)=1.
\]

The two norm cosets provide a canonical binary phase-parity channel immune to the whole norm-one gauge. In the unramified local lift Q3(i), this is the Teichmuller quotient mu_8/mu_4=C2. Mapping the repository orientation bit into these norm cosets is a proposed encoding, not yet a hardware-derived identity.

## 8. Pass9973–9980 — V2 has a multiplicative C13 clock, not an additive 13-quotient

Parallel Pass9861–9884 independently falsified the sampled law that the frame-pair relation depends only on the sum class: at 34 sampled classes there are at least three relation types and six conflicting shared sums.  In addition, V2=(F2)^12 has additive order 4096, coprime to 13, so there is no nontrivial additive homomorphism V2 -> C13.

But 13 survives linearly because

\[
\operatorname{ord}_{13}(2)=12.
\]

Hence Phi_13 is irreducible over F2. The 12x12 companion matrix of Phi_13 has order 13, and every nonidentity power M^k has rank(M^k-I)=12. Thus its action is fixed-point-free on V2\{0}, giving

\[
4095=315\cdot13
\]

thirteen-cycles.  Interpreting nonzero V2 directions through parallel Pass9921–9944 as type-8 frame/A1^24-neighbor directions yields the common semiregular clock architecture

\[
315\quad\text{V2 frame/neighbor clocks},\qquad
32\quad\text{G2 vertex clocks},\qquad
1600\quad\text{G2 edge clocks}.
\]

The companion C13 is currently an abstract GL(12,2) construction; membership in the actual Co0 stabilizer of canonical V2 is not yet established.

## Parallel-lane reconciliation

Two parallel results materially changed this packet and are retained as constraints:

1. **Pass9861–9884:** the apparent two-valued/sum-determined V2 frame relation dies under larger sampling. No theorem here assumes it.
2. **Pass9921–9944:** the intrinsic type-8 frame is the bridge to an A1^24 2-neighbor; binary Golay lives as that neighbor's glue, not as a coordinate code on Lambda/2Lambda. This is used in the V2 C13 neighbor-clock interpretation. The same parallel pass correctly rejects the false claim that type-4 classes have no 2-neighbors.

## Consolidated frontier

The selector problem has shifted from searching for a hidden canonical point or quotient to searching for a **controlled cyclic/fusion structure**:

- full symmetry cannot pick one plus Lagrangian;
- full G2 cannot support the proposed 13-block quotient;
- Q- and Q+ 7,371-object natural schemes are not isomorphic;
- nevertheless both the G2 carriers and abstract V2 admit semiregular C13 clocks;
- the glue phase space now has an explicit F9/local-field coordinate model;
- optical orientation has both a continuous gauge-invariant Bargmann loop and a finite F9 norm-parity C2 candidate.

This narrows the next weld to: identify an actual order-13 element in the canonical V2/Co0 stabilizer, compare its 315 A1^24-neighbor cycles with the 32/1600 G2 cycles, and search for a common fusion/phase observable rather than a nonexistent fully equivariant 13-block quotient.
