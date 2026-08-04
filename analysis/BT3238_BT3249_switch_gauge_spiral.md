# Passes 3238–3249 — exact switch orbits, non-Abelian logical ports, and a real unit-spiral machine

## Status and boundary

This packet executes the five requested continuations of Passes 3226–3237 and two independent high-risk constructions. The exact chromatic boundary remains

\[
10\leq\chi(H)\leq 11.
\]

One hundred bounded MILP shard runs were executed, but every run terminated without a primal model and without an infeasibility certificate. They are diagnostics only. SAT is promoted only after the independent 540-frame checker accepts the model; UNSAT is promoted only after an external DRAT/LRAT checker accepts the proof.

## 3238–3239 — the 243 exact covers carry an affine involution, not five logical qutrits

The five commuting \(K_{4,4}\) switches give coordinates \(x\in\mathbf F_3^5\) on 243 exact 60-frame covers. Reconstructing all 25,920 elements of \(PSp(4,3)\) gives a setwise stabilizer of order four and structure \(C_4\). Its square fixes every cover; its quotient involution is

\[
\tau(x_1,x_2,x_3,x_4,x_5)=(-x_4,1-x_3,1-x_2,-x_1,x_5).
\]

The fixed locus has 27 covers, cut out by \(x_3=1-x_2\) and \(x_4=-x_1\). The other 216 covers form 108 pairs. Thus the family contains 135 internal \(PSp(4,3)\)-equivalence classes. Cover stabilizers have order two for 216 covers and order four for the fixed 27, giving full-group orbit sizes 12,960 and 6,480 respectively.

The useful conclusion is exact but narrower than the tempting interpretation: \(\mathbf F_3^5\) is a valid switch-coordinate system, but the full five-qutrit translation group is not induced by \(PSp(4,3)\).

## 3240–3241 — gauge fixing exposes a free non-Abelian logical layer

The 45-block port complex has

\[
(V,E,F)=(45,720,240).
\]

A deterministic spanning tree removes 44 edge variables. Because the 240 triangular face boundaries have disjoint edge supports, one distinct chord can be eliminated per face. Exactly 436 free chords remain and no relation remains among them:

\[
\pi_1(X)\cong F_{436}.
\]

Consequently flat \(S_3\)-gain assignments modulo switching are simultaneous-conjugacy classes of \(\operatorname{Hom}(F_{436},S_3)\). Burnside's lemma gives

\[
N_{S_3}=\frac{6^{436}+3\,2^{436}+2\,3^{436}}6.
\]

The exact count has 339 decimal digits. A fixed-length enumerative label needs 1,128 bits, versus 1,308 bits for a naive three-bit label on every generator.

Abelianizing \(S_3\to C_2\) leaves \(2^{436}\) classes. This is exactly the 436-dimensional binary logical shadow of the \([[720,436,2]]\) port CSS complex. The binary code is therefore not the whole connection theory; it is the sign-character projection of a much larger non-Abelian logical port space.

This is standard gain-graph switching language: oriented edges carry invertible group labels, and switching acts at vertices. The finite calculations here are repository-specific; no complete contextuality invariant is claimed.

## 3242–3243 — an integral four-dimensional unit-spiral controller

The complex companion

\[
C=\begin{pmatrix}i&-1\\1&0\end{pmatrix}
\]

realifies to

\[
R=\begin{pmatrix}
0&-1&-1&0\\
1&0&0&0\\
1&0&0&-1\\
0&0&1&0
\end{pmatrix},
\qquad \chi_R(t)=t^4+3t^2+1,
\qquad \det R=1.
\]

In state coordinates \((x_0,x_1,y_0,y_1)\),

\[
(x_0,x_1,y_0,y_1)\mapsto(-x_1-y_0,x_0,x_0-y_1,y_0).
\]

It preserves the split metric

\[
G=\begin{pmatrix}
-2&0&0&-1\\
0&-2&-1&0\\
0&-1&2&0\\
-1&0&0&2
\end{pmatrix},
\qquad R^TGR=G,
\]

whose signature is \((2,2)\) and determinant 25. It also preserves two independent unimodular symplectic forms \(\Omega_0,\Omega_1\). The endomorphism \(K=\Omega_0^{-1}\Omega_1\) commutes with \(R\) and satisfies \(K^2=-I\), recovering the complex structure internally.

The involution

\[
S=\begin{pmatrix}
0&1&0&0\\1&0&0&0\\0&0&0&1\\0&0&1&0
\end{pmatrix}
\]

satisfies \(S^2=I\) and \(SRS=R^{-1}\). Thus \(\langle R,S\rangle\) is an exact integral infinite-dihedral realization combining recursion, iteration, reversal, split relativity and symplectic bundle structure.

## 3244–3245 — all 100 shards executed locally and proof lanes installed

The 100 missing-colour shards were all executed under the exact proper-colouring MILP with a 0.35-second HiGHS limit per shard. Result:

- SAT models: 0;
- verified UNSAT proofs: 0;
- time-limit/no-primal outcomes: 100.

This changes no theorem boundary. The packet adds a separate CaDiCaL plus DRAT-trim matrix workflow. Each of the 100 CNFs is generated from the frozen 7,800-variable, 146,289-clause base formula with two assumption clauses. A SAT result must pass the independent model checker. An UNSAT result must pass DRAT-trim; an LRAT conversion/checking route can subsequently reduce the trusted checker surface.

## 3246 — BONKERS: the fixed 27 are a weighted ternary cube, not Schläfli

Write the 27 fixed covers as

\[
(a,b,c)\longmapsto(a,b,1-b,-a,c),\qquad(a,b,c)\in\mathbf F_3^3.
\]

Their intersection metric is exactly

\[
|C_x\cap C_y|=60-8[\Delta a\ne0]-8[\Delta b\ne0]-4[\Delta c\ne0].
\]

The pair-intersection histogram is

\[
40^{108},\;44^{54},\;48^{108},\;52^{54},\;56^{27}.
\]

Every union of these five relations was tested. No degree-ten union has the Schläfli parameters \((27,10,1,5)\). The repeated count 27 is therefore not an \(E_6\) identification here; the exact object is a weighted ternary Hamming cube.

## 3247 — BONKERS: the unit spiral compiles the six physical port matchings

Modulo two, \(R\) has order six and \(\langle R,S\rangle\) has order 12. The subgroup \(\langle R^2,S\rangle\) has order six and is isomorphic to \(S_3\). It acts faithfully on the three nonzero vectors of an invariant \(\mathbf F_2^2\) plane.

Therefore the six perfect matchings of every physical \(K_{3,3}\) port bridge can be selected by the mod-two shadow of the same integral unit-spiral controller. The port-gauge selector is no longer an unrelated lookup table: it is a finite quotient of the recursive/iterative spiral dynamics. Synthesizable RTL and an exhaustive six-selector testbench are included.

## 3248–3249 — publication and evidence

The packet contains an exact generator, compact certificate, focused regressions, the SAT shard driver, spiral/S3 RTL, a shared theorem insert, a public-index insert, an idempotent four-front-door integrator, a focused RTL/PDF workflow, and a separate 100-shard proof workflow.

At source publication the previous Passes 3226–3237 evidence job remained queued. This packet likewise does not promote Icarus, Yosys, placement, integrated-paper or PDF success until the new workflows are terminal green and their artifacts are inspected.

## Literature boundary

- T. Zaslavsky, *Biased graphs. I. Bias, balance, and gains*, JCTB 47 (1989), DOI `10.1016/0095-8956(89)90063-4`.
- M. J. H. Heule, W. A. Hunt Jr., and N. Wetzler, *Bridging the gap between easy generation and efficient verification of unsatisfiability proofs*, STVR 24 (2014), DOI `10.1002/stvr.1549`.
- L. Cruz-Filipe et al., *Efficient Certified RAT Verification*, CADE 26 (2017), DOI `10.1007/978-3-319-63046-5_14`.
- M. Dekking and A. van Loon, *On the representation of the natural numbers by powers of the golden mean*, Fibonacci Quarterly 61 (2023), pp. 105–118.
