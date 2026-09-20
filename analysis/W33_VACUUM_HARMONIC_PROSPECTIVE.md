# Vacuum certificates, harmonic redundancy and a prospective surface test

September 20, 2026. Followthrough on five requested directions. Three mathematical/software directions have executable results; the measurement direction has an intake contract but no captured physical data, and the prospective direction has a frozen conditional prediction but no unseen observations. None establishes a completed theory of everything.

## 1. Alternative singlets and the actual FI ray

Holotrade's `analysis/flagship_full_cartan_fi_audit.py` reconstructs the anomalous generator directly from fresh orbifolder output. Its squared norm is 50/3 and the engine charge trace is 200. The latter is a dimensionless normalization quantity, not a measured dimensionful FI parameter. In moment-map coordinates we test `sum p_i |v_i|^2 + eta t_A = 0` for nonnegative eta.

Every one of the previous 14 projected rank-four positive circuits remains infeasible after replacing each canonical field by the union of **all** physical fields with the same projected charge. All component mixtures are allowed, a larger set than single representative choices. Fixed primitive type totals are retained. Exact Farkas witnesses rule out both zero FI and any nonnegative amount of the actual FI ray. Thus alternative representatives do not rescue these particular projected circuits.

The full set of 65 singlet fields, with 132 component weights, **does** admit exact Cartan solutions at zero FI and at positive FI. The positive-ray witness uses n_2, n_11, n_16, n_19 and n_20, with component-level rational squared VEVs archived in the certificate. These fields carry hidden nonabelian charges. A further exact check rejects this particular sparse candidate: the unbroken root (0,-1,0,1,0,0,0,0 | 0,0,0,0,0,0,0,0) has exactly one active transition, between n_2 components0 and1, so its off-diagonal D moment cannot vanish for any phases. The 34 one-component singlets alone also fail to cancel the positive FI ray, with a separate exact Farkas witness. Other configurations involving hidden charged fields and phase cancellations remain open; no F-flat vacuum or mass-matrix rank is established. The anomalous generator projects onto the four organizer roots as (-8/3,2/3,2,-11/3), explaining why the fixed zero-D circuit ratios cannot absorb a positive FI term. This broader support is distinct from the restricted mass-coupling support in parallel commit babfd48. The classical physical context is [Cleaver et al.](https://arxiv.org/abs/hep-th/9711178).

## 2. Explicit holonomy projectors, with prior ownership

Holotrade's prior joint-stabilizer census already owns the block pattern (3,2,1,1,1,1), and a6f1cae owns the missing-partner plane distinction. The new `flagship_joint_holonomy_tensors.py` constructs polynomial projectors in the actual ordered nine-weight basis. Remove a common projective phase from W3 and from 3V, calling the resulting commuting operators W and H. Then

`P0=(I+W+W^2)/3`, `P_triplet=P0(I+H)/2`, `P_doublet=P0(I-H)/2`.

Exact arithmetic modulo `z^2+z+1` verifies ranks three and two. W alone keeps the visible five together; the pair separates them. The associative centralizer is `M3 + M2 + C^4`, dimension17; its traceless Lie algebra has dimension16, matching the prior census. It is different from the older singlet spurion algebra `C I9 + M4`, despite the equal associative dimensions.

The endomorphism `m_T P_triplet + m_D P_doublet` is invariant under this joint centralizer and not under local A8. It names an explicit symmetry-permitted mass ansatz. It does **not** determine m_T,m_D, prove a world-sheet coupling is allowed, supply partner intertwiners, or calculate CFT amplitudes. [Orbifold selection rules](https://arxiv.org/abs/1107.2137) remain additional conditions.

## 3. Physical measurement: intake built, capture pending

`w33_prospective_surface_test.py` accepts a CSV with `time_s,gap_m,vertex_m`, a separate independent mass-in-kg or stiffness-in-N/m calibration record, and mode-fit estimates/covariance bound to the trace by SHA256. It checks units, timestamps, hashes, finite values, covariance positivity and recorded model assumptions. It rejects declared synthetic traces for prospective evaluation. Metadata and hashes do not authenticate a laboratory instrument; supplied fit results must still be independently reproduced. Tests deliberately fabricate temporary records to exercise software only.

No measured oscillator trace or independent calibration was supplied in this execution. The prior 801-point trace is synthetic. A request for accessible hardware/calibration remains pending. There is no claimed completed measurement.

## 4. Harmonic faults need redundancy outside the Hodge projector

`w33_harmonic_qutrit_redundancy.py` checks the existing 66-by-12 closed cycle matrix and its exact intersection form before assigning one abstract qutrit to each of six symplectic handle pairs. It then applies the **known** nine-qutrit Shor construction independently to the six handles, across nine carrier copies. This is a [[54,6,3]]_3 code with48 stabilizer generators. Prior ownership: BT300's Shor discussion and the [published nine-qutrit construction](https://arxiv.org/abs/1807.01863); the code itself is not new.

For one block the audit checks all73 identity/single-site Pauli errors, all5329 error pairs and all2304 weight-two Paulis. Equal syndromes leave only stabilizers; no weight-one or weight-two logical operator survives. A weight-three logical X supplies the explicit distance upper bound and failure control. Therefore an arbitrary error supported on the six handles of one carrier copy is correctable in the declared tensor-product encoding: its Pauli expansion has at most one site error in each block. Errors spanning several copies can be logical.

This is an entangled encoding isometry, not cloning a state. Surface homology alone does not physically quantize an oscillator into a qutrit. No hardware syndrome-extraction circuit, threshold or noise budget is established.

## 5. A frozen, scale-consistent conditional prediction

`w33_prospective_surface_test.json` freezes one ratio before future observations. For the declared engineered dynamics `M=mI`, `K=kL1`, where the prior Lutz surface has gap `2-sqrt(2)` and vertex eigenvalue12,

`omega_gap,natural^2 / omega_vertex,natural^2 = (2-sqrt(2))/12`.

Natural squared frequencies are recovered as damped squared frequency plus decay-rate squared. The full four-parameter covariance propagates into the ratio; the registered discrepancy rule is absolute standardized residual greater than3. One independent calibration fixes the remaining scale through `omega_vertex,natural^2=12 k/m`. Uniform masses/stiffnesses, mode identification and the damping model must be checked independently. The baseline is an unconstrained two-mode ratio; no Bayes factor is invented without a baseline distribution.

This tests a conditional substrate model, not a universal constant or the whole TOE. There is no new observed trace, no prospective test outcome and no credit for agreement with already-known data. The registry is created exclusively and cannot be silently overwritten by `--freeze`.

## Parallel intake and scope regressions

Reviewed incoming W33 history through6150ca9b6 and Holotrade history through7d9b467, including the changed paper rows and the restricted D/F and Gordan source/certificates. This was targeted semantic intake, not a complete rereading of every repository file or all three full papers. Incoming papers also retract the one-field-per-plane derivation of the cubic top; the coupling is reported as measured, not derived from that rule.

A separate `flatness_scope_counterexamples.py` in Holotrade supplies three exact toy examples: a D-flat support whose W is empty by an R selection rule; a nonempty W=(xy-1)^2 with a nonzero D/F-flat critical point; and W=z*x^2 whose restriction to z=0 vanishes while F_z does not. These do not refute the scanned charge data. They show why charge-cone existence, actual selection rules, termwise F-flatness and full derivative equations cannot be substituted for one another. Existing stronger parallel wording has been surfaced for the user's decision and is not overwritten here.

The retrospective formula audit was refreshed against the incoming replacement census:51323 exact and49901 structural families, universe SHA256396131cb74f2950a1292f13fac98df2dbe767c67e2730e596b177e1efa52e3d2. Its three adjusted sensitivity bounds remain1. This explicitly replaces the previous51294/49872 input version; it is not a prospective test.

## Reproduction

W33: run `python3 analysis/w33_harmonic_qutrit_redundancy.py` and the focused tests in `tests/test_harmonic_prospective_execution.py` plus `tests/test_surface_toe_followthroughs.py`. The prospective registry is already frozen; do not regenerate it to accommodate data. Real-record evaluation uses `--metadata`, `--trace`, and `--calibration`.

Holotrade: run `python3 analysis/flagship_full_cartan_fi_audit.py`, `python3 analysis/flagship_joint_holonomy_tensors.py`, and `python3 analysis/flatness_scope_counterexamples.py`; the focused suite independently reconstructs stored exact witnesses. See its `analysis/FLAGSHIP_FI_HOLONOMY.md` for engine provenance.
