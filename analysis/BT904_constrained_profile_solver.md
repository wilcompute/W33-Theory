# BT904 — Constrained \(9\times9\) Profile Solver

BT904 constructs the first constrained multiplicity-space scaffold inside

\[
V_{\rm profile}=\mathbb C^9\otimes\mathrm{Std}(S_3).
\]

It is **not** an empirical mass fit. It is a constructive proof that the old numerical constants can be housed in the profile commutant without damaging the shifted-reflection Yukawa skeleton.

## Rotation planes

The solver uses four disjoint two-planes inside \(\mathbb C^9\):

\[
\sin\theta_C=\frac3{\sqrt{178}},
\]

\[
\sin^2\theta_{12}=\frac4{13},\qquad
\sin^2\theta_{13}=\frac2{91},\qquad
\sin^2\theta_{23}=\frac7{13}.
\]

The ninth multiplicity coordinate remains available as a neutral/sentinel coordinate.

## Equivariance

The profile operators lift as

\[
A\otimes I_2,\qquad B\otimes I_2,
\]

so they commute with the \(S_3\) standard rotation and reflection generators. The up/down Gram profiles themselves do not commute, which is exactly the required location for CKM/PMNS mixing.

## Koide bridge

Koide remains the exact equal-norm condition

\[
Q=\frac23\Longleftrightarrow
\|y_{\mathbf1}\|^2=\|y_{\mathbf2}\|^2=\frac12.
\]

## Conclusion

\[
\boxed{\text{A single }9\times9\text{ multiplicity-space profile can house Cabibbo, PMNS scaffold, and Koide while preserving flavor }S_3.}
\]

## Witness

```text
analysis/bt904_constrained_profile_solver.py
data/PART_BT904_CONSTRAINED_PROFILE_SOLVER_results.json
```
