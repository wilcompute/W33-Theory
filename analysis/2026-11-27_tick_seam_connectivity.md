# Summable higher-order tick interactions still lose connectivity

On the labeled degree-two graph ensemble, the finite-density pair-swap result extends to **any bounded Hermitian interactions on consecutive sites with a summable boundary cost**. This includes signed and noncommuting higher-order terms. I construct one such all-order model from the repository's shared tick cumulants and verify a noncommuting three- and four-site control. The extension rules out connectivity selection by simply adding bounded local higher-order terms to this ensemble.

## Cut and rejoin bound

Use the same local site space on every graph and assign one copy of a Hermitian operator \(h_r\) to each oriented consecutive length-\(r\) window of a cycle. Use each site at most once in a window and omit the term on cycles shorter than \(r\). Use reflection-symmetric interactions or a consistent orientation convention. If restricting the trace, use the same invariant sector in the compared systems. Define

\[
K=\sum_{r\ge 2}(r-1)\|h_r\|.
\]

Cut one edge from each of the \(m\) cycles to leave paths. The remaining length-\(r\) windows are exactly the windows internal to those paths. The cut removes at most \(m(r-1)\) windows of each width. Rejoining the paths into a single ring introduces at most the same number. Thus \(\|H(G)-H(C_n)\|\le 2mK\) on the shared Hilbert space. The eigenvalue min-max principle bounds the absolute log partition-function ratio by \(2bmK\) at matter inverse temperature \(b\ge 0\). Positivity of Hamiltonian matrix entries is unnecessary. The same inequality follows directly from the usual quantum Gibbs variational principle. [Gibbs variational principle in many-body mechanics](https://jep.centre-mersenne.org/item/10.5802/jep.18.pdf)

For Wilson cycle weight \(q>0\), the fragmented-to-connected odds with matter are bounded below by \(e^{-2bK}\) times the matter-free odds at \(q_{\rm eff}=qe^{-2bK}\). The matter-free generating function has connected probability of order \(n^{-q_{\rm eff}/2}\). Hence every fixed finite \(b,K\) still gives vanishing connectivity. Reversing the inequality gives a lower bound with the corresponding \(qe^{2bK}\) exponent. These bounds do not identify the exact exponent. The earlier pair-swap proof achieves a better constant using swap positivity.

## An explicit convergence condition for an all-order shared-tick model

Let \(M_B\) be the average of products of tick projectors on distinct sites in a block \(B\), normalized by averaging over the 120 labels. Each such product is dominated in operator order by keeping just one site projector. Since the one-site average is \(I/3\), every nonempty block has \(\|M_B\|\le 1/3\). The coefficient on \(r\) distinct sites in the formal logarithm of \(\mathbb E\prod_i(1+z_i P_i)\) is a sum over set partitions. The block operators in each partition act on disjoint sites and commute. A partition with \(k\) blocks has coefficient \((-1)^{k-1}(k-1)!\). These square-free coefficients were obtained in the parallel [all-order exchange report](2026-11-27_all_order_exchange_connected_five_fronts.md).

Consequently its norm is bounded by \(a_r=\sum_k S(r,k)(k-1)!/3^k\), with \(S\) the Stirling numbers of the second kind. The exponential generating function is \(A(t)=-\log((4-e^t)/3)\), since the contribution with \(k\) blocks is \(((e^t-1)/3)^k/k\). If these square-free cumulants are used as consecutive-window interactions with supplied weights \(t^r/r!\), then

\[
K\le t A'(t)-A(t)
=\frac{t e^t}{4-e^t}+\log((4-e^t)/3),\qquad 0\le t<\log 4.
\]

This gives a concrete all-order family with finite boundary cost in which the obstruction holds even after including cross-direction signed cumulants. The factorial weights and consecutive-window placement are model choices. The derivation does not claim that the full logarithm of a univariate tick transfer operator has this decay, since that logarithm also contains repeated-site terms. It leaves open interactions with non-summable boundary cost, dynamic gauge histories whose Hamiltonian does not reduce to this form, and graph ensembles other than degree two.

The numerical control uses the single-qutrit factors of the repo's three-register projector and the averaged fourth-order reflections, with different signs in the Hamiltonian. It compares \(C_3+C_3\) with \(C_6\), verifies that overlapping terms do not commute, and checks the seam norm and free-energy differences at three temperatures. It also evaluates the exact combinatorial majorants and checks their summed boundary cost. Run `python analysis/toe_20261127_tick_seam_connectivity.py` to reproduce the certificate.
