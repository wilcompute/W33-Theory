# 36-channel process-tomography protocol

## Claim boundary
This protocol tests one implemented 36-channel linear optical stack. It does not establish a physical theory, a clock, or a hardware result until measured data and uncertainty analysis are supplied.

## Procedure
1. Phase-reference all 36 inputs and reconstruct the complex transfer matrix \(M\), including repeated calibrations.
2. Compare to the declared ideal \(U\) using conditional overlap \(F_{HS}=|Tr(U^\dagger M)|^2/[36 Tr(M^\dagger M)]\).
3. Report common insertion loss, source efficiency, detector efficiency, phase drift, and differential loss separately from conditional overlap.
4. Retain the independent \(|\delta V(F_3)|\le0.05\) and radial-leakage \(\le0.10\) falsifiers.
5. Publish raw transfer matrices, calibration timestamps, estimator code, and bootstrap or Bayesian intervals.

## Acceptance
The engineering target is \(F_{HS}\ge0.99\) with a lower confidence bound at least 0.99 under a predeclared uncertainty model. Failure of that condition is a failed target, not evidence for or against finite Hesse/E8 mathematics.
