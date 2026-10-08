# Passes11750–11757: integral anomaly geometry, primitive flux and Lorentzian dynamics

The two constructive advances are an explicit effective quotient fivebrane
cycle with the **integral** Bianchi class, and a primitive E8 frame with
integral torus transition functions. These close particular mathematical
interfaces left open in11742–11749. They do not select a physical vacuum.
The other investigations expose stronger Higgs, metric and volume boundaries.

All files are in `C:\Repos\Theory of Everything`, on the W33 track.
Reservation: `bf6d2f6fb`. Scientific parent:11742–11749,
`9af1eaddfcf0c0233f8eb0a1852f6a2c5fbe571a`; receipt `faf454550`.

| Requested target | Executed result | Physical boundary |
|---|---|---|
| Kinetic metrics and Yukawas | Explicit invariant polynomial, induced metric and bundle-curvature residuals; all four closed global type2 reference forms; large-flux index obstruction | Ricci-flat/HYM/harmonic training and normalized Yukawa integrals remain undone |
| Geometric anomaly and balancing | Named equivariant effective curve; integral quotient descent proved | Backreaction and opposite-charge balancing fields remain absent |
| Light Higgs and proton safety | All-alignment character-rank theorem; supplied adjoint splitting checked against actual proton sources | Cubic route fails; tested deformation still has proton operator |
| Global E8 frame and equations | Primitive tensor frame, signed six-form map, integral transitions, flux-induced radius equations | Full quantum consistency and stationary compactification remain open |
| Lorentzian dynamics and volume | Eight-radius Lorentzian3D gravity, lapse constraint, rolling solutions | No4D gravity, derived fixed volume or vacuum-energy screening |

Additional independent probes are the integral spectral sequence and full
pullback lattice (11755), the conditional splitting experiment (11756), and
the geometric balancing inventory (11757).

## Prior ownership and search

The actual E8 bracket is11681; the projected3875 tensor is11732/11734;
the signed E6 cubic is11271/11636 and11741. The particular three-mode
quotient and its nonzero cup are11742. The factor7 local frame,
equal-VEV Higgs/proton obstruction, effective rational cover class and
kinetic nonidentifiability are11743/11747–11749. Those are used directly,
not advertised as new. Per Continuity decision-a74edb18, the prior report
deliberately retained the geometric and physical boundaries.

Searched `RESULTS_INDEX.md`, `TOPICAL_ALIASES.md`, `docs/index.html`,
`w33_paper.tex`, recent reports, Python producers and certificate vocabulary
for the result formulas and their variants: primitive six/seven-form flux,
Cartan–Leray, `(4,0,2,2,0,4)`, genus5-to-genus2, all-alignment ranks,
`R^-30`, HYM and sliding singlets. The translation-coinvariant work11560
explicitly warns against applying free-action descent to its nonfree action;
the present CY action is free. No priority claim over the mathematical
literature is made for spectral sequences, Chevalley integrality, flux
reduction or doublet-triplet mechanisms.

## 11750 — a real metric calculation, with its failures measured

Use the prior bundle

```
K1=(-2,1,1,0), K2=(0,-3,0,1), K3=(2,2,-1,-1)
```

on the tetraquadric, with the exact positive zero-slope Kähler point
from11742. Let `q=(1+z²,1-z²,2z)` on each projective factor. The21
products with trivial total Klein-four character form the invariant
hypersurface system. A named numeric snapshot assigns the first21 primes
in lexicographic section order. Its complete affine polynomial and
coefficients are in the certificate. Simultaneous sign and reciprocal
invariance are checked exactly.

At two explicitly recorded hypersurface points, evaluate the induced
ambient Fubini–Study metric. With `h_i=t_i/(1+|z_i|²)²` and `F_i=partial_i F`,
the residue volume comparison is

```
eta = det(g_induced) |F_3|² = (product_i h_i) sum_i |F_i|²/h_i.
```

The determinant lemma proves this expression is independent of which
coordinate is eliminated. An independent test checks all four choices.
The two computed densities differ by a factor **5.8714743894**; local
bundle-curvature contractions are also nonzero. Thus these reference
objects fail the constant-density Monge–Ampère and HYM targets. Variation
of density alone is not presented as a local Ricci-tensor calculation. The numeric snapshot's
global smoothness is not certified; the generic smooth/free family
existence is the earlier theorem. No global mass integral uses this snapshot.

The physical calculation requires a Ricci-flat correction, three HYM
metrics, closed harmonic representatives including a type2 lift, and
volume-normalized kinetic integrals. The paper and authors' implementation
provide an actual computational route for tetraquadric line bundles:
[Constantin et al.,2402.01615](https://arxiv.org/abs/2402.01615),
[heteroticyukawas](https://github.com/kitft/heteroticyukawas).
In this bundle, `K3` has no ambient cohomology and its four modes arise
from `H²(A,K3-D)`: treating it as a restricted ambient harmonic1-form
would feed the wrong object into the solver. The extension below supplies
the missing closed input; training has **not** run here.

Write `kappa=1+z*barz`. Six global primitives, with columns p=0,1
and rows k=0,1,2, are

```
u_kp = 1/(2 kappa^2) *
 [[barz*(2+z*barz), barz^2],
  [-1,                 z*barz^2],
  [-z,                -(1+2*z*barz)]].
```

They obey `dbar u_kp=z^k barz^p/kappa^3 dbarz`. Under the south chart
their O(-1) section coefficients transform to `-u_(2-k,1-p)` and remain
smooth. This is an implementation of the published primitives in
[Blesneag et al.,1512.05322,eqs3.22/5.28–5.29](https://arxiv.org/abs/1512.05322),
not a new integration formula.

For `F=sum_(k=0)^2 f_k(z0,z1,z3) z2^k`, set

```
nu_pq = sum_k f_k u_kp(z2,barz2) * barz3^q/(1+z3*barz3)^3 dbarz3.
```

Exactly, `dbar nu_pq=F omega_pq`. Restricting to X gives four closed
reference forms representing the four independent connecting-map classes.
Full rational pullbacks under g and h are checked: g gives
`(-1)^(p+q)nu_pq` and h gives `nu_(1-p,1-q)`. Thus `nu_00+nu_11`
is an explicit invariant mode. These are global reference forms, **not
harmonic** forms for an uncomputed Ricci-flat/HYM metric.
For the trace convention `(2pi i)^-1 integral dz wedge nu`, each displayed
H1(O(-3)) basis pairs as `-I/2` with `(1,z)`. Two factors pair as `I/4`;
the unit-Serre connecting basis is therefore `4 nu_pq`. An independent
radial-integral test checks this factor before it can enter normalization.

Another potential shortcut was checked rather than assumed.
[Blesneag's thesis2204.01165](https://arxiv.org/abs/2204.01165) treats
localization at large internal flux. Uniformly replacing `K_i` by `ell K_i`
gives total quotient Riemann–Roch index `-3 ell³`, since their sum vanishes.
Only positive integer `ell=1` preserves this three-generation index.
This rules out that specific large-flux shortcut, not other bundle designs.

## 11751 — an explicit effective quotient fivebrane cycle

Order pair classes as `01,02,03,12,13,23`. Prior11748 gave

```
b=c2(TX)-c2(V)=(6,0,2,3,-1,5),
r=(1,-1,0,0,-1,1)=0 in H4(X,Q),
b-r=(5,1,2,3,0,4).
```

An effective cover class alone did not construct a quotient cycle. Here
we name one. Define the invariant graph surface by

```
D01: u0*u1+v0*v1=0,
D02: u0*u2+v0*v2=0.
```

It is `P1 x P1`, with
`[u1:v1]=[u2:v2]=[-v0:u0]`; factor3 is free. Its intersection `C`
with a generic invariant tetraquadric has bidegree `(6,2)` and class

```
[C]=(J0+J1)(J0+J2)=(1,1,0,1,0,0).
```

The restricted invariant system is basepoint-free. Bertini gives a smooth
curve; ampleness gives connectedness. Adjunction gives genus5. The
ambient action preserves the graph, and the free action on X restricts
freely to C. Riemann–Hurwitz gives genus2 on `C/Gamma`.

For any pair `i,j`, fix both factors to `[1:0]` and include its h-image
with both `[0:1]`. Each component is a residual `(2,2)` elliptic curve.
Its g-stabilizer acts freely because X is free. The invariant two-component
union descends to one elliptic curve with pullback class `2 Ji Jj`.
Use these orbit pairs with multiplicities2,1,1,2 for pairs01,03,12,23.
The resulting effective cycle has pullback

```
[C]+2(2 J0J1+J0J3+J1J2+2 J2J3)
 = (5,1,2,3,0,4)=b-r.
```

These smoothness/freeness conditions can be imposed on one common generic
invariant hypersurface: each is a nonempty open condition. Repeated
components are allowed effective-cycle multiplicities. There is no division
of an averaged cycle by four. Degrees against the descended `O_X(2Ji)`
are `(7,7,7,9)`; `O_X(Ji)` itself does not descend.

11755 proves integral pullback injectivity. Hence this cycle is exactly
`c2(TY)-c2(VY)` in **integral** H4 of `Y=X/Gamma`, with trivial second E8
bundle. Holomorphic fivebrane support closes this topological anomaly
condition. It does not solve the differential Bianchi identity, corrected
HYM equations or fivebrane backreaction.

## 11752 — alignment cannot repair the cubic Higgs ranks

Allow all six complex singlet VEV components `S_k=(s_k,t_k)`.
In a fixed SU5 gauge component the5-to-two-bar5 family mass is3-by6:

```
M_ij=c_k t_k, M_i,j+3=-c_k s_k (i!=j, {i,j,k}={0,1,2});
M_ii=M_i,i+3=0.
```

The actual signed27 cubic independently checks the two singlets' epsilon
pairing. For each character, the prior exact cup gives `c_k=+-1/2`.
Put `epsilon_k=2c_k`,

```
d0²=epsilon1 epsilon2/epsilon0,
d1=epsilon2/d0, d2=epsilon1/d0.
```

Then `d_i d_j=epsilon_k`, and exactly as a polynomial in all six VEVs,

```
M_chi=diag(d0,d1,d2) M_++ diag(d0,d1,d2,d0,d1,d2).
```

Both diagonal factors are invertible phases. Every character sector has
the same rank **for every alignment**, including rank-deficient loci.
Therefore lifting all colored5s by this cubic also lifts all weak5s.
This is stronger than the earlier equal-VEV check. It is a theorem about
this inventory and linearization, not all E6 model building.

## 11753 — primitive E8 flux and integral global transitions

Use the actual prior tensor `T`, section `S_i=A_3i`, and roots `R_i`
from its seven symmetric terms. For each nonzero `R_i` individually,
the following identity holds on every one of248 generators:

```
B(S_i,a)R_i+[S_i,[R_i,a]]+B(R_i,a)S_i = Tsharp(a).
```

There are **1736** exact basis checks. The ancillary term is
`Sigma_a sharp=-B(R_i,a)S_i`; it remains section-constrained and constant.
The prior closure argument applies with a single derivative term, yielding
`L_(E_a,Sigma_a) E_b=exp(ad C_i)[Tsharp(a),b]` for `C_i=y_i R_i`.
The factor7 in the earlier summed potential is not a minimal flux quantum.

To establish the physical form dictionary, use the eight coordinates
`P=(0,1,2,4,5,6,7,8)` and oriented `Omega8`. Set
`alpha7=i_1 Omega8`, `beta_i=i_i alpha7`. The antisymmetric generator
`J_ab=sign(3,a,b) x_sorted(3,a,b)` maps to `-i_b i_a Omega8`.
This gives `R_i=-J_1i -> beta_i`. The producer checks every root against
all56 off-diagonal SL8 generators: **1568** exact six-form covariance
checks, in addition to the seven contraction signs.

The potential `C6_i=n y_i beta_i` has `F7=n alpha7`. Different choices
satisfy

```
C6_i-C6_j=d(n y_i y_j i_j i_i alpha7).
```

On a unit torus, crossing `y_i -> y_i+1` adds the closed integral form
`n beta_i`. These are classical six-form gerbe patches.

The integral lattice is explicitly built from240 root vectors and eight
simple coroots, obtained from the indecomposable positive actual roots.
Their Gram determinant is1. `exp(+-ad R_i)` terminates at degree2 and
maps every lattice basis vector integrally; **3472** forward/inverse
checks prove both directions. Integer powers give integral flux n.
The transition generators commute and preserve the section and ancillaries.
This checks adjoint-lattice integrality and classical global patching; it
does not establish all quantum M-theory conditions or a stationary vacuum.

The generalized/ancillary and form-patching framework is established prior
theory: [Inverso–Rovere,2410.14520](https://arxiv.org/abs/2410.14520),
especially sections2.4,3.5 and appendixB. The particular root dictionary,
primitive identity and integral transitions are the present computation.

## 11754 — the primitive flux produces rolling Lorentzian volume

Keep all eight torus radii `R_i=exp(lambda_i)`. The flux singles out
coordinate1, so an isotropic-only ansatz cannot silently be treated as a
consistent truncation. Use

```
ds11²=exp(-2 sum lambda_i) ds3_E² + sum_i exp(2lambda_i)dy_i²,
S3=(1/(2 kappa3²)) integral sqrt(-g)[R-Gij d lambda_i d lambda_j-U],
G=I8+ones(8), G^-1=I8-ones(8)/9.
```

The Weyl measure contributes `exp(-2 sum lambda)`. Seven inverse internal
metrics contribute `exp(-2 sum_(i!=1) lambda_i)`. Thus

```
U=A n² exp(-2lambda_1-4 sum_(i!=1)lambda_i), A>0.
```

Every logarithmic-radius derivative is negative for nonzero flux. There
is no finite-radius stationary vacuum in this bare flat-torus sector.
On the isotropic restriction, `U~R^-30`; `phi=12 log R` puts the kinetic
term at `-1/2(dphi)²` **inside the displayed action**. This normalization
must not be confused with an action having Einstein term R/2.

For flat2-space FRW, lapse variation gives

```
2H²=v^T G v+U,
Hdot=-v^T G v,
lambda_ddot=-2Hv-(1/2)G^-1 grad U.
```

The canonical lapse Hamiltonian is
`N[-p_a²/8+p_lambda^T G^-1 p_lambda/(4a²)+a²U]=0`.
For flux exponent vector `k=(4,2,4,4,4,4,4,4)`, `k^T G^-1 k=16`.
The formal nonzero-potential flat-FRW power law would require
`p=1/4,U0=-1/8`, incompatible with positive flux energy; this does not
exclude kinetic-dominated rolling solutions.

Two such finite-time solutions are explicitly integrated from equal
zero initial radius velocities and the appropriate lapse constraint.
With A=n=1, initial unit volume, and t from0 to1, final volume is
**1.4635850292**. Adding the diagnostic higher-dimensional vacuum term
`C exp(-2 sum lambda)` with C=1 changes it to **1.6572239802**.
Maximum constraint residuals are below `1.6e-10`. C changes the initial
Hubble rate as required by the constraint; it is not an extra allowed
cosmological term in supersymmetric11D supergravity. It tests sensitivity
to additional vacuum contributions, not a new11D theory.

This is supplied Lorentzian3D gravity with dynamical geometric volume,
not occupation-number volume. The common shift affects its forces;
fixed-N cancellation from11746 does not imply gravitational screening.
The classical distinction between rolling and stationary flux reductions
is also discussed in [Andriot–Cribiori–Van Riet,2504.08634](https://arxiv.org/abs/2504.08634).
No4D cosmology, stabilization, observable Lambda or entropy-bound result
is inferred here.

## 11755 — remove the integral-descent ambiguity

Let `Y=X/Gamma` for the specific free diagonal Klein-four action.
Lefschetz gives `pi1(X)=0` and integral homological `H2(X)=Z4`.
The universal coefficient theorem then makes cohomological H3(X)
torsion-free. The action on H2(X) is trivial.

The lifts of `O(J_i)` anticommute. For `g=(a,b),h=(c,d)`, their projective
cocycle is `(-1)^(bc)`. All64 cocycle identities are checked. It is not
a coboundary: coboundaries on an abelian group are symmetric, whereas this
cocycle has commutator-1. A tensor of the two periodic integral C2
resolutions independently computes `H2(Gamma,Z)=C2`, hence
`H3(Gamma,Z)=C2` by UCT.

The Cartan–Leray transgression from invariant H2(X) to H3(Gamma,Z)
is precisely the equivariant line-bundle obstruction:

```
d3(n0,n1,n2,n3)=sum_i n_i mod2.
```

It is surjective. The degree-three filtration terms `(3,0),(2,1),(1,2)`
are consequently zero: respectively killed by d3, H1(X)=0, and
`Hom(Gamma,Z4)=0`. The remaining `(0,3)` term is a subgroup of the free
H3(X); there are no incoming differentials. Therefore H3(Y) is free.
UCT implies homological H2(Y) is torsion-free, and six-dimensional
Poincaré duality implies cohomological H4(Y) is torsion-free. Transfer
annihilates the kernel of pullback by4, so H4 pullback is injective.

We can determine its entire image, not only its kernel. The free Picard
pullback is the index2 lattice `L={n in Z4:sum n even}`. Perfect integral
Poincaré pairing downstairs gives

```
pi*H4(Y,Z)=4 L_dual
 ={a in Z4: all a_i even and all a_i congruent modulo4}
```

in the upstairs integral J-pairing coordinates. This lattice has index
**128**, with basis `(2,2,2,2),4e0,4e1,4e2`. The actual budget
`(14,14,14,18)` has coordinates `(9,-1,-1,-1)` in that basis.
Integral equality of the11751 pullbacks therefore gives integral equality
downstairs, with no unnoticed torsion remainder.

The projective-versus-equivariant distinction is standard; see
[Braun,1003.3235,section4.1](https://arxiv.org/abs/1003.3235).
The spectral-sequence deduction above is for this action and is not a
general statement about CY quotient Brauer groups.

## 11756 — try an actual algebraic way around the Higgs theorem

Supply an additional SU5-adjoint family-selective operator, leading to

```
M(y)=1/2 [[0,1-y/3,1],[1-y/3,0,1],[1,1,0]],
Y6=diag(-2,-2,-2,3,3).
```

At weak weight y=3 the rank is2, with nullvector `(-1,1,0)`.
At color weight y=-2 the rank is3. This is a conditional5/bar5 Higgs-pair
escape, using a tuned coupling absent from the certified cubic.
`H1(X,O)=0` also prevents simply assuming a massless adjoint chiral field.

Reusing the **actual signed-root linear sources** from11747 and replacing
only the massive color block still gives `W_eff=-abcd/4` for the prior
`Uc_0 Ec_1 Uc_2 Dc_0` component. Splitting the weak pair has not removed
the proton operator in this experiment.

Adjoint tuning and sliding singlets are prior methods, including E6
extensions: [Maekawa–Yamashita,hep-ph/0305116](https://arxiv.org/abs/hep-ph/0305116).
The result here is a tested conditional deformation and its failure to
solve both requirements, not a new protected GUT mechanism.

## 11757 — anomaly support does not manufacture the balancing fields

The visible-SU5-singlet part of the E8 adjoint is the hidden24, branching
under the selected SU3 family and SU2 factors as

```
24=(8,1)_0+(1,3)_0+(1,1)_0+(3,2)_{+5}+(bar3,2)_{-5}.
```

The nonzero-X sectors carry K_i and K_i dual. Their H1 dimensions are
4 and0 per line on the cover, hence24 and0 including the SU2 doublet;
on the quotient they are6 and0. The family-neutral nonzero-X count is0.
The family-neutral P,Q of11745 thus cannot be claimed as elementary
zero modes of this geometry. Adding the holomorphic fivebrane cycle
closes the topological anomaly condition but does not by itself supply
those fields. Fivebrane worldvolume dynamics, bundle deformations and
nonperturbative sectors require separate objects and calculations.

## Reproduction and interpretation

Producer: `analysis/w33_pass11750_11757_integral_geometry_and_flux_dynamics.py`.
Certificate: `data/w33_pass11750_11757_integral_geometry_and_flux_dynamics.json`.
Independent regressions:
`tests/test_w33_pass11750_11757_integral_geometry_and_flux_dynamics.py`.
Run with `OPENBLAS_NUM_THREADS=1 python3`; source hashes normalize CRLF.

Final local validation:26 new regressions plus25 previous-interface regressions,
**51 passed in147.44s**; all eight producer sections PASS. Four-file corpus
intake is clean, with no collisions or forced arithmetic. Exact-commit hosted
replay and publication receipts are recorded separately after execution.
A PASS certificate means
the stated identities and controls passed. It does not convert an open
metric calculation, conditional EFT, rolling3D reduction or topological
anomaly condition into a solved theory of everything.
