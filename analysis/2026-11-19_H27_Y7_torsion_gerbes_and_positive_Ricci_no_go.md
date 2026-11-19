# H27 seven-manifold: hidden integral 3-torsion behind b3 = 0

**Date:** 2026-11-19. **Status:** mathematical theorem conditional on the explicitly specified free H27 action; reproducible finite-group and Serre-E2 certificate. Not a TOE or physical compactification.

## Starting point and novelty

The existing `analysis/toe_20261118_H27_S5T2_G2_sextic_center_sequential.py` proves that
`Y7=(S^5 x T^2)/H27` is a compact, smooth, free quotient with real Betti vector
`(1,2,1,0,0,1,2,1)`, and therefore is not torsion-free G2.
**Real cohomology cannot see integral torsion.** We compute the previously
unreported low-degree integral answer:
```
H^3(Y7;Z) = (Z/3)^2,   although H^3(Y7;R) = 0.
H_2(Y7;Z) = Z direct-sum (Z/3)^2.
```

## Proof

Use H27 elements `(a,b,c) in F3^3` and law
`(a,b,c)*(A,B,C)=(a+A,b+B,c+C+a*B)`.
Its center is `Z=<c> = C3`. Let
`rho(a,b,c)=omega^c X^b Z^a` act on `S^5 subset C^3`,
where `ZX=omega XZ`, and let `(a,b)` translate each factor of
`T^2=R^2/Z^2` by `a/3,b/3`. If `(a,b) != (0,0)` the torus
translation has no fixed point. For central nonidentity elements, the
sphere action is the fixed-point-free scalar `omega^c`.
Thus all 26 nonidentity group elements act freely.

The quotient by the full group fibers over the quotient torus:
```
L^5(3) = S^5 / Z(H27)  -->  Y7  -->  T^2 .
```
The monodromy on the lens space is induced by `H27/Z=C3^2`.
Conjugation on the central `C3=pi1(L^5(3))` is trivial, and therefore
monodromy on `H^2(L^5(3);Z)=Z/3` is trivial.

Integral lens-space cohomology in degrees 0 through 5 is
`Z,0,Z/3,0,Z/3,Z`. The Serre spectral sequence for the fibration has
`E_2^{p,q}=H^p(T^2;H^q(L^5(3);Z))`. On total degree three the **only**
nonzero entry is
`E_2^{1,2}=H^1(T^2;Z/3)=(Z/3)^2`.
No differential can hit or leave this term: all possible targets have
base degree >2, while all possible sources have negative base degree.
No additive extension is possible because there is only one term on
the diagonal. Hence `H^3(Y7;Z)=(Z/3)^2`.

The deck group of the universal cover `S^5 x R^2` is
`Gamma={(x,y,c):x,y in Z,c in Z/3}`, with multiplication
`(x,y,c)(x',y',c')=(x+x',y+y',c+c'+xy' mod3)`.
Its commutator subgroup is `Z/3`, so `H_1(Y7;Z)=Z^2`.
Universal coefficients, together with `b_2=1`, give
`H_2(Y7;Z)=Z direct-sum (Z/3)^2`.

## Geometry / physics boundary

There are two independent order-three **flat bundle-gerbe (NS B-field)
topological classes** even though there is no nontrivial real harmonic
three-form. More precisely the flat-gerbe holonomy group is
`H^2(Y7;R/Z) = U(1) x (Z/3)^2` (noncanonically). Torsion classes have
zero de Rham curvature and are **not** a nonzero classical 3-form flux.

Because `pi1(Y7)` surjects onto `Z^2`, it is infinite; by Myers this
same *topological manifold* admits **no metric of positive Ricci
curvature**, regardless of its chosen metric. In particular it cannot
support a nearly parallel G2 metric (which would be positive Einstein),
nor a torsion-free G2 structure (as already excluded by b3 = 0).
This does not exclude every torsionful G2 structure, singular internal
space, or a different compactification.

## Reproduce

```bash
python analysis/toe_20261119_h27_integral_torsion_gerbes.py
python -m unittest tests/test_toe_20261119_h27_integral_torsion_gerbes.py
```

Public background: lens-space integral cohomology (nLab lens-space notes),
nearly-parallel G2 positive Einstein (Kovalev, *On nearly parallel
G2-manifolds*), and Dixmier-Douady classification (Murray, *Bundle gerbes*).
These sources supply general background; the quotient-specific spectral
sequence calculation above is derived here.

## Open physical bridge

Compute a physical (anomaly-consistent) embedding of these torsion gerbe
classes into the E8 compactification. Torsion does not solve the missing
harmonic G2 three-form or Dirac zero-mode obstruction. A different
seven-manifold or singular gauge background is still required.
