# BT781 — H15 Frame Action Certificate

Verifier added: `analysis/bt781_h15_frame_action.py`.

The verifier constructs the generated matrix action from the 40 W33 point
transvections and checks its action on the H15 Gram frame.

Core facts checked:

- generated matrix order: 51840
- projective permutation order on the 40 W33 frame vectors: 25920
- central kernel size: 2
- H15 spectrum: 24^15 plus 0^25
- every generated projective permutation preserves the H15 Gram matrix

Interpretation:

The normalized H15 frame has a verified generated PSp(4,3) frame action of
order 25920. Since the H15 Gram entries distinguish W33 adjacency from
non-adjacency, any full frame-set automorphism must preserve the W33 point
Graph.

Boundary: this verifies the generated PSp(4,3) action. It does not independently
enumerate every graph automorphism.
