# Code-distance risk and the heat-return cusp in prime covers

2026-11-27. Continuation of 4a2a9acfe and afa7044e. Repo search for short relation systole probability did not surface a directly equivalent formula (not exhaustive). Literature background: Siegel primitive lattice averages and Rogers second moments, https://doi.org/10.3934/jmd.2025015 and https://academic.oup.com/imrn/article/2021/8/5825/5314048 ; Hecke equidistribution https://doi.org/10.1007/s002220100126 ; established geometry of numbers. We derive the following finite incidence formulas directly, without relying on random-lattice moment convergence.

Fix prime p, rank d>=2, H uniform hyperplane of F_p^d, Lambda its inverse image in Z^d. Use the cubical edge CSS code from previous pass. Its Z distance is exactly the L1 shortest nonzero lattice vector. For integer 1<=R<p, let M be the number of distinct projective residues represented by primitive integer vectors v with 0<||v||_1<=R, identifying signs. Any vector in this ball can be reduced to primitive by dividing the coordinate gcd (invertible mod p), so dZ<=R iff at least one of those projective lines belongs to H. Let X count these lines. Hyperplane incidence gives

E X = M theta, E X(X-1)=M(M-1) eta,
theta=(p^(d-1)-1)/(p^d-1), eta=(p^(d-2)-1)/(p^d-1).

Writing mu=M theta and f=M(M-1) eta, the union bound, two-term Bonferroni bound, and Cauchy-Schwarz/Paley-Zygmund give

max(mu-f/2, mu^2/(mu+f)) <= Pr(dZ<=R) <= min(1,mu).

These are exact finite-p bounds on distance risk, not actual decoder failure probability. For d=2 a hyperplane is itself one projective line, so the probability is exactly M/(p+1), with no approximation. If R^2<p all primitive directions up to signs remain distinct mod p: proportional residues imply all 2x2 minors divisible by p, but the absolute minors are at most R^2, hence zero. Thus the rational directions coincide and primitive representatives differ only by sign.

For fixed a>0, R=floor(a p^(1/d)), in d>=3 the minor condition holds for sufficiently large p. Primitive vector density from Mobius inversion gives M/p -> C_d a^d, C_d=2^(d-1)/(d! zeta(d)), using volume of the L1 unit ball. Therefore, for small a, along primes the distance-risk probability is squeezed between C_d a^d - O(a^(2d)) and C_d a^d (in liminf and limsup). For d=2 and 0<a<1 the limit is exactly a²/zeta(2), by the minor condition and disjoint events. This is an elementary finite-projective version of small-radius lattice systole estimates. It supplies a quantitative tail beyond the typical-distance exponent in the previous pass.

## Joint heat and code obstruction

Write Y=p R_H(t), t=alpha p^(2/d), h_t the heat kernel on (Z/p)^d. If a projective line ell lies in H then
 Y >= p sum_{v in ell} h_t(v).
This is a finite exact lower bound since all heat terms are nonnegative; code distance risk implies at least the minimum of these line weights over short directions. The verifier checks the bound against the independently computed dual spectral return for every failed geometry at six enumerated ensembles, using direct 1D Fourier heat kernel products.

For fixed a>0 and any H with dZ<=a p^(1/d), choose a shortest v in Lambda. Since ||v||_2<=a p^(1/d), the infinite-grid heat kernel wrapped over Lambda gives, for every fixed J, 
 liminf Y >= (4 pi alpha)^(-d/2) sum_{j=-J}^J exp(-j² a²/(4 alpha)).
This follows by the local CLT uniformly on the bounded scaled set of all jv, and positivity; letting J grow yields the Gaussian theta sum. The same deterministic inequality holds directly in the continuum for Y_alpha(L) when the L1 systole of the unimodular L is at most a. Poisson summation in one dimension shows the lower bound is asymptotic to (4 pi alpha)^(-(d-1)/2)/a as a->0. Combined with the short-distance probability lower bound (or the same limiting Haar probability by Hecke equidistribution and continuity of systole away from null-measure level sets), the limiting heat observable has tail at least c y^-d for sufficiently large y. Hence every moment of order r>=d diverges in the Haar limit. No matching upper bound or exact coefficient for the heat tail is claimed. Weak convergence plus lower semicontinuity/truncation then gives divergence of corresponding uncentered finite-p moments. Because the limiting mean is finite, centered absolute moments of these orders diverge too (finite-p mean remains bounded by the previous mean formula).

In particular rank3 has finite limiting variance (previous pass) but divergent third absolute moment, rank4 divergent fourth. Demanding finite moments of every order would reject every fixed d in this uniform model; the earlier variance criterion alone is not a fundamental selection law. A metric-moduli or cusp-suppression mechanism is needed if stronger stability is a physical requirement. Short logical strings and large critical-scale return fluctuations are tied through the same short lattice vectors, but high return need not imply poor code distance at an arbitrary finite threshold. This is not a proof of self-correction, gravitational dynamics, or actual physical dimension selection.

Replay: node analysis/toe_20261127_prime_code_heat_risk.js. Exact integer first and factorial second incidence counts, numerical Fourier comparison. All six selected ensembles fully enumerated, not Monte Carlo. No workstation/CI replay. 
