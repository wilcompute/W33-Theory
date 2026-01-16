# Affine involution vs tomotope15

Affine involution: a -> -a + (0,0,0,2) (mod 3).

- tomotope15 lines: 15
- mapped into tomotope15: 6
- intersection idx27: [11, 12, 16, 19, 23, 24]

m0 mapping counts (m0 -> mapped_m0):
- 0 -> 0: 3
- 1 -> 2: 3
- 2 -> 1: 9

missing_sector transitions (only for mapped lines):
- 2 -> 3: 3
- 3 -> 2: 3

completion_class transitions (only for mapped lines):
- sec2_m0 -> sec3_m0: 1
- sec2_m1 -> sec3_m2: 1
- sec2_m2 -> sec3_m1: 1
- sec3_m0 -> sec2_m0: 1
- sec3_m1 -> sec2_m2: 1
- sec3_m2 -> sec2_m1: 1

See `hyperplane_affine_involution_tomotope15_mapping.csv` for details.
