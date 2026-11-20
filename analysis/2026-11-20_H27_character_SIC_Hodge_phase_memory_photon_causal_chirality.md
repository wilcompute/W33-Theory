# Six exact physical-consistency gates for the W33/TOE program

**2026-11-20 research continuation | baseline `8e862155995bf9e7423ba8bffcbe42e0d2b658a5`**

The code and tests in this packet distinguish **new finite statements proved/verified here**, **classical mathematics reused as a constraint**, **experimental-model assumptions**, and **unresolved physical conjectures**. Nothing below establishes a Theory of Everything, a complete E8 UV Higgs sector, a 4D chiral compactification, a laboratory Holonet, or a beyond-standard-quantum-mechanics prediction. No earlier research report was overwritten. Previous precise work is in `analysis/2026-11-19_H27_orbit_SIC_qutrit_noise_G2_SU3_twirls_causal_arrow.md`, `analysis/2026-11-19_five_deep_TOE_gates_SIC_gauge_poset_memory_SU3.md`, and `analysis/2026-11-19_native_qutrit_memory_Welch_G2_real_causal_dual_SU3_calibration.md`.

## 1. MAIN ADVANCE — 19 *equivariant Fourier baryons* give an H27-symmetric, locally massive, anomaly-free SU3 SIC gauge toy

The prior 19 arbitrarily selected coordinate baryons were not H27-translation-closed; demanding a **set of coordinate baryons** to be translation-closed required 27 and introduced eight surplus linear multiplier modes. That result did not rule out 19-dimensional **invariant linear combinations**. This pass constructs them.

Define nine color triplets with species labels `(a,b) in F3²`, `i=3b+a`, and use the unnormalized Hesse SIC vacuum

```
Q*_(a,b) = X^b Z^a (1,-1,0)^T,   X^3=Z^3=I,   ZX=omega XZ,
omega^3=1,  omega!=1.
```

The finite flavor transformation on the *fundamental fields* is

```
T_(u,v) Q_(a,b) = omega^(u b) Q_(a+u,b+v).
```

Its projective group law contains the usual Heisenberg central phase. The entire vacuum is transformed by an SU3 color rotation:

```
T_(u,v) Q* = (X^v Z^u) Q*.
```

Both color matrices have determinant one. The resulting action on every `B_ijk=det(Q_i,Q_j,Q_k)` is therefore well defined on the nine-element *abelian translation quotient* because the central omega phase cubed is one. It is a **monomial action**, NOT merely permutation of species indices: there is an essential cube-root phase on each baryon.

For each character `(r,s) in F3²`, Fourier-average the orbit of one baryon:

```
F_(r,s),t(Q) = sum_(u,v in F3²) omega^(-r u-s v) (T_(u,v) B_t)(Q),
T_(u,v) F_(r,s),t = omega^(r u+s v) F_(r,s),t.
```

At the SIC vacuum, `F_(r,s),t(Q*)=0` for nontrivial characters. In the trivial character, the source values are nonzero allowed invariant constants. No nontrivial character receives an explicitly symmetry-breaking constant.

**Exact differential representation result:** all 84 baryon derivatives form a 19-dimensional row space after factoring the eight complex SL3 gauge-orbit tangent directions. The nine Fourier-character eigenspaces have ranks

```
(r,s):   00  01  02  10  11  12  20  21  22
rank:     3   2   2   2   2   2   2   2   2
```

The producer explicitly selects **19 linearly independent Fourier baryon polynomials** and provides their `(r,s)` and seed-triple labels. Exact arithmetic over `F7`, with the algebraic reduction `omega->2` (`2²+2+1 = 0 mod 7`), gives a nonzero **19×19 determinant equal to 2 mod 7**. Therefore the integral Eisenstein-polynomial determinant is nonzero in characteristic zero. The known eight-dimensional complex gauge tangent space supplies the matching upper rank bound. Complex numerical singular values are supplementary, not the proof of exact rank.

Construct the holomorphic, gauge- and finite-flavor-equivariant superpotential

```
W = sum_(r,s,k) L_(r,s,k) [F_(r,s),k(Q)-b_(r,s),k]
  + sum_(a,b) sum_(j=0)^2 S_(a,b),j [tildeQ_(a,b) . Q_(a+delta_a(j), b+delta_b(j))],
(delta_a,delta_b) in {(0,0),(1,0),(0,1)}.
```

The 19 singlets `L` carry inverse H27 character. The nine anti-triplets `tildeQ` transform with inverse species phase, and the 27 auxiliary singlets `S` transform as the inverse of the relative displacement character. Each of the 27 bilinear anti-triplet contractions then belongs to a *closed* finite-symmetry orbit. The full affine superpotential, including the nonzero trivial-character constants `b=F(Q*)`, is invariant. A full nine-element group covariance test is included for the 19 Fourier sources, the vacuum, and the anti-triplet/singlet couplings. Gauge invariance follows because the baryons are determinants and the mass couplings are fundamental–antifundamental contractions.

At `Q=Q*`, `L=S=tildeQ=0`, all F-terms vanish and `sum_i Q_i Q_i†=6I`, so all SU3 D-terms vanish. The offsets form nine independently invertible 3×3 frames, so the `27x27` anti-triplet/singlet coupling block has full rank. The full **100×100 holomorphic mass Hessian has rank 92**. Its eight zero directions are precisely the complexified SU3 gauge orbit, not leftover singlet multipliers. The gauge cubic anomaly cancels between nine color triplets and nine anti-triplets; the L/S fields are color singlets. Generic nonzero Hessian singular values are controlled by the chosen superpotential couplings/normalizations; they are not predicted particle masses.

**Boundary:** H27-invariance has been achieved for this engineered SU3 gauge toy **without 27 coordinate Lagrange multipliers**, but nothing here proves an E8-invariant microscopic origin. The imposed baryon constants still choose the SIC vacuum; global uniqueness, Kähler metric, quantum-corrected vacuum energy, fermion representation realism, gravitational dynamics, anomalous discrete symmetries and a chiral 4D compactification remain open.

## 2. Genuine three-time qutrit witness: raise robustness and derive a 99% *model-conditional* shot contract

Reuse the **externally established** multi-time witness of Beyer et al. and the repo's three explicit pairwise classical-memory qutrit instruments. Their ideal channels are an initial qutrit replacement channel of strength `gamma`, then full dephasing in computational/Fourier mutually unbiased bases. With independent isotropic depolarizing noise `epsilon` on the two late output channels,

```
W3(epsilon,gamma) = 6*(2 sqrt((1-2epsilon/3)*(epsilon/3)) + epsilon/3) - 2gamma.
```

Critical epsilon values (the witness loses negativity, not necessarily quantum memory):

| gamma | epsilon at W3=0 |
|---:|---:|
| 0.36 | 0.010263207616 |
| 0.75 | 0.042893218813 |
| 1.00 | 0.075049408851 |

**Design implication:** increasing `gamma` to 0.75 buys a 4.29% threshold in this idealized noise model, more than fourfold the earlier gamma=0.36 threshold. At `gamma=.75,epsilon=.01`, `W3=-0.789492939934717`.

For a finite-shot **conditional** demonstration, prepare the first channel on the maximally mixed state and measure `|0>`: a Bernoulli event with `p0=(1+2gamma)/3`. For the late basis eigenstates, measure wrong-basis outcomes, pooled over the two channels and three basis inputs: Bernoulli probability `q=2epsilon/3` **if the depolarizing model is independently verified**. If each population is sampled `N` times with two-sided Hoeffding radius `t=sqrt(log(4/delta)/(2N))`, use

```
p0_lower = p0_hat-t,       q_upper=q_hat+t,
gamma_lower=(3p0_lower-1)/2, epsilon_upper=3q_upper/2,
W3_upper=W3(epsilon_upper,gamma_lower).
```

With `delta=.01`, a conservative **prospective** guarantee that `W3_upper<0` with probability ≥99% *for the stated population parameters and model* follows once `N=30650` per population, **61300 accepted independent trials total**. This incorporates both possible deviations of estimates from their means and the confidence-radius addition; hence it is larger than merely the number of trials that makes an expected witness negative. The seeded 61300-shot simulation gives a negative upper witness. A successful measured demonstration must separately verify channel form, MUB alignment, SPAM, source stability, postselection bias and loss. This Bernoulli certificate is **not device independent or a complete general process-tomography confidence region**.

Source: https://arxiv.org/abs/2611.17268. The dimension-independent witness, its classical-memory hierarchy and the experimental qubit study are external prior art.

## 3. SU3 Wilson readout: full 9-setting Weyl uniformity is *necessary* for arbitrary unknown detector bias

The prior round proved that averaging over all nine qutrit Weyl conjugations removes any **fixed, linear, positive** detector effect. Here is the converse, within the restricted family of Weyl settings. Let nonnegative setting probabilities be `p_ab`, normalized to sum one, and let

```
T_p(eta)=sum_ab p_ab (X^a Z^b)^dag eta (X^a Z^b).
```

This channel maps **every** 3×3 detector matrix `eta` to `(Tr eta/3)I` if and only if all eight nonidentity Weyl-character Fourier coefficients of `p` vanish. Since the finite Fourier matrix on `F3²` is invertible, this holds **if and only if**

```
p_ab=1/9  for each of the nine settings.
```

So within schemes made **only** of Weyl conjugations and one nonnegative probability per setting, *all nine settings and equal effective weights are necessary* for an arbitrary unknown detector. For diagonal detector effects, three cyclic X shifts with uniform weights suffice, but a three-shift average leaves offdiagonal bias. An explicit nondiagonal detector/loop example passes the nine-setting identity and fails the three-setting identity.

If setting-dependent acceptance rates change the effective weights, or gate rotations are imperfect, then for normalized positive `eta`, unitary holonomy `K`, probability variation `p-u`, and worst-case operator-norm gate error `tau`, the absolute character bias is bounded conservatively by

```
|Delta Tr K| <= 3 ||p-u||_1 + 6 tau.
```

This is an **identifiability and calibration constraint**, not a statement about optimal generalized SU3 designs, a functioning multiport, or a dynamical Yang-Mills field.

## 4. Exceptional chirality: round S7 is not a viable untwisted fermion compactification

Established Schrödinger–Lichnerowicz theory gives `D²=nabla*nabla+R/4` on an **untwisted** smooth closed spin manifold. The unit round seven-sphere has scalar curvature `R=42`, so `|lambda_D|>=sqrt(42/4)=sqrt(10.5)>0`. The exact known unit S7 spin-Dirac eigenvalues are

```
lambda = ±(k+7/2),  k=0,1,2,...
multiplicity of EACH sign = 8*binomial(k+6,k).
```

No fermion zero modes exist in this untwisted example. Separately, a finite periodic chiral operator `Q` is square and automatically has `dim ker Q - dim ker Q†=0`; a periodic wall profile cannot create an unpaired finite-dimensional index by counting its sign changes. These are **known geometry/linear-algebra facts**, independently instantiated numerically, not claims of a new index theorem. The scalar-curvature gap does not apply unchanged to twisted gauge bundles or singular spaces, where extra curvature/defect terms appear.

This is consistent with Acharya and Witten's older M-theory observation that smooth G2-holonomy compactifications do not by themselves supply charged chiral four-dimensional matter, requiring appropriate singularities. A round S7 is not G2-holonomy and should not be presented as a substitute for an actual singular G2 solution. Sources: https://arxiv.org/abs/hep-th/0109152 and https://arxiv.org/abs/hep-th/0108165 ; sphere spectrum https://www.math.uni-potsdam.de/fileadmin/user_upload/Prof-Geometrie/Dokumente/Publikationen/sphere.pdf.

## 5. A genuine 3+1D Minkowski causal-sprinkling arrow control

Previous finite examples showed `A3(P)=sum_i(p_i³-f_i³)` is odd under order reversal but not a complete orientation invariant. The new producer makes **320 independent, uniform-volume random sprinklings of 48 events into a 3+1D Minkowski causal diamond**, constructs each exact future-directed causal relation, and then reverses all times. Every one of the 320 arrow statistics reverses sign **exactly**. The sampled single-orientation mean is subject to stochastic fluctuation; the paired original+reversed ensemble mean is identically zero.

The theorem is general: any time-reflection-invariant probability measure on causal orders has zero expectation for a measurable orientation-odd statistic. Samplewise arrow asymmetry does not, on its own, show a thermodynamic arrow or a fundamental irreversible time direction. This remains an exact/in-silico falsifier of **geometry-only orientation claims**, not a causal-set quantum gravity measure or a demonstrated 4D Einstein limit.

## 6. OUTSIDE-BOX — exact W33 protected-Hodge phase-error law

Reuse the rigorously established W33 Levi chain from BT545–BT548. W33 has 40 points, 40 lines, Levi graph 80 vertices/160 flag edges and first Betti number 81. The *signed cycle-space projector* has

```
P = K/160,  K_ef = (-3)^(4-distance(e,f))
(distance in the 160-node Levi flag-line graph),
K^2=160K, rank(P)=81, and P_ee=81/160.
```

The new producer reconstructs the 40-point symplectic GQ, all 40 isotropic lines, all 160 flags, the 4-class line-graph distance shells `(1,6,18,54,81)` and `K²=160K` **with exact integers**. Crucially, `P_ef` is **nonzero for every flag pair e,f**, not just for adjacent edges.

Let `D=diag(e^{i theta_e})` act as independent coherent edge phase errors while the reference cycle projector is *held fixed*. The protected subspace is invariant under D precisely when `DPD†=P`, which requires `e^{i(theta_e-theta_f)}=1` whenever `P_ef !=0`. Since every entry is nonzero,

```
D preserves the entire 81D cycle sector  <=>  all 160 edge phases coincide.
```

For a **single-edge** phase deviation `phi` (all other edges unchanged), define squared total Hodge leakage

```
L(phi)=||(I-P) D P||_F²
      =4 sin²(phi/2)*(81/160)*(79/160).
```

This follows by writing `D=I+(e^{i phi}-1)|e><e|` and using projector properties. It has no fit parameters.

For independent Gaussian edge phases `theta_e ~ N(0,sigma²)`, use `E e^{i(theta_e-theta_f)}=exp(-sigma²)` for `e!=f`; then

```
E L = (6399/160)*(1-exp(-sigma²)).
```

At `sigma=.11` radians this is `0.4810084055` total squared Frobenius leakage across the 81D sector. A 400-trial seeded simulation returns about `0.4803`, independently checking the formula. `L` is an unnormalized **subspace Frobenius leak**, not a per-photon error probability; normalized average over protected input directions is `L/81`.

**Physics boundary:** a gauge-covariantly transformed projector and connection may track a physically equivalent local phase change. The result concerns *actual independent edge-diagonal phase faults relative to a fixed reference Hodge code*, not pure gauge reparametrizations. The 81D topology alone does not automatically protect arbitrary coherent edge phase disorder; active correction, transported connections, error-bias constraints or a physical gap are needed. Prior BT547/548 projector and radial-kernel formulas are acknowledged; the phase-noise leakage laws are the new increment here.

## Reproduction

```
python analysis/toe_20261120_H27_equivariant_sic_memory_weyl_g2_causal_hodge.py
python -m unittest discover -s tests -p 'test_toe_20261120_*.py' -q
```

The producer writes `data/toe_20261120_H27_equivariant_sic_memory_weyl_g2_causal_hodge.json`. It uses NumPy and SciPy, no downloaded external state, and deterministic random seeds. The focused suite contains **33 tests**. Test the actual published source on the connected Windows checkout; report the exact outcome of any broader daily suite rather than claiming one without running it.

## Five independent research directions after these gates

1. **Actual E8 UV lift of the H27-equivariant 19-baryon Higgs module.** Represent all source and auxiliary fields in a consistent E8-breaking multiplet algebra, derive rather than impose the invariant constants, check global F/D extrema, masses, discrete anomalies and chiral matter.
2. **Fully calibrated, loss-aware qutrit temporal-memory witness.** Validate departure from the isotropic noise model experimentally, including complete process-tomography bounds, heralding selection bias, memory survival, photon number and calibrated source/detector errors; test finite-shot negativity with a shared memory device.
3. **Phase-stable optical Weyl twirl.** Compile nine qutrit X/Z conjugations into time-bin/OAM circuits with an actual interleaved identity reference, control setting-dependent efficiencies and prove that the measured character remains invariant under deliberate internal basis scrambling.
4. **Singular G2/E6 chiral compactification.** Choose a genuine compact 7-manifold with appropriate singularity data, specify gauge bundles and a charged Dirac problem, and calculate 4D chirality, local anomaly inflow and a realistic nondegenerate family spectrum. Untwisted S7 and smooth-wall count matches do not suffice.
5. **W33 quantum error correction and 4D causal dynamics as distinct falsifiers.** For W33, derive a microscopic noise channel whose Kraus structure the 81-cycle projector can genuinely correct, using the exact Gaussian edge-phase leakage as baseline. Independently, devise a local order-invariant gravitational action and nonmanifold-entropy test in 4D causal sprinklings; avoid interpreting a finite odd arrow statistic as gravity.
