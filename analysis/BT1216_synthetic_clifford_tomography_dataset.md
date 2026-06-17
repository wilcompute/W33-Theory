# BT1216 -- Synthetic Clifford Tomography Dataset

## Purpose

BT1214 defined the encoded Clifford/gate-tomography target. BT1216 creates a deterministic synthetic dataset and recovery report for that target.

This is not hardware data. It is a simulated closure-signature dataset that lets the verifier logic be tested before experiment.

## Single-qutrit target

The expected single-qutrit holonomy group is

\[
2T=\mathrm{SL}(2,3),
\qquad |2T|=24.
\]

The expected element-order spectrum is

\[
\{1^1,2^1,3^8,4^6,6^8\}.
\]

The visibility set is

\[
V\in\left\{0,\frac13,\frac1{\sqrt3},1\right\}.
\]

## Two-qutrit target

The two-qutrit Clifford closure target is

\[
\mathrm{Sp}(4,3),
\qquad |\mathrm{Sp}(4,3)|=51840.
\]

BT1216 samples synthetic closure products with a small closure-error rate and asks whether the target signature is still recovered.

## Result

The synthetic recovery report passes:

- single-qutrit order 24 recovered,
- element-order spectrum recovered,
- visibility errors remain below threshold,
- two-qutrit order 51840 retained,
- sampled closure success \(0.998\ge0.995\).

So the BT1214 target signature can be recovered under the toy noise model.

## Files

- Code: `analysis/bt1216_synthetic_clifford_tomography_dataset.py`
- Result: `data/bt1216_synthetic_clifford_tomography_recovery_summary.json`

## Boundary

This does not enumerate \(\mathrm{Sp}(4,3)\) and does not replace real gate tomography. It is a deterministic synthetic dataset for testing the protocol and dashboard plumbing.
