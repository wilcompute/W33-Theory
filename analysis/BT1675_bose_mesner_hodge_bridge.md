# BT1675 — Bose–Mesner/Hodge Bridge Idempotent Test

## Purpose

BT1671 proved that the automorphism twirl of an incidence-edge-supported bridge is
uniform over the 160 W33 Levi incidence edges. BT1675 connects that uniform twirl
to the Levi Hodge decomposition.

## Levi chain complex

For the W33 Levi graph,

\[
|V|=80,
\qquad
|E|=160,
\qquad
\operatorname{rank}D=79.
\]

Thus

\[
\boxed{\beta_1=160-79=81.}
\]

The cycle-space Hodge projector has trace

\[
\operatorname{tr}P_{H_1}=80.99999999999997,
\]

and idempotence residual

\[
2.5848363704990327\times10^{-14}.
\]

## Uniform incidence-edge idempotent

The automorphism-twirled bridge edge idempotent is

\[
E_{\rm unif}=\frac{\mathbf 1_E\mathbf 1_E^T}{160}.
\]

It has rank

\[
\boxed{1}
\]

and idempotence residual zero.

For a BT1671 eight-cycle selector with 64 edge events, the mean edge weight is

\[
64/160=0.4.
\]

## Hodge overlap

Let \(u=\mathbf1_E\).  The cycle projection is numerically zero:

\[
\|P_{H_1}u\|=2.3633435577592544\times10^{-14}.
\]

The normalized Hodge overlap is

\[
\frac{u^TP_{H_1}u}{u^Tu}
=-6.817896941457846\times10^{-16}.
\]

Thus

\[
\boxed{P_{H_1}E_{\rm unif}\simeq0.}
\]

## Interpretation

With the standard point-to-line orientation, the uniform incidence-edge vector has
boundary value

\[
-4
\]

on every point vertex and

\[
+4
\]

on every line vertex. It is therefore a bipartite cut/gradient mode, not a cycle.

So the fully twirled bridge has no protected Levi \(H_1\) content. Gauge fixing is
not just a nuisance; it is necessary to retain a homological clock-to-Levi bridge.

## Boundary

This identifies the uniform incidence-edge twirl and its Hodge overlap. It does
not classify all higher edge-pair Bose--Mesner idempotents.

## Files

- `analysis/bt1675_bose_mesner_hodge_bridge.py`
- `data/PART_BT1675_BOSE_MESNER_HODGE_BRIDGE_results.json`
