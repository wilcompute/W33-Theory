# BT1212 -- Lambda-Lock Adversarial Uncertainty Model

## Purpose

BT1209 gave the clean inference protocol. BT1212 asks the more experimental question: can the lambda-lock survive plausible systematic adversaries?

The accepted rule is now:

\[
q=3\in [q_i-3\sigma_i-\Delta_i,\ q_i+3\sigma_i+\Delta_i]
\]

for every channel \(i\), where \(\Delta_i\) is the worst-case systematic half-width.

## Channels

### Drive channel

\[
q_{\rm drive}=\frac{1}{1+\cos\theta_{\rm BC}}.
\]

At the holonet value \(q=3\),

\[
\frac{dq}{d\cos\theta}=q^2=9.
\]

So the BC-angle channel is calibration-sensitive: small cosine biases are amplified by a factor of nine in q.

Systematics included:

- phase-lock drift,
- dispersion bias,
- recirculation-path calibration.

### Chern channel

\[
q_{\rm Chern}=|C|+1.
\]

Systematics included:

- gap-closing misidentification,
- Berry-grid discretization,
- finite-sample transfer bias.

### Carrier channel

\[
q_{\rm carrier}=N_\perp+1=3.
\]

This is a fixed physical boundary condition for a massless photon.

## Result

The adversarial intervals are:

\[
q_{\rm drive}\in[2.919,3.081],
\]

\[
q_{\rm Chern}\in[2.775,3.225],
\]

\[
q_{\rm carrier}=3.
\]

All contain \(q=3\), so the adversarial protocol passes.

## Files

- Code: `analysis/bt1212_lambda_lock_adversary_model.py`
- Result: `data/bt1212_lambda_lock_adversary_model_summary.json`

## Boundary

These budgets are demonstrator-design budgets, not measured hardware data. The model defines how future data should be judged: no channel gets to pass merely by nominal agreement if systematic half-width excludes the lock.
