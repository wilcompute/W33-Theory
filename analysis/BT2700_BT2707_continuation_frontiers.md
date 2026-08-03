# Passes 2700–2707 — continuation frontiers

## Executive result

This continuation reconciles the finished Pass-2560–2567 packet and pushes the still-open fronts without weakening their quantifiers. The strongest new global result is the exact orbit-disjoint U6 bound

\[
U_6^{\mathrm{singleton}}\ge 30{,}974{,}400.
\]

The strongest new structural result is that the complete 720-signature carrier is simultaneously a 45-fiber chiral \(A_2\) bundle, a two-angle tight fusion frame in dimension 20, an \(S_3\)-coherent tower, and an objectwise refinement of the Schläfli tritangent incidence.

## Pass 2700 — chromatic frontier, fail-closed

Pass 2551 proved that no nine maximum independent sets partition the 540 frames, hence \(\chi(H)\ge10\). Pass 2561 supplied a literal proper eleven-colouring. Therefore

\[
\boxed{10\le\chi(H)\le11.}
\]

This continuation ran proof-oriented ten-colour searches. No proper ten-colouring and no UNSAT certificate was obtained. The best valid heuristic state retained nine conflicting edges. A separate restart-bookkeeping defect produced a 47-conflict assignment and was rejected. Search difficulty is not evidence of nonexistence, so the exact value remains open.

## Pass 2701 — 599 exact U6 singleton orbits

The search uses the frozen 240 syndrome columns. It constructs the complete weight-four image of size

\[
91{,}007{,}752
\]

and all

\[
\binom{240}{3}=2{,}275{,}280
\]

triple records. With deterministic seed `93731`, 5,000 six-supports split as

\[
169\text{ lower-shadow hits},\qquad4{,}232\text{ collisions},\qquad599\text{ singleton witnesses}.
\]

Exact orbit classification under the effective group of order \(51{,}840\) gives

\[
596\text{ trivial-stabilizer orbits}
\]

and

\[
3\text{ stabilizer-two orbits}.
\]

Thus the disjoint union has size

\[
596\cdot51{,}840+3\cdot25{,}920
=\boxed{30{,}974{,}400}.
\]

The geometric-weight split is

\[
10:207{,}360,\quad12:1{,}788{,}480,\quad14:7{,}179{,}840,
\]

\[
16:14{,}618{,}880,\quad18:7{,}179{,}840.
\]

This is a rigorous lower bound, not equality.

## Pass 2702 — chiral affine A2 fibers

For every exact-cover signature \(t\in\mathbb Z^{45}\), define

\[
u=3t-4\mathbf1.
\]

The norm census is

\[
144^{45},\quad216^{270},\quad360^{135},\quad432^{270}.
\]

Each norm-144 point is the center of a unique 16-point affine rank-two fiber. In a basis \(a,b\) with

\[
\begin{pmatrix}a\cdot a&a\cdot b\\b\cdot a&b\cdot b\end{pmatrix}
=
\begin{pmatrix}72&36\\36&72\end{pmatrix},
\]

the fiber is

\[
\{0\}\cup R\cup T\cup2R,
\]

where

\[
R=\{(1,0),(0,1),(1,-1),(-1,1),(0,-1),(-1,0)\}
\]

is the \(A_2\) root hexagon and

\[
T=\{(1,1),(1,-2),(-2,1)\}
\]

is one chiral weight triangle. Hence

\[
\boxed{720=45(1+6+3+6).}
\]

## Pass 2703 — exact A2 tight fusion frame

For each fiber basis \(a_i,c_i\), define the integer projector numerator

\[
N_i=2a_ia_i^T-a_ic_i^T-c_ia_i^T+2c_ic_i^T,
\qquad P_i=N_i/108.
\]

The 45 planes span the common 20-dimensional module and satisfy the exact tight identity

\[
2\sum_iN_i=3U_0^TU_0,
\]

or

\[
\boxed{\sum_iP_i=\frac92E_{20}.}
\]

Their quotient graph is

\[
\operatorname{SRG}(45,12,3,3).
\]

For its 270 adjacent pairs the squared principal cosines are

\[
(1/4,0),
\]

while all 720 nonadjacent pairs are equi-isoclinic with

\[
(1/16,1/16).
\]

## Pass 2704 — the S3 coherent tower

The local Weyl group of the \(A_2\) coordinates is \(S_3\). It acts regularly on each root hexagon and doubled-root hexagon and transitively with stabilizer \(C_2\) on the chiral triangle.

The global exact coherent closures sharpen this local observation:

- shell 216: 45 regular \(S_3\) fibers, closure rank 21;
- shell 360: 45 \(S_3/C_2\) triangles, closure rank 8;
- shell 432: 45 regular \(S_3\) fibers, closure rank 21, radially doubled from shell 216.

Thus

\[
\boxed{720=45(1+S_3+S_3/C_2+S_3)}
\]

over the same 45-point quotient.

## Pass 2705 — septic C5 character squaring

Pass 2563 proved that the full 51,840-element group has a unique degree-seven polynomial self-covariant. Restricting it to the four primitive eigendirections of an order-five subgroup gives a nonzero map on every direction.

Homogeneity forces the character exponent map

\[
k\longmapsto7k\equiv2k\pmod5,
\]

so projectively

\[
\boxed{1\to2\to4\to3\to1.}
\]

This identifies the first full-group nonlinear survivor as a finite character-squaring dynamical channel. It is still a self-map of the faithful four-dimensional module, not a carrier-changing map.

## Pass 2706 — local A2 / global Schläfli weld

Modulo two, the 720 signatures split globally as

\[
720=45\cdot7+27\cdot15.
\]

Inside every 16-point \(A_2\) fiber, the center and doubled-root hexagon form one seven-point light class. The six roots and three chiral weights divide among three heavy classes, each class containing exactly two roots and one chiral weight. These three heavy classes are precisely the three Schläfli lines incident with the light tritangent class.

Therefore each fiber refines one tritangent as

\[
\boxed{16=7+3+3+3.}
\]

The resulting \(45\times27\) incidence has row degree 3 and column degree 5, and the 27-object line graph is

\[
\operatorname{SRG}(27,10,1,5),
\]

the Schläfli graph.

## Evidence boundary

The finite counts, rational projector identities, orbit sizes, and incidence parameters are exact. The chromatic ten-colour decision and global U6 equality remain open. No physical interpretation is promoted merely from a count or module isomorphism.
