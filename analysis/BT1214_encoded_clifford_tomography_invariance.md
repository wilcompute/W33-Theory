# BT1214 -- Encoded Clifford / Gate-Tomography Invariance

## Purpose

BT1211 showed that the inferred q-value survives encoding:

\[
q_{\rm bare}=q_{D_4\,GKP}=q_{\rm Steinberg}=3.
\]

BT1214 checks the next invariant: the Clifford closure signature.

The target is:

\[
2T=\mathrm{SL}(2,3),\qquad |2T|=24
\]

at the single-qutrit holonomy layer, and

\[
\mathrm{Sp}(4,3),\qquad |\mathrm{Sp}(4,3)|=51840
\]

at the two-qutrit Clifford layer.

## Encoded tomography protocol

The protocol has four tests:

1. **Single-qutrit holonomy fingerprint.** Recover \(2T=\mathrm{SL}(2,3)\), order 24, with element-order spectrum \(\{1,1,8,6,8\}\).
2. **Two-qutrit Clifford closure.** Recover \(\mathrm{Sp}(4,3)\), order 51840, modulo Pauli and frame conventions.
3. **Encoded alphabet preservation.** Verify logical Pauli/displacement classes close over \(\mathbb F_3\).
4. **Logical-code preservation.** Verify the outer operations preserve the \([[240,81,4]]_3\) codespace and act on 81 logical qutrits.

## Layer signatures

The static target signature is preserved across:

- bare demonstrator,
- inner \(D_4\) GKP layer,
- outer Steinberg logical layer.

At every layer:

\[
q=3,
\qquad
|2T|=24,
\qquad
|\mathrm{Sp}(4,3)|=51840.
\]

## Why this matters

BT1211 proved q-invariance. BT1214 upgrades that to gate-signature invariance. If the encoded machine is truly the same holonet rather than a new architecture, it must preserve both:

\[
q=3
\]

and

\[
\mathrm{Clifford}_{2\text{-qutrit}}\cong \mathrm{Sp}(4,3).
\]

## Files

- Code: `analysis/bt1214_encoded_clifford_tomography_invariance.py`
- Result: `data/bt1214_encoded_clifford_tomography_invariance_summary.json`

## External benchmarking anchor

Randomized-benchmarking tomography is the right experimental style here because it reduces sensitivity to state-preparation-and-measurement errors while still reconstructing gate information. The holonet version should use its finite Clifford closure as the benchmark ensemble.

## Boundary

BT1214 is a target-signature verifier and protocol map. It does not claim that encoded hardware has achieved \(\mathrm{Sp}(4,3)\) closure. It says exactly what must be measured once GKP and Steinberg syndrome recovery exist.
