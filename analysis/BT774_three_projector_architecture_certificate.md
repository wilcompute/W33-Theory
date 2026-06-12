# BT774 — Three-Projector Architecture Certificate

Status: verifier added.

Verifier: `analysis/bt774_three_projector_architecture.py`.

## Point space

The W33 point space splits as

\[
40=(1+24)+15.
\]

The octet carrier is the image of the point/octet incidence matrix:

\[
M_{\rm octet}M_{\rm octet}^{T}.
\]

Its spectrum is

\[
72^1\oplus12^{24}\oplus0^{15}.
\]

The null 15-sector is

\[
H_{15}=8I-4A_{W33}+J,
\]

with spectrum

\[
24^{15}\oplus0^{25}.
\]

The two point-space projectors are orthogonal in integer form:

\[
(MM^T)H_{15}=H_{15}(MM^T)=0.
\]

## Chart space

The 240 centered local K3,3 charts form a 27-regular chart graph with spectrum

\[
27^1\oplus9^{24}\oplus3^{75}\oplus(-1)^{81}\oplus(-3)^{24}\oplus(-9)^{35}.
\]

The 81-memory sector is the \(-1\)-eigenspace.  The verifier constructs the
integer spectral numerator

\[
L_{81}=\prod_{\lambda\ne -1}(B_{\rm chart}-\lambda I)
\]

and checks

\[
\operatorname{rank}(L_{81})=81,
\qquad
L_{81}^2=-17920L_{81}.
\]

## Packet/chart separation

Let \(N\) be the chart/packet incidence matrix from BT773.  It has 2160 ones.
The key separation law is

\[
L_{81}N=0.
\]

Interpretation:

- point octet carrier: \(1+24\)
- point null companion: \(15\)
- chart memory carrier: \(81\)
- packet/chart routing does not excite the chart-memory \(81\)-sector

Boundary: this is the integrated linear-algebra architecture. It does not yet
construct the full 51840 root-torsor table.
