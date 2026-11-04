# Independent W33 five-front falsifier audit (plus phase-frustration certificate)

**Status: exact finite calculations with separately labeled numerical spectral/evolution checks.** Not an emergent 3+1 spacetime, nonlinear Einstein dynamics, physically predictive flavor model, or realized hardware circuit.

**Code:** analysis/toe_20261103_fivefront_independent_controls.py
**Tests:** tests/test_toe_20261103_fivefront_independent_controls.py
**Result:** data/toe_20261103_fivefront_independent_controls.json

## Repo and prior-art intake

Reused the verified 81-apartment, congestion-optimal H=BB^T construction from analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py, itself building on the 160 flags, 1620 apartments, and Steinberg cycle module already established by BT545-BT551, BT744 and related older work. The adjacency-polynomial flat-band no-go is already in analysis/2026_11_03_levi_flatband_locality_tradeoff.py. Local Maxwell plaquettes are already discussed in analysis/w33_20261010_toe38_local_maxwell_2complex.py. Standard E6 anomaly cancellation is already checked in analysis/w33_20261019_round13_chiral_anomaly_27.py.

This note adds **specific transvection-symmetry stress tests of the November 3 H**, a nonclosing gauge-invariant local-density Poisson bracket, an explicit 160-mode signed-coupling resource census, and a gauge-invariant negative-triangle obstruction. No research-priority claim beyond these specified calculations.

## 1. Continuum and conditioning

The unrefined W(3,q) Levi flag graph has degree 2q and diameter four; q=3 BFS yields eccentricity four at all 160 flags. Merely growing q does not create unbounded graph distances, a fixed-valence manifold triangulation, a physical length scale or a 3+1 Lorentzian metric. A separate refinement and a genuine continuum are required.

The selected H has 81 positive numerical eigenvalues ranging from 6.776153468e-5 to 23.29636527, condition number ~343799. Exact cycle-cut decoupling is not a physically robust energy gap.

External analytic anchor: fractal spectral decimation and heat kernels https://www.aimsciences.org/article/doi/10.3934/cpaa.2015.14.2509 .

## 2. The basis selects a symmetry frame

For each projective v in F3^4, form the symplectic transvection T_v(x)=x+<x,v>v, transport its action through the W33 lines and 160 point-line flags, then compare the 81-octagon support family and the conjugated H.

All 40 projective transvections tested; **zero** preserve the chosen support family. Relative Frobenius change ||H-THT^T||_F / ||H||_F ranges from 0.89117 to 0.95336. This is **not** proof that every optimal five-load family breaks every transvection; only the constructed family was tested.

Schur's lemma for the irreducible complex Steinberg module also prevents a non-scalar in-band operator from commuting with the entire symplectic group. Actual symmetry-selection dynamics, and any possible proper-subgroup invariance, remain to be built.

Prior transvection constructions already exist in the repo (e.g. analysis/w33_pass4472_4479_apartment_module_thermo_ihara_pauli.py).

## 3. Gauge invariance is not the Einstein constraint algebra

For a selected signed eight-cycle c_i, define an edge phase-space local density h_i=(c_i·x)^2/2 + sum_(e in supp c_i) p_e^2/2. D is the oriented 80x160 Levi incidence; G=D p are Abelian gauge generators. Because D c_i=0, h_i commutes with the Gauss generators.

Select cycles c_0 and c_15 with one shared edge and signed overlap -1. At exact integer data x=c_0, p=c_15, D p=0 yet the canonical bracket is:

**{h_0,h_15} = -7.**

So these specific gauge-invariant local quadratic densities fail to close into Gauss constraints alone. This is a constructive boundary against mistaking Maxwell-type gauge closure for the hypersurface-deformation algebra of general relativity. It is **not** a no-go for all possible gravitational discretizations.

Prior mathematical physics: Bahr-Dittrich discrete gravity constraints and pseudo-constraints https://research-portal.uu.nl/en/publications/from-covariant-to-canonical-formulations-of-discrete-gravity/ ; perfect 4D linearized discretization https://link.springer.com/article/10.1007/JHEP05%282022%29172 .

## 4. E6 chiral-matter control; anomaly cancellation does not predict a generation count

Standard E6 -> SO(10)xU(1) branching 27 = 16_(+1)+10_(-2)+1_(+4).
- U(1) gravitational coefficient: 16 - 20 + 4 = 0.
- U(1) cubic coefficient: 16 - 80 + 64 = 0.
- SO(10)^2 U(1): 2(1)+1(-2)=0 in standard index normalization.
- SU(5)^3 coefficient: 1-1+1-1=0 from 10+5bar+1+5+5bar+1.
- U(1)-neutral cubic representation channels: 16*16*10 and 10*10*1.

This is established E6 representation theory and a replay of repo controls, **not a novel model prediction**. Conjugate 27bar is also anomaly-free. Selection of handedness, three generations, particle masses, Yukawas, and vacuum remains open.

Literature: https://academic.oup.com/ptep/article/2014/11/113B03/2929939 and https://doi.org/10.1140/epjc/s10052-025-15043-7 .

## 5. Tight-binding experimental resource and perturbation budget

The 160x160 signed real H has **1883 nonzero undirected off-diagonal couplings**, with **871 positive and 1012 negative**, maximum 31 off-diagonal neighbors per flag and absolute coupling up to four. Flag participation loads are {3:9,4:134,5:17}. This is a mathematical target, not proof that such a coupler array can be manufactured or calibrated.

A single onsite potential lambda |e><e| leaks from the protected sector. For psi=P|e>/sqrt(p), p=81/160, the short-time cut probability is lambda^2 * 81*79/160^2 * t^2 + higher order. Complex unitary propagation at normalized H and lambda=0.05 agrees with this leading term for t=0.02, 0.04, 0.08 to within 0.03 percent. This requires further loss, control and fabrication modeling.

Relevant experiments: Rydberg interaction-driven caging https://www.nature.com/articles/s41567-024-02714-7 ; photonic Floquet-Lieb compact loops https://www.nature.com/articles/s42005-025-02138-6 ; programmable SU(2) optical synthetic fields https://pubmed.ncbi.nlm.nih.gov/39743600/ .

### Sixth, outside-the-box result: pi-flux sign frustration is unavoidable for this H

Let S_ij = sign(H_ij), S_ii=0. Exact integer trace counts give:
- Tr(|S|^3)/6 = **5250** graph triangles;
- Tr(S^3)/6 = **3690** signed sum;
- (5250-3690)/2 = **780 negative-product triangles**, 4470 positive-product triangles.

Explicit triangle flags (0,1,2) have couplings (-1,-2,-1), product -2. A closed-path product of hopping phases is gauge invariant under local onsite U(1) rephasings. Therefore **no onsite gauge can convert all 1883 signed hoppings to positive real amplitudes**. A faithful implementation requires programmable phase/sign resources (pi flux), not a network restricted to positive couplings.

This obstruction is a finite tight-binding gauge-phase statement, **not a measured electromagnetic field or emergent curvature**.

## Independent next routes

1. Derive compatible local refinement maps, a spectral-decimation recursion and a continuum with controlled dimension and propagation speed.
2. Search for an optimally congested apartment family respecting a proper subgroup and a principle selecting that subgroup.
3. Construct a derived discrete gravitational action and check the full phase-space-dependent hypersurface-deformation algebra, not Gauss alone.
4. Solve genuinely chiral E6 vacua, Yukawas and anomaly constraints against precision data without retrospectively fitting all parameters.
5. Compile the pi-flux triangle / eight-cycle gadget into physical photonic or superconducting gates and simulate loss, disorder, calibration and gate infidelity.


## 6. Spectral optimization within the *same* proven congestion optimum

A second producer, analysis/toe_20261103_spectral_conditioning_apartment_search.py, evaluates 33 reproducibly seeded greedy GF(2) cycle bases, each with 81 eight-edge apartments and maximum load five. All 33 satisfy exact integer rank/closure/load checks; the 81 nonzero Gram eigenvalues are numerically evaluated. The finite sample has **no global spectral optimum guarantee**.

| Metric | Seed 1 | Seed 12 | Seed 33 |
|---|---:|---:|---:|
| Max flag load | 5 | 5 | 5 |
| Smallest nonzero Gram eigenvalue | 0.0000677615 | 0.00950998 | 0.01818952 |
| Largest Gram eigenvalue | 23.296365 | 23.505841 | 23.142731 |
| Condition number | 343799.26 | 2471.70 | **1272.31** |
| Nonzero hopping pairs | 1883 | 1926 | **1896** |
| Negative signed triangles | 780 | 809 | **752** |

Thus seed 33 improves condition number by **270.216x** compared with the original basis while increasing the number of nonzero hoppings by only 13 (0.69%). It also decreases the number of pi-flux triangles by 28. This is a sampled Pareto improvement, not a claim that the absolute best set of 81 apartment cycles has been found.

Note the exact limitation: for a local defect lambda|e><e|, the leading leakage coefficient lambda^2 p(1-p) is a property of the fixed Hodge projector P and does **not** improve merely from changing the choice of basis B. Better intrinsic spectral condition does not itself imply fault-tolerant quantum memory. Further appropriate hardware metrics include signed-link calibration error, finite-time leakage, spectral control gap, input/output photon loss, and postselection costs.

**Scientific contribution of this round:** a reproducible, negative-result-first six-front test battery with an additional quantitative spectral-design candidate. The verified group, algebra, and anomaly identities are mathematical structure and control experiments; no experimentally verified TOE is being asserted.
