# Recovering the five-dimensional charge cubic from ten quiver supports

The 40 cubic single-trace supports of the [nine-node del Pezzo quiver](2026-11-15_cubic_quiver_steiner_reconstruction.md) each retain 27 of the 45 tritangent terms. On the same 27 labeled variables take the Dickson form of the split $E_6$ cubic,

$$N(A,B,C)=\det A+\det B+\det C-\operatorname{tr}(ABC).$$

Here $A,B,C$ are the three $3\times3$ arrow blocks of the reference quiver. The 18 determinant terms are exactly the terms omitted by its directed trace rule. The Dickson form is the standard cubic on the split minimal module. The five-dimensional two-derivative supergravity charge classification uses this cubic, with large black-hole entropy proportional to $\sqrt{|N|}$ in the corresponding charge normalization. [Vavilov and Luzgarev, Dickson form](https://mahalex.net/about/publications/norme6.pdf) · [Ferrara and Günaydin, charge orbits](https://arxiv.org/abs/hep-th/9708025)

## Failure on one support

Write $T=\operatorname{tr}(ABC)$. The full cubic and the trace projection can assign different charge strata even on integral examples.

| $(A,B,C)$ | $T$ | $dT$ | $N$ | $dN$ |
|---|---:|---|---:|---|
| $(I,0,0)$ | $0$ | $0$ | $1$ | nonzero |
| $(\operatorname{diag}(1,1,0),0,0)$ | $0$ | $0$ | $0$ | nonzero |
| $(I,I,I)$ | $3$ | nonzero | $0$ | $0$ |

The first two trace-blind examples persist for arbitrary coefficients on the same directed triangle support. Each derivative of a triangle still contains an arrow from at least one zero block. The third example uses the Dickson coefficients shown above.

For the standard trace polynomial the affine critical locus is $AB=BC=CA=0$. Write its ranks as $(r_A,r_B,r_C)$. Adjacent ranks sum to at most three, since the image of each map lies in the following kernel. Conversely every rank triple satisfying these conditions occurs. At each of the three vector spaces, choose a kernel of dimension $3-r_{\rm out}$ and then an image of dimension $r_{\rm in}$ inside it. Finally choose each rank-$r$ isomorphism from source modulo kernel to image at the next vertex. The dimension of the stratum is

$$6\sum_i r_i-\sum_i r_i^2-\sum_{i<j}r_i r_j.$$

The three cyclic permutations of $(2,1,1)$ attain the maximum 13, so the projectivized critical locus has dimension 12. The projective critical locus of $N$ is the complex Cayley plane of dimension 16. These dimensions exclude linear equivalence over $\mathbb C$, even with overall scaling. [Iliev and Manivel, Cartan cubic and Cayley plane](https://arxiv.org/abs/1102.3618)

## Optimal reconstruction with arbitrary scalar weights

For support $p$, define $N_p$ by keeping the coefficients of $N$ on its 27 terms. This defines all 40 polynomials in a common basis. Let $S$ be the 40-by-45 matrix of support masks and $B$ be the 40-by-40 point–line incidence matrix of $Q(4,3)$. The column degrees of $S$ are 24, so the uniform mean is $(3/5)N$. The overlaps and point–line incidence give

$$SS^{\mathsf T}=15J+3BB^{\mathsf T}.$$

The diagonal is $27=15+3\cdot4$. Two distinct quadric points share one line when their masks intersect in 18 terms, and share zero when the intersection has 15 terms. For weights $w$ with $\sum_p w_p=1$, the Gram identity gives the squared coefficient error of the unrescaled reconstruction,

$$\left\|S^{\mathsf T}w-\frac35{\bf 1}\right\|^2
=3\left\|B^{\mathsf T}w-\frac1{10}{\bf 1}\right\|^2.$$

This uses the Hermitian norm for complex weights. The signed polynomial coefficients give the same error since the Dickson coefficients are all $+1$ or $-1$. Exact reconstruction is equivalent to giving every polar line weight $1/10$. Each support lies on four lines, so at least ten supports are needed just to touch all 40 lines. With ten, each line meets exactly one chosen support and the weights must all be $1/10$.

More generally, $k\le10$ nonzero weights touch at most $4k$ lines. The line weight vector has sum four. Cauchy–Schwarz bounds its squared norm below by $16/(4k)$, so the squared coefficient error is at least $12/k-6/5$. Equality holds exactly at equal weights on $k$ mutually nonadjacent supports. Subsets of an ovoid attain it for every $k\le10$.

Any formula recovering $N$ up to nonzero scale has nonzero total weight, by summing the 45 mask coefficients. Thus the bound also applies to unnormalized linear combinations, including signed or complex coefficients. The ten-support optima are exactly the ovoids of $Q(4,3)$. Each tritangent occurs six times in each such ovoid $O$, so

$$N=\frac16\sum_{p\in O}N_p.$$

The verifier enumerates all 36 ovoids and confirms that they are the 10-point elliptic hyperplane sections. Under point–line duality these are the 36 spreads of $W(3,3)$. The [existing spread verifier](w33_pass4957_q43_ovoids_are_w33_spreads.py) identifies the dual spreads, and the [association-scheme calculation](w33_spread_double_six_association_scheme.py) compares their incidence parameters with those of double-sixes. The direct map below identifies which spread matches each double-six in the quiver action. [Ball, Govaerts and Storme, ovoids of parabolic quadrics](https://web.mat.upc.edu/simeon.michael.ball/ovoidsofparabolics.pdf)

The minimal reconstructions do not generate all nonnegative reconstructions by convex mixing. Each pair of ovoids meets in one or four points. The 30-point complement of any ovoid meets each line three times, so uniform weights on this complement give another exact reconstruction. Its zero weights on the omitted ovoid exclude every minimum solution from the support of a convex mixture. The certificate verifies the complement formula $N=\frac1{18}\sum_{p\notin O}N_p$.

A 20-point hemisystem gives an extreme nonnegative reconstruction, $N=\frac1{12}\sum_{p\in H}N_p$. Linear programming found the support. The exact verifier checks two points per line, twelve occurrences of every tritangent, and a connected nonbipartite induced graph. Any weight perturbation supported in $H$ preserving the line sums must change the weights at the two ends of each edge by opposite amounts. An odd cycle and connectedness force every change to vanish. Any convex decomposition of this solution into nonnegative reconstructions would also have to use only points of $H$, which proves extremality. [Bamberg, Kelly, Law and Penttila, classification of $m$-ovoids in $Q(4,3)$](https://cage.ugent.be/~bamberg/Research_files/Tight%20Sets%20and%20movoids%20of%20Polar%20Spaces.pdf)

## Which double-six gives which reconstruction

Given a double-six $D$, take the supports that have at least one determinant block disjoint from $D$. These are precisely the ten supports in its ovoid. For the standard double-six $\{E_i,Q_i:1\le i\le6\}$, the 15 remaining lines are $L_{ij}$. The ten disjoint determinant blocks are the nine crossing pairs for the ten unordered $3+3$ partitions of the six labels. Each belongs to one of the ten supports, once. The [earlier trihedral-pair enumeration](w33_e6_120_steiner_trihedral_pairs.py) detects the 9-line carriers as complements of double-six triples. Here they select ten quiver supports for each of the 36 double-sixes. The rule uses only incidence and is Weyl-equivariant.

Run the exact certificate producer with NetworkX installed.

    python -B analysis/toe_20261115_cubic_quiver_ovoid.py

The [certificate](../data/toe_20261115_cubic_quiver_ovoid.json) lists every double-six and its optimal supports, the exact coefficient errors by budget, and the trace critical rank strata. The weights are a reconstruction in the fixed signed Dickson basis. Establishing a physical mechanism that combines quiver descriptions or fixes their couplings requires additional dynamics.
