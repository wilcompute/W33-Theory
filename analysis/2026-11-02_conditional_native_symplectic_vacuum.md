# A conditional classical vacuum selects the native symplectic form

The nine-front packet constructs an actual Clifford action on the signed native
27-coordinate cubic. A further probe asks whether the same cubic admits a
configuration selecting its older symplectic subgroup. **It does, under supplied
field-theory assumptions.** This is a classical model, not a physical TOE.

Assume four-dimensional globally supersymmetric N=1 SU(4) gauge theory,
canonical Kahler potential and superpotential

```
W = Pf6(A) + u^T A v,
A in Lambda^2(C6), u,v in dual(C6).
```

Only the SU(4) acting on the first four coordinates is gauged. Supersymmetry,
the spacetime dimension, gauging and kinetic terms are choices. The cubic and
its coordinate map come from `w33_20261102_clifford_native_cubic_repair.py`,
which credits the earlier Pfaffian/E6 bridge and standard SL6 representation.
F/D-flatness criteria are standard; see [Martin's Supersymmetry Primer](https://arxiv.org/abs/hep-ph/9709356).
The SU(4)/Sp(4) coset is established physics, including
[lattice composite-Higgs investigations](https://arxiv.org/abs/2202.05516).
No novelty is claimed for the coset or supersymmetric Higgs mechanism.

Let Omega be the existing skew form with Omega02=Omega13=1. Set the first
four-by-four block of A to t*Omega, u4=t, v5=t, and all other entries to zero,
where t is arbitrary complex. In the actual signed native coordinates this is
simply **z12=z14=z15=z17=t**, with every other coordinate zero.

All 27 holomorphic F-terms vanish, checked independently in both cubic coordinate
systems. The SU(4) D-moment is zero because Omega*Omega-dagger=I4 and the two
other nonzero fields are SU(4) singlets. A pure Omega condensate would fail:
F_A45=Pf4(Omega)=-1 at t=1. The existing singlet product u4*v5=1 cancels this
term. No extra superpotential term is introduced. The complete matter content
is 6+2*4+2*bar4+5*1, with cancelling perturbative cubic gauge anomaly.

For t nonzero the continuous gauge stabilizer is USp(4), defined by
U*Omega*U-transpose=Omega. At t=1 the canonical SU(4) gauge-variation Gram matrix
has ten zero and five unit eigenvalues, using Tr(TaTb)=delta_ab/2. The
holomorphic superpotential Hessian has rank ten, with spectrum 0^17,2^5,(-2)^5.
Every gauge-orbit tangent is in its kernel, checked directly. Removing the five
complex Goldstone directions leaves twelve quadratic zero directions. This
does **not** establish twelve nonlinear moduli or a quantum-stable vacuum.

The finite stabilizer can also be computed from the actual six-form action.
The 23,040-element rotational signed B6 group has an orbit of twelve oriented
coordinate axes. The subgroup fixing i*Omega therefore has order 1,920; its
spinor lift has order **3,840**, containing the previous linear subgroup of
order 1,920 with index two. Its projective image has order 1,920. The six-form
stabilizer is rotational B5+, abstractly isomorphic to W(D5): in odd dimension
five the map Q -> det(Q)*Q restricts to an isomorphism from even-sign W(D5)
onto rotational B5+. This differs from the even-dimensional B6+/W(D6)
distinction proved in the nine-front packet.

Parallel Pass12525 identifies W(D5) as the q=5 hyperoval stabilizer. The matching
abstract group is a useful connection to investigate, **not an explicit map to
that finite-field geometry**. No such intertwiner is asserted here.

The homogeneous cubic leaves the scale t unselected. The potential, supplied as
a sum of F/D squares, has this classical zero-energy family, including t=0.
Quantum corrections, residual strongly coupled gauge dynamics, full E6
D-flatness, isolation of a vacuum, Standard Model chirality and gravity remain
unresolved. This configuration is a concrete starting point for those tests.

Reproduce with `py -3 analysis/w33_20261102_conditional_symplectic_vacuum.py`.
Its JSON exports both VEV coordinate systems, exact Hessian and gauge-Gram
data, group orders, input hashes and the assumptions. Producer assertions test
the native gradient, the failed pure-condensate alternative, all Ward tangents,
the literal finite stabilizer and the odd-dimensional group isomorphism.

Five independent investigations: quantum stability of this family; an explicit
q=5 stabilizer intertwiner; all-quartet quantum tunneling; minimal common-cover
compression; experimentally calibrated information-geometry tests.
