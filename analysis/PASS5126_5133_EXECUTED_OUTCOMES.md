# Passes 5126–5133 — executed outcomes

Status: **EXECUTED on branch; pending merge gate**.

## Pass5126 — q=5 sub-625 chamber leader is at least 18

Pass5110 identifies chamber-generator gauge with the binary Levi cut space. For a cut-minimal 17-edge representative, the selected Levi subgraph is bipartite, max degree 3, and girth at least 8. A pure-Python exhaustive prescribed-degree search rejects every degree-sequence pair with wedge count at least 26; wedge count 25 is attained. Under the exact q=5 chamber distance-scheme Delsarte inequalities, `N1<=25` has extremal pair distribution

\[
(N_1,N_2,N_3,N_4)=(25,66,45,0),
\]

with pair-overlap budget 5000, hence the Bonferroni apartment-weight lower bound is

\[
17\cdot625-2\cdot5000=625.
\]

Therefore any q=5 word of weight strictly below 625 has minimum chamber-generator leader at least 18. Equality at leader 17 and leaders >=18 remain open.

## Pass5127 — all-q first-order theta expansion is blind to distance

For every nonzero codeword support S, Pass5119 gives ambient theta degree `D=8(q-1)` and induced/external selected degree `D/2=4(q-1)`. Consequently

\[
|E(S)|=2(q-1)|S|,
\qquad
|\delta(S)|=4(q-1)|S|,
\]

and a one-step theta random walk started uniformly on S satisfies

\[
P(\mathrm{stay})=P(\mathrm{exit})=\tfrac12.
\]

The indicator Laplacian Rayleigh quotient is identically

\[
\frac{1_S^T L1_S}{\|1_S\|^2}=4(q-1)=D/2.
\]

Thus ordinary first-order spectral/Cheeger data cannot distinguish minimum codewords; the missing invariant must retain higher-order theta/chart information.

## Pass5128 — BT865 torsor group gauge closes and reveals point/line parabolic asymmetry

For the q=3 point parabolic of order 648, the induced action on the four lines through the fixed point has image A4 of order 12. Its kernel has order 54, center order 3, and derived subgroup order 27. After the Pass5105/BT865 chamber alignment, that derived subgroup is exactly the root-controller Heisenberg `H27`. The quotient of the point parabolic by H27 has order census

`1^1 2^1 3^8 4^6 6^8`,

identifying `SL(2,3)`.

For the line parabolic, the action on the four points of the fixed line has full S4 image of order 24 and kernel order 27; that kernel is exactly the flat root-controller `F3^3`.

Hence the BT865 state/program torsor *groups* are canonical parabolic subgroups. The remaining BT865 noncanonicity is the choice of three free rank-3 H1 cycle seeds, not the torsor groups themselves.

## Pass5129 — odd-q bicycle formula reduced to one cross-characteristic rank statement

Let N be the W(3,q) point-line incidence matrix and `P=(q+1)(q^2+1)`. For odd q,

\[
\operatorname{rank}_{\mathbb Q}N
=1+\frac{q(q+1)^2}{2}.
\]

For the binary Levi vertex-edge incidence B, even degree `q+1` gives

\[
BB^T\equiv
\begin{pmatrix}0&N\\N^T&0\end{pmatrix}
\pmod2,
\]

so connectedness yields

\[
\dim\mathrm{Bike}=2\,\operatorname{null}_{\mathbb F_2}(N)-1.
\]

Therefore

\[
\dim\mathrm{Bike}=q^3+q-1
\]

iff

\[
\operatorname{rank}_{\mathbb F_2}N
=\operatorname{rank}_{\mathbb Q}N.
\]

Exact no-drop anchors now hold at q=3,5,7,9,11,13. q=9 is an extension-field anchor. The all-odd-q no-drop theorem remains open.

## Pass5130 — rank-three Jennings/root-height protected memory

In the safe characteristic range, the regular Sylow-unipotent module has associated-graded Hilbert series

\[
\prod_{\alpha>0}
(1+t^{\mathrm{ht}(\alpha)}+\cdots+t^{(p-1)\mathrm{ht}(\alpha)}).
\]

New exact rank-three anchors:

- A3, p=5: positive-root heights `(1,1,1,2,2,3)`, dimension `5^6=15625`, 41 palindromic layers, center layer 931.
- C3, p=7: positive-root heights `(1,1,1,2,2,3,3,4,5)`, dimension `7^9=40353607`, 133 palindromic layers, center layer 925601.

This extends the C2 memory-height law to rank three. Augmentation depth is algebraic nilpotence, not a physical latency claim.

## Pass5131 — q=4 derivative geometry in genuine F4

Using exact F4 arithmetic, the type-C2 maximal unipotent group has order `4^4=256`. The 256 positive-root cosets form a square root-coset incidence matrix. The derivative point graph has exact spectrum

\[
12^1,8^6,6^{24},4^9,2^{24},0^{84},(-4)^{72},(2\sqrt2)^{18},(-2\sqrt2)^{18}.
\]

The integer annihilator

\[
x(x-12)(x-8)(x-6)(x-4)(x-2)(x+4)(x^2-8)
\]

vanishes exactly. Root-coset incidence ranks are 184 generically but 180 over native F2: native drop 4.

## Pass5132 — q=5 derivative spectrum closes exactly

The 625-vertex q=5 derivative graph has degree 16 and exact square-free annihilator factors

`x-16, x-11, x-6, x-1, x+4, x^2-12x+31, x^2-2x-4, x^2-7x-4, x^2-2x-14`.

Exact trace moments force spectrum

\[
16^1,11^8,6^{16},1^{140},(-4)^{220},
\]

plus conjugate pairs

\[
(6\pm\sqrt5)^{20},
(1\pm\sqrt5)^{40},
\left(\frac{7\pm\sqrt{65}}2\right)^{20},
(1\pm\sqrt{15})^{40}.
\]

The generic root-coset incidence rank is `625-220=405`; the native F5 rank is 397, drop 8.

## Pass5133 — higher-order theta triangle curvature is nonconstant

At q=3 first-order support geometry is rigid: every support has induced theta-edge count `4|S|`. But fully selected triangle count varies.

- chamber star: `(weight, edges, triangles)=(81,324,108)`;
- XOR of two chamber stars at gallery distance 1: `(108,432,108)`;
- distance 2: `(144,576,168)`;
- distance 3: `(156,624,196)`;
- distance 4: `(160,640,208)`.

Every fully selected theta-*check* triangle count is zero by parity. The varying triangles are therefore the common-root/Tanner-six-cycle triangles from Pass5079. This is the first concrete higher-order curvature statistic in the current distance program that sees information erased by Pass5127's fixed first-order Rayleigh data.

## Evidence firewall

- q=5 distance 625 is **not** yet proved for all leaders; only sub-625 leaders <=17 are excluded.
- all-odd-q bicycle formula is **not** yet proved; the no-binary-rank-drop equivalence plus anchors are exact.
- q=4/q=5 derivative rank defects and quadratic fields are finite algebraic invariants with no particle/charge assignment.
- Jennings depth is a modular group-algebra filtration, not physical time.
- triangle curvature is a candidate higher-order distance invariant; no all-q curvature inequality is yet claimed.
