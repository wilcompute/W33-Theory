# Transport Z2 invariants vs hyperplane level sets (orbit0 edges)

sum_m_mod3 computed from (img_sec0_m0,img_sec1_m0,img_sec2_m0,img_sec3_m0).

## Counts by edge_elem_2T
- (0 1 2): sum=0 -> 0, sum=1 -> 31, sum=2 -> 0
- (0 2 1): sum=0 -> 0, sum=1 -> 0, sum=2 -> 27
- e: sum=0 -> 63, sum=1 -> 0, sum=2 -> 0
- e*: sum=0 -> 4, sum=1 -> 0, sum=2 -> 0

## Counts by defect bit (is_defect = edge_elem_2T == e*)
- is_defect=0: sum=0 -> 63, sum=1 -> 31, sum=2 -> 27
- is_defect=1: sum=0 -> 4, sum=1 -> 0, sum=2 -> 0

## Counts by hyperplane shift bit (is_shift = sum_m_mod3 != 0)
- is_shift=0: sum=0 -> 67, sum=1 -> 0, sum=2 -> 0
- is_shift=1: sum=0 -> 0, sum=1 -> 31, sum=2 -> 27

## sigma_product by sum_m_mod3
- sum=0: n=67, mean_sigma=1.000, frac_sigma_pos=1.000
- sum=1: n=31, mean_sigma=-1.000, frac_sigma_pos=0.000
- sum=2: n=27, mean_sigma=-1.000, frac_sigma_pos=0.000
