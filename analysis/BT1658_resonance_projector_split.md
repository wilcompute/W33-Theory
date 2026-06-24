# BT1658 — Resonance Projector Split Theorem

## Problem

BT1655 found that the coupled clock--matter eigenvalue

\[
30
\]

is degenerate:

\[
6^8_{\rm clock}\otimes24^{15}_{\rm matter}\mapsto30^{120},
\]

but also

\[
0^1_{\rm clock}\otimes30^{24}_{\rm matter}\mapsto30^{24}.
\]

So the full coupled 30-eigenspace has rank

\[
144=120+24.
\]

BT1658 asks whether a natural graph operator separates these two pieces.

## Projectors

Let \(L_c\) be the Heawood flag-clock Laplacian.  Its spectrum is

\[
0^1\oplus(3-\sqrt2)^6\oplus(3+\sqrt2)^6\oplus6^8.
\]

The endpoint and ground projectors are polynomial projectors:

\[
P_{c,0}
=
-\frac{(L_c-6I)((L_c-3I)^2-2I)}{42},
\]

\[
P_{c,6}
=
\frac{L_c((L_c-3I)^2-2I)}{42}.
\]

Let \(L_m\) be the matter-graph Laplacian with spectrum

\[
0^1\oplus24^{15}\oplus30^{24}.
\]

Then

\[
P_{m,24}
=
\frac{L_m(L_m-30I)}{24(24-30)},
\]

and

\[
P_{m,30}
=
\frac{L_m(L_m-24I)}{30(30-24)}.
\]

The verifier checks idempotence, orthogonality, and the correct ranks:

\[
\operatorname{rank}P_{c,0}=1,
\qquad
\operatorname{rank}P_{c,6}=8,
\]

\[
\operatorname{rank}P_{m,24}=15,
\qquad
\operatorname{rank}P_{m,30}=24.
\]

## Split of the degenerate 30-sector

The resonance block is

\[
\boxed{
P_{\rm res}=P_{c,6}\otimes P_{m,24}
}
\]

with

\[
\operatorname{rank}P_{\rm res}=8\cdot15=120.
\]

The companion block is

\[
\boxed{
P_{\rm comp}=P_{c,0}\otimes P_{m,30}
}
\]

with

\[
\operatorname{rank}P_{\rm comp}=1\cdot24=24.
\]

Thus

\[
\boxed{
P_{30}=P_{\rm res}+P_{\rm comp},
\qquad
\operatorname{rank}P_{30}=144.
}
\]

## Natural separator

The partial clock Laplacian

\[
K_c=L_c\otimes I_m
\]

separates the degeneracy:

\[
K_cP_{\rm res}=6P_{\rm res},
\]

but

\[
K_cP_{\rm comp}=0.
\]

Therefore, on the coupled 30-eigenspace,

\[
\boxed{
\frac{K_c}{6}
}
\]

is the resonance selector.

## Boundary

The split is projector-natural and graph-operator-natural.  It is not a coordinate basis selector and does not by itself choose vectors inside the rank-120 resonance block.

## Files

- `analysis/bt1658_resonance_projector_split.py`
- `data/PART_BT1658_RESONANCE_PROJECTOR_SPLIT_results.json`
