# TOE87 — Five independent TOE86 continuations: a stable Heisenberg module theorem, triple-orbit counterexamples, integral Bocksteins, a fault-aware routing model, and adversarial quantum-memory nulls

**15 October 2026 — checked in an isolated worktree against the W33-Theory repository.**

This pass executes all five TOE86 follow-ups. Distinguish carefully: the representation identities, module filtrations, Bockstein ranks, and synthetic counterexamples are **exact finite mathematics**; the stochastic circuit and quantum-channel numerical results are **declared idealized models**. None is experimental evidence of a Theory of Everything, gravity, a physical temporal arrow, or a working fault-tolerant quantum computer.

## Front 1 — Is the 468-pair H1/H2 rank polarization forced for arbitrary square additions?

TOE86 established that each of its 468 admissible **two**-H27-orbit square-face surgeries has a common unique rank-minimizing order-nine subgroup on H1(F3) and H2(F3). To look for a plausible general exact-sequence theorem, add a **third** complete 27-square orbit to the selected TOE83 pair (0,10), ensuring H27 invariance and a valid cellular chain complex. Rebuild every induced signed face/edge action, and compute H1 and H2 quotient/kernel actions over F3.

**Explicit failure of a broader uniqueness claim:** orbit triple (0,10,1) has 45 triangles +81 squares =126 faces, rank d2(F3)=105, H1 dimension 4 and H2 dimension 21. For the four noncentral Pauli direction representatives (1,0,0), (0,1,0), (1,1,0), and (1,2,0), the exact rank(g-I) vectors are:

```
H1: [2,2,2,2]  (no unique preferred direction)
H2: [13,12,13,13] (second direction preferred)
```

Ten of twelve tested deterministic additional orbits break *unique* shared minimizer agreement. This is **not an exhaustive three-orbit census**, and does not contradict the 468 two-orbit theorem. It rigorously disproves the naïve assertion that every H27-invariant extension preserves a common **unique** minimizing direction. A stronger future theorem requires explicit hypotheses distinguishing two-orbit surgery from arbitrary H27-invariant extensions.

## New structural theorem discovered while executing front 1

A different H1/H2 relationship **is** forced by equivariant cellular chains, independently of square-pair selection, over F2.

For a connected two-dimensional cellular complex `C2 -> C1 -> C0`, the Euler identity in the Grothendieck representation ring is:

```
[H1] - [H2] = [H0] - [C0] + [C1] - [C2].
```

For the native H27 Schläfli complex with **any two complete regular square orbits**:

- `C0 = Reg(H27)` (one 27-point regular H27 orbit);
- `C1 = 5 Reg(H27)` (five 27-edge regular H27 orbits);
- `C2 = T45 + 2 Reg(H27)` (five 9-triangle H27 orbits, plus two 27-square regular orbits);
- `H0 = trivial` because the underlying graph is connected.

The independent module projector verifies over F2:

```
Reg27 = 1 + V1+V2+V3+V4 + 3 W6
T45   = 5(1) + 2(V1+V2+V3+V4) + 4 W6
```

where each `Vi` is a different 2D binary simple module inflated from H27/Z, and `W6` the faithful 6D simple module.

Consequently the virtual class is `[H1]-[H2]=2[W6]-2[1]`. Since char(F2)=2 does not divide |H27|=27, Maschke semisimplicity upgrades the virtual equality to a **stable, actual H27-module isomorphism**:

```
H1(F2) + 2 (trivial 1D)   ~=   H2(F2) + 2 (faithful 6D).
```

It holds for any such two-orbit complex, not merely the 468 admissible pairs. The code verifies all cell orbit sizes, projector simple multiplicities, and all 13 classes representing the 468 pairs. The statement does not force an F3 clock rank selector because F3[H27] is not semisimple.

## Front 2 — Full modular fingerprints for all 13 families

For every representative of the full 1296-element direction-preserving H27 normalizer's 13 equivalence classes, construct chain-level H1 and H2 representations **over F2 and F3**. Record exact binary irreducible multiplicities via central/maximal-abelian subgroup projectors and the complete augmentation-ideal Loewy filtrations over F3.

| Integral H1 torsion | Pairs | Binary H1 simples | Binary H2 simples |
|---|---:|---|---|
| none | 36 | 3 W6 + V1+V2+V3+V4 | W6 + V1+V2+V3+V4 + 2(1) |
| (Z/3)^2 | 360 | 2 W6 | 2(1) |
| (Z/6)^2 | 72 | 2 W6 + one Vi | 2(1) + the same Vi |

The identity from front 1 holds in each line: subtract H2 simples from H1 simples to obtain 2 W6 minus 2 trivial modules.

**All 36 torsion-free cases** have F3 augmentation-radical dimension sequences:

```
H1: [26,24,21,15,11,6,3,1,0]
H2: [16,13,10,6,4,2,1,0]
```

**All 432 torsion cases** have:

```
H1: [14,13,11,7,4,1,0]
H2: [4,3,2,0]
```

These are *layer dimension sequences*, not proof that the entire modules within one family are conjugate/indecomposable. Modules with identical Loewy layers may carry different extension data. The binary/simple and F3/Loewy fingerprints are exact checks within the 13-class enumeration.

## Front 3 — Gate faults, syndrome readout, and a deliberately limited decoder

Compile TOE86's exact signed 135-qutrit chain-automorphism gates for H27 generators x, y and z using two connectivity assumptions: (a) unconstrained all-to-all SWAP decomposition (90 SWAPs) and (b) the generated linear nearest-neighbor SWAP schedules (4,740, 1,828, and 498 adjacent SWAPs).

Run a reproducible stochastic circuit-level **X-type** qutrit Pauli fault model, propagating faults through every physical SWAP. Add local signed orientation-inversion gate faults, conditional correlated two-wire faults, and independent ternary syndrome readout digit errors. Use an explicitly weak single-site syndrome lookup and score *exact zero residual physical X error* (not logical success), as well as fault/syndrome rates. With 192 seeded shots per layout/generator:

```
p_SWAP = 0.0002
p_local_orientation_inversion = 0.0002
p_syndrome_readout_wrong_digit = 0.001
p_correlated_two_wire_given_SWAP_fault = 0.10
```

| Generator | Layout | SWAP count | Exact independent-gate no-fault probability |
|---|---|---:|---:|
| x | all-to-all | 90 | 0.97161 |
| x | linear NN | 4740 | 0.38332 |
| y | all-to-all | 90 | 0.97628 |
| y | linear NN | 1828 | 0.68960 |
| z | all-to-all | 90 | 0.97863 |
| z | linear NN | 498 | 0.90194 |

These exact fault-exposure probabilities depend on the hypothetical rates, not on measured devices. The accompanying seeded Monte Carlo JSON freezes syndrome readout, correlation and decoder observations. No repeated stabilizer extraction circuit, logical threshold, realistic native photonic operation, or noise-calibrated device is claimed.

## Front 4 — Adversarial entanglement-breaking null for the temporal-memory experiment

The earlier TOE86 single-superposition return test, based on an entanglement-breaking clock-basis dephasing null, **does not exclude arbitrary entanglement-breaking channels**. An adversarial channel that measures and reprepares in a rotated basis can reproduce the chosen superposition probe *perfectly*, giving success probability 1. This is an important explicit negative control.

Construct all 12 qutrit states forming the four MUB bases: the computational Z basis and the three quadratic Fourier bases. They satisfy the complete MUB overlaps and form an exact complex projective **2-design** (validated numerically by its second-moment operator). For trusted randomized input-state preparation and state-matched output survival tests, any entanglement-breaking qutrit channel obeys

```
mean state fidelity <= 2/(3+1) = 1/2
```

since its normalized Choi state is separable and its maximally entangled overlap is <=1/3.

Clock-basis dephasing and the adversarial rotated-basis dephasing both have **mean fidelity 0.5** over the 12 inputs, while the synthetic coherent channel with visibility v=0.25 has mean fidelity **0.625**.

For an explicitly specified nuisance model with 2% symmetric wrong-class readout, 3% independent uniform subspace leakage/replacement, and 8% state-independent heralded loss, the code calculates the calibrated EB bound and coherent alternative. With **1,200 independently randomized accepted shots**, the rejection threshold is **643** successful state-matched returns, with exact binomial null-tail probability <=0.001 and model alternative power **0.9999998200492886**. The binomial model is valid for independently and uniformly randomized preparation settings each accepted shot, *not* a fixed balanced allocation (Poisson-binomial), and **not** when losses depend on the secret preparation setting.

Do not interpret this test as device-independent certification, non-Markovianity, spacetime emergence or a physical time-arrow detection. Adversarial preparation/measurement correlations, state-dependent postselection, coherent calibration drift and channel memory are not bounded by the proposed i.i.d. test.

## Front 5 — Integral torsion via explicit Bockstein connecting maps

TOE86 computed exact SNF patterns across all 468 two-orbit pairs: 36 torsion-free, 360 with factors [3,3], and 72 with factors [6,6]. This pass goes past invariant-factor counts by constructing the Bockstein on 2-cycles:

```
beta_p([x mod p]) = [d2(x_lift)/p mod p] in H1(Fp).
```

Use exact oriented integer d2. Compute every mod-p H2 kernel basis, choose a canonical integer coefficient lift, divide the resulting integer boundary by p (exact divisibility verified), and reduce mod p modulo face-boundary span. The exact image ranks are

| Torsion | Bockstein image rank mod 2 | Bockstein image rank mod 3 |
|---|---:|---:|
| none (36 pairs) | 0 | 0 |
| [3,3] (360 pairs) | 0 | 2 |
| [6,6] (72 pairs) | 2 | 2 |

These are chain-level geometric witnesses for the prime-primary torsion and agree with the Smith invariant factors for all 13 pair classes. A simple cross-orbit square *shared-edge histogram* does **not** uniquely classify torsion: the profile [675,54,0,0,0] occurs for both torsion-free and [6,6] representatives. The certificate freezes this negative result, preventing a spurious local-overlap explanation for 2-torsion.

## Reproduction and validation

- `analysis/w33_20261015_toe87_modular_bockstein_triples.py` — all 13 H1/H2 modular classifications; Bockstein; 12 triple-orbit checks.
- `analysis/w33_20261015_toe87_euler_stable_module.py` — representation-ring Euler theorem, orbit decomposition and all 13 class checks.
- `analysis/w33_20261015_toe87_fault_aware_routing.py` — two-layout stochastic gate/syndrome/decoder fault model.
- `analysis/w33_20261015_toe87_adversarial_temporal.py` — full four-MUB projective design, adversarial entanglement-breaking spoof, and calibrated binomial analysis.
- `data/w33_20261015_toe87_*.json` — frozen exact finite certificates and reproducible numerical synthetic models.
- `tests/test_w33_20261015_toe87_all_five.py` and GitHub Actions CI.

```bash
python -m analysis.w33_20261015_toe87_modular_bockstein_triples
python -m analysis.w33_20261015_toe87_euler_stable_module
python -m analysis.w33_20261015_toe87_fault_aware_routing
python -m analysis.w33_20261015_toe87_adversarial_temporal
python -m pytest -q tests/test_w33_20261015_toe87_all_five.py
```

## Five independent next investigations

1. **Cyclic-group Tate cohomology:** derive an exact F3 representation-theoretic formula for the two-orbit joint rank selector or produce an explicit two-orbit counterexample once the admissibility condition is altered.
2. **Primary torsion local systems:** find a geometric 2-cocycle/relative spin structure that detects Z/2 content invisible to the square-pair shared-edge histogram; extract genuine Bockstein cochain witnesses.
3. **Fault-tolerant syndrome circuit:** compile repeated qutrit stabilizer measurement ancillas, hook-error propagation, gate-dependent noise and a nontrivial decoder on a specified coupler graph; bound circuit-level logical failure.
4. **Adversarial temporal certification:** implement a loophole-aware four-MUB optical test with random settings, explicit loss heralding, device calibration and SPAM-robust entanglement witnesses; challenge it with adaptive EB strategies.
5. **Integral-to-modular representation bridge:** characterize whether Bockstein image and Loewy filtrations define natural H27-equivariant extension classes across all 13 families, rather than coincidental layer fingerprints.
