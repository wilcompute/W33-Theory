# TOE88 — Five research tracks: cyclic Tate polarization, parity membranes, ancilla hooks, adversarial MUB controls, and the 26D Albert comparison

**15 October 2026.** Based on W33-Theory `master` at `8ce0c9a4f3bc613e1ef1ab173d6e3a55eb545771`. Only the clean TOE88 worktree was modified; other agents' dirty root checkout was left untouched.

## Executive distinction

This pass contains exact finite-field algebra, integer incidence calculations, and entirely synthetic quantum-channel/circuit models. It **does not** prove a theory of everything, spacetime emergence, physical time ordering, an F4 embedding, or a fault-tolerant photon computer.

### Track 1 — Explain the ternary directional polarization using cyclic Tate/Jordan invariants

For every one of the 13 orbit-pair normalizer classes of TOE87 (representing all 468 admissible pairs), reconstruct `H1(F3)` and `H2(F3)` as genuine representations of H27. For each of the four representative noncentral order-three Pauli directions (and the center), calculate `J=g-I`, `rank(J)`, `rank(J²)`, and exact counts of Jordan blocks of sizes 1, 2 and 3:

```
b3 = rank(J²)
b2 = rank(J) - 2 rank(J²)
b1 = dimension - 2 rank(J) + rank(J²)
```

Since `N=1+g+g²=(g-I)²=J²` over F3, the cyclic Tate groups for C3 have equal dimensions

```
dim Hhat^0(C3,V) = dim Hhat^(-1)(C3,V)
                 = dim ker(g-I) - rank(N) = b1 + b2.
```

The rank-minimizing direction is exactly the **unique Tate-dimension-maximizing direction**, simultaneously for H1 and H2, for all 13 two-orbit classes; the 468-pair extension is by exact equivariance. This gives an explicit **cohomological characterization** of the observed selection rule, not yet a structural theorem explaining why its maxima must agree beyond the exhaustively classified families.

For the selected torsion-free pair (0,10), generic-direction Jordan block counts (sizes 1/2/3) and the unique selected-direction counts are:

| Module | Generic | Selected | Generic Tate dim | Selected Tate dim |
|---|---|---|---:|---:|
| H1(F3), dimension 26 | [0,1,8] | [1,2,7] | 1 | 3 |
| H2(F3), dimension 16 | [1,0,5] | [3,2,3] | 1 | 5 |

For the 432 torsion cases, H1 generic [0,1,4] vs selected [1,2,3]; H2 generic [1,0,1] vs selected [2,1,0]. In both H1 and H2, the special direction has a higher Tate dimension. The center is separately computed. These results must be read together with TOE87's three-orbit **failure** of a uniquely shared minimizer.

### Track 2 — Explicit geometric mod-2 torsion detector

Start with the oriented integer 135-by-99 boundary `d2` of a two-square-orbit code. Let `x` be any mod-2 closed 2-face chain. Lifting its 0/1 coefficients to integers yields an *even* exact boundary `d2(x_lift)=2 y`; the class `[y mod2]` modulo face boundaries is the Bockstein image in H1(F2). Nonzero image detects integral 2-primary torsion and does **not** require an integer Smith-normal-form computation.

For explicit representatives:

| square orbit pair | prior integral torsion | mod-2 Bockstein rank | sparse witness counts |
|---|---|---:|---|
| (0,10) | none | 0 | none |
| (1,2) | (Z/3)^2 | 0 | none |
| (1,31) | (Z/6)^2 | 2 | two 24-face membranes |
| (1,36) | (Z/6)^2 | 2 | two 24-face membranes |

The script freezes every chosen 24-face support, its face triangle/square support decomposition, and the edge support of its nonzero Bockstein image, with exact divisibility and independent quotient-class tests. The two torsion-positive codes and negative controls demonstrate a **constructive parity-incidence detector** rather than a numerological match. Extension to a closed local geometric invariant that predicts the class without calculating the face boundary remains open.

### Track 3 — Repeated 99-ancilla qutrit syndrome extraction with quantified hook errors

The selected CSS geometry has 135 physical edge qutrits and 99 oriented face Z checks. Compile a bipartite-conflict-free sequence of **351** weighted qutrit SUM gates per extraction round, packed into **6 parallel two-qudit gate layers** with no gate sharing an ancilla or data qutrit within a layer. Repeat extraction in three rounds. Model exact Pauli-frame conjugation for `SUM^w` with control=data and target=ancilla:

```
(x_d,z_d; x_a,z_a) -> (x_d, z_d - w z_a; x_a + w x_d, z_a) mod 3.
```

One controlled ancilla `Z` fault after an earlier interaction causes a **hook `Z` fault** on data through a later interaction in that check; this fault is not observed by these same Z-type checks. Freeze an explicit witness pair of SUM gates and exact propagated Pauli exponent. Thus the one-check-family extraction schedule is **NOT fault-tolerant**.

The 320-shot per-condition seeded circuit model uses three repeated rounds, specified per-gate X-data, ancilla X/Z, conditional correlated data-X given ancilla Z, and readout wrong-digit probabilities. The direct hook-positive and hook-disabled scenarios quantify the difference: the hook-positive scenario produces a nonzero data-Z incidence, the control none. Majority voting on the three measured syndromes reduces the *observed mismatch* under this specific model; it is not a valid spacetime decoder when data errors evolve between rounds, and does not correct the invisible Z hooks.

The complete model, rates and frozen measured statistics are in `data/w33_20261015_toe88_ancilla_syndrome.json`. It is not an end-to-end CSS extraction protocol, optical hardware calibration or a circuit-level logical threshold. The next physical step must add complementary X checks, ancilla verification, and hook-aware decoding.

### Track 4 — SPAM-robust four-MUB test versus adaptive entanglement-breaking adversaries and basis leakage

TOE87's four-MUB input ensemble is a full qutrit 2-design, giving universal mean state survival `<= 1/2` for any entanglement-breaking (EB) qutrit channel with trusted state-matched measurements, secret independent setting selection and fair sampling. This remains an **adaptive** null bound for sequential EB strategies if the *conditional* next-trial success probability remains <= the calibrated p0: fresh iid uniforms couple its success count to Binomial(n,p0). Temporal correlations alone do not evade that bound under the conditional assumption.

Add per-setting preparation trace-distance calibration `eps_state<=0.01` and measurement-effect expectation error `eta<=0.01`, conservatively relaxing the ideal EB survival to `<=0.52`. Include known symmetric wrong-class readout at 2% and uniform leakage replacement at 3%; the calibrated measured EB threshold is `p0=0.508968`. For coherent visibility 0.25, conservative true survival `>=0.605`, then the same readout model gives a higher alternative mean.

An independently randomized **1,200 accepted-shot** protocol rejects at **665** or more successful state-matched returns; its exact iid-binomial null bound is <=0.001 and the model-specific idealized alternative power is **0.9932423412730284**. Using the conditional-probability bound makes the stated false-positive upper bound also valid against past-adaptive EB processes; the quoted *power* additionally assumes stable channel statistics.

Important adversarial **loophole**: if a device leaks the secret basis and can accept its basis-matching inputs with probability 1 while accepting other bases with probability 0.1, a measure-and-reprepare (EB) apparatus can arrange **84.6% accepted-shot fidelity** even though only **32.5%** of trials are accepted. Thus state-dependent postselection/basis side-channels invalidate a naïve fair-sampling EB witness. Control strategies and their acceptance imbalance are frozen as a stress test. This result is synthetic and does not establish an optical detector calibration.

### Track 5 — The E6 27 / F4 26 dimension bridge: explicit binary isomorphism, ternary obstruction

The W33 native regular `H27` permutation action on 27 cubic-surface addresses contains the 26-dimensional *augmentation* module `ker(sum: F_p[H27] -> F_p)`. Construct its exact induced action on the canonical basis `delta_g-delta_identity`, independent of any assertion about an Albert product.

Over **F2**, the selected 26-dimensional `H1(F2)` has the same simple multiplicities, and an explicit deterministic cyclic-vector map with 26 linearly independent orbit images is constructed and checked for full **H27 equivariance**. This proves an exact **H27-module isomorphism** between the binary code H1 and the regular 27-point augmentation module.

Over **F3** the same tempting 26D equivalence is **mathematically false**. The central element `z=(0,0,1)` has Jordan block-size counts [0,1,8] on the 26D augmentation module (rank(z-I)=17), but [1,2,7] on the selected ternary H1 (rank=16). Therefore the central actions are not conjugate; there is no equivariant isomorphism for these specified H27 actions in characteristic 3.

In standard characteristic-zero Lie theory the exceptional Jordan/Albert algebra J27 has a traceless F4-minimal 26D component and an E6 27D module. But **an H27-equivariant augmentation isomorphism does not prove an F4 subgroup embedding or an Albert-product intertwiner**, and special characteristic 2/3 requires care with Jordan-algebra normalization. This pass explicitly rejects the unsupported extension from dimension matching to an F4/THEORY OF EVERYTHING identification.

## Files, reproduction, and limitations

- `analysis/w33_20261015_toe88_tate_albert_bridge.py`
- `analysis/w33_20261015_toe88_parity_membranes.py`
- `analysis/w33_20261015_toe88_ancilla_syndrome.py`
- `analysis/w33_20261015_toe88_adaptive_mub.py`
- Frozen `data/w33_20261015_toe88_*.json` files, `tests/test_w33_20261015_toe88_all_five.py`, and `.github/workflows/w33_toe88_all_five.yml`.

```bash
python -m analysis.w33_20261015_toe88_tate_albert_bridge
python -m analysis.w33_20261015_toe88_parity_membranes
python -m analysis.w33_20261015_toe88_ancilla_syndrome
python -m analysis.w33_20261015_toe88_adaptive_mub
python -m pytest -q tests/test_w33_20261015_toe88_all_five.py
```

## Five independent next investigations

1. Prove the full F3 two-orbit cyclic-Tate polarization selector agreement conceptually using the equivariant long exact sequence and norm maps, including explicit hypotheses that exclude the three-orbit counterexamples.
2. Construct a finite E6/cubic-surface intrinsic parity cocycle whose evaluation reproduces the 24-face mod2 Bockstein witness **without** scanning all integer face supports, and classify its W(E6) transformation.
3. Build complementary X/Z qutrit check ancilla circuits with flag hooks, repeated spacetime decoding, and numerically bound postcorrection logical failure against an explicit circuit noise model.
4. Bound adversarial basis leakage and loss with a calibrated, setting-blind, energy-constrained optical acceptance protocol; develop robust martingale statistics valid under non-iid channel drift.
5. Independently test whether the characteristic-2 augmentation representation admits ANY Albert Jordan product preservation or a compatible F4 Lie action, and prove a representation obstruction if not.
