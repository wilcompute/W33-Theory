# BT771 — Null 15-Sector Kernel Certificate

Status: all checks pass.

The verifier is `analysis/bt771_null_15_sector_kernel.py`.

Core identity:

\[
H_{15}=8I-4A_{W33}+J.
\]

Entry law:

- diagonal: 9
- W33 adjacent pair: -3
- W33 nonadjacent pair: 1

Projector law:

\[
H_{15}^2=24H_{15}.
\]

Spectrum:

\[
\operatorname{spec}(H_{15})=24^{15}\oplus0^{25}.
\]

Octet matrix condition:

\[
H_{15}M_{\mathrm{octet}}=0,
\qquad
M_{\mathrm{octet}}^TH_{15}=0.
\]

Tight-frame interpretation:

\[
G_{15}=H_{15}/9
\]

is the Gram matrix of 40 unit vectors in a 15-dimensional sector.  The frame
bound is

\[
40/15=8/3.
\]

Inner products:

\[
1,\quad -1/3,\quad 1/9.
\]

Boundary: this identifies the 15-sector as a W33 point-space tight frame and
octet-sum null kernel. It does not yet add PG(3,2) labels to the 15 basis
directions.
