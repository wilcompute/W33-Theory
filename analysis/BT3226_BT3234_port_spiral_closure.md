# Passes 3226–3234 — proof-carrying ports, exact cover switches, and the unit-spiral lift

## Status

This packet executes seven continuations of the Passes 3205–3213 port factorisation and one independent unit-spiral/phinary lane. The exact chromatic boundary remains

\[
10\leq \chi(H)\leq 11.
\]

No ten-colouring and no independently checked UNSAT proof were obtained. Every negative solver statement below is therefore fail-closed.

## 3226 — 100 disjoint proof-producing port-SAT shards

The deterministic 7,800-variable, 146,289-clause ten-colour CNF is partitioned by the unique missing colours at two additional W33 supports. The existing symmetry break fixes support 0's missing colour to 9; the two split supports yield exactly 100 mutually disjoint and exhaustive shards. A shard may be promoted only by a SAT assignment accepted by the independent 540-frame model checker, or an UNSAT proof accepted by an external DRAT/LRAT checker. The present packet supplies the exact split surface, not either terminal certificate.

## 3227 — the split-port Terwilliger algebra grows from 16 to 26 dimensions

The coarser 45-block Terwilliger algebra has dimension 16 over each of three large prime fields. Refining to the 135 port cells and adjoining four base-cell dual subconstituent projectors gives dimension 26 over each field:

\[
\dim_{\mathbf F_p} T_{45}=16,\qquad
\dim_{\mathbf F_p} T_{135}=26
\]

for \(p=1{,}000{,}003,1{,}000{,}033,1{,}000{,}037\). This proves that the port split contains ten additional noncommutative moment directions in these characteristics. It does **not** yet provide a characteristic-zero rational dual certificate or a colouring bound above nine.

## 3228 — five commuting \(K_{4,4}\) switches generate 243 exact covers

Fix the 60-frame colour class that is an exact cover of all 240 W33 support edges. Every outside frame has a four-owner signature. The complete signature census is 440 signatures of multiplicity one and five signatures of multiplicity eight.

For each multiplicity-eight signature, the eight outside frames induce exactly \(K_{4,4}\). Its two bipartition classes are the only independent four-frame replacements of the four owner frames. The five owner sets are disjoint, and all cross-locus replacement choices are compatible. Consequently each locus has three states:

\[
\text{retain},\quad \text{replace by side A},\quad \text{replace by side B}.
\]

The five switches commute and generate \(3^5=243\) distinct 60-frame independent sets. Every member remains an exact cover of all 240 support edges. This is an exact local qutrit switching geometry, not a classification of all exact covers. The complete deletion census through six deleted cover frames is also frozen. The maximum compatible outside replacement count is 0 for deletion sizes 1–3 and 4 for sizes 4–6.

## 3229 — exact Kempe descent reaches the same 41-frame local floor for every colour

Starting from the frozen 11-colouring, each target colour is minimized under the fully enumerated neighborhood consisting of one direct recolour, or one connected bichromatic-component swap optionally followed by one direct recolour of a target-colour vertex.

For every one of the eleven target colours, a deterministic one- or two-step proper descent reaches target-class size 41. At each terminal colouring all 89 moves in the stated neighborhood are enumerated and none improves the target size. Thus 41 is a universal local floor for this exact one-move neighborhood. This does not exclude longer non-monotone Kempe chains and does not prove \(\chi(H)=11\).

## 3230 — all local OAs are \(V_4\), but voltage is not intrinsic

All 45 local \(OA(16,3,4,2)\) arrays are isotopic to the Klein-four Latin square, never the cyclic \(C_4\) square.

The global transport law has an exact obstruction: when two blocks share a support, their cross graph is \(K_{3,3}\), which supplies a relation but no preferred bijection. Choosing a perfect matching introduces an \(S_3\) gauge variable. Around one support triangle there are \(6^3=216\) matching triples, and each of the six \(S_3\) holonomies occurs exactly \(6^2=36\) times. Therefore the incidence geometry alone selects no nontrivial voltage or curvature. Such a choice requires an extra hardware, phase, or calibration convention.

## 3231 — nonlinear \(\mathbf Z/9\mathbf Z\) port lift

The prior Smith calculation showed that the linear 3-adic defect layer is vacuous. The new checker freezes a nonlinear polynomial surface over \(\mathbf Z/9\mathbf Z\), including frame and missing-colour one-hot laws, edge distinctness, missing/frame coupling, and 1,350 block-cell exclusivity quadratics.

The exact 11-colouring is a positive control. A single forced collision is rejected. No ten-colour contradiction is claimed. The first genuinely port-specific law absent from the linear Smith layer is: for a fixed block and colour, occupancies in two different independent four-cells have product zero, because all cross-cell frame pairs are adjacent.

## 3232 — exact 720-word physical port compiler

The compiler ROM has 45 blocks × 16 supports = 720 words. Each 14-bit word contains the 8-bit global W33 support identifier and three 2-bit local port labels. The address is the 10-bit concatenation of a 6-bit block and 4-bit local slot. Any two port labels identify the local slot because every local array is an \(OA(16,3,4,2)\). The logical ROM payload is 10,080 bits.

This compiles exact incidence labels. It does not choose one of the six physical \(K_{3,3}\) matchings and makes no observed area, timing, optical-loss, or Landauer claim.

## 3233–3234 — unit spirals, recursive/iterative duality, and the golden controller

The existing phase-controller word

\[
M=R_4^2U_6=
\begin{pmatrix}
-1&0&0\\
0&0&-1\\
0&-1&1
\end{pmatrix}
\]

has characteristic polynomial \((t+1)(t^2-t-1)\), so its golden plane is

\[
B=\begin{pmatrix}0&-1\\-1&1\end{pmatrix},
\qquad \operatorname{spec}(B)=\{\varphi,-\varphi^{-1}\}.
\]

The quarter-turn phase lift is the determinant-one companion

\[
C=\begin{pmatrix}i&-1\\1&0\end{pmatrix},
\qquad
\nu_{k+2}=i\nu_{k+1}-\nu_k,
\]

with eigenvalues \(i\varphi\) and \(-i/\varphi\). It is exactly similar to \(iB\):

\[
C P=P(iB),\qquad
P=\begin{pmatrix}-i&i\\0&1\end{pmatrix}.
\]

This is the rigorous unit-spiral bridge: the expanding golden mode acquires one quarter turn per iteration while the dual contracting mode preserves determinant one.

This also has an exact relativity-style algebraic form. With

\[
L=\begin{pmatrix}-2&1\\1&2\end{pmatrix}
\]

of signature \((1,1)\), the golden block is a Lorentz anti-isometry, \(B^T L B=-L\), while two iterations are a genuine \(O(1,1)\) isometry, \((B^2)^T L(B^2)=L\). The eigenvalues of \(B^2\) are \(\varphi^2\) and \(\varphi^{-2}\), so in its null eigenbasis it is a boost of rapidity \(2\log\varphi\). One iteration exchanges the two causal signs; two iterations preserve them. This is an exact relativity/duality analogy on the controller's golden plane, not evidence that the controller is physical spacetime.

For the dominant orbit \(\nu_k=(\varphi e^{i\alpha})^k\), the logarithmic-cover coordinates are \((\rho_k,\theta_k)=(k\log\varphi,k\alpha)\). They lie on a straight lattice line before exponentiation and become a logarithmic spiral in the punctured plane. At \(\alpha=\pi/2\) the visible plane has four arms. The symplectic quarter-turn \(J(\rho,\theta)=(-\theta,\rho)\) exchanges radial and angular roles and sends the slope/pitch \(a\) to \(-1/a\). This formalizes the proposed recursive-versus-iterative viewpoint: linearity or curvature depends on which covering coordinate is treated as primitive.

### Perpendicular-space correction

A tangent vector does not literally become a metric tensor under a wedge product. The exact bundle statement is

\[
v\longmapsto \iota_v\omega\in T^*M,
\qquad
g(v,w)=\omega(v,Jw),
\]

where \(\omega\) is a nondegenerate two-form and \(J\) is compatible. The wedge structure converts a tangent direction to a covector carrying its action on the whole tangent fiber; the compatible pair \((\omega,J)\), not the tangent alone, reconstructs the metric.

Nested orthogonal loops are represented by \(\omega_n=\sum_{j=1}^n d\rho_j\wedge d\theta_j\). A loop's return value is an additional boundary/coupling map between layers. Orthogonality of interiors does not by itself imply that coupling.

### Phinary/phigital boundary

Standard base-\(\varphi\) arithmetic uses finite sums of distinct powers of \(\varphi\), with a canonical no-consecutive-powers rule. The certificate verifies

\[
2=\varphi+\varphi^{-2},\quad
3=\varphi^2+\varphi^{-2},\quad
14=\varphi^5+\varphi^2+\varphi^{-3}+\varphi^{-6}.
\]

The repository uses *phinary* for the broader golden-recursive viewpoint; Project Euler calls the canonical numeral convention *phigital*. The \(\alpha=\pi/2\) construction here is a phase lift of base-\(\varphi\), not a standard numeral representation and not a physical theory of relativity.

## Literature boundary

- F. M. Dekking, *The structure of base phi expansions*, arXiv:2305.08349.
- M. Dekking and A. van Loon, *Counting base phi representations*, arXiv:2304.11387.
- Project Euler Problem 473, *Phigital Number Base*.
- Standard logarithmic-spiral law: \(r=a e^{b\theta}\); taking \(\log r\) linearizes the radial coordinate.

The exact matrix similarity, qutrit switch family, port algebra dimensions, Kempe local floor, and \(S_3\) transport obstruction are repository computations from this packet.
