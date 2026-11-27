# With both gluing permutations free, flatness and connectivity need separate weights

Let \(a,b\) range independently over all permutations of \(n\) sites. Give a configuration weight \(e^{-\beta|\operatorname{supp}[a,b]|}\). This removes the supplied horizontal cycle from the earlier square-gluing model. **The plaquette penalty selects exact flatness for \(\beta-\log n\to+\infty\), but the probability of being both flat and connected tends to zero at every coupling.** A separate penalty per component can select one connected torus cover. Its scale is explicit, including the critical crossover along prime sizes.

## Flatness alone leaves many torus covers

A commuting pair is a labeled action of \(\mathbb Z^2\). Its joint orbits are the connected covers. A transitive action of size \(m\) is specified up to isomorphism by an index-\(m\) subgroup of \(\mathbb Z^2\). Hermite normal forms count \(\sigma_1(m)\) subgroups, and each action has \(m\) automorphisms, namely translations. Thus the exponential generating coefficient for one component is \(a_m=\sigma_1(m)/m=\sum_{d\mid m}1/d\). The coefficient for all flat pairs is the partition number \(p(n)\), by the assembly formula or the centralizer count. The conditional probability of a single component on the flat branch is exactly \(a_n/p(n)\). Since \(a_n\le1+\log n\), the Hardy–Ramanujan growth of \(p(n)\) makes this probability vanish. This upper bounds the unconditional probability of the joint flat and connected event for every \(\beta\). [Commuting tuples and subgroup counts](https://pmc.ncbi.nlm.nih.gov/articles/PMC11449981/) · [Hardy–Ramanujan partition asymptotics](https://ramanujan.sirinudi.org/Volumes/published/ram36.html)

For a specified commutator \(g\), its number of permutation pairs is at most the number of commuting pairs. Indeed for each \(a\), the possible choices of \(b\) form an empty set or a coset of its centralizer. Summing this bound gives \(n!p(n)\). There are at most \(n^j\) permutations with support \(j\), and a nonidentity commutator is even and moves at least three sites. Thus at \(\beta=\log n+c\), \(c>0\), nonflat-to-flat odds are at most \(e^{-3c}/(1-e^{-c})\). At \(\beta\le(1-\delta)\log n\) for fixed \(\delta>0\), the full partition sum is at least \((n!)^2 e^{-\beta n}\), which makes the flat probability tend to zero. These bounds locate the leading flatness threshold. They do not give an exact critical-window law for flatness with both permutations free.

## A separate component weight has a prime-size critical window

On the flat ensemble insert \(q\) per joint orbit. Its weight after dividing by \(n!\) is

\[
f_n(q)=[z^n]\exp(q A(z)),\qquad A(z)=\sum_{m\ge1}a_m z^m .
\]

Consequently \(n f_n=q\sum_{m=1}^n \sigma_1(m)f_{n-m}\), \(f_0=1\), and the probability of one cover is \(q a_n/f_n(q)\). This orbit-weighted ensemble is established. The results below concern its size-dependent low-weight regime. [Abdesselam and Starr on orbit-weighted commuting tuples](https://arxiv.org/abs/2505.11469)

Write \(a^{*k}(n)\) for the coefficient of \(A(z)^k\). The first and second moment bounds

\[
\sum_{m\le n}a_m\le n\zeta(2),\qquad
\sum_{m\le n}a_m^2\le n C,\qquad
C=\sum_{d,e\ge1}\frac{\gcd(d,e)}{d^2e^2}<\infty
\]

follow by interchanging the divisor sums and counting multiples of the least common multiple. Cauchy–Schwarz bounds \(a*a\) by \(nC\), so \(a^{*k}(n)\le C\zeta(2)^{k-2}n^{k-1}\) for \(k\ge2\). Since \(a_n\ge1\), these estimates show that \(qn\to0\) selects one component uniformly over sizes. The two-component term alone shows that \(qn/a_n\to\infty\) excludes one component. At prime sizes \(a_n=1+1/n\), so these two regimes meet at \(q\) of order \(1/n\).

For the exact prime-size crossover, fix \(k\ge2\) and truncate all divisors in \(a_m\) at \(D\). For each fixed tuple \((d_1,\ldots,d_k)\), the equation \(\sum d_i x_i=n\) with positive \(x_i\) has no solutions for sufficiently large prime \(n\) if their gcd exceeds one. If their gcd is one, the coefficient of \(\prod_i z^{d_i}/(1-z^{d_i})\) has leading term \(n^{k-1}/[(k-1)!\prod_i d_i]\). The pole at 1 has order \(k\) while all other poles have smaller order. Multiplying by the reciprocal divisor weights and summing yields the primitive divisor sum. Truncation can be removed uniformly: the mean square of the reciprocal-divisor tail is at most \(n\sum_{d,e>D}\gcd(d,e)/(d^2e^2)\). In each telescoping difference of convolutions pair the tail with another factor by Cauchy–Schwarz and bound the remaining factors by the first moment. The normalized tail bound tends to zero with \(D\).

The primitive divisor sum is \(\zeta(2)^k/\zeta(2k)\), obtained by splitting all tuples by their common gcd. Thus for \(q=c/n\), along primes,

\[
\lim P(\text{one cover}\mid\text{flat})
=\left[1+\sum_{k\ge2}
\frac{c^{k-1}\zeta(2)^k}{k!(k-1)!\zeta(2k)}
\right]^{-1}.
\]

The convolution bound justifies termwise convergence for every fixed \(c\ge0\). The verifier enumerates all commuting pairs through \(n=5\), compares exact orbit-weighted totals with the recurrence, and checks the limit numerically on prime sizes through 4093. Nearby composite controls emphasize why the prime-size qualification matters.

An explicit sufficient joint regime in the full ensemble is \(q=n^{-2}\) per orbit and \(\beta=\log n+\sqrt n\). Divide the nonflat weight bound by the single-component flat weight \(q n!a_n\), and use the original unweighted commutator bound because \(q\le1\). The resulting relative weight is at most \(p(n)e^{-3\sqrt n}/[q a_n(1-e^{-\sqrt n})]\), which vanishes, and \(qn\to0\) suppresses disconnected flat covers. This gives a connected flat outcome without fixing either permutation. The supplied orbit penalty is global and the sufficient plaquette scaling is deliberately coarse. A local microscopic replacement for the orbit penalty and a physical spacetime interpretation remain open.

At prime sizes a uniform single cover has a uniform index-\(n\) subgroup among \(n+1\) kernels classified by the projective line over \(\mathbb F_n\). For \(R<n\), each nonzero integer vector of length at most \(R\) in the Manhattan metric belongs to exactly one kernel. Thus the fraction of covers with a relation this short is at most \(2R(R+1)/(n+1)\). If \(R=o(\sqrt n)\), the covering graph therefore has exact induced square-grid balls of radius \(\lfloor(R-1)/2\rfloor\) with probability tending to one. Unlike the earlier cyclic construction, neither coordinate is chosen as a distinguished spanning cycle. The verifier counts the short-relation kernels explicitly as a separate check.
