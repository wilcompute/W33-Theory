# Independent extension: the integral cup ring and the winding BF staircase

**Status:** Exact topological statements; computational check of a specified classical 11D fluctuation band. **Not** a TOE solution, not a full IIB string stability claim.

Sources: `analysis/2026-11-16_D9_mtheory_uplift.md`, `analysis/2026-11-16_D9_iib_conifold_dual.md` (the latter was an untracked parallel research note at audit time), and Gubser–Mitra (JHEP 2002) for the unequal-charge T^{p,q} BF instability. Earlier project check `toe_20261116_iib_circle_gysin_betti_BF_audit.py` computes additive homology but **not** this ring or lattice census.

## 1. Gcd does not classify the integral cohomology RING

Let `pi:Y(p,q)->S2 x S2` have `c1=p x+q y` with `x^2=y^2=0`, `xy` the positive generator of base H4. Put `g=gcd(|p|,|q|)`, `a=p/g`, `b=q/g`. Gysin gives
- H²(Y)=Z²/<(p,q)> = Z + Z_g and H⁴(Y)=Z/<p,q> = Z_g,
- H³(Y)=Z, with its generator pushing forward to `a x - b y`,
- pi1(Y)=Z_g.

Set `u=pi*(a x+b y)` (the canonical generator of the torsion subgroup of H²) and choose `t=pi*(r x+s y)`, `a s-b r=1` (free generator). If `w=pi*(xy)` generates H⁴(Y), the integral cup products are

`u² = 2 a b w`,  `u t = (a s+b r)w`,  `t²=2 r s w` (coefficients modulo g).

The free class `z in H³(Y)` with `pi_*(z)=a x-b y` obeys `<t z,[Y]>=1` and `<u z,[Y]>=0`. These formulae follow by naturality of the cup product and the projection formula; no speculative physics is used.

**New discriminant.** `Y(3,0)` and `Y(3,3)` both have pi1=Z3 and the same additive integral homology, but the square of their degree-two torsion generator is respectively `0` and `2 w` in H⁴=Z3. Thus their integral cohomology rings differ. In fact `Y(3,0)=L(3,1) x S2`, whereas `Y(3,3)=T^{1,1}/Z3` in the standard circle-bundle presentation. The distinction is invariant under changing the torsion generator by a unit. A classification relying on gcd or Betti numbers alone loses this global datum.

For equal Chern integers `p=q=N`, `u²=2w mod N`; it is nonzero for any N>=3 except when N divides 2. This **does not** imply a field-theory interaction without a separate reduction of the actual gauge potentials and action.

## 2. Count the already-derived BF-violating torus-momentum states

At equal flux, the repo's eleven-dimensional sphere-exchange-odd scalar/Maxwell subsystem has
`m_minus² L²=lambda - 2 - sqrt(4+16 lambda)`.
The BF bound is violated precisely for `0<lambda<12` and the minimum is `-25/4` at `lambda=15/4`.

For torus modulus `tau in H`, integers `(m,n) != (0,0)`, and positive periods `N,N0`:
`lambda(m,n)=3*pi*N0/N * |m+n tau|²/Im(tau)`.

**New modular staircase:** the exact count of unstable Fourier labels in this sector is
`U(N,N0;tau) = #{(m,n) in Z² - {(0,0)} : |m+n tau|²/Im(tau) < 4N/(pi N0)}`.

This is modular invariant under reparametrizing the lattice (the code checks T and S generators); thresholds are discrete lattice shells. Each opposite pair corresponds to two independent real sine/cosine Fourier modes, so counting all signed nonzero integer labels is the count of real Fourier coefficients in this band, not the degeneracy of the complete supergravity spectrum.

At square shape, `U(1,1;i)=4`, `U(1,2;i)=0`, `U(2,1;i)=8`, `U(5,1;i)=20`. In particular `lambda_1=3 pi<12` for `N=N0=1`: **this case IS unstable in the derived sector**. A previous untracked Gysin-audit script's comment called it BF-safe while its own inequality correctly implied the opposite; that comment should not propagate to manuscripts.

A hexagonal lattice maximizes the shortest squared covolume-one momentum vector: `Q_min<=2/sqrt(3)`. Therefore `N/N0>pi/(2 sqrt(3))` forces a violating momentum for **every** torus shape. For smaller positive ratios, elongated shapes still contain BF-violating modes, so there is no uniform stability over the entire modular domain. This supplies an arithmetic multiplicity and modular-wall refinement to the repo's pre-existing lowest-mode criterion.

## 3. Exact Weyl-law scaling at fixed torus shape

For fixed `tau`, the momentum quadratic form `Q=|m+n tau|²/Im(tau)` has determinant 1. Thus the ellipse `Q<R` has Euclidean area `pi R`. At `R=4N/(pi N0)` this equals **`4N/N0`**. This is not an unexplained project constant: it is the ordinary lattice-point Weyl coefficient.

An elementary finite bound avoids appealing to asymptotics alone. The covolume-one lattice has basis `v1=(1/sqrt(y),0)`, `v2=(x/sqrt(y),sqrt(y))`. Its centered fundamental parallelogram fits inside a disk of radius `delta=(1+|tau|)/(2 sqrt(y))`. If `rho=sqrt(4N/(pi N0))`, comparison of covered unit-area cells with the disks of radii `rho +/- delta` proves

`pi max(rho-delta,0)^2 - 1 <= U <= pi(rho+delta)^2 - 1.`

In particular, as `N/N0 -> infinity` at **fixed** `tau`,

`U(N,N0;tau)=4N/N0+O_tau(sqrt(N/N0))`.

This establishes linear growth of the multiplicity of BF-violating Fourier modes in this sector when flux ratios increase, independently of the fixed torus shape at leading order. It is **not uniform** when `tau` is simultaneously taken to the modular cusp. The verifier checks both finite bounds and the counts at multiple integer ratios.

## 4. Controlled large-radius counterfamily — the deeper physical consequence

There is a quantized equal-flux family whose **entire compact geometry becomes parametrically large in eleven-dimensional Planck units, yet the number of BF-violating modes diverges**. Put `N0=t`, `N1=N2=N=t²`, `t` a positive integer, and fix a square torus. The existing uplift's exact equal-flux quantization laws give

`(L/lp)^3=(9 pi/2)t`, `r_sphere=L/sqrt(6)`,
`A_T2/lp²=6 pi² t²/(L/lp)`.

Consequently `L/lp ~ t^(1/3)`, `r_sphere/lp ~ t^(1/3)`, and each torus circumference in Planck units grows as `t^(5/6)` (equivalently a physical circle radius grows as `t^(5/6)`). Thus the source-free classical geometry has controlled large radii as `t->infinity`; local curvature corrections become parametrically suppressed.

At square shape `lambda(m,n)=3 pi (m²+n²)/t`. The previously derived BF inequality yields the instability count `U=4t+O(sqrt(t))`. Crucially, a *uniformly deep* sub-band obeys

`m_minus² L² <= -6 iff 2<=lambda<=6`.

Its Fourier labels occupy the planar annulus `(2t)/(3 pi) <= m²+n² <= (2t)/pi`, of area exactly `(4/3)t`. Ordinary lattice-point bounds prove that the number of modes at least **two units below** the AdS5 BF bound is

`D(t)=(4/3)t+O(sqrt(t))`.

This is a robust, quantitative negative result for the particular equal-flux eleven-dimensional solution family: there are arbitrarily many linearized instabilities with an order-one BF violation **in a simultaneously large-radius eleven-dimensional regime**. It does not rely on dubious small-flux examples, and it does not constitute a no-go theorem for every M-theory compactification. The Type IIB fiber is correspondingly small, so neglecting wrapped-string sectors in the IIB low-energy truncation is unjustified for this scaling.

## 5. Physics boundary

The winding interpretation survives only as an M-theory/Type IIB duality map; a label count is not an on-shell string spectrum calculation. Local IIB supergravity sees the Betti vector from b3(Y)=1 but omits nonzero fiber string windings. For unequal flux the independent homogeneous instability already excludes stability. For equal flux the lattice count proves instability only when the displayed Fourier modes are present and the two-derivative M-theory analysis is trustworthy. In particular N=1,N0=1 is not a controlled large-flux semiclassical assertion.

Run: `python analysis/toe_20261116_circle_bundle_ring_winding_lattice.py` and `python -m unittest discover -s tests -p test_toe_20261116_circle_bundle_ring_winding_lattice.py -v`.
