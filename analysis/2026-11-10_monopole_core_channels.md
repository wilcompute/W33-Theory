# Primitive monopole core forcing and light radial channels

The primitive W33 monopole charge admits an embedded `SU(2)` in the canonical `SU(5)` chart. The published scalar potential sources both an adjoint direction outside this `SU(5)` and a matter field inside the core. The frozen-spectator embedded monopole therefore fails the full scalar equations. An exact torus reduction gives a smaller consistent sector in which to solve them. [Primitive cocharacter](2026-11-10_global_gauge_topology.md), [Canonical flat vacuum](2026-11-09_canonical_sm_flatness.md)

## The core sources

On the faithful five-block, choose the step operator taking the charged weak coordinate to the first color coordinate. Its commutator with its transpose is the primitive cocharacter `m=diag(1,0,0,-1,0)`. The replay constructs both matrices on the 27 and checks the `sl2` relations. The adjoint contains one triplet, twenty doublets, and 35 singlets under this monopole root.

Write the asymptotic adjoint `A0 = 6Y = A_perp − (5/2)m` using the trace metric. A regular embedded trial profile holds `A_perp` fixed and sets `A(s)=A_perp−(5/2)s m` in a diagonal gauge, with `s=0` at the center and `s=1` at infinity. Keep the original matter VEVs fixed for this test. They are singlets under the embedded `SU(5)`, and every trial adjoint annihilates them. The mixed terms, signed cubic, split masses, and centered trace interactions give zero first derivatives on this locus. The dressed Yukawa and optional neutral-current operators have zero first and second derivatives there because their endpoint factors annihilate the VEVs. The spectator vanishes, and the D moment map is zero on the trial profile.

The surviving F energy comes from the adjoint trace polynomial. In the unit trace kinetic metric, the exact Cartan projection of `A^5−3A^4−283A` gives the F gradient. The derivative of its squared norm in the `A_perp` direction is `(s²−1)` times a polynomial with strictly positive coefficients in `s²`. Its core value is `−1061338875/128`. There is also a nonzero core derivative `1503375` along the internal circle generator with charge four on `e0`. That generator is outside the embedded `SU(5)` and commutes with the monopole root. The transverse Cartan gradient vectors span dimension three along the trial line.

The mixed interaction `Z[1] A X[0]` also transmits the adjoint F gradient to the real `e0 ⊗ f2` component of `X[0]`. Its exact potential derivative is `100(s²−1)`. These frozen directions have zero covariant kinetic derivative on the trial ansatz, so they cannot satisfy the full equations. The result concerns this embedded ansatz with frozen spectators. It leaves open solutions with the sourced fields allowed to vary.

## A consistent sector for the coupled equations

Take the connected rank-three torus in the Standard Model Cartan that annihilates the monopole root character. It commutes with the embedded monopole `SU(2)`. Its fixed part of the 27 is exactly `span(e0,e1)`. Its fixed part of the internal adjoint has dimension ten and consists of the monopole triplet and seven singlets. Thus the fixed gauge algebra has real dimension eighteen including the external family algebra. The fixed chiral scalars comprise thirty complex fundamental and dual components and ten complex adjoint components. The family spectator can be set to zero because its interactions start at quadratic order in that field.

Gauge and scalar equations close on this fixed sector because the action and the monopole transition function respect the torus. This statement supplies a symmetry reduction and retains the sourced fields. A radial solution still requires the gauge constraints, coupled scalar profiles, and regularity conditions.

The forty fixed complex scalar components have holomorphic mass rank 26 and broken complex gauge orbit rank 14. The heavy spectator supplies no additional flat component. Thus the F-flat vacuum is locally isolated modulo complex gauge in this fixed sector. With the positive kinetic metric, imposing D-flatness selects the compact orbit locally. One can see this from the positive Gram of the broken gauge directions, which is the linearized D equation along their noncompact complex partners.

## Smooth trial fields and an energy bound

In the magnetic-charge-one sector, take the regular hedgehog profiles `s(r)=r/sqrt(r²+R²)` and `K(r)=R²/(r²+R²)` for the scalar triplet and the gauge field. They are smooth at the origin, approach the prescribed charge at infinity, and give finite energy. With gauge kinetic term `Tr(F_ij F_ij)/(2g²)` and adjoint kinetic scale `t`, their energy is

```text
E_trial = 4 pi [ a/(g² R) + b t R + c R³/t ].
```

The coefficient `a=63 pi/32` follows from the gauge integral `3∫[2K'^2+(1−K²)^2/r²]dr` at unit radius. The coefficient `b=225 pi/16` follows from the scalar gradient `75∫[r²s'^2+2K²s²]dr`. The coefficient `c` is the beta-function integral of the exact F potential in the certificate. Minimizing over positive `R` gives about 4490.87 at unit `g,t` in the supplied field units. This is a variational upper bound for the infimum. The smooth normal perturbation `δA = ε K(r) A_perp` has strictly negative first variation of the energy at positive `ε`, with coefficient `4 pi R³/t` times `−378464532375 pi/32768`. Its kinetic cross term vanishes by trace orthogonality and commutation with the monopole group.

Completing the magnetic and adjoint gradient squares gives the Bogomolny lower bound `120 pi sqrt(t)/g` because the flux is `2 pi m` and `|Tr(A0 m)|=30`. A smooth solution in the fixed sector cannot saturate it. Saturation requires both vanishing F and D potential and `B/g = ±sqrt(t) D A`. Near infinity the local flatness result would force the fields onto the compact vacuum orbit, so `Tr(A D A)=d Tr(A²)/2=0`. The first-order equation would then give zero asymptotic `Tr(A B)` flux, contradicting the charge. This excludes saturation for such a solution. It does not give a strict lower bound on the infimum beyond the Bogomolny value.

## Lowest angular channels

A left Weyl weight of monopole flux charge `n` gives the sphere Dirac index `n`. In the flux-one sectors the corresponding lowest angular momentum is zero. The 49 light chiral components have flux charges `−1,0,+1` with multiplicities `13,23,13`. The twelve unbroken gauginos add `3,6,3`, giving `16,29,16` for the exact supersymmetric massless spectrum. The light chiral gauge anomaly traces vanish. In the Cartan basis `(color1,color2,2T3,6Y)` the mixed traces `sum n B q` and `sum n L q` both equal `(0,0,-3,9)`. Their projections onto the electromagnetic and monopole generators vanish, as does their difference on the full Cartan. [Lowest-wave monopole channels](https://doi.org/10.1007/JHEP02%282023%29159)

At unit adjoint kinetic normalization, projecting the monopole step operator onto the physical light chiral quotient gives rank twelve between the two thirteen-dimensional charged sectors. The unmatched input is an up-type Higgsino. The down-antiquark block has rank three only when the orthogonal down-Higgsino row is included. Its three lepton rows alone have rank two, leaving one pure lepton combination without a direct projected root pairing. The unbroken gaugino root projection is zero because their hypercharge is zero and the monopole step has nonzero hypercharge. Other interactions can mix chiral fermions and gauginos in the actual core.

These are angular channels and projected currents. The exact vacuum has massless asymptotic fields, and this calculation supplies neither a gapped Callias problem nor a scattering boundary condition. Normalizable modes and baryon catalysis require a core solution and a radial fermion analysis. [Massless monopole index boundary](https://arxiv.org/abs/2106.13820)

Run `python analysis/toe_20261110_monopole_core_channels.py` from the repository root. [Frozen gradients and channel matrices](../data/toe_20261110_monopole_core_channels.json)
