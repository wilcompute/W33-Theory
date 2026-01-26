# Transport edge elements: projective action vs D6

- (0 1 2): auto_id=, order=, delta=
- (0 2 1): auto_id=, order=, delta=
- e: auto_id=0, order=1, delta=0
- e*: auto_id=0, order=1, delta=0

Notes:
- e and e* map to the identity permutation on projective classes.
- (0 1 2) and (0 2 1) do not match any D6 auto_id on the m0 quartet; they shift m0->m1/m2 and permute sectors (1->3->2) while fixing sector 0, which is outside the D6 incidence action.
- Applying these projective actions to hyperplane quartets maps 0/27 back into the hyperplane (see `transport_edge_elem_hyperplane_embedding_details_summary.md`).
