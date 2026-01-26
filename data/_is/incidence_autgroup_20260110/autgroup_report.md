# Automorphisms of the 12-point / 15-line tomotope-induced configuration (2026-01-10)

We form an incidence structure with:
- 12 points = the projective classes sec{s}_m{m}
- 15 lines = the 15 rainbow quartets produced by the tomotope triangles

## Degree spectrum (point → number of lines containing it)
- sec0_m2 has degree 9 (unique)
- sec0_m0 and sec0_m1 have degree 3 (a 2-point orbit)
- all remaining points have degree 5 (but split further by pairwise-incidence signature)

## Exact automorphism group size
Brute-force search over all degree- and signature-preserving permutations finds:

  |Aut| = 12

So this configuration has a nontrivial but small internal symmetry group.

## Useful generators (explicit point maps)
We provide three concrete automorphisms:
- g_cycle_m_on_1_2_3 : cycles m on sectors 1,2,3 while fixing sector 0 and the distinguished point sec0_m2.
- g_reflect : swaps certain m-labels and also swaps sec0_m0 <-> sec0_m1.
- g_kernel_swap_1_2 : an involution that intertwines sectors 1 and 2 with a nontrivial m-scramble, while fixing sector 0 and sector 3.

Files:
- incidence_12points_15lines.csv
- automorphism_group_order12_point_maps.csv
- automorphism_generators_examples.csv
