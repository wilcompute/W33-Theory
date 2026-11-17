# Five-front follow-up: E6 mirror-messenger obstruction, full SU5 quantum shape, physical AdS BF correction threshold, twisted K-theory and calibrated-loss qutrit MUB witness

**17 November 2026 | `wilcompute/W33-Theory` | reproducible research packet from TheHeavyCrown**. Baseline: the 12-file five-front commit `36fd368c3a4822cda3be7d0685516ae3417fa77e`. Current `master` also contains independent ongoing work on AdS flux branches, SMASH/axion and intermediate-scale cosmology (e.g. Pass 12688). This packet does NOT replace any other session's staged, modified or untracked files.

**Classification:** verified group algebra, explicit perturbative effective SU5 quantum vacuum calculation, physical but *two-derivative* gauge-constrained 11D spectral robustness bound, integral topological K-theory and spectral-sequence information, and exact mathematical photonic POVM/witness compilation. **NOT** a complete E6 ultraviolet completion, full 11D eight-derivative action/mass shift, physical M/IIB Page-charge map, actual optical implementation, hardware calibration, or a Theory of Everything.

## 1. E6 mirror-exchange symmetry is possible — but a complete 27 multiplet has an exact quartic no-go

Consider two vectorlike E6 `27+27bar` messenger pairs, indexed `+/-`, and a chiral adjoint `A^a` in 78. The renormalizable E6-invariant superpotential couplings can be arranged as

`W = M(barF_+ F_+ + barF_- F_-) + y A^a(barF_+ T_a F_+ - barF_- T_a F_-)`.

The **mirror exchange** `F+ <-> F-`, `barF+ <-> barF-`, `A -> -A` makes these terms invariant and can enforce the opposite Yukawa signs assumed in the prior SU5 one-loop selector. There is a caveat: a nonzero A VEV may spontaneously break this additional global Z2 and introduce sign-related disconnected vacua. This mirror symmetry is a candidate **sector symmetry**, not a proven exact feature of a complete E6 model.

The crucial new algebraic obstruction was verified by constructing the 45 signed monomial constraints of the E6 27 cubic `I3=det A+det B+det C-Tr(ABC)`, whose diagonal-stabilizer kernel has rank 6. For **arbitrary six-variable** E6 Cartan `H`,

`Tr_27(H³)=0`, `Tr_27(H⁴)=[Tr_27(H²)]²/12`, and `Tr_27(H⁵)` is generically nonzero.

For the COMPLETE 27 messenger pairs with COMMON M, y and soft scalar `Delta` across all 27 components, mirror cancellation of odd powers yields at quartic order only `kappa Tr_27(H⁴)`: this is **purely radial**, so it cannot select an E6 adjoint direction such as SU5's 3+2. The positive SU5 `Tr Phi⁴` result from `36fd368` **requires** incomplete/split multiplets, different heavy backgrounds, mixed multiplet thresholds or higher-degree E6 invariants. The threshold splitting must derive from explicit E6-breaking fields; it cannot simply be stipulated as an E6 gauge-invariant 27 component mass.

We also verified operator selection with the established **`Z4^R`** assignment `R(Q,U,D,L,E,N,F,barF)=1`, `R(Hu,Hd,A78)=0` and superpotential charge 2. It allows all ordinary Yukawas, the Weinberg neutrino operator, mirror messenger masses and adjoint couplings; it forbids perturbative `QQQL`, `UUDE`, `UDD`, `LLE`, `LQD`, `LH_u` and `Hu Hd`. However an R-charge-2 spurion allows `S Hu Hd`; actual R-breaking can reintroduce effects, and **dimension-six gauge-mediated proton decay is unaffected**. We did **not** compute E6 discrete gauge anomalies or a Green–Schwarz mechanism. The `Z4^R` operator pattern is known prior art; the present contribution is a precise compatibility table and complete-27 quartic obstruction for this mirror construction.

References: [E6 27⊗27bar=1+78+650](https://www.sciencedirect.com/science/article/pii/S0550321311002951); [realistic renormalizable supersymmetric E6 Higgs sectors](https://link.springer.com/article/10.1007/JHEP02%282014%29058); [unique `Z4^R` MSSM protection](https://arxiv.org/abs/1009.0905).

**Verifier:** `analysis/toe_20261117_E6_mirror_Z4R_no_go.py`. **Certificate:** `data/toe_20261117_E6_mirror_Z4R_quartic_nogo.json`.

## 2. Beyond quartic: sixth/eighth order and local positive curvatures of the full one-loop log

The previous two-mirror SU5 effective potential, with `M=y=1` and soft scalar `Delta=-0.1`, has one-loop contribution

`V_CW(Phi) = (1/16pi²) sum_i [g(1+phi_i)+g(1-phi_i)]`,
`g(z)=f(z²+Delta)-f(z²)`, `f(s)=s²(log s-3/2)`.

The old result found a **positive `phi^4` coefficient**. This pass symbolically differentiates the **full logarithm to eighth order**. The coefficient of `phi^6`, before the common `1/(8pi²)` mirror prefactor, is EXACTLY

`-Delta*(1-Delta)*(Delta²+10Delta+1)/(15*(1+Delta)^4)`.

At `Delta=-0.1`, the quartic coefficient is positive `kappa4=0.0003334318944`, the sixth coefficient is also positive but small, and the eighth coefficient is **negative**. That is an unambiguous **higher-order caution**: a quartic sign is not sufficient evidence for the global minimum near the heavy threshold or outside the EFT radius.

At fixed normalized adjoint norm `r/M=.2`, compare the full logarithmic potential of the normalized `3+2` and `4+1` eigenvalue patterns. It gives

`V_(4+1)-V_(3+2) = 2.22260765367 × 10^-7`

in model units, agreeing with quartic-plus-sixth predictions within 0.5%. The exact full-log *angular* shape Hessian has two positive independent eigenvalues: the `SU3`-splitting and `SU2`-splitting curvatures, each computed from high-precision first and second derivatives. Numerical optimization from **64 random traceless 5-component shapes** reaches the 3+2 energy in several starts and encounters other stationary points. This is a **local shape stability and competitor test**, NOT a global minimization or physical E6 vacuum.

It remains necessary to match quadratic radial counterterms, gauge loops, the entire `E6` breaking sector, negative-soft scalar stability, renormalization prescription and finite-temperature effects. The 24-component bosonic scalar Hessian from the prior packet remains valid only for its specified tree+quartic potential and does not become the full quantum-E6 Hessian.

**Verifier:** `analysis/toe_20261117_SU5_CW_higher_orders_shape.py`. **Certificate:** `data/toe_20261117_SU5_CW_sixth_order_local_shape_stability.json`.

## 3. A quantitative *necessary target* for full 11D eight-derivative BF stabilization

The parallel repo has a new, properly gauge-constrained, positive-norm **five-scalar** metric–C3 pencil `M v=m² K v` for the two-derivative `AdS5×S2×S2×T2` compactification. It proves a sphere-singlet BF-negative eigenmode for every nonzero torus Fourier momentum `0<lambda<12` regardless of mixed flux asymmetry `|d|<=1`. Our preceding pass also derived the explicit 2D projected Rayleigh certificate.

Now place the still-unknown higher-derivative corrections into the BF quadratic form:

`K' = K+deltaK`, `M'=M+deltaM`, `Q'=M'+4K'`.

For the *actual gauge-admissible* unit-K-normalized negative mode of the established two-derivative pencil, define its BF deficit `Delta_BF=-4-m0²>0`. A rigorous sufficient condition for persistence of **at least one** BF-violating mode is

`||K^(-1/2) deltaK K^(-1/2)||_2 < 1` (positive physical kinetic form),

`||K^(-1/2)(deltaM+4deltaK)K^(-1/2)||_2 < Delta_BF`.

Courant–Fischer ensures that no unbounded mixing between this subspace and other physical modes removes its negative Rayleigh direction. Numerically at `lambda=3pi`, the existing five-scalar pencil has `Delta_BF≈1.016944` at equal mixed flux `d=0` and `≈0.884698` at the extreme `d=1`, with sample values for `d=0,.25,.5,.75,1`. The verifier tests rank-one positive correction just below/above the critical norm, and off-diagonal mixing as strong as `1000`.

If a future eight-derivative calculation **independently proves** the K-normalized correction norm is at most `C/N²`, then `N > sqrt(C/Delta_BF)` is sufficient to retain instability. The certificate tabulates the maximum permissible `C` at `N=10,30,50,100,500`. **C is not computed from M-theory here.** The full supersymmetric eight-derivative `R4`, mixed `G4`, and `C3 wedge X8` fluctuation operators, corrected backgrounds, gauge and Page conditions remain missing, and the parallel nonlinear modulated branch requires its OWN fluctuation study. A 2025 JHEP source discusses eight-derivative terms and the incomplete full supersymmetric completion: https://inspirehep.net/files/65f681b8896ec2475d56288da6abaae2 .

**Verifier:** `analysis/toe_20261117_11D_BF_eightderiv_robustness.py`. **Certificate:** `data/toe_20261117_11D_BF_eightderiv_required_norm_bounds.json`.

## 4. An integral twisted K-theory *charge shadow* beyond the circle bundle gcd

Let `Y(p,q)->B=S²×S²` be the principal circle bundle with Euler class `e=p x+q y`, `g=gcd(|p|,|q|)>0`. The topological type-II circle T-duality with NS H flux `H=k z` and `k != 0` from the previous packet gives dual Euler `e'=(k p/g, -k q/g)` and dual H coefficient `sign(k)g`.

We now compute **actual untwisted complex K-theory** of `Y` using the K-theoretic circle Gysin exact sequence. Since `K^0(B)=Z[x,y]/(x²,y²)`, the Euler difference operator acts by multiplication with

`[L]-1=(1+x)^p(1+y)^q-1=p x+q y+pq xy`.

Its full `4x4` integer matrix has nonzero Smith invariants **`g,g`**, so

`K^0(Y)=Z² ⊕ Z_g ⊕ Z_g`, `K^1(Y)=Z²`,

with trivial cyclic factors omitted at `g=1`. This is an **exact integral K-group calculation**, not only cohomology.

For *nonzero* NS flux `H=kz`, the twisted complex K Atiyah–Hirzebruch spectral-sequence differential at first nontrivial order is `d3=Sq_Z^3+H cup`. On this oriented 5-manifold the relevant nonzero maps are free `H^0(Y)=Z -> H^3(Y)=Z` by multiplication `k`, and free `H²(Y)=Z⊕Z_g -> H^5(Y)=Z` by multiplication `k` on a primitive free generator. The first gives odd residual factor `Z_|k|`, the second another odd factor; the pre-existing even torsion in degrees 2,4 gives two factors `Z_g`.

Thus the `E_infty` **associated graded factors** have total order **`g²` in even** and **`k²` in odd** twisted K-theory. These orders are interchanged under topological T-duality's parity shift; a `(g,k)=(6,5)` example exchanges **36 and 25**. Smith invariants and parity-matched orders were independently checked for **1,200 signed integer triples**. **Important:** the *extension problem remains unsolved* for the twisted groups. Do NOT claim `K^even=Z_g×Z_g` or `K^odd=Z_k×Z_k` from these `E_infty` factors without further work, or equate these topological K-group invariants to Page charges. Differential K-theory, curvature, RR/self-dual field conditions, brane endpoints and the M-theory dual still need explicit constructions.

Literature: [Bouwknegt–Evslin–Mathai T-duality](https://arxiv.org/abs/hep-th/0306062), [equivariant twisted K-theory](https://link.springer.com/article/10.1007/s00220-024-05044-0).

**Verifier:** `analysis/toe_20261117_Ypq_twisted_K_AHSS.py`. **Certificate:** `data/toe_20261117_Ypq_KGysin_twisted_AHSS_charge_shadow.json`.

## 5. Full qutrit MUB analyzer compiler, and a **better trusted-loss entanglement witness**

Explicitly construct the four MUB of a qutrit from the computational `Z` eigenbasis and three eigenbases `X Z^b`, `b=0,1,2`, with Weyl shift X and phase Z. All **six distinct pairs** satisfy `|<u|v>|²=1/3`; every analyzer `U_b†` is reconstructed with machine precision using **at most three adjacent two-mode Givens mixing stages plus phases**, in the spatial three-rail abstraction. The computational basis needs no mixing stages; the other three each need three stages in the deterministic QR compiler. Converting actual time bins into rails and choosing the measurement basis independently after heralding still requires real fast switches, delays and fidelity calibration.

**Conservative throughput firewall:** with two independent 90.2%-efficient reference memories, path .95, two .9 detectors, router throughput .995 each, source `v=.75`, phase noise sigma=.15 and *loss-independent* null `p0=.51`, an additional three couplers in **each** qutrit analyzer makes the modeled event-ready gross match `<.51` for all nominal coupler throughputs `<=.9995`. A symmetric stage throughput `>.9995602` is required in that worst-case six-stage *loss-independent p0* accounting. This is an intentional conservative **selected witness** limit, not a physics theorem preventing optical entanglement.

**New, stronger alternative:** if each local instrument is verified by **operator-level measurement tomography** to have *state-independent*, **setting-known** erasure throughputs, then the separable witness threshold can be reduced. Under common known per-heralded-trial throughput `a` and setting-dependent relative *pair* throughput `(1,t,t,t)` for computational and three noncomputational MUBs (here `t=c^6`), the complete 4-MUB 2-design identity is

`sum_{b,j} |u_bj,u_bj*><u_bj,u_bj*| = I_9+3|Phi_3><Phi_3|`.

For ANY separable pure product source, the sum over all bases of the matched probabilities is `1+|<alpha*|beta>|² <=2`, while the computational-basis-only contribution is at most 1. Therefore the **exact, attainable separable bound** is

`p_sep <= a[ t*2 + (1-t)*1]/4 = a(1+t)/4.`

Mixed separable states obey it by convexity. Computational product states saturate it. The verifier checks the exact 9×9 operator identity and **1,000 random products** against the bound.

For a specified mixed state `rho=(1-v)I9/9+v[(1-E) sum_j |jj><jj|/3+E|Phi_3><Phi_3|]`, `E=exp(-sigma²)`, the matched probabilities are `q_Z=(1+2v)/3=0.8333333`, and `q_each_other=(1+2vE)/3≈0.82220895`. Their uniform mean exactly reproduces the previously used formula `q(v,sigma)`. Including the setting-dependent analyzer losses, the expected genuine-qutrit-state gross match is

`p_ent = a[q_Z+3t q_nonZ]/4.`

For reference `eta_mem=.902` on two arms, router=.995 each, path=.95, each detector=.9, each mixing stage=.995 (so `t=.995^6≈.970373`), the **trusted-calibrated** model yields

`a≈.61982325`; `p_sep≈.30532067`; `p_ent≈.50002384`.

Thus an ideal source would **violate the calibrated separability bound by ≈.194703**, despite not violating the old conservative `.51` bound. The *oracle fixed-alt Bernoulli likelihood* information scale for threshold e-value 100 is **≈56 preparations**; for two hypothetical `39.2%` memories it is ≈437 preparations, again **only in the idealized trusted calibration model**, not a guarantee or hardware result. Exactly this reinterpretation of the measurement—the ability to calibrate known loss as part of the POVM rather than treating all unclicked trials adversarially—is the strongest new practical insight from this round.

**Critical loophole firewall:** These improvements do NOT hold merely because a lab quotes "90.2% memory efficiency." To use `p_sep=a(1+t)/4` the *whole input-to-outcome quantum measurement instrument* (memory retrieval, routing, analyzer, detectors) must be certified as basis-known state-independent erasure for **all admissible qutrit states** with valid upper bounds on source-conditioned drift, leakage and calibration errors. The bound used in the anytime-valid e-process must hold **conditionally on every trial's past**. Arbitrary state-dependent loss, postbasis coincidence selection or setting leakage invalidates the sharpened null; in those conditions fall back to the previously conservative `p0=.51`. No qutrit memory, source, analyzers, QND herald or real timetags were built.

Hardware reference: [PRL accepted Sept 2026, 90.2(4)% weak-coherent-pulse memory and 99.3(1)% time-bin qubit fidelity](https://journals.aps.org/prl/accepted/10.1103/28st-q915), **NOT a direct qutrit hardware demonstration**.

**Verifiers:** `analysis/toe_20261117_qutrit_four_MUB_loss_compiler.py` and `analysis/toe_20261117_qutrit_calibrated_loss_witness.py`. **Certificates:** `data/toe_20261117_qutrit_four_MUB_analyzer_stage_loss.json`, `data/toe_20261117_qutrit_efficiency_aware_MUB_witness.json`.

## Test and sync audit

All **six new Python verifiers** wrote independent deterministic JSON certificates. A **55-test** focused new unit suite passed; three prior suites comprising **33,58,47** tests also passed (193/193 targeted regressions across new and prior suites). No tests ran on experimental data or evaluated the complete repo-wide test collection. Preserve all other agents' uncommitted work. Stage/commit only the following **14** new paths:

- Six new `analysis/toe_20261117_*.py` files named in the sections
- Six `data/toe_20261117_*.json` certificates named in the sections
- This report `analysis/2026-11-17_TOE_E6_mirror_CW_BF_twistedK_calibrated_qutrit.md`
- `tests/test_toe_20261117_mirror_quantum_BF_K_qutrit_aware.py`

Reproduce on the authorized Windows checkout:

```bat
python analysis/toe_20261117_E6_mirror_Z4R_no_go.py
python analysis/toe_20261117_SU5_CW_higher_orders_shape.py
python analysis/toe_20261117_11D_BF_eightderiv_robustness.py
python analysis/toe_20261117_Ypq_twisted_K_AHSS.py
python analysis/toe_20261117_qutrit_four_MUB_loss_compiler.py
python analysis/toe_20261117_qutrit_calibrated_loss_witness.py
python -m unittest discover -s tests -p test_toe_20261117_mirror_quantum_BF_K_qutrit_aware.py -v
```

## Five independent physical next falsifiers

**E6 model:** Explicitly embed the split 27 messenger thresholds in a F/D-flat E6 Higgs sector, derive a non-spurious discrete symmetry with anomaly control and test complete gauge- and triplet-mediated proton decay.

**Vacuum:** Construct a renormalization-consistent *global* E6 CW potential and complete soft/gauge/Higgs scalar Hessian, scan shape + radius beyond fixed norm, and compute finite-temperature dynamical selection with domain walls.

**11D:** Derive the actual on-shell supersymmetric eight-derivative coupled `R4+G4+C3X8` quadratic kinetic/mass operator on the product AND modulated backgrounds, compute a physically meaningful bound on `C`, and test corrected BF stability.

**Duality:** Resolve extensions of the `E_infty` twisted K groups through an independent geometric K-theory presentation; implement differential refinements and explicit physical RR, M2/M5 and Page-charge/endpoints.

**Photonic:** Perform device-level quantum process/POVM tomography demonstrating state- and setting-independent erasure for a genuine time-bin qutrit in four MUBs; measure all port losses, drift and temporal setting-leakage bounds; then run the calibrated sequential e-process on actual timetags.

**No solved physical Theory of Everything or experimentally observed qutrit entanglement is claimed.**
