# Full Sp(4,3) normalizer of the E8-derived Pauli representation

The E8 construction fixes a distinguished two-qutrit Pauli basis
\[
(X_{\rm int},X_{\rm ext},Z_{\rm int},Z_{\rm ext})
\]
on the projective phase space \(\mathbf F_3^4\).

The repository already contains four explicit symplectic transvections that generate
\[
\boxed{|Sp(4,3)|=51,840}.
\]
In exactly the same coordinate gauge, the qutrit Clifford ABI provides \(9\times9\) unitary lifts satisfying
\[
U_TD_xU_T^\dagger=D_{Tx}
\]
with no residual Pauli phase in the chosen odd-prime Weyl convention.

This pass checks all four transvections against the E8-derived commutator form and all 81 Weyl labels per generator, for 324 exact conjugation checks. The projective permutations act on the same 40 rays as the certified \(E_8\to W33\) bridge.

Therefore the representation normalizer is
\[
\boxed{3_+^{1+4}:Sp(4,3)}.
\]

The boundary is essential: the Pauli subgroup itself is constructed inside E8, but this calculation proves the full symplectic group as a normalizer of its 9-dimensional Schrödinger representation and projective phase space. It does **not** prove that every Clifford lift lies inside compact E8, nor that
\[
N_{E_8}(3_+^{1+4})=3_+^{1+4}:Sp(4,3).
\]
