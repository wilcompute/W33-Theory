# Passes 5142–5149 — theta curvature/spectral inversion and modular root-coset arithmetic

**Status:** EXECUTED on a collision-clean branch after Pass5126–5133. A later audit found that Pass5118–5125 had already landed the all-q theta half-regular theorem, the q=7 native-rank falsifier, and the safe-characteristic Jennings theorem. Those duplicated drafts were deleted before release. Pass5134–5141 was separately reserved by another live continuation and is not touched here.

## Pass5142 — exterior theta parity and active-check conservation
Pass5119 gives the selected-vertex half-regular law. The complementary theorem is that every unselected apartment has an **even** number `t_v` of selected theta-neighbors. A theta triple has codeword parity zero, so it contains either zero or two selected apartments. Therefore

`A_active = 2(q-1)|S|`,

`sum_{v outside S} t_v = 4(q-1)|S|`,

and, writing `b_{2r}=#{v outside:t_v=2r}`,

`sum_r r b_{2r}=2(q-1)|S|`.

For a chamber star only `b_2` is nonzero, with `b_2=2(q-1)q^4`; the exact values are 32, 324, 1536, 5000 for q=2,3,4,5.

## Pass5143 — second-moment theta curvature
Let `D=8(q-1)`, `k=D/2=4(q-1)`, and `A` be theta adjacency. For `x=1_S`, selected vertices have `k` selected neighbors. Since every exterior selected-neighbor count `t_v` is even,

`x^T A^2 x >= k(k+2)|S|`.

The exact curvature defect is

`Delta_2 = x^T A^2 x-k(k+2)|S| = sum_{v outside S} t_v(t_v-2) in 8 Z_{>=0}`.

Equality holds iff every exterior boundary apartment has exactly two selected neighbors. Chamber stars attain equality at q=2,3,4,5. At q=2 the entire `[90,16,16]_2` code was exhaustively enumerated: all 65,535 nonzero words were tested, exactly 45 have `Delta_2=0`, every one has weight 16, and the smallest positive defect is 64. Thus curvature equality alone reconstructs the complete q=2 minimum shell.

## Pass5144 — centered theta Rayleigh weight inversion
The uncentered indicator Rayleigh quotient is constant by Pass5119, but centering restores the missing weight information. Let `N` be the apartment count, `alpha=|S|/N`, `D=8(q-1)`, `x=1_S`, and `y=x-alpha*1`. Then

`rho(S)= (y^T A y)/(y^T y) = D(1/2-alpha)/(1-alpha)`.

This is exactly invertible:

`alpha=(D/2-rho)/(D-rho)`.

Hence centered theta adjacency determines the Hamming weight of every nonzero proper codeword indicator exactly. Chamber-star anchors are

- q=2: `rho=116/37`, `alpha=8/45`;
- q=3: `rho=144/19`, `alpha=1/20`;
- q=4: `rho=1636/139`, `alpha=8/425`;
- q=5: `rho=460/29`, `alpha=1/117`.

The remaining distance problem can therefore be phrased as a sharp upper bound on the **attainable centered Rayleigh quotient** among nonzero codewords. The identity itself does not supply that bound.

## Pass5145 — exact q=4 root-coset Smith form
For the 256-by-256 q=4 C2 root-coset incidence matrix, exact integral Smith reduction gives

`1^180 + 2^4 + 0^72`.

Thus

`rank_Q=184`, `rank_F2=180`, `rank_F3=184`,

and

`coker(M_4) ~= Z^72 direct_sum (Z/2)^4`.

The entire characteristic-two rank loss is therefore four genuine integral 2-torsion directions. This complements the already known q=3 cokernel `Z^12 direct_sum Z/3`.

## Pass5146 — two-step theta Markov curvature
Start the simple random walk on the theta graph uniformly on a codeword support. One step is universally blind:

`P[X_1 in S]=1/2`.

At two steps the curvature appears:

`P[X_2 in S] = (x^T A^2 x)/(D^2|S|) >= 1/4 + 1/D`,

with exact excess

`P_2-(1/4+1/D)=Delta_2/(D^2|S|)`.

The sharp chamber-star values are `3/8, 5/16, 7/24, 9/32` at q=2,3,4,5. At q=2 exactly the 45 minimum words attain equality. This is finite graph diffusion only, not a hardware/noise model.

## Pass5147 — augmentation relation versus hidden native defect
Every root-coset incidence column has q ones, so in defining characteristic `p|q` the all-ones left functional supplies one explicit native relation:

`1^T M = q 1^T = 0`.

Using the already certified ranks at q=2,3,4,5,7, the native rank drops are

`0,1,4,8,10`.

Therefore one displayed augmentation relation cannot account for the full loss once q>=4. At least `3,7,9` additional independent modular defect dimensions remain at q=4,5,7 respectively. Pass5145 identifies the q=4 loss integrally; the q=5/q=7 hidden composition factors remain open.

## Pass5148 — positive-root volume/depth two-statistic calculus
Two different statistics of the same positive-root poset control two distinct project structures:

- `N=|Phi+|` controls maximal-unipotent volume `q^N` and the first root-coset derivative `N q^(N-1)`;
- `H=sum ht(alpha)` controls the top Jennings degree `(p-1)H` in the previously proved safe range.

For A2, C2, G2 the pairs `(N,H)` are

`(3,4), (4,7), (6,16)`.

Thus the user's C2 `q^4 -> 4q^3` derivative is the `N=4` statistic, whereas the C2 augmentation-memory depth is governed by `H=7`. They are two root-system statistics, not one invariant.

## Pass5149 — first-order theta expansion is provably blind
Every nonzero codeword support has ordinary theta conductance exactly

`Phi(S)=1/2`,

independent of weight. Equivalently, the one-step stay and exit probabilities are both 1/2, the uncentered adjacency indicator Rayleigh quotient is `D/2`, and the normalized-Laplacian indicator quotient is `1/2`.

Therefore a proof of `d_q=q^4` cannot use first-order Cheeger conductance or the uncentered indicator Rayleigh quotient alone. Pass5143's second moment is the first local statistic in this hierarchy that distinguishes chamber-star curvature, while Pass5144 shows that the **centered** quotient still retains exact weight information.

## Evidence firewall
- q=5/all-q minimum distance remains open unless another packet closes it.
- Pass5142 refines Pass5119; it does not re-own the half-regular theorem.
- Pass5147 uses previously certified q=7 ranks rather than claiming them anew.
- Pass5148 is a synthesis of the existing derivative and safe Jennings theorems, and group-ring depth is algebraic nilpotence, not physical latency.
