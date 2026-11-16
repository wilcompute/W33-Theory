# Probe index of the primitive torus-wrapped M5

The [minimum-action torus probe](2026-11-16_Tpq_M5_probe_action.md) wraps \(S^4_a\times T^2\) at a minimum of \(A\) in the [warped eleven-dimensional lift](2026-11-16_Tpq_warp_mtheory_lift.md). The remaining four embedding scalars and the Abelian chiral two-form add no negative modes to the radial sector. The internal normal mass matrix has trace exactly \(16/a^2\). On the axial branch the positive eigenvalues are two copies of \(8/a^2\) at a pole or one copy of \(16/a^2\) at the equator, with a different number of internal collective coordinates in each case. The calculation uses the two-derivative single-brane probe action with vanishing background worldvolume three-form and compatible flat \(C\)-field data. [M5 action](https://arxiv.org/abs/1308.2231) · [M5 Hamiltonian](https://arxiv.org/abs/hep-th/9805065)

## Internal normal fields and quadratic decoupling

At the saddle point \(y_*\), use fixed product coordinates on the worldvolume and vary a graph in the four-dimensional base transverse to the wrapped torus, with normal displacement \(\xi\). In the induced metric the gradients of \(\xi\) enter quadratically with the positive base metric. At zero gradient the product volume density depends on the base position through \(e^{4W}\rho^{-4/3}=e^{4A}\). Its first variation vanishes at \(y_*\), and the second variation divided by the common positive tension is \(4\nabla^2 A(\xi,\xi)\). The connection used in this Hessian can be that of the physical eleven-dimensional base metric because \(dA=0\) at the evaluation point. The quadratic mixed term with the radial normal is zero for the same reason.

In the electric potential choose the local representative \(C_4^{\rm ext}\wedge\gamma\), with \(dC_4^{\rm ext}=dV_{H^5}\) and \(\gamma=e^{5W}*_6G_4\). The coefficient of the reference torus area form in \(\gamma\) is independent of the transverse position. The other components are two-forms on the base spheres. Each starts at second order under pullback to the torus graph, with a constant coefficient at \(y_*\) multiplying \(d_T\xi^i\wedge d_T\xi^j\). The integral over the torus vanishes for smooth periodic displacements, at every external point. The sphere components of \(\gamma\) therefore give no quadratic term. This also removes the possible gradient term of either sign from the Wess–Zumino contribution.

The pullback of the magnetic four-form vanishes on the unperturbed product. Its first variation is \(d\,X^*(\iota_\xi G_4)=0\). Contraction of any horizontal or mixed component of \(G_4\) still leaves at least one transverse base leg. Consequently the first variation of the pulled-back \(C_3\) is exact and can be absorbed into the gauge-invariant chiral field strength. The unperturbed \(C_3\) pullback can be set to zero in the compatible flat sector, and \(H^3(S^4\times T^2)=0\). This makes the embedding and chiral quadratic actions independent. At higher order the pullback of \(G_4\) can be nonzero and the worldvolume Bianchi identity matters again.

## An exact mass trace

Let \(g_{6,B}\) be the lifted base metric and \(h_B=e^{2D}g_1+e^{2B}g_2\) the conformal-frame base from the [coupled equations](2026-11-16_Tpq_coupled_warp_branch.md). At a critical point of \(A\),
\[
 e^{2W}\Delta_{g_{6,B}} A=e^{16A/3}\Delta_h A
 =4(e^{-8A}-1).
\]
The first equality uses \(e^{2W}g_{6,B}^{-1}=e^{16A/3}h_B^{-1}\) and the vanishing first derivatives. The second is the exact scalar equation; the fiber derivative of \(A\) is zero. With \(\alpha=e^{4A_*}\) and \(a=e^{W_*}\alpha/\sqrt{1-\alpha^2}\), the mass trace becomes
\[
 a^2\operatorname{tr}M^2_{\rm normal}
 =4a^2\Delta_{g_{6,B}}A
 =16\,\frac{\alpha^2}{1-\alpha^2}(e^{-8A_*}-1)=16.
\]
Since \(A_*\) is a minimum, all four eigenvalues are nonnegative. The second sphere is a two-dimensional family of equivalent positions and contributes two zeros. At a polar minimum on the first sphere, the fixed-point rotations force the two remaining eigenvalues to agree. At an equatorial minimum, one further eigenvalue vanishes along the circle of equivalent positions. Thus the polar masses are \(a^{-2}(8,8,0,0)\), and the equatorial masses are \(a^{-2}(16,0,0,0)\). These are exact under the specified symmetry. The Pell sequences approach a polar minimum on the negative-amplitude side and an equatorial one on the positive-amplitude side. The numerical checks use \((7,8),(8,9),(38,43)\) and recover the exact nonzero values within \(2\times10^{-8}\).

Each internal eigenvalue receives the nonnegative addition \(\ell(\ell+3)/a^2+|k_T|_{\rm phys}^2\) at sphere harmonic \(\ell\) and physical worldvolume torus momentum \(k_T\). The IIB D3 check is also direct. In bubble-radius units the physical base Hessians agree because \(e^{2W}g_{6,B}^{-1}=e^{2A}g_{Y,B}^{-1}\). At zero worldvolume torus momentum the M5's flat two-form holonomy provides the compact scalar that corresponds to the D3 fiber position; the other tensor zero-momentum fields give the D3 Maxwell field. [Torus reduction of the self-dual tensor](https://arxiv.org/abs/0905.2720)

## Chiral modes and the total probe index

Use the physical Euclidean contour obtained by continuation of the Lorentzian chiral Hamiltonian. A real self-duality condition on Euclidean three-forms would have the wrong Hodge-star square. With zero torus momentum the chiral field gives a four-dimensional Maxwell field and a compact scalar from its torus holonomy. The scalar spectrum on \(S^4_a\) is \(\ell(\ell+3)/a^2\). The Maxwell transverse spectrum is \((\ell+1)(\ell+2)/a^2\) for \(\ell\ge1\), with no harmonic one-forms. At nonzero torus momentum choose a local orthonormal torus frame with its first direction parallel to \(k_T\). The gauge component with a first-direction leg can be removed because that Fourier derivative is invertible. The remaining four-dimensional two-form and one-form are related by the linear self-duality constraint, which gives a single Proca field of squared mass \(|k_T|_{\rm phys}^2\). Its transverse eigenvalues are \((\ell+1)(\ell+2)/a^2+|k_T|_{\rm phys}^2\). These positive quadratic operators have no negative directions. The harmonic two-form on \(T^2\) contributes one compact flat holonomy, and there is no harmonic three-form on the worldvolume. [Round differential-form spectra](https://doi.org/10.18910/6956)

The resulting bosonic probe index is exactly
\[
 1+\#\{\,k_T\ne0:\ |k_T|_{\rm phys}^2<4/a^2\,\},
\]
where the count uses signed lattice labels, giving the correct two real modes for a nonzero pair of opposite momenta. Equality produces additional radial zeros. Away from such threshold equalities the bosonic collective coordinates are the five external center coordinates, two or three internal position coordinates, and the compact holonomy. In the [large-radius fixed-shape window](2026-11-16_Tpq_M5_probe_action.md) the count is zero and the full bosonic physical probe has index one. The determinant phase, fermionic spectrum, bulk perturbations and dynamical backreaction are separate from this quadratic probe result.

Reproduce the [JSON output](../data/toe_20261116_Tpq_M5_probe_index.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_probe_index.py`.
