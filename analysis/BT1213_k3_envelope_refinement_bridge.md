# BT1213 -- K3 Envelope-Grounded R3 Refinement Bridge

## Purpose

BT1210 made a toy convergence ladder. BT1213 grounds that ladder in the existing repo artifact:

```text
data/bt1127_k3_sample_envelope.json
```

That envelope already contains real K3 topological checks:

\[
\chi=24,
\qquad
\sigma=-16,
\qquad
b_2=22,
\qquad
(b_2^+,b_2^-)=(3,19).
\]

It also explicitly says the metric entries are placeholders. BT1213 keeps that boundary.

## What BT1213 adds

BT1213 reads the envelope and constructs a schema-grounded refinement bridge using the existing finite W33 prefactors:

\[
\frac{a_2^{\rm finite}}{a_0}=\frac{14}{3},
\qquad
\frac{a_4^{\rm finite}}{a_2}=\frac{55}{7}.
\]

The bridge tracks proxy rows for

\[
n=4,8,16,32,64,
\qquad h=1/n.
\]

The curvature proxy converges to the K3-normalized target

\[
\int |Rm|^2/(8\pi^2)=24.
\]

## Result

The schema-grounded bridge passes:

- envelope valid,
- \(\chi=24\),
- signature \(-16\),
- \(b_2=22\),
- intersection signature \((3,19)\),
- Ricci-flat \(A_2=0\),
- curvature proxy converges to 24,
- spectral \(C_4\) proxy converges to 24.

## Why this is better than BT1210 alone

BT1210 was a pure interface witness. BT1213 attaches the interface to an actual repo envelope, including the correct K3 topology and the finite W33 product prefactors.

That creates a clean next compute lane:

\[
\text{BT1127 topology/schema envelope}
\to
\text{BT1213 refinement bridge}
\to
\text{future real metric/Dirac K3 sample family}.
\]

## Files

- Code: `analysis/bt1213_k3_envelope_refinement_bridge.py`
- Result: `data/bt1213_k3_envelope_refinement_bridge_summary.json`

## Boundary

This is not a physical K3 metric computation. It is the schema-grounded bridge that tells the future real metric/Dirac compute lane exactly what it must output to graduate from placeholder to R3 evidence.
