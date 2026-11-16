# Radial index of the detuned spherical D3 wall

The [spherical discharge calculation](2026-11-16_D3_spherical_discharge.md) excludes a finite-radius solution on the classical, round, homogeneously smeared D3 branch at charge-normalized tension. Reducing the tension by hand gives spherical saddles. For the six detuned saddles tested here, the constrained \(O(5)\)-invariant sector has index one. Its negative direction is a change of the wall radius with the breathing mode relaxed. The bulk fields on either side contribute a positive form when the wall radius and scalar value are fixed.

## Eliminate the radial lapse

Use \(ds^2=N(a)^2da^2+a^2d\Omega_4^2\), with \(a\) increasing from the regular center to the asymptotic boundary. Keep the exterior flux and AdS sources fixed. In each constant-flux region the Gibbons–Hawking term cancels the radial second derivative of the metric in the Einstein action. After dropping the common positive factor \(\Omega_4/(2\kappa_5^2)\), the bulk integrand in \(a\) is

\[
\mathcal L=N(a^4 V-12a^2)+N^{-1}(G a^4 b_a^2/2-12a^2),
\qquad G=80/3.
\]

Let \(x=\log a\), \(v=db/dx\), \(c=G/24=10/9\), \(K=(1-a^2V/12)^{1/2}\), and \(S=(1-cv^2)^{1/2}\). Solving the lapse equation on the branch with \(N>0\), \(K>0\), and \(S>0\) gives \(N=S/K\) and the integrand \(-24a^3 KS\) in \(x\). The Hessian in \((b,v)\), divided by \(24a^3\), is

\[
h=\begin{pmatrix}
-K_{bb} S & c v K_b/S\\
c v K_b/S & cK/S^3
\end{pmatrix},
\qquad
\det h=\frac{c}{S^2}\left(\frac{a^2V_{bb}}{24}+S^2 K_b^2\right).
\]

Thus \(V_{bb}>0\) is sufficient for a positive bulk quadratic form. For the repo's breathing potential \(V=q^{-4/3}(-20e^{-16\delta b/3}+8e^{-40\delta b/3})\), where \(\delta b=b-\log(q)/4\), the convexity condition is \(\delta b<\log(5/2)/8\). Both profiles of the six tested solutions stay in this interval and have \(V<0\). The regular interior shot starts above its minimum and increases to the wall. The normalizable exterior shot starts below its minimum when integrated inward and decreases to the wall. The sign of \(V_b\) prevents a first turning point in either integration direction by the radial scalar equation \(b''+4(a'/a)b'=V_b/G\). The wall value then bounds the relevant excursion. The background radial constraint gives \(S^2=K^2/(a')^2>0\), where \(a'=da/d\xi\) in proper radius \(\xi\).

## Reduce the index to the wall

Use \(x_s=\log a_s\) and \(b_s\) as independent endpoint variables. Split a radial variation into the response obtained by solving the linearized bulk equations with the specified endpoint variation, plus a variation that vanishes at the wall. The cross term vanishes by the linearized field equations, regularity, and fixed exterior sources. The wall action has no dependence on the fixed-endpoint fluctuations. Since the two fixed-endpoint blocks are positive, the negative index equals that of the Hessian of the on-shell bulk action plus the wall action in \((x_s,b_s)\).

In units \(q_+=L_+=1\), the wall term is \(a_s^4\tau\), where \(\tau=\alpha\,4(1-q_-)e^{-20b_s/3}\), and \(\alpha\) is fixed when differentiating. The bulk canonical momentum in the \(a\) coordinate is \(p=Ga^4 b'\) and its Hamiltonian is \(H=24a^2/N\). With the jump defined as exterior minus interior, the endpoint gradient is

\[
\partial_{x_s}I=4a_s^4\big(6[(\log a)']+\tau\big),
\qquad
\partial_{b_s}I=a_s^4\big(-G[b']-\tfrac{20}{3}\tau\big).
\]

Both components vanish precisely at the wall junctions. The computation varies both endpoint data independently and re-solves each bulk shot. It compares centered differences at steps \(3\times10^{-5}\) and \(10^{-5}\), checks Hessian symmetry, and repeats the middle radius at charge ratio 0.75 with both radial integration boundaries moved away from the wall.

| \(q_-/q_+\) | \(a_s/L_+\) | Negative Hessian eigenvalue | Positive Hessian eigenvalue |
|---:|---:|---:|---:|
| 0.75 | 6 | −0.107219 | 319.998556 |
| 0.75 | 10 | −0.039486 | 319.999162 |
| 0.75 | 16 | −0.015546 | 319.999631 |
| 0.90 | 6 | −0.042748 | 320.152107 |
| 0.90 | 10 | −0.015776 | 320.054562 |
| 0.90 | 16 | −0.006216 | 320.021287 |

The eigenvalues refer to the endpoint matrix divided by the background \(a_s^4\). Their signs give the quadratic-form index and their magnitudes depend on the endpoint coordinates. The radius Schur complement (the curvature after extremizing over \(b_s\)) approaches \(-16(1-q_-)/a_s^2\) in this normalization. Under a differentiable near-planar expansion, the coefficient follows from the previous relation \(\alpha=1-1/(2a_s^2)+o(a_s^{-2})\). Differentiating the scalar-relaxed radius stationarity equation along the family gives \(I_{xx}^\star=-I_{x\alpha}^\star\,d\alpha/dx_s\), with \(I_{x\alpha}^\star/a_s^4\to16(1-q_-)\) in the planar limit. The two radius-16 values are within 0.6% of the asymptotic form.

The calculation applies to the reduced five-dimensional ensemble and the indicated detuned parameters. Angular harmonics, internal harmonics, and ten-dimensional corrections to the D3 wall action and flux background require separate calculations. For comparison, Gregory et al. also use the areal coordinate for monotone gravitational bounces in a different boundary-value problem. [Gregory et al.](https://arxiv.org/abs/1808.02305) [Lee and Weinberg](https://arxiv.org/abs/1408.6547) [Jinno and Sato](https://arxiv.org/abs/2010.04462)

Reproduce with `py -3 -B analysis/toe_20261116_D3_radial_negative_mode.py`. The [JSON output](../data/toe_20261116_D3_radial_negative_mode.json) includes both endpoint eigenvalues, the radius curvature, and the cutoff check.
