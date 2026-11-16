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

## 3. Physics boundary

The winding interpretation survives only as an M-theory/Type IIB duality map; a label count is not an on-shell string spectrum calculation. Local IIB supergravity sees the Betti vector from b3(Y)=1 but omits nonzero fiber string windings. For unequal flux the independent homogeneous instability already excludes stability. For equal flux the lattice count proves instability only when the displayed Fourier modes are present and the two-derivative M-theory analysis is trustworthy. In particular N=1,N0=1 is not a controlled large-flux semiclassical assertion.

Run: `python analysis/toe_20261116_circle_bundle_ring_winding_lattice.py` and `python -m unittest discover -s tests -p test_toe_20261116_circle_bundle_ring_winding_lattice.py -v`.
