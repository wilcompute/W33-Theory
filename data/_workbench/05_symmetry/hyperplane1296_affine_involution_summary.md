# Hyperplane 1296 closure: affine inversion generator

The D6/D8 generators in `generators_on_27.txt` produce a 648-element subgroup.
Adding the affine involution

    a -> -a + (0,0,0,2)  (mod 3)

expands the closure to 1296 elements and matches the saved order distribution.
On the hyperplane, the same action admits a linear representative with c=0 and det(A)=2 (see `hyperplane_affine_involution_a_map_summary.md`).

Sizes and order distributions:

- base size: 648 order_dist={1: 1, 2: 45, 3: 98, 4: 162, 6: 198, 9: 144}
- full size: 1296 order_dist={1: 1, 2: 135, 3: 98, 4: 216, 6: 594, 9: 144, 12: 108}

Permutation cycles for the involution are in `hyperplane_affine_involution_c0002_cycles.txt`.
Index mapping is in `hyperplane_affine_involution_c0002_map.csv`.

Interpretation on m-coordinates (m0=a0, m1=a0+a1, m2=a0+a2, m3=a0+a1+a2+a3):
- m0 -> -m0, m1 -> -m1, m2 -> -m2, m3 -> 2 - m3 (mod 3).
- On projective classes: sectors 0/1/2 swap m1<->m2 with m0 fixed; sector 3 swaps m0<->m2 with m1 fixed.
- Conjugation property: inv_c T_t inv_c = T_{-t} for all translations t in the hyperplane.
