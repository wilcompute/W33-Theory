# BT775 — PG(3,2) Equivariance Obstruction Certificate

Status: verifier added.

Verifier: `analysis/bt775_pg32_equivariance_obstruction.py`.

Question:

\[
\text{Do the BT772 mod-2 PG(3,2) labels define a full }Sp(4,3)\text{-equivariant quotient?}
\]

Answer:

\[
\boxed{\text{No.}}
\]

A single symplectic transvection already breaks the label map.

The counterexample transvection is along the W33 projective vector

\[
(0,0,0,1).
\]

Its matrix over \(\mathbb F_3\) is

\[
\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&1&0\\
0&1&0&1
\end{pmatrix}.
\]

The verifier checks:

- identity preserves the PG labels
- the counterexample matrix is symplectic
- the counterexample permutes the 40 W33 projective points
- the counterexample fails mod-2 label equivariance

Interpretation:

The PG(3,2) labels from BT772 are a useful coordinate gauge for the 15-sector,
not a full W33 automorphism quotient. The obstruction is structural and should
be tracked rather than hidden.

Boundary: this falsifies full \(Sp(4,3)\)-equivariance only. It does not yet
classify the subgroup preserving the PG labels.
