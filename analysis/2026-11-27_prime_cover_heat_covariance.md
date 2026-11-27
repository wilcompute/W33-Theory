# Prime-cover heat fluctuations: finite projective covariance and random-torus limit

2026-11-27. Independent continuation of 04d6eb4cc (higher-rank flat covers) and 3960347da (component fugacity). Audit scope: 399 unique commit entries on master from Nov 20 00:00 UTC through 6fd041f5a; selected relevant diffs inspected (not a full diff audit). Subsequent 29213010a determinant scaling also checked. Searches for heat return variance, Hecke equidistribution, Rogers, prime heat, random lattice found no directly equivalent result in returned hits. This does not establish priority.

## Exact covariance, all prime sizes

Let p be prime, d>=2, H a uniform hyperplane of F_p^d and Lambda its inverse image in Z^d. The continuous-time nearest-neighbor walk uses rate one per oriented direction. Write R_H(t) for its quotient return, and Y_H(t)=p R_H(t). Let h_t(v) be the heat kernel on (Z/p)^d, and w_t(v)=p h_t(v). Set S_t=p-w_t(0), and for every projective line ell (one-dimensional linear subspace) let b_t(ell)=sum_{v in ell excluding 0} w_t(v).

Put theta=(p^(d-1)-1)/(p^d-1) and eta=(p^(d-2)-1)/(p^d-1). Then

E Y_H(t)=w_t(0)+theta S_t,

Cov(Y_H(t),Y_H(s)) = (theta-eta) sum_ell b_t(ell)b_s(ell)
                         + (eta-theta^2) S_t S_s.

Proof: Y=w_t(0)+sum_{v!=0}w_t(v) 1_{v in H}. Two nonzero vectors on the same line have joint inclusion probability theta; independent vectors have probability eta, by counting projective normals annihilating their span. The formula includes d=2 (eta=0). The independent spectral calculation is Y=1+sum_{k in H^perp excluding 0} exp[-t lambda(k)], lambda(k)=2 sum_j(1-cos(2 pi k_j/p)). All projective normal lines partition nonzero characters. The verifier checks both formulas and a third direct primal enumeration, for 27 combinations of p,d,t,s. These are floating point checks of an exact combinatorial identity.

## Continuum distribution, not merely the ensemble mean

Take t=alpha p^(2/d), alpha>0. The lattices L=p^(-1/d)Lambda have determinant one and form the index-p Hecke orbit of Z^d. By Hecke equidistribution they converge weakly in the space of unimodular lattices to invariant probability measure. The dual spectral representation converges, uniformly on compact sets of lattice space, to

Y_alpha(L)=sum_{u in L*} exp(-4 pi^2 alpha |u|^2)
          =(4 pi alpha)^(-d/2) sum_{v in L} exp(-|v|^2/(4 alpha)).

Indeed centered representatives k of H^perp correspond to dual vectors u=p^(1/d-1)k; their exponent converges locally uniformly to 4 pi^2 alpha |u|^2. The lower bound sin(pi k_j/p)^2 >= 4 k_j^2/p^2 in the centered cube controls the omitted tails by Gaussian sums, uniformly on compact sets (shortest vector uniformly bounded below). The Gaussian tail outside the growing cube vanishes there as well. Tightness from equidistribution yields convergence in distribution; Poisson summation gives the second expression. No uniform control over the cusp is inferred from weak convergence. The theta functional is continuous and nonconstant: rectangular determinant-one lattices with a shrinking direction make it unbounded; Haar measure has full support. Thus the crossover observable does NOT converge in probability to a deterministic constant. The earlier subcritical diffusion-in-probability result is not contradicted.

## Critical variance for d>=3, and dimension-two divergence

Write r=p^(1/d) and g(x)=(4 pi alpha)^(-d/2) exp(-|x|^2/(4 alpha)). By the continuous-time local CLT, p h_infinite(alpha*r^2,v) tends to g(v/r) uniformly on bounded scaled sets. Truncate |v| at r log p: the omitted total scaled weight is O(p exp(-c log^2 p)), by the exponential moment of a difference of two Poisson variables in each coordinate. This also removes wraparound contributions and gives negligible covariance error, since 0<=Y<=p. For d>2 all 2x2 minors of pairs in the truncated region are o(p), so proportionality modulo p is precisely rational collinearity. The coefficient theta-eta is asymptotic to 1/p; the negative cross-term is O(p^(2-d)) and tends to zero.

For each unoriented primitive integer vector u the parallel pairs are m u,n u, nonzero signed integers m,n. The primitive-vector density is 1/zeta(d), obtained by Mobius inversion and Riemann sums. Consequently the limit is
  (1/(2 zeta(d))) sum_{m,n != 0} integral_R^d g(mx)g(nx) dx
= 2(4 pi alpha)^(-d/2)/zeta(d) sum_{m,n>=1} (m^2+n^2)^(-d/2).
For clarity, dominated convergence in the multiplier sum follows from the uniform bound p h_infinite(t,v)<=C exp(-c |v|^2/r^2) on |v|<=r log p. It follows by splitting the heat semigroup at t/2, using sup h_(t/2)=O(r^-d) (Fourier integral) and a Chernoff tail bound for the other half; at least one of the two summands must have norm >=|v|/2. The Gaussian sum over nonzero integer u is bounded by C r^d (m^2+n^2)^(-d/2) (including when (m^2+n^2)^1/2>r); the multiplier series is summable exactly for d>2. For fixed m,n the primitive Riemann sum follows by Mobius inversion with absolutely summable inverse powers. This proves convergence of the finite-p variances, not just the Haar second moment.

Using the square-lattice Epstein sum 4 zeta(s) beta(s) at s=d/2 (beta is Dirichlet beta), the answer is

Var limit = 2(4 pi alpha)^(-d/2) [zeta(d/2) beta(d/2)/zeta(d) - 1].

For alpha=1/2 the limits are 0.1115943979 (d=3) and 0.0198640572 (d=4).

For d=2, restrict to primitive directions of norm <=c sqrt(p) and integer multiples of norm <=sqrt(p)/4; distinct rational lines in this small box cannot coincide mod p (all minors <p). On this box w_t is bounded below by a positive constant at fixed alpha, by the local CLT. The positive parallel-pair contribution is at least C sum_{primitive u, |u|<=c sqrt(p)} |u|^-2 = Omega(log p), by primitive-vector density in annuli. The negative term is bounded because S_t<=p and eta-theta^2=-1/(p+1)^2. Hence the variance diverges at least logarithmically. No matching upper bound or exact leading coefficient is claimed.

## Interpretation and checks

The selected connected, flat ensemble admits typical local Euclidean diffusion, but global metric moduli survive at the critical volume scale. A TOE using these covers must either predict the distribution of moduli, or derive a new selector for them. The rank-two cusp divergence is a useful discriminator, not a derivation of three spatial dimensions. A scalar heat kernel is not a Lorentzian metric, Einstein dynamics, or a chiral matter theory. The calculation does not supply the dimension, flatness, connectivity, or a physical action.

Run: node analysis/toe_20261127_prime_cover_heat_covariance.js
The stored JSON uses that exact JS implementation, evaluated before commit. A separate NumPy enumeration reproduced means, variances, medians and maxima (median conventions differ for even counts). No local workstation available.

Prior art: Marklof and Strombergsson, random circulant graphs, https://arxiv.org/abs/1103.3152 ; Clozel, Oh and Ullmo, Hecke operators and equidistribution of Hecke points, https://doi.org/10.1007/s002220100126 ; Rogers second-moment background (Kelmer and Yu), https://arxiv.org/abs/1802.09645 ; Lawler and Limic, Random Walk: A Modern Introduction. The Haar-lattice moment framework is established; the finite projective covariance and crossover application here are a repository extension, not a claim of literature novelty.
