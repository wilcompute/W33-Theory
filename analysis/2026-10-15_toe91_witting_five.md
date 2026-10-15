# TOE91 — Five independent continuations of Vlasov/Witting quantum communications

**15 October 2026**. The project uses the W33 Schläfli/Heisenberg repository and prior Vlasov/Witting work. Development started from master `c53a005ed5425ba50c50357f820e7925b1ba856c` in an isolated Windows Git worktree; the main, heavily dirty checkout was not touched.

The results separate **proved finite geometry**, **calculated toy hardware**, **conditional entropic cryptography**, and **no-go/non-identification**. No composable QKD security, experimental gate, privacy amplification implementation, detector calibration, or theory of everything is established.

## Prior art checked before computation

- **TOE90**, `analysis/2026-10-15_toe90_vlasov_witting_research.md`, arXiv:2503.18431: exactly 40 C^4 Witting rays, 40 orthogonal tetrads, an exact projective 2-design, and the bipartite trusted matched-basis entanglement witness `P_match=(1+4F_Phi)/5 <=2/5` on separable states.
- **BT1408–BT1411** already compiled the 40-ququart delayed-query, 13/40 admission, and 40 sparse 4-mode analyzer bank. No duplicate novelty is claimed.
- **`tools/witting_graph_isomorphism.py`**, `docs/witting_graph_isomorphism.md`, `tools/witting_phase_symplectic_mapped.py`, and `data/_witting/witting_symplectic_clifford_extension.py` predate TOE91's explicit operator lifts.
- **TOE83–TOE88** already developed the distinct 27-vertex/135-edge H27-invariant Schläfli CSS code. Do not identify its chain groups with W33's 40-ray/240-edge spaces.

## 1. Cryptographic finite-key boundary and a calculable asymptotic rate

**New check:** start from the exact isotropic two-ququart family, not from unspecified observed correlations:

```text
rho_v = v |Phi4><Phi4| + (1-v) I16/16
lambda_Phi = (1+15v)/16,   lambda_other=(1-v)/16 (multiplicity 15).
P_match = (1+3v)/4;   entanglement witness threshold v > 1/5.
```

The standard **one-way hashing/coherent-information lower bound for this assumed isotropic quantum state**, and the Devetak–Winter expression for its standard projective matched-basis raw key under a canonical purification, equal:

```text
R_hash = max[0, 2 - S(rho_v)]  bits/pair.
```

The *unclipped* coherent information crosses zero only at `v = 0.6910194010409...`. At `v = 0.25`, the state passes the Witting separability witness (`P_match=0.4375`) but has `2-S(rho)=-1.6244697611`, hence no positive rate from this hashing bound. A negative lower bound is **not** a no-secret-key theorem.

For 8,192 independent matched events and tail `epsilon=0.001`, one-sided Hoeffding uncertainty is `sqrt(log(1000)/(2*8192))`. A statistically significant Witting entanglement witness need not produce a positive key rate. A general **finite-key, composable** QKD security proof requires smooth entropy, leakage estimation, coherent Eve attacks, error correction, authentication, and explicit finite-size privacy amplification. These are **not derived** here.

Producer: `analysis/w33_20261015_toe91_finitekey_analyzer_carrier.py`, entry `finite_key`.

## 2. Calibrated 40-analyzer optical witness (declared component model)

For each of the 40 BT1411 tetrads, form the exact Alice/Bob pairwise measurement matching operator. Perturb each setting by a deterministic, declared four-rail unitary rotation (at most 0.01 radians in the underlying recipe) with independently rotated Alice/Bob analyzer models. Reconstruct the complete 16x16 observed matched-state operator `C_cal` and compute its **actual Hermitian spectral deviation** from the TOE90 ideal `C_0=(I+4Phi)/5`.

Any trusted separable two-ququart state satisfies the rigorous perturbative bound

```text
Tr(rho_sep C_cal) <= 0.4 + ||C_cal - C_0||op.
```

With a declared outcome-independent **per-setting** acceptance factor in `[eta_min=0.94, eta_max=0.98]`, the ratio bound is

```text
P_reported <= (eta_max/eta_min) * [0.4 + ||C_cal-C_0||op].
```

The numerical certificate gives **0.421097360886** as the conservative threshold for this particular hypothetical calibration/efficiency model. The implementation checks all 40 bases and 160 local state projectors; its input unitaries are exact to machine precision.

**Not** real photonic loss data; the bound does not cover outcome-dependent acceptance, detector blindness, side-channel basis leakage, or arbitrary SPAM perturbations.

Producer `analysis/w33_20261015_toe91_finitekey_analyzer_carrier.py`, entry `analyzer_calibration`.

## 3. An explicit finite symplectic ↔ complex-unitary operator bridge

The Witting ray ↔ PG(3,3) graph-label correspondence already exists in `docs/witting_graph_isomorphism.md`; do not count that isomorphism as a TOE91 discovery.

For each standard coordinate vector `e_j in F3^4`, choose the symplectic transvection `T_v(x)=x+omega(x,v)*v`. Transport its 40-point permutation across the repository's published graph isomorphism.

First verify **all 3,240 unordered nonorthogonal Witting ray triples** preserve the complex Bargmann third-order phase invariant `<i|j><j|k><k|i>`; the selected transvections preserve it with residual below 1e-12, while none acts as an antiunitary on the same triplets. This is a necessary *complex projective* lift test, stronger than graph adjacency preservation.

Then explicitly solve the **four projective basis-column phases** of a 4×4 complex operator U from the Witting ray coordinates. Each transvection has a lift satisfying:

```text
U†U = I4                          (to numerical tolerance)
|<ray_{perm(i)} | U ray_i>| = 1   (all 40 rays)
U^3 = I4                          (after global phase normalization)
U permutes all 40 tetrads.
```

The four explicit real/imaginary matrices and their 40-entry permutations are frozen. This is a **genuine concrete 4-mode Hilbert-space operator bridge for the four tested finite-field generators**, not just group order or graph isomorphism. It does **not** establish a cocycle-consistent representation of all PSp(4,3), nor any embedding into two-qutrit 135-data-qudit fault correction. In particular, four coordinate transvections alone may generate only a subgroup of the full symplectic group.

Producers: `analysis/w33_20261015_toe91_symplectic_phase_audit.py`, `analysis/w33_20261015_toe91_symplectic_unitary_lift.py`.

## 4. Explicit separable false-positive using basis-dependent postselection

Construct the exact **product** state `|ray0><ray0| ⊗ |conj(ray0)><conj(ray0)|`. Its matched-outcome probabilities across 40 Witting bases average exactly `0.4` as predicted by TOE90's 2-design witness.

But four bases contain ray0, and each yields **P_match=1** on this separable state. An adversarial setting-dependent acceptance rule that retains these four bases and rejects all remaining bases reports

```text
accepted fraction: 4/40 = 0.10
postselected matched fraction: 1.0 (100%)
```

A softer rule accepting the other 36 bases with probability 0.1 yields:

```text
accepted fraction: 0.19
reported matched fraction: 0.684210526316...
```

This falsifies the unsafe claim that `>40%` **postselected** matching always witnesses entanglement. The 40% operator inequality applies to the **uniformly averaged, trusted-POVM, unconditioned** 40-basis distribution; outcome-dependent or setting-dependent loss requires explicit controls. This attack is stronger than a heuristic intercept-resend cartoon because the underlying source is an **exact separable state** and all reported fractions are from the 40 physical Witting bases.

Producer: `analysis/w33_20261015_toe91_finitekey_analyzer_carrier.py`, entry `product_state_postselection_attack`.

## 5. Witting detector error events are exactly W33 oriented-edge carriers

Each of the 40 four-slot Witting measurements has 4 possible true slots and 3 wrong slots. Hence there are `40*4*3=480` possible **basis-local directed slot substitutions**.

For every such `(basis_id, source_slot, wrong_destination_slot)`, map its two different Witting rays to the directed W33 graph edge `(u,v)`. Each orthogonal pair belongs to **exactly one** tetrad, so the mapping is **one-to-one and onto** all 480 oriented W33 edges.

Each directed edge then has 11 non-backtracking continuations, partitioned into **2 triangle turns and 9 open turns**. The oriented edge-to-vertex ternary incidence boundary `d1: F3^240 -> F3^40` has exact rank 39 and cycle-kernel dimension **201**. The certificate constructs the entire 40×240 incidence matrix over F3 and checks its rank.

Thus the previously abstract W33 non-backtracking `B=T+O` propagator has a natural, *operationally labelable* classical carrier: time-ordered bad-detector-slot events after ququart basis selection.

**Important firewall:** an error-event label is not a physical two-qutrit Pauli operator. This 40-ray/240-edge W33 chain complex is **not** the separate 27-vertex/135-edge Schläfli H27 CSS code; no encoded isometry, chain map, syndrome recovery or fault-tolerant physical operation has been constructed. This is an experimentally falsifiable **error-log compiler**, not a completed quantum ECC.

Producer: `analysis/w33_20261015_toe91_finitekey_analyzer_carrier.py`, entry `detector_to_W33_carrier`.

## Reproduction / audit

```bash
python -m analysis.w33_20261015_toe91_symplectic_phase_audit
python -m analysis.w33_20261015_toe91_symplectic_unitary_lift
python -m analysis.w33_20261015_toe91_finitekey_analyzer_carrier
python -m pytest -q tests/test_w33_20261015_toe91_witting_five.py
```

Three exact/numerically stabilized JSON certificates under `data/w33_20261015_toe91_*.json`, dedicated test module and GitHub Actions workflow freeze the results.

## Five best independent next directions

1. **Complete the 4D Weil/Witting representation:** generate the entire `PSp(4,3)` action from a certified full generator set, compute projective multipliers and the central extension, and verify whether the four-mode unitaries implement the required group relations globally.
2. **Composable finite-key Witting QKD:** derive smooth-min-entropy bounds and practical privacy amplification with Eve's quantum side information; a 40%-matched entanglement witness alone cannot give a key rate.
3. **Instrument-calibrated optical test:** compile the 40 analyzer settings and losses into an experimental bill of materials, uncertainty budget, setting-blind heralding and a preregistered entanglement threshold.
4. **Detector-adversarial stress testing:** search over local hidden-variable, detector-blinding and measurement-device-dependent attacks under measured per-basis and per-outcome efficiency constraints; optimize tight worst-case separable bounds.
5. **Physical W33 edge-code bridge:** realize a checkable process/instrument that converts a measured ququart detector substitution into a protected Pauli channel on an encoded qutrit space and supplies verified 135-edge H27/CSS stabilizer syndromes.
