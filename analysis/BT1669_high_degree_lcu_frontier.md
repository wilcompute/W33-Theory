# BT1669 — High-Degree LCU Tradeoff Frontier

## Purpose

BT1666 optimized the projector implementation under a minimal-degree constraint.
BT1669 relaxes that constraint and asks how the LCU coefficient mass changes if
higher graph-walk powers are allowed.

## Method

For each target projector, solve the linear program:

\[
\min \sum_i |c_i|
\]

subject to exact interpolation on the graph spectrum:

\[
p(\lambda_j)=\delta_{j,t}.
\]

Clock degrees are swept from 3 to 9. Matter degrees are swept from 2 to 8.

## Baseline

The BT1666 minimal-depth point is

\[
(d_c,d_m)=(3,2),
\qquad
\text{max walk depth}=5,
\]

with total two-port mass

\[
\boxed{\|c\|_1=19/48=0.3958333333333333.}
\]

## Frontier

The best point at depth 6 is already

\[
(d_c,d_m)=(3,3),
\qquad
\|c\|_1=0.01379243827160492.
\]

At the largest tested depth,

\[
(d_c,d_m)=(9,8),
\qquad
\text{max walk depth}=17,
\]

with

\[
\boxed{\|c\|_1=2.0822330410596202\times10^{-10}.}
\]

Using the BT1664 placeholder per-walk survival discount, this point has adjusted
mass

\[
2.3861869114584497\times10^{-10}.
\]

## Interpretation

The algebraic coefficient mass falls rapidly with degree, especially on the
matter side because the matter eigenvalues are 24 and 30. This means minimal walk
depth is not automatically coefficient-optimal.

## Boundary

This is an algebraic LCU frontier. A physical optimizer must add:

- block-encoding normalization;
- phase precision;
- calibration drift;
- component-specific depth loss;
- finite dynamic-range constraints.

So BT1669 does not replace BT1666. It marks the next hardware-optimization axis.

## Files

- `analysis/bt1669_high_degree_lcu_frontier.py`
- `data/PART_BT1669_HIGH_DEGREE_LCU_FRONTIER_results.json`
