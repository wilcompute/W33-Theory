# Passes11742–11749: nonzero holomorphic flavor and an explicit local E8 frame

Reservation **3b08c1d72** was pushed before computation. This packet pursues
all five previous targets and three additional independent checks. It is
written directly in `C:\Repos\Theory of Everything`.

The two strongest positive results are a supplied smooth Calabi–Yau quotient
with three chiral cohomology modes and a nonzero holomorphic cubic, and an
explicit local generalized parallelization for the previous rank14 E8
embedding tensor, including its constrained ancillary parameters. These
remove particular mathematical obstructions. They do not give measured
flavor, a complete compactification vacuum, or a physical TOE.

Artifacts: [producer](w33_pass11742_11749_nonzero_flavor_and_flux_frame.py),
[source-bound certificate](../data/w33_pass11742_11749_nonzero_flavor_and_flux_frame.json),
[independent regressions](../tests/test_w33_pass11742_11749_nonzero_flavor_and_flux_frame.py).

## Intake and ownership

GitKraken fetch/review found no incoming science after the previous receipt
and merge. The parallel formula-universe freeze `c16496fe5` was incorporated
in merge `875b47e8c`; it changes the formula-search inventory, not the imported
scientific implementations. The unrelated10956 source/certificate and mixed
Continuity stores are preserved. All deliberate changes are logged.

The previous11734–11741 report, certificate/interfaces, current site results,
and the forty-points physics scorecard and epilogue were revisited. Their
unresolved measured flavor, dynamical principle, continuum gravity and vacuum
problems remain the standard of comparison. We searched the result values
and degree vectors, not only topic names: `(-2,1,1,0)`, `(0,-3,0,1)`,
`(2,2,-1,-1)`, `sqrt(241)`, type112, free Klein4, rank14 gaugings,
generalized-frame/ancillary formulas and the actual anomaly coefficients.
The `sqrt(241)` hits in11602–11606 concern another singular-value calculation;
matching an integer does not identify the construction.

Ownership and primary external checks:

- **11681** owns the actual sl9+trivector E8 bracket and split real form.
- **11732/11734** own the actual projected rank14 tensor; **11733** owns
  the constant eight-direction section. **11735/11741** own the alternative
  topology-compatible Higgs and the earlier cubic-zero CY inventory.
- **11271/11636** own the signed E6 cubic. **11739** supplies its actual
  signed81-root dictionary. No new E6 invariant or45/270 count is claimed.
- [Blesneag, Buchbinder, Candelas and Lukas,1512.05322](https://arxiv.org/html/1512.05322v2)
  supplies the type1/type2 Koszul/cup method and diagonal free Klein4
  tetraquadric action. Its equation4.17 has cover dimensions(2,2,4).
  The degree choice below is a particular(4,4,4) application of that method.
- [Inverso and Rovere,2410.14520](https://arxiv.org/html/2410.14520v1)
  supplies E8 generalized Lie/Dorfman and ancillary-frame conventions,
  equations3.3 and3.10–3.24. The general14D abelian gauging type already
  occurs in the Hohm2006 material cited by11734. The addition here is the
  explicit frame for this repository's projected tensor.
- [Anderson, Gray, Lukas and Palti,1202.1757](https://arxiv.org/html/1202.1757)
  supplies the heterotic line-bundle axion mass/D-term framework; we apply
  its charge-map rank test to the stated bundle.
- [Dorey et al.,hep-th/0209099](https://arxiv.org/abs/hep-th/0209099)
  discusses mass-deformed N=4/N=1* vacua. The SU2-representation F-flat
  mechanism is classical prior art; our conditional coupling is specified below.
- **10962** already uses complex-orbit D-flatness and credits Luty–Taylor
  and Kempf–Ness. Moving along a complex F-flat orbit is not a new general
  mechanism;11745 supplies explicit matrices and the shared SU2/X scale
  relation for the present added-field inventory. Its supplied CY route
  does not supersede10962's orbifold-spectrum exclusions.
- **11619/11671/11730/11738** already distinguish common shifts,
  fixed-volume conditions and sector weights. The supplied boson model
  below is a concrete carrier/test, not a new general sequestering mechanism.
  [Kaloper et al.,1505.01492](https://arxiv.org/abs/1505.01492) is the
  separate local-sequestering framework; its gravitational action is not
  derived by our occupation-number model.

##11742 — Change the cohomology type, rather than deform the old zero cubic

Let X be a smooth tetraquadric in A=(CP1)^4, normal degree D=(2,2,2,2).
Take the three summands of V=K to have degrees

```
K1=(-2, 1, 1, 0)
K2=( 0,-3, 0, 1)
K3=( 2, 2,-1,-1).
```

Their sum is zero. Bott–Künneth and the Koszul exact sequence give
h(X,Ki)=(0,4,0,0), h(X,Ki*)=(0,0,4,0). There are no nonzero source/target
Koszul overlap maps requiring a generic-rank assumption. K1,K2 are type1;
K3 is type2, represented by H2(A,K3-D)=H2(A,O(0,0,-3,-3)).
This is a different bundle from11741, whose local all-type1 cubic remains zero.

The exact positive Kähler point is

```
t=(1,(13+sqrt(241))/12,1/2,(5+sqrt(241))/36).
```

All three slopes vanish: Ki·κ=0, κ_i=sum_{j<k; j,k!=i}t_j t_k.
Hence the split holomorphic bundle is polystable at this supplied point.
The same construction scales to large volume; neither the scale nor a
quantum-corrected moduli vacuum is selected.

Let g=diag(1,-1), h=swap(u,v) act on all four factors. Their lifts anticommute
on O(1), but each Ki has even total degree, so its full line lifts commute.
Their determinant product is trivial. In the O(2) eigenbasis
u²+v², u²-v²,2uv the three characters are ++,+-,-+.
There are21 invariant degree(2,2,2,2) products. At each CP1 point at least
two of the three sections are nonzero. Every one of the81 minimal
availability patterns contains an invariant four-factor product. Thus the
invariant linear system is basepoint-free, not merely nonzero at corners.
Bertini gives a generic smooth member. Each nonidentity g,h,gh has16
isolated ambient fixed points, with trivial hypersurface fiber character;
avoiding their finite union is a nonempty open condition. The residue3-form
is invariant. Consequently a generic free quotient X/Gamma is a smooth CY.
This is an existence proof for a family, not a chosen explicit vacuum polynomial.

In Serre-dual coefficient bases, the cohomology actions are

```
K1,K2: g=-G tensor G, h=-H tensor H
K3:    g= G tensor G, h= H tensor H.
```

Each is a four-dimensional regular representation, with character(4,0,0,0).
Every line has exactly one invariant cohomology class. The quotient therefore
has three chiral modes and no opposite partners, verified directly by
characters rather than inferred only by dividing an index.

The natural invariant coefficient matrices are epsilon,epsilon,I2, where
epsilon=[[0,1],[-1,0]]. The type112 product is the threefold Serre contraction

```
C(a,b,c)=sum_{i,j,k=0,1} a_ij b_ik c_jk.
C(epsilon,epsilon,I2)=2.
```

In this declared residue/Serre normalization the quotient integral is2/4=1/2.
Unit Euclidean coefficient vectors give cover value1/sqrt2. Neither number
is a canonically normalized physical coupling: the Ricci-flat/HYM kinetic
metrics are missing. Nonvanishing is unchanged by finite positive metrics.

The actual base27 roots carry the physical-family fundamental, so V=K is
used, and the hidden defining5 is W=K*+O². This fixes an otherwise easy
orientation mismatch. Integral c3(V) is-24 on X and-6 on X/Gamma;
chi(V)=-12/-3, while h1-h2=12/3. Conjugating all matter reverses chirality
and X charges. No arrow-of-time selection of that orientation is derived.

##11743 — An actual local generalized parallelization

Use the previous seven symmetric tensor pairs T and invariant form B with
long-root norm2 (Killing=60B). Write

```
S_i=A_3i, i in {0,1,2,4,5,6,7,8}
T=sum_i S_i odot R_i
R_0=x013, R_2=-x123, R_i=x13i for i=4,...,8, R_1=0.
```

All Ri commute with every Rj and Sj in the actual11681 bracket. Define

```
C(y)=sum_i y_i R_i, E_a(y)=exp(ad C(y))a, rho=1.
p_a^i=B(S_i,a), q_a^i=B(R_i,a)
Sigma_a sharp=-sum_i q_a^i S_i.
```

The exponential is finite because its adjoint generator is nilpotent;
the producer also bounds each individual generator's nilpotency.
The anchor is constant, and the derivative directions form an integrable
constant coordinate section. The ancillary parameter is constrained to
that same section and is constant. We check on all248 basis generators

```
D(a)=sum_i [S_i,[R_i,a]]=6 Tsharp(a),
Tsharp(a)=sum_i(p_a^i R_i+q_a^i S_i).
```

The generalized vector product has transport term[pR,b], projected rotation
term[D(a),b], and ancillary term[qS,b]. The density divergence vanishes.
Together they give

```
L_(E_a,Sigma_a) E_b=7 exp(ad C)[Tsharp(a),b].
```

Omitting the ancillary gives coefficient6 instead of7 in the qS channel,
so it cannot be silently discarded. For full Dorfman closure the rotation
is constant (it lies in the abelian image of Tsharp); hence DeltaSigma=0.
Ancillary transport and constrained derivative terms vanish. The right
ancillary parameter is also zero, because B(Ri,[Tsharp(a),b])=0 by invariance
and [Ri,Tsharp(a)]=0. Thus both components close, not only the vector part.
The effective embedding tensor is7T, up to the sign of the conventional
definition E_A circle E_B=-X_AB^C E_C and an overall gauge coupling.
Singlet and trombone components vanish.

This constructs a local frame on a supplied R8 section. Compact patching,
integral flux, higher-dimensional solutions and a physical vacuum are not
obtained. Split E8 duality and compact internal E8 gauge symmetry remain
different roles; this eight-dimensional section is not identified with
the six-dimensional CY used for matter.

##11744 — Exotic pairing exists; the minimal singlet vacuum does not

The actual-root Cartan
X=diag(1,1,1,0,0,0,-5,1,1) gives the base27 charges

```
27 -> 10_2 + 5_-4 + 2 bar5_-1 + 2 singlet_5.
```

The SU5³, SU5²X, gravitational-X and X³ anomalies vanish per27. The rank2
family axion charge map can make the two family U1 vectors massive at a
positive kinetic metric, using the standard heterotic mechanism. It does
not mass X: that generator is orthogonal to the family bundle flux.
These anomaly checks do not replace the ten-dimensional Bianchi identity.

The A36 singlet component of the actual signed E6 cubic pairs each of the
five5 components with one of the two bar5 sets. Its gauge block has rank5.
For three singlet VEVs v_i the family mass block is

```
Y(v)=1/2 [[0,v3,v2],[v3,0,v1],[v2,v1,0]], detY=v1 v2 v3/4.
```

At all v_i nonzero the15-by30 exotic block has rank15. It could leave
three(10+bar5) chiral SU5 families. This is a conditional mass route.
All available SM-singlet chiral matter has X=+5; the opposite modes have
zero H1. With zero X FI,

```
D_X=5 sum_i,alpha |S_i,alpha|².
```

Positive kinetic metrics force S=0 in a supersymmetric SM-preserving
minimal vacuum. Thus the same inventory cannot both be D-flat and use
that exotic mass route. Bundle moduli have X=0 and do not fix this sign
problem. Quantum-corrected complete-vacuum data are not supplied here.

##11745 — A coupled conditional repair and its remaining degeneracy

Add an explicitly imported SU5-singlet vectorlike pair P,Q with X charges
+5,-5 and zero family charges, and neutral Z. These are not inferred from
the preceding cohomology or asserted to form a full E8 multiplet.
In a rigid broken-phase EFT take the supplied superpotential

```
W=Tr(Phi1[Phi2,Phi3])+(m/2)sum_a Tr(Phi_a²)
  +W_E6 +Z(PQ+(2/3)sum_a Tr(Phi_a²)).
```

On the global trivial doublet start with Phi_a=i m J_a, zero on K*, and Z=0.
The matrix F terms and adjoint-only D terms vanish. Since
sum Tr(Phi_a²)=-3m²/2, F_Z sets PQ=m², tying the balancing scale to the Higgs mass input.
At m=1, S_i=1 in the A36 component and all charged exotics zero, put r=3.
More generally r=sum|S_i|² and

```
|P|²=(sqrt(r²+4m⁴)-r)/2,
|Q|²=(sqrt(r²+4m⁴)+r)/2.
```

These solve PQ=m² and D_X=5(r+|P|²-|Q|²)=0. Equal weighted S_i norms
cancel the three family charges at the supplied zero-slope point. The
E6 cubic F terms vanish on the singlet-only locus by the actual charge
selection rule. The imported pair adds zero linear/cubic X anomaly.

There is another gauge equation: A36 is an SU2 highest-weight doublet,
verified by the actual E8 brackets. Its three singlet densities contribute
r Jz to D_SU2. Normal Phi alone therefore does **not** give the claimed
full D-flat configuration. The final witness uses the complex F-flat orbit

```
Phi_a=i m g J_a g^-1,
g=diag(sqrt(a),1/sqrt(a)),
a²=(sqrt(r²+4m⁴)-r)/(2m²).
```

Now sum[Phi,Phi dagger]=m²(a²-a^-2)Jz=-r Jz, cancelling that density.
Tr(Phi²) and the F equations are unchanged. The same rescaling gives
P=m a,Q=m/a, so both nontrivial gauge D equations are solved by one
algebraic relation. At m=1,r=3 it is a²=(sqrt13-3)/2.
This global transformation acts only on O². We retain the failed
normal-Higgs partial-D control in the certificate and a dedicated regression.

This action still does not select the wanted branch: all seven SU2
partitions of5 solve its matrix F equations, and suitable P,Q can satisfy
F_Z on each branch. Geometry/moduli and clocks remain inputs. The
construction is a named conditional repair, not a derived string vacuum,
full-E8-covariant action, supergravity F-flat solution or quantum stability proof.
The seven partitions are a local matrix census, not seven global vacua:
11728 still obstructs the global principal5. Zero and the trivial-doublet
branch both extend globally, so that refinement does not give uniqueness.

##11746 — Fix state and boundary data in a quantum volume carrier

On the actual40-vertex W33 commutation graph use

```
H=sum_ij L_ij b_i dagger b_j +(u/2)sum_i n_i(n_i-1), u=2/3.
```

The one- and two-boson sectors have dimensions40 and820. H conserves total
N, while [H,n_0] is nonzero. If volume is supplied as alpha N, a common
vacuum shift is C alpha N I within a fixed sector. At the same initial
state, observation time and boundary sector it produces only a common
unitary phase and cancels from normalized Gibbs correlators. The test
includes the actual820-dimensional same-state unitary evolution.

The controls matter: an inhomogeneous shift C n_0 changes the Gibbs state;
mixing N=1,2 changes normalized sector weights, with d_C p=-beta p(1-p)
in the degenerate two-sector model. Conservation of occupation is built
into this Hamiltonian. Equating it to spacetime volume, deriving its
constraint from gravity and explaining the measured cosmological constant
remain open. This supplies no Einstein equation or gravitational screening.

##11747 — Exhaustive character robustness

For every one of64 character triples the exact cup is computed. All16
triples whose product is trivial have raw cover value+2 or-2; all48 forbidden
triples vanish. Each individual character retains one mode on each line.
For every possible common Wilson character on5/bar5, invariant singlets
give a full-rank three-family exotic mass matrix. Thus the nonzero route
survives these character choices. This does not establish proton stability,
full Wilson-line spectra or stability under other deformations.

Two further controls reject the simple equal-VEV repair as a realistic model.
All these character mass blocks are full rank, so the electroweak doublets
are lifted along with colored triplets; no light5/bar5 Higgs pair remains.
Also let the four surviving light fields be

```
a=family0 x123, b=family1 x378,
c=family2 x013, d=family0 A31.
```

Their E6 weights are three10s and one bar5. With singlets v_i=1, form the
actual15-by15 mass block between5 and the k-type bar5. Reconstruct the
linear sources J_5,J_bar5 directly from the signed cubic, and eliminate
this block by W_eff=-J_bar5^T M^-1 J_5. The result contains

```
W_eff=-a b c d/4.
```

The two relevant cubic entries have sign-1 and the inverse family entry
is1; the producer also sums the full sources to exclude a hidden cancellation.
On visible slots(0,1,2,7,8), the first three are colors and the last two
weak indices. This is a Uc_0 Ec_1 Uc_2 Dc_0 component of10³bar5, surviving
the visible diag(1,1,1,-1,-1) Wilson parity. It is a nonzero dimension-five
baryon/lepton operator. Such a triplet-exchange mechanism is standard GUT
physics; the stated coefficient is the computed application of this exact
root/cup/mass inventory. We have not computed a decay rate or proved that
every alignment or added sector has this operator. The absence of the
minimal supersymmetric VEV and this conditional-vacuum obstruction are
different tests; importing P,Q fixes the first and does not fix the second.

##11748 — A negative coefficient was a coordinate artifact

In pair order01,02,03,12,13,23 the cover Bianchi budget c2(TX)-c2(V) is
(6,0,2,3,-1,5). The six formal pair classes span only a four-dimensional
rational H4. In particular

```
J0J1+J2J3-J0J2-J1J3=0.
```

Its pairing with every J_i is zero; h11=4 and Poincaré duality make this
a rational cohomology identity. Subtracting it gives the effective
representative(5,1,2,3,0,4), with divisor pairings(14,14,14,18).
Each nonnegative pair is a complete-intersection effective curve class.

This proves an effective cover budget. It does not build an integral
equivariant cycle on the quotient, address torsion or give a hidden bundle.
Averaging over Gamma multiplies a cycle class by4; division by4 is not an
integral descent construction. Quotient anomaly completion remains a
specific missing object rather than a false negative-coefficient alarm.

##11749 — Why a nonzero cubic still cannot predict masses

For any invertible holomorphic Dirac matrix Y and positive Hermitian Q,
take Z_L=I and Z_R=Y dagger Q^-1 Y. Then

```
M=Y Z_R^(-1/2), M M dagger=Q.
```

With the *same* equal-VEV holomorphic Y from11744 we give exact positive
metrics producing singular values(1,2,3) or(1,1/10,1/100), and a complex
Hermitian Q with nontrivial left mixing. This proves underdetermination
when kinetic metrics are unspecified. It does not say a fixed CY vacuum
can choose arbitrary metrics, nor give independent left/right metrics
to one Majorana field. Computing the vacuum metrics is indispensable.

## Execution and limits

The producer certifies all eight sections, with exact algebraic quantities
and explicitly labelled floating-point evolution/bracket comparisons.
Independent tests cover the source-bound frozen certificate and actual
11681 tensor brackets, quotient cohomology and nonzero Serre contraction,
finite-coordinate frame transport and ancillary closure, actual-root exotic
pairing, coupled F/D equations,820-dimensional fixed-state dynamics,
cohomology-class effectivity, positive-metric counterexamples and the explicit
heavy-exchange baryon/lepton operator and the full SU2 singlet/adjoint
D cancellation. The final suite contains25 new tests.

All five targets were investigated. The frame and nonzero holomorphic
interaction are constructed locally/in the supplied geometry; measured
normalization is not. The anomaly/exotic target identifies an exact minimal
obstruction and conditional EFT repair, not geometric completion. The
coupled action still leaves branches/moduli/clocks unselected. The vacuum
test retains fixed-sector cancellation and mixed-sector response; it does
not solve the cosmological constant. The three additional probes close the
character, cover-class and identifiability questions in their stated scopes.
