# Cross-domain TOE falsifiers — 2026-11-03 (Nov 3 afternoon local)

**Scope.** A five-front research pass beyond W33 plus three independent ideas. Exact finite theorems, actual numerical CLASS results, independent observational data, prescribed toy effective actions, and unproven TOE claims are deliberately separated. **Not a TOE. Not a complete coupled-ultralight CLASS. Not a full RSD likelihood. Not a chiral fermion measure. Not a theory-independent quantization witness. Not a complete quantum-stable UV model.**

## Provenance and parallel work

GitHub `wilcompute/W33-Theory`, `master`, was synchronized with `C:\Repos\Theory of Everything` at intake SHA `665622ee17ae010311d30e7235f07bcb5c6dfd04`; 54 existing unrelated dirty local entries, clean staged index, no parallel commits ahead at intake. Relevant prior results belong to prior project commits: patched CLASS fading model (Pass12550–12557 and paper source), the toy ultralight WKB/pressure model and real 5-redshift CLASS transfers (2026-11-03 eight-front pass), uncommitted four-dimensional overlap and holomorphic/neutrino mechanisms, and their own earlier discoveries. These are not rebranded as original.

External sources researched **before choosing tests**:
- [Accurate effective fluid approximation for ultralight axions](https://doi.org/10.1103/PhysRevD.105.123529), Passaglia & Hu (2022), for the oscillating scalar fluid / switch problem.
- [Screened axio-dilaton cosmology](https://link.springer.com/article/10.1140/epjc/s10052-025-14735-4) (2025), for adiabatic mass transfer and perturbation conventions.
- [Dark monodromies](https://doi.org/10.1103/PhysRevD.94.103526) (2016), for the known protected light-axion coupled-sector alternative.
- [DESI DR1 peculiar velocity growth measurement](https://doi.org/10.1051/0004-6361/202558368) (2026), for the published independent low-z consensus f sigma8=0.450+/-0.055 at z=0.07.
- [DESI DR2 official publication index](https://data.desi.lbl.gov/doc/papers/dr2/) and [Cobaya BAO/RSD documentation](https://cobaya.readthedocs.io/en/latest/likelihood_bao.html), which explicitly notes that DESI BAO-only is not an RSD likelihood and that single compressed f sigma8 can be inaccurate for some non-LCDM models.
- [Craig, gauge-invariant lattice chiral measure](https://arxiv.org/abs/2610.09093) (October 2026), [Thorngren–Preskill–Fidkowski chiral disentanglers](https://link.springer.com/article/10.1007/JHEP07%282026%29271), for exact prior-art standards.
- [Gravity-induced entanglement is not a theory-independent witness](https://doi.org/10.1103/r8ry-sp35) (October 2026), and [When does entanglement through gravity imply gravitons?](https://doi.org/10.1103/lq47-1hfg) (July 2026), for the mediator-inference limitations.

## Front 1: covariant scalar + oscillating-axion WKB consistency and compact-mass obstruction

`analysis/toe_20261103_covariant_wkb_axion_periodicity.py` + `data/toe_20261103_covariant_wkb_and_axion_periodicity.json`.

We actually evolved a **self-consistent homogeneous** flat Friedmann system, rather than combining an externally chosen phi clock with a nonconserved cosmological constant. The declared *input* action is Einstein gravity with canonical rolling scalar x=phi/Mpl, V(x)=V0 exp(-lambda x) (lambda=.5 **supplied**, not fitted), WKB dark matter rho_c=3Mpl²H0² Omega_c a^-3 exp(-beta x), beta from the stored CLASS best fit. Set x0=0 and velocity v0=dx/dln a=.5 (**supplied**, not fitted), and normalize V0 by E(0)=1. E²=(rho_bar_b+rho_bar_c+rho_bar_r+Vbar)/(1-v²/6), h_N=-(3/2)(Omega_b+Omega_c)-2 Omega_r-v²/2, and Klein-Gordon v_N=-(3+h_N)v+3(lambda Vbar+beta rho_bar_c)/E². The numerical integration to z=5 verifies both the Friedmann/Raychaudhuri identity and interacting scalar/dark matter energy exchange to <=3e-13 in the chosen dimensionless residuals.

This **does not** reproduce the published best-fit H(z), CMB or w(z); it proves that a coherent exact background can be constructed and numerically tested, a prerequisite for full oscillating-wave CLASS perturbations.

**Structural periodicity theorem:** For a genuinely compact axion phi~phi+2pi f, physical mass m(phi)=m0 exp(-beta phi/Mpl) is single-valued iff beta=0 for real nonzero f. That is incompatible with using an *exact* compact shift symmetry to protect the same exponential rolling-field coupling. A noncompact rolling modulus, multi-valued monodromy theory, or periodic local replacement can evade the narrow objection, but these require independent definition.

An explicit periodic local mass `m=m0 exp[-beta*(f/Mpl)*sin(phi/f)]` has the same tangent beta at phi=0, but beta_eff(phi)=beta*cos(phi/f). For the frozen measured-fitted excursion Delta phi=0.279594 Mpl, bounding drift in beta across the entire excursion (assuming start at zero phase) gives `f>=0.619906 Mpl` for 10%, `f>=1.975379 Mpl` for 1%, `f>=6.25139 Mpl` for 0.1%. **Not** a universal axion/WGC bound; other periodic functions and shifted phase points can behave differently. The original exact global exponential is not periodically protected.

## Front 2: actual CLASS linear growth vs independent 2026 DR1 peculiar velocities

`analysis/toe_20261103_class_RSD_PV_holdout.py`, data `data/toe_20261103_class_PV_real_RSD_singlepoint.json`. The producer used the already connected Ubuntu `~/cosmo/class_fading/class` binary, repository's `class_cmb.run_class` source, and stored Planck+DESI DR2+Dovekie best-fit parameters. Re-evaluated three **real** linear spectra at seven redshifts z=0,.04,.06,.07,.08,.10,.15, with linear P(k) (non_linear=none). Integrating CLASS `P_m(k,z)` against a radius-8 Mpc/h top-hat yields sigma8(z); at z=0 the reconstructed sigma8 matches the CLASS printed value within 0.019% across all three runs. Finite derivative gives linear f sigma8(z=.07)=-(1+.07)*d sigma8/dz.

| Model | f sigma8(z=.07) | single independent public consensus |
|---|---:|---:|
| Fading fit cp=.0529975 | 0.43904564 | 0.450 +/-0.055 |
| Same cosmological parameters and c, cp=0 (**not refitted**) | 0.43313916 | |
| Separately fitted native LambdaCDM (**confounded parameters**) | 0.43124024 | |

Fading minus cp=0 has Delta f sigma8=0.00590648, only `0.1074` of the reported DR1 consensus uncertainty. Each model lies <0.35 standard deviations from the published central value. This is a **single independent-data diagnostic**, not a full RSD likelihood, not a statistically blinded holdout (we inspected the measurement before designing the calculation), and there are model assumptions in the quoted consensus. The patched CLASS still evolves *pressureless* coupled CDM, **not** the ultralight wave fluid; no fuzzy-DM Ly-alpha transfer function was fitted.

## Front 3: UV/shift protection, not a hidden successful completion

The periodic-mass obstruction above gives a narrow strong result: the rolling scalar cannot simultaneously be an **ordinary exactly compact axion** and the globally defined exponential-coupling variable of the best-fit CLASS Lagrangian. This is independent of the previously verified *small one-real-boson Coleman-Weinberg correction* (which only bounds the loop from the ultralight particle). Light-axion coupled sectors and monodromy are established prior art; to claim a UV completion we need full heavy-sector threshold spectrum, appropriate periodic/monodromy gauge redundancy, SUSY-breaking/uplift corrections, and a viable positive-energy vacuum. **None supplied.**

## Front 4: exotic-B-L chiral-lattice resolution, anomaly versus topology

`analysis/toe_20261103_chiral_topological_resolution_guard.py` and `data/toe_20261103_chiral_topological_resolution_guard.json` recheck existing committed sterile Q=3(B-L) charges (-15,+12,+12). These cancel three generations' SM linear/cubic anomalies: sum sterile Q=9, sum sterile Q³=81, but sum sterile Q²=513. **Anomaly cancellation does not erase individual topological index sectors.** For background smooth U(1) flux n12=n34=1, each charge-q Dirac index magnitude is q² (topological index theorem; no numerical dense-L10 index calculation is claimed).

A *declared conservative* unwrapped plaquette phase condition `|q|*2pi/L²<pi/3` forces `L²>6|q|` for a uniform unit flux torus. Hence Q=15 needs at least L=10 (10,000 four-dimensional sites; 40,000-component spinor kernel) and a single **dense complex128** kernel needs 23.84 GiB; Q=18 needs L=11 (58,564 components; 51.11 GiB). This is a **chosen benchmark sufficient small-phase control**, not a mathematically necessary universal admissibility criterion. Sparse rational/overlap sign approximations and gauge-sector-aware Weyl basis are essential for engineering an actual exotic nonperturbative regulator. The existing user's uncommitted L=3,4 overlap tests and published 2026 measures are recognized, not claimed here.

**Not a chiral fermion measure:** Fermion determinant phase, global holonomy/integrability, locality uniform in L, gauge Ward identities for coupled charged sectors and mirror exclusion remain open.

## Front 5: operational gravitational entanglement, testing *potential shape* not quantumness

`analysis/toe_20261103_gravity_phase_decoherence_null.py` and `data/toe_20261103_gravity_phase_decoherence_null.json`. In an explicitly idealized two-mass Newtonian model with each mass 2e-14 kg, center separation d=200 micrometers, path displacement 100 micrometers, t=1s, the controlled two-qubit phase is -0.843855916 rad and the pure concurrence is 0.40952009, satisfying exact `C=|sin(DeltaPhi/2)|`. Independent local dephasing on both path qubits gives a PPT-negativity threshold when the single-qubit off-diagonal factor falls below eta≈0.671085 (equivalent gamma~0.39886 s^-1 at t=1s). This is a mathematical quantum-channel example, **not** a feasible lab forecast: electrostatics, wavepacket extension, thermal/environmental decoherence, retardation and gravity noise ignored.

A genuinely independent idea: a **single distance cannot distinguish** an unknown potential normalization multiplying 1/r from one multiplying exp(-r/lambda)/r: amplitudes can be calibrated to agree at that one separation. For fixed arm separation 50 micrometers and hypothetical Yukawa range 150 micrometers, normalizing both at center distance 200 micrometers yields Yukawa/Newton phase-shape ratios `1.08177` at 150 micrometers, `1.0000` at 200 micrometers, `0.79739` at 300 micrometers, `0.41584` at 500 micrometers. Multiple distances can test potential shape **without solving gravity quantization**. As shown in October2026 PRD, detecting entanglement does not by itself eliminate every classical nonlocal mediator model; an actual relativistic mediator inference requires additional assumptions and retardation tests. The dark-matter-only cosmological fifth force is not assumed to couple to the visible test masses.

## Three additional independent ideas beyond the prior 5

1. **Exact compact-axion no-go and quantitative periodic replacement.** A global shift symmetry can invalidate an apparently straightforward exponential mass ansatz. The field-space geometry must be stated, not inferred from radiative lightness.
2. **Fisher/nullspace experiment selection.** `analysis/toe_20261103_class_growth_nuisance_projection.py`, certificate `data/toe_20261103_class_growth_nuisance_projection.json`: project real CLASS fixed-background-pair log growth responses in k={.05,.10,.20,.5,1,3} h/Mpc onto the complement of the free normalization vector. Mean log response 0.00331042, RMS scale-shape 3.04965e-6, max 4.52963e-6. At hypothetical independent 1% error per scale the shape-only chi² after exactly marginalizing one constant amplitude is `5.58e-7`. Thus growth *shape alone at one redshift* is essentially blind to the coupling in this chosen control. An impossible assumption of ~780 independent same-precision DR1-PV points would be needed for 3 sigma if every point measured the identical 0.005906 separation; this is **an illustrative lower-bound sensitivity**, not a realistic survey design. Species-sensitive baryon lensing and redshift evolution are more promising than adding more k bins.
3. **Operational mediator-identifiability by distance.** The gravitational protocol above separates "nonzero controlled phase" from "quantum mediator" and replaces a one-point inference with a multi-distance model-selection problem, with fully calculated witness, decoherence and potential ratios.

## Exact reproducibility, ownership and outstanding TOE gap

Scripts under `analysis/toe_20261103_*.py`; JSON certificates under `data/toe_20261103_*.json`. One 12-test suite `tests/test_toe_20261103_crossdomain_falsifiers.py` checks exact continuity, monodromy, full CLASS independent integration, measured PV point, nuisance projection, Newtonian entanglement PPT, index resource guard and scope boundaries. Full CLASS producer must run on the authorized Ubuntu computer with `~/cosmo/class_fading/class`; the others use installed Python/SciPy/NumPy. The full repo test suite is not claimed.

**Physics still missing:** A local Lorentz-invariant single action producing the observed chiral gauge content, fermion mass matrix, stable de Sitter-like cosmological solution, coupled ultralight dark matter and measured gravity, with few non-fitted parameters. No finite geometry or graph adjacency alone supplies this. These results narrow the field-theory requirements and experimental identifiability.

### Five independent next experiments

1. Implement the coupled oscillating-axion effective-fluid perturbations in CLASS *with* covariant background energy exchange, matched early radiation-era evolution, and verified convergence to pressureless fading-CDM as mchi/H -> infinity; then reevaluate the same CMB+DESI+Dovekie cosmology without freezing a massless-CDM transfer function.
2. Build a genuinely independent multi-tracer RSD+lensing likelihood (published covariance and AP/growth selection functions), concentrating on species-specific redshift response and marginalizing biases correctly.
3. Construct explicit shift-symmetric or monodromy two-field dark Lagrangians and evaluate periodicity, radiative thresholds, SUSY-breaking and uplift **in the same EFT**, instead of combining unrelated working modules.
4. Turn the uncommitted small-L overlap regulator into a sector-aware sparse solver for actual exotic charge Q=15, test low modes/index and gauge-current reconstruction, then confront the nonperturbative 2026 measure constructions.
5. Test multi-distance gravitational entanglement *and* complementary quantum clocks for retardation, mediator locality, source composition and electromagnetic/decoherence nulls, rather than proclaiming a graviton from a single entanglement witness.
