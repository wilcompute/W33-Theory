# N12 extended summary (new imports)

## N12 index (59 manifolds)
- aut_order_dist: 1:39, 2:9, 4:7, 6:2, 12:1, 3:1
- dual_girth_min: 6
- dual_girth_max: 6
- dual_diameter_min: 5
- dual_diameter_max: 6

## N12_58 missing triangle orbits
- automorphism_group_order: 12
- missing_triangles_count: 176
- missing_triangle_orbit_count: 16
- missing_triangle_orbit_size_counts: 4:2, 12:14

## N12_58 orbit cup analysis
- H1_dim_mod2: 12
- missing_triangle_orbits_count: 16
- orbit_size_histogram: 12:14, 4:2
- h1_span_dim_histogram: 3:2, 6:6, 8:5, 9:3
- h1_unique_count_histogram: 12:10, 4:2, 6:4

## Packet matching phase analysis (orbits 0 and 13)
- summary: In each notable orbit, the 12 packet H1 classes (mod2 supports in symplectic basis) span a 6D symplectic subspace; the mod-2 commuting graph has exactly 59 perfect matchings.

### Orbit 0
- orbit_index: 0
- orbit_size: 12
- perfect_matchings: 59
- perfect_matchings_count_commute_mod2: 59
- matchings_orbit_size_histogram_under_A4: 12:51, 4:2, 6:6
- phase_signature_histogram_mod8: [0, 0, 0, 0, 0, 2]:5, [0, 0, 0, 2, 6, 6]:10, [0, 0, 0, 0, 2, 6]:22, [0, 0, 0, 0, 0, 6]:12, [0, 0, 0, 0, 6, 6]:6, [0, 0, 0, 0, 0, 0]:4

### Orbit 13
- orbit_index: 13
- orbit_size: 12
- perfect_matchings: 59
- perfect_matchings_count_commute_mod2: 59
- matchings_orbit_size_histogram_under_A4: 12:58, 6:1
- phase_signature_histogram_mod8: [0, 0, 0, 0, 0, 2]:5, [0, 0, 0, 2, 6, 6]:10, [0, 0, 0, 0, 2, 6]:22, [0, 0, 0, 0, 0, 6]:12, [0, 0, 0, 0, 6, 6]:6, [0, 0, 0, 0, 0, 0]:4

## A4 Sp12 representation
- group_isomorphic_to: A4
- order_distribution: 1:1, 2:3, 3:8
- irrep_decomposition_over_C: 4 copies of the 3-dimensional irreducible (no 1D pieces) inferred from traces: tr(2)= -4, tr(3)=0
- involution_eigenvalue_counts: each involution has eigenvalues +1 (mult 4) and -1 (mult 8) in this symplectic basis

## A4 clock phase bundle (N12_58)
- tau_definition: tau := (-I) * g3 where g3 is an order-3 element in the induced Sp(12,Z) representation; tau has order 6 (binary tetrahedral extension).
- tau_order_verified: 6
- Sp12_representation_elements: 12
- missing_triangle_orbits_size4: 2
- intersection_rank6_graph_isolated_orbits: 4

## Orientable symplectic meta
- Symplectic bases for orientable N12_1..N12_29 (genus 6). Basis given as integer 1-cochains on oriented edges of K12 (66 edges). J is in interleaved order (e1,f1,e2,f2,...). Electric coordinates can be taken as e1..e6 (indices 0,2,4,6,8,10) and magnetic as f1..f6 (indices 1,3,5,7,9,11).
