# 2026-11-03 — TOE physics five fronts and three independent falsifier ideas

**Executive assessment:** The most meaningful new result is a negative observational identifiability finding. The real patched-CLASS fading-DM model changes CMB lensing by 1.1–2.8% at L=40–1000 with the other cosmological parameters held fixed, but **99.9808% of the squared log-response is absorbed** by allowing standard primordial amplitude and spectral index variations in an idealized six-bin linear test. Separate fronts established a corrected canonical WKB benchmark, constructed a 40,000-dimensional exotic-charge sparse 4D Wilson kernel with verified gauge covariance, integrated a fully periodic two-function scalar/DM background, and quantified nuisance vulnerability in a four-distance gravitational experiment. **No TOE was proved.** The general method is to attack the strongest non-W33 physical interpretations with ordinary physics consistency requirements.

## Exact repository intake and ownership

At intake, authorized Windows checkout `C:\Repos\Theory of Everything` and GitHub `wilcompute/W33-Theory` both had HEAD `eb3269903bbbc3fc00aace9dc334910a47cf7c71`; staged index was empty, with **54 unrelated preexisting worktree entries**. The latest parallel package was already integrated: no new remote commits were seen during research. Recent public work already included the full fading-CDM CLASS+Planck/DESI/Dovekie best fit `b5b4db003`, first species transfer benchmark `665622ee1`, prior exact scalar background `eb3269903`, and speculative local unpublished multi-sector mechanisms, including a small-L 4D overlap operator and SUSY portal leakage. **None of those is claimed here as an original discovery.** Do not include, stage or reset unrelated dirty files.

Web verification before the new tests:
- [Passaglia and Hu, accurate effective-fluid approximation for ultralight axions (PRD 2022)](https://doi.org/10.1103/PhysRevD.105.123529) and [Moss et al., CAMB implementation (PRD 2025)](https://doi.org/10.1103/fy1y-rjst). A naive dust fluid needs switching and perturbation validation against the exact Klein–Gordon oscillator; these researchers already own the controlled effective-fluid literature.
- [DESI DR1 peculiar-velocity measurement A&A 2026](https://doi.org/10.1051/0004-6361/202558368), providing 0.450±0.055 at z=.07. We do not count the same correlated survey twice.
- [CLASS documentation, lensing C_l output](https://huggingface.co/spaces/santicas/CLAPP/blob/main/class-data/explanatory.ini). `o_cl.dat` names `phiphi`; CMB `C_l^phiphi` is distinct from a galaxy weak-lensing shear tomographic observable and from a reconstruction likelihood.
- [Misumi, overlap and Ginsparg–Wilson constraints, PRD 2026](https://doi.org/10.1103/756m-stz5); [Craig, chiral measure, October 2026](https://arxiv.org/abs/2610.09093). Sparse Wilson matrices are not already globally invariant Weyl measures.
- [D'Amico, Hamill, Kaloper, light axion and dark-monodromy protection (PRD 2016)](https://doi.org/10.1103/PhysRevD.94.103526). SUSY cancellations and portals are established prior methods and already present in the uncommitted local mechanism.
- [Di Biagio, gravity-induced entanglement not a theory-independent witness (PRD, October 2026)](https://doi.org/10.1103/r8ry-sp35). No claim to observe or prove gravitons is made.

## Front 1 — exact oscillating Klein–Gordon versus adiabatic dust, with a finite-H correction

`analysis/toe_20261103_exact_kg_wkb_crosscheck.py` + `data/toe_20261103_exact_kg_wkb_crosscheck.json`.

We solved the full high-frequency **test** oscillator in a supplied, homogeneous, exactly covariant coupled-dust/scalar Friedmann solution. It does **not** double-count its self-gravity: the rapidly oscillating `chi` is a test field; the background has an independently averaged coupled-dust component. The oscillator obeys `chi_NN+(3+H_N/H)chi_N+(m/H)^2 chi=0` with `m(x)=m0 exp(-beta*x)`. We tested dimensionless `m(today)/H0={20,40,80,160}` over z=1 to0 with DOP853.

The naive instantaneous comoving number `J=e^(3N) rho_chi/m` is not an accurate pointwise action at finite H/m. In particular at `m/H0=160`, its endpoint median drifts by `0.00342299` and late-time central 90% spread is `0.018656`. Define the canonical field `Q=a^(3/2)chi`, which satisfies `Q_ddot+Omega_eff² Q=0` with `Omega_eff²=m²-(3/2)Hdot-(9/4)H²`. The corresponding instantaneous canonical action `J_Q=(Qdot²+Omega_eff² Q²)/(2 Omega_eff)` corrects this error: endpoint drift `4.20527e-5`, late 90% spread `1.6889e-4` at `m/H0=160`; checked separately over four frequencies. At `m/H0=40`, naive endpoint drift is `0.06017` versus canonical `0.000812`. **This is an empirical numerical canonical-adabatic benchmark**, not a proof of global error order nor the already published accurate Passaglia–Hu EFA scheme. Unlike a cosmological mchi=1e-20 eV where m/H is enormous today, these smaller Q values stress the switching regime in code.

**Unmet original scope:** no full radiation-era coupled ultralight CLASS Boltzmann hierarchy, high-k transfer or Ly-alpha likelihood; the background only is self-consistent. This provides an independently reproducible exact-KG convergence target for implementing the actual field in CLASS.

## Front 2 — real CLASS lensing with amplitude AND tilt marginalization

`analysis/toe_20261103_class_lensing_growth_jacobian.py` and `analysis/toe_20261103_class_lensing_tilt_projection.py`, with frozen corresponding JSON certificates.

Four **real patched-CLASS** runs were performed in Ubuntu using the existing frozen best-fit `analysis/toe_uv/class_fit_dovekie.json`: (a) fitted cprime, (b) identical other input parameters with cprime=0, (c) fitted cprime but `ln(10^10 As)` increased by 0.01, (d) fitted cprime but `ns` increased by .005. `CLASS o_cl.dat phiphi` was directly read at six multipoles L={40,100,200,400,700,1000}. The ratio `Cphi(fading)/Cphi(cprime0)-1` is +1.118%, +1.450%, +1.817%, +2.218%, +2.571%, +2.780%.

The six-lens log response is strongly correlated with a primordial amplitude shift; adding the independently measured finite-difference `ns` response makes it worse. Fitting the six-bin cprime log response by one amplitude plus one ns-shaped tilt gives residuals `{+0.000445,-0.000343,-0.000328,-0.000099,+0.000172,+0.000153}`. **99.9808119401% of the squared response is removed by the two nuisance modes.** In a FICTIONAL 1%-precision independent six-point Gaussian Fisher matrix, marginalized sigma(cprime) rises from 0.0373 (amplitude nuisance only) to 0.7603 (amplitude and ns nuisance) against fitted cprime=0.053. Finite cprime variation from 0 to0.053 is a **secant**, so this is a sensitivity stress test, not an exact posterior or a true differential Fisher at zero coupling. Real CMB lensing multipoles are correlated, have reconstruction/foreground/noise and have Planck constraints on ns; all other parameters were fixed, and neither actual lensing survey data nor galaxy shear covariance was evaluated. The existing independent DESI DR1 PV analysis in prior commit gives only 0.11σ separation on a single growth point. **Do not claim 3σ lensing detection, or a new RSD/lensing likelihood.**

### Additional original selection insight: nuisance-aware orthogonal lensing curvature

A linear combination of actual six CLASS Cphi outputs can be projected exactly onto the orthogonal complement of the two fixed fitted-design response columns (1, dlogCl/dns). Only that combination is diagnostic of the coupling independent of amplitude+tilt *to first order*. The measured six-bin residual norm is far smaller than the original spectrum response. This is a precise model-selection null experiment under stated assumptions and is stronger than merely contrasting lens amplitudes. Its construction and norm are reproducible in the tilt certificate.

## Front 3 — compact field-space physics and one-loop UV window

`analysis/toe_20261103_compact_two_function_uv_window.py`, corresponding JSON.

A **strictly compact** scalar x~x+2pi F cannot have globally single-valued *either* `mchi=m0 exp(-beta x)` with beta!=0 *or* `V=V0 exp(-lambda x)` with lambda!=0. The earlier pass proved the mass obstruction; here the potential obstruction is added and we integrate **both periodic replacements simultaneously**, with `y=F sin(x/F)`, `m=m0 exp(-beta y)`, `V=V0 exp(-lambda y)`. Their derivatives include `dy/dx=cos(x/F)`; the homogeneous Friedmann/Raychaudhuri/Klein–Gordon equations are integrated through z=5 with residual <3e-10. F is tested at {.5,1,2,4} Mpl and compared with the exactly exponential noncompact benchmark for the same **supplied** v0=.5 and lambda=.5. For the illustrative z=1 case, E² changes from 3.89477 for noncompact to 3.94385 for F=.5 and 3.89781 for F=2. Thus a globally consistent periodic completion changes the cosmological history, not just a notation.

One-loop threshold stress test for an unprotected isolated real boson with mheavy(φ) varying with dimensionless slope g uses `|delta mphi²|~g² Mheavy^4/(8pi² Mpl²)`. The heavy mass 1 TeV demands `g < 3.13e-29` to keep this *one assumed* curvature below H0², absent cancellations/protection; at 1e16GeV it is even more restrictive. This is conditional naturalness, not an observed constraint, and the previous uncommitted SUSY portal analysis already treats soft-loop leakage in a specific UV model. **No complete quantum-stable UV model was produced** and a compact axion with explicit monodromy would require new branch physics.

## Front 4 — actual sparse Q=15 4D Wilson construction, not just resource estimation

`analysis/toe_20261103_sparse_exotic_chiral_q15.py` and JSON.

Prior uncommitted `analysis/toe_20261103_mechanism_four_dimensional_overlap.py` constructs **dense** small-L overlap sign operators, index and Weyl intertwiner. This pass independently constructs the Hermitian Wilson pre-overlap kernel `H=gamma5(W-m0),m0=1` as `scipy.sparse` Kronecker shifts from link phases with integer exotic Q=3(B-L). At L=3, q=1, dense cross-validation gives index -1 (as in previous work), full spectral gap 0.345509781, sparse minimum eigen 0.345509781; gauge covariance relative error `2.43e-16`. At L=4, q=1, gauge covariance error `2.47e-16`.

At **L=10, Q=15**, the matrix has dimension 40,000, **680,000 nonzeros**, Hermitian defect exactly zero in sparse coefficients, and gauge covariance on a random actual 40,000-component vector to `2.38e-16`. CSR data+indices+indptr use **13.12 MiB** rather than the 23.84 GiB dense complex128 kernel. This is a major enabling computational representation, but not the *full overlap sign*, **not an L10 topological index**, **not a globally invariant Weyl measure**, and not a proof of uniform locality in all admissible backgrounds. The 4D lattice geometry is externally supplied and not derived from any finite graph.

## Front 5 — gravity experiment under nuisance and composition constraints

`analysis/toe_20261103_gravity_multidistance_nuisance_design.py`, JSON.

Optimized the *earlier* static Newton/Yukawa two-mass controlled-phase test against four center-to-center separations chosen from 150–500 μm, with mass 2e-14 kg each, path displacement 50 μm, t=1s and Yukawa trial range λ=150 μm. A priori unrelated phase offset and Yukawa normalization are each fitted away. The best among the tested four-distance combinations is **150,200,225,500 μm**. With independent Gaussian phase error **0.01 rad** at every distance (invented experiment, not measured noise), the best separation from Yukawa is **0.862σ**, not a discovery. Adding one inverse-cube phase background nuisance drops it to **0.060σ**. This is an explicit quantitative experimental falsifier: the potential shape difference is NOT robust to even one sufficiently flexible background. A separate gravitational clock height difference `g Δh/c²=1.0911e-16` for 1m is controlled by the same potential—combining it with a stationary matter-wave phase at one location need not provide an independent mediator observable.

**No experiment was performed**, no electromagnetic/Casimir source model, retardation, finite wavepackets or measured decoherence covariance. No theory-independent evidence for gravitons is claimed; October 2026 PRD expressly qualifies the LOCC inference.

## Three additional creative ideas, executed within these five fronts

1. **Canonical adiabatic action**: use the (a^{3/2}) rescaling to construct an integration control that suppresses finite-H oscillatory contamination by up to two orders of magnitude over the naive `rho/m` diagnostic. This gives a better switch/error test for any future coupled effective fluid.
2. **Nuisance-orthogonal lensing response**: a 1–3% apparent signal loses 99.98% of its squared detectability when one allows the actually measured CLASS primordial amplitude+tilt response. This identifies what a future independent observable must measure, rather than counting fitting improvements.
3. **Exotic-charge sparse regulator with direct gauge covariance**: the exact 40k-dimensional operator now fits in ~13 MiB and supports test-vector gauge transformations. This moves the chiral program from a large dense estimate to an actionable, verifiable Wilson kernel.

## Tests, novelty, explicit open problems

The research consists of six Python producers, six frozen JSON result certificates, this report and one independent regression suite under `tests/`. No uncommitted local owner file is changed or staged. Math and solver validation are distinguished from physics confirmation. Four CLASS runs are executed inside Ubuntu on the user's authorized Windows desktop; the other producers run in Windows Python SciPy. Focused suite validates numerical identities, operator dimensions, rescaling gains, model scope, source input, and external lensing data; existing mechanism and prior physics regression suites are run for compatibility. **No full repository suite, full likelihood, real galaxy shear analysis, chiral gauge measure or complete TOE is claimed.**

### Top five independent next steps

1. Integrate a **covariantly energy-conserving oscillating-ultralight effective-fluid hierarchy** into a *separate* CLASS fork with validated constant-mass and beta→0 limits, accurate radiation-era switching, gauge stress tests, and actual CMB/Lyman-alpha transfer predictions.
2. Find genuinely **nuisance-orthogonal** cosmic observables by combining reconstructed matter/baryon transfer functions, low-z PV, CMB lensing, independent shear tomography, and expansion distance—include survey covariance, ns/As/prior volume, not illustrative 1% independent bins.
3. Construct a single field-space complete **protected** two-field EFT (noncompact modulus versus monodromy), checking global scalar periodicity, heavy thresholds, mixing, uplift, radiative stability, and the observed expansion trajectory without tuned independent patches.
4. Implement a gap-bounded sparse sign function on the actual 40k Q15 matrix, calculate the q² flux index, stress gauge-current Ward identities and the 2026 integrable chiral measure before claiming a fermionic QFT.
5. Design a gravity protocol where sensitivity survives electromagnetic/Casimir nuisance *and* perturbations of source separation, clock height, decoherence, retardation and mediator locality, rather than declaring a graviton from ideal point masses.
