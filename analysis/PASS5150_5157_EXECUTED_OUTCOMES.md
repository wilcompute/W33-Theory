# Passes 5150–5157 — theta curvature, centered spectral inversion, and q4 root-coset torsion

**Status:** EXECUTED, collision-reconciled. Earlier drafts were renumbered after a live Pass5142–5149 owner appeared. Pass5118–5125 remains the owner of the all-q theta half-regular theorem, q7 native-rank falsifier, and safe Jennings theorem; this packet only adds new consequences.

## 5150 — exterior parity / active-check conservation
For every apartment-code support `S`, each exterior apartment has even selected theta-neighbor count `t_v`. Exact identities:

`A_active=2(q-1)|S|`,

`sum_out t_v=4(q-1)|S|`,

and with `b_{2r}=#{v outside:t_v=2r}`,

`sum_r r b_{2r}=2(q-1)|S|`.

A chamber star has only `b_2`, with values 32, 324, 1536, 5000 for q=2,3,4,5.

## 5151 — quantized second-moment curvature
Put `D=8(q-1)`, `k=D/2`, and let `A` be theta adjacency. For `x=1_S`,

`x^T A^2 x >= k(k+2)|S|`.

The exact defect is

`Delta_2=sum_out t_v(t_v-2) in 8 Z_>=0`.

Equality iff every exterior boundary vertex has exactly two selected neighbors. Chamber stars attain equality for q=2,3,4,5. Exhaustive q=2 enumeration of all 65,535 nonzero words gives exactly 45 zero-defect words, all weight 16; the smallest positive defect is 64. Thus curvature equality exactly reconstructs the q=2 minimum shell.

## 5152 — centered theta Rayleigh weight inversion
For `N` apartments, `alpha=|S|/N`, `x=1_S`, `y=x-alpha*1`, and theta degree `D`,

`rho=(y^T A y)/(y^T y)=D(1/2-alpha)/(1-alpha)`.

Hence

`alpha=(D/2-rho)/(D-rho)`.

The chamber-star centered quotients are `116/37`, `144/19`, `1636/139`, `460/29` at q=2,3,4,5. The distance problem can therefore be restated as a sharp upper bound on the centered quotient attainable by nonzero codeword indicators. The identity itself is not that bound.

## 5153 — exact q=4 root-coset Smith form
The 256-by-256 q=4 C2 root-coset incidence matrix has Smith form

`1^180 + 2^4 + 0^72`.

Therefore

`rank_Q=184`, `rank_F2=180`, `rank_F3=184`,

and

`coker(M_4) ~= Z^72 direct_sum (Z/2)^4`.

The characteristic-two rank loss is exactly four integral 2-torsion directions.

## 5154 — two-step theta Markov curvature
A one-step theta walk started uniformly on any nonzero codeword support stays inside with probability exactly 1/2. Two steps are different:

`P2 >= 1/4+1/D`,

with

`P2-(1/4+1/D)=Delta_2/(D^2|S|)`.

Chamber-star equality values are `3/8,5/16,7/24,9/32` at q=2,3,4,5. At q=2 exactly the 45 minimum words attain equality.

## 5155 — augmentation relation versus hidden modular defect
Each root-coset column has q ones, hence the all-ones left functional becomes a defining-characteristic relation. Combining prior certified ranks with the new q4 Smith result gives native rank drops

`0,1,4,8,10` at q=2,3,4,5,7.

One displayed augmentation relation cannot explain the whole loss for q>=4: at least 3,7,9 additional independent modular defect dimensions remain at q=4,5,7. The q4 defect is now integrally identified; q5/q7 composition factors remain open.

## 5156 — root volume/depth two-statistic calculus
For A2, C2, G2 the positive-root height multisets give

`(N,H)=(3,4),(4,7),(6,16)`,

where `N=|Phi+|` controls `|U(q)|=q^N` and root-direction count `N q^(N-1)`, whereas `H=sum ht(alpha)` controls top Jennings degree `(p-1)H` in the already-proved safe range. Thus C2's `q^4 -> 4q^3` derivative and `7(p-1)` group-ring depth are related through the same root poset but are not the same invariant.

## 5157 — first-order theta expansion blindness
Every nonzero codeword support has ordinary theta conductance exactly 1/2. The one-step stay/exit probabilities are 1/2, the uncentered adjacency indicator quotient is `D/2`, and the normalized-Laplacian indicator quotient is 1/2, all independent of Hamming weight.

Therefore first-order Cheeger conductance or the uncentered indicator quotient cannot prove `d_q=q^4`. The first local discriminator is Pass5151's second moment; Pass5152 shows the centered quotient still carries the exact weight.

## Firewall
No q=5/all-q distance closure is claimed here. Prior q7/Jennings results are inputs, not re-owned. Markov statements are finite graph statements, not hardware diffusion/noise models; Jennings depth is algebraic nilpotence, not physical latency.
