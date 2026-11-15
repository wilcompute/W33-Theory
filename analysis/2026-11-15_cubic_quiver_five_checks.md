# Five tests of the cubic quiver reconstruction

The [ten-support identity](2026-11-15_cubic_quiver_ovoid_recovery.md) reconstructs the signed Dickson cubic in a common basis of 27 coordinates. These tests compare that identity with wrapped charges, the four-dimensional quartic, the marked Fermat superpotential, Seiberg mutation, and the set of nonnegative reconstruction weights.

## Wrapped D3 charge lattice

Let $S$ be the smooth cubic surface, $C=-K_S$, and $Y\to S$ the primitive circle bundle of first Chern class $C$, up to fiber orientation. The integral Gysin sequence gives $H^3(Y,\mathbb Z)\cong C^\perp\cong E_6(-1)$ and $H^2(Y,\mathbb Z)\cong\operatorname{Pic}(S)/\mathbb ZC\cong E_6(-1)^*$. The pairing on the free lattice is perfect by Poincaré duality. For the D3 brane wrapping the circle bundle over $\ell$, its charge is the pairing with $\ell$ on $C^\perp$. The previous [Type IIB circle-bundle calculation](2026-11-14_cubic_iib_spin.md) derived the RR gauge fields and identified these minuscule weights. The 27 wrapped lines give 27 distinct weights in one nontrivial discriminant coset, with squared norm $4/3$ in the positive convention. [Dibaryon Spectroscopy](https://arxiv.org/abs/hep-th/0305048)

In this basis, the charge of a configuration of 27 formal occupation coordinates is a **rank-six** linear map. The verifier checks all degree-three monomials, allowing repeated species. The 45 tritangents are exactly the neutral triples. In particular, populating only the three species of a single tritangent with unit coefficients gives total Betti charge zero and Dickson value $+1$ or $-1$. The zero configuration has the same Betti charge and Dickson value zero. Consequently the Dickson cubic cannot descend to a function of the six measured Betti charges. Identifying a 27-dimensional physical charge sector requires more conserved charges than these six RR gauge fields provide.

## Four-dimensional Freudenthal quartic

In electric and magnetic dual bases write $K(p,q)=\langle dN(p),dN^\vee(q)\rangle$. The $4d/5d$ charge form includes $4K$ alongside the square of the scalar pairing and the two terms linear in $N,N^\vee$. Those linear terms inherit the earlier factor of $1/6$ for each ovoid. For the pairing one obtains

$$K(p,q)=\frac1{36}\sum_{u,v\in O}\langle dN_u(p),dN_v^\vee(q)\rangle.$$

Here the dual signed cubic uses the same tritangent support in the paired charge basis. The count applies with arbitrary nonzero fixed primal and dual tritangent coefficients in those bases. [Ceresole, Ferrara and Marrani, 4d/5d correspondence](https://arxiv.org/abs/0707.0964)

Every tritangent supplies three same-term derivative products and every coordinate belongs to five tritangents. There are 135 same-term and 540 ordered mixed-term products. In a single support these counts are 81 and 162 because it keeps three of the five tritangents through each coordinate. A weighted sum of within-support pairings would require the sum of weights to be both $135/81$ and $540/162$. The relevant terms are separately identifiable because two intersecting lines determine their tritangent. Thus even all 40 within-support pairings cannot supply the quartic term by scalar weighting alone.

Within the chosen ten-support ovoid the coefficient equations on the 100 ordered pair weights have exact rank 100. The uniform $1/36$ solution is unique, so all 100 ordered pairs are required within this bilinear representation. Across all 40 supports, same-tritangent products appear 24 times and mixed products 12 times. Thus there is also an exact corrected diagonal implementation $K=(1/12)\sum_u\langle dN_u,dN_u^\vee\rangle-D$, where $D$ is the sum of same-tritangent derivative products. This uses the independent tritangent correction.

## Fermat couplings and rescaling stabilizer

Choose six skew Fermat lines from the two coordinate pairings $01|23$ and $02|13$. There are three in each family, with phases $(a,a)$ and $(a,a+1)$ respectively. Pick the exceptional marking given in the certificate. The blowdown coordinate ratios come from quotients of tritangent plane equations sharing the same residual $Q_i$. Their common divisor cancels, leaving ratios of pullbacks of linear coordinates on the plane. Normalize the first four blown-up points to the projective frame and substitute the resulting last two coordinates into Wijnholt's Eq. (3.35) over $\mathbb Q(\sqrt{-3})$. The resulting 27 coefficients are all nonzero. A different indicated marking gives three zero coefficients in that presentation. [Wijnholt, §3.4 and Eq. (3.35)](https://arxiv.org/abs/hep-th/0212021)

For a nonzero $3\times3\times3$ coefficient array, the eight alternating products around the $2\times2\times2$ boxes anchored at $(0,0,0)$ are a complete set of ratios for field rescaling. Each field touches exactly two indices. When two arrays have equal ratios, their pointwise quotient can be reconstructed from its entries on the three coordinate slabs as a product of three pair-index factors. The exact test finds **12 of the 648** directed permutations preserving the marked Fermat coefficients modulo field scales. The four permutations fixing the three blocks setwise form a Klein four group. The other eight elements have order three, so the stabilizer is $A_4$. Gauge kinetic couplings and the other Fermat markings have separate stabilizer questions.

## Seiberg moves and support adjacency

Each of the nine equal-rank nodes has $N_f=3N$, so a one-node dual has rank $2N$ at that node. Its nine mesons have reverse-arrow partners. At the all-nonzero Fermat marking these partners all pair off, leaving 18 arrows after eliminating the massive pairs. For each meson $M$ and old reverse arrow $Y$ the pertinent magnetic terms have the form $M(cY+q\widetilde q)+YR$. Eliminating both variables gives $-Rq\widetilde q/c$ and preserves the reduced magnetic Jacobian algebra by substitution. This accounts for the quartic terms and gives the meson substitution without identifying a different Weyl support. Gauged spectator anomalies cancel with the mutated rank vector. At the dualized node the SQCD cubic flavor anomaly checks as $-2N+3N=N$ before gauging spectators. [Seiberg, electric–magnetic duality](https://arxiv.org/abs/hep-th/9411149) · [Wijnholt's explicit one-node dual, Eq. (3.38)](https://arxiv.org/abs/hep-th/0212021)

Thus none of the 240 edges of the support graph is implemented by a single Seiberg dual between these equal-rank presentations. The quiver and rank scan gives 9, 63, 354 and 2,088 newly reached labeled states at depths one through four. Equal ranks first recur in 27 new states at depth four, all with the original abstract arrow pattern up to relabeling. Transport the six Abelian grades by giving each meson the sum of its two quark charges and choosing the common magnetic quark shift by complementary-flavor baryon matching. The 27 endpoints are the 27 distinct supports sharing 15 cubic terms with the original. They are precisely its nonneighbors in $Q(4,3)$.

The verifier follows the exact marked Fermat potential along the four-move paths. It adds the meson–dual-quark terms and eliminates massive pairs by solving both Jacobian equations before proceeding. The elimination respects all six grades and produces the corresponding 27-term cubic at every endpoint. For example, the sequence $(1,4,7,1)$ has arrow counts $18,20,18,27$ and ends with 27 cubic terms. By composing two such paths and carrying the actual coefficients and charges through the intermediate relabeling, it also reaches **all twelve adjacent supports in eight moves**. The certificate gives paths to all 39 other supports from the reference. The eight-move paths are upper bounds on distance. The verifier checks both the cubic gauge-anomaly balance and the six mixed gauge–baryonic anomaly coefficients at every intermediate node. This tests the superpotential and the chiral-ring substitution for integrating out the quadratic pairs. A full comparison of quantum chiral rings, including nonperturbative relations at finite rank, remains open.

## Exact partial classification of nonnegative reconstructions

Rescale weights so that each line sum is one. The point–line constraints have rank 25, and the positive uniform solution shows that the nonnegative polytope has affine dimension 15. A support is extreme exactly when its incidence columns are independent. The verifier enumerates every integer line cover of totals 1, 2, and 3 and checks this independence over the rationals. The search is exhaustive in those grids. On a line with one positive weight, any feasible perturbation vanishes there. On a line with two, the perturbations have opposite signs. These relations reduce the rank test to a small system for the free bipartite components.

| Weight grid | Feasible points | Extreme points on that grid |
|---|---:|---|
| Integers | 36 | 36 ovoids |
| Multiples of $1/2$ | 990 | 36 ovoids and 324 hemisystems |
| Multiples of $1/3$ | 19,768 | 36 ovoids and 1,872 nonuniform vertices |

The 1,872 have weights $1/3$ and $2/3$, with support sizes 21, 22, and 25 and multiplicities 360, 1,080, and 432 respectively. Each of these three types is a single Weyl orbit, verified with the six simple reflections. The ovoids and the hemisystems each form one orbit as well. The full census for higher denominators remains open. [Bamberg, Kelly, Law and Penttila, $m$-ovoids](https://cage.ugent.be/~bamberg/Research_files/Tight%20Sets%20and%20movoids%20of%20Polar%20Spaces.pdf)

Run the [verifier](toe_20261115_quiver_five_checks.py) with NetworkX and SymPy installed.

    python -B analysis/toe_20261115_quiver_five_checks.py

The [certificate](../data/toe_20261115_quiver_five_checks.json) gives the marked Fermat coefficients and invariants, the exact rank tests, and the integer-cover census.
