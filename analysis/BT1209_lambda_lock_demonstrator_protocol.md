# BT1209 -- Lambda-Lock Demonstrator Inference Protocol

## Purpose

BT1207 made the lambda-lock into a three-channel q-estimator. BT1209 turns it into a lab-facing protocol.

The three measured inputs are:

\[
\cos\theta_{\rm BC},\qquad |C|,\qquad N_{\perp}.
\]

They infer:

\[
q_{\rm drive}=\frac{1}{1+\cos\theta_{\rm BC}},
\]

\[
q_{\rm Chern}=|C|+1,
\]

\[
q_{\rm carrier}=N_{\perp}+1.
\]

For the holonet:

\[
\cos\theta_{\rm BC}=-\frac23,\qquad |C|=2,\qquad N_{\perp}=2,
\]

so

\[
\boxed{q_{\rm drive}=q_{\rm Chern}=q_{\rm carrier}=3.}
\]

## Protocol

1. Estimate the BC twist from the recirculation phase orbit and compute \(q_{\rm drive}\).
2. Estimate the two-tone pump Chern magnitude and compute \(q_{\rm Chern}\).
3. Use the physical massless-photon transverse-state count \(N_{\perp}=2\) as the carrier channel.
4. Propagate uncertainties and require all three 3-sigma intervals to contain \(q=3\).
5. Require the weighted consensus to contain \(q=3\) and the channel estimates to be mutually compatible.

## Default certificate

With a conservative example uncertainty

\[
\sigma_{\cos}=0.002,\qquad \sigma_C=0.05,
\]

BT1209 gives:

\[
q_{\rm drive}=3.000\pm0.018,
\]

\[
q_{\rm Chern}=3.000\pm0.050,
\]

\[
q_{\rm carrier}=3.000.
\]

All channels pass the 3-sigma lock.

## Files

- Code: `analysis/bt1209_lambda_lock_demonstrator_protocol.py`
- Result: `data/bt1209_lambda_lock_demonstrator_protocol_summary.json`

## Boundary

The carrier channel is not an experimentally varied helicity law. It is a fixed physical channel: a massless photon has two transverse states. The falsifier is whether the measured drive and Chern channels independently infer the same q required by that carrier.
