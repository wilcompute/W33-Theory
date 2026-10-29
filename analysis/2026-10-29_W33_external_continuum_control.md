# A falsifiable continuum control: W33 internal modes × externally added cubic lattice

**October 29, 2026.** The W(3,q) point graph is diameter two, with degree growing in q and a three-atom adjacency spectrum. Existing repository work already identifies this as inadequate for an intrinsic Weyl-law/heat-kernel continuum limit. This packet does **not** rediscover or solve that no-go; it builds a clean *positive control* to isolate precisely the missing ingredient.

For each periodic cubic lattice \((\mathbb Z/m\mathbb Z)^3\), put a copy of W33 at each cell. Use the ordinary local graph Cartesian-product Laplacian
\[
L_{m}=L_{W33}\otimes I + I\otimes L_{\mathrm{cubic},m}.
\]
The W33 internal Laplacian has eigenvalues \(0^1,10^{24},16^{15}\). The lattice has one-dimensional Bloch energies \(\epsilon(k)=2(1-\cos(2\pi k/m))\), so its complete heat return per vertex is **exactly**
\[
P_m(t)=\frac{1+24e^{-10t}+15e^{-16t}}{40}
\left[\frac1m\sum_{k=0}^{m-1}e^{-2t(1-\cos(2\pi k/m))}\right]^3.
\]
Define the effective spectral dimension \(d_s(t)=-2\,d\log P_m(t)/d\log t\). The producer \`analysis/w33_20261029_external_3d_torus_control.py\` evaluates this analytically (no numerical differentiation). At \(m=80\), \(d_s(t)=3.64853,3.27546,3.15507,3.08401,3.05014\) for \(t=1,2,3,5,8\). The 39 nonconstant W33 internal modes are exponentially suppressed in this window, leaving the familiar three-dimensional diffusion sector. The spatial lattice's smallest positive energy tends to zero as \(m^{-2}\).

**Logical implication:** the exact finite W33 internal data do not prevent continuum-like diffusion if one **adds external local space**. The experiment isolates the needed *external* ingredient; it is not an intrinsic W33 derivation, and the continuum here is Euclidean heat propagation rather than dynamically curved 3+1 Lorentzian spacetime. An actual TOE requires deriving locality, causal structure, a dynamical metric and its coupling to matter without assuming the desired geometry at the outset.

The result is a conventional local product-graph construction; no originality is claimed for its spectral formula, only for its targeted use as a W33 control and its independently executable certificate.
