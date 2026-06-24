# BT1689 — Ancilla Success Accounting

## Model

For an LCU with coefficient mass \(\lambda\), the single-try success probability is

\[
p=\lambda^{-2}.
\]

Without amplification, the shot-noise SNR scales by

\[
\sqrt p.
\]

## Separate-port accounting

For the resonance port,

\[
\lambda=1.2939453125,
\]

so

\[
p=0.597413338718975.
\]

The shot inflation is

\[
1.6739564538002014,
\]

and the unamplified effective SNR is

\[
28.625716516580017.
\]

For the companion port,

\[
\lambda=1.25,
\]

so

\[
p=0.64.
\]

The shot inflation is

\[
1.5625,
\]

and the unamplified effective SNR is

\[
29.865313063424016.
\]

## Monolithic two-port accounting

If both ports are selected through one combined LCU with

\[
\lambda=2.5439453125,
\]

then

\[
p=0.1544685004281349,
\]

shot inflation is

\[
6.473811864852905,
\]

and effective SNR is

\[
14.557904134592752.
\]

## Conclusion

Separate-port postselection is already high-success.  A monolithic two-port
selection is still above five sigma under placeholder assumptions, but it should
use amplification or extra shots in a real run card.

## Boundary

This accounts for abstract LCU success only.  It does not include hardware-specific
ancilla loss, imperfect controlled-select operations, or phase error in any
amplification layer.

## Files

- `analysis/bt1689_ancilla_success_accounting.py`
