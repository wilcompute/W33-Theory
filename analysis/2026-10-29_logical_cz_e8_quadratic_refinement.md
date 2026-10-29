# Transversal phase on the W33 adjacency code realizes four logical controlled-Z gates

**October 29, 2026.** Companion to \`analysis/2026-10-29_oddq_css_transversal_clifford_t_obstruction.md\`. This is a gate interpretation of a **previously established** \(E_8/2E_8\) quadratic isometry, not a claim to have discovered that isometry. Existing code \`analysis/w33_20261029_explicit_mod2_E8_isometry.py\` already proves the eight-dimensional plus-type quadratic space and explicit coordinate equivalence to \(E_8\) modulo two.

**Exact statement.** Let \(C=\operatorname{im}_{\mathbf F_2}A\subseteq\mathbf F_2^{40}\), with \(A\) the W33 point adjacency matrix. The prior \([[40,8,6]]_2\) CSS stabilizers are \(X(C),Z(C)\). The unique all-ones vector of weight 40 is in \(C\), so \(C^\perp=\ker A\) contains only even-weight vectors. Every \(c\in C\) has weight divisible by four.

Consequently the quadratic form
\[
Q([x])=\frac{\operatorname{wt}(x)}2\pmod2,\qquad [x]\in H=C^\perp/C
\]
is well-defined. Indeed, for \(x\in C^\perp,c\in C\),
\[
\frac{\operatorname{wt}(x+c)-\operatorname{wt}(x)}2
=\frac{\operatorname{wt}(c)}2-|\operatorname{supp}(x)\cap\operatorname{supp}(c)|
=0\pmod2.
\]
Its polar form is the nondegenerate alternating dot product on the eight-dimensional quotient. Exhaustive enumeration of its \(256\) classes gives \(136\) isotropic and \(120\) anisotropic classes; this is Arf invariant zero, the *plus-type* quadratic space underlying the existing \(E_8/2E_8\) identification.

For the CSS computational basis
\[
|\overline{x}\rangle=|C|^{-1/2}\sum_{c\in C}|x+c\rangle,
\]
the uniform physical phase gate \(S^{\otimes40}\) acts by
\[
S^{\otimes40}|\overline{x}\rangle
=(-1)^{Q([x])}|\overline{x}\rangle.
\]
There exists a hyperbolic logical basis \(e_1,f_1,\ldots,e_4,f_4\) satisfying \(Q(e_i)=Q(f_i)=0\) and \(B(e_i,f_j)=\delta_{ij}\). Writing \([x]=\sum_i(a_ie_i+b_if_i)\) yields
\[
Q([x])=\sum_{i=1}^4 a_ib_i.
\]
**Therefore, in this explicitly chosen logical basis, the native physical transversal \(S\) acts as \(\mathrm{CZ}_{12}\mathrm{CZ}_{34}\mathrm{CZ}_{56}\mathrm{CZ}_{78}\).** It is an entangling logical Clifford network, **not** a tensor product of eight independent logical phase gates. This follows despite \(S^{\otimes40}\) being only a product of single-physical-qubit gates: the logical encoding is nonlocal.

The companion \`analysis/w33_20261029_logical_cz_e8_quadratic_refinement.py\` reconstructs \(W(3,3)\), computes the kernel quotient \(24-16=8\), evaluates all \(256\) logical quadratic phases, constructs four hyperbolic pairs, and checks the entire truth table against four disjoint CZ gates. It must be run from the repository root using \`python analysis/w33_20261029_logical_cz_e8_quadratic_refinement.py\` after the first companion verifier has landed.

**Honesty boundary.** Four logical CZs require a choice of encoded computational basis, do not supply a native photonic two-photon gate, and do not by themselves establish universality, fault tolerance, dimensionful interactions, or a TOE. The 40-physical-qubit CSS block must not be conflated with a one-photon 40-mode Hilbert space.
