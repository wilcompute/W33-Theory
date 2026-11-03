# 2026-11-03 — Outside W33: TOE audit and three independent dark-sector consistency tests

**Executive finding:** The strongest present opportunity is not another W33–exceptional-group coincidence; it is an empirically constrained dark-sector field theory whose background, growth, quantum corrections, and galaxy scales must be accounted for by one Lagrangian. This round derives a constant-clock falsifier against the fitted CPL central trajectory, an idealized matter-era baryon/CDM bias and joint observable inversion, and a conditional ultralight scalar-dark-matter loophole to the existing heavy-particle radiative problem. **This is not a TOE, not a new discovery, and not a new cosmological-data fit.**

## Actual repo and local audit

At intake, `wilcompute/W33-Theory` and `C:\Repos\Theory of Everything` were synced at `59151dee68a85202d3770f7c92c30498f3de7d08`, with a clean staging index and 54 preserved local tracked/untracked working entries. The GitHub sequence since the previous Nov2/3 phase report includes:

- `60ae56bf` and `11e73d595`: exact 27-coordinate product and native qutrit/vacuum/kagome controls, with scope limitations.
- `6d6432fe`, `86b133b9`: independent q7/q9 even-set solver controls and q7 minimal hyperoval/cube classification; substantial finite mathematics, not a TOE.
- `22ae8fc22`, `68c0b327`, `6e84d4b00`, `4b61d4c50`, `e55ad2797`, `e7264c1ea`: non-W33 constraints, gravity/no-AdS3, Higgs scheme stability, chiral matter and real SN/BAO likelihood work.
- `b5b4db003`: actual patched CLASS/CMB/BAO/SN fitting of fading CDM. Full Planck plik-lite + DESI DR2 + Dovekie best-fit dark-sector slope `cp=0.05299751293406564`, `c=-0.9014357644`; conditional cosmological preference; matter-drag fixed point; coupled-moduli stability and clock constraints.
- `aae4f41f5` and `59151dee68`: physical-completion falsifiers and publication. An actual neutral SUGRA completion is SUSY AdS, heavy field-dependent CDM threatens a light scalar radiatively, a specified 1+1D 3450 chiral mirror is realizable, and sterile charge spectra plus gravity interferometry have additional model and interpretation requirements.

We also inspected the 201-line unpublished local `analysis/2026-11-03_toe_mechanism_completion.md` and several of its producers. That different in-progress packet contains engineered nilpotent uplift, 4D overlap index, Dirac-neutrino messenger chain, and gravity-identifiability controls. **Those unpublished local files and all unrelated working changes were preserved, not staged or copied.** This audit is of commit subjects, several full latest physics reports, raw fit records, representative actual producers and local mechanism work; it is NOT a claim to have read every file in the enormous repository.

## Research/priority checks before new calculations

- [DESI DR2 publication index](https://data.desi.lbl.gov/doc/papers/dr2/) and [DES-Dovekie SN 2026 recalibration](https://doi.org/10.1093/mnras/stag632): some evolving-DE fit improvements survive, but the Dovekie calibration reduced nominal 4.2 to 3.2 sigma and gave only weak Bayesian odds (~5:1). Treat a best fit as a target, not a detection of a microscopic model.
- [Antusch, King & Wang JCAP09(2026)115](https://doi.org/10.1088/1475-7516/2026/09/115): canonical scalar coupled to CDM can produce apparent effective phantom dark energy without a ghost if the early field is frozen and its late dynamics turn on. This background mechanism is PRIOR physics.
- [Amendola PRD62,043511 (2000)](https://doi.org/10.1103/PhysRevD.62.043511) and [Amendola–Tocchini-Valentini PRD66,043528 (2002)](https://doi.org/10.1103/PhysRevD.66.043528): phiMDE attractor and species-dependent linear baryon bias are established. We reproduce a narrowly defined analytic test-species limit, NOT a new cosmological perturbation theory.
- [D'Amico–Hamill–Kaloper PRD94,103526 (2016)](https://doi.org/10.1103/PhysRevD.94.103526): light axions/mixed light sectors can evade heavy varying-DM naturalness constraints; the general idea is PRIOR physics.
- [Liu, Gong & Zhou JCAP09(2026)051](https://doi.org/10.1088/1475-7516/2026/09/051): pure fuzzy DM lower bound m>1.9e-21 eV under the stated Lyman-alpha analysis, with different mixed-fraction bounds. These constraints cannot be adopted unchanged for an interacting model.
- [Yang et al EPJC86,1115 (2026)](https://doi.org/10.1140/epjc/s10052-026-16366-9): new DESI multi-probe RSD constraints remain consistent with zero coupling for studied phenomenological models; current data are not definitive interacting-dark-sector evidence.

## Experiment A — exact canonical scalar clock reconstruction and no-go for the central CPL shape

Producer `analysis/toe_20261103_dark_sector_consistency_triangle.py`; certificate `data/toe_20261103_dark_sector_consistency_triangle.json`.

Declare Einstein gravity, ordinary baryons/radiation, canonical x=phi/Mpl, and CDM particle mass m(x)=m0 exp(-beta x). Freeze beta=0.05299751293406564 from the repository's published full-Planck/Dovekie *fading* fit. For a deliberately simple scalar clock x=s N, N=ln a, choose present densities from the independent **CPL** best-fit panel in the same frozen fit JSON and Omega_r=9.2e-5 as a declared illustrative radiation prior. These DIFFERENT best-fit parameter sets are intentionally mixed to create a shape diagnostic, not represented as a self-consistent likelihood fit.

The Raychaudhuri/Friedmann equations yield an exact, positive background in 0<=z<=2:

`E2(N)=C exp(-s²N)+[3Omega_b/(3-s²)]exp(-3N)+[3Omega_c/(3+beta s-s²)]exp(-(3+beta s)N)+[4Omega_r/(4-s²)]exp(-4N)`

where C makes E2(0)=1, and the required potential is exactly

`V/(Mpl² H0²)=3E2 -rho_b-rho_c-rho_r - E2*s²/2`.

The code independently verifies the scalar Klein–Gordon and interacting continuity equations at five redshifts to better than1e-11. The equivalently uncoupled effective density is

`rho_de_eff=rho_phi+rho_c(today) a^-3 [exp(-beta s N)-1]`,

so the **exact** inferred effective equation of state is

`w_eff=-1+(H² s²+rho_c-rho_c(today) a^-3)/rho_de_eff`.

Note: rho and H use common units Mpl²H0², beta includes the sign convention in the CLASS patch. For small negative s, w_eff can be < -1 while canonical w_phi is >= -1; this is an established effective energy-transfer phenomenon, not a ghost.

The CPL central fit has w0=-0.8093548015, wa=-0.6853038517. Setting `|s|=sqrt[3Omega_DE(1+w0)]=0.6274115` exactly matches w0. The two sign branches then predict

| Input phi derivative sign | Predicted local wa tangent | w_eff(z=1) |
|---|---:|---:|
| positive s | +0.1569888490 | -0.5675960266 |
| negative s | +0.1316465844 | -0.6337727441 |
| actual CPL fitted central trajectory | -0.6853038517 | -1.1520067274 |

Thus this specified simple **constant-speed** scalar clock cannot reproduce both central CPL coefficients at the frozen beta. This is *not an observational likelihood exclusion* and *not a refutation* of the actual fitted, time-dependent CLASS fading model: it proves that changing the scalar velocity over cosmic history is essential to mimic this central target. The reconstructed multi-exponential V is supplied, not selected by a UV theory.

## Experiment B — baryon/CDM growth bias, cross-era mass drift and observable identifiability

The exact idealized phiMDE saddle of a coupled canonical scalar with beta, negligible baryon density and negligible scalar potential has

`phi_prime/Mpl = 2 beta; Omega_phi=w_total=2 beta²/3; rho_c∝a^(-3-2beta²)`.

The subhorizon CDM growing mode and uncoupled *test-baryon* tracking ratio solve a two-species linear ODE and admit exact expressions

`delta_c∝a^(1+2 beta²)` and

`delta_b/delta_c=(3-2 beta²)/[(1+2 beta²)(3+2 beta²)]`.

For the actual frozen beta=0.0529975129: growing exponent 1.00561747, test-baryon/CDM bias 0.9906968052, ideal unscreened dark-sector `Geff/G=1+2beta²=1.005617473`. Independent numerical ODE integration reproduced the analytic values within 6.2e-12. **This 0.93% slip is an idealized phiMDE benchmark, not a prediction for the real late-time multi-component universe or current RSD constraints.** Baryon gravitational backreaction, halo bias, baryonic physics, non-negligible V, screening and a full CLASS fit are still needed.

The frozen CLASS best-fit field values are `phi_today/Mpl=0.3845070556`, `phi_rec/Mpl=0.1049129674`, so the CDM particle-mass ratio is exactly `m_rec/m_today=exp[beta*(phi_today-phi_rec)]=1.0149281190`. Naively extending the early phiMDE saddle from recombination to today would give 1.0401288855 instead. They are **not inconsistent**: the phiMDE saddle does not hold through the radiation and DE eras.

Independent observable producer `analysis/toe_20261103_dark_sector_observable_identifiability.py`. On subhorizon unscreened massless scalar scales, the two phenomenological observables `D=ln(m_rec/m_today)=beta*DeltaPhi` and `g=Geff/G-1=2beta²` have exact Jacobian determinant `-4beta²` with respect to (beta,DeltaPhi). For nonzero beta they identify its magnitude and the excursion modulo the simultaneous sign ambiguity. A finite-range Yukawa scalar with unknown comoving mu makes one growth scale insufficient; two growth scales yield

`1/g(k)=1/(2beta²)+mu²/(2beta²*k²)`,

so slope/intercept determine `mu²` and beta². The frozen synthetic control mu=0.03 h/Mpc, k=0.05 and0.2 h/Mpc is reconstructed at machine precision. This massive scalar is an **instrumental identifiability stress-test**, not the repository's actual H0-scale rolling field. The signal is only 0.562% in G at beta=.053; growth data must resolve small effects and distinguish baryons from CDM.

## Experiment C — a conditional ultralight bosonic dark-matter window

The previous exact 4D *fermion* one-loop naturalness benchmark in `analysis/toe_20261103_dark_radiative_stability.py` gave a ~0.017 eV field-dependent mass upper scale under its specific scheme and no protection. That is neither a measured bound nor a universal exclusion.

Consider instead canonical real ultralight scalar dark matter chi with a field-dependent quadratic mass, `Vchi=0.5*mchi0² exp(-2beta phi/Mpl)*chi²`, and a separate canonical quintessence phi with a still-unknown technically natural V(phi). If mchi >> H it oscillates coherently and behaves as coupled dust on sufficiently long scales.

For an explicit input mchi0=1e-20 eV, a factor ~5.3 above the September2026 **pure-FDM** Lyman-alpha lower limit, the supplied standard-radiation/matter background gives:

- H0=1.4466703e-33 eV, mchi/H0≈6.91e12.
- Oscillation onset when H=mchi at z≈26,844,452; at recombination mchi/H≈2.94e8, so the adiabatic oscillator approximation is comfortably valid then.
- Present coherent amplitude chi0/Mpl≈1.815e-13; extrapolated onset amplitude chi_osc/Mpl≈0.0252 (assuming dust redshift scaling from onset).
- Instantaneous comoving Jeans k(z=5)≈444 Mpc^-1 for the stated effective nonrelativistic scalar perturbation estimate. This is **not** the Lyman-alpha transfer-function calculation; radiation-era suppression and nonlinear hydrodynamics still matter.
- Real-boson one-loop curvature in the explicitly chosen `MSbar`-style benchmark scales as beta²*mchi⁴/(8pi²*Mpl²). It is approximately **2.87e-74 H0²** at this mass. The corresponding single-field one-loop curvature scale is ~0.0243 eV, versus mchi=1e-20 eV.

Therefore, at the level of this toy EFT, the oscillating-boson option can be both cold-like at BAO scales and radiatively innocuous. **It is not a fit for interacting fuzzy dark matter**, and the published pure-FDM Lyman-alpha limit cannot simply be reused as an exclusion/passing certificate for the coupled model. Also: postulating mchi(phi) does not derive its shift-symmetry protection or compatibility with quantum gravity, and no matter-action/V(phi) UV origin is supplied. The 2016 dark-monodromies paper already investigates light-axion protection; no novelty priority is claimed.

## What actually constrains a TOE now

The chain of independent constraints is much sharper than matching a graph eigenvalue to a measured coupling: a single field theory must pass CMB/BAO/SN and RSD/weak-lensing likelihoods with a consistent perturbation theory; the dark particle must form galaxies and respect phase-space/free-streaming constraints; the quintessence potential must survive heavy particle and SUSY-breaking loops; the model must possess a controlled positive vacuum, correct 3+1D chiral gauge content, observed neutrino masses/flavor and a self-consistent UV interpretation; and it must make at least one genuinely parameter-free or tightly correlated prediction beyond the data used to calibrate it.

There is currently **no published common action** accomplishing all of that in the repository. Some local uncommitted mechanism code addresses pieces (nilpotent uplift, overlap 4D index, Dirac neutrino messengers), but those pieces are model assumptions with independent cutoffs, scalars and couplings. They are expressly not represented as already unified by this analysis.

## Reproducibility and limits

- Run `python analysis/toe_20261103_dark_sector_consistency_triangle.py`.
- Run `python analysis/toe_20261103_dark_sector_observable_identifiability.py`.
- Run `python -m unittest discover -s tests -p test_toe_20261103_nonw33_dark_sector_falsifiers.py -v`.
- Frozen JSON records actual fit values and source distinctions, analytic formula residuals and numerical controls. Focused tests are not a full repository CI run.
- No new Planck, ACT, DESI, RSD, Lyman-alpha, or supernova likelihood has been evaluated in this pass. **The only signal-to-noise and significance statements come from the explicitly cited published work and existing repository fits.**

## Five independent next experiments

1. Implement oscillating-field perturbations for mchi(phi) consistently in CLASS, with nonlinear transfer predictions and Lyman-alpha likelihood as a **new interacting-FDM model**, not a naive import of pure-FDM bounds.
2. Measure the baryon/CDM relative growth and weak-lensing response by integrating the full beta=.053 CLASS solution, then compare to the actual 2026 RSD and CMB lensing covariance without treating 0.5% as an automatic detection.
3. Find or rule out technically natural UV protection for a two-scalar fading sector in the presence of the positive-energy SUGRA uplift and visible-sector portal from the unpublished local mechanisms.
4. Turn the 4D overlap-fermion index sector and Dirac-neutrino messenger Lagrangian into an anomaly-free, gauge-invariant **single** regulated chiral action with mass hierarchy and flavor controls.
5. Run a blind predictive holdout on later-independent cosmic chronometer/lensing/SN calibrations: classify model complexity/prior-volume costs and preserve data provenance rather than tuning to every dataset after viewing it.
