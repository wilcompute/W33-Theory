# BT1671 — Automorphism-Twirl Bridge Theorem

## Purpose

BT1668 twirled the bridge over root gauges. BT1671 replaces that with a true
symmetry action: the projective symplectic action on \(W(3,3)\).

## Group action

The script generates the projective symplectic action from symplectic
transvections over \(\mathbb F_3\). The projective action has order

\[
25920.
\]

The full symplectic group has order

\[
|\mathrm{Sp}(4,3)|=51840,
\]

with the central \(\pm I\) acting trivially on projective points, so the
projective action has half the order.

## Orbit test

The action is transitive on:

\[
40\text{ points},
\qquad
40\text{ lines},
\qquad
160\text{ incidence edges}.
\]

Therefore the automorphism orbit of one incidence edge has size

\[
\boxed{160.}
\]

## Twirl conclusion

The automorphism twirl of any edge-supported bridge is uniform over all W33 Levi
incidence edges.

For the BT1662 eight-cycle selector, each gauge has

\[
8\text{ cycles}\times8\text{ edges}=64
\]

edge-incidence events. The automorphism-twirled mean edge weight is therefore

\[
\boxed{64/160=0.4.}
\]

## Interpretation

The full symmetry twirl does not recover a sparse canonical \(8\)-cycle support.
It collapses the bridge to the uniform incidence-edge idempotent. This supports
the BT1665/BT1668 conclusion: the bridge is useful only after a gauge choice;
without that choice the natural object is global.

## Boundary

The test uses the projective symplectic action. Dualities swapping points and
lines are not required for the incidence-edge transitivity result.

## Files

- `analysis/bt1671_automorphism_twirl_bridge.py`
- `data/PART_BT1671_AUTOMORPHISM_TWIRL_BRIDGE_results.json`
