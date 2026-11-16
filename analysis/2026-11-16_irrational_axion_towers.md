# Irrational axions, recurrent light towers, and the five-dimensional cutoff

On the [toroidal six-form and volume slice](2026-11-16_torus_axion_r4.md), the protected \(R^4\) and \(\partial^4R^4\) coefficients grow with the modular height. The momentum–M5 charge lattice determines that height exactly. At a rational axion the same charge direction becomes permanently light as the volume goes to zero. Irrational axions give a different limit: arbitrarily late returns to finite height, with light-tower excursions governed by continued fractions. The calculation below keeps the determinant-one torus shape fixed. [Ruiz and Varona, toroidal dual frames](https://arxiv.org/abs/2611.00235)

## Exact charge gaps and excursion intervals

Write \(z=x+iy\). Normalize the lattice gap of a single momentum–M5 doublet by

$$m(z)^2=\min_{(p,q)\in\mathbb Z^2\setminus\{0\}}\frac{|qz-p|^2}{y},
\qquad H(z)=m(z)^{-2}.$$

A shortest pair is primitive. The same \(H\) is the greatest imaginary part of \(z\) under integral modular transformations, since their bottom rows are precisely the primitive pairs. A finite fixed shape changes component masses by fixed factors. The two-dimensional doublet lattice has area one in this norm. If two primitive charge lines were distinct and both had norm smaller than one, the area of their parallelogram would be smaller than one. Its area is a nonzero integer. Thus whenever \(H>1\), exactly one primitive doublet up to sign gives the excursion. The six copies of this doublet supply the wrapped dual of the six-dimensional momentum lattice.

For \(q>0\), put \(\epsilon=|x-p/q|\). If \(x\) is irrational, the height from this charge takes its maximum at \(y=\epsilon\),

$$m_{p,q}(y)^2=2q^2\epsilon\,\cosh\!\left(\log\frac y\epsilon\right),\qquad
H_{\rm peak}(p,q)=\frac1{2q^2\epsilon}.$$

For a threshold \(L\geq1\), the interval where this charge has height greater than \(L\) is

$$\left|\log(y/\epsilon)\right|<\operatorname{arcosh}(H_{\rm peak}/L)$$

if \(H_{\rm peak}>L\). The intervals for different primitive charges are disjoint. A peak higher than one requires \(\epsilon<1/(2q^2)\), so Legendre's criterion forces \(p/q\) to be a continued-fraction convergent. Conversely each convergent satisfying this inequality gives its own exact excursion interval. These are direct mass formulas for the modular cusp coding. [Series, geodesics on the modular surface and continued fractions](https://doi.org/10.1017/S0143385700009585)

Each interval for an irrational \(x\) is bounded away from \(y=0\). Hence \(H\leq1\) occurs at arbitrarily small \(y\): otherwise an entire connected tail would lie inside one of the disjoint intervals. Along those returns the ray lies in the compact part of the modular slice, and the quantized 27-charge norm has a uniform positive lower bound for any nonzero lattice vector. This includes irrational numbers with arbitrarily deep excursions. The path has infinite accumulated length in the covering hyperbolic metric. Its distance from a fixed reference point in the quotient stays bounded along the returns, so the path does not escape to infinite moduli distance.

## Sharp depth laws

For irrational \(x\), the convergent bounds put \(q|qx-p|\) between \(1/(a_{\rm next}+2)\) and \(1/a_{\rm next}\), where \(a_{\rm next}\) is the next continued-fraction digit. Consequently the doublet mass is bounded away from zero exactly when the digits are bounded. More precisely,

$$\liminf_{y\to0}m(x+iy)^2=2\liminf_{q\to\infty}q\,\|qx\|.$$

The lower bound uses \(m_{p,q}^2\geq2q|qx-p|\) and the fact that a bounded denominator cannot minimize the mass as \(y\to0\) for irrational \(x\). The upper bound uses the peak volumes. For the golden-ratio conjugate the right side is \(2/\sqrt5\), by the Fibonacci convergents and Legendre's criterion.

Define \(\mu(x)\) as the supremum of the exponents \(\mu\) for which \(|x-p/q|<q^{-\mu}\) infinitely often. With \(t=-\log y\), the exact depth exponent is

$$\limsup_{t\to\infty}\frac{\log H(x+i e^{-t})}{t}=1-\frac2{\mu(x)}.$$

To obtain the upper bound, write \(Q=\log q\) and \(E=-\log\epsilon\). Away from the thick part, a winning charge has \(E>2Q\). Its log height is at most \(\min(t-2Q,2E-t-2Q)\). Dividing by \(t\) maximizes this bound at \(t=E\), giving \(1-2Q/E\). The definition of \(\mu\) bounds \(E/Q\) for large denominators. Approximants attaining the limsup and their exact peak volumes give the matching lower bound. In the case \(\mu=2\), the modular fundamental domain also supplies a fixed positive lower bound on \(H\).

The examples in the verifier give explicit controls. Taking each next digit to be the square of the current denominator gives \(\mu=4\), by the convergent error bounds and Legendre's criterion. The deepest excursions then have \(\log H/t\) tending to \(1/2\). Taking increasing powers of the denominator gives a Liouville limit with depth exponent one. Both constructions still return to finite height infinitely often.

For Lebesgue-almost every \(x\) the exponential depth exponent is zero and the sharper law is

$$\limsup_{t\to\infty}\frac{\log H(x+i e^{-t})}{\log t}=1.$$

Apply Khintchine's theorem to \(\epsilon<q^{-2}(\log q)^{-\gamma}\). Its approximation sum converges for \(\gamma>1\) and diverges for \(\gamma\leq1\). The convergent peaks give the lower bound. For an arbitrary deep excursion the peak bound applies and \(H>1\) implies \(\log q<t/2\), giving the upper bound. At the winning peaks the two logarithmic clocks agree up to their finite factors. [Beresnevich and Velani, the metric approximation criterion](https://www.impan.pl/shop/en/publication/transaction/download/product/82487)

## How often the tower becomes light

For almost every fixed axion, the fraction of hyperbolic path time spent above any height \(L\geq1\) tends to

$$\frac{3}{\pi L}.$$

The reduced fundamental domain has area \(\pi/3\), and the cusp above \(L\) has area \(1/L\). For the vertical ray with specified forward endpoint \(x\), geodesic-flow ergodicity and Fubini in endpoint coordinates give the same time averages as a generic geodesic with that forward endpoint. After a constant shift of the time parameter, rays with that common endpoint converge in hyperbolic distance. Approximation by continuous observables applies the result to the cusp indicator, whose boundary has measure zero. Thus in the unit doublet normalization the time fraction with \(m<\eta\), for \(0<\eta\leq1\), tends to \(3\eta^2/\pi\). [Series, geodesic flow and its continued-fraction coding](https://doi.org/10.1017/S0143385700009585)

## Three scales in the deep excursions

At large \(H\), the dual upper-half-plane point has volume \(H\) and bounded axion. The six-dimensional light KK lattice has counting law \(N(\Lambda)\asymp(\Lambda/m)^6\). The five-dimensional species estimate \(\Lambda_{\rm sp}^3 N(\Lambda_{\rm sp})\asymp M_5^3\) gives \(\Lambda_{\rm sp}/M_5\asymp H^{-1/3}\), the higher-dimensional Planck scale in five-dimensional units. The omitted KK threshold of the action with only massless fields is at \(m/M_5\asymp H^{-1/2}\). [Species scale in decompactification](https://doi.org/10.1007/JHEP06%282024%29037)

From the protected four-graviton coefficients, the suppression scales defined by comparing each operator to the Einstein term behave as

$$\Lambda_{R^4}/M_5\asymp H^{-1/3},\qquad
\Lambda_{\partial^4R^4}/M_5\asymp H^{-7/20}.$$

The \(R^4\) scale has the same exponent as the species estimate. The \(\partial^4R^4\) scale is smaller by a relative factor of order \(H^{-1/60}\). These are coefficient-defined scales. The zero-mode derivative expansion reaches the first KK threshold before either of them in a deep excursion. For almost every axion the deep-height time law also gives tails proportional to \(K^{-1/2}\) and \(K^{-2/7}\) for the time fractions with \(R^4\) and \(\partial^4R^4\) coefficients above \(K\). Their leading constants follow from the corresponding published large-volume coefficients. [Green, Miller, Russo and Vanhove, M-theory constant terms](https://arxiv.org/abs/1004.0163)

## The Kaluza–Klein box explains the threshold hierarchy

The five-dimensional one-loop scalar box for an internal mode of mass \(m_\ell>0\), after removing its common tensor and normalization, has parameter integrand \([m_\ell^2-sx_1x_3-tx_2x_4]^{-3/2}\) over the unit three-simplex. The order-\(k\) coefficient is proportional to \(m_\ell^{-3-2k}\) times the corresponding simplex moment. In the crossed sum the linear term cancels by \(s+t+u=0\). The quadratic term is nonzero and sums to the convergent six-dimensional Epstein series \(\sum_{\ell\neq0}m_\ell^{-7}\). This reproduces the \(H^{7/2}\) leading scaling and shape dependence of \(\partial^4R^4\). The zeroth-order sum has a different ultraviolet behavior and requires the eleven-dimensional matching used for \(R^4\). [Green, Gutperle and Vanhove, the Kaluza–Klein four-graviton loop](https://arxiv.org/abs/hep-th/9706175) · [Green, Russo and Vanhove, Appendix G](https://arxiv.org/abs/1001.2535)

At fixed moduli, on \(t=u=-s/2\), the massive KK contribution to the one-loop analytic germ has **exact radius \(4m_{\min}^2\) in \(s\)**, where \(m_{\min}\) is the lightest nonzero KK mass in the reduced frame. For boxes containing \(s\), the absolute maximum of the coefficient of \(s\) in the simplex denominator is \(1/4\), attained when two opposite parameters equal \(1/2\). The third box has a smaller maximum. The even moments are positive. Their \(k\)-th roots approach \(1/4\), since neighborhoods below the maximum have positive measure, and the binomial factor has unit \(k\)-th root in the limit. The lightest mode then bounds the coefficient growth from below. For the upper bound, factor out the same radius and dominate the remaining sum by \(\sum_{\ell\ne0}m_\ell^{-7}\) for \(k\ge2\). This proves the radius by Cauchy–Hadamard. The verifier checks exact low-order simplex moments by their factorial formula. This calculation concerns the massive one-loop analytic part, with the massless threshold separated and finite local subtractions allowed.

The [certificate](../data/toe_20261116_irrational_axion_towers.json) checks the doublet determinant, peak formulas, and scale exponents, and gives exact interval-based witnesses for bounded, unbounded, and feedback-generated continued-fraction digits. The arithmetic and scale laws apply to the fixed-shape toroidal slice. A dynamical solution selecting such a trajectory and a microscopic identification with the del Pezzo probe remain open.

    python -B analysis/toe_20261116_irrational_axion_towers.py
