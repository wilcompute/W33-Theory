# BT1666 — Projector LCU Cost Optimizer

## Scope

BT1666 optimizes the BT1661 projectors under the exact minimal-degree constraint:
no higher walk powers are introduced.

## Individual LCU masses

\[
\|P_{c,6}\|_1=\frac13,
\qquad
\|P_{c,0}\|_1=\frac73,
\]

\[
\|P_{m,24}\|_1=\frac{31}{144},
\qquad
\|P_{m,30}\|_1=\frac{5}{36}.
\]

## Tensor selector costs

For the resonance selector,

\[
P_{\rm res}=P_{c,6}\otimes P_{m,24},
\]

we get

\[
\|P_{\rm res}\|_1=\frac13\cdot\frac{31}{144}=\frac{31}{432}.
\]

It has 6 tensor terms and maximum walk depth 5.

For the companion selector,

\[
P_{\rm comp}=P_{c,0}\otimes P_{m,30},
\]

we get

\[
\|P_{\rm comp}\|_1=\frac73\cdot\frac5{36}=\frac{35}{108}.
\]

It has 8 tensor terms and maximum walk depth 5.

The combined two-port LCU mass is

\[
\boxed{
\frac{31}{432}+\frac{35}{108}=\frac{19}{48}.
}
\]

## Hardware depth

Both selectors have maximum walk depth

\[
\boxed{5}.
\]

Inside the 2048-bin envelope, the depth margin is

\[
2048-5=2043.
\]

## Decision

Under the pass-minimal exact-projector constraint, the BT1661 polynomials are the
right compiler target. The dominant coefficient cost is the companion selector,
because \(P_{c,0}\) carries the identity branch and has \(\ell_1\) mass \(7/3\).

## Boundary

Higher-degree polynomial identities can reduce coefficient mass, but they consume
more walk depth. That tradeoff only becomes meaningful after inserting calibrated
loss-per-pass hardware data.

## Files

- `analysis/bt1666_projector_lcu_cost_optimizer.py`
- `data/PART_BT1666_PROJECTOR_LCU_COST_OPTIMIZER_results.json`
