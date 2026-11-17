# Nonuniform radial bifurcations of the wrapped M5 probe

The [wrapped M5 probe index](2026-11-16_Tpq_M5_probe_index.md) identifies torus-momentum radial zero modes when the physical worldvolume wave number reaches \(2/a\). They do generate nearby nonuniform saddles. The bifurcation is subcritical: the saddles lie on the side where the round probe's torus modes are still positive, and they have higher action. This holds for every shortest-momentum shell, including degenerate shells. The square torus has both a stripe and a branch with equal modulation along both axes. The calculation is for unfluxed single-brane probes. [M5 action](https://arxiv.org/abs/1308.2231) · [Perturbative bifurcation method in a different gravitational problem](https://arxiv.org/abs/gr-qc/0608115)

## The radial graph and its reduction at threshold

Fix the internal position at a polar or equatorial minimum of the near-resonant warp. Both \(A\) and the torus radius have zero base gradient there by axial symmetry and evenness. The pressure coefficient on the wrapped torus is independent of that position. Thus radial graphs at fixed internal position solve the first variation in the transverse base directions as well. The ambient magnetic four-form pulls back to zero, so vanishing worldvolume three-form remains admissible. The same is true for external variations changing the four-sphere shape, since the radial graph preserves its \(SO(5)\) symmetry.

Let the hyperbolic distance be \(r(\theta)\), where \(\theta\) is a coordinate on the wrapped flat torus. Normalize a reference flat torus metric so its shortest-momentum modes obey \(\Delta f=-f\), take \(K\) to be their common squared physical wave number in local AdS units, and let the reference gradient be \(\nabla\). The action, divided by the positive factor \(\Omega_4 T\) of the [round probe](2026-11-16_Tpq_M5_probe_action.md), is the average over the reference torus of
\[
 \sinh^4r\sqrt{1+K|\nabla r|^2}
   -4q_0\int_0^r\sinh^4 v\,dv,\qquad q_0=1/\alpha.
\]
Put \(r=r_0+x\) with \(\tanh r_0=\alpha\) and \(u=\operatorname{csch}^2r_0=q_0^2-1\). Normalize action differences further by \(\sinh^4r_0\). The quadratic form is then \(\langle K|\nabla x|^2/2-2u x^2\rangle\) and the critical value is \(K=4u\). This is precisely the earlier radial index threshold. A torus rescaling at fixed shape varies \(K\), and the quantized fluxes sample this scale discretely if the shape is fixed.

At \(K=4u\) the cubic density is \(-4q_0u x^3+8q_0u x|\nabla x|^2\). On the critical eigenspace its integrated value vanishes by \(\langle f|\nabla f|^2\rangle=\langle f^3\rangle/2\). This cancellation also applies to a shortest shell with resonant triads. The cubic variational source is \(F=4q_0u f^2-8q_0u|\nabla f|^2\). The complementary quadratic operator \(H=4u(-\Delta-1)\) is invertible away from the critical modes. It obeys \(H(-q_0 f^2)=-F\); if \(f^2\) has a critical component, project that component out of the response. Because \(F\) is orthogonal to the kernel, the projection does not change the quartic action. In particular the constant radius is allowed to adjust even though it is itself a negative direction.

Combining the direct quartic action and \(\langle F(-q_0 f^2)\rangle/2\), and using \(\langle f^2|\nabla f|^2\rangle=\langle f^4\rangle/3\), gives
\[
 {\cal Q}_4(f)=u^2\left(\frac13\langle f^4\rangle
                                     -2\langle|\nabla f|^4\rangle\right).
\]
Write \(f=\sum_i a_i\cos(k_i\cdot\theta+\varphi_i)\) for one representative of each opposite pair in the critical shell. In two dimensions four unit vectors that sum to zero pair into opposites. To see this, two vectors of prescribed nonzero sum are determined as an unordered pair by intersecting the unit circle with its translate; if the sum is zero the pairing is immediate. Thus the quartic averages are phase-independent and
\[
 {\cal Q}_4=-u^2\left[\frac58\sum_i a_i^4
          +\sum_{i<j}\left(\frac12+2(k_i\cdot k_j)^2\right)a_i^2a_j^2\right].
\]
In particular it is negative definite. If \(\sigma=K-4u\), the reduced action begins with \((\sigma/4)\sum_i a_i^2+{\cal Q}_4\). The derivative along common amplitude scaling excludes a sufficiently small nonzero solution for \(\sigma\le0\). For \(\sigma>0\), any sufficiently small nonuniform solution has positive action excess and a negative amplitude direction at leading order. This follows by substituting its radial stationarity into the action and into its second derivative along amplitude scaling. The negative constant-radius direction survives in the complementary block.

## Stripe and square branches

A stripe uses one pair, and exists with \(a_1^2=\sigma/(5u^2)+O(\sigma^2)\). One can fix its phase and solve all other harmonics by the implicit function theorem. The exact translation by half its period flips its amplitude, giving the indicated even expansion. Its normalized action excess is \(\sigma^2/(40u^2)+O(\sigma^3)\). Its amplitude direction is negative and its phase is neutral. The competing shortest directions are positive to leading order: for a different pair with \(d=k_1\cdot k_j\) their slope is \(\sigma(3-8d^2)/10\) in cosine-amplitude coordinates. Shortest vectors in a lattice have \(|d|\le1/2\), since their sum and difference are also lattice vectors. For a degenerate shell this is a positive statement on all competing pairs because the quartic form has no phase dependence. Hence the stripe has index two in the radial graph sector close to the bifurcation.

For a square torus the mixed quartic coefficient is \(-u^2/2\). Exchanging the axes gives an invariant branch with equal modulation in both axes, \(a_1^2=a_2^2=\sigma/(7u^2)+O(\sigma^2)\). Its normalized excess is \(\sigma^2/(28u^2)+O(\sigma^3)\), larger than the stripe excess. Both its magnitude directions are negative and both phases are translations, giving index three in the radial graph sector. These local results do not exclude disconnected nonuniform saddles at finite amplitude.

The numerical check solves the full stripe equation
\[
 4\coth r/\sqrt{1+K r_\theta^2}-4q_0
         -K r_{\theta\theta}/(1+K r_\theta^2)^{3/2}=0
\]
at \(u=1\), using a Fourier projection of this exact equation and independent action integration. The prior large-radius fixed-shape Pell regime has no torus mode near the radial cutoff and is outside the bifurcation regime. The calculation stays within the classical probe action and does not compute bulk backreaction.

Reproduce the [certificate](../data/toe_20261116_Tpq_M5_nonuniform_probe.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_nonuniform_probe.py`.
