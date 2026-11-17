# A quantized warped background in the capped M5 fold regime

The [nonlinear normal-graph calculation](2026-11-16_Tpq_M5_cap_nonlinear_fold.md) found a fold and action exchange at chosen pressure ratios near \(\alpha=0.91758\). The three original warped backgrounds sat above that range. Solving the [coupled Type IIB equations](2026-11-16_Tpq_coupled_warp_branch.md) along the polar branch gives a primitive integer pair \((p,q)=(100,107)\) with \(\alpha=0.9173606959\), inside the negative-quartic, positive-sixth region. The probe action crossing can be realized by a rectangular torus with these magnetic flux ratios. [Warped Type IIB field equations](https://arxiv.org/abs/hep-th/0510125) · [Wrapped M5 probe channel](https://arxiv.org/abs/2610.08939)

## Chern quantization and numerical background

Vary the shape in the common even axial differential equations with \(k_1=4(1+\eta)\) and \(k_2=4(2-\eta)\), keeping the polar quadrupole sign. The shape scan brackets the desired pressure ratio. Each candidate is then evaluated at the root of
\[
 q^2\eta(2-\eta)^2-p^2(1-\eta)(1+\eta)^2=0
\]
for primitive integer \(p,q\). This equation is the Einstein Chern relation for the unwarped reference connection in the ansatz. The actual connection used for the warped solution is the deformed one with fixed curvature integrals. The certificate retains the scan, the final field profiles, and checks of both the retained equations and the separately evaluated traceless one. Refinement from 23 to 28 even Legendre harmonics changes the pressure ratio by less than \(2\times10^{-9}\) and both sampled equation residuals are below \(10^{-10}\). These are numerical checks on the branch, rather than a global existence theorem beyond the earlier local analytic construction.

The pressure ratio is obtained from the actual warp minimum, \(\alpha=e^{4A_{\min}}\), at a pole. At this value the quartic is approximately \(-2.57415\times10^{-5}\) and the reduced sixth-order coefficient is \(+2.28023\times10^{-3}\). The same full nonlinear cap solver gives a fold at \(K-K_c=4.08836\times10^{-7}\) and equal action at \(3.05843\times10^{-7}\). At a shared detuning of approximately \(2.75259\times10^{-7}\) the small and large modulated caps have action excesses \(+5.3062\times10^{-11}\) and \(-4.5954\times10^{-11}\), respectively, relative to the uniform cap in the fixed normalization.

## Exhibit a torus compatible with the periods

Use the [eleven-dimensional lift](2026-11-16_Tpq_warp_mtheory_lift.md) at fixed Page period. The unwarped torus area in AdS units is \(16\pi p/(N_0 k_2\sqrt{8\eta})\). At fixed Page period it acquires the factor \(1+j_P\) from the horizontal flux integral, with \(j_P\) its relative shift before restoring the scale. The local area in units of the local AdS length then also picks up \(e^{4A_*/3-2C_*}\) from the warped metric. At the nonlinear equal-action point, choose the spectator circumference \(2\pi/\sqrt{K}\) and take the longitudinal one to be the area divided by it. The resulting rectangle has side lengths \(8.28946\) and \(51.47065\) in local AdS units, while the unmodulated cap occupies a width of \(6.56198\) along the long direction. The cap therefore has room for the small modulations without approaching its periodic images. The transverse size is a shape modulus at these classical orders, so choosing the equal-action value does not require discretizing the circumference independently.

The periods can be \((N_0,N_1,N_2)=s(1,100,107)\) for positive integer \(s\). The common mixed-flux factor changes the IIB fiber quotient and preserves the local dimensionless warp profile. Scaling all periods together increases the eleven-dimensional lengths in Planck units at fixed dimensionless shape. It also makes the fractional one-unit source charge small. This establishes compatibility of the numerical probe configuration with the flux lattice. It does not compute the backreaction, higher-derivative change of the fold, or behavior of the modulated cap after continuation.

Reproduce the [certificate](../data/toe_20261116_Tpq_quantized_cap_fold.json) with `py -3 -B analysis/toe_20261116_Tpq_quantized_cap_fold.py`.
