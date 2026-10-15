# Passes11994–11998: native clock order, full metric coordinates and a joint CP vacuum

Reservation `4cb9f43450b9b919762b1cd3f11f9e0d23337fc6` was pushed before computation.
All five requested targets were investigated. The strongest positive changes are
an exact global clock-order theorem, an exact ten-component native metric chart,
and a jointly stable numerical singlet/flavour scalar vacuum. None closes the
paper's open physical TOE problems. The actual missing dynamical inputs are
identified below rather than replaced by names or dimension counts.

##11994: the native currents supply angular clock order

Use11991's literal135 harmonic edge rows C and primitive lattice L. On the
A-fixed character plane write u=L^T(x,y,0,0). With r=x²+xy+y² the even native
moments are exactly

```
I2 = sum_e (C_e u)^2 = 54r,
I4 = 54r²,
I6 = 54r³ +81x²y²(x+y)².
```

The sextic anisotropy is therefore an explicit native tensor, not a fitted
angular function. Choose the declared H27-invariant Landau potential

`V=(rA-1)²+rB+rB²+(I6-I2³/2916)/81`,

where rA=x²+xy+y² and rB=z²-zt+t² in character coordinates. Every term is
nonnegative. Its complete global zero set is exactly

`(x,y,z,t)=(±1,0,0,0),(0,±1,0,0),(±1,∓1,0,0)`.

All four real Hessian eigenvalues at each point are positive. The six vectors
form two H27 orbits of three, exchanged by time reversal; each has exact
stabilizer A={(0,b,c)}, the actual TOE84/85 rank-selected subgroup. Removing the
sextic term restores a continuous angular vacuum degeneracy, an independent
negative control. This improves11991's example-vector permission to an explicit
conditional global order model.

For each u, use the actual acoustic G to construct

`eta=[G-2 Gu u^T G/(u^T G u)]/(u^T G u)`.

Here u^T G u=2 and u^T eta u=-1; eta has one negative direction in two drawings.
But the kinetic family K_alpha=G-alpha Gu u^T G/(u^T G u) has determinant
`det(K_alpha)/det(G)=1-alpha`. The clock potential does NOT choose alpha>1.
The quotient, relative character masses, Lorentz kinetic sign and physical
interpretation remain supplied. Older10972/10975 clock cubic/Reynolds tensors
act on a different four-clock augmentation; those are prior constructions,
not this135-edge harmonic moment or its six-minimum theorem.

##11995: the native graph supports all ten metric components

With positive edge weights W, recompute the harmonic representative

`h=V-b(b^T W b)^-1 b^T W V`, `G(W)=h^T W h/27`.

Do not keep the old h when varying W. The envelope derivative at unit weights is
`dG_ij/dw_e=h_ei h_ej/27`. Its exact rational rank is10, with active edge indices
`[2,3,4,5,6,7,8,9,29,32]` and determinant

`128/717897987691852588770249`.

Thus the implicit-function theorem gives an OPEN neighborhood of the baseline
four-dimensional metric realized by positive native weights, fixing the other
125 weights. This is an exact local existence theorem; the displayed Newton
solutions are numerical examples. They reproduce the full offdiagonal Q-dependent
Gowdy metric after the stated Euclidean-clock conversion. An independent weighted
Bloch-band refinement checks the acoustic response, beyond fitting a matrix.

For a full metric chart including shift, define E=(R^-1 G(W) R^-T)^-1 and fixed
clock e=(1,0,0,0), then g=E-2 Eee^T E/(e^T E e). This is an involution between
positive E and Lorentz g with e timelike. Consequently a SUPPLIED continuum
Einstein–Hilbert action S_EH[g(W)] is locally a field redefinition of GR on ten
weight fields. It inherits standard constraints/two propagating modes only
because the Einstein action and continuum derivatives were input. Generic
kinetic terms for135 independent weights would not have that property.

Prior11956 owns weighted-harmonic metric matching on a different3D cover,
including a stronger quantitative contraction certificate for its particular
flat target. Prior11992 owns the genuine nonlinear Gowdy benchmark. This new
four-cover metric capacity does not repair11976's finite constraint failure
or derive Einstein gravity, G or Lambda. A dynamical timelike vector also
requires an extra-mode audit: [Jacobson–Mattingly](https://arxiv.org/abs/gr-qc/0402005)
find additional coupled modes in general Einstein-aether theories.

##11996: replace the standalone CP source by an actual singlet composite

The actual11978 soft-singlet model contains S1,S2 with identical charges
X=-1,Z=0. Set `tau=Im(S1 conj(S2))/rho`, rho=1/32. It is gauge invariant and CP
odd. Couple its complete soft singlet potential to11981's three triplets via

`V=Lambda^4 V11978 + vf^4 V11981(x,tau(S))`,

with SUPPLIED Lambda=10^16GeV,vf=10^3GeV. There is no independent tau double well.
A100-digit Newton solve retains all singlet/flavour backreaction. At the root:

- tau=-0.9999999990435755; the largest singlet displacement from11978 is3.60e-20.
- All32 core/flavour gradients, scaled by their respective energy factors,
  are below2.4e-100. The80-digit root and75-digit full32x32 Hessian are stored.
- A positive congruence rescaling gives30 positive modes and exactly2 gauge
  zeros; its smallest positive eigenvalue is6.74e-33. These rescaled eigenvalues
  are NOT physical masses.
- The actual multiplier/spectator blocks contribute14 additional positive
  modes. Restoring13 complex positive-mass flavour mediators gives72 real
  scalar coordinates,70 positive physical modes and2 gauge zeros by completing
  squares. CP-conjugate vacua have identical energy.

This is the11978 soft-mass-only model, not its separate pinned-hidden SUGRA
model. The portal is a nonholomorphic scalar EFT interaction, not a new
supersymmetric superpotential completion. Neither the scale hierarchy nor a
full E6/hidden vacuum or global minimum is derived. The raw flavour texture
has J≈0.0144, not the observed value. The separately matched Barr transmission
uses11951/11989's FITTED real couplings and retains tree determinant positivity.

**Do not stop at scalar stability.** Apply11954's standard neutral-scalar B0
matching to this actual18D flavour Hessian and actual fitted B=C h vertices.
Add a supplied real neutral Higgs fluctuation H with the positive square

`DeltaV=1/2 [5H+(kappa/5)(|h|²-|h0|²)]²`.

It preserves the local scalar minimum. In this explicitly declared19-scalar
non-SUSY slice, kappa=.1 gives theta_one_loop=-1.5463556e-4. Zero portal gives
zero, CP reverses the result, and changing the MSbar scale leaves it unchanged.
The small-kappa slope gives a conditional |kappa|≲6.47e-8 requirement for a
1e-10 phase target. This is not total72-field theta: singlet/mediator/gauge/
colored/SUSY loops and tadpole shifts are omitted, and cancellations are not
excluded. It identifies an actual matching problem rather than asserting
radiative safety from the tree determinant.

The general [E6 Nelson–Barr mechanism](https://arxiv.org/abs/1802.08109) and
[loop analysis](https://arxiv.org/abs/2105.09122) are established literature.
Prior11953 already proves allowed leakage cannot be dismissed by matter parity.

##11997: an exact finite gap and a global gauge-orbit tube frame

For11991's actual finite27-vertex quotient, Q0 is a108-dimensional Hermitian
Gaussian-rational matrix. A rational approximate inverse with grid10^-8 gives
an EXACT integer residual bound below6.05e-6. A proved int64 product bound
precludes overflow. Neumann inversion and Hermiticity imply

`gap(Q0)>=399997583/907801064 > .44`.

For gauge-fixed physical link phases a, the explicit per-edge bound is
`||Q(a)-Q0||<=sum_e (1+sum_i|J_ei|/2)|q a_e|`.
Restrict that sum to g0/16. The entire domain is uniformly gapped; projector
perturbation ensures a single Stiefel chart exists throughout it. Extend over
ALL rooted U1 gauge transformations using periodic tree-link products. This
constructs an explicit gauge-covariant frame on a full gauge-orbit tube, not
just one numerically selected gauge orbit. All six integer SM charges,
arbitrarily large gauge phases,2pi windings and a three-chart cocycle are tested.
The multiplet is supplied; three families are not selected.

**The frame is nonlocal:** tree products depend on long root paths. Therefore
it does not satisfy the spatial locality requirement of a physical chiral
measure. Only the finite-cell weak-cycle tube is covered, not all Blochmomenta,
nonzero topology or non-Abelian configurations. A global section on this tube
is not a completed native4D chiral continuum. Prior11429 owns the Stiefel
method and nonzero anomaly-free curvature;11443/11462 own the earlier gauge-
orbit/flux-patch boundaries. [Luscher's construction](https://arxiv.org/abs/hep-lat/9811032)
requires substantially more than the finite section constructed here.

##11998: preserving a family triplet changes the native gate controls

Use11988's actual atlas J, not an arbitrary complex structure on R6. Exact
linear algebra splits so6 into a9-dimensional centralizer u3 and a6-dimensional
anticommuting complement. For J=Jn/sqrt3:

`A_keep=(A-JAJ)/2=(A-Jn A Jn/3)/2`.

For each actual11987 even gate rotation R, the complex-linear part
K=(R-JRJ)/2 is nonsingular. Its polar factor gives an explicit closest U3
transport. Lifting these modified rotations to the actual spinor four-space
preserves a1+3 decomposition. The computed charge spectrum is
approximately -3/2,+1/2,+1/2,+1/2, as in the standard Spin6 branching. Native
singlet-to-triplet probabilities numerically equal0,3/4,3/4,9/16,9/16; after the reduction they vanish numerically.

A supplied penalty kappa||RJ-JR||² has zero set U3 and positive quadratic cost
on exactly six infinitesimal directions. It changes the connection; it is not
an identification of the original connection with a complex-linear one.
The reduced spinor library is therefore not dense in SU4. These same six
pairing directions are necessary controls in the Majorana interpretation.
A charged family triplet and an unbroken full gate algebra cannot both be
assigned to this identical U3-reduced connection without extra controlled
symmetry breaking. A particle/hole Bogoliubov interpretation remains an
alternative mathematical model, not proof of physical family charges.
Prior11987/11988/11993 own the gates, tangent map, obstruction and Fock carrier.

## Checks, ownership and remaining scientific target

Searches compared exact identities, coefficients and determinants against the
result index, analysis sources, JSON certificates, docs/index.html and the
current physics/epilogue paper. The clock Reynolds and prior weighted metric,
scalar-loop and determinant-line constructions are cited above. This is an
application/extension packet, not a novelty claim for Landau theory, harmonic
homogenization, the implicit-function theorem, GR field redefinitions,
Nelson–Barr, Stiefel sections, polar decomposition or Spin6 branching.

Five producers, independent regressions and a frozen/regenerated hosted workflow
are provided. Actual test outcomes and publication hashes are recorded in the
receipt. Papers are unchanged. A common microscopic action selecting signature,
Einstein dynamics and local chiral matter; a full E6 flavour vacuum; radiatively
protected total strong CP; and observed parameter predictions remain open.
