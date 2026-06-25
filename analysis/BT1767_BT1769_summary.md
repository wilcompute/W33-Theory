# BT1767-BT1769 summary

Executed all three requested next moves after BT1764-BT1766.

## BT1767: BC-ring adjacency model

Added `analysis/bt1767_bc_ring_adjacency_model.py`.

The 30 selector completions now have an explicit graph model:

```text
30 vertices
3 decagon strands
10 triangular cross-sections
60 edges
degree 4 at every vertex
```

Construction: choose a Hamilton decagon through the 10 zero-pair classes, then put three residual states above each zero-pair. Each residual layer is a 10-cycle; the three residual states above each zero-pair form a triangle. This upgrades BT1764 from count resonance to a concrete BC-ring-like adjacency model. Boundary: still not a 600-cell coordinate embedding.

## BT1768: noncentral hexagon action search

Added `analysis/bt1768_noncentral_hexagon_action_search.py`.

A bounded conjugation search in the implemented E8 simple-reflection model checked Coxeter conjugates through reflection-word depth 12:

```text
distinct conjugates visited: 65,356
candidate exponents: [1,7,11,13,17,19,23,29]
found exponents: [1]
not found: [7,11,13,17,19,23,29]
```

Boundary: bounded search only. It does not prove noncentral normalizer elements do not exist.

## BT1769: orientation candidate admissibility

Added `analysis/bt1769_orientation_candidate_admissibility.py`.

The 12 BT1766 orientation candidates were tested at canonical smallest-automorphism representatives. All 12 canonical representatives contain 6-cycles. The known incumbent orientation remains admissible only at the noncanonical BT1738 stabilizer choices with score `(44,73,9)`.

Conclusion: graph admissibility does not collapse the orientation fiber by orientation alone; stabilizer choices inside each target-line/orientation fiber are essential.
