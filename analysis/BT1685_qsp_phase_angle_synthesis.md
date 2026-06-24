# BT1685 — QSP Phase-Angle Synthesis Status

## Purpose

BT1685 attempts to move from scalar bounded polynomials to QSP/QSVT phase
schedules.  A direct nonlinear fit for collapsed single-sequence phase angles was
not reliable enough to certify.  Therefore BT1685 records the exact part that is
certifiable now: Chebyshev-term QSP schedules plus LCU/ancilla routing.

## Chebyshev term library

In the standard walk convention, a Chebyshev term \(T_k(x)\) is implemented by
\(k\) zero-phase signal-walk steps.  Thus the phase library is:

\[
T_0: [],
\qquad
T_1: [0],
\qquad
T_2: [0,0],
\qquad
T_3: [0,0,0],
\qquad
T_4: [0,0,0,0].
\]

## Component schedules

The bounded components are implemented as LCUs over these term schedules:

\[
e_c=\frac{5}{28}T_0+\frac{9}{28}T_2,
\qquad
\|e_c\|_{1}=0.5.
\]

\[
o_c=\frac{19}{56}T_1+\frac{9}{56}T_3,
\qquad
\|o_c\|_{1}=0.5.
\]

\[
e_{30}=-\frac18T_0+\frac58T_2,
\qquad
\|e_{30}\|_1=0.75.
\]

\[
o_{30}=\frac12T_1,
\qquad
\|o_{30}\|_1=0.5.
\]

\[
p_{24}=\frac{1325}{2048}T_0-\frac{175}{512}T_2-\frac{625}{2048}T_4,
\qquad
\|p_{24}\|_1=1.2939453125.
\]

## Selector routing

The endpoint selectors are routed as

\[
P_{c,6}=\operatorname{LCU}(e_c)+\operatorname{LCU}(o_c),
\]

\[
P_{c,0}=\operatorname{LCU}(e_c)-\operatorname{LCU}(o_c),
\]

and

\[
P_{m,30}=\operatorname{LCU}(e_{30})+\operatorname{LCU}(o_{30}).
\]

The matter-24 selector uses the single even LCU \(p_{24}\).

## Resource result

The two-port resources are

\[
\|P_{c,6}\otimes P_{m,24}\|_1=1.2939453125,
\]

\[
\|P_{c,0}\otimes P_{m,30}\|_1=1.25,
\]

and therefore

\[
\boxed{\|c\|_{1,\rm combined}=2.5439453125.}
\]

The maximum clock term depth is 3, the maximum matter term depth is 4, and the
maximum tensor term depth is 7.

## Boundary

The listed phases are exact for Chebyshev terms.  BT1685 does not claim a
collapsed single-sequence QSP phase list for each whole polynomial.  It gives a
certified LCU-of-QSP-terms implementation.

## Files

- `analysis/bt1685_qsp_phase_angle_synthesis.py`
- `data/PART_BT1685_QSP_PHASE_ANGLE_SYNTHESIS_results.json`
