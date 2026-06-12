# BT784 — PG Gauge / H15 Action Bridge Certificate

Status: bridge certificate added; full verifier upload was blocked by the connector.

Goal:

Compare the BT772 PG-labeled H15 basis with the generated PSp(4,3) H15 frame
action from BT781.

Resulting interpretation:

- BT772 gives a rigid PG(3,2)-labeled coordinate gauge for the 15-sector.
- BT778 proves that this PG label partition has only the central matrix
  stabilizer inside Sp(4,3), projectively trivial.
- BT781 proves that the H15 Gram frame still carries the generated projective
  PSp(4,3) action of order 25920.

Therefore the large projective action does not preserve the PG labels. It moves
between PG gauges of the same H15 frame. The intended bridge object is the
basis-change matrix from a fixed PG gauge to its image under each generated W33
motion.

Boundary:

A compact exact verifier for these basis-change matrices was prepared, but the
connector blocked the code upload. The mathematical target remains clear: for a
PG-gauge basis C and a generated frame action P, compute X from C X = P C and
verify X preserves C^T C while not being a PG-label permutation in general.
