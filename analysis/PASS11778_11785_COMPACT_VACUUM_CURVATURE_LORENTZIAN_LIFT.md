# Passes11778–11785: an attained quantum vacuum, nonlinear curvature and a Lorentzian lift

The actual11769 current-square Hamiltonian has **compact resolvent**. Its positive lowest eigenvalue is therefore attained with finite multiplicity, and a positive gap separates that entire ground-state sector from the next distinct level. This resolves the mathematical attainment/gap question left open in11770–11777, without assigning a numerical gap, physical energy unit or ground-state multiplicity.

A second result changes the geometric interpretation. The centered common quadratic cone of11771 does not extend automatically to displaced backgrounds. Exact Gaussian Wick dynamics instead gives a positive kinetic metric with a **nonzero magnetic two-form**, certified by a rational W33 matrix element. Applying the established Eisenhart–Duval construction gives an explicit80-dimensional Lorentzian null-geodesic representation of that variational dynamics. Neither the dimension nor the lift is identified with physical spacetime or Einstein gravity.

Reservation:94fd9d49d, following science8a7f41f51023285e531de73c8d513ff430e53ea8 and receiptfd7a162cd. All work is in the original Theory of Everything checkout.

## Inputs, ownership and the five requested investigations

The160 actual point–line Levi edges, the78-dimensional carrier
`W=(1,s)^perp`, and the real Lie closure `sl78 semidirect h157` of dimension6240 belong to11767. The self-adjoint current flows, positive form, Gaussian covariance and proposed Hamiltonian belong to11769–11770. The improved trial estimate127.619509... belongs to11775. The centered matched cone, Clifford-current operator, typeI modular obstruction and full-conversion collapse belong to11771–11777. We use those owners rather than reconstructing their results as new claims.

The paper's actual open physics questions were rechecked in `papers/forty_points/sec11_epilogue.tex`; the current physics cards in `docs/index.html` and prior certificates were read. Searches for the **results** included compact resolvent, attained vacuum, Weyl averaging, the rational curvature `31/10`, trace coefficient `2106`, Bott index, current-net interval construction and Eisenhart/Bargmann lifting. The known mathematical tools below are credited to primary literature; their application to the actual current Hamiltonian is the subject of this packet. This is not a claim of a new general compactness theorem or a new general Lorentzian lift.

| Requested direction | Executed investigation | Exact boundary |
|---|---|---|
| Vacuum and quantitative lower bound |11778 compactness/attainment/gap; Weyl-pair lower bound;11783 finite Gibbs trace|The lower bound is expressed in finite control distances, not a computed decimal.|
| Observable net with geometric modular translations |11779 explicit interval current net on78 internal components|A supplied standard chiral net; no limit map from the current Hamiltonian.|
| Current Clifford zero modes and chiral index |11780 Gaussian-product obstruction and expected curvature; untruncated Bott index control|Actual current-Dirac Fredholmness/index remains open. Bott is a different operator.|
| Stability of the common cone under interactions |11781 exact displaced Wick kinetic metric;11784 nonzero magnetic curvature|Already obstructed off center in variational dynamics; no one-loop self-energy was computed.|
| Constraints retaining matter |11782 explicit isotropic Abelian reduction;11785 parametrized clock and null lift|Matter survives, but the choices are supplied and are not the gravitational constraint algebra.|

##11778: compactness from actual current control

Write, with `a=1/sqrt20`,

```
J_e=(V_e.q+a)(U_e.p+a),  U_e.V_e=0,
h[psi]=sum_e ||J_e psi||^2,
H=the Friedrichs operator of h on L2(W).
```

The prior unitary current flows integrate the current Lie algebra. Let `G` be their connected represented finite-dimensional Lie group and `d` its horizontal control distance for the160 original generators. Its Lie algebra contains all78 translations,78 modulations and their central phase, by11767. Bracket generation implies finite control distance on the connected group and that `d` induces its manifold topology.

For a finite product of horizontal one-parameter flows, telescope the difference from the identity. Every summand has a unitary prefix multiplying a difference acting on the **original** vector. The one-generator spectral inequality and Cauchy–Schwarz give the11770 estimate

```
||(pi(g)-I)psi|| <= d(1,g) sqrt(h[psi]).                 (1)
```

For simultaneous horizontal controls, `||sum c_e J_e psi|| <= |c| sqrt(h[psi])`; products approximate controlled paths. The estimate extends from the common Schwartz core to the closed form domain. It does not assume that the individual flows preserve `h`.

Fix a bounded form ball `B={psi: ||psi||^2+h[psi]<=R}`. Equation(1), restricted to its Heisenberg subgroup, proves uniform continuity of `B` under both ordinary translations `exp(-it.p)` and modulations `exp(ix.q)` as their parameters tend to zero.

For epsilon>0 introduce

```
K_epsilon=exp(-epsilon |q|^2) exp(-epsilon |p|^2).
```

Both factors are normalized Gaussian averages of their respective Weyl flows, with parameter distributions concentrating at zero as epsilon tends to zero. Split each average into a small parameter ball, where(1) is uniformly small on `B`, and its complement, bounded by `2 sqrt(R)` times a Gaussian tail. Hence

```
sup_(psi in B) ||(K_epsilon-I)psi|| -> 0.               (2)
```

The integral kernel in orthonormal coordinates on `W=R78` is

```
e^(-epsilon |q|^2) (4pi epsilon)^(-39)
  exp(-|q-y|^2/(4epsilon)).
```

Its squared Hilbert–Schmidt norm is `(4epsilon)^(-78)<infinity`, independently checked from the one-dimensional Gaussian integrals. Thus every `K_epsilon` is compact. Uniform compact approximation(2) makes `B` totally bounded: its image under a fixed `K_epsilon` has a finite net and(2) transfers that net to `B`. The closed form embedding into `L2(W)` is compact, and therefore `(H+1)^(-1)` is compact.

The space is infinite dimensional, so the eigenvalues have finite multiplicity and tend to infinity. The prior positive floor excludes zero. Consequently `E0>0` is attained and `E_next-E0>0`. There is **no uniqueness theorem**, no numerical value of this gap, and no conversion of these dimensionless quantum-mechanical levels into observed particle masses. The parallel five-state collective-Hermite calculation now supplies the stronger upper estimate `E0<=127.619377843339...`; its printed decimal is floating evaluation, not an outward-rounded interval at every displayed digit. Its owner is `analysis/2026-10-08_collective_hermite2_4_ritz_refinement.md` and its committed JSON, integrated in1a0a2fd52.

The parallel selection rule in `analysis/2026-10-08_current_curvature_antiunitary_selection.md` (03746aaf2) provides a further connection. Its antiunitary T fixes every current and obeys T^2=1. The attained finite-dimensional ground sector is invariant under T and therefore has an orthonormal T-real basis: write any vector as the sum of its real and imaginary T-fixed parts, then use real Gram–Schmidt. **A T-invariant attained ground ray exists even without uniqueness.** Its Hermitian current-curvature expectations vanish. These expectations can be defined as `i(<J_e psi,J_f psi>-<J_f psi,J_e psi>)` on the finite-energy form domain, so no unproved commutator operator-domain regularity is needed. This does not establish that every ground ray is T-invariant or decide chirality in an infinite-volume theory.

### Parallel intake during this packet

Ten incoming commits from42d6a31e8 through7e956355d were fetched and reviewed before publication. Besides the five-state trial and antiunitary rule above, they supply exact single-edge CV homodyne cumulants, a degree-two minimality theorem for the centered adjacency-polynomial cone, a heterotic parity scope audit, their regressions, and formula-search catalog refreshes. The optical witness remains a single quartic CV gate; the heterotic audit correctly separates the selected215-model ledger from published distinct R-parity models. Their code and certificate values were read, not inferred from commit subjects. The centered minimality theorem is consistent with our off-center obstruction: quadratic matching needs a two-hop polynomial, while nonlinear matching is a separate problem. No parallel source is rewritten by this packet.

### A property(T)-independent positive floor

Let `r=(e_point0-e_point1)/sqrt2` in `W`, `M=exp(i r.q)` and `T=exp(-i pi r.p)`. Then `MT=-TM`. Their Hermitian real parts `X=Re M`, `Y=Re T` anticommute, have norms at most one, and obey `(X+Y)^2=X^2+Y^2<=2I`. For every vector,

```
||(M-I)psi||^2+||(T-I)psi||^2
  >= (4-2sqrt2)||psi||^2.
```

Combining this with(1) gives

```
H >= (4-2sqrt2)/(d(1,M)^2+d(1,T)^2) I.                (3)
```

The denominator is finite and nonzero, so(3) is a defined positive bound without a Kazhdan constant. Computing certified numerical upper bounds for these particular control distances is still required to turn it into a decimal lower bound. The Weyl relation itself also precludes a common zero vector: the generated Heisenberg center cannot act both trivially and with its nonzero represented phase.

##11783: finite-temperature trace from the stored Lie words

We inspect every parent and reduction step in the6240-row mod101 witness. Lifting the same word expressions to characteristic zero preserves independence, since a nonzero minor modulo101 cannot be zero rationally. The depth counts are

```
word-degree upper bound:  1    2     3     4     5
witness rows:           160  480  1840  2601  1159.
```

These are bounds for this specific witness, **not** asserted minimal dimensions of the graded filtration. They show that horizontal brackets of length at most five span the group Lie algebra. The local control estimate is therefore `d(1,exp z)<=C|z|^(1/5)` for small `z`. Theorem2.3 in [Jean's control-geometry notes](https://arxiv.org/abs/1209.4387) gives the required estimate and topology statement.

Apply this to the translation and modulation subgroups in(1), then use their Fourier difference-quotient characterization. For every `0<theta<1/5`,

```
|| |p|^theta psi||^2+|| |q|^theta psi||^2
  <= C_theta(h[psi]+||psi||^2).
```

Near zero the radial integral is `integral r^(2/5-2theta-1) dr`; for large parameters use `||(U-I)psi||<=2||psi||`. Choosing `theta=1/6` leaves the positive integrability margin `1/15`. Thus, as forms,

```
H >= c(|p|^(1/3)+|q|^(1/3))-C,   c>0,C>=0.
```

Min-max comparison and the Golden–Thompson heat bound for the fractional confining oscillator give, for every beta>0,

```
Tr exp(-beta H)
 <= exp(beta C) * 36 Gamma(234)^2/[2^78 Gamma(39)^2]
                  * (beta c)^(-468) < infinity.
```

The prefactor follows from the independent radial phase-space integral with Fourier normalization `(2pi)^(-78)`. Constants `c,C` have not been evaluated. The exponent468 is deliberately loose and has **no physical dimension interpretation**. A finite Gibbs trace gives a faithful typeI Gibbs state; it does not fix the previous modular-translation obstruction by itself.

##11779: an actual local algebra, supplied rather than inferred

Take `h1=L2(R,dtheta) tensor W_C` and its symmetric Fock space. For an interval `I`, define

```
K(I)=closure{hat g(exp(-theta)): g real in C_c^infty(I,W), integral g=0},
M(I)={Weyl(xi):xi in K(I)}'',  Omega=Fock vacuum.
```

Translations and dilations act by

```
[U(alpha,t)xi](theta)=exp(i t exp(-theta))xi(theta-alpha).
```

Their translation generator is multiplication by `exp(-theta)>0`. The half-line modular group is `Delta^(is)=Gamma(U(-2pi s,0))`, giving exactly

```
Delta^(is) T(t) Delta^(-is)=T(exp(-2pi s)t).
```

This explicit real-subspace construction, locality and standardness are established in section2.4 of [Modular Operator for Null Plane Algebras in Free Fields](https://link.springer.com/article/10.1007/s00220-022-04432-8); the modular commutation relation is discussed in [Longo–Witten](https://arxiv.org/abs/1004.0616). TypeIII1 for interval algebras is the conformal-net theorem stated as Theorem3.4 in [Kawahigashi's lectures](https://park.itc.u-tokyo.ac.jp/MSF/UGMSS/Kawahigashi.pdf).

There is also a direct nontriviality/locality check: for `g=phi'`, `h=psi'`, the symplectic pairing is `2Im<g,h>=-integral phi psi'`. Disjoint supports give zero. Choosing `phi=(1-x^2)^6` on[-1,1], zero outside, and `psi=phi'` gives the strictly positive rational `integral(phi')^2`. These piecewise-polynomial vectors belong to the closure of smooth interval tests; they are not incorrectly called smooth at the endpoints. The inclusion `M(1,infinity) subset M(0,infinity)` is half-sided and has a nontrivial relative commutant containing `M(0,1)`.

This supplies a local continuum algebra with the modular property the ordinary finite-cell typeI algebra lacks. **It is not a constructed limit of H**, and it is a chiral one-dimensional theory with78 internal labels, not a derived3+1 interacting universe. An abstract Hilbert-space isomorphism would not provide the missing dynamics or observable map.

##11780: spin tests and an honest index control

For the actual current-Dirac operator `D_current=sum160 gamma_e J_e`, its square is `H` plus the commutator spin curvature from11773. In the centered covariance family `C=t C0`, phase `F=fD`, and `U=VD`, both `VU^T` and `VCFU^T` are symmetric. Therefore every expectation `<[J_e,J_f]>` vanishes. **No constant-spinor Gaussian product improves the bosonic energy through its mean curvature term.**

More sharply, at `q=0` any centered Gaussian has zero gradient, so

```
D_current(eta psi)(0)=a^2(sum160 gamma_e)eta psi(0),
[a^2(sum160 gamma_e)]^2=(2/5)I.
```

There is no nonzero zero mode of this product form. This does not rule out entangled spin–configuration zero modes. Compact resolvent of `H` is not automatically compact resolvent of `D_current^2`: cancellation with its curvature is precisely the issue. Its Fredholm index remains open.

As an independent control, canonical q,p in the generated Lie algebra support the established Bott oscillator supercharge

```
Q_B=sqrt2 sum78(c_i^dagger a_i+c_i a_i^dagger),
a_i=(q_i+partial_i)/sqrt2,
Q_B^2=2(N_b+N_f).
```

Its unique zero is the even Gaussian times the fermion vacuum, so its even-to-odd index is+1. The exact heat supertrace is1. The one-mode annihilation equation has the L2 solution `exp(-q^2/2)`, while its odd partner grows as `exp(q^2/2)`. No finite-Fock-cutoff index was used. This is the known harmonic-oscillator index mechanism, also derived in section3.5 of [Wulkenhaar](https://arxiv.org/abs/0907.1351). It selects a different energy law and156 Clifford directions, so it neither assigns the index of `D_current` nor predicts a Standard Model generation or spacetime chirality.

##11781 and11784: the cone breaks into metric and magnetic curvature

For fixed optimized Gaussian covariance define `x=Vq+a`, `y=Up+a`, and the prior moments `vx=t*m`, `vy=m/t+f^2*t*m`, `c=f*t*m`. Exact Wick expectation is

```
E(q,p)=sum_e[x_e^2*y_e^2+vx*y_e^2+vy*x_e^2
             +4c*x_e*y_e+vx*vy+2c^2].
```

Writing `E=.5 p^T P(q)p+ell(q)^T p+V0(q)`,

```
P(q)=2 U^T diag(vx+(Vq+a)^2) U,
ell(q)=U^T[2a(Vq+a)^2+4c(Vq+a)].
```

`P(q)` is globally positive, because `vx>0` and `U` spans W. With the old fixed matched gradient `P(0)^(-1)`, the squared-speed matrix is `P(q)P(0)^(-1)`. For the prior integer kernel witness `w=(w_point,0)`, `||w||^2=216`, the exact trace is

```
trace[P(epsilon*w)P(0)^(-1)]-78
  =2106 epsilon^2/[5(vx+1/20)] >0  if epsilon!=0.
```

The proof uses the exact equal leverage `u_e^T P(0)^(-1)u_e=39/[160(vx+1/20)]`, cancellation of the linear trace, and `sum(V_e.w)^2=864`. At epsilon=.1, the squared speeds span approximately .950927 to2.314299. The all-one spectrum of the centered principal cone is lost. This is a stronger finite-background warning before any loop calculation; it is **not** a computed radiative correction. A prescription replacing the spatial metric by a background-dependent inverse would require a further action and consistency test.

Trace alone would still allow a single rescaled speed; an additional exact witness excludes that possibility. Let `r=e_point0-e_point39`, `s=e_line0-e_line39`. Both have `r^T P(0)r=s^T P(0)s=16(vx+a^2)`. Exact edge sums give `sum(Vw)[(Ur)^2-(Us)^2]=40` and the same sum with `(Vw)^2` equal to208. Their generalized Rayleigh quotients differ by `(10a epsilon+26epsilon^2)/(vx+a^2)>0` for epsilon>0. Hence `P(q)` is not proportional to `P(0)`: the split cannot be removed merely by a common speed renormalization.

Complete the square:

```
A(q)=-P(q)^(-1)ell(q),
Veff=V0-.5 ell^T P^(-1)ell,
E=.5(p-A)^T P(p-A)+Veff.
```

The compactness theorem has another consequence here: `Veff(q)=min_p E(q,p)>=E0>0` and **Veff is proper**, tending to infinity as `|q|` tends to infinity. If not, choose minimizing momenta along an escaping q-sequence. Their normalized displaced fixed-covariance Gaussians would have bounded form energy, yet converge weakly to zero, since their Gaussian moduli translate to infinity regardless of their phases. Compactness of that form ball would force a strongly convergent subsequence, contradicting unit norm. Thus the quantum variational scalar potential confines even after momentum relaxation; this is not inferred from the classical current-zero locus.

There is an independent **explicit quadratic confinement bound**. Put `d=vy-4c^2/vx`. Minimizing each edge over its y separately, a relaxation of the actual shared momentum, gives

```
(vx+x^2)y^2+4cxy+vy*x^2
  >= vy*x^2-4c^2*x^2/(vx+x^2) >= d*x^2,
Veff(q)>=160(vx*vy+2c^2+a^2*d)+d*q^T(4Pw-Adj)q.
```

Exactly `d=(m/t)(1-3f^2t^2)>0`: `f=-2b/(3mt+b)`, `b=1/20`, implies `|ft|<2b/(3m)` and `m>33/40`. Since `4Pw-Adj` has positive least eigenvalue `4-sqrt6` on W, this gives a quantitative quadratic growth coefficient. At the optimized covariance d is approximately .844940848 and the scalar term is122.693541734. **This scalar term is a lower bound for the fixed-covariance Gaussian trial family only; it is not a lower bound for the full quantum ground energy.** The formula is exact in the previously isolated algebraic t,m,f; displayed decimal evaluations are floating controls.

Let `beta=2(c+a^2)/(vx+a^2)`. Taylor expansion gives

```
A(q)=-beta Dq+2a(2beta-1)P(0)^(-1)U^T(Vq)^2+O(|q|^3).
```

The linear term is a removable phase gradient; the quadratic term is not. Define `M=Pw/4-Adj/10+Adj^2/40`, `r=e0-e39`, `s=e40-e79`, and `S=antisym[M U^T diag(Vw)V]`. Integer arithmetic on the stored actual geometry gives

```
r^T S s = -19840000/6400000 = -31/10.
```

Therefore at `q=a epsilon w`,

```
r^T(dA-dA^T)s
  =-31 a^2(2beta-1)/[5(vx+a^2)] epsilon+O(epsilon^2),
```

with a nonzero coefficient at the optimized covariance. This exact rational geometric witness is checked against an independent numerical derivative and a second orthogonal basis. The exterior curvature cannot be removed by a local scalar canonical phase. It is an induced variational magnetic field, not yet an identified gauge field of nature.

##11782 and11785: matter-preserving constraints and an explicit Lorentzian lift

On two copies of the78 canonical pairs impose only the mutually commuting `C_i=q1_i+q2_i`. The invariant canonical variables are `Q=(q1-q2)/2`, `P=p1-p2`. Their brackets are canonical and they commute with every constraint. The nonlinear current energy built from Q,P is gauge invariant; the Abelian BRST charge squares to zero. Reduction leaves `312-2*78=156` phase dimensions, hence78 canonical modes. Distributional states `delta(q1+q2)psi(Q)` and group averaging recover physical `L2(R78)`.

Unlike the full opposite-center conversion of11772, this supplied isotropic half retains matter. The graph has not selected that half. Alternatively an ideal clock with constraint `p_t+H=0` gives `Psi(t)=exp(-itH)psi0`, retaining the same physical Hilbert space. Neither choice derives the gravitational hypersurface-deformation algebra.

The standard [Eisenhart lift](https://arxiv.org/abs/1503.07802), including its magnetic generalization discussed by [Cariglia, Duval, Gibbons and Horvathy](https://arxiv.org/abs/1605.01932), applies directly to the computed P,A,Veff:

```
ds^2=G_ij dq_i dq_j+2du[dv+A_i dq_i-Veff du], G=P^(-1),
H_lift=.5(p-p_v A)^T P(p-p_v A)+p_u p_v+Veff p_v^2.
```

The inverse metric and Hamiltonian identity are checked symbolically; the full80D numerical metric independently has signature(79,1). The vector `partial_v` is null and Killing. Fixing its conserved momentum `p_v=1` and the null constraint `H_lift=0` recovers exactly `p_u+E=0`. Thus the same variational matter survives a reparametrization constraint and has an explicit Lorentzian geodesic representation.

There is a useful cosmological-constant control: shifting `Veff` by a constant Lambda is removed in this lift by `v_new=v-Lambda*u`. A constant energy shift is therefore a coordinate change here, **not** a demonstration of gravitational vacuum-energy screening. The metric was constructed to encode a Hamiltonian; no Einstein equation, four-dimensional compactification, measured gravitational coupling or cosmological constant has been derived.

## Reproduction and validation

Three producer sources and their matching `data/` certificates cover all eight passes. `tests/test_w33_pass11778_11785_compact_geometry.py` checks actual witness ancestry, Fourier/Weyl integrals, exact rational geometry, differential kernels, independent energy derivatives, second-basis covariance, full metric signature and null reduction. The earlier quantum-physics and antiunitary regressions are included in the focused CI workflow. Analytic compactness, operator domains and index scope require the proofs above; passing finite computations alone would not establish them.

The physical questions in the Forty Points paper remain distinct: selection of a realistic energy law and vacuum, an actual local continuum limit, spacetime chirality, observed masses/mixings/couplings and dynamical gravity. This packet establishes a finite-model attained vacuum and exact variational geometry, and supplies explicit controls where those physical links remain missing.
