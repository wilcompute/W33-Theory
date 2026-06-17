# BT1211 -- Encoded Lambda-Lock Invariance

## Purpose

BT1207 and BT1209 made the lambda-lock operational at the demonstrator layer. BT1211 checks that the same inferred value

\[
q=3
\]

survives the fault-tolerant encoding stack.

## Stack

The stack is:

\[
\text{single photon demonstrator}
\to D_4\text{ GKP inner code}
\to [[240,81,4]]_3\text{ Steinberg outer code}.
\]

At each layer the same q is read three ways:

\[
q_{\rm drive}=3,
\qquad
q_{\rm Chern}=3,
\qquad
q_{\rm logical}=3.
\]

## Interpretation by layer

### 1. Single-photon demonstrator

The bare layer reads:

\[
\cos\theta_{\rm BC}=-2/3,
\qquad
|C|=2,
\qquad
N_\perp=2.
\]

Thus:

\[
q=3.
\]

### 2. Inner \(D_4\) GKP layer

The \(D_4\) code changes the physical representation from a fixed photon-number register to oscillator displacement cosets. It does not change the alphabet:

\[
\text{encoded digit}=\text{qutrit over }\mathbb Z/3.
\]

So the q-estimator survives analog-to-digital conversion.

### 3. Outer Steinberg layer

The outer code is explicitly

\[
[[240,81,4]]_3,
\]

so the encoded logical alphabet remains over \(\mathbb F_3\). The rate is

\[
\frac{81}{240}=\frac{27}{80}.
\]

The code protects 81 logical qutrits; it does not change q.

## Result

All three layers preserve the q-estimator:

\[
\boxed{q_{\rm bare}=q_{\rm GKP}=q_{\rm Steinberg}=3.}
\]

## Files

- Code: `analysis/bt1211_encoded_lambda_lock_invariance.py`
- Result: `data/bt1211_encoded_lambda_lock_invariance_summary.json`

## Boundary

This theorem proves alphabet/estimator invariance, not hardware threshold. It does not solve squeezed-state quality, qutrit GKP generation, syndrome extraction, or cubic-resource preparation. It says that once those layers exist, they preserve the same substrate q rather than replacing it.
