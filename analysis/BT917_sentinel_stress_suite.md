# BT917 — Sentinel Stress Suite

BT917 systematically perturbs the four profile planes and the sentinel channels from BT913.

## Target profile

\[
\left\{\frac9{178},\frac4{13},\frac2{91},\frac7{13}\right\}.
\]

## Perturbation steps

\[
\frac1{178},\qquad \frac1{91},\qquad \frac1{13}.
\]

## Result

- Cases tested: 33
- Positive-response cases: 32
- Baseline energy: 0
- Minimum nonzero energy: 0.00003155406514835409
- Maximum tested energy: 1.375

The only zero case is the exact clean profile.

## Conclusion

\[
\boxed{\text{The sentinel coordinate has a crisp threshold: exact clean profile gives zero, every tested profile perturbation or release/fault channel gives positive energy.}}
\]

This gives the leftover \(+1\) coordinate a useful operational role without turning it into matter content.

## Witness

```text
analysis/bt917_sentinel_stress_suite.py
data/PART_BT917_SENTINEL_STRESS_SUITE_results.json
```
