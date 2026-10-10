# TOE Round 32 — temporal qutrit decoder, compact W33-cover search, E8 hypercharge obstruction, dynamical locality, and C8 hardware-platform screening

**Date:** 10 October 2026
**Repository:** wilcompute/W33-Theory
**Boundary:** Five independent directions requested after Round31. Separate proved mathematics, numerical sampling, and conditional physics. No measured quantum device, noise threshold, Standard Model theory, Lorentzian gravitational continuum, or physical gauge vacuum is claimed.

## Prior art reviewed

Round26 and Round30 already produced the native [[160,1,8]]_3 checks and a verified GHZ/CZ single-fault circuit under ideal verifier/readout; Round31 gave the classical verifier budget, an explicit connected 17-fold girth10 Levi graph cover, conditional Spin16 obstructions, observer-imposed Z3 spatial unwrapping, and a two-photon lifetime estimate. New parallel Passes11839–11843, *already on master*, explicitly construct the Rac/Di crosscap map, finite Poincare shell propagators, cubic couplings, and a Tits-embedded E8 commutant su(3) + su(2) (dimension11, centre0), contrasted with a one-dimensional u(1) commutant of the separate Weil embedding. The new parallel work remains finite kinematic mathematics, not gravity or an experimental gauge theory. This pass does not rebrand those results as original.

## I. Synthetic five-round ternary syndrome filtering vs final-round decoding

Use the actual W33 `[[160,1,8]]_3` code: 80 Wilson-Z and 79 Gauss-X checks. On 160 data links, simulate independent per-channel X/Z errors with probability pd=.0005 per link per round, each a random nonzero F3 Pauli, over **five rounds**. Each stabilizer report independently flips to one of two wrong qutrit outcomes with probability pm=.01,.02,.04. Use 180 frozen-seed trials per pm.

**New model:** a separate three-state Bayesian temporal filter for each check, starting from initial all-zero syndrome. Prediction at each step uses approximate change rate rho=check_weight×pd; measurement likelihood 1-pm for the observed value and pm/2 for each alternative. Run the old EXACT data-only radius-three decoder on (i) the raw final check reports, (ii) the temporally filtered final reports, and (iii) the uncorrupted true final reports. Check full stabilizer-equivalent logical correction, not only equality of decoded physical Pauli frames.

| pm | logical failures raw /180 | temporal /180 | perfect measurement /180 | wrong syndrome values raw→temporal total |
|----|----:|----:|----:|---|
|1%|144|40|1|279→80|
|2%|171|35|0|572→127|
|4%|180|53|1|1186→147|

This gives a substantive **phenomenological** improvement without assuming measurement reports never change. However, filtering check histories independently ignores the exact joint code constraints, and a decoded set of check values can be inconsistent with any physical F3 Pauli error. It is NOT a joint space-time maximum-likelihood decoder, cat-gate noise simulator, verified-GHZ circuit acceptance model, or rigorous threshold estimate. The ideal-syndrome baseline shows the remaining gap.

Reproducer: `analysis/w33_20261010_toe32_phenom_temporal_decoder.py`; certificate: `data/w33_20261010_toe32_phenom_temporal_decoder.json`.

## II. Attack cover degrees smaller than17 honestly; 17 remains best verified

Prior Round31 certificate: cyclic degree17 cover has 1,360 base-incidence vertices, 2,720 edges, girth10, and ternary HGP [[9245281,1852321,10]]_3 (distance10, rate20.035%). Rank GF2 contradiction excludes **cyclic degree2**, but says nothing about 4-fold or 8-fold covers.

Perform a new longer seeded local-voltage optimizer for groups Z/4, Z/5, Z/7, Z/8, Z/11, Z/13, maintaining all 1,620 oriented native eight-cycle holonomies and reducing those equal to zero. Total budget **141,000 attempted local updates** across 18 restarts (exact summed budget: 15,000+15,000+18,000+15,000+30,000+48,000=141,000). Best remaining forbidden eight cycles:

| cyclic degree | best zero-holonomy eight-cycles | exact no-go? |
|---:|---:|---|
|4|255|no|
|5|178|no|
|7|88|no|
|8|65|no|
|11|23|no|
|13|8|no|

**No new smaller cover was found.** These failures are **not** mathematical nonexistence claims. In particular the p=13 candidate is near feasible but still FAILS to eliminate eight-cycles, so DO NOT publish distance10 for p13. Only prior degree17 remains a certified exact girth10 cover. No girth12 cover produced either.

Reproducer: `analysis/w33_20261010_toe32_voltage_opt_search.py`. Frozen search ledger `data/w33_20261010_toe32_voltage_opt_search.json`. The search reruns separately (~80 seconds) rather than during fast regression.

## III. A rigorous hypercharge obstruction for the *fixed* Tits E8 Lorentz embedding

Pass11843 already computed, using actual Chevalley E8 Tits automorphisms and numerical closure checks, the centralizer of the finite Lorentz group L within e8:

`c_e8(L) = su(3) ⊕ su(2)`, dimension11, semisimple and centre0.

Pass11837 separately computed an unrelated Weil E8 embedding with centralizer u1. They are **different** representations of the finite Lorentz action; their centralizers cannot simply be added. Our script reads and asserts the independent Pass11843 machine certificate (e8 dimension248, Jacobi tolerance, centralizer dimension11, derived dimension11, centre0 and both su3, su2 constituents).

**New extension no-go:** For ANY overgroup H containing the **same embedded finite Lorentz L** (for example a proposed finite Poincare group L with added translations), `c_e8(H) ⊂ c_e8(L)`. Therefore its commuting internal algebra has dimension at most11. If the entire su3+su2 is to survive, no independent commuting hypercharge u1 can be added inside the same fixed E8 embedding: its centralizer has zero centre. A proposed SM commuting algebra su3+su2+u1 would require dimension12, which is impossible under that containment.

The overgroup may instead shrink the commutant. A smaller commutant can have a nonzero centre, but cannot simultaneously preserve the full su3 and su2. The theorem is **conditional on identifying the internal gauge algebra with the E8 commutant of this fixed Lorentz embedding**. Different E8 actions, gauge/Higgs symmetry breaking, bundles and dynamical models are not excluded. No actual finite-translation E8 generators were constructed. An E8 commutant, even if exact, does not establish observed Standard Model gauge bosons.

Reproducer: `analysis/w33_20261010_toe32_e8_extension_monotonicity.py`; input: `data/w33_pass11843_e8_tits_lorentz_commutant.json`; output certificate `data/w33_20261010_toe32_e8_extension_monotonicity.json`.

## IV. Internal finite graph dynamics: different growth and no STRICT continuous-time null cone

Use the explicit Round31 degree17 Levi cover (N=1,360 vertices; 4-regular; girth10) as an honest W33-derived spatial carrier. Independently reconstruct all edges from its 160 mod17 voltage values. Run exact BFS at 13 selected roots (including all vertex class representatives and distant sites), verify the same first five graph shells `1,4,12,36,108`. By girth10 these are the exact 4-regular tree shells through radius4. Spatial graph balls are `1,5,17,53,161`, whereas the **externally imposed** Z³ cubic balls are `1,7,25,63,129`. At one tested root the lift ball sizes are `1,5,17,53,161,432,894,1262,1359`, then saturate the finite 1,360 positions.

Thus our *native* cover initially expands exponentially `∼3^r` as a tree, not `∼r³` as cubic 3D space. This excludes claiming that this specific cover automatically provides local 3D continuum geometry.

For physical-style continuous-time hopping `U(t)=exp(-itA)`, the first nonzero Taylor coefficient of the amplitude between vertices u,v at graph distance d is `(-i)^d(A^d)_{uv}/d!`, where (A^d)uv is a positive number of shortest walks. Therefore exact amplitude cannot vanish **identically as a function of time** outside any finite-radius cone. Accidental zeros at discrete times are possible. A rigorous upper bound on the small tails at distance d is `sum_{n=d}^∞(4|t|)^n/n!`. Approximate Lieb–Robinson locality may still hold. Do not conflate this with the discrete leapfrog strict finite-step cone of Round28.

No physical speed c, spacetime dimension4, Einstein dynamics or Lorentz invariance is derived.

Reproducer: `analysis/w33_20261010_toe32_cover_causal_growth.py`; machine certificate `data/w33_20261010_toe32_cover_causal_growth.json`.

## V. Compare ACTUAL published experimental platforms against an assumed C8 doublon design

2026 literature screened for concrete relevant experiments:

| Published result | Source-grounded capability | Does it meet our required C8 pair experiment? |
|---|---|---|
| 21-site superconducting Bose-Hubbard simulator (2026) | Multimode driven-dissipative phases, spectroscopy, time-domain measurements | **Unknown:** no demonstrated exact 8-site ring, 160MHz attractive Kerr and 60us coherent two-boson pair survival in abstract |
| 5-site coupled superconducting artificial atoms (2021) | Bose-Hubbard photon transport, transmission and cross-Kerr band visualization | **Unknown:** only 5-site driven-dissipative chain described |
| 4×4 superconducting HARD-CORE Bose-Hubbard (2024) | 16-site hard-core particles, entanglement measurements | **NO in hard-core encoding**: each site has n∈{0,1}, so (a†)²=0 and |2_i> doublon is absent |
| Integrated silicon photon source/detection platform (2025) | On-chip photon-pair generation, manipulation, detection | **Unknown:** pair *generation* does not establish strong attractive on-site Kerr interaction or long two-particle coherent storage |

Sources:
- https://doi.org/10.1103/rvhv-ms4t (PRX Quantum 2026, 21 sites)
- https://doi.org/10.1103/PhysRevLett.126.180503 (PRL 2021, 5 artificial atoms)
- https://doi.org/10.1038/s41586-024-07325-z (Nature 2024, hard-core 16 sites)
- https://doi.org/10.1038/s41586-025-08820-7 (Nature 2025, silicon photonics)

The algebraic NO-GO for the published HARD-CORE model is exact: local Hilbert space {|0>,|1>} cannot support our assumed on-site two-boson attractive bound state or `−U n_i(n_i−1)/2` energy. It could be redesigned using higher transmon levels, which is a DIFFERENT Hamiltonian.

Model target remains eight sites, eight links, `U/t=32`, `t/h=5MHz`, `U/h=160MHz`, band gap ≈0.18175MHz. Under an *assumed*, not measured, independent Markovian loss model `P(pair alive,t)=exp(-2t/T1)`, the ≥50% pair survival requirement is `T1≥57.7μs` at t=20μs for a direct experiment, or `T1≥173.1μs` at t=60μs Ramsey. Neither bound is experimentally certified for the cited devices; the actual pair-selective contrast, Kerr sign, circuit detuning and coherence data must be measured.

Reproducer: `analysis/w33_20261010_toe32_C8_platform_gap_screen.py`; machine certificate `data/w33_20261010_toe32_C8_platform_gap_screen.json`.

## Executive result

One substantive numerical improvement: the approximate temporal decoder reduces observed noisy readout recovery failures dramatically, though still far from ideal. One honest negative search: no cyclic cover smaller than degree17 certified (p13 misses eight constraints). One exact new TOE-relevant theorem: simply adjoining translations to the SAME Tits E8 finite Lorentz action cannot generate a commuting SU3×SU2×U1 gauge algebra if its original SU3×SU2 remains. One geometry no-go: native degree17 cover looks like a 4-regular tree at small radii, not 3D cubic locality; continuous-time hopping yields tails. One experimental discriminator: hard-core BH platforms cannot directly realize the attractive doublon Hamiltonian.

**No new physical theory-of-everything derivation, actual E8 hypercharge, experimental universal photonic computer, physical four-dimensional spacetime, circuit-level noise threshold or genuine deployed C8 machine is claimed.**
