# W33-Theory — best available natural-constant derivations and competing formulas
**Audit date:** 2026-11-07  
**Audited branch:** master at `47683e807f8fd9347d3a7a4632668cafb9f34113`  
**Purpose:** One preferred repo expression for each distinct constant/observable, older alternatives retained, claim strength audited. This is a research catalog, **not** proof that W33 determines measured physical constants.

## Evidence rules
- **E** = exact **mathematical** finite-geometry, group, or spectral result (does not establish a physical identification).
- **R** = retrospective numerical relation to a measured observable; usually no unique action, renormalization, or holdout prediction.
- **C** = conditional physical calculation with supplied model, coupling, scale, or sector assignment.
- **D** = dimensional/SI definitional identity or needs an external unit scale.
- **O** = open/no defensible independent derivation; candidate retained only for comparison.
- **W** = withdrawn or contradicted as a physical derivation.

Selection favors (1) explicit source operator or invariant, (2) algebraically reproducible, (3) independently fixed physical mapping/units/scale, (4) resistance to formula-search multiplicity, (5) held-out predictive power. A small numerical residual alone is not a derivation. **None of the measured Standard Model or cosmological constants below has cleared all five tests.** “Best” means best **documented candidate**, not a validated W33 prediction.

## Substrate dictionary (genuine E mathematics)
Define q=3 for W(3,3) with SRG parameters (v,k,lambda,mu)=(40,12,2,4) and adjacency spectrum 12^1, 2^24, (-4)^15. The graph has E=vk/2=240 edges and 540 nonedges; the incidence Levi graph has 40+40=80 vertices, 160 flags/edges, and first Betti number 160-80+1=81. The finite symplectic group PSp(4,3) has order 25,920, and the full projective similarity group has order 51,840. Cyclotomic evaluations: Phi3=q^2+q+1=13, Phi4=q^2+1=10, Phi6=q^2-q+1=7, Phi12=q^4-q^2+1=73; q!=6, p_Ih=k-1=11. **Do not confuse** graph lambda=2 with Wolfenstein lambda, and mu=4 with particle masses.

## A. Electromagnetic, weak, strong, and unified couplings
| Observable | Preferred documented W33 expression | Other derivations or variants to retain | Audit |
|---|---|---|---|
| Fine structure, alpha_EM^-1(0) | **Numerically closest documented:** 137 + 1/28 + 4/14045 ≈ 137.035999085 (BT53; TOE master synthesis) | Exact graph skeleton 144-(2+4+1)=137=(11)^2+4^2=2^7+3^2; 137+1/28; spectral inverse response 137+40/1111=137.03600360036; 137+880/24445=137.0359991818; 137+1/27 | **R**. Four-term choice postselected, not a QED coupling calculation; operator-derived 40/1111 variant is substantially outside CODATA uncertainty. |
| Fine structure, alpha_EM^-1(M_Z) | 128-2/40=127.95 (master precision expansions) | 2^Phi6=128; 137-9=128 | **R**. Must specify the precise Z-pole running scheme, thresholds and independent derivation. |
| Alpha_EM running between 0 and M_Z | 9+1/28 (in TOE master synthesis) | 137.036-128~9.036; perturbative vacuum polarization is the actual physical mechanism | **R**. Difference of chosen endpoints, not an RGE derivation. |
| Strong alpha_s(M_Z) | 1/(110/13+1/74) ≈ 0.11799 (BT53) | 13/110≈0.11818 (TOE companion); 9/76≈0.11842 (earlier inventory); many explicit 2/3-loop RGE scripts with initial inputs | **R/C**. Parameter-dependent QCD running is physical; an integer ratio chosen after data does not supply the beta function and boundary condition. |
| Strong alpha_s(m_t) | alpha_s^-1=Phi4-q/mu=9.25 (so alpha_s≈0.10811) | RG-running scripts at top mass | **R/C**. Needs consistent two/three-loop scheme. |
| Weak mixing sin^2 theta_W(M_Z), MS-bar | 3/13+1/2200≈0.231224 (BT53 corrected) | 3/13≈0.230769 (simplest tree/finite ratio); thetaW from coupled running and EW thresholds | **R/C**. Precise correction chosen retrospectively. |
| Weak mixing at GUT normalization | 3/8=0.375, standard SU(5) representation normalization | Earlier papers sometimes mislabeled 3/13 and 3/8 as same-scale outputs | **C**. 3/8 follows from chosen embedding, not measured electroweak value. |
| GUT inverse coupling | **No single canonical answer:** 26=40-12-2=2*13 in some scripts | 24 (spectral multiplicity), 240 (E/2) elsewhere | **O**. Mutually conflicting scales/formulas; running and threshold normalization missing. |
| Higgs self-coupling lambda_H | Phi3/100=13/100=0.13 | Standard SM extraction lambda_H=m_H^2/(2v_EW^2) using measured Higgs mass and VEV | **R**. Denominator 100 not uniquely induced by W33. |
| Top Yukawa y_t | 1 | Standard y_t=sqrt(2)m_t/v_EW | **R**. Closeness to unity, not consequence of the finite graph. |
| Bottom/tau Yukawa ratio | Phi6/q=7/3≈2.333 | GUT boundary/renormalization-group relations; source companion | **R/C**. Scheme and reference scale required. |
| Fine-structure alpha_G gravitational coupling | (m_p/M_Pl)^2 ~ q^(-80)=3^-80 as proposed | Newton constant and proton mass set the actual dimensionless gravitational coupling | **R/D**. Two independently calibrated dimensional scales are required. |
| Neutron beta/vector weak constants, G_F | No source-level parameter-free G_F | Standard G_F=1/(sqrt(2)v_EW^2), with supplied VEV | **O/D**. |

## B. Flavor mixing, lepton observables, CP
| Observable | Preferred candidate | Other versions | Audit |
|---|---|---|---|
| Cabibbo | **Most elementary matrix candidate:** |V_us|^2=2/v=1/20; hence |V_us|≈0.2236068 | sin(13 degrees)≈0.22495; tan theta=1/sqrt(19)≈0.22942; 3/13 as tangent from later exact flavor spine; theta=13+1/25 degrees; +1/1428 fit for |V_us| | **R**. Angles/degree unit not a natural group-theoretic phase unless rotation representation is fixed. |
| CKM |V_ud|^2 | 1-2/v=0.95 | Row unitarity relation with other measured entries | **R**; not independent from preceding candidate. |
| CKM |V_cb|^2 | 1/[(mu+1)kPhi4]=1/600≈0.00166667 | Detailed paper section4 one-loop Hashimoto correction with input alpha_s(m_b) | **R/C**. |
| CKM CP phase delta_CKM | tan(delta)=Phi4/mu=10/4=2.5 (delta~68.2 degrees) | delta=pi/3; 13+1/25 degrees is Cabibbo; other alpha-supplemented alternatives | **R**. |
| Wolfenstein A | mu/(mu+1)=4/5=0.8 | Numerical CKM fits and RGE evolution | **R**. |
| PMNS solar sin² theta12 | mu/Phi3=4/13≈0.30769 | 33+4/10 degrees in finely corrected synthesis | **R**. |
| PMNS atmospheric sin² theta23 | **No unique winner:** 6/11≈0.54545 (TOE companion) | 7/13≈0.53846 (root W33, website exact flavor spine); 6/11+1/667; older theta23=45 degrees | **R/O**. Octant and mass-ordering evidence must choose the regime, not near-fit alone. |
| PMNS reactor sin² theta13 | 2/(Phi3Phi6)=2/91≈0.0219780 | Earlier W33 spectral angles | **R**. |
| PMNS CP delta | No agreed constant; -pi/2 in ultimate table | 14pi/13 in historic website; Wilson-loop +pi/2; old theta_CP~232 degrees | **O**. Incompatible branches; no established physical holonomy map. |
| Neutrino mass-squared ratio | v-q!=34 | 33=2Phi3+Phi6 on website; older 33 etc. | **R**. Scheme/data-dependence; multiple claims are not one theorem. |
| Sum of neutrino masses | No unique physical derivation | 30.7 meV in W36 and 100 meV in BT53; 3.07+9.21+18.42 meV in W36 is internally inconsistent with known atmospheric splitting | **O**. Need independently normalized seesaw/Weinberg operator plus fits. |
| Charged-lepton Koide Q | 2/3, if explicitly imposed as S3 singlet-doublet equipartition | Exact lightcone/spectral representations in pass251/257; Koide identity alone is mass relation not 3 masses | **R/C**. Physical dynamical mechanism not derived. |
| Muon/electron mass ratio | **Best numerically of cited W33 arithmetic:** 206 + 77/100=206.77 | 206=(mu+1)v+q!; 207=q²*23; 91²/40=207.025; later exact electron-packet ratio 208 (not physically identified) | **R**. Correction tuned after known value 206.768283. |
| Tau/muon, tau/electron ratios | No selected unique W33 derivation | Koide plus two measured masses; Yukawa-tower and Heegner fits | **O/R**. |
| Neutral-kaon CP magnitude |epsilon_K| | 1/[4*137-9*11]=1/449≈0.00222717 | Alternate loop/flavor constructions | **R**. Arbitrary arithmetic cannot substitute a K0 mixing Hamiltonian. |
| Muon anomalous magnetic moment *discrepancy* | Delta a_mu=3^-18≈2.581e-9 (historical) | Standard a_mu prediction is a quantum loop expansion, and discrepancy changes with theory/experiment updates | **R/O**. This is not the total a_mu, and the discrepancy is not a fixed natural constant. |
| Baryon asymmetry eta_B | No validated selection; W33_PREDICTIONS.json target 6.12e-10 | Sphaleron/leptogenesis scripts; entropy/logarithm candidate ~10^(-240/26) | **O/C**. Need decay rates, CP phases and washout, not a number match. |

## C. Charged particles, hadrons, electroweak spectrum
These formulae assign graph **numbers** to masses in **chosen MeV/GeV units**. Without an independently fixed energy conversion they are not physical mass derivations. All entries marked D/R.

| Observable | Preferred catalog expression | Other candidates/notes | Audit |
|---|---|---|---|
| Proton/electron mass ratio | k*q²*Ogg7=12*9*17=1836 | Other W33 ratios (exact observed ~1836.15267) | **R**. |
| W/proton mass ratio | q^(q+1)=81 | Experiment depends on pole and mass definitions | **R**. |
| Higgs VEV v_EW | E+q!=240+6=246 GeV | Independently fixed in SM by Fermi constant | **D/R**. |
| W boson m_W | 2v=80 GeV | One-loop model in PAPER_SECTION4B_MW_ONELOOP.tex, but takes supplied v_EW and couplings | **D/R/C**. |
| Z boson m_Z | Phi6*Phi3=91 GeV | m_W/cos thetaW from SM with input angle | **D/R**. |
| Higgs boson m_H | (mu+1)^q=5³=125 GeV | 2^Phi6-q=125 | **D/R**. Integer identity is exact; MeV/GeV assignment and mass dynamics are not. |
| Top quark mass m_t | Heegner163+Phi4=173 GeV | Phi3²+mu=173; multiple Yukawa-tower fits | **D/R**. |
| Tau lepton mass m_tau | Phi6(q²+2^q)/67=119/67≈1.77612 GeV | From Higgs Yukawa mass after supplying v_EW | **D/R**. |
| Strange quark m_s | Phi3Phi6=91 MeV | E6/Yukawa and L-infinity manuscripts; scale-dependent running mass | **D/R**. |
| m_s/m_d | v/2=20 | E6 metric; running ratios | **R**. |
| m_s/m_u | Heegner43=43 | running ratios | **R**. |
| m_top/m_b | Ogg12=41 | tree/running and experimental masses | **R**. |
| Pion charged mass | lambda*Phi4*Phi6=140 MeV | Numerical resonance and QCD computational approaches | **D/R**. |
| Charged neutron lifetime tau_n | 2v*p_Ih=880 s; refined 880 - q/(mu+1)=879.4 s | Weak decay rate with experimentally calibrated G_F and g_A | **D/R**. |
| Z leptonic branching (per generation) | 1/(qPhi4)=1/30 | Actual SM partial widths and radiative corrections | **R**. |
| Z invisible/neutrino branching | 1/(mu+1)=1/5 | Same Z width model | **R**. |
| Z hadronic branching | Phi6/Phi4=7/10 | Exact proposed bookkeeping 3*(1/30)+1/5+7/10=1 | **R**. Sum=1 is arithmetic tautology, not partial-width dynamics. |
| Cosmological acoustic sound horizon r_s | q*Phi6²=147 Mpc | corrected 147+2/v=147.05 Mpc | **D/R**. Unit insertion; external cosmology required. |

## D. Cosmology, inflation, composition and gravitational scales
| Observable | Preferred catalog expression | Alternatives / key limitation | Audit |
|---|---|---|---|
| Primordial scalar tilt n_s | 27/28+1/1639≈0.964896 | 27/28; earlier inflation 29/30≈0.9667 | **R/C**. Tilt requires inflationary dynamics and comparison against later independent data. |
| Matter clustering sigma8 | 13/16-1/2000=0.812 | 13/16=0.8125 | **R**. No amplitude power-spectrum calculation. |
| Omega_DM/Omega_b | 27/5+1/100=5.41 | 27/5=5.4 | **R**. |
| Omega_Lambda/Omega_DM | Phi3/(mu+1)=13/5=2.6 | Other dark-sector count assignments | **R**. |
| Fractions Omega_b/Omega_DM/Omega_Lambda | Normalize 1 : 27/5 : (27/5)*(13/5) -> (0.04902,0.26471,0.68824) | historical docs use 9/13 or 351/511 etc. for Omega_Lambda | **R**. Component fractions are dependent on two input ratios. |
| Hubble constant early / CMB | 67 km/s/Mpc = (2^7+3!)/2 | different W33 old fit 67.2 | **D/R**. |
| Hubble constant late / SH0ES | Phi12=73 km/s/Mpc | Different data sets and calibration disputes | **D/R**. |
| Hubble discrepancy | 73-67=q!=6 km/s/Mpc | Not a fundamental constant; difference of two observational inferences | **D/R**. |
| Cosmological constant rhoLambda/M_Pl^4 | q^(-mu^4)=3^-256~10^-122.14 | other proposals based on 1/v², zero-point spectral zeta, toroidal counts, 10^-120 | **R/O**. Huge exponent chosen, cannot derive vacuum energy; see explicit matching-to-rho caveat below. |
| Hubble/Planck hierarchy | H0/M_Pl = q^(-2^Phi6)=3^-128 | follows approximately as square-root power of vacuum ratio; not independent | **R**. |
| Electroweak/Planck hierarchy | mW/M_Pl=3^(-36); vEW/M_Pl=3^(-35) | scalar hierarchy models and W33 q-ladder | **R/D**. Absolute scale boundary. |
| Proton/Planck hierarchy | mp/M_Pl=3^-40 | m_Pl≈3^40 GeV identity only if unit GeV is supplied | **R/D**. |
| Helium primordial mass fraction Yp | 1/4-1/333≈0.246997 | 1/mu=0.25 | **R**. Requires BBN nuclear-network rates and N_eff. |
| Reionization optical depth tau_reion | Phi6/(Phi3Phi4)=7/130≈0.05385 | other fits | **R**. |
| First CMB acoustic peak ell1 | C(k,3)=C(12,3)=220 | higher peaks attributed to other binomial expressions | **R**. Need full acoustic transfer function. |
| Effective neutrino count N_eff | q+mu/(Phi3Phi6)=3+4/91≈3.04396 (candidate) | Standard SM neutrino decoupling physics | **R**. |
| Inflation e-fold number N | 2(v-Phi4)=60 | 50–60 from phenomenology | **R**. |
| Inflation tensor-to-scalar r | 12/N²=1/300 for chosen Starobinsky-like model | other direct W33 candidates; not measured detection | **C** (assumes the model). |
| Dark-energy equation of state w0 | No independent derivation; W33_PREDICTIONS.json says -0.9847 | Current November 2026 dark-sector fitted fading models versus LCDM and CPL | **O/C**. Fit parameters/model selection, not a universal constant. |
| DM relic abundance Omega_chi h² | 0.1201 in dark_matter_section.tex | Freeze-out equation includes assumed cross section, masses and cosmology | **C**, not zero-parameter. |
| Baryon-to-photon eta_B | 6.12e-10 stored target | See leptogenesis scripts; washout and source phases not fixed | **O/C**. |
| Cosmological constant via spectral zeta | rhoLambda=(hbar*c/a^4)*zeta_W(4)/v | paper/section_cosmology.tex determines *a* by setting observed rhoLambda, reversing inference | **C/D**, **not** prediction of rhoLambda. |
| Hawking / Page time, entropy | Historical formulas S_BH=v=40, T_H=q!=6, Page time 6.1e67 solar-mass years | Area, mass, Planck constant and gravity are external physical inputs | **O/C**. |

## E. Dimensional constants and the SI definitions — crucial no-go
| Constant | Actual status | Repo claim and why it is insufficient |
|---|---|---|
| Speed of light c | **D/O** | Its numerical SI value 299,792,458 m/s is exact **by definition**. Factorizations of decimal digits cannot predict an invariant speed without geometry and independently fixed clocks/lengths. |
| Planck h and reduced hbar | **D/O** | h=6.62607015e-34 J s is exact by SI definition; hbar=h/(2pi) is an algebraic definition. W33 phase-step or unit normalization does not derive physical h. |
| Elementary charge e | **D/O** | e=1.602176634e-19 C fixed by SI definition; no independent electric-charge normalization from W33 is shown. |
| Boltzmann kB | **D/O** | kB=1.380649e-23 J/K exact SI definition; converting statistical temperature to SI units requires reference conventions. |
| Avogadro NA | **D/O** | 6.02214076e23 mol^-1 defined exactly; no microscopic dynamical deduction needed or possible from graph count alone. |
| Cesium hyperfine frequency Delta nuCs | **D/O** | 9,192,631,770 Hz defines the SI second. Its chosen integer factorization is not a prediction of atomic energy splitting. |
| Luminous efficacy Kcd | **D/O** | 683 lm/W at 540 THz fixed by SI convention; observer/perception photometric definition. |
| Newton G | **O** | Measured dimensional gravitational coupling. Various W33 actions/RG fixed-point guesses do not select its SI magnitude or reproduce independently Einstein gravity. |
| Absolute particle masses | **O/D** | Graph-count GeV/MeV arithmetic does not calibrate the natural-energy scale; the scale covariance counterexample rules out selection by finite dimensionless incidence alone. |
| Cosmological H0 and Lambda | **O/D** | Unit-bearing values require measured seconds/meters/M_Pl or an independent calibrated cosmological action and boundary conditions. |

**Reason this is a genuine obstruction, not semantics:** the October 19 scale test shows H->sH, T->sT, kappa->s kappa, t->t/s preserves normalized Gibbs distributions, graph projectors and unitary propagators. Therefore dimensionless finite incidence alone cannot fix *any* absolute energy, time, c, G or h. Adding a suitable physical action/clock/boundary condition might evade the no-go, but would be an additional explicit input.

## F. Exact mathematical constants and invariants, NOT physics parameters
These are the most defensible truly derived numbers:

| Invariant | Exact derivation | Level |
|---|---|---|
| Points of W(3,3) | (3^4-1)/(3-1)=40 | E |
| Degree, intersection numbers | (k,lambda,mu)=(12,2,4) by the symplectic generalized quadrangle W(3,3) | E |
| Edges and nonedges | 40*12/2=240; C(40,2)-240=540 | E |
| Adjacency spectral multiplicities | 12^1 + 2^24 + (-4)^15; multiplicities 1+24+15=40 | E |
| Automorphism orders | PSp(4,3)=25,920; PGSp(4,3)=51,840; distinguish from Sp(4,3) double cover | E |
| Polar lines/contexts | 40 lines, each 4 points; 160 flags | E |
| Levi cycle dimension | 160-80+1=81 | E |
| Levi 8-cycle count | 1,620 apartments/cycles in generalized-quadrangle building | E |
| Graph projector rank | E4=(1/160) CC^T has rank 81 (reported verified cycle-space identity) | E |
| E8 roots | 240 roots for E8 (standard root-system computation); coincidence with W33 edge count alone is *not* a physical canonical bijection | E |
| E8 Lie dimension | 248 roots+8 Cartan directions=248 | E |
| E6, E7, F4, G2 dimensions | 78,133,52,14 from standard root systems/representation theory, not merely matching W33 arithmetic | E |
| Fine-structure **integer** 137 | Multiple identities such as 12²-(2+4+1)=137, (12-1)²+4²=137 | E (arithmetic only) |
| Heawood/Fano 28 nonincidences | 7*7-7*3=28 | E |
| Extended Golay parameters | [24,12,8] is an independent coding-theory theorem; [f,k,k-mu] numerically matches | E for code, not forced existence by W33 alone |
| 3/8 SU(5) weak normalization | ratio of group traces under the stipulated SU5 hypercharge embedding | E/C, not a measured value at MZ |
| Golden ratio | (1+sqrt(5))/2 by x²-x-1=0; pi and e also have independent mathematical definitions | E; no need to attribute to W33. |

## Duplicate/conflict audit — do not silently merge
1. **alpha(0):** 137, 137+1/28, 137+40/1111, 137+880/24445, 137+1/28+4/14045. The two 137+40/1111 and 137+880/24445 are explicitly documented as inconsistent in docs/consistency_notes.md. The best numerical match is not the best theoretical mechanism.
2. **alpha_s(MZ):** 9/76, 13/110, 1/(110/13+1/74), and input-dependent QCD running. Choice of scale and scheme essential.
3. **thetaW:** 3/13 and 3/13+1/2200 are weak-scale candidates; 3/8 is GUT-group normalization. Do not report as one numerical output.
4. **alpha_GUT^-1:** 24 versus 26 versus 240 within the project; no consolidated derived coupling.
5. **PMNS atmospheric:** 7/13, 6/11, 6/11+1/667, and 1/2. The preferred published site still uses 7/13, the constants companion 6/11.
6. **PMNS CP:** -pi/2, +pi/2, 14pi/13 and ~232 degrees. No unique claim.
7. **neutrino mass-splitting ratio:** 33, 34, and fitted versions.
8. **muon/electron mass ratio:** 206, 206.77, 207, 207.025 and 208; none physical derivation.
9. **inflationary tilt:** 27/28, 27/28+1/1639 and 29/30.
10. **cosmological Lambda:** 3^-256, powers of 10, spectral zeta with an inferred lattice spacing, etc. None removes measured scale as input.
11. **generation count:** historical W33_PREDICTIONS.json stores n_generations=5, while the W33 SM narrative claims 3; require explicit definition and matching.
12. **W33 240 edges vs E8 240 roots:** numerical equality does not imply an equivariant identification; the site now explicitly distinguishes the proved local-axis lift from old unsupported statements.

## Evidence anchors (best sources read in this pass)
- **Current public index/site**: [docs/index.html](../docs/index.html) and [index.html](../index.html), verified rendered at https://wilcompute.github.io/W33-Theory/ . The public site explicitly demotes physical interpretations relative to exact geometry.
- **Two full constants manuscripts**: [toe_constants_companion.tex](../papers/standalone/toe_constants_companion.tex), [toe_master_synthesis.tex](../papers/standalone/toe_master_synthesis.tex).
- **Major TeX crosschecks**: [BT407_PAPER.tex](../papers/standalone/BT407_PAPER.tex), [W36_PAPER.tex](../W36_PAPER.tex), [W36_PRL_LETTER.tex](../W36_PRL_LETTER.tex), [w33_everything.tex](../w33_everything.tex), [W33_FOR_EVERYONE.tex](../W33_FOR_EVERYONE.tex), [paper/w33_preprint.tex](../paper/w33_preprint.tex), [paper/main.tex](../paper/main.tex), [paper/section_cosmology.tex](../paper/section_cosmology.tex), [paper/section_gravity_CC_supplement.tex](../paper/section_gravity_CC_supplement.tex), [single_photon_universal_computation.tex](../single_photon_universal_computation.tex), [photonic_holonet.tex](../photonic_holonet.tex), [paper/w33_holographic_tower_final.tex](../paper/w33_holographic_tower_final.tex), plus 19 individually inspected papers/standalone TeX files and the forty-points manuscript. This is **not** a claim that every TeX among the very large analysis/passes archive was individually read.
- **Code/JSON:** [ultimate constants table](w33_ultimate_substrate_constants_table.py), [BT53 precision constants](w33_BREAKTHROUGH_53_substrate_precision_constants.py), [physical constants summary](w33_TOE_physical_constants_summary.py), [cosmology observables](w33_cosmology_observables_substrate.py), [precision companion](w33_MLI_MLX_constants_companion_precision.py), [SI integer encoding](w33_MCCCLXXXII_all_SI_constants_substrate.py), [SI exponent encoding](w33_MCCCLXXXIII_si_exponents_substrate.py), [measured constants encoding](w33_MCCCLXXXIV_measured_constants_substrate.py), [physics inventory](../PHYSICS_INVENTORY.md), [masterkey](../docs/masterkey_table.md), [prediction targets](../W33_PREDICTIONS.json).
- **Negative/control evidence:** [formula drift note](../docs/consistency_notes.md), [prediction preregistration](../data/w33_prediction_registry_v1.json), [formula-search null audit](w33_frozen_formula_null_audit.py), [scale covariance no-go](w33_20261019_round6_scale_nogo.py), [scale result audit](2026-10-19_round6_chevalley_heptad_optics_scale.md).

## Bottom line
**W33 really determines its own finite-geometry invariants, spectral multiplicities, group orders, projectors and homology.** The repository also contains many intriguing expressions matching dimensionless measured constants, often after selecting among numerous alternatives. Until a normalized physical action and independent observable map supply unique couplings, renormalization prescriptions, masses and prospective predictions, these are mathematical/phenomenological candidates rather than derived laws of nature.

**Best independent next tasks:** (1) freeze a unique alpha(Q) action and predict a not-yet-used running measurement; (2) construct a common CKM/PMNS mass-and-phase model with predeclared scales and holdout data; (3) prove or falsify the scale-setting bridge for c, G, h and the cosmological constant; (4) automate a full-repo TeX/JSON/Python formula provenance and conflict ledger; (5) run multiplicity-adjusted retrospective null tests on every candidate, including the discarded ones.
