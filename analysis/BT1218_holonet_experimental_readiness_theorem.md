# BT1218 -- Holonet Experimental Readiness Theorem

## Purpose

BT1218 consolidates BT1207 through BT1217 into a paper-ready theorem packet. The central point is separation:

1. the finite demonstrator has a sharp q-estimator protocol;
2. the encoded GKP/Steinberg machine preserves the q=3 alphabet but is not threshold-ready;
3. the K3/R3 lane has a schema and topology bridge but not a computed metric sample yet.

## Theorem statement

Define

\[
q_{\rm drive}=\frac{1}{1+\cos\theta_{\rm BC}},
\]

\[
q_{\rm Chern}=|C|_{\max}+1,
\]

\[
q_{\rm carrier}=N_\perp+1.
\]

For the holonet values

\[
\cos\theta_{\rm BC}=-\frac23,
\qquad
|C|_{\max}=2,
\qquad
N_\perp=2,
\]

all three channels return

\[
\boxed{q=3.}
\]

Under the BT1212 adversarial budget, the intervals are

\[
q_{\rm drive}\in[2.919,3.081],
\]

\[
q_{\rm Chern}\in[2.775,3.225],
\]

\[
q_{\rm carrier}=3.
\]

So the demonstrator has a precise rejection rule: reject the lock if any calibrated channel excludes q=3 or if the channels become mutually incompatible.

## Encoded invariant

BT1211 and BT1214 add the encoded condition:

\[
q_{\rm bare}=q_{D_4\,GKP}=q_{\rm Steinberg}=3.
\]

The gate signature is

\[
2T=SL(2,3),\quad |2T|=24,
\]

and

\[
Sp(4,3),\quad |Sp(4,3)|=51840.
\]

## R3 boundary

BT1215 fixes the future K3 sample contract:

\[
\chi=24,
\quad
\sigma=-16,
\quad
b_2=22,
\quad
(b_2^+,b_2^-)=(3,19).
\]

But the current K3 sample is still a schema stub, not a computed metric/operator sample.

## Readiness summary

BT1217 gives a 90 percent protocol-readiness score. This means the demonstrator has a rigorous experimental roadmap. It does not mean the fault-tolerant hardware or metric-continuum lane is finished.

## Files feeding this theorem

- BT1207--BT1209: q-estimator and inference protocol.
- BT1212: adversarial systematic budget.
- BT1211 and BT1214: encoded q and Clifford invariance.
- BT1215: K3 geometry schema.
- BT1216: synthetic tomography recovery.
- BT1217: fused readiness dashboard.
