# Native scalar response with temporal Gauss constraints and optical relaxation

The previous four-holonomy scalar-loop calculation now extends to all 135 native edge coordinates at zero external deck momentum. The new calculation retains 26 nonconstant temporal density variables, removes them by the Gauss Schur complement, and then allows all 105 optical coordinates to relax. It is a tree-gauge plus scalar-one-loop quadratic model with supplied couplings and compactification. It does not solve the TOE or establish an interacting gauge continuum.

The significant action check is exact: equal coefficients on the previously selected 105 independent face boundaries break 26 of the 27 left-H27 controller actions. Equal coefficients on all 1,287 short zero-integer-voltage faces preserve all 27. These are different magnetic Hessians with the same rank-105 rowspace. A basis of constraints is not automatically a symmetry-invariant choice of physical couplings.

## Provenance and reading

The native graph, four periods, harmonic representatives, face enumeration and ranks belong to the prior October 23/27 face-module work and Pass 11991. The prior full-band scalar potential and coupled response supply the scalar action and spectral conventions: [full-band report](2026-11-08_native_fullband_scalar_holonomy.md), [coupled report](2026-11-08_coupled_holonomy_dynamic_response.md). The October 27 acoustic-density source already contains native thermal-fermion density and Ward calculations. Temporal vertices, Schur complements and Ward identities are standard methods; this packet applies them to the full native scalar edge response and audits the magnetic action choice.

Targeted searches covered analysis Python/Markdown, data JSON, the result index, and prior face/density sources. Selected quotient/Ward and coalescence matches concern different operators; absence of a targeted hit is not a priority claim. Earlier weekly and concurrent batches remain incompletely read. No incoming commit after baseline `29d473868c17166a0417345c24d41efd7b2efa25` was observed at initial intake; the publication receipt records the final fetch.

Manuscript pages 119–120 were read in full as extracted text: finite two-qutrit/Kähler/Weil and Wilson-line claims, then flavour degeneracy and theta-zero constraints. Personal cumulative text coverage is pages 1–120 of 215, not the entire PDF. No new visual-page inspection or independent proof of those manuscript claims is asserted.

Primary literature consulted: [Meurice, discrete aspects of continuous symmetries](https://arxiv.org/html/2003.10986v2), selected local-gauge/temporal-fixing sections; [Dütsch, Peters and Rehren, scalar-QED Master Ward identity](https://arxiv.org/abs/2008.08514), abstract only; [one-loop Lorentz-violating scalar QED](https://arxiv.org/html/2606.23523v1), selected Appendix B ordinary minimal bubble/seagull cancellation. No nonminimal or Lorentz-violating model is imported, and no whole-paper reading is claimed. These provide context for standard contact terms, not numerical inputs or a proof of this graph model.

## Independent temporal vertices

For oscillator frequencies a,b>0, p=a+b and Euclidean external frequency nu, direct frequency integration gives

```
I0 = p / (2ab (p²+nu²))
I1 = (b-a) nu / (2ab (p²+nu²))
I2 = p (4ab+nu²) / (2ab (p²+nu²))
contact - I2 = (a-b)² p / (2ab (p²+nu²)), contact=p/(2ab).
```

The density vertex is constructed directly as U†diag(Q)U for a zero-mean orthonormal vertex basis Q. The literal edge-current vertex separately obeys J(B chi)=i[H,chi]. It is not defined from the desired Ward result. The full 161-by-161 scalar-loop kernel, including mixed current-density terms and the temporal contact, annihilates all 26 gauge vectors. Omitting that contact provides a failing control. The uniform temporal mode is redundant in the neutral vacuum and its density response separately vanishes numerically.

Actual server-side V8 Simpson integration with 65,536 panels checks I0/I1/I2 to below 3e-15 on the selected examples. Independent 35-digit mpmath integrals in the tests cover three frequencies and all three numerators. The server also checks a generic nested Schur/profile transformation, not a separate native-135-edge replay.

## Two reductions and their meaning

Use spatial coordinates (4 harmonic,105 coexact,26 gradient). With E(s)=Ebare+Z(s), eliminate the 26 temporal variables:

```
Ephysical = E_PP - E_PL E_LL^-1 E_LP
Fphysical(s) = Kloop_PP + Kmag_PP - s Ephysical(s).
```

Below the optical gap, a second Schur complement eliminates the 105 coexact modes. Changing a spatial representative by a gradient changes the fixed-A0 answer but leaves the Gauss-reduced kernel invariant. Tests reconstruct the constrained full spatial equations from the reduced root, check temporal/optical basis changes, and compare analytic slopes against finite differences.

For the harmonic four-coordinate restriction, 0 <= Zeffective <= Zclamped. Consequently the fixed-A0 roots are no larger than the Gauss-only roots, which are no larger than the tree roots in the tested subthreshold range. Optical relaxation lowers the roots relative to the Gauss-only restriction. Their net shift relative to the earlier clamped model is not assigned a universal sign.

The positive spectral Gram representation permits Z(s)=Z0+s Z1+s² Z2 plus a positive remainder bounded by q³/(1-q) Z0, q=s/(4m²). Every reported low root is also evaluated with the unexpanded spectral kernel. Residual-derived mass-squared bounds and unreduced moment bounds are recorded; they do not certify floating-point roundoff. Residues use both Schur derivatives.

## Magnetic action sensitivity

Both prescriptions use the same native edge space and face orientations. The all-face matrix annihilates incidence and period columns exactly; every selected face occurs in it up to orientation. The prior independent rank-105 certificate plus containment establishes the same rowspace. Signed edge permutations explicitly check every H27 controller with integer arithmetic:

| Magnetic prescription | Faces | Maximum exact symmetry error | Broken controllers |
|---|---:|---:|---:|
| Independent basis, unit weights | 105 | 15 | 26 |
| All short faces, unit weights | 1287 | 0 | 0 |

At torus sizes (2,2,2,2), m=0.8 and g=1, the basis prescription gives the first two squared frequencies approximately 0.0008759168895 and 0.0008759179873. The all-face prescription gives approximately 0.00087591831575 for both. The second pair is approximately 0.00090172752072. The full JSON contains both couplings g=0.5,1 and sizes (2,2,2,2),(3,3,3,2), Ward residuals, metric corrections, root checks and residues.

The small basis-induced splitting is an action sensitivity, not an observed particle splitting. All-face unit weights are also supplied physical couplings; no unique weighting across triangles, quadrilaterals and pentagons has been derived. In particular, the all-face prescription has not been shown to preserve the earlier engineered nonzero-momentum common propagation cone. Zero-momentum symmetry and a common continuum cone must be tested together.

## Verification and remaining boundary

The new suite contains 25 cases. The final frozen validation regenerates the producer and runs those with the prior 22 coupled-response cases; the validation JSON records commands, results and unchanged selected source/input hashes. The publication manifest preserves earlier numerical parents and unrelated dirty fixtures. Repository-wide guard failures/timeouts, if any, remain explicit in that manifest; local scientific tests do not imply a green repository or hosted CI.

This calculation includes all scalar bands and local unit-cell Gauss constraints at zero external deck momentum. It still assumes continuous time, scalar mass, torus sizes, gauge coupling and magnetic weights. Higher gauge loops, a charged fermionic Hamiltonian and anomaly-complete matter, nonzero external momentum, physical units, radius dynamics, a selected 3+1 continuum and observational tests remain unresolved. It is a sharper finite-model result and an action-selection obstruction, not a completed fundamental theory.
