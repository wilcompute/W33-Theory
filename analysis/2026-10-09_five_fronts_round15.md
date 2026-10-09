# W33 Theory of Everything research — Round 15: five fronts plus two further mathematical results
**Date:** October 9, 2026. **Baseline:** GitHub master 6a47bd45a9ad7765a877b021913c8cc4ed3f55c4. **Scientific status:** finite exact statements and model-specific necessary conditions; no established Theory of Everything.

## Independent provenance and parallel-agent context

Reviewed current parallel history and scripts, including Claude-track Passes 11713–11716 (E8 SU(9) two-qutrit levels), Passes 11802–11807, the previous Pass11797–11801 actual Z6-II 176-field benchmark metadata, and prior Round14 quantum/optical/isospectrality code. Commit 6a47bd45 reserved Pass11802–11809 but only changed data/w33_formula_search_universe_v1.json; the **subsequent** commit 6b2129ef supplies genuine Pass11802–11807 analyses. Their corrected Z6-I count is 33 core models (31 with cubic up texture), rather than the earlier 28. Most importantly, parallel Pass11806 EXPLICITLY establishes that the separate **Z6-II** Codex benchmark has D7+U1 theta-squared classes rather than the SU(9)/A8 class: its full two-qutrit level dictionary does NOT literally apply to our n81 cubic. This pass respects that firewall and uses the original benchmark's own recovered charges and fixed-point data. No parallel mathematics was overwritten or reattributed.

Ownership from earlier passes: Pass11769 supplies the full 160-current 78D differential Hamiltonian; Pass11778 gives its previously published qualitative spectral results, not any new numeric global lower bound here. Round14 proved rank16 magnetic curvature at one special rational point, 80-flag Levi full-band isospectrality across 86400 optimal three-flag selectors, and clipped paired optical protocol. The n81*n17*n82 candidate is Pass11797 prior work. We independently created six fresh Round15 certificates.

## Frontier 1: the noncompact classical zero set is MUCH larger than a Hessian tangent space

The exact classical W33 current-square symbols are J_e(q,p)=(V_e.q+a)(U_e.p+a), e=1..160 and a=1/sqrt20, acting on the physical 78-dimensional point-plus-line augmentation for BOTH q and p.

For each of **40 W33 points**, set q=a*(39 at chosen point, -1 at all other points, zero at all lines); for each of **40 W33 lines**, set q=-a*(39 at chosen line, -1 at all other lines, zero at all points). Direct integer computation on all 80 cases shows **exactly four active affine z factors**; the other 156 are exactly zero. The 4 integer U0=40U vectors have universal exact Gram G=(1600 I4+1520 J4), with eigenvalues (1600,1600,1600,7680), and therefore independent rank4. For each star, the physical momentum reference p0/a=-(sum of these four U0 rows)/192 solves U_active.p0+a=0 exactly.

Every p=p0+delta with U_active.delta=0 remains an **exact** classical zero of ALL 160 currents; this is a 74-dimensional affine momentum plane in the 78D physical momentum space. All 80 star q anchors yield distinct sets of active flags. These 80 exact noncompact classical zero subspaces improve on the prior observation that one classical Hessian has nullity74: they are NOT merely tangent directions.

Thus strictly classical confinement is impossible along these spaces. The actual quantum operator can still have compact resolvent and a gap from operator commutators/subellipticity (previous Pass11778); this pass does **not** provide a numerical global ground energy lower enclosure. Producer: analysis/w33_20261009_round15_eighty_classical_zero_planes.py, all 80 active sets and two reference p certificates in JSON.

## Frontier 2: direct original Z6-II orbifolder charge twins expose a corrected-R veto

The original benchmark source data/w33_pass11797_full_benchmark_metadata.json.gz has explicit exact q (nine Abelian charges), twists k, fixed_point_translation, corrected RQ, G and oscillator_count per field. We separately checked the latest parallel Z6-I two-qutrit family-level result rather than assuming it describes this Z6-II field coupling.

The fields n81 and n83 share ALL nine Abelian charges, identical k=5 sector, G labels and a fixed-point translation. However they differ in oscillator content and corrected R charges. The candidate n81*n17*n82 has twist degrees 5+2+5=12=0 mod6, exact zero nine-charge sum, and corrected R/nonR congruence residuals [0,0,0]; it passes those **necessary** conditions. Replacing n81 with its same-Abelian-charge twin n83 preserves charge neutrality, k and fixed-point input but gives corrected R residuals [4,1,0], so the cubic n83*n17*n82 is vetoed.

The conventional SU3 Z3 and SO4 Z2xZ2 fixed-point translation congruences, applied to the source's six lattice-coordinate translation vectors, pass for the two configurations, and therefore do not distinguish them. This is a **partial necessary-congruence check**, NOT a complete product of conjugacy-class representatives in the orbifold space group. Neither fixed-point worldsheet instantons nor Rule4/5/6 nor the physical amplitude lambda of the admitted n81 cubic was computed. We do NOT claim F-flatness fails, nor that the physical cubic is nonzero.

Source-faithful contrast is essential: an identical gauge weight need not mean an identical allowed physical coupling, because corrected R and oscillator selection can separate physically distinct localized states. Producer: analysis/w33_20261009_round15_heterotic_charge_twin_rule.py, source SHA fingerprint and both full exact witness rows frozen to JSON.

Related published literature: Kobayashi, Parameswaran, Ramos-Sanchez, Zavala, arXiv:1107.2137 (additional torus lattice and instanton rules); CFT twisted coupling amplitudes are not inferable from gauge/R alone.

## Frontier 3: exact generically FULL-RANK curvature of the actual 78D quantum connection

The quantum kinetic metric and first-order effective connection are K(q)=Uᵀ diag(z²)U and A(q)=K(q)^-1 a Uᵀ z² where z=V q+a. Its curvature dA is an antisymmetric 78x78 rational function of normalized rational coordinate inputs q=(a/10)D k, with D the fixed 80x78 integer augmentation chart and dual cotangent normalization essential.

Round14 proved **exact rational rank16** at one symmetry-reduced point. This time we computed the entire curvature **modulo independent primes 10007 and 10009**, using exact modular inverses of K at a collection of rational physical positions. Certified Fp rank profiles, same at both primes:

| position | rank over both tested finite fields |
|---|---:|
| all coordinates zero | 0 |
| one-coordinate symmetry-reduced position | 16 |
| point-only two-coordinate displacement | 22 |
| mixed point/line four-coordinate displacement | **78** |
| mixed point/line eight-coordinate displacement | **78** |

At the explicit four-coordinate position, both primes have **nonzero 78x78 exact finite-field curvature determinants and invertible kinetic matrices**. Consequently the rank over Q is *exactly* 78 at that rational configuration. More strongly, the rational determinant/Pfaffian is a nonzero rational function, so the effective curvature has maximal possible rank **generically on a nonempty real Zariski-open set** wherever K is nonsingular. The rank16 point is a special lower-rank locus. Fp rank22 by itself is ONLY a rank>=22 over Q witness; Fp rank0 at origin is not by itself an exact rational zero proof.

This identifies a mathematically nondegenerate effective two-form on generic configuration space. It is NOT automatically a physical electromagnetic field, a Berry curvature of an actual ground state, a Lorentzian spacetime metric, a proof of degeneracy or an actual vacuum PSp irrep. The numerical global E0/first excitation gap is still not enclosed. Producer: analysis/w33_20261009_round15_magnetic_generic_fullrank.py.

## Frontier 4: distribution-free causal optical *effect size* confidence interval, rather than just a null rejection

Previous Round14 paired active/sham protocol tested whether an optical-path effect exists at a specified alpha. This pass inverts the paired randomization test into a **finite-sample (1-alpha) two-sided confidence interval** for the causal effect on the *clipped detector output*. Define two clipped potential outcomes Y_{j1}(a),Y_{j2}(a), a=0,1, in each randomized pair, independent of the independent binary path assignment z_j. The triple pump/gate/route sign r_j is randomized independently of z_j and held fixed within pair. Let X=sum_j z_j*r_j*(Y_j1(observed)-Y_j2(observed)). The target finite-pair signed causal contrast is

tau=(1/(2M))*sum_j r_j[(Y_j1(1)-Y_j1(0))+(Y_j2(1)-Y_j2(0))].

Conditional on fixed potential outcomes, E_z[X/M]=tau. Full per-shot clipping at absolute threshold T bounds each randomized contribution by 2T; Hoeffding gives the level 1-alpha interval

tau in [ X/M - w, X/M + w ],

where w=2T sqrt(2 log(2/alpha)/M)+2eta+2TK/M accounts additionally for an **independently certified** direct switch-electronics leakage eta per reading and at most K arbitrary corrupted raw shots after assignment.

For Round14's M=8000 pairs, T=.15, eta=.0004, K=14, alpha=.01, the certified conservative half-width is approximately **0.01224343 in clipped detector-output units**. Across 30 seeded synthetic trials per arm, **30/30** optical-path-injected intervals exclude zero, **0/30** null and **0/30** electronics-only intervals exclude zero. Typical optical-path-injected lower endpoint ~0.08253. This is **not raw photon nonlinear phase**, is NOT hardware data and does not by itself isolate a quartic mechanism from some other physical path difference. Without the independent leakage/fault budget, no such guarantee is claimed. Producer: analysis/w33_20261009_round15_optical_causal_effect_CI.py.

## Frontier 5: ALL FIVE W33 orbit phases separated by intrinsic multiway correlators

Round14's full-band theorem says that all 86400 optimal three-flag selectors have exactly the same single-particle 80-band Peierls-phase characteristic polynomial. This rules out distinguishing orbits by **eigenvalue-only single-particle band spectroscopy**, not by all spatially resolved observables.

Define PP[x,p]=1 when W33 points x,p are collinear (excluding equal points), LL[L,l]=1 when lines L,l meet, and N[x,l]=1 when point x lies on line l. For selected three flags with points p_i and lines l_i, define THREE PSp-invariant native incidence correlation counts:

Cp=sum_x prod_{i=1}^3 PP[x,p_i],
Cl=sum_L prod_{i=1}^3 LL[L,l_i],
J=sum_x (prod_{i=1}^3 PP[x,p_i])*(sum_{i=1}^3 N[x,l_i]).

These are triple-source/conditional-four-body geometric motifs, not measured physical multi-photon correlations. **The complete five orbit signatures** are:

| PSp orbit size | Cp | Cl | J |
|---:|---:|---:|---:|
| 4320 | 4 | 0 | 3 |
| 4320 | 4 | 2 | 3 |
| 25920 | 1 | 0 | 1 |
| 25920 | 1 | 2 | 1 |
| 25920 | 1 | 2 | 0 |

Thus the three native correlators distinguish **all five** inequivalent symmetry orbits, including the two generic orbits that shared the previous (Cp,Cl) signature. Each can be made the unique lowest **orbit** of a finite PSp-invariant integer Hamiltonian H=w_p Cp+w_l Cl+w_J J, with the following exact small coefficients in table order:

[-1,+1,0], [-1,-1,0], [+1,+1,0], [+1,-1,-1], [0,0,+1].

The exact positive gap to other orbit classes is 2,2,2,1,1 respectively; the ground-state degeneracy remains the orbit cardinality 4320 or 25920. These local incidence polynomial Hamiltonians are **engineered finite mathematics**, not a microscopic derived interaction, spontaneous thermodynamic symmetry breaking, or emergent relativistic gravitational continuum. A spatially resolved multiway correlator could in principle evade the band-only spectral no-go; no photonic hardware for it is claimed. Producer: analysis/w33_20261009_round15_complete_five_orbit_interactions.py.

## Exact tests and reproducibility

From repo root run: python -m pytest -q tests/test_w33_20261009_five_fronts_round15.py.

All Round15 scripts expose deterministic certificate() entrypoints and write accompanying JSON outputs under data/. New files are isolated from any concurrent agents' preexisting modifications. No original source paper, website, upstream data, other agents' local dirty files or benchmark frozen datasets are overwritten.

## Five independent next advances

1. **Subelliptic quantum lower enclosure despite 80 exact flat classical momentum planes.** Analyze the nonlinear bracket terms normal/tangent to the 74-dimensional leaves and produce rigorous constants in an exterior IMS/commutator inequality sufficient to compute E0 and the first excitation, not just a qualitative theorem.
2. **Real Z6-II CFT amplitude for n81*n17*n82.** With actual constructing-element representatives and oscillators, evaluate complete orbifold Rules4–6 and worldsheet instanton saddle and coefficient; then solve FI-corrected full F/D flatness without scaling the VEV background to zero.
3. **True vacuum PSp representation.** Use the generically rank78 curvature and its exceptional rank strata in certified group-projected quantum lower/upper sector energy bounds; establish the ground irrep rather than inferring it from curvature alone.
4. **Measured causal optical experiment with calibrated leakage and fault budget.** Build a blinded path intervention, independent optical reference and sensor swaps, validate the fixed potential-outcomes/randomization assumptions and infer a confidence interval for a *specific* calibrated optical nonlinearity, not just clipped detector voltage.
5. **Derive genuine interactions and a native continuum from the five orbit-selecting motif energies.** Test realizable multiphoton nonlinear couplers, exact 3-body coincidence/four-body conditional amplitudes and infinite-limit dispersion. Show that a selected orbit produces measurable distinctions beyond one-particle eigenvalues, and derive—not assume—spatial dimension and Lorentzian metric.

**Epistemic boundary:** no demonstrated Theory of Everything, quantitative global W33 quantum mass gap, physical heterotic vacuum, realized nonlinear photonic gate or emergent Einstein gravity is asserted.
