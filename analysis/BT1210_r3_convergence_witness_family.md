# BT1210 -- R3 Convergence Witness Family

## Purpose

BT1202 gave the R3 checklist. BT1210 makes it executable as a toy finite-refinement witness family.

This is not a proof of the K3/spacetime continuum. It is a proof-of-shape: the R3 residual can be written as a monotone witness protocol instead of a vague open problem.

## Refinement ladder

The toy family uses refinements

\[
n=4,8,16,32,64,128,
\qquad h=1/n.
\]

The tracked witnesses are:

- shape-regular minimum quality,
- curvature energy,
- spectral moment error,
- gauge holonomy error,
- operator resolvent error,
- metric-propinquity proxy,
- scale-separation ratio.

The model is deliberately simple:

\[
E_{\rm curv}(h)=24+3h^2,
\]

\[
\epsilon_{\rm spec}(h)=h^2,
\]

\[
\epsilon_{\rm gauge}(h)=h,
\]

\[
\epsilon_{\rm op}(h)=h^2,
\]

\[
\epsilon_{\rm metric}(h)=h.
\]

## Result

All monotonicity checks pass:

\[
h\downarrow,
\qquad
\text{shape quality}\uparrow,
\qquad
E_{\rm curv}\downarrow24,
\]

and

\[
\epsilon_{\rm spec},\epsilon_{\rm gauge},\epsilon_{\rm op},\epsilon_{\rm metric}\downarrow0.
\]

## Why this matters

This turns R3 into a future finite-data program. A real R3 proof now has a template:

1. choose a concrete K3/spacetime approximant sequence;
2. measure the same seven witnesses;
3. prove monotone bounds or compactness;
4. only then claim a metric continuum.

## Files

- Code: `analysis/bt1210_r3_convergence_witness_family.py`
- Result: `data/bt1210_r3_convergence_witness_family_summary.json`

## Boundary

This is a toy witness family. It is not the physical K3 refinement sequence and it does not prove continuum emergence. It gives the correct finite-verifier interface for the eventual proof.
