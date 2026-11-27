# Local tick refresh restores a bounded cut cost, but not a connected geometry

The previous shared tick model assigned a single randomly chosen label to each connected cycle. Its full logarithm has an extensive cost for rejoining two cycles. Here the label instead propagates through the supplied nearest-neighbor rule \(M=(1-\epsilon)I+\epsilon J/L\) with \(L=120\) and \(0<\epsilon\le1\). This restores a bounded cut cost and gives a finite label correlation length at every fixed positive refresh probability. The probability of a connected graph still tends to zero. At thermal power two, even arbitrarily weak fixed refresh restores the ordinary Wilson connectivity exponent. The approach to that limit is much slower than the loss of memory of a single label.

## Bounded operator cost and graph measure

For a ring, weight the label sequence by \(\prod_i M_{a_i a_{i+1}}\) and normalize by \(z_l=\operatorname{Tr}M^l\). The physical transfer \(K_l\) is the expectation of \(\bigotimes_i A_{a_i}\) with \(A_a=sI+(1-s)P_a\) as in the full shared-label model. On disjoint cycles labels are independent. At \(\epsilon=0\) this becomes exactly the shared-label prescription, and at \(\epsilon=1\) it gives an independent label per site. This is a finite-dimensional auxiliary transfer construction of the kind used in finitely correlated chains. [Fannes, Nachtergaele and Werner](https://doi.org/10.1007/BF02099178)

Cut one edge from each of \(m\) cycles. For each fixed assignment of labels, either set of rejoining edges contributes a factor between \(M_{\min}^m\) and \(M_{\max}^m\). Thus the two unnormalized physical transfers dominate each other in positive operator order up to \(R^m\), where \(R=M_{\max}/M_{\min}\). The normalizing label partition functions obey the same bound, giving factors \(R^{2m}\) for the normalized transfers. The logarithm is operator monotone, so the norm of the difference of their dimensionless Hamiltonians \(-\log K\) is at most \(2m\log R\). This controls rejoining operations. It does not assert a term-by-term short-range expansion of the operator logarithm.

At any fixed positive thermal power \(p\), eigenvalue monotonicity bounds the trace ratio after rejoining by \(R^{2pm}\) in either direction. The generating-function comparison from the previous bounded-cut theorem then applies with a strictly positive effective constant cycle weight \(qR^{-2p}\) for the upper bound on connectivity. This proves disconnection in probability throughout the fixed-positive-refresh model. In the infinite-chain label measure, the transition modes orthogonal to the uniform distribution decay as \((1-\epsilon)^d\) over distance \(d\). Since all \(A_a\) have the same trace, taking a normalized physical trace does not alter the original label probabilities for single-copy observables.

## Exact power-two law and singular small-refresh crossover

Put \(Z_2=3+6s^2\) and \(D_{ab,ab}=\operatorname{Tr}(A_a A_b)/Z_2\). The normalized power-two trace is

\[
\frac{\operatorname{Tr}K_l^2}{Z_2^l}
=\frac{\operatorname{Tr}S_\epsilon^l}{(\operatorname{Tr}M^l)^2},
\qquad S_\epsilon=D^{1/2}(M\otimes M)D^{1/2}.
\]

For fixed positive refresh, \(S_\epsilon\) is strictly positive entrywise and its largest eigenvalue \(\lambda\) is simple. It has nonnegative spectrum because \(M\) is positive semidefinite. After dividing by \(\lambda^l\), the power-two weight tends to one exponentially with \(l\). The factor \(\lambda^n\) cancels across all graphs of size \(n\), so the asymptotic Wilson fugacity is \(q\). At zero refresh, \(S_0=D\) has \(L\) maximal eigenvalues and \((\operatorname{Tr}M^l)^2=L^2\), yielding \(q/L\). The connectivity exponent therefore jumps from \(q/(2L)\) at zero refresh to \(q/2\) at every fixed positive refresh. The two limits do not commute.

For \(s=1/2\), the three entries of \(D\) are \(1,5/6,8/9\) for equal labels, unequal outcomes in the same direction, and different directions. Perturb \(S_\epsilon\) about \(\epsilon=0\) on the \(L\)-dimensional equal-label eigenspace. The first-order term is scalar since changing just one label leaves this eigenspace. The second-order effective matrix has constant diagonal. For distinct equal-label pairs \(aa\) and \(bb\) its off-diagonal entry is

\[
L^{-2}\left(1+\frac{2D_{ab,ab}}{1-D_{ab,ab}}\right).
\]

The \(1/L^2\) term is direct double refresh. The two intermediate states \(ab,ba\) supply the other term through the reduced resolvent \((I-D)^{-1}\). Thus the off-diagonal values within and between the 40 triples are \(a=11/L^2\) and \(b=17/L^2\). Removing the common diagonal, the three eigenvalues are \(2a+117b\) on the uniform mode, \(2a-3b\) for contrasts between triples, and \(-a\) for within-triple contrasts. Since \(b>a\), the separation of the two largest eigenvalues is \((3a+117b)\epsilon^2+O(\epsilon^3)=(337/2400)\epsilon^2+O(\epsilon^3)\). The associated replica relaxation length diverges as \((2400/337)\epsilon^{-2}\), while the underlying label length grows as \(\epsilon^{-1}\).

The executable verifier compares a three-class Perron reduction with the full 14,400-component replica operator, and independently contracts the two-site physical density for each refresh probability. Run `python analysis/toe_20261127_refreshing_tick_labels.py`. This is a controlled local label rule on the degree-two ensemble. It leaves open a derived microscopic label-update law, higher-dimensional graph selection and dynamical gauge links.
