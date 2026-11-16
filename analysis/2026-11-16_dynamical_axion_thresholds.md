# Dynamical axion excursions, cosmological redshift, and radiation freezing

The [continued-fraction mass law](2026-11-16_irrational_axion_towers.md) describes a path in the fixed-shape torus moduli. Here the volume and six-form axion are coupled to the five-dimensional Einstein equations. The expanding vacuum solution traverses that path, and the light-tower threshold competes with a different time dependence for redshifting radiation. A homogeneous radiation density changes the late-time conclusion.

## Einstein equations on the volume–axion slice

Let \(T>0\) be proper time from the kinetic singularity of the expanding solution, \(a(T)\) the external scale factor, and \(\mathcal H=\dot a/a\) the Hubble parameter. Set \(z=x+iy\) with \(y=V\) the torus volume. In the action convention \(M_5^3[R-G_{AB}\partial\phi^A\partial\phi^B]/2\), the scalar metric is
\[
  G_{AB}d\phi^A d\phi^B=\frac{dx^2+dy^2}{2y^2}.
\]
Reduction with external metric factor \(V^{-2/3}\) and internal metric factor \(V^{1/3}\) gives the log-volume coefficient \(1/3+1/6=1/2\). The spacetime four-form kinetic term carries \(V^2\), and dualization yields the axion term proportional to \(V^{-2}\). Its normalization in the complex coordinate is the one in the [integral momentum–M5 block](2026-11-16_torus_axion_r4.md). An isotropic scale on a fixed flat shape and a spacetime four-form give a classical truncation with no anisotropic internal source. The four-form is supported in five dimensions, so its wedge with itself vanishes in the eleven-dimensional Chern–Simons equation. This is the ungauged, two-derivative theory with no scalar potential. [Toroidal exceptional-field-theory reduction](https://arxiv.org/abs/1312.0614) · [Kination and higher-dimensional evolution](https://arxiv.org/abs/2212.10293)

With only scalar kinetic energy on a spatially flat external slice,
\[
   D_T\dot\phi+4\mathcal H\dot\phi=0,\qquad
   6\mathcal H^2=\tfrac12|\dot\phi|_G^2 .
\]
The nontrivial expanding solution has \(a\propto T^{1/4}\), \(d\ell/d\log T=\sqrt3/2\) for canonically normalized scalar distance \(\ell\), and unit-curvature modular arc length \(v\,d\log T\) with \(v=\sqrt{3/2}\). Thus every homogeneous background in this class follows a modular geodesic. The vertical solution has \(x\) constant and \(y=y_0(T/T_0)^{-v}\). General axion momentum gives a semicircle with limiting endpoint \(x_\infty\). Writing it as \(x=x_c+R\tanh\lambda,\ y=R\,\operatorname{sech}\lambda\) gives \(x_\infty-x=O(y^2)\) and \(y\propto T^{-v}(1+O(T^{-2v}))\). The squared mass of every fixed charge in the doublet has a one-Lipschitz logarithm in the unit hyperbolic metric, since it is the inverse transformed height times a charge-dependent constant. Thus the semicircle and the vertical ray at the same small \(y\) give squared masses within a uniform factor \(1+O(y)\). The endpoint controls the strict asymptotic threshold classes even with nonzero axion momentum. [Series, modular geodesics and continued fractions](https://doi.org/10.1017/S0143385700009585)

## The Hubble scale and the redshifting probe give different tests

Write \(h(z)\) for reduced modular height and \(m_*^2/h(z)\) for the lightest doublet mass squared at the chosen fixed shape. The log of \(h\) is also one-Lipschitz. This gives the bounds
\[
 m_{\min}\ \gtrsim\ T^{-v/2},\qquad
 \frac{m_{\min}}{\mathcal H}\ \gtrsim\ T^{1-v/2}\ \longrightarrow\ \infty .
\]
The bounds hold even at irrational endpoints with unbounded cusp excursions and for a rational runaway. For each mode of fixed charge, \(|\dot m|/m^2\le v/(2Tm)\); the bound goes uniformly to zero. For a free minimally coupled probe, the physical momentum redshifts as \(T^{-1/4}\). The canonical oscillator of a scalar in four external spatial dimensions has squared frequency \(m^2+(k/a)^2+1/(4T^2)\). Its real-time first WKB parameter is bounded by \(1/(T m)\), since the logarithmic derivatives of the three positive terms have magnitudes at most \(2/T\). This is a local adiabatic estimate for the free modes. Cumulative interacting production and stress-energy backreaction require a separate computation. [Tower and Hubble scales in asymptotic cosmology](https://arxiv.org/abs/2208.08989)

Now send two counterpropagating massless test modes of equal comoving momentum. Each has energy \(P(T)=P_0(T/T_0)^{-1/4}\) and pair-production kinematics opens when \(P(T)>m_{\min}(T)\). On the vertical ray \(P^2=K y^r\) with \(r=1/(2v)=1/\sqrt6\). For irrational \(x\) and a primitive fraction \(p/q\), let \(\epsilon=|x-p/q|\). The exact moving-target ratio for this charge is
\[
 \frac{P^2}{m_{p,q}^2}
 =\frac{K}{m_*^2q^2}\frac{y^{1+r}}{y^2+\epsilon^2}.
\]
It reaches its maximum at \(y=\epsilon\sqrt{(1+r)/(1-r)}\), displaced from the static mass minimum. The peak ratio is \(C_r (K/m_*^2) q^{-2}\epsilon^{-(1-r)}\), where \(C_r=\tfrac12(1+r)^{(1+r)/2}(1-r)^{(1-r)/2}\). Infinitely many late open windows occur exactly when infinitely many reduced fractions satisfy
\[
   \epsilon < \left(C_r K/m_*^2\right)^{1/(1-r)}
                  q^{-2/(1-r)} .
\]
Finite early peaks and fixed bounded denominators play no role in this criterion. At late times every qualifying fraction is a continued-fraction convergent. The exact critical irrationality exponent is
\[
    \mu_{\rm crit}=\frac{2}{1-1/\sqrt6}.
\]
Below it the threshold is eventually closed, including almost every endpoint. Above it the windows reopen arbitrarily late. At equality the exponent must be supplemented by approximation constants. For example define continued fractions recursively with next digit asymptotic to \(q^{\mu_{\rm crit}-2}(\log q)^2\) or \(q^{\mu_{\rm crit}-2}(\log q)^{-2}\). Both have the critical exponent, while their peak ratios diverge or vanish, respectively, for any fixed nonzero \(K/m_*^2\). The truncated recurrence in the verifier uses high-precision bounds on these ratios.

The geodesic still leaves each excursion for an irrational endpoint. At an arbitrarily late opening edge the height scales as \(T^{1/2}\), so the probe energy divided by the six-dimensional KK species estimate scales there as \(T^{-1/12}\). This places the opening edge below that scale even in cases where the deepest part of a cusp would put the same probe above it. The pair-opening test refers to local scattering in an adiabatically evolving background. It does not count actual particle events in the vacuum. [Toroidal gap and species scale](2026-11-16_irrational_axion_towers.md)

## Proper-time occupancy has a sharp golden-ratio boundary

For almost every endpoint the modular cusp fraction in \(\log T\) is \(3/(\pi L)\) for heights above \(L\ge1\). The fraction of elapsed proper time has a different behavior. If \(b\) is a unit tangent vector and \(g^u\) is modular geodesic flow, define
\[
 F_L(b)=\int_0^\infty e^{-u}\,
       \mathbf 1_{\{h(g^{-vu}b)>L\}}\,du .
\]
The proper-time fraction up to \(T\) differs from \(F_L\) at the current tangent by \(O(T_0/T)\). This follows by substituting \(T'=Te^{-u}\) in the time average. The function \(F_L\) is continuous because a geodesic spends zero time on the level horocycles \(h=L\), and the exponential weight bounds the omitted past. Its mean in the invariant geodesic-flow measure is \(3/(\pi L)\), by invariance and Fubini. Its supremum is one since \(h(g^{-vu}b)\ge h(b)e^{-vu}\).

The least possible maximum height of a complete modular geodesic is \(H_*=\sqrt5/2\). The lower bound follows from Hurwitz approximation along any irrational backward endpoint, by comparison to its asymptotic vertical ray. A rational backward endpoint escapes upward. For the golden geodesic, the endpoints \(\varphi,\varphi'\) have difference \(\sqrt5\). A modular transform with bottom row \((c,d)\) gives the transformed semicircle radius \(\sqrt5/(2|d^2+cd-c^2|)\le H_*\). Thus \(F_L=0\) along this periodic geodesic when \(L\ge H_*\). For \(1\le L<H_*\), every past geodesic visits \(h>L\) somewhere, so \(F_L>0\) at every tangent. The reduced thick part of the unit tangent bundle is compact, and the large-height lower bound for \(F_L\) tends uniformly to one. Therefore its infimum is strictly positive for \(L<H_*\).

Almost every geodesic samples every open set of positive invariant measure infinitely often. Vertical rays with generic endpoints inherit the extrema by stable-leaf convergence, as do other rays with the same forward endpoint. The proper-time fraction has limsup one and liminf zero for \(L\ge H_*\). For \(1\le L<H_*\) its liminf is strictly between zero and one. In either case the fraction fails to converge. The logarithmic-time average of the weighted observable still converges to \(3/(\pi L)\). [Series, modular geodesic coding](https://doi.org/10.1017/S0143385700009585) · [Matheus and Moreira, modular height spectra](https://doi.org/10.4171/cmh/498)

## A homogeneous radiation component ends the infinite excursion sequence

Take a positive, separately conserved radiation fluid with pressure \(p_r=\rho_r/4\) and no direct scalar force. Then \(\rho_r\propto a^{-5}\) and \(\rho_{\rm kin}\propto a^{-8}\). The scalar still follows the same geodesic track, but the Friedmann equation changes the relation between expansion and field distance:
\[
 \frac{d\ell}{d\log a}
   =\frac{\sqrt{12}}{\sqrt{1+u_0(a/a_0)^3}},
 \qquad u_0=\frac{\rho_r(a_0)}{\rho_{\rm kin}(a_0)} .
\]
The entire remaining scalar distance is exactly
\[
    \ell_\infty-\ell(a_0)
    =\frac4{\sqrt3}\operatorname{arsinh}\!\left(u_0^{-1/2}\right).
\]
It is finite for every \(u_0>0\). The geodesic stops at a finite point of the cover, where the gap is positive. Later \(a\propto T^{2/5}\) and an equal-comoving-momentum test probe eventually stays below that gap. The ideal vacuum limit is singular in the remaining distance. This result models separately conserved homogeneous radiation, such as a stipulated neutral radiation bath. The stress tensor of dynamically produced massive towers, scalar potentials, and other moduli directions are outside this truncation. The repo's [dark-sector drag calculation](PASS12550_12557_DARK_MATTER_DRAG.md) treats a distinct case with a direct modulus force from massive matter.

## The full \(E_{6(6)}\) geodesic has a sharp Hubble bound

The stronger bound on the doublet uses the fixed shape. A weaker but sharp statement holds for the full scalar manifold \(E_{6(6)}/USp(8)\) under the same vacuum, kinetic, homogeneous assumptions. Rotate the tangent geodesic by the local compact group to the split Cartan. In log-circle radii \(t_i\), \(i=1,\ldots,6\), the physical scalar metric on this Cartan is \(G=I+\mathbf 1\mathbf 1^{\mathsf T}/3\), and the charge-decay weights in the signed torus frame are
\[
 e_i+\tfrac13\mathbf 1,\qquad -e_i-e_j+\tfrac13\mathbf 1,\qquad
 e_i-\tfrac23\mathbf 1 .
\]
They represent the six momenta, fifteen M2 charges and six complementary M5 charges. This is the physical Cartan realization of the 27 minuscule weights already identified in the [repo's finite geometry](../docs/index.html). The dual metric \(G^{-1}=I-\mathbf 1\mathbf 1^{\mathsf T}/9\) gives every weight squared length \(4/3\). The proper scalar speed per \(\log T\) is still \(\sqrt3/2\), since the homogeneous Einstein equations only see the norm of the tangent. Cauchy–Schwarz bounds each contraction exponent by one. [Signed toroidal charge basis](2026-11-15_quiver_torus_charge_dictionary.md) · [Kinetic matrix from the cubic](2026-11-15_torus_kinetic_reconstruction.md) · [Central charges in extended supergravity](https://arxiv.org/abs/hep-th/9608015)

An arbitrary initial coset point and compact rotation send the charge lattice to a fixed full-rank real lattice in the Cartan weight frame. Along the geodesic each dressed charge component scales as \(T^{-\alpha_j}\) with \(\alpha_j\le1\). Thus \(T\) times the norm of every nonzero dressed charge is bounded below uniformly by a positive lattice constant. The local BPS lower mass bound uses the greatest central-charge skew eigenvalue, a norm comparable to the Euclidean norm of the dressed 27. Consequently the local mass scale of electric states carrying these charges cannot fall parametrically below \(\mathcal H\propto T^{-1}\). This covers the charged sector of the ungauged toroidal theory. It does not establish a gap for neutral states.

Equality in the Cauchy–Schwarz bound can select at most one weight line, since the weights are distinct and have equal length. If the rotated charge lattice has no nonzero vector on that line, \(T\) times the lightest dressed charge norm still tends to infinity. Indeed a bounded subsequence would have to use a finite set of vectors, because the diagonal map \(T\operatorname{diag}(T^{-\alpha_j})\) has singular values at least one for \(T\ge1\). A vector appearing arbitrarily late would have to vanish on all weights with \(\alpha_j<1\). Directions with \(\max_j\alpha_j<1\) give a power-law separation directly. This is a lattice criterion for the dressed norm. A marginal lattice vector's realization as an actual BPS particle is a separate spectral question.

One realized marginal example grows one circle, \(t_1=(3/4)\log T\) and the other \(t_i\) fixed. A pure momentum charge along circle one has exactly \(m\propto T^{-1}\). The 27 exponents in that direction are \(1\), \(1/4\), and \(-1/2\), with multiplicities \(1,16,10\), respectively. In eleven-dimensional proper time \(Y\propto T^{3/4}\) the noncompact spatial dimensions have constant scale, the growing circle has radius proportional to \(Y\), and the other circles are constant. The lift is locally flat Milne space with an identified boost coordinate. The mass-to-Hubble ratio of that mode stays at an initial-data-dependent constant in the five-dimensional frame. [Kination and Kasner uplift](https://arxiv.org/abs/2212.10293)

The [verifier](toe_20261116_dynamical_axion_thresholds.py) checks the Friedmann normalization, the displaced mass-ratio maximum, four continued-fraction regimes, nonvertical endpoint alignment, and the radiation distance integral against independent numerical quadrature. It also checks the norms and saturation exponents of all 27 weights with rational arithmetic. See the [generated certificate](../data/toe_20261116_dynamical_axion_thresholds.json).
