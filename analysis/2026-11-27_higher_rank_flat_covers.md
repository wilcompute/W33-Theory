# Three- and four-direction flat covers have a stronger component scale

When all gluing directions commute, a penalty per orbit can select one connected cover. For \(d\) directions the critical scale along prime sizes is \(q=c/n^{d-1}\), so the required component suppression strengthens with dimension. The selected connected prime covers also have an exact ensemble heat-return identity. It extends the \(d\)-dimensional diffusion window to every time \(1\ll t\ll n^{2/d}\) in probability. These results impose pairwise commutation and the number of directions. They address the flat ensemble and do not select spacetime dimension dynamically.

## Orbit weights

A connected \(d\)-tuple represents a transitive \(\mathbb Z^d\)-action, specified by an index-\(m\) sublattice for a size-\(m\) orbit. Write \(a_d(m)=g_d(m)/m\) for the connected exponential generating coefficient, where Hermite normal form gives the subgroup count \(g_d(m)=\sum_{\prod_i u_i=m}\prod_i u_i^{i-1}\). Then \(a_d(m)=m^{d-2}B_d(m)\) with \(B_d(m)=\sum_{e\mid m}c_d(e)\) and

\[
c_d(e)=\sum_{\prod_{j=1}^{d-1} u_j=e}\prod_{j=1}^{d-1}u_j^{-j}.
\]

The full orbit-weighted coefficient is \([z^n]\exp(q\sum_{m\ge1}a_d(m)z^m)\). This model and the fixed-orbit counting problem are established. Here the target is the normalized size-dependent finite-orbit window and its geometry. [Orbit-weighted commuting tuples](https://arxiv.org/abs/2505.11469) · [Recent fixed-orbit asymptotics](https://www.evidencepress.org/releases/commuting-permutations-few-orbits/)

For a fixed \(k\ge2\) and prime \(n\), the normalized \(k\)-component convolution has the limit

\[
\frac{a_d^{*k}(n)}{n^{k(d-1)-1}}\ \longrightarrow\
T_{d,k}
=\frac{\Gamma(d-1)^k}{\Gamma(k(d-1))}
\sum_{\gcd(e_1,\ldots,e_k)=1}\prod_i\frac{c_d(e_i)}{e_i}.
\]

To see this, first truncate the divisor sum at a fixed cutoff. The coefficient for an orbit size divisible by \(e\) has a pole of order \(d-1\) at one with leading factor \(\Gamma(d-1)/e\), from the series \(\sum_{j\ge1}(ej)^{d-2}z^{ej}\). For a primitive tuple the other roots of unity cannot be poles of every factor, so they contribute lower powers. Nonprimitive tuples have no solutions at sufficiently large prime size. The truncation is uniform because \(\sum_{m\le n} B_d(m)=O(n)\) and \(\sum_{m\le n}B_d(m)^2\le n\sum_{e,f} c_d(e)c_d(f)/\operatorname{lcm}(e,f)=O(n)\). Indeed \(e c_d(e)=\sum_{\prod u_j=e}\prod_j u_j^{-(j-1)}\le (1+\log e)\prod_{j=2}^{d-2}\zeta(j)\). Fix the factors other than \(u_1\), which is then determined, and bound the remaining harmonic and convergent sums independently. This bound makes the least-common-multiple sum absolutely convergent. The mean square of the discarded divisor tail is \(o_D(n)\) by the same sum. Cauchy–Schwarz bounds the convolution of two factors uniformly and controls one discarded factor. The other factors use their first moment. Inserting \(m^{d-2}\le n^{d-2}\) gives the indicated scaling and a bound geometric in \(k\) after normalization.

The primitive sum is an Euler product whose \(p\)-factor is \(F_p^k-(F_p-1)^k\), with \(F_p=\prod_{j=2}^d(1-p^{-j})^{-1}\). Consequently at \(q=c/n^{d-1}\) the one-cover probability tends, along primes, to

\[
\left[1+\sum_{k\ge2}\frac{c^{k-1}}{k!}T_{d,k}\right]^{-1}.
\]

For \(c=1\), this is approximately 0.37458, 0.77465, and 0.94022 for two, three, and four directions. Along prime sizes, \(qn^{d-1}\to0\) gives one orbit with high probability and \(qn^{d-1}\to\infty\) excludes it, by the geometric convolution bound and the two-orbit term, respectively. This quantifies how the same orbit fugacity acts differently in each rank. It does not derive a rank-specific weight.

## Return probability on one uniformly chosen prime cover

A connected prime cover is \(\mathbb Z^d/\Lambda\), where \(\Lambda\) is the inverse image of a uniformly chosen hyperplane of \(\mathbb F_n^d\). A nonzero residue lies in that hyperplane with probability \(\theta=(n^{d-1}-1)/(n^d-1)\). A union bound over short integer vectors gives exact grid balls of radius \(o(n^{1/d})\) with probability tending to one, taking a radius at most half the shortest relation to avoid extra induced edges.

Write \(p_{\mathbb Z^d}(t,v)\) for the rate-one-per-edge continuous-time walk on the infinite grid. Projection to the quotient sums its heat kernel over \(\Lambda\). Averaging over the hyperplane gives the exact identity

\[
\mathbb E_\Lambda\,p_\Lambda(t,0)
=\theta+(1-\theta)\sum_{v\in n\mathbb Z^d}p_{\mathbb Z^d}(t,v).
\]

The quotient return minus the infinite-grid return is nonnegative. Its expectation is bounded by \(\theta+O((t+t^2)/n^4)\): the nonzero points in \(n\mathbb Z^d\) require displacement at least \(n\), and the symmetric walk's fourth moment is \(O(t+t^2)\). Markov's inequality and the infinite-grid asymptotic \((4\pi t)^{-d/2}\) give the same leading return in probability for \(1\ll t\ll n^{2/d}\). At \(t=\alpha n^{2/d}\) for fixed positive \(\alpha\), the scaled ensemble mean \(n\,\mathbb E p_\Lambda\) tends to \(1+(4\pi\alpha)^{-d/2}\). This last conclusion is about the ensemble mean, not the distribution of individual heat kernels. It is compatible with established geometric scaling of random circulant lattices. [Marklof and Strömbergsson](https://arxiv.org/abs/1103.3152)

The verifier exhausts the small commuting-tuple orbit counts, tests the prime crossover through 4093 sites, samples short lattice relations at 65,537 sites, and checks the heat-return identity by enumerating every hyperplane at prime size five. Run `python analysis/toe_20261127_higher_rank_flat_covers.py`.
