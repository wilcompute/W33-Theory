# BT1691 — Run-Card Simulator v3

## Rule

A run card passes if the effective SNR is at least five after component loss,
phase jitter, parity/sign flips, and LCU postselection.

## Separate-port run card

For the resonance port,

\[
P_{c,6}\otimes P_{m,24},
\]

the parameters are

\[
\lambda=1.2939453125,
\qquad
p_{\rm LCU}=0.597413338718975,
\qquad
\text{depth}=7.
\]

The effective SNR at 2048 bins is

\[
28.625716516580017.
\]

The number of bins needed for five sigma is

\[
62.48233180211645.
\]

The parity/sign-flip threshold for five sigma is

\[
0.41919644057439054.
\]

For the companion port,

\[
P_{c,0}\otimes P_{m,30},
\]

the parameters are

\[
\lambda=1.25,
\qquad
p_{\rm LCU}=0.64,
\qquad
\text{depth}=5.
\]

The effective SNR at 2048 bins is

\[
29.865313063424016.
\]

The number of bins needed for five sigma is

\[
57.40316226486634.
\]

The parity/sign-flip threshold for five sigma is

\[
0.42255434221095167.
\]

## Monolithic two-port run card

For one combined two-port LCU,

\[
\lambda=2.5439453125,
\qquad
p_{\rm LCU}=0.1544685004281349,
\qquad
\text{depth}=7.
\]

The effective SNR at 2048 bins is

\[
14.557904134592752.
\]

The number of bins needed for five sigma is

\[
241.58627116866884.
\]

The parity/sign-flip threshold for five sigma is

\[
0.34109118674204353.
\]

## Recommendation

Run the resonance and companion as separate postselected ports.  Both separate
ports clear five sigma with fewer than 64 effective bins under the current
placeholder model.  The monolithic two-port LCU still passes at 2048 bins, but it
has much less parity/sign-flip margin.

## Boundary

Component values remain placeholders.  LCU success is abstract and does not yet
include imperfect controlled-select operations or measured ancilla loss.

## Files

- `analysis/bt1691_run_card_simulator_v3.py`
