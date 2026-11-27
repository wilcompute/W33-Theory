# A local auxiliary-field realization of the component penalty

The component weight used to select one flat cover can be approximated uniformly by integrating out two fields with nearest-neighbor quadratic terms. The construction uses a small mass scale that runs with graph size. Fixed positive masses lose the desired penalty on large cycles. If the auxiliary fields carry a nontrivial flat gauge holonomy, the zero mode producing the penalty can disappear.

## Local expression and graph-uniform control

On a graph with combinatorial Laplacian \(L\), take one complex boson with kernel \(L+\delta I\) and one complex Grassmann pair with kernel \(L+\epsilon I\), with \(0<\epsilon\le\delta\). The normalized Gaussian integrals give

\[
Z(G)=\frac{\det(L+\epsilon I)}{\det(L+\delta I)}.
\]

The quadratic actions use on-site mass terms and one difference term per edge. They contain no explicit orbit count. The boson integral is convergent, and after the Grassmann integral every graph has a positive weight. This is a Euclidean auxiliary statistical construction. It does not furnish a physical Lorentzian matter multiplet. The individual Laplacian determinants are familiar from rooted spanning forests. [Chebotarev–Shamis matrix-forest theorem](https://arxiv.org/abs/math/0602575) · [Grassmann representations of forests](https://arxiv.org/abs/cond-mat/0403271)

With \(c\) components and \(q=\epsilon/\delta\), the Laplacian zero modes contribute exactly \(q^c\). For each strictly positive eigenvalue \(\lambda\), the logarithm of the remaining factor is between \(-(\delta-\epsilon)/\lambda\) and zero, by integrating the derivative of \(\log(\lambda+x)\). Consequently

\[
0\le c\log q-\log Z(G)\le(\delta-\epsilon)\operatorname{Tr}L^+
\le(\delta-\epsilon)n^2/6.
\]

The last bound is uniform over graphs whose present edges have conductance at least one. On a component of size \(m\), the reciprocal-eigenvalue sum is \(m^{-1}\sum_{i<j}R_{ij}\) by the effective-resistance formula and the row sums of \(L^+\). Each resistance is bounded by its distance in any unit-conductance spanning tree. The sum of tree distances is at most \(m(m^2-1)/6\): delete a leaf inductively, and use that the distances enumerated in increasing order from the removed leaf are at most \(1,\ldots,m-1\). Summing the component bounds yields \(\operatorname{Tr}L^+\le n^2/6\). A simple path attains the component bound, so the scale \(n^{-2}\) in the uniform estimate is relevant. Small-difference expansions improve the bound on particular geometries but need their own spectral input.

If a graph ensemble has any common base weight, the corresponding normalized measure with \(Z(G)\) has density between \(e^{-\eta}\) and \(e^\eta\) relative to the measure with \(q^c\), where \(\eta=(\delta-\epsilon)n^2/6\). This also holds after conditioning on any event common to both models. Thus for \(\delta=o(n^{-2})\) the two measures are uniformly close in total variation. For example, choosing \(\delta=n^{-3}\), \(\epsilon=q\delta\), and \(q=n^{-d}\) reproduces the previous single-orbit selection regime for flat prime covers of rank \(d\). A fixed \(q=c_0/n^{d-1}\) instead reproduces the nontrivial prime-size crossover at that \(c_0\). The bosonic and Grassmann resolvents are both becoming long ranged in this limit despite the local quadratic action. The mass hierarchy and its size scaling are supplied, not dynamically derived.

## Two failure modes

For a cycle of length \(l\), put \(\vartheta_\mu=\operatorname{arcosh}(1+\mu/2)\). Fourier eigenvalues give

\[
\det(L+\mu I)=e^{l\vartheta_\mu}(1-e^{-l\vartheta_\mu})^2.
\]

At fixed positive \(\epsilon,\delta\), the exponential bulk ratio cancels when the total site count is fixed. The remaining weight of a long component tends to one rather than \(q\). In a cycle assembly, its difference from one decays exponentially in length, so the fixed-mass ratio does not change the leading cycle generating-function singularity. A massless or volume-dependent limit is essential for this realization.

For a charged auxiliary pair, replace differences by covariant differences with a fixed unitary link field. The Laplacian kernel consists of covariantly constant sections, since its quadratic form is a sum of squares. On a connected cycle with holonomy \(e^{2\pi i/3}\) there is no such section, so the determinant ratio tends to one as both masses go to zero at fixed \(q\). Topological zero-mode suppression of every component therefore requires neutral auxiliaries, or a separately justified protected invariant section per orbit. [Kenyon's vector bundle Laplacian](https://arxiv.org/abs/1001.4028)

The verifier tests the error bound over every simple labeled graph through five vertices, checks a flat permutation ensemble directly against ideal orbit weights, and verifies the cycle determinant and the twisted-holonomy control. Run `python analysis/toe_20261127_local_component_fugacity.py`.
