# 2026-11-22 — Exact one-phase Witting/Hessian/Heisenberg controllability

**Status:** exact, reproducible finite-dimensional theorem. **Not** a claimed universal multi-photon processor, empirical quantum-switch demonstration, derivation of the Standard Model, or Theory of Everything.

## Repo review and novelty boundary

The repository's seven-day reconciliation (`analysis/2026-11-22_weekly_TOE_reconciliation_and_independent_gate_frontier.md`) pins 307 earlier weekly commits; the predecessor full-patch audit processed 260, and 47 later diffs were directly reviewed. An additional 25 November 22 commits following that historical reference were individually fetched and their patches examined before this release. The direct new work concerns **continuous-control Lie closure**; previous November 22 work compiled individual fixed Witting reflections and found operator-Schmidt resource bounds.

Importantly, the *Hessian group and abstract Heisenberg H27 are not new discoveries*. `analysis/w33_20261011_witting_displacement_firewall.py` already realizes order-648 G25 inside G32 and a transverse H27 triplet; `analysis/2026-10-15_toe92_witting_five.md` already uses regular H27 addresses on 27 cubic-surface objects. The new object here is the **specific three-mirror action on the canonical forty Witting ququart rays**, its explicit regular 27-ray orbit and a minimal controllability scheme using one continuously adjustable phase.

## Exact source definitions

Let `omega^2+omega+1=0` and use the canonical Witting ray ordering from `analysis/toe_20261121_hermitian45_pauli_sic_bridge.py`, with zero-based indices.

- `v5=(1,0,-1,-1)`
- `v26=(1,-omega,0,omega^2)`
- `v33=(1,0,-omega^2,-omega)`
- `v36=(0,1,-omega^2,omega^2)`

All have norm squared three; put `P_j=v_j v_j^dagger/3`. Their adjustable phase operations are `R_j(theta)=I+(exp(i theta)-1)P_j`.

## Theorem A: four rank-one controls are minimal for full U(4)

`Lie_R(iP5,iP26,iP33,iP36)=u(4)`.

The exact modular Lie-word certificate produces successive spans of dimensions `4,8,14,16`. The same 16 words have rank sixteen modulo six primes `7,13,19,31,37,43`. Nonzero determinant in any of these fields implies linear independence over the characteristic-zero field `Q(omega)`; the real Lie algebra of skew-Hermitian generators has the full possible dimension 16. Three rank-one controls or fewer leave a common nonzero orthogonal complement fixed, so cannot equal U(4). This is minimal **under the independently addressable rank-one projector control model**.

## Theorem B: one tunable phase plus three fixed order-three mirrors

Freeze `R5(2pi/3)`, `R26(2pi/3)`, `R33(2pi/3)` and allow `R36(theta)` to vary continuously. The fixed operations, exactly computed over `Q(omega)`, permute all 40 projective Witting rays. Their permutation group has order **648** with orbits **27+12+1**. The orbit of ray 36 contains rays **0,2,7,20**. Their four rank-one projectors pass the same rank-sixteen Lie witness over all six primes. Conjugation of `P36` by fixed-group elements therefore supplies full `u(4)`, and the mixed discrete/continuous group is dense in U(4). This proves one continuously adjustable optical phase is sufficient *given these three exact finite mirrors*. Two or fewer fixed rank-one mirrors plus one tunable rank-one projector leave a nonzero common fixed subspace, establishing minimality in this restricted scheme.

The theorem is about reachable **four-mode unitary operators**, not a particular routing graph, finite optical circuit depth, loss-tolerant calibration, or coherent quantum switch.

## Theorem C: a genuine normal Heisenberg H27 acts as a 27-address torsor

Within the above order-648 fixed-mirror group, take the normal closure of `R5 R33^-1`. Exact permutation-group arithmetic gives order `27`, center order `3`, commutator subgroup order `3`, and element order census `1^1 3^26`. This identifies the exponent-three extraspecial group `3_+^(1+2)`, the finite Heisenberg group `H27`. It acts freely/transitively on the 27-element orbit of the tunable ray: the point stabilizer is trivial. The quotient of the 648-group by this subgroup has order 24.

**Crucial distinction:** this proves a canonical *computational orbit* for the chosen generator set; it does not establish an `E6` matter field, identify a physical Higgs triplet, or derive a spacetime causal structure from the 27 addresses. The Hessian group itself and an abstract H27 bridge are prior art within the repo; their explicit orbital control role here is the advance.

## Reproduction and evidence levels

Scripts: `analysis/toe_20261122_witting_minimal_lie_control.py`, `analysis/toe_20261122_witting_one_phase_three_fixed.py`, `analysis/toe_20261122_witting_h27_phase_control.py`.

Frozen results: `data/toe_20261122_witting_four_ray_lie_controllability.json`, `data/toe_20261122_witting_one_phase_three_fixed.json`, `data/toe_20261122_witting_h27_phase_control.json`.

Regression tests: three corresponding `tests/test_toe_20261122_witting_*.py` files. Server-side independent execution: **8 focused tests passed**. The isolated GitHub Actions workflow `witting-h27-controllability.yml` also runs these scripts and compares certificates against the committed frozen output.

**Local-machine limitation:** Desktop Commander reports monthly usage exhausted, so the Windows checkout `C:\Repos\Theory of Everything` was neither inspected nor pulled. GitHub `master` is updated; do **not** claim Windows synchronization.

## Physics and open boundaries

The Lie-rank condition assumes arbitrary coherent repetition and a continuously variable phase, not a finite exact compiler or bounded optical depth. A single-photon ququart can be controlled universally as a four-mode **single-system** operation; this does not supply deterministic nonlocal gates on multiple ququarts. The 27-ray Heisenberg addresses are a legitimate finite geometry but no UV completion, gauge dynamics, relativistic propagation, observed chiral matter or gravity equations follow from them.

References: control Lie algebra rank condition [EPJ Quantum Technology](https://link.springer.com/article/10.1140/epjqt/s40507-022-00138-x), programmable optical interferometers [Clements et al.](https://ora.ox.ac.uk/objects/uuid:12001441-51c7-4bb7-913c-18a1c208ed2e), complex reflection group tables [Magma](https://docs.magma-maths.org/LieTheory/ReflectionGroups/create-group-refl-complex.html).

## Independent next fronts

1. Test whether a finite physically calibrated phase alphabet on the single tunable control is dense, finite, or confined, with an algebraic density certificate and noise robustness.
2. Construct a genuinely composable quantum-process tensor and a causal-order inequality; reject identification of ordinary static Witting overlap interference with indefinite causal order.
3. Determine whether the normal H27 action on the 27 Witting rays intertwines *equivariantly and with matching central cocycle* with the repo's separate E6/trinification H27 operator algebra.
4. Derive anomaly-free chiral matter and a local Lorentzian continuum gravitation limit from a specified action, with explicit no-go negative controls.
5. Model full photonic cost: port connectivity, splitter phases, tunable-element count, insertion loss, calibration Fisher information and resource-accounted nonlocal gates.
