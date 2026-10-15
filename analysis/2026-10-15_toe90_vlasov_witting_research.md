# TOE90 — Vlasov Witting-polytope quantum communication: W33 rays form an exact ququart 2-design and a trusted EPR entanglement witness

**15 October 2026.** Independent check of **Alexander Yu. Vlasov**, *Scheme of quantum communications based on Witting polytope*, arXiv:2503.18431v1 (24 March 2025), https://arxiv.org/html/2503.18431 ; related *Penrose dodecahedron and the Witting polytope are identical in CP(3)* by Waegell and Aravind, arXiv:1701.06512. The paper's claims are distinguishable below from new calculations and from W33-Theory prior work.

## Repository novelty firewall — not a newly discovered Witting/W33 identification

The project **already explicitly incorporated Vlasov**:
- `analysis/BT1408_witting_contextual_communication_bridge.md` and `tools/bt1408_witting_contextual_communication_bridge.py`: 40 Witting rays, exactly 40 four-state tetrads, `1+12+27=40`, delayed-query admission `13/40`; distinction between 36/40 exact classical one-mark satisfiability optimum and Abramsky–Barbosa contextual fraction 1.
- `analysis/BT1409_witting_duplex_admission_scheduler.md`: logical state compatibility `13/40`, four basis apertures per ray, `1/10` basis-witness incidence aperture.
- `analysis/BT1410_witting_delayed_query_frame_compiler.md`: full 1600 query-pair table; 640 tetrad-local basis/slot records.
- `analysis/BT1411_witting_basis_analyzer_unitaries.md`: full bank of 40 ququart analyzer unitaries, with sparsity families 1 direct / 12 direct-plus-tritter / 27 contextual.
- Several BT15xx research packets already reuse these results.

**TOE90 does not claim discovery of the Witting/W33 bridge.** It builds a separately testable *operational 2-design and bipartite EPR entanglement witness* for the existing BT1411 analyzers, calibrates its shot-count under a declared detector-error model, and analyzes a specified intercept-and-resend attack.

## Read-through of Vlasov's actual paper

Section II provides 240 Witting polytope vertices in C^4 modulo phases, yielding 40 projective normalized rays: four coordinate states and 36 phase states built from 3rd roots of unity. Reflection symmetries and 40 four-state bases are tabulated.

Section III proposes maximally entangled ququart pairs `|Phi4> = (|00>+|11>+|22>+|33>)/2`, where Alice measures a Witting basis and Bob the complex-conjugated counterpart. It describes the naive same-basis rate 1/40 and contextuality-aware state/basis admission.

Section IV compares contextual card markings and classical substitutes. The paper includes examples with 34/40 valid tetrades; the project independently has an **exact 36/40** optimum. Never reinterpret the illustrative 34/40 value as a global optimum.

Section V acknowledges no practical ququart implementation and discusses the delayed-query state-pair compatibility probability 13/40. The paper **does not** establish a composable finite-key QKD security theorem, SPAM calibration, or device-independent entanglement test.

## Exact ray geometry and 2-design theorem

Generate exactly the 40 rays using the equations from Section II, independently using the existing BT1408 reference implementation. Their squared pairwise overlaps are:

```
40 diagonal ordered pairs:       1
480 off-diagonal ordered pairs:  0
1080 off-diagonal ordered pairs: 1/3
```

Define adjacency by zero overlap; the orthogonality graph has parameters SRG(40,12,2,4) and 40 tetrahedral maximum cliques, each ray belonging to exactly four. These reproduce the paper's Witting measurement geometry and the established repo W33 geometry.

The second frame potential for 40 unit rays is exactly

```
FP_2 = [40 + 1080*(1/9)]/40^2
     = 1/10 = 2/[d(d+1)] at d=4.
```

The Welch lower bound is saturated. By the equality characterization, these 40 rays are an exact **complex projective 2-design**:

```
(1/40) sum_r (|r><r|) tensor (|r><r|)
  = (I_16 + SWAP)/20.
```

A separate 16x16 matrix implementation checks this identity numerically to absolute tolerance 1e-12; the *theorem* follows from the exact integer overlap census and Welch equality. This is standard projective-design mathematics instantiated in the Witting configuration, not claimed as a novel general 2-design theorem.

## Novel bridge within the project: use all 40 ququart analyzers as an EPR entanglement witness

Let Alice/Bob share any two-ququart state rho_AB. For each of the 40 Witting bases B, Alice measures projectors P_j and Bob the conjugate projectors P_j^* on that same basis, recording the probability of matching state labels (not the raw card number from another arbitrary labeling).

Define

```
C = (1/40) sum_B sum_{r in B} P_r tensor P_r*.
```

Because every ray belongs to exactly four bases, use the partial conjugation of the 2-design operator to obtain the exact identity

```
C = (I_16 + 4|Phi4><Phi4|)/5.
```

Thus for `F_phi = <Phi4|rho_AB|Phi4>` the *average same-basis matching probability* is

```
P_match = Tr(rho_AB C) = (1+4 F_phi)/5.
```

The spectrum of C is `1^1 + (1/5)^15`. For all separable states, `F_phi<=1/4`, hence `P_match<=2/5=0.4`. Any trusted observed *basis-average* matching rate above 40% certifies entanglement. It does **not** by itself certify quantum-key security, causal ordering, no-signaling, contextuality, or device independence.

For the isotropic state `rho_v=v|Phi4><Phi4|+(1-v)I_16/16`:

```
P_match = (1+3 v)/4,  detectable iff v>1/5.
```

This derives a simple optical experiment with the existing 40 BT1411 analyzer matrices. The inequality applies only when the intended bases/projectors are actually implemented and the data sampling/loss assumptions are controlled.

## Exact attack categories and an important negative control

For a uniform random Witting basis E selected by an intercept-and-resend eavesdropper and target Alice/Bob basis B:

```
P_match(B,E) = (1/4) sum_{i in B, j in E} |<i|j>|^4.
```

Among the 40 ordered possibilities E for each fixed B:

| E vs B | Counts | Matching probability |
|---|---:|---:|
| same basis | 1 | 1 |
| exactly one common ray | 12 | 1/2 |
| disjoint | 27 | 1/3 |

Thus averaged uniformly over E, `P_match=(1+12/2+27/3)/40=2/5`: a 60% raw outcome mismatch on matched-basis test rounds. This specified intercept/resend attack **saturates** the separable threshold. It is not an optimization over all attacks or a QKD key-rate lower bound.

## Synthetic detector readout calibration / falsifiable shot target

Assume each side independently reports the correct 4-outcome symbol with probability `1-e` and, with total probability `e=0.02`, one of three wrong symbols uniformly.

For a true matched symbol, the reported equality probability is `a=(1-e)^2+e^2/3`. For a true mismatch it is `b=2e(1-e)/3 +2e^2/9`. A true match probability p becomes `p_obs=b+(a-b)p`.

- Separable true bound `p=2/5` -> observed calibrated bound `0.392106666... `
- Alternative isotropic visibility `v=1/4`: true `p=7/16` -> observed `0.427633333...`
- Choose **8192** i.i.d. accepted paired measurements with uniform secret random tetrad settings. Reject the separable null at **3350** or more reported matches.
- Exact binomial null tail: **0.000961720054...**; alternative detection power: **0.999707050783...**.

These are model-specific theoretical design targets. The simple noise-calibration correction is invalid for uncharacterized detector efficiency, setting-dependent postselection, detector blinding, adaptive device attacks, basis leaks, or correlated state preparation. The project already separately tests such limitations for a qutrit MUB protocol (TOE87/TOE88), not a ququart hardware experiment.

## Reproduction

```bash
python -m analysis.w33_20261015_toe90_vlasov_ququart_design
python -m analysis.w33_20261015_toe90_witting_shot_certification
python -m pytest -q tests/test_w33_20261015_toe90_vlasov_ququart_design.py
```

Sources:
`analysis/w33_20261015_toe90_vlasov_ququart_design.py`,
`analysis/w33_20261015_toe90_witting_shot_certification.py`,
two `data/w33_20261015_toe90_*.json` certificates, and the TOE90 regression workflow.

## Five independent next research directions

1. **Witness experiment:** compile measurement ordering, readout calibration and a signed finite-shot acceptance test for all 40 BT1411 sparse four-mode optical analyzers; demonstrate on calibrated devices before interpreting physical entanglement.
2. **Composable QKD:** derive a finite-key security proof—or an explicit practical attack—for Witting-context QKD with reused rays, basis announcements and loss. Entanglement and contextuality tests are insufficient alone.
3. **Witting/Schläfli/E6 symmetry:** construct an explicit intertwiner between the projective 40-ray `U(4)` Witting symmetry and the projective symplectic action `PSp(4,3)` on 40 W33 Pauli points, with certified generator conjugation, not only SRG isomorphism.
4. **Leakage-aware witness:** derive adversarial measurement-device and setting-dependent loss bounds for the 40-context ququart protocol, paralleling TOE87's ququart-independent MUB adversarial tests.
5. **Hardware/cohomology integration:** connect measured basis-transition errors, repeated-ray contexts and ququart contextuality statistics to the native H27/CSS fault-syndrome modules via an operational channel map, while distinguishing mathematical relabeling from a physical fault-tolerant mechanism.
