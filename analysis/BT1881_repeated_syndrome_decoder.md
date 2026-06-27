# BT1881 — Repeated-Syndrome Decoder

BT1881 extends the BT1878 single-error decoder into a conservative syndrome-history decoder.

## Input

```text
parent code = [[66,13,3]]_3
single-error table = 528 unique nonidentity one-qutrit Pauli syndromes
weight-2 errors detected = 137280
generic weight-2 correction = not claimed
```

## History policy

For two or three syndrome rounds:

```text
000 -> no correction
SS0 or 0SS -> correct if same nonzero syndrome persists two adjacent cycles
S0S -> flag intermittent; request another cycle
SST with T != S -> flag collision/history inconsistency
STR all different -> flag multi-error/noise history
SSS -> correct single-error S with high confidence
```

## Dangerous relation handling

BT1878 identified the first dangerous weight-3 relation:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

A two-edge shadow of this relation can mimic the opposite single-edge completion.  The repeated decoder therefore treats alternating nearest-single outputs from this relation class as untrusted rather than applying a nearest-single correction.

## Verdict

The decoder corrects persistent weight-1 histories and flags relation shadows.  It deliberately does not claim generic weight-2 correction, preserving the distance-3 boundary.

Boundary: history-rule decoder only; not a maximum-likelihood decoder or calibrated detector-time noise model.
