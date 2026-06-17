# BT1207 -- Lambda-Lock Operational q-Estimator

## New idea

BT1201 stated the lambda-lock as a unifying law:

\[
\lambda=q-1=2
\]

appears as BC drive deficit, topological protection strength, and photon transverse-state count. BT1207 turns that into an operational falsifier: each face independently estimates the substrate dimension.

## Three estimators

From the BC drive relation,

\[
\cos\theta_{\rm BC}=-\frac{q-1}{q}=-1+\frac1q,
\]

so

\[
\boxed{q_{\rm drive}=\frac{1}{1+\cos\theta_{\rm BC}}.}
\]

From the spin-\((q-1)/2\) two-tone pump,

\[
|C|_{\max}=q-1,
\]

so

\[
\boxed{q_{\rm Chern}=|C|_{\max}+1.}
\]

From the massless photon carrier,

\[
N_{\perp}=2,
\]

so

\[
\boxed{q_{\rm carrier}=N_{\perp}+1=3.}
\]

For the holonet values,

\[
\cos\theta_{\rm BC}=-\frac23,\qquad |C|=2,\qquad N_{\perp}=2,
\]

we get

\[
\boxed{q_{\rm drive}=q_{\rm Chern}=q_{\rm carrier}=3.}
\]

## Why this is stronger

This converts the lambda-lock from a coherence statement into a measurement protocol. The demonstrator can test two of the three quantities directly:

1. reconstruct the BC twist angle or its phase orbit and compute \(q_{\rm drive}\);
2. reconstruct the two-tone pump Chern response and compute \(q_{\rm Chern}\).

The third quantity is fixed by the physical carrier: a massless photon has two transverse states. Agreement of all three estimators is a sharp substrate-level check.

## Near misses

The exact scan shows:

- \(q=2\) has \(\cos\theta=-1/2\), so the BC angle is rational-compatible and the Chern strength is only \(|C|=1\). It is the qubit near-miss.
- \(q=4\) and higher are BC-aperiodic by the Niven-style rational-cosine certificate, but their Chern strength is \(|C|\ge3\), so they do not match the two-state massless carrier.
- \(q=3\) is the only integer in the scan that closes the master seed \(q!=2q\), the BC estimator, the Chern estimator, and the carrier estimator simultaneously.

## Result artifact

- Code: `analysis/bt1207_lambda_lock_q_estimator.py`
- Result: `data/bt1207_lambda_lock_q_estimator_summary.json`

## External anchors used

- Two-frequency topological frequency conversion gives a Chern-quantized energy-pumping law between irrationally related drives.
- GKP codes are naturally continuous-variable lattice codes, supporting the page-36 distinction between unencoded demonstrator and fault-tolerant lattice stack.
- Wigner little-group analysis is the correct external language for why a massless photon has transverse helicity states rather than a massive-vector longitudinal mode.

## Boundary

The carrier estimator is not a variable-helicity law. It is a fixed physical fact about the massless photon. The theorem says that the substrate value \(q=3\) is uniquely compatible with that fact.
