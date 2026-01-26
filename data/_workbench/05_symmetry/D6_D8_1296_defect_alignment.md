# D6/D8/1296 alignment vs defect cocycle

Inputs:
- data/_toe/take_it_all_way_20260110/generators_on_27.txt
- data/_toe/take_it_all_way_20260110/hyperplane27_phasefunctions.csv
- data/_is/incidence_autgroup_20260110/automorphism_group_order12_point_maps.csv
- data/_toe/coupling_20260110/orbit0_edges_with_projective_images.csv

1296-closure on hyperplane 27 (D8 lifts + full D6 incidence action):
- D6_group_size: 12
- D8_group_size: 8
- combined_group_size: 1296
- orbit_size (any point): 27
- point_stabilizer_size (idx 0): 48
- tomotope15_set_stabilizer_size: 12
- m0=2_9block_stabilizer_size: 108
- m0_partition_stabilizer_size (preserve all three m0 blocks): 54

D6 action on the m0 quartet (sec0_m0 sec1_m0 sec2_m0 sec3_m0):
- setwise_stabilizer_auto_ids: [0]
- pointwise_stabilizer_auto_ids: [0]

Defect edges vs projective image:
- defect_edge_count (delta_sum_mod8==4): 4
- defect_projective_image ('sec0_m0', 'sec1_m0', 'sec2_m0', 'sec3_m0'): total_edges_with_image=67, defect_edges_with_image=4
- defect_quartet_in_hyperplane27: False

Notes:
- The generators in `generators_on_27.txt` alone produce a 648-element subgroup; adding the affine involution a -> -a + (0,0,0,2) yields the full 1296 closure (see `hyperplane1296_affine_involution_summary.md`).
- The full 1296 group contains the entire 27-element translation subgroup of the hyperplane (t0−t1−t2+t3=0), with stabilizer size 48 (see `hyperplane_translation_subgroup_summary.md`).
- The stabilizer order distribution matches S4×Z2 (see `hyperplane_translation_stabilizer_structure.md`).
- So the 1296 closure has the structure 3^3 ⋊ (S4×Z2) with a regular translation subgroup (see `hyperplane_translation_subgroup_summary.md`).
- The stabilizer’s S4 action is explicit on four translation‑vector pairs (see `hyperplane_translation_stabilizer_pair_vectors.md`).
- Only one of the four S4 vertex translations (t=(0,1,1,2)) preserves the tomotope15 set; the others map most lines out (see `hyperplane_translation_pair_tomotope_overlap.md`).
- In the stabilizer, only identity and sec1↔sec2 act as pure sector permutations (see `hyperplane_stabilizer_sector_permutations_summary.md`).
- Even allowing per‑sector shifts, only those two elements act as sector‑wise affine maps (see `hyperplane_stabilizer_sector_affine_actions_summary.md`).
- The D6 incidence action on the hyperplane includes a Z3 translation cycle (t=(0,1,1,2)) and its inverse (see `hyperplane_translation_d6_overlap.md`).
- The determinant character on a-space splits the full 1296 group into 648+648, but the base 648 subgroup already contains both det values (so it is not the det=1 subgroup). See `hyperplane1296_det_character_summary.md`.
- Transport 3-cycles (0 1 2) and (0 2 1) act nontrivially on projective classes but map 0/27 hyperplane quartets back into the hyperplane, so they lie outside the hyperplane closure (see `transport_edge_elem_hyperplane_embedding_summary.md`).
- The transport 3-cycles are affine on a with v·c=1 or 2, so they shift the hyperplane level set; adding this shift extends the closure to size 3888 and makes the action transitive on Z3^4 (see `transport_edge_elem_affine_m_a_summary.md` and `hyperplane_transport_closure_summary.md`).
- On orbit0 edges, sigma_product is +1 exactly when the projective image has sum_m_mod3=0 (hyperplane level preserved), and -1 when sum_m_mod3 is 1 or 2 (shifted); see `transport_edge_z2_vs_hyperplane_levels_summary.md`.
- Brute-force enumeration confirms the 1296/3888 orbit sizes on Z3^4 and the transport-aware stabilizer counts; see `hyperplane_transport_closure_bruteforce_summary.md` and `transport_aware_stabilizer_summary.md`.
- The D6 action on a-coordinates is purely linear (no translation), fixes the hyperplane normal, and has det=1 for delta=0 and det=2 for delta=1 (see `D6_action_affine_a_summary.md`).
- The 1296 closure is transitive on the 27 hyperplane points; the 108-element subgroup preserves the m0=2 nine-block.
- Defect edges are projectively trivial and share the m0-quadruple image; that quartet is not on the hyperplane (sum mod 3 = 0), so the hyperplane action does not directly act on defect support.
- Without an explicit map from hyperplane generators to orbit-0 vertex/edge permutations, the defect cocycle can only be aligned indirectly via these projective-image constraints.
