# Passes11786–11793: certified spectrum, a transition-field limit and the gravity source test

All five requested directions were executed as explicit mathematical investigations. The strongest conclusions are a rational **ground-energy upper bound `E0 < 127.595533`**, a named dynamics-preserving selected-transition construction of a free local field, and the exact failure of the existing Gaussian Lorentzian lift to satisfy **vacuum Einstein equations for any cosmological constant**. An additional investigation constructs a primitive full-field **order-four charge action whose light-field quotient is matter parity**, despite the absence of a suitable global order-two character. None establishes a complete TOE, an F-flat realistic vacuum, observed particle masses, a numerical spectral gap, or the full current-Dirac index.

## Intake and ownership

Original Theory of Everything checkout; reservation `485bfa609`. Remote changes through `4dcb27d3c`, especially science `6ab13216a`, were read before computing. The parallel track owns the nine-state trial, single-pair curvature bound, full fifteen-model heterotic fixture and Wilson sieve, eighth-moment optical correction, and arbitrary-dimensional product heat kernel. Its additional local files were left untouched. `RESULTS_INDEX.md`, recent reports/certificates, `docs/index.html`, the paper and its actual open-problem epilogue were searched by formulas and results before novelty claims.

Prior inputs:

- `w33_pass11769_quantized_current_vacuum.py`: actual currents/Hamiltonian, Gaussian, analytic two-state span.
- `w33_pass11775_symmetric_non_gaussian_vacuum.py`: **correct** point/line covariance and derivative signs; three-state quartic trial.
- `w33_pass11778_11783_compact_vacuum_thermodynamics.py`: compact resolvent, attained positive finite ground sector and qualitative gap.
- `w33_pass11781_11784_11785_nonlinear_cone_bargmann_lift.py`: nonlinear Gaussian kinetic metric, magnetic curvature, standard Lorentzian lift.
- `w33_20261009_9state_ritz.py`: parallel nine-state basis, orbit reduction and floating trial calculation.
- `w33_20261009_curvature_perturbation.py`: parallel single-pair relative form bound.

**Intake conflict found:** the later5/7/9-state block applies the point/line sign to both momentum covariance and polynomial derivative. Only the position covariance has that sign. The older11775 producer already has the correct convention. The old floating nine-state value `127.595518296517` is therefore superseded as a claimed bound for the named Hamiltonian. This packet preserves the earlier files and supplies an explicit independent audit; editorial treatment of the earlier report was surfaced to the user. Initial working11786 output repeated that mistake, was withdrawn, and is replaced by the corrected certificate. A second quadrature rule did not catch it because both rules integrated the same wrong polynomial.

**Concurrent intake:** while this packet was tested, `3fdef4a22` and scope correction `a1f780d38` reached master. Their eleven-state extension inherits the same reduced line-sign issue, so its numerical upper bound and min–max counting values are not adopted here. The independent E8 Weyl/lattice benchmark identification and assignment-aware six-singlet FI support are separate results: `n_1=n_54=n_80=n_82=9/37`, `n_19=n_56=27/74`. The exact source ledger gives charge balance `(-1,0,...,0)` and the old all-label B-L gate has a minimal inconsistent three-row core. That warrants the parallel scope correction, but its own certificate has zero compatible full charge-lattice Z2 characters and does not establish F-flatness or an MSSM vacuum. No old blanket heterotic conclusion is imported into this packet. The joint homodyne, finite-ground response and native Cartesian-power controls were read and kept distinct from the continuum construction here.

Two added independent tests verify the stored six-singlet charge/representation/hypercharge/B-L witness directly over rational numbers, and verify the three-row contradiction. A separate Hermite-normal-form construction of the full rank9 charge lattice exhausts all512 order-two characters and confirms zero compatible survivors. These witness checks avoid importing the cone-search library. Fifteen original full-model raw hashes and the gauge-weight raw-source hash also match their frozen fixtures.

## 1. Certified energies and transition observables —11786

Let `H` be the nonnegative Friedrichs current-square Hamiltonian on `L²(R^78)` already defined in11769. Its quantum energy units are supplied conventions.

The parallel basis consists of the optimized Gaussian and normalized collective point/line Hermite sums of orders2,4,6,8. Their exact norms are

```
N_n = 40(1+12/3^n+27/9^n).
```

Set `X=V_e q`, `Z=U_e C0^-1 q/t`, `Y=w q/sigma`, `sigma=sqrt(108t)`, and `s=+1` on points, `-1` on lines. The full80-coordinate covariance gives

```
Cov(X,Y)=s*t*r/(2sigma),  Cov(Z,Y)=r/(2sigma),
U_e grad(Y)=r/sigma.
```

The last two expressions have no line-side minus sign. These identities are tested on every edge, three markings per side, against the full matrices rather than the reduced formula.

The new producer evaluates every matrix element by the exact Isserlis/Wick recurrence, including every vacuum coupling. It encloses `sqrt10` using integer square roots, isolates the unique stationary `t` with rational endpoint signs, and rounds every arithmetic operation outward on a rational `10^-36` grid. Floating eigenvectors only select rational trial coefficients; the proof is their interval Rayleigh quotient.

The corrected nine-state Rayleigh quotient is approximately `127.59553206`. Its interval is stored verbatim in the certificate, and proves

```
E0 <= R_trial < 127.595533.
```

The interval's lower endpoint is **not a lower bound on E0**. The analytic11769 two-state span independently gives an ordered second-energy upper bound around `161.59063993`, with outward bounds in the JSON. An ordered second eigenvalue need not be the first distinct excitation if the ground sector is degenerate. Neither a numerical full-H lower bound nor a numerical gap is obtained here.

Actual compactness nevertheless supplies exact eigenvectors. Choose T-real `g,e` with `E_e>E0`, and define bounded transitions `S+=|e><g|`, `S-=S+*`. Then `[H,S+]=omega S+`, `omega=E_e-E0>0`. These are named observables; identifying them with experimentally accessible current polynomials is a further task.

## 2. Actual Dirac domain and index controls —11787

For `D=sum_e gamma_e J_e`, the current identity `U=VD` uses the point/line involution, here denoted `D_side` to avoid ambiguity. The differential operator is first order with coefficients at most linear in q. Its propagation speed satisfies

```
c(R) <= sqrt312 (a+sqrt(39/20) R), a=1/sqrt20.
```

The integral of `1/c(R)` diverges. Current divergences vanish because `U_e.V_e=0`. The zeroth-order part is the smooth Hermitian linear potential `a Gamma(Vq)+a² Gamma(1)`; it is unbounded but does not affect propagation speed. The [Chernoff completeness criterion](https://doi.org/10.1016/0022-1236(73)90003-7) therefore makes the full symmetric first-order operator essentially self-adjoint on compactly supported smooth spinors. This settles a domain issue before asking its index.

Its affine linearization is

```
D_lin = a Gamma(V(q+D_side p)) + a² Gamma(1),
D_lin² = a² (q+D_side p)^T(4P_W-Adj)(q+D_side p) + 2/5.
```

The78 quadratures `q+D_side p` commute, and a symplectic metaplectic rotation turns them into multiplication coordinates. The constant vector is perpendicular to `col(V)`. Thus `D_lin` is invertible with inverse norm at most `sqrt(5/2)`. Its graded chiral block has **index0**. The inverse is not compact. This differs from the separately supplied Bott index+1 in11780.

For the full operator the principal symbol loses rank: at the actual classical position `q/a=(39,-1,...,-1;0)` only four current rows survive. This is an exact nonellipticity test, not a proof of non-Fredholmness.

The exact current adjacency degree is6. Summing the parallel one-pair bound on spinor forms gives `|k|<=6h` for the Clifford curvature in `D²=H+k`. The interpolation `h+theta k` is closed and compactly embedded for `|theta|<1/6`. **Actual theta=1 lies outside this band.** Compactness of H does not settle cancellation in D². Full Fredholmness and index remain open; the unbounded quadratic remainder is not a justified Fredholm homotopy.

## 3. A nonlinear action with one front cone —11788

Use the computed variational `G=P^-1,A,Veff` and supply spatial coordinates and `c0>0`:

```
S=integral dt d^d x [G_ij(q)(qdot_i qdot_j
    -c0² sum_a partial_a q_i partial_a q_j)/2
    +A_i(q) qdot_i - Veff(q)].
```

Its principal Euler–Lagrange operator is `G(q)(partial_t²-c0² Delta)`. The characteristic determinant is `det G*(-omega²+c0²|k|²)^78`: all backgrounds have one front cone. This resolves the earlier fixed-gradient cone mismatch by an **explicit additional prescription**, rather than pretending the earlier mismatch disappeared.

The nonzero magnetic term survives below principal order and selects a time direction. A two-field exact control has

```
omega_±(k)=sqrt(c0²k²+m²+B²/4) ± B/2.
```

Both front speeds are c0; for B nonzero these are not relativistic Klein–Gordon mass shells. A common characteristic cone is therefore insufficient for boost invariance. A covariant clock completion would add equations needing an actual solution. Spatial dimension, coordinates and speed are supplied.

## 4. A dynamics-preserving transition-to-field map —11789,11791,11792

At each supplied lattice site replicate M actual cells, restrict each to `span{g,e}`, and take the symmetric Dicke sector. The embedding maps oscillator occupation n to the normalized symmetric n-excitation state. Actual restricted cell dynamics is exactly `omega n`, and

```
I_M* S+ I_M |n> = sqrt((n+1)(M-n)) |n+1>.
```

Supply couplings

```
H_M=omega sum_x(Sz+M/2)
    +(kappa/M)sum_<xy>(Sx(x)-Sx(y))²
    +(r/M)sum_x Sx(x)².
```

As M grows, `Sx/sqrtM -> Q/sqrt2` on every fixed finite-occupation core. The resulting quadratic Hamiltonian has

```
Omega_ell(k)² = omega[omega+r+4kappa sum_a sin(k_a ell/2)²].
```

The weighted ladder error is explicitly `O(N sqrt(N)/M)` and the quadratic core error is `O(1/M)`. Independent two-site matrices test convergence without touching a cutoff boundary. At a fixed finite lattice, self-adjoint core convergence yields strong resolvent and time-evolution convergence; this is a named dynamics-preserving construction, not an abstract Hilbert-space isomorphism. The spin-to-boson method is the established [Holstein–Primakoff construction](https://journals.aps.org/pr/abstract/10.1103/PhysRev.58.1098).

Choose supplied `kappa=c0²/(omega ell²)` and `r=m_phys²/omega-omega`, with `m_phys>0`. The continuum dispersion becomes `m_phys²+c0²|k|²`. The maps

```
phi_x=Q_x/(sqrtomega ell^(d/2)), pi_x=sqrtomega P_x/ell^(d/2)
```

make smeared CCR converge to `i integral f g`. Smooth-test vacuum covariances converge by Fourier/Riemann sums, first on a fixed torus and then in infinite volume. Chosen occupation-truncated quadratic Gaussian states embed through `I_M`; convergence of exact finite-M ground states is not asserted. The causal KG propagator defines the local Weyl net, consistent with the established [free-field/modular localization framework](https://arxiv.org/abs/math-ph/0203021).

Two independent obstructions explain why this extra structure matters:

- T-even current fluctuations in a T-invariant state have zero expected commutator form, so their product-state Gaussian fluctuation algebra is commutative. The explicit T-odd partner `B=i(S+-S-)`, paired with `A=S++S-`, gives `-i<g|[A,B]|g>=2` and repairs the symplectic degeneracy.
- Actual cell energy `H-E0` has a positive excitation gap. A Borchers dilation would scale every positive spectral value arbitrarily near zero, an immediate contradiction. Thus it cannot itself be the nontrivial modular translation generator. In a massive continuum, energy can be gapped while the **lightlike** generator `m exp(-theta)` is gapless and dilates under boosts; see [Araki–Zsido](https://arxiv.org/abs/math/0412061).

This selected-sector free net does not derive dimension3, mass, interactions, all original observables, or a physical universe. Those inputs are enumerated in the certificate.

## 5. Exact curvature and required source —11790,11793

For the existing stationary80D Bargmann lift, `partial_v` is covariantly constant because `g_vA` is constant and coefficients are v-independent. Consequently `Ric_vA=0` globally. At the centered vacuum, `A=F=grad Veff=0`, giving

```
Ric_uu(0) = tr[P0 Hess Veff(0)]
         = alpha tr(16P_W-Adj²) = 960 alpha > 0,
alpha=4[(vx+1/20)(vy+1/20)-4(c+1/20)²].
```

The exact integer trace is960; alpha has a positive rational enclosure. Numerically `alpha≈3.234995418210114`, `Ric_uu≈3105.595601481710` in the supplied variational units. The tidal eigenvalues are `10alpha`48 times and `16alpha`30 times. These recover11771's centered normal frequencies as null-geodesic tidal data; they are not particle-mass predictions.

Vacuum Einstein equations would require `Ric=lambda g`. The uv component forces lambda0, but the uu component is strictly positive. **No cosmological constant can make this lift a vacuum Einstein solution.** For the null vector `L=partial_u+Veff(0)partial_v`, an Einstein equation instead requires

```
T(L,L)=960alpha/(8pi G_N)>0.
```

Neither the scalar-curvature term nor the cosmological term contributes to this null contraction. Other stress components are still uncomputed. Defining a stress tensor as the Einstein tensor is not a derived matter action or coupled gravitational solution.

Independent symbolic controls compute the entire Ricci tensor of a flat magnetic lift: `Ric_uu=2mu+B²/2`; a rotating-flat example cancels it at `mu=-B²/4`. A nonconstant transverse metric checks the critical-point formula separately. The established distinction between an Eisenhart lift and its required gravitational sources is discussed by [Fordy–Galajinsky](https://arxiv.org/abs/1901.03699) and [Cariglia et al.](https://arxiv.org/abs/1605.01932).

## Reproduction and scope

### Additional connection: a larger character can retain light matter parity —11793

The parallel witness supplies a rational continuous B-L covector x with no component along the ledger's anomalous U1 coordinate. On all176 left-chiral fields, `3x.Q` is integral for112 and half-integral for64. Consequently `6x.Q` is integral on the entire field-generated charge lattice, and

```
g(phi)=exp(i*pi*3x.Q_phi)*phi=i^(6x.Q_phi)*phi
```

defines a genuine order-four **field-charge action**. In the canonical integral Hermite-normal-form basis its character is

```
epsilon=(0,4,-30,-12,-22,-8,-17,-29,-9),
epsilon mod4=(0,0,2,0,2,0,3,3,3).
```

Every field pairing is checked against the original rational charges. Multiplicities of charges0,1,2,3 are **68,32,44,32**. The64 odd-charge fields make the full action order4. All thirteen selected matter labels have charge2, while all six condensates have charge0. Candidate Higgs doublets `l_1,bl_1` have charge0; `l_2,l_3,l_4` have charge2 and can be chosen as three lepton labels at the charge level.

On this selected light carrier, g acts as matter odd/Higgs even, while g² acts trivially. Its faithful light image is therefore `Z4/<g²> = Z2`. On the entire field carrier, g² acts nontrivially on the odd exotic charges. **Absence of a global Z2 character does not eliminate this larger action's effective matter-parity quotient.** This explicitly completes the earlier conditional higher-order hint instead of treating the narrower gate as exhaustive. This is a non-R action; it is not the standard `Z4^R` assignment.

The character permits ordinary up/down/lepton Yukawa monomials and a Higgs mu monomial at the charge level, and forbids `udd,LQd,LLe,LHu`. All candidate-family combinations are checked. `QQQL` and `uude` are allowed: **dimension-five proton decay is not excluded**. Charge-permitted monomials are not proved present in the worldsheet superpotential. The distinction between discrete field actions, matter parity and stronger proton symmetries is established prior literature, e.g. [Dreiner–Luhn–Thormeier](https://arxiv.org/abs/hep-ph/0512163); the new content is this exact actual-fixture character.

The continuous B-L gravitational and cubic charge traces vanish exactly. All six condensates are actually continuously B-L neutral. Their full9-coordinate charge rank is6, so **three Abelian Lie directions remain unbroken**; this is not an MSSM gauge vacuum. Exact F-flatness, extra-gauge breaking, vectorlike mass ranks, full axion/global-gauge-group and anomaly completion, and a physical family/Higgs identification remain necessary. No source ledger, prior no-go producer, or main paper was changed.

Five producers write five JSON certificates. The focused test module independently checks covariance signs, rational root/moment enclosures, the older correct three-state block, second-basis symbol bounds, principal actions, Dicke convergence, spatial CCR and dispersion, Ricci sources, rational parallel witnesses and the larger charge character. CI replays all five producers and checks regenerated certificates. Publication/actual hosted evidence is recorded separately in the verification receipt.

The five targets are investigated, not all closed. Missing numerical lower/gap estimates, actual Dirac Fredholmness, physical Lorentz symmetry, selected spacetime/masses, interacting continuum dynamics and self-consistent gravity remain explicit mathematical or physical tasks.
