# Causal order to local fermion operator: the first critical dependency closed in code

**2026-11-19. Scientific status:** constructed conditional finite mechanism; NOT a Theory of Everything, an intrinsic 3+1 Lorentzian Dirac operator, a physical spin selection, or a Standard Model prediction.

## Provenance and literature

The latest W33 master during this pass included commits b9e08278 (independent causal topology reconstruction), d93f49a1 (eight spin/gauge/fermion determinant gates) and 75389b70 (E8 anomaly shifts and physical dependency gates). We reviewed their changes. This present follow-up differs by **constructing the local 1D Wilson transport matrix from causal-incidence overlap, not from a manually supplied ring graph**, then checking exact determinants and the failure of oversmoothed topology.

External November 2026 preprint and original code: Tsilioukas, Topology change and the Gauss-Bonnet term in causal set theory, https://arxiv.org/abs/2611.06102 ; https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory . We pinned upstream commit 4de8bfb5ce307431e0cae81283219a1b8459fb39 in a separate Windows TEMP directory and independently executed the 2+1 and 3+1 selftests.

Additionally:
- The published 3+1 topology-change experiment at N=20,000, 250 landmarks, cap=14 was reproduced 3/3 seeds, with (b0,b1)=(1,0) before and (1,1) after.
- The larger N=200,000 3+1 experiment (150 landmarks, cap=12, lambda=0.80, neck=1.5, maxdim=2) completed successfully in 145.73 seconds: full (b0,b1,b2)=(1,0,0) before and (1,1,1) after. This is an independent reproduction of an existing external topological result, not independent validation of its speculative cosmological/axion interpretation.

Foundational sources: causal homology from thickened antichains https://arxiv.org/abs/gr-qc/0604124 ; Dowker theorem https://doi.org/10.1007/s41468-026-00239-x ; Wilson/Dirac lattice index https://doi.org/10.1007/s11005-026-02080-w ; 2026 causal fermion systems curved-spacetime continuum study https://doi.org/10.1007/s11005-026-02168-3 .

## I. A genuine small-scale construction without an inserted circle edge list

Begin with a synthetic 1+1 Lorentzian cylinder represented only by a selected antichain of n=12 spacelike events A and n=12 later witness events W, and a binary causal relation R(a,w). Numerical spatial coordinates are used once to generate the relation; all subsequent geometry recovery uses ONLY R and the known two-layer partition.

1. Compute the common-past overlap C_{w,w'} = sum_{a in A} R(a,w) R(a,w'), exactly a matrix product R_AW^T R_AW.
2. Independently reconstruct the Dowker nerve: witness subsets with a common causal-past antichain event form simplices. Compute its GF(2) H0,H1 by boundary matrices.
3. **Require connected H0=1 and H1=1** before accepting the circle hypothesis. A stable plateau occurs at shadow radii r=1 and r=2.
4. For a qualifying scale, keep exactly the pairs of future witnesses with maximal *positive off-diagonal* common-past overlap. At r=1, diagonal C=3; neighboring witnesses share 2 antichain events, next-nearest share 1 and distant ones share none.
5. Exactly n edges survive, with every witness vertex degree two and all witnesses connected: a combinatorial n-cycle. Extract its cyclic order without using physical coordinate positions.
6. **Only now** construct a prescribed 1D r=1 Wilson operator D=(1+m)I-T_theta on these inferred edges. The transport shift T is along the recovered cycle with a chosen boundary spin/gauge holonomy exp(-i theta).
7. Calculate det D directly on that cycle and verify the exact identity det D_n(m,theta)=(1+m)^n-exp(-i theta).

The new code tested n=12 at both stable radii and n=20 at r=1, with masses 0,0.01,0.1 and twists 0,pi. It recovers one periodic zero mode in the massless Wilson operator (not two naive doublers) and no antiperiodic zero mode. Independent random relabeling of BOTH antichain and witness events preserves the calculated topology and determinants. No spatial edge list was provided to the transport reconstruction.

## II. Deliberate counterexample: a graph can LOOK like a circle even when its topology is gone

For n=12, the full shadow-radius series has nerve H1:

| radius | H1 | physically accept circle transport? |
|---:|---:|---|
| 0 | 0, 12 connected components | no |
| 1 | 1 | yes |
| 2 | 1 | yes |
| 3 | 0 | no |
| 4 | 0 | no |
| 5 | 0 | no |

Without the homology filter, the maximal-overlap graph can STILL be an n-cycle at over-smoothed r=3 or beyond. Its 1-skeleton alone creates a false topological impression: triangles and higher faces have filled the hole in the full nerve. The implementation deliberately REJECTS these false positives.

This is an important TOE methodology result: matching a familiar graph or spectrum cannot establish physical topology. The same event data must survive multiple independent invariants, resolution choices, and relabelings.

## III. The conditional new connection to physical spin-sector weighting

The previously developed one-dimensional Wilson determinant spin/gauge toy was originally calculated on a supplied ring. Here its ring adjacency is derived from causal-incidence overlap. The remaining choices are explicit: Wilson kinetic rule, Euclidean dimension, site spacing, selected antichain/scale, spin lift, gauge representation/connection, fermion masses and the physical measure.

For flat central SU2 gauge winding z and spin winding s, a fundamental fermion sees s+z (mod2), while a gauge singlet sees s. Given an assumed massless doublet+singlet, zero-source determinants conditionally select one of four spin-center sectors. For a continuum mass-times-circle-length mu, det_P/det_AP approaches tanh(mu/2), so the sector weighting is strongly sensitive to matter masses and compactification length.

**This does NOT establish actual physical spin selection.** A massless zero determinant only suppresses an unsaturated *zero-source* Grassmann vacuum contribution; charged insertions can saturate zero modes. Integrating over continuous SU2 holonomies, determining which spin structure extends over the actual cobordism, and imposing full 3+1 anomaly-free chiral matter could change the result completely.

The first missing element is an intrinsic Lorentzian causal Dirac operator on an order-recovered *3+1* spacetime. Only after that has passed index/causality/locality tests can a real fermionic path integral weight global bundles and a physical quantum state.

## III-b. Extra independent gate: causal topology does not determine handedness

An additional exact group-action check finds a *different* missing premise: even a correctly reconstructed circle and its mod-2 spin sectors do not determine an oriented integer first-homology generator.

On the synthetic causal cylinder, the spatial reflection sigma:j->-j (mod n), applied consistently to both antichain and witness event labels, preserves **every causal relation** R. However, this same automorphism acts on H1(S1;Z) by multiplication by -1, reversing every directed generator of the reconstructed cycle. We verified this for n=12 at both stable radii and n=20.

Suppose a deterministic procedure assigns a nonzero preferred integer cycle orientation c from R and is equivariant under every automorphism of R. Reflection would require c=-c, implying c=0 because H1(S1;Z) has no 2-torsion. **Contradiction.** Thus the *unoriented reflection-symmetric causal relation itself* does not select a nonzero handedness. This is a standard and elementary automorphism argument; we make it executable on the same nerve and transport construction.

Crucially, modulo 2 the orientation sign disappears: -1=+1 mod2. Both Z2 spin twist classes still exist and are unchanged by reflection. In the Wilson determinant with generic twist theta=.71, orientation reversal conjugates det D(theta) and det D(-theta), while the absolute value agrees. So even the parity-even spin-resolved determinant need not select a chirality sign.

**Scope restriction:** This is a no-go only for deterministic, automorphism-equivariant *orientation selection on reflection-symmetric finite orders*. It is NOT a no-go for genuinely asymmetric causal histories, oriented/complex microscopic data, boundary conditions, chiral matter representations or spontaneous parity breaking. But it sharpens the dependency map: before claiming weak chiral physics, the TOE needs a physical source of oriented spin/chiral structure, not merely recoverable H1(Z2).

Reproduce:

    python analysis/toe_20261119_causal_parity_orientation_obstruction_v8.py
    python -m pytest -q tests/test_toe_20261119_causal_parity_orientation_obstruction_v8.py

New artifacts: analysis/toe_20261119_causal_parity_orientation_obstruction_v8.py ; tests/test_toe_20261119_causal_parity_orientation_obstruction_v8.py ; data/toe_20261119_causal_parity_orientation_obstruction_v8.json. All 10 new tests passed in the focused three-suite regression (87 passed total). This is an independent extension, not proof of observed electroweak chirality.

## IV. The dependency DAG: derive first the thing that makes other unknowns calculable

Our executable dependency DAG ranks:

| Stage | Current status | What it unlocks |
|---|---|---|
| A: causal partial order + selected antichain | input/synthetic | order-based topology |
| B: persistent spatial Dowker nerve | reconstructed, independently externally benchmarked | candidate spin structures |
| C: maximal-shadow-overlap 1D cycle | constructed, label invariant | local adjacency without a coordinate graph |
| D: 1D Wilson matrix on inferred cycle | constructed conditional on Wilson rule | exact kinetic determinant |
| E: conditional spin/center sector weights | toy mechanism constructed | sensitivity to matter masses |
| F: intrinsic 3+1 Lorentzian causal Clifford/Dirac operator | **MISSING KEYSTONE** | real local chirality, index, anomalies and physical propagators |
| G: physically derived matter/flavor and mass mechanism | MISSING | true fermion determinants, couplings and hypercharge selection |
| H: real 3+1 fermion path-integral spin selection | MISSING | physical bundle-sector weighting |
| I: unique microscopic gauge/gravity action | MISSING | normalized quantum history amplitudes |
| J: positive normalized decoherence functional on unlabeled histories | MISSING | relative nonmanifold vs manifoldlike phase probability |
| K: Lorentzian Einstein/graviton continuum + observations | MISSING | testable unification |

The program checks acyclicity and topologically sorts this partial dependency order. The first **fundamental** unknown after the demonstrated finite bridge is F. This does NOT prove that F alone would derive the others; it identifies where solving one missing piece would immediately make several other tests physically meaningful.

## V. Which connections are useful, and what they do NOT mean

- **Topology -> fermion:** an order-derived ring plus supplied Wilson law reproduces twisted kinetic determinants, a constructive arrow beyond graph numerology.
- **Matter -> topology selection:** the determinant uses physical representations and mass-length scale, so the latter cannot be left arbitrary; a novel prediction would require deriving those inputs.
- **Gauge center -> matter:** a positive-transfer SU2 family has identical quadratic curvature but different line-operator sectors; a true global SM quotient and chiral representation would constrain physically meaningful choices.
- **Action -> gravity:** destructive interference of bad causal histories does NOT mean 4D gravity emerged; a positive normalized decoherence functional comparing against manifoldlike histories is needed. Existing toy coherence leakage yields an exponentially severe threshold.
- **Flavor -> charge:** generation-dependent anomaly-free L_mu-L_tau deformation shows anomalies do not select observed charges absent neutrino neutrality/flavor data.

**No 3+1 spin physics, gravity action, Born rule, Standard Model generation count, mass or measured coupling has been derived.** All five ultimate theoretical goals remain open.

## Reproducibility

    python analysis/toe_20261119_order_to_wilson_dirac_critical_path_v7.py
    python -m pytest -q tests/test_toe_20261119_order_to_wilson_dirac_critical_path_v7.py

Program: analysis/toe_20261119_order_to_wilson_dirac_critical_path_v7.py
Tests: tests/test_toe_20261119_order_to_wilson_dirac_critical_path_v7.py
Data: data/toe_20261119_causal_order_wilson_dirac_dependency_v7.json
Report: analysis/2026-11-19_TOE_order_to_Dirac_critical_path.md

**19 new V7 and 10 new V8 focused tests, all passing.** Their three-suite run with prior V6 had **87 passing tests**; the broader 529-test physics regression is verified below.

## Final broad regression (including all concurrent November 19 physics suites)

The complete current suite of **37** test modules matching tests/test_toe_20261119*.py passed **529 tests in 101.77 seconds** on the connected Windows PC. Both independent new executables were rerun after that suite and emitted PASS certificates. The separately executed focused three-suite run (V6, V7, V8) passed **87 tests**. The original published external causet topology code also passed 2+1 and 3+1 selftests and independent topology-change cases, including the N=200000 full b2 demonstration. No 3+1 Dirac, observed chirality or completed TOE follows from these regression successes.

## Top five independent high-upside next experiments

1. **Intrinsic 3+1 chiral causal Dirac:** build spin lifts and transport on the external 3+1 antichain nerves, demand correct four-dimensional overlap index, Lorentzian causality, locality and no doublers *without* supplying a smooth metric.
2. **Select action via matter global structure:** couple the recovered causal fermions to the SU2 fundamental/adjoint transfer family and a global SM quotient; test center line operators and RG scaling and reject models needing arbitrary action coefficients.
3. **Calculate physically normalized state/fermion weights:** integrate true chiral Grassmann fields, including zero-mode-saturating observables, over the possible spin and center bundles; derive a positive quantum state rather than assign equal priors.
4. **Show a genuine 3+1 gravitational phase:** introduce a fully specified oscillatory unlabeled causal action and decoherence measure, compare nonmanifoldlike versus manifoldlike **relative** weights, recover Einstein constraints and physical spin-two propagation.
5. **Derive observed flavor from topology:** demand three anomaly-free chiral families, neutral neutrinos, physical Yukawa overlap integrals and masses from the same microscopic geometry, not from adjustable source charges.

**Result:** a previously imposed spatial edge list has been removed in one controlled 1D benchmark. This identifies the 3+1 Lorentzian causal Dirac construction as the first high-leverage physics gap, not a finished TOE.
