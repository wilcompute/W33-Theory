# BT772 — PG(3,2)-Labeled 15-Sector Certificate

Status: verifier added.

Verifier: `analysis/bt772_pg32_labeled_15_sector.py`.

Core construction:

1. Build W(3,3) from the finite symplectic model.
2. Build the null 15-sector matrix

\[
H_{15}=8I-4A_{W33}+J.
\]

3. Reduce each W33 point coordinatewise modulo 2:

\[
\mathbb F_3^4 \longrightarrow \mathbb F_2^4.
\]

4. Use the 15 nonzero binary vectors as PG(3,2) labels.
5. Choose one W33 representative over each PG(3,2) point such that the selected
   15 columns of \(H_{15}\) have full rank.

Verified claims:

- PG(3,2) has 15 points.
- PG(3,2) has 35 lines.
- Every PG(3,2) line has 3 points.
- Every PG(3,2) point lies on 7 lines.
- Every pair of PG(3,2) points lies on exactly one line.
- The mod-2 reduction hits all 15 PG labels.
- The selected 15 columns of \(H_{15}\) have rank 15.
- The selected columns lie in the \(H_{15}\) image with eigenvalue 24.
- The selected columns are null against the octet matrix:

\[
M_{\rm octet}^{T}C=0.
\]

Boundary: this is a canonical PG(3,2)-labeled coordinate frame for the 15-sector. Full group-action equivariance is still a separate target.
