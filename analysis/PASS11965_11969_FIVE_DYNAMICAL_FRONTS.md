# Pass11965–11969: execute the five dynamical research fronts

The five requested fronts were taken through explicit constructions and
falsifiable calculations. This packet does not close the nonlinear gravity,
full E6 vacuum, parameter-free flavour or4D chiral-continuum problems.

##11965 — transmit a genuine vacuum phase to quark CP

Pass11953 owns the F/D-flat singlet vacuum
`S=(1,i), T=(1,-i)` and its positive physical Hessian. Its conjugate is
distinguished by the gauge-invariant `Im(S1 T2)`. Pass11964 showed why a
nonzero coordinate phase or holonomy alone is insufficient.

Here that prior vacuum is connected to a quark weak-basis observable using
the real rational mass/Yukawa benchmark of11954. Set

```
m=[[1,1,0],[0,2,1],[1,0,3]]/10,
r=[1,2,1]/10, t=[1,-1,2]/10, mu=1/5,
B=r+i t, Hu=diag(1,4,9),
Hd=m [I-Bdagger B/(mu²+B Bdagger)] m.T.
```

Exact symbolic arithmetic gives

```
Im Tr([Hu,Hd]^3)=1071/800000,
det [[m,0],[B,mu]]=7/5000 >0.
```

Conjugating the vacuum reverses the weak invariant and preserves the
positive determinant. The nonzero invariant rules out every quark
weak-basis transformation restoring CP, including an attempted generalized
CP transformation compensating the scalar phase through flavour rotations.
A second nontrivial unitary basis gives the same exact value. Diagonalizing
the actual4x4 mass matrix at increasing heavy scales independently checks
the decoupling quartet.

This is transmission on an already constructed vacuum with supplied real
couplings. It does not derive measured quark masses, lift all E6 components
or establish radiatively safe strong CP. Scalar-vacuum priority remains11953.

##11966 — compute the light mode and the soft response

The11958 five-by-seven holomorphic constraint Jacobian has five positive
singular values.90-digit diagonalization, rechecked at120 digits, gives the
lowest canonical singlet mass

```
m_light=0.5805947896988066 GeV if Lambda=10^16 GeV, rho=1/32.
```

These scales are supplied inputs. This is a singlet-sector mass, not an
observed-particle prediction. It sharpens the prior4.71653GeV Rayleigh bound.
The F modes are orthogonal to the two complex gauge kernels; D terms lift
their radial gauge partners. The extra spectator masses lie above this mode
under the stated normalization.

We then vary an exact restricted curve satisfying the first four F
constraints and both D constraints:

```
P=p, S=(sqrt(p),i sqrt(p)), T=(sqrt(p),-i sqrt(p)),
PhiMinus=sqrt(u(p)), PhiPlus=1/sqrt(u(p)),
u-1/u=(2p+p²)/12.
```

With all multipliers zero, the remaining potential plus a supplied positive
P soft mass is exactly

```
V/Lambda^4=|sqrt(u(p)) p^12-sqrt(u(rho)) rho^12|²
           +(msoft/Lambda)² p².
```

At0.1GeV soft mass the selected minimum persists at `p/rho=0.999088347`.
At1GeV and1TeV no nonzero local minimum was found on the curve; the origin
is preferred. These are a restricted-curve result and a failure of the
small-soft-perturbation assumption, not a classification of every possible
softly broken vacuum.

In the leading constant-high-norm limit the normalized potential is
`(x^12-1)^2+kappa² x²`. Exact coexistence occurs at `x^12=10/11`, and the
nonzero minimum disappears at `x^12=5/11`. Both are symbolic regression
controls, distinct from the exact varying-u numerical curve.

There is also an exact obstruction to a simple repair. Charge assignments
on these seven condensates preserving the constraint polynomials satisfy a
rank5 linear system; its two-dimensional kernel is precisely the existing
X/Z charge span. An additional Abelian factor supplies no independent D
direction at the same F/D-flat branch. New fields or changed stabilization
operators are required. Shifted-FI vacua remain outside this statement.

A low-scale gauge-mediation scale example gives gravity-scale breaking
`m_3/2=2.97955e-8 GeV`, small enough on the restricted curve. The example
does not compute direct transmission, kinetic mixing, A terms, tadpoles or
a supergravity vacuum. [Giudice–Rattazzi](https://arxiv.org/abs/hep-ph/9801271)
is prior art for the mediation framework.

##11967 — test flavour-selection potentials and a surviving route

Separate-sector spectral potentials are invariant under independent unitary
orientation changes and cannot select mixing. For a single mixed potential
`V=-Tr(A U B Udagger)` with simple spectra, stationarity gives
`[A,U B Udagger]=0`; trace rearrangement selects an aligned permutation.
The derivative is verified against an independent finite difference.
This familiar alignment mechanism does not select observed mixing.

Applying a Majorana Coleman–Weinberg potential to the five stored11960
lepton roots also fails to select an unambiguous phase. The symmetry-allowed
invariant counterterm `c Tr[(Mnu† Mnu)^2]` changes their ranking. Its UV
matching coefficient and the full stabilizing potential are unspecified.
The calculation demonstrates matching dependence, not that every displayed
coefficient defines a stable full UV vacuum. The absolute splitting scale
and subtraction scale are supplied. TOE51 owns the branch-observable work.

The obstruction does not apply to every Majorana-sensitive potential. A
known O2 right-handed invariant gives a constructive positive control:

```
I_R=Tr[(Ynu Ynu.T)(Ynu Ynu.T)dagger]
   =2 y1² y2²+t(y1²-y2²)², t=|(U_R U_R.T)11|².
```

A positive coefficient globally selects the offdiagonal symmetric unitary
orientation. The exact example has `I_min=8/81` versus `I_diagonal=17/81`.
Its two Takagi masses are both2/9. The displayed45-degree basis is therefore
not a prediction of an observable angle: the masses are degenerate.
This is a positive orientation mechanism to extend and split, not a repaired
three-family fit. [Alonso et al.](https://arxiv.org/abs/1306.5922) own the
Majorana/O2 mechanism; [their earlier potential work](https://arxiv.org/abs/1103.2915)
also establishes the dynamical-alignment context.

##11968 — native tensor constraints and an explicit linear completion

Build three native antisymmetric vertex derivatives
`D_i=C.T diag(j_i) B/2`, where B is signed incidence, C unsigned incidence,
and j_i is the harmonic projection of the three marked voltage cochains.
`B.T j_i=0` guarantees antisymmetry. The derivatives do not commute.

The corresponding canonical linear tensor Hamiltonian/momentum constraint
attempt has the exact rational Poisson bracket

```
{H_vertex34,M_component1_vertex70}=8667/4096000 !=0.
```

This is distinct from11301's scalar-lapse obstruction and11955's continuum
Fierz–Pauli positive control. A rotated derivative basis retains the total
commutator norm, protecting the conclusion against a coordinate artefact.

An explicit finite linear completion is possible. Let P_M project onto the
momentum-constraint row space, define `Hc=H(I-P_M)`, and let P_H project onto
row(Hc). Then `Hc M.T=0` exactly as an algebraic construction. With
`Q=I-P_M-P_H`, the named positive quadratic Hamiltonian

```
Hphys=(p.T Q p+q.T Q (I6 tensor B.T B) Q q)/2
```

preserves the constraints and gauge flows. At the stored numerical rank
threshold the momentum rank is234, Hc rank78, and physical configuration
dimension168. The projection has substantial offsite support: this is a
nonlocal added choice, not local Einstein dynamics or a two-helicity proof.
Nonlinear hypersurface-deformation closure and coupling to stress energy
remain open. [Bonzom–Dittrich](https://arxiv.org/abs/1304.5983) establishes
discrete gravitational algebras in specific sectors, not this completion.

##11969 — an interacting quantum gauge–fermion Hilbert space

The native octagon now has all70 half-filled eight-site fermion
configurations and one compact global flux integer. Gauss's law is solved
exactly. Fermion hopping shifts the crossed electric link; independently
constructed Jordan–Wigner operators verify the statistics, including the
periodic boundary. Bare fermion hopping without the rotor violates Gauss.

At winding cutoffs1,2,3,4 the native gap is respectively
`1.084433461,1.082280628,1.082278020,1.082278018`; the final Hilbert space has
630 states. All eight fermions and the rotor are quantum and coupled.
Exterior links are frozen: this is not the full1385-plaquette native theory.

The front now also defines the **full declared finite native operator**.
Its physical Hilbert space is
`ell²(Z^81) tensor wedge^40(C^80)`, with79 tree links reconstructed from
the80 site charges and81 integer chord fluxes. Signed subtree charge sums
solve Gauss exactly; tree unimodularity proves the coordinate map is
bijective over integers. Every native edge hop and every supplied plaquette
shift has an explicit action in these coordinates. Zero commutator-chain
rows contribute identity Wilson operators, whose magnetic terms cancel.

The matrix-free compiler verifies1312 legal fermion hops in16 full random
states and all1385 plaquette moves. Acting on one state generates2847
nonzero-or-diagonal destination entries without enumerating the Fock space,
whose half-filled dimension is107507208733336176461620. Electric energy is
a self-adjoint positive diagonal operator; the finite magnetic-shift and
fermion-hopping sums are bounded symmetric perturbations. Thus the named
full Hamiltonian has a self-adjoint semibounded closure. This defines the
quantum model; it is not a whole-spectrum diagonalization or4D continuum
proof. The exterior-freezing limitation applies to the octagon benchmark,
not to this full compiler.

A separate standard1D refinement provides a real continuum control. The
initial `m_lat=0` regulator missed the known Schwinger gap by about21% at
ten sites. The published mass matching

```
m_lat=m_physical-e²a/8
```

repairs this. Its integer translation/flux map is explicitly built; exact
rational energy cancellation and the bulk hopping intertwiner are checked.
For unit-charge fermions it relates distinct theta theories, rather than
being an internal symmetry at fixed theta. The finite flux cutoff is not
invariant under the map, so the exact claim is untruncated and the numerical
operator check excludes boundary columns.

| Sites | Matched gap | Known comparator e/sqrt(pi) |
|---:|---:|---:|
|8|0.393450389|0.394932708|
|10|0.393582836|0.394932708|
|12|0.393852563|0.394932708|

With mass matching and explicit source-sign averaging, static screening
extracts charges0.67860,0.68684,0.69105 at8,10,12 sites against the supplied
charge0.7. The largest separation is held out of the extraction; prediction
errors are0.000906,0.000255,0.000109. This is finite-spacing effective-charge
matching, not a prediction of the supplied charge or a4D beta function.
The1D cycle refinement is not a constructed W33 refinement tower.

[Dempsey et al.](https://arxiv.org/abs/2206.05308) own the mass-shift theorem.
The contribution is its explicit verification in this coupled Hamiltonian,
native subsystem quantization and controlled benchmark. Standard quantum
link/continuum work is also [prior art](https://arxiv.org/abs/2104.00025).

## Reproduce and remaining boundary

Run the five `w33_pass11965_11966`, `11967`, `11968`, `11969_quantum`,
`11969_full_native` producers and
`tests/test_w33_pass11965_11969_five_dynamical_fronts.py`. Certificates retain
the mathematical and physical scope of each front; the dedicated hosted
workflow checks frozen and regenerated results separately.

The packet supplies an exact weak-CP transmission witness, a quantitative
soft-stability gate and charge-kernel obstruction, a tested Majorana
orientation route, an explicit native linear constraint completion, and a
coupled quantum gauge–fermion simulator calibrated against known1D physics.
It does not yet supply a single stable UV action selecting all observed
parameters and reproducing nonlinear gravity and the chiral Standard Model.
