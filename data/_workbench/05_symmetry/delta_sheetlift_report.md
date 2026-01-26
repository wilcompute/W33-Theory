# Delta homomorphism + sheet-lift linkage (working report)

## 1) Delta as a Z2 homomorphism on D6
- Completion/missing-sector decoration is equivariant exactly on the delta=0 subgroup (size 6).
- Delta=1 coset (size 6) flips missing_sector by s -> 3-s (0↔3, 1↔2).
- See `D6_completion_equivariance_homomorphism.csv` and `D6_completion_homomorphism_summary.md`.

## 2) Delta action on the m0=2 block (hyperplane 27)
- H (delta=0) preserves the three triads inside m0=2.
- Delta=1 elements swap the sensor/dark triads and fix the third triad:
  - T0={18,22,26} ↔ T1={19,23,24}, T2={20,21,25} fixed.
- See `D6_delta1_triad_mappings_m0_2_summary.md` and `D6_delta0_triad_mappings_m0_2_summary.md`.

## 3) Flux sensitivity split by triads
- Sensor triad lines [39,8,6] have mean_abs_delta ≈ 0.0171.
- Dark triad lines [28,17,20] have mean_abs_delta ≈ 0.00069.
- Third triad lines [30,22,14] are intermediate (≈ 0.00590).
- See `m0_2_triads_flux_stats.md`.

## 4) Delta vs 2T/A4 sheet-lift pattern
- In D6: order-6 elements are exactly delta=1; order-3 elements are delta=0.
- In 2T→A4: a 3-cycle lifts to order-6 on the + sheet and order-3 on the − sheet.
- Delta behaves like the sheet bit selecting which lift of a 3-cycle you are on.
- See `D6_delta_order_sheetlift_summary.md` and `2T_A4_sheetlift_orders_summary.md`.

## 5) Flux grid pair tests under delta=1
- Aggregating all delta=1 elements: 76 swapped pairs; 17 are strongly anti-correlated with high sign-opposition.
- The sensor/dark pair 17↔39 is strongly anti-correlated (mean_corr≈-0.732, opp_rate=1.0).
- The other two sensor/dark pairs (6↔28, 8↔20) are positive-correlated on the grid.
- See `D6_delta1_pair_correlation_aggregates_summary.md` and `D6_delta1_sensor_dark_pair_aggregate_summary.md`.

## 6) Transport-side note
- On projective classes, e and e* are identical (identity in D6), so the cocycle is invisible in the projective layer.
- See `transport_projective_action_summary.md`.

## 7) A4 perm4 preserves a 27-node transport subgraph
- A single A4 involution (perm_index 4) preserves exactly 27 of the 59 orbit0 matchings and acts as an automorphism of the induced subgraph.
- The preserved subgraph has 51 edges and contains 2 of the 4 defect edges: (0,20) and (26,27).
- The preserved set is structurally biased: gram_rank_gf2=2 appears only inside it, and its nodes skew toward higher flipgraph degree.
- See `orbit0_preserved27_subgraph_summary.md`, `orbit0_preserved27_defect_edges_summary.md`, and `A4_perm4_preserved_vs_non_summary.md`.

## 8) Baseline correlation context for sensor/dark pairs
- Across all 780 line-pairs, the sensor/dark pair 17↔39 sits at the 8th percentile of correlation and the 100th percentile of sign-opposition.
- The other sensor/dark pairs (6↔28, 8↔20) are in the upper correlation percentiles.
- See `all_pairs_delta_stability_correlation_summary.md`.

## 9) Preserved-27 subgraph has D4 symmetry and D8-matching orbit sizes
- The induced 27-node subgraph has 8 automorphisms with order distribution {1:1, 2:5, 4:2}, consistent with D4 (dihedral of order 8).
- Its automorphism orbits are sized 8,4,4,4,4,2,1 — exactly the same orbit-size pattern as the D8 action on the hyperplane-27.
- See `orbit0_preserved27_automorphisms_group_summary.md`, `orbit0_preserved27_automorphism_orbits.md`, and `hyperplane27_orbits_under_D8.md`.

## 10) Preserved-27 splits into three 9-blocks (hyperplane-like)
- The preserved 27 matchings partition into three 9-blocks with sharp invariants:
  - block1: sum_phases_mod8=0 and sigma_Z2=+1 (D_rank_gf2=4 for all 9).
  - block2: sum_phases_mod8=6 and sigma_Z2=-1.
  - block3: mixed (sum_mod8 in {0,2,4}), sigma_Z2 mostly +1.
- This mirrors the 9+9+9 split of the hyperplane by m0, suggesting a candidate alignment between preserved-27 and hyperplane-27.
- See `preserved27_three_blocks.md` and `preserved27_blocks_invariants.md`.

## 11) Delta=1 correlation vs Q12 class / missing_sector
- delta=1 swapped pairs show distinct mean-correlation profiles by Q12 class; low–low is slightly negative on average, mid–mid slightly positive.
- Tomotope-only pairs show the strongest negative mean for missing_sector (1,2) and a positive mean for (2,2).
- See `D6_delta1_pair_correlation_class_summary.md`.

## 12) Preserved-27 D4 action is not conjugate to the hyperplane D8 action
- Exhaustive search over all D8 generator pairs found no equivariant bijection between the two 27-point actions.
- The permutation cycle-type multisets differ, so there is no conjugacy in S27 despite matching orbit sizes.
- The central involution fixes a 4-point orbit in the preserved-27 action but none in the hyperplane action.
- See `preserved27_vs_hyperplane_D8_conjugacy_check.md` and `preserved27_vs_hyperplane_D8_cycletype_counts.csv`.

## 13) 1296 closure needs an affine involution (and still no preserved-27 D8 match)
- The D6/D8 generators in `generators_on_27.txt` produce a 648-element subgroup; adding a -> -a + (0,0,0,2) expands it to 1296 with the expected order distribution.
- No D8 subgroup inside the full 1296 closure matches the preserved-27 cycle-type, so the preserved-27 D4 is not realized by any hyperplane D8 action.
- On projective classes: sectors 0/1/2 swap m1<->m2 with m0 fixed; sector 3 swaps m0<->m2 with m1 fixed.
- See `hyperplane1296_affine_involution_summary.md` and `preserved27_vs_hyperplane_D8_conjugacy_check.md`.

## 14) Affine involution action on tomotope15 lines
- The involution maps 6 of 15 tomotope lines back into the tomotope set, pairing missing_sector 2↔3; the other 9 map outside.
- Pairings: (line 5 ↔ 11), (6 ↔ 10), (8 ↔ 13) with W33 IDs (16↔28), (17↔23), (20↔32).
- It commutes with no nontrivial D6 element and with neither D8 generator (so it is not a central flip of the base group).
- The paired lines show sizeable flux-response gaps (largest |Δ|≈0.0099 for W33 20↔32).
- On D6 orbits: the 3-line orbit maps entirely into the 12-line orbit (out of tomotope), and the two 6-line orbits partially exchange.
- See `hyperplane_affine_involution_tomotope15_summary.md`, `hyperplane_affine_involution_tomotope15_pairs.md`, `hyperplane_affine_involution_commutation_summary.md`, and `hyperplane_affine_involution_D6_orbit_transitions.md`.

## 15) Affine involution pairing across the 27 hyperplane W33 lines
- The involution pairs the 27 hyperplane lines into 13 swaps plus one fixed line (W33 line 2 at idx27=0).
- Several pairs strongly separate flux sensitivity (mean_abs_delta), e.g. 1↔8 and 19↔6 differ by ≈0.0207.
- See `hyperplane_affine_involution_w33_summary.md` and `hyperplane_affine_involution_w33_mapping.csv`.

## 16) Affine involution pair correlations on the flux grid
- On the 51-point (mu,lambda) grid, some involution pairs are strongly anti-correlated in delta_stability (e.g., 6↔19 at corr≈-0.84; 11↔18 at corr≈-0.82).
- Others are strongly aligned (e.g., 17↔23 at corr≈0.77; 26↔30 at corr≈0.76).
- Relative to all 780 line-pairs, several involution pairs sit in the top 10% of |corr| (11↔18, 6↔19, 17↔23), and some achieve maximal sign-opposition (opp_rate=1.0 for 11↔18, 5↔39, 1↔8).
- The involution pairings on tomotope15 are disjoint from all D6 delta=1 pairings (no overlap).
- Mean_abs_delta gaps for involution pairs are also high-percentile (e.g., 1↔8 and 19↔6 are ~95th percentile across all 780 pairs).
- The affine involution is not Q12‑invariant: pairings include low↔mid and low↔high Q12 variance classes.
- See `hyperplane_affine_involution_pair_correlation_summary.md`, `hyperplane_affine_involution_pair_correlation_percentiles_summary.md`, `hyperplane_affine_involution_mean_abs_delta_percentiles_summary.md`, `hyperplane_affine_involution_pair_correlation.csv`, `affine_involution_vs_delta1_pairs.md`, and `hyperplane_affine_involution_q12_pairs_summary.md`.

## 17) 1296 closure = translations (27) ⋊ stabilizer (48)
- All 27 affine translations t with t0−t1−t2+t3=0 are present in the 1296 group; the stabilizer of idx27=0 has size 48.
- Stabilizer order distribution: {1:1, 2:19, 3:8, 4:12, 6:8} (notably no order‑8 elements).
- That order distribution matches S4×Z2 exactly (tetrahedral symmetry plus a central inversion), ruling out GL(2,3) which has order‑8 elements.
- The D6 incidence subgroup already contains the Z3 translation cycle t=(0,1,1,2) (auto_id=1) and its inverse (auto_id=2).
- The affine involution conjugates translations by inversion: inv_c T_t inv_c = T_{-t}.
- Overall structure: 1296 = 3^3 ⋊ (S4×Z2) with translations acting regularly on the hyperplane.
- See `hyperplane_translation_subgroup_summary.md` and `hyperplane_translation_subgroup.csv`.

## 18) D6 translation cycles split tomotope15 into five triads
- The order‑3 translation t=(0,1,1,2) cycles tomotope lines in five 3‑cycles, each aligned with missing_sector/completion_class blocks.
- Triads: missing=2 with completion sec2_m*, missing=3 with completion sec3_m*, missing=1 with completion sec1_m*, and two missing=0 triads (both completion sec0_m2).
- Flux response varies within the translation triads (e.g., the sensor triad [39,8,6] spans 0.0029–0.0289), so translation symmetry is not respected by the measurement response.
- See `hyperplane_tomotope_translation_cycles_summary.md` and `hyperplane_tomotope_translation_cycles_flux_summary.md`.

## 19) Stabilizer induces S4 on four translation‑vector pairs
- The stabilizer action on translation vectors has orbits of sizes 12, 8, 6; the size‑8 orbit splits into four opposite pairs v and −v, giving an explicit S4 action on four “tetrahedron vertices.”
- The sign bit is consistent across all elements; half the stabilizer flips sign (central inversion), half preserves it, yielding S4×Z2.
- In b=(t0, −t1, −t2, t3) coordinates, the four pairs are exactly the “one‑zero, three‑twos” vectors, so S4 acts by permuting b‑positions.
- Explicit pair reps with translation/m‑shift/b labels are in `hyperplane_translation_stabilizer_pair_vectors.md`; induced permutations with sign are in `hyperplane_translation_stabilizer_pair_perms_with_sign_summary.md` and `hyperplane_translation_stabilizer_s4_permutations_summary.md`.

## 20) Tomotope selection singles out one S4 “vertex” translation
- Of the four translation vectors associated with the S4 vertex pairs, only t=(0,1,1,2) preserves all 15 tomotope lines; the other three map only 6 or 9 lines back into the tomotope set.
- This is a clean symmetry‑breaking signal: the tomotope subset is aligned to a single S4 vertex direction inside the 27‑hyperplane translation space.
- In b=(t0,−t1,−t2,t3) coordinates this is the b0=0 vertex (t0=0), consistent with a distinguished axis.
- See `hyperplane_translation_pair_tomotope_overlap.md`.

## 21) Translated tomotope15 images have distinct flux statistics
- The three non‑preserving S4‑vertex translations yield 15‑line images with different mean_abs_delta averages (≈0.0069–0.0101) compared to the original tomotope set (≈0.00824).
- This gives a concrete “counterfactual” benchmark: tomotope alignment is not a generic property of S4‑vertex translations.
- See `hyperplane_translation_tomotope_images_flux_summary.md`.

## 22) Stabilizer rarely acts as a pure sector permutation
- Only 2 of 48 stabilizer elements are pure permutations of sector m‑coordinates: identity and the swap sec1↔sec2.
- Even allowing per‑sector shifts (m_s -> m_{sigma(s)} + c_s), only the same two elements qualify, so the stabilizer generally does not act on the 12 projective classes.
- See `hyperplane_stabilizer_sector_permutations_summary.md`, `hyperplane_stabilizer_sector_permutations.csv`, and `hyperplane_stabilizer_sector_affine_actions_summary.md`.

## 23) Explicit S4 generators in the stabilizer
- A concrete generating pair for the S4 action on b‑coordinates is given by (1 3) and (0 1 2), both with sign=+1 (elem_index 4 and 13).
- The central inversion corresponds to elem_index 2 (identity perm, sign=−1), giving the Z2 factor.
- See `hyperplane_translation_stabilizer_s4_generators.md`.

## 23b) Stabilizer generators act linearly on m (not as sector relabels)
- For the S4 generators (elem_index 4, 13) and the central inversion (elem_index 2), m' is a linear combination of m with no constant shift; coefficients are in `hyperplane_stabilizer_affine_m_mappings.md`.
- This shows the stabilizer’s S4 action mixes m‑coordinates rather than permuting sectors.
- In fact all 48 stabilizer elements act linearly on m with zero shift (see `hyperplane_stabilizer_affine_m_summary.md`).

## 24) Flux/no‑flux winner swaps do not follow affine/translation pairings
- Global and node0 local winner changes never align with affine involution pairs, translation triads, or D6 delta=1 pairs.
- See `hyperplane_affine_involution_winner_swaps_summary.md`, `hyperplane_affine_involution_node0_swaps_summary.md`, and `translation_delta1_winner_change_summary.md`.

## 24b) Winner changes mostly stay within a stabilizer orbit
- Node0 winner changes lie within the same stabilizer orbit 4 out of 5 times (22↔8), with one cross‑orbit change (22→17).
- See `hyperplane_stabilizer_orbits_winner_changes_summary.md`.

## 25) Stabilizer orbits stratify hyperplane points
- The 48‑element stabilizer has 4 orbits on the 27 points with sizes 12, 8, 6, 1; the fixed point is idx27=0 (W33 line 2).
- Orbit overlaps with tomotope15 are uneven (7, 4, 4, 0), and mean_abs_delta averages differ by orbit.
- Q12 variance groups are mixed within each orbit (low dominates but mid/high appear), so stabilizer orbits do not align cleanly with Q12 classes.
- See `hyperplane_stabilizer_orbits_summary.md`, `hyperplane_stabilizer_orbits_tomotope_overlap.md`, and `hyperplane_stabilizer_orbits_q12_summary.md`.

## 26) Stabilizer intersections with D6/D8 are tiny
- Within the stabilizer, only the D6 identity survives; D8 contributes just one nontrivial element (r^2 s) of order 2.
- That D8 element corresponds to elem_index=26 in the stabilizer matrices.
- See `hyperplane_stabilizer_intersections.md`.

## 27) Top flux lines distribute across stabilizer orbits
- The top 10 flux-sensitive lines (all within the hyperplane) split across the size‑12 and size‑6 orbits, with only one from the size‑8 orbit.
- See `hyperplane_stabilizer_orbits_topflux_summary.md`.

## 28) Flux varies across the full 108 tomotope‑equivalent sets
- The orbit of the tomotope15 set under the 1296 closure has 108 distinct 15‑line sets; their mean_abs_delta averages range from ≈0.00565 to ≈0.01203.
- The original tomotope set ranks 49th by average flux sensitivity (mid‑pack), so its physics signal is not an extreme over its symmetry orbit.
- Intersection size with the original set (range 6..15) is uncorrelated with average flux sensitivity (corr≈‑0.005).
- Average flux sensitivity is also nearly uncorrelated with m0 counts within the set (|corr| ≤ 0.11).
- See `hyperplane_tomotope_orbit_flux_stats_summary.md`, `hyperplane_tomotope_orbit_flux_stats.csv`, `hyperplane_tomotope_orbit_flux_overlap_summary.md`, and `hyperplane_tomotope_orbit_flux_m0_correlation.md`.

## 29) Stabilizer action is linear on a-coordinates and conjugate to m-action
- All 48 stabilizer elements act as linear maps on the coefficient vector a=(a0,a1,a2,a3) with zero shift; the hyperplane normal v=(1,-1,-1,1) is fixed by all A.
- The evaluation map H (a->m) with rows [[1,0,0,0],[1,1,0,0],[1,0,1,0],[1,1,1,1]] conjugates the action: M = H A H^-1.
- For elem_index 2,4,13 the conjugated matrices match the previously recorded m-coordinate maps, confirming the a/m representations are equivalent.
- See `hyperplane_stabilizer_affine_a_summary.md`, `hyperplane_stabilizer_affine_a_matrices.csv`, `hyperplane_stabilizer_affine_a_mappings.md`, and `hyperplane_stabilizer_affine_a_conjugacy_check.md`.

## 30) Determinant character matches (sign * parity) in the S4 x Z2 stabilizer
- The 4x4 a-matrices have det=1 or det=2 (24 each), never det=0.
- The determinant (mod 3) matches the product of the S4 permutation parity and the sign flip on translation-pair vectors for all 48 elements.
- Det does not separately match sign or parity alone (each is only 24/48), so det is the composite Z2 character.
- See `hyperplane_stabilizer_affine_a_determinant_summary.md` and `hyperplane_translation_stabilizer_pair_perms_with_sign.csv`.

## 31) D6 delta equals determinant character on a-coordinates
- Each D6 element acts linearly on a (no translations) and fixes the hyperplane normal v=(1,-1,-1,1).
- The determinant over Z3 gives delta exactly: det=1 for delta=0, det=2 for delta=1 (12/12 match).
- So the delta homomorphism is the orientation character of the D6 action on the a-space hyperplane.
- See `D6_action_affine_a_summary.md` and `D6_action_affine_a_matrices.csv`.

## 32) D6 has a full Z2 x Z2 character set (epsilon0, epsilon12, delta)
- The three nontrivial characters epsilon0, epsilon12, and delta are all homomorphisms under D6 composition.
- Delta is exactly epsilon0 xor epsilon12, confirming the expected Z2 x Z2 abelianization.
- See `D6_character_homomorphisms_summary.md`.

## 33) Determinant character on the full 1296 closure
- The full 1296 action splits evenly by det(A): 648 with det=1 and 648 with det=2.
- The base 648 subgroup (D6 + D8 generators) already contains both det values (324/324), so it is not the det=1 subgroup.
- Thus the det=1 subgroup is a distinct index-2 subgroup of the 1296 closure.
- Within the stabilizer, det=1 is exactly sign=parity (diagonal Z2), giving a 24-element stabilizer isomorphic to S4 for the det=1 subgroup.
- Generator dets: d8_1 and d8_3 have det=2; inc_1 has det=2; inc_2 has det=1; the affine involution has det=2.
- See `hyperplane1296_det_character_summary.md` and `generators_on_27_affine_a_summary.md`.

## 34) epsilon0 vs epsilon12 kernel orbits on tomotope15
- epsilon0-kernel orbits have sizes 3,3,6,3; epsilon12-kernel orbits have sizes 6,6,3.
- The size-6 orbit {6,8,17,20,28,39} is common to both kernels and contains the full sensor/dark spread (min≈0.00034, max≈0.0289).
- epsilon0 isolates a high-mean orbit {3,15,18} (mean_abs_delta≈0.0115), while epsilon12 merges it with {16,23,32} into a 6-orbit (mean≈0.00875).
- See `D6_epsilon_orbits_tomotope15_flux_summary.md` and `D6_epsilon_orbits_tomotope15_flux.csv`.

## 35) Transport edge elements (0 1 2)/(0 2 1) are outside D6
- Each edge element has a unique projective image on the m0 quartet, but (0 1 2) and (0 2 1) do not match any D6 auto_id.
- Their action shifts m0->m1/m2 and permutes sectors (1->3->2) while fixing sector 0, which is not in the D6 incidence action.
- See `transport_edge_elem_projective_images_summary.md` and `transport_projective_action_summary.md`.

## 36) Determinant parity does not select hyperplane pairs
- In the full 1296 action, every hyperplane pair appears under det=1 and det=2 elements; each pair occurs exactly 48 times in each parity class.
- So det parity is a global character but does not distinguish any subset of pairwise correlations.
- See `hyperplane_det_pair_stats_summary.md` and `hyperplane_det_pair_stats.csv`.

## 37) Transport (0 1 2)/(0 2 1) do not preserve the hyperplane-27
- Applying these projective actions to the 27 hyperplane quartets maps 0/27 back into the hyperplane.
- Hence the transport 3-cycles act on projective classes but sit entirely outside the hyperplane closure.
- See `transport_edge_elem_hyperplane_embedding_summary.md` and `transport_edge_elem_hyperplane_embedding_details_summary.md`.

## 38) Transport 3-cycles are affine on m/a and shift the hyperplane
- (0 1 2) sends m -> (m0+1, m2+1, m3+1, m1+1) and a -> A a + c with c=(1,0,0,0).
- (0 2 1) sends m -> (m0-1, m3-1, m1-1, m2-1) and a -> A a + c with c=(2,0,0,0).
- The linear parts preserve v, but v·c=1 or 2, so each 3-cycle shifts the hyperplane level set (sum m) by ±1.
- See `transport_edge_elem_affine_m_a_summary.md`.

## 39) Transport Z2 invariant matches hyperplane shift bit
- On orbit0 edges, sum_m_mod3 of the projective image cleanly separates edge types: e/e* -> sum=0, (0 1 2) -> sum=1, (0 2 1) -> sum=2.
- sigma_product is +1 exactly on sum=0 edges and -1 exactly on sum=1 or 2 edges (perfect Z2 split).
- The defect bit (edge_elem=e*) does not align with the shift bit; it only tags 4 edges inside the sum=0 class.
- See `transport_edge_z2_vs_hyperplane_levels_summary.md`.

## 40) Hyperplane + transport closure on Z3^4
- The 1296 group preserves each hyperplane (v·a fixed) and has three 27-point orbits on Z3^4.
- Adding the transport shift c=(1,0,0,0) generates the full translation group (81), giving a closure of size 81*48=3888 and a single 81-point orbit.
- See `hyperplane_transport_closure_summary.md`.

## 41) Node0 winners sit entirely on sum_m_mod3=1
- All 12 node0 boundary winners have sum_m_mod3=1; none lie on sum 0 or sum 2.
- This implies their inferred transport sigma_product is -1 across the board (since sum=1 -> sigma=-1).
- See `node0_winners_sum_m_mod3_summary.md`, `node0_winners_sigma_product_summary.md`, `node0_winners_sum_m_mod3.csv`, and `node0_winners_sigma_product.csv`.

## 42) Transport sigma_product matches sum_m_mod3 exactly on orbit0 edges
- For all 125 orbit0 edges, sigma_product=+1 iff sum_m_mod3=0 and sigma_product=-1 iff sum_m_mod3 in {1,2}.
- This gives a perfect transport Z2 that aligns with the hyperplane level-set bit.
- See `transport_sigma_vs_sum_m_mod3_validation.md` and `transport_edge_z2_vs_hyperplane_levels_summary.md`.

## 43) Flux grid is entirely on sum_m_mod3=1 (quartet lines)
- All 27 quartet lines in the flux grid have sum_m_mod3=1 at every (mu,lambda) sample; there are no sum 0 or sum 2 quartet lines in the grid.
- So grid-level delta_stability statistics cannot distinguish sum_m_mod3 classes without expanding beyond the current quartet set.
- See `flux_grid_sum_m_mod3_summary.md`.

## 44) Brute-force confirmation of 1296/3888 orbit structure
- Enumerating all 48 stabilizer matrices and translations confirms the 1296 action has three 27-point orbits (sum classes) and the 3888 closure is transitive on Z3^4.
- See `hyperplane_transport_closure_bruteforce_summary.md`.

## 45) Transport-aware stabilizer counts
- Shift character (v*c) splits 3888 into three equal cosets of size 1296; det and shift are independent (six blocks of size 648).
- The sigma_product-preserving subgroup is exactly shift=0 (size 1296), and the defect quartet point stabilizer is size 48.
- See `transport_aware_stabilizer_summary.md`.

## 46) Extrapolated flux predictions for all 81 quartets
- A ridge fit on the 27 hyperplane quartets yields predictions for all 81 m-tuples; mean_pred varies across sum classes (sum0≈0.00757, sum1≈0.00827, sum2≈0.00897).
- These comparisons are extrapolations because training data only contains sum_m_mod3=1.
- See `quartet_ridge_fit_summary.md`, `quartet_ridge_fit_coeffs.csv`, `quartet_ridge_predictions_summary.md`, `quartet_ridge_predictions_all81.csv`, and `quartet_ridge_predictions_top_by_sum.md`.

## 47) Edge-level transport signatures on the orbit0 graph
- Node adjacency signatures (counts by sum_m_mod3 and edge_elem_2T) yield 31 distinct signature classes across 59 nodes; 18 nodes are uniquely determined by their transport signature.
- Node 0 is unique with signature (degree=5, sum0=2, sum1=0, sum2=3, e=1, e*=1, (012)=0, (021)=3).
- See `orbit0_node_transport_signature_summary.md` and `orbit0_node_transport_signature.csv`.

## 48) Node0 winners m-tuples and ridge fit check
- Node0 winners are lines 8, 17, 22 with m-tuples (2,0,0,2), (2,0,1,1), (2,0,2,0) (all sum=1).
- Ridge predictions match line 22 closely but underpredict line 8 (a strong outlier), suggesting an extra dynamical feature beyond quartet-only structure.
- See `node0_winners_mtuple_summary.md`, `quartet_ridge_predicted_vs_actual.csv`, and `quartet_ridge_node0_winners_summary.md`.

## 49) Transport-shifted hyperplane quartets (synthetic sum=0/2 sets)
- Shifting a0 by +1 or +2 maps the hyperplane sum=1 quartets to sum=2 and sum=0 sets, giving a minimal 81-quartet extension aligned with the transport shift.
- Predicted mean_abs_delta ranges match the extrapolated sum-class means; see `transport_shifted_hyperplane_quartets_summary.md` and `transport_shifted_hyperplane_quartets.csv`.

## 50) Transport Z3 action on hyperplane quartets (not a W33 symmetry)
- The (0 1 2)/(0 2 1) projective action sends the 27 sum=1 quartets to a full 81-quartet closure, with 27 Z3 orbits of size 3.
- Each Z3 orbit contains exactly one sum_m_mod3 in {0,1,2}; the action cycles these sum classes.
- This Z3 action does not preserve the W33 rainbow line set: every sum=1 quartet maps to sum=2 then sum=0.
- See `transport_projective_z3_quartet_summary.md` and `transport_projective_z3_w33_line_shifted_quartets.csv`.

## 51) Transport Z3 shift predictions for top flux lines and node0 winners
- For each top flux line and the node0 winners (8,17,22), the transport-shifted sum=2 and sum=0 images have ridge-predicted mean_abs_delta values.
- A companion summary lists predicted response-law coefficients along the same Z3 shifts for quick sign/magnitude comparisons.
- See `transport_projective_z3_w33_line_shifted_summary.md` and `transport_projective_z3_w33_line_shifted_coeffs_summary.md`.

## 52) Z3 shifts flip response-law coefficient signs for many lines
- Across the 27 rainbow lines, predicted coefficient signs flip in ~12-16 cases per coefficient when shifting sum1 -> sum2 or sum1 -> sum0.
- Line 19 shows no predicted sign flips; line 17 flips all coefficients on both shifts, and line 8 flips several (delta, flux_coh, def_mass, mu, lambda).
- See `transport_projective_z3_coeff_sign_flips_summary.md` and `transport_projective_z3_coeff_sign_flips.csv`.

## 53) Predicted vs actual response coefficients (sum=1)
- The ridge-predicted coefficients correlate moderately with actual response-law fits across the 27 rainbow lines (r ~ 0.61-0.70 depending on coefficient).
- This suggests the quartet-only features capture a meaningful part of the response law but leave substantial line-level variation.
- See `quartet_ridge_response_coeffs_validation_summary.md` and `quartet_ridge_response_coeffs_validation.csv`.

## 54) Tomotope completion vs Z3-shifted predictions
- Tomotope lines with missing_sector=3 are very low in sum1 sensitivity but map to higher predicted sum2 sensitivity under the Z3 shift.
- Missing_sector=1 shows the opposite tendency (higher predicted sum2 than sum0), while missing_sector=0 is more balanced.
- See `tomotope_completion_z3_shift_summary.md` and `tomotope_completion_z3_shift_table.csv`.

## 55) D6 irrep decomposition of native C24 modes (rainbow lines)
- Using the D6 action on the 27 rainbow quartets, mode1 decomposes primarily into E1/E2 (about 0.29 + 0.35 of the norm), with a nontrivial B1 component (about 0.13).
- Mode2 spreads across A1/A2/B1/B2/E1/E2, while mode3 is dominated by E2 (about 0.46) and B2 (about 0.15).
- This follows the PySymmetry methodology: project onto irreps using character projectors for the D6 action.
- See `d6_irrep_decomposition_rainbow_mode1_summary.md` and `d6_irrep_decomposition_rainbow_modes_summary.md`.

## 56) D6 symmetry breaking in the rainbow covariance
- The rainbow-line covariance M = D^T D is not D6-equivariant: off-block mass is about 0.716 in a symmetry-adapted basis.
- The D6-averaged covariance M_sym is perfectly block-diagonal, but only about 0.37 of ||M|| lies in the symmetric part.
- This isolates a large D6-breaking component in the measurement response, likely tied to transport/decoration structure beyond incidence.
- See `d6_rainbow_covariance_block_summary.md` and `d6_rainbow_covariance_symmetrized_summary.md`.

## 57) Response-law coefficient covariance is also strongly D6-breaking
- Using the 5 response-law coefficients per line, the rainbow-line covariance shows even higher off-block mass (~0.770).
- Only about 0.327 of the coefficient covariance lies in the D6-symmetric component.
- See `d6_rainbow_response_coeffs_covariance_summary.md`.

## 58) D6 orbit residuals highlight symmetry-breaking lines
- Canonical mean_abs_delta residuals are dominated by lines 8, 19, 39 (positive) and lines 20, 28, 17 (negative).
- Native mean_abs_delta residuals are dominated by the same winners (8, 3, 14, 36, 7, 1) and large negative residuals on lines 30 and 4.
- Mode1 residuals are similarly concentrated on lines 8/3 (negative) and 36/7/1 (positive).
- See `d6_orbit_residuals_rainbow_metrics_summary.md` and `d6_orbit_residuals_rainbow_metrics.csv`.
