# BT778 — PG(3,2)-Label Stabilizer Classification Certificate

Status: verifier added.

Verifier: `analysis/bt778_pg32_label_stabilizer.py`.

BT775 showed that the BT772 PG(3,2) coordinate labels are not equivariant for
the full W33 automorphism group. BT778 classifies the exact stabilizer of that
label partition inside the generated matrix group \(Sp(4,3)\).

Construction:

- Generate \(Sp(4,3)\) from the 40 symplectic transvections, one per W33
  projective point.
- Confirm generated order \(51840\).
- For every generated matrix, test whether the coordinatewise mod-2 PG labels
  are preserved as a partition.

Result:

\[
\operatorname{Stab}_{Sp(4,3)}(\text{PG-label partition})=\{+I,-I\}.
\]

Therefore the projective stabilizer is trivial:

\[
\operatorname{PStab}=1.
\]

Interpretation:

The PG(3,2) labels are a rigid coordinate gauge for the 15-sector, not a hidden
quotient symmetry. The obstruction found in BT775 is maximal: aside from the
central sign, no nontrivial matrix in \(Sp(4,3)\) preserves the label partition.

Boundary: this classifies the stabilizer of the BT772 coordinate-label
partition. It does not classify unrelated real-frame automorphisms of the
15-dimensional Gram representation.
